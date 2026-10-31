"""Shared helpers for the test-suite: byte-level vocabulary and a deterministic driver."""

from typing import Any, Dict, List

import numpy as np

from src.fsm import JSONFunctionFSM
from src.vocabulary import Vocabulary, _BYTE_DECODER

_BYTE_TO_CHAR = {byte: char for char, byte in _BYTE_DECODER.items()}


def raw_token(text: str) -> str:
    """Encode plain text the way vocab.json stores it (byte-level encoding)."""
    return "".join(_BYTE_TO_CHAR[byte] for byte in text.encode("utf-8"))


FUNCTIONS: List[Dict[str, Any]] = [
    {
        "name": "fn_add_numbers",
        "description": "add two numbers",
        "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
    },
    {
        "name": "fn_echo",
        "description": "echo a string",
        "parameters": {"text": {"type": "string"}},
    },
    {
        "name": "fn_opt",
        "description": "one required and one optional parameter",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "string"}},
            "required": ["a"],
        },
    },
    {
        "name": "fn_all_optional",
        "description": "every parameter is optional",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}},
            "required": [],
        },
    },
]

# One token per printable ASCII character (plus é) guarantees that every literal
# and every value used below is representable. The multi-character tokens mimic
# BPE merges and exercise the "token spans several characters" logic.
TOKENS: List[str] = list(
    dict.fromkeys(
        [chr(code) for code in range(32, 127)]
        + ["é"]
        + [
            '{"name": "',
            '", "parameters":',
            " {",
            "}}",
            ' "',
            '": ',
            '"',
            ",",
            " ",
            "true",
            "false",
            "12",
            "-1.5",
            "42",
            'fn_add_numbers"',
            'fn_echo"',
            'fn_opt"',
            'fn_all_optional"',
            ' "a": ',
            ' "a": "',
            ' "b": ',
            ' "b": "',
            ' "text": "',
            'fn\\"q"',
            '",',
            '"}',
            '"}}',
        ]
    )
)


def drive(
    fsm: JSONFunctionFSM,
    vocab: Vocabulary,
    target: str,
    max_steps: int = 2000,
) -> str:
    """Write `target` token by token, letting `select_token` pick each model token.

    Forced tokens are taken directly from the FSM. When the model has a real
    choice, the allowed token whose text is the longest prefix of the remaining
    target is given the highest logit, so `select_token` must return it.
    """
    text = ""
    for _ in range(max_steps):
        if fsm.is_finished():
            return text
        token = fsm.forced_token()
        if token is None:
            remaining = target[len(text):]
            candidates = []
            for token_id in fsm.get_allowed_token_ids():
                piece = vocab.get_clean_text(token_id)
                if piece and remaining.startswith(piece):
                    candidates.append((len(piece), token_id))
            assert candidates, (
                f"target unreachable in {fsm.current_state.name} after {text!r}"
            )
            token = max(candidates)[1]
            logits = np.full(len(vocab.token_to_id), -10.0, dtype=np.float32)
            logits[token] = 10.0
            selected = fsm.select_token(logits)
            assert selected == token, (
                f"select_token returned {selected} instead of {token}"
            )
            token = selected
        text += vocab.get_clean_text(token)
        fsm.advance(token)
    raise AssertionError(f"generation did not finish after {max_steps} steps: {text!r}")
