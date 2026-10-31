"""Module for finite state machine (FSM) constrained JSON decoding with strict Pydantic validation."""

import json
import re
import sys
import time
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

import numpy as np

from src.logit_masker import LogitMasker, StaticTokenSets, select_best_token
from src.models import FunctionSchema
from src.vocabulary import Vocabulary


class JSONState(Enum):
    """FSM states representing structural JSON milestones for Function Calling."""
    START = auto()
    NAME_KEY = auto()
    FUNCTION_NAME = auto()
    PARAMS_KEY = auto()
    PARAMS_OPEN = auto()
    PARAM_NAME = auto()
    PARAM_COLON = auto()
    PARAM_VALUE = auto()
    PARAM_COMMA = auto()
    CLOSE_PARAMS = auto()
    CLOSE_ROOT = auto()
    END = auto()


# Characters allowed inside a JSON number.
_NUMBER_CHARS = frozenset("0123456789.-")
_ESCAPABLE = frozenset('"\\/bfnrt')


def _scan_string_token(text: str, pending: bool) -> Optional[bool]:
    """Check a token inside a JSON string; return the new 'escape pending' flag or None if invalid.

    A backslash must be followed by one of the JSON escape characters
    (possibly at the start of the next token, hence the `pending` flag).
    """
    i = 0
    if pending:
        if not text or text[0] not in _ESCAPABLE:
            return None
        i = 1
    while i < len(text):
        char = text[i]
        if char == "\\":
            if i + 1 == len(text):
                return True
            if text[i + 1] not in _ESCAPABLE:
                return None
            i += 2
            continue
        if char == '"' or ord(char) < 32 or char == "\ufffd":
            return None
        i += 1
    return False


_INT_PREFIX = re.compile(r"^-?(?:0|[1-9][0-9]*)?$")
_NUM_PREFIX = re.compile(r"^-?(?:(?:0|[1-9][0-9]*)(?:\.[0-9]*)?)?$")
_INT_DONE = re.compile(r"^-?(?:0|[1-9][0-9]*)$")
_NUM_DONE = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$")
_MISSING = object()
# A string value longer than this many tokens is forced to close (prevents endless generation).
MAX_STRING_TOKENS = 100
# Same idea for numbers: past this many characters only a terminator is accepted.
MAX_NUMBER_CHARS = 20


class JSONFunctionFSM:
    """Finite State Machine enforcing 100% valid JSON syntax and strict Pydantic schema compliance.

    The generated text always has the shape::

        {"name": "<function>", "parameters": {"<param>": <value>, ...}}

    A BPE token can span several characters, so every state is a small
    "literal" (or a value) that may be emitted by one or several tokens: a token
    is allowed only if its text is a prefix of what is still expected.

    Features:
    - Cached masks: every distinct situation is computed once, then reused.
    - Type enforcement based on Pydantic field definitions (number, integer, string, boolean).
    - Required field validation: the JSON cannot be closed until all required parameters are emitted.
    - Forced tokens: when only one text is possible, no LLM call is needed.
    """

    def __init__(self, vocab: Vocabulary, functions_def: Sequence[Union[Dict[str, Any], FunctionSchema]]) -> None:
        """Initialize the FSM with Pydantic model schemas and pre-compute allowed token IDs.

        Args:
            vocab: Instantiated Vocabulary object.
            functions_def: List of function definitions (dicts or FunctionSchema models).
        """
        self.vocab: Vocabulary = vocab
        self.masker: LogitMasker = LogitMasker(
            vocab_size=max(vocab.token_to_id.values()) + 1
        )
        self.token_sets: StaticTokenSets = StaticTokenSets(vocab)

        # Parse and store Pydantic validated schemas per function name
        self.schema_by_name: Dict[str, Dict[str, Any]] = {}
        for fn in functions_def:
            if isinstance(fn, FunctionSchema):
                schema_obj = fn
            else:
                schema_obj = FunctionSchema.model_validate(dict(fn))

            prop_types: Dict[str, str] = {
                name: prop.type
                for name, prop in schema_obj.parameters.properties.items()
            }
            # Order is kept so the FSM can write required parameters itself,
            # instead of spending a model call to let it pick a fixed name.
            required_order: List[str] = []
            for name in schema_obj.parameters.required:
                if name not in required_order:
                    required_order.append(name)

            self.schema_by_name[schema_obj.name] = {
                "properties": prop_types,
                "required": set(required_order),
                "required_order": required_order,
                "all_params": set(prop_types.keys()),
            }

        self.func_names: Set[str] = set(self.schema_by_name.keys())
        # JSON-escaped names: a name containing a quote or a backslash must not
        # break the JSON that the FSM is supposed to guarantee.
        self._func_literals: Dict[str, str] = {
            json.dumps(name, ensure_ascii=True)[1:]: name
            for name in sorted(self.func_names)
        }

        # Tokens indexed by first character (fast prefix lookups), built once.
        self._by_first: Dict[str, List[Tuple[int, str]]] = {}
        for tid, text in vocab.id_to_token.items():
            if text and "\ufffd" not in text:
                self._by_first.setdefault(text[0], []).append((tid, text))
        self._numeric_tokens: List[Tuple[int, str]] = [
            (tid, vocab.get_clean_text(tid)) for tid in self.token_sets.digits
        ]
        self._string_ids: Dict[bool, Set[int]] = {}
        self._quote_ids: Optional[Set[int]] = None
        self._closing_combo_cache: Dict[Tuple[bool, bool], Set[int]] = {}
        self._allowed_cache: Dict[str, Set[int]] = {}
        self._forced_cache: Dict[str, Optional[int]] = {}

        # State tracking variables
        self.current_state: JSONState = JSONState.START
        self.selected_function: str | None = None
        self.current_param: str | None = None
        self.generated_params: Set[str] = set()
        self.generated_tokens: List[int] = []
        self._lit_buf: str = ""
        self._value_buf: str = ""
        self._escape_pending: bool = False
        self._value_tokens: int = 0
        self.debug: bool = False

    def reset(self) -> None:
        """Reset the FSM state for a new generation session."""
        self.current_state = JSONState.START
        self.selected_function = None
        self.current_param = None
        self.generated_params.clear()
        self.generated_tokens.clear()
        self._lit_buf = ""
        self._value_buf = ""
        self._escape_pending = False
        self._value_tokens = 0

    def required_params_satisfied(self) -> bool:
        """Check if all required Pydantic fields for the selected function have been generated.

        Returns:
            True if all required parameters are present in generated_params, False otherwise.
        """
        if self.selected_function is None or self.selected_function not in self.schema_by_name:
            return True
        required_set = self.schema_by_name[self.selected_function]["required"]
        return bool(required_set.issubset(self.generated_params))

    # ------------------------------------------------------------------ helpers
    def _dbg(self, message: str) -> None:
        """Print a debug line on stderr when debug mode is on."""
        if self.debug:
            print(f"      [fsm] {message}", file=sys.stderr, flush=True)

    def _enter(self, state: JSONState) -> None:
        """Switch to a new state and clear the per-state buffers."""
        self._dbg(
            f"{self.current_state.name} -> {state.name}"
            f" (function={self.selected_function}, param={self.current_param},"
            f" emitted={sorted(self.generated_params)})"
        )
        self.current_state = state
        self._lit_buf = ""
        self._value_buf = ""
        self._escape_pending = False
        self._value_tokens = 0

    def _value_kind(self) -> str:
        """Return 'number', 'integer', 'boolean' or 'string' for the current parameter."""
        raw = "string"
        if self.selected_function is not None and self.current_param is not None:
            props = self.schema_by_name[self.selected_function]["properties"]
            raw = (props.get(self.current_param) or "string").lower()
        if raw in ("number", "float"):
            return "number"
        if raw in ("integer", "int"):
            return "integer"
        if raw in ("boolean", "bool"):
            return "boolean"
        return "string"

    def _comma_options(self) -> Dict[str, Any]:
        """Texts allowed after a value: ',' (more parameters) and/or '}}' (close)."""
        options: Dict[str, Any] = {}
        if self.selected_function is not None:
            schema = self.schema_by_name[self.selected_function]
            if schema["all_params"] - self.generated_params:
                options[","] = None
            if self.required_params_satisfied():
                options["}}"] = None
        return options

    def _literal_options(self) -> Dict[str, Any]:
        """Full texts the current state may complete, mapped to a payload (name or None)."""
        state = self.current_state
        if state == JSONState.START:
            return {'{"name": "': None}
        if state == JSONState.FUNCTION_NAME:
            return dict(self._func_literals)
        if state == JSONState.PARAMS_KEY:
            return {', "parameters":': None}
        if state == JSONState.PARAMS_OPEN:
            return {" {": None}
        if state == JSONState.PARAM_NAME:
            assert self.selected_function is not None
            schema = self.schema_by_name[self.selected_function]
            # Required parameters are written in schema order without asking the
            # model: their names are fixed, only their values are a real choice.
            remaining_required = [
                name for name in schema["required_order"]
                if name not in self.generated_params
            ]
            if remaining_required:
                candidates = remaining_required[:1]
            else:
                candidates = sorted(
                    schema["all_params"] - self.generated_params
                )
            if not candidates:
                return {"}}": None}
            lead = " " if self.generated_params else ""
            options: Dict[str, Any] = {}
            for param in candidates:
                kind = (schema["properties"].get(param) or "string").lower()
                is_string = kind not in ("number", "float", "integer", "int", "boolean", "bool")
                escaped = json.dumps(param, ensure_ascii=True)
                key = f'{lead}{escaped}: ' + ('"' if is_string else "")
                options[key] = param
            # A function whose parameters are all optional may be called with none:
            # let the model choose between the first parameter and the empty object.
            if not self.generated_params and self.required_params_satisfied():
                options["}}"] = None
            return options
        if state == JSONState.PARAM_VALUE and self._value_kind() == "boolean":
            return {"true": None, "false": None}
        if state == JSONState.PARAM_COMMA:
            return self._comma_options()
        return {}

    def _literal_remaining(self) -> List[str]:
        """Texts still to emit, given what was already written in the current literal."""
        buf = self._lit_buf
        return sorted(
            {opt[len(buf):] for opt in self._literal_options() if opt.startswith(buf)}
        )

    def _tokens_prefixing(self, remaining: List[str]) -> Set[int]:
        """Token IDs whose text is a non-empty prefix of one of the remaining texts."""
        allowed: Set[int] = set()
        for text_left in remaining:
            if not text_left:
                continue
            for tid, tok in self._by_first.get(text_left[0], ()):
                if text_left.startswith(tok):
                    allowed.add(tid)
        return allowed

    def _closing_quote_ids(self) -> Set[int]:
        """Token IDs whose full text is the closing quote (computed once)."""
        if self._quote_ids is None:
            self._quote_ids = set(self.vocab.get_token_ids_matching({'"'}))
        return self._quote_ids

    def _closing_combo_ids(self) -> Set[int]:
        """Tokens that close the string *and* start the following JSON syntax.

        Qwen's vocabulary contains tokens such as ``",`` and ``"}``.  Allowing
        them lets the model close a value with its natural token instead of
        being forced to emit a lone quote and then continue writing text inside
        the string until the 100-token cap.
        """
        options = self._comma_options()
        key = ("," in options, "}}" in options)
        cached = self._closing_combo_cache.get(key)
        if cached is None:
            cached = set()
            for tid, text in self.vocab.id_to_token.items():
                if len(text) < 2 or not text.startswith('"'):
                    continue
                remainder = text[1:]
                if any(option.startswith(remainder) for option in options):
                    cached.add(tid)
            self._closing_combo_cache[key] = cached
        return cached

    def _string_token_ids(self) -> Set[int]:
        """Token IDs usable inside a JSON string (valid escapes only) + the closing quote."""
        pending = self._escape_pending
        if pending not in self._string_ids:
            ids = {
                tid for tid, text in self.vocab.id_to_token.items()
                if text and _scan_string_token(text, pending) is not None
            }
            if not pending:
                ids.update(self._closing_quote_ids())
            self._string_ids[pending] = ids
        return self._string_ids[pending]

    def _number_class(self) -> str:
        """Coarse class of the number written so far (fully determines the allowed tokens)."""
        buf = self._value_buf
        if buf == "":
            return "E"
        if buf == "-":
            return "M"
        if re.fullmatch(r"-?0", buf):
            return "Z"
        if re.fullmatch(r"-?[1-9][0-9]*", buf):
            return "I"
        if buf.endswith("."):
            return "D"
        return "F"

    def _number_done(self) -> bool:
        pattern = _INT_DONE if self._value_kind() == "integer" else _NUM_DONE
        return bool(pattern.match(self._value_buf))

    def _state_key(self) -> str:
        """Unique key of the current allowed-token situation (used by the mask caches)."""
        if self.current_state == JSONState.PARAM_VALUE:
            kind = self._value_kind()
            if kind == "string":
                capped = self._value_tokens >= MAX_STRING_TOKENS
                enders = "\x1f".join(sorted(self._comma_options()))
                return (
                    f"PARAM_VALUE|string|{self._escape_pending}|{capped}|{enders}"
                )
            if kind in ("number", "integer"):
                enders = ""
                if self._number_done():
                    enders = "\x1f".join(sorted(self._comma_options()))
                capped = len(self._value_buf) >= MAX_NUMBER_CHARS
                return f"PARAM_VALUE|{kind}|{self._number_class()}|{enders}|{capped}"
        remaining = "\x1f".join(self._literal_remaining())
        return f"{self.current_state.name}|{remaining}"

    def _compute_allowed(self) -> Set[int]:
        if self.current_state == JSONState.PARAM_VALUE:
            kind = self._value_kind()
            if kind == "string":
                if self._value_tokens >= MAX_STRING_TOKENS and not self._escape_pending:
                    return (
                        set(self._closing_quote_ids())
                        | self._closing_combo_ids()
                    )  # must close now
                allowed = set(self._string_token_ids())
                if not self._escape_pending:
                    allowed |= self._closing_combo_ids()
                return allowed
            if kind in ("number", "integer"):
                pattern = _INT_PREFIX if kind == "integer" else _NUM_PREFIX
                allowed = {
                    tid for tid, text in self._numeric_tokens
                    if pattern.match(self._value_buf + text)
                }
                if self._number_done():
                    enders = self._tokens_prefixing(sorted(self._comma_options()))
                    if len(self._value_buf) >= MAX_NUMBER_CHARS:
                        return enders
                    allowed |= enders
                return allowed
        return self._tokens_prefixing(self._literal_remaining())

    # ------------------------------------------------------------------- public
    def _allowed_for_key(self, key: str) -> Set[int]:
        """Allowed token IDs for a state key, computed and cached once."""
        allowed = self._allowed_cache.get(key)
        if allowed is None:
            start = time.perf_counter()
            allowed = self._compute_allowed()
            self._allowed_cache[key] = allowed
            self._dbg(
                f"new mask key={key!r}: {len(allowed)} allowed tokens"
                f" ({time.perf_counter() - start:.3f}s)"
            )
        return allowed

    def get_allowed_token_ids(self) -> Set[int]:
        """Return the set of allowed token IDs based on FSM state and Pydantic constraints.

        Returns:
            Set of permitted token IDs (computed once per situation, then cached).
        """
        if self.current_state == JSONState.END:
            return set()
        return self._allowed_for_key(self._state_key())

    def _longest_prefix_token(self, text_left: str) -> Optional[int]:
        """Longest vocabulary token that is a prefix of `text_left` (cached)."""
        if text_left not in self._forced_cache:
            best: Optional[Tuple[int, int]] = None
            for tid, tok in self._by_first.get(text_left[0], ()):
                if text_left.startswith(tok) and (best is None or len(tok) > best[0]):
                    best = (len(tok), tid)
            self._forced_cache[text_left] = best[1] if best else None
        return self._forced_cache[text_left]

    def forced_token(self) -> Optional[int]:
        """Return the token to emit when only one text is possible (no LLM call needed).

        Returns:
            The longest token that fits the single expected text, or None if the
            model has a real choice to make.
        """
        if self.current_state == JSONState.END:
            return None
        if self.current_state == JSONState.PARAM_VALUE:
            # Inside a string or a number the token is the value itself: the
            # model must choose it unless the FSM is left with a single option.
            if self._value_kind() != "boolean":
                allowed = self._allowed_for_key(self._state_key())
                return next(iter(allowed)) if len(allowed) == 1 else None
        remaining = self._literal_remaining()
        if len(remaining) == 1 and remaining[0]:
            return self._longest_prefix_token(remaining[0])
        allowed = self._allowed_for_key(self._state_key())
        return next(iter(allowed)) if len(allowed) == 1 else None

    def select_token(self, logits: np.ndarray) -> int:
        """Filter logits using cached state mask and select the optimal token ID.

        Args:
            logits: Raw logit distribution array from model.

        Returns:
            Selected token ID.
        """
        key = self._state_key()
        allowed_ids = self._allowed_for_key(key)
        if not allowed_ids:
            self._dbg(f"EMPTY allowed set, key={key!r}")
            raise RuntimeError(f"No token allowed in state {self.current_state.name}")
        mask = self.masker.get_mask(key, allowed_ids)
        return select_best_token(logits, mask, allowed_ids)

    def advance(self, token_id: int) -> None:
        """Enumération et mise à jour de l'état interne de la FSM.

        Args:
            token_id: Identifiant du token choisi.
        """
        self.generated_tokens.append(token_id)
        text = self.vocab.get_clean_text(token_id)

        if self.current_state == JSONState.END:
            return

        if self.current_state == JSONState.PARAM_VALUE:
            kind = self._value_kind()
            if kind == "string":
                if text.startswith('"') and not self._escape_pending:
                    # The token may be the lone quote, or a natural Qwen token
                    # such as '",' / '"}' / '"}}' that closes the value and
                    # already contains the start of the following JSON.
                    remainder = text[1:]
                    self._enter(JSONState.PARAM_COMMA)
                    if remainder:
                        self._consume_literal(remainder)
                else:
                    self._value_buf += text
                    self._value_tokens += 1
                    self._escape_pending = bool(
                        _scan_string_token(text, self._escape_pending)
                    )
                return
            if kind in ("number", "integer"):
                if text and all(c in _NUMBER_CHARS for c in text):
                    self._value_buf += text
                    return
                # Any other token ends the number: it belongs to the "after value" literal.
                self._enter(JSONState.PARAM_COMMA)

        self._lit_buf += text
        payload = self._literal_options().get(self._lit_buf, _MISSING)
        if payload is _MISSING:
            return  # literal not finished yet (multi-token literal)
        self._on_literal_complete(payload)

    def _consume_literal(self, text: str) -> None:
        """Write `text` in the current literal state (used after a closing combo)."""
        self._lit_buf += text
        payload = self._literal_options().get(self._lit_buf, _MISSING)
        if payload is not _MISSING:
            self._on_literal_complete(payload)

    def _on_literal_complete(self, payload: Any) -> None:
        """Transition once the literal of the current state has been fully written."""
        state = self.current_state
        if state == JSONState.START:
            self._enter(JSONState.FUNCTION_NAME)
        elif state == JSONState.FUNCTION_NAME:
            self.selected_function = payload
            self._enter(JSONState.PARAMS_KEY)
        elif state == JSONState.PARAMS_KEY:
            self._enter(JSONState.PARAMS_OPEN)
        elif state == JSONState.PARAMS_OPEN:
            self._enter(JSONState.PARAM_NAME)
        elif state == JSONState.PARAM_NAME:
            if payload is None:
                self._enter(JSONState.END)
            else:
                self.current_param = payload
                self.generated_params.add(payload)
                self._enter(JSONState.PARAM_VALUE)
        elif state == JSONState.PARAM_VALUE:  # boolean literal
            self._enter(JSONState.PARAM_COMMA)
        elif state == JSONState.PARAM_COMMA:
            if self._lit_buf == ",":
                self._enter(JSONState.PARAM_NAME)
            else:
                self._enter(JSONState.END)

    def is_finished(self) -> bool:
        """Check whether the FSM has reached the terminal END state."""
        return self.current_state == JSONState.END
