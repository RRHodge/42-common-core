"""Call Me Maybe: function calling with FSM-constrained decoding.

Run from the project root with `python -m src` (or `uv run python -m src`).
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from src.fsm import JSONFunctionFSM, MAX_NUMBER_CHARS, MAX_STRING_TOKENS
from src.incremental import IncrementalLogits
from src.loaders import (
    load_function_definitions,
    load_test_prompts,
    save_function_results,
)
from src.models import FunctionResult, FunctionSchema
from src.prompts import PromptBuilder
from src.vocabulary import TokenVocabulary

if TYPE_CHECKING:
    from llm_sdk import Small_LLM_Model

MAX_TOKENS = 200


def max_generation_steps(functions: List[FunctionSchema]) -> int:
    """Upper bound on the number of emitted tokens for one prompt.

    A fixed 200-token budget is not enough when a function has several string
    parameters: the FSM caps each string at MAX_STRING_TOKENS tokens, so the
    budget must grow with the number of parameters. The JSON syntax alone is
    also counted (one token can always be as small as one character).
    """
    max_params = 0
    literal_chars = 64
    for function in functions:
        params = set(function.parameters.properties) | set(function.parameters.required)
        max_params = max(max_params, len(params))
        # Names are JSON-escaped in the generated text, so measure the escaped
        # form: every character may need its own token.
        escaped_name = len(json.dumps(function.name, ensure_ascii=True))
        escaped_params = sum(
            len(json.dumps(name, ensure_ascii=True)) + 4 for name in params
        )
        literal_chars = max(literal_chars, 64 + escaped_name + escaped_params)
    # Each value costs at most MAX_STRING_TOKENS tokens (numbers are shorter).
    per_value = MAX_STRING_TOKENS + MAX_NUMBER_CHARS + 8
    return max(MAX_TOKENS, literal_chars + per_value * max_params)


def parse_arguments(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Call Me Maybe: LLM function calling with constrained decoding."
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        help="JSON file with the available function schemas.",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        help="JSON file with the test prompts.",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
        help="Where to write the results.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print timings, FSM transitions and every generated token on stderr.",
    )
    return parser.parse_args(argv)


def resolve_path(path: str, fallbacks: List[str]) -> Path:
    """Return the requested path, or the first existing fallback path."""
    for candidate in [path, *fallbacks]:
        if Path(candidate).exists():
            return Path(candidate)
    raise FileNotFoundError(f"File not found: {path}")


def dbg(enabled: bool, message: str) -> None:
    """Print a debug line on stderr when debug mode is on."""
    if enabled:
        print(f"  [debug] {message}", file=sys.stderr, flush=True)


def to_token_list(encoded: Any) -> List[int]:
    """Convert the output of `llm.encode` (list or 1D/2D tensor) to a list of ids."""
    ids = encoded.tolist() if hasattr(encoded, "tolist") else list(encoded)
    if ids and isinstance(ids[0], list):
        ids = ids[0]
    return [int(i) for i in ids]


_SIMPLE_REGEX_ATOM = re.compile(
    r"^(?:\[[^\]]+\]|\\[dDwWsS])(?:[+*?]|\{\d+(?:,\d*)?\})?$"
)


def _simplify_regex(value: str) -> str:
    """Remove small-model artifacts from a regex value.

    The model often wraps a simple pattern in a redundant capturing group
    (``([0-9]+)``) or appends a whitespace matcher (``([0-9]+)\\s``).  A
    capturing group is only removed when it contains a single class/escape atom,
    so patterns with backreferences or real structure are left untouched.
    """
    value = value.strip()
    for suffix in ("\\s*", "\\s+", "\\s"):
        if value.endswith(suffix):
            prefix = value[: -len(suffix)]
            if (
                prefix.startswith("(")
                and prefix.endswith(")")
                and _SIMPLE_REGEX_ATOM.match(prefix[1:-1])
            ):
                value = prefix
            break
    if value.startswith("(") and value.endswith(")"):
        inner = value[1:-1]
        if _SIMPLE_REGEX_ATOM.match(inner):
            value = inner
    return value


def _normalize_string_parameter(name: str, value: str) -> str:
    """Normalize the two structured string parameters produced by the model."""
    lowered = name.lower()
    if "regex" in lowered:
        return _simplify_regex(value)
    if "replacement" in lowered:
        return value.strip()
    return value


def coerce_parameters(
    parameters: Dict[str, Any], function: Optional[FunctionSchema]
) -> Dict[str, Any]:
    """Cast the generated values to the declared types (e.g. 2 -> 2.0 for a 'number')."""
    if function is None:
        return parameters
    props = function.parameters.properties
    result: Dict[str, Any] = {}
    for key, value in parameters.items():
        if isinstance(value, str):
            value = _normalize_string_parameter(key, value)
        declared = props[key].type.lower() if key in props else ""
        is_num = isinstance(value, (int, float)) and not isinstance(value, bool)
        if declared in ("number", "float") and is_num:
            value = float(value)
        elif declared in ("integer", "int") and is_num:
            value = int(value)
        result[key] = value
    return result


def generate_constrained(
    llm: "Small_LLM_Model",
    prompt_text: str,
    functions: List[FunctionSchema],
    vocab: TokenVocabulary,
    builder: PromptBuilder,
    fsm: Optional[JSONFunctionFSM] = None,
    stats: Optional[Dict[str, int]] = None,
    system_prompt: Optional[str] = None,
) -> FunctionResult:
    """Generate the function call for one prompt, token by token, under the FSM.

    Pass an existing `fsm` to reuse its pre-computed token tables between prompts
    and `system_prompt` to avoid rebuilding the tool list for every prompt.
    """
    chat_prompt = builder.build_chat_prompt(prompt_text, functions, system_prompt)

    if fsm is None:
        fsm = JSONFunctionFSM(vocab=vocab, functions_def=functions)
    fsm.reset()

    debug = fsm.debug
    prompt_ids = to_token_list(llm.encode(chat_prompt))
    if debug:
        dbg(True, f"prompt: {len(prompt_ids)} tokens")

    # Most tokens are forced (JSON syntax, required parameter names). They are
    # accumulated and forwarded in one batch through the KV cache, so the model
    # only runs a forward pass for a real decision and never re-reads the full
    # prefix unless the SDK falls back to its public API.
    provider = IncrementalLogits(llm, prompt_ids)
    pending: List[int] = []

    max_steps = max_generation_steps(functions)
    for step in range(max_steps):
        if fsm.is_finished():
            break
        state = fsm.current_state.name
        # Only one possible text (fixed JSON syntax, a required parameter name,
        # a single function...): skip the model call.
        token_id = fsm.forced_token()
        if token_id is None:
            # Fail before paying for a forward pass that cannot produce a token.
            if not fsm.get_allowed_token_ids():
                raise RuntimeError(f"No token allowed in state {state}")
            if stats is not None:
                stats["model_calls"] = stats.get("model_calls", 0) + 1
            t0 = time.perf_counter()
            logits = provider.feed(pending)
            pending.clear()
            t1 = time.perf_counter()
            token_id = fsm.select_token(logits)
            kind = f"model {t1 - t0:.2f}s + mask {time.perf_counter() - t1:.3f}s"
        else:
            if stats is not None:
                stats["forced"] = stats.get("forced", 0) + 1
            kind = "forced"
        if debug:
            dbg(
                True,
                f"step {step:3d} [{state}] {kind} -> id={token_id} "
                f"{vocab.get_clean_text(token_id)!r}",
            )
        pending.append(token_id)
        fsm.advance(token_id)

    if not fsm.is_finished():
        if debug:
            partial = "".join(
                vocab.get_clean_text(tid) for tid in fsm.generated_tokens
            )
            dbg(
                True,
                f"STOPPED in state {fsm.current_state.name}, partial text: {partial}",
            )
        raise RuntimeError(
            f"No complete JSON after {max_steps} tokens "
            f"(state {fsm.current_state.name})"
        )

    generated_text = "".join(
        vocab.get_clean_text(tid) for tid in fsm.generated_tokens
    )
    if debug:
        dbg(True, f"generated text: {generated_text}")

    parsed = json.loads(generated_text)
    function = next((f for f in functions if f.name == parsed["name"]), None)
    return FunctionResult(
        prompt=prompt_text,
        name=parsed["name"],
        parameters=coerce_parameters(parsed["parameters"], function),
    )


def main(argv: Optional[List[str]] = None) -> int:
    """Run the whole pipeline and return the process exit code."""
    args = parse_arguments(argv)

    try:
        funcs_path = resolve_path(
            args.functions_definition,
            ["data/functions_definition.json", "functions_definition.json"],
        )
        input_path = resolve_path(
            args.input,
            ["data/function_calling_tests.json", "function_calling_tests.json"],
        )
        functions = load_function_definitions(funcs_path)
        prompts = load_test_prompts(input_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[X] {exc}", file=sys.stderr)
        return 1

    os.environ.setdefault("HF_HOME", str(Path("./.cache/huggingface").resolve()))
    from llm_sdk import Small_LLM_Model

    debug = args.debug
    dbg(
        debug,
        f"functions: {funcs_path} ({len(functions)}), "
        f"prompts: {input_path} ({len(prompts)})",
    )
    t0 = time.perf_counter()
    llm = Small_LLM_Model()
    dbg(debug, f"model loaded in {time.perf_counter() - t0:.1f}s")
    t0 = time.perf_counter()
    vocab = TokenVocabulary(vocab_path=Path(llm.get_path_to_vocab_file()))
    builder = PromptBuilder()
    # The system prompt only depends on the function list: build it once.
    system_prompt = builder.build_system_prompt(functions)
    fsm = JSONFunctionFSM(vocab=vocab, functions_def=functions)
    fsm.debug = debug
    dbg(
        debug,
        f"vocab ({len(vocab.token_to_id)} tokens) + FSM ready "
        f"in {time.perf_counter() - t0:.1f}s",
    )

    results: List[FunctionResult] = []
    failures = 0
    for idx, prompt_obj in enumerate(prompts, start=1):
        print(f"[{idx}/{len(prompts)}] {prompt_obj.prompt}", flush=True)
        stats: Dict[str, int] = {}
        start = time.perf_counter()
        try:
            result = generate_constrained(
                llm,
                prompt_obj.prompt,
                functions,
                vocab,
                builder,
                fsm,
                stats,
                system_prompt=system_prompt,
            )
        except (RuntimeError, ValueError) as exc:
            print(f"    [!] skipped: {exc}", file=sys.stderr)
            failures += 1
            continue
        print(
            f"    [{time.perf_counter() - start:.1f}s] "
            f"model calls: {stats.get('model_calls', 0)}, "
            f"forced tokens: {stats.get('forced', 0)}"
        )
        print(f"    -> {result.name} {json.dumps(result.parameters, ensure_ascii=False)}")
        results.append(result)

    save_function_results(args.output, results)
    print(f"[+] {len(results)} results saved to '{args.output}' ({failures} failed).")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
