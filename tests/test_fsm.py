"""FSM tests: valid JSON, required parameters, optional parameters, caps and escaping."""

import json
from typing import List, Sequence

import numpy as np
import pytest

import src.fsm as fsm_module
from src.fsm import JSONFunctionFSM
from src.models import FunctionSchema
from src.vocabulary import Vocabulary
from tests.helpers import drive


def test_numbers_and_strings_produce_valid_json(
    vocab: Vocabulary, functions: List[FunctionSchema]
) -> None:
    fsm = JSONFunctionFSM(vocab, functions)
    target = '{"name": "fn_add_numbers", "parameters": {"a": 2, "b": -1.5}}'
    text = drive(fsm, vocab, target)
    assert text == target
    assert json.loads(text) == {
        "name": "fn_add_numbers",
        "parameters": {"a": 2, "b": -1.5},
    }


def test_string_escapes_are_valid_json(
    vocab: Vocabulary, functions: List[FunctionSchema]
) -> None:
    fsm = JSONFunctionFSM(vocab, functions)
    target = '{"name": "fn_echo", "parameters": {"text": "a\\"b\\\\c\\n"}}'
    parsed = json.loads(drive(fsm, vocab, target))
    assert parsed["parameters"]["text"] == 'a"b\\c\n'


def test_required_parameter_cannot_be_skipped(
    vocab: Vocabulary, functions: List[FunctionSchema]
) -> None:
    fsm = JSONFunctionFSM(vocab, functions)
    # "b" is required: once "a" is written, only "," may follow, never the end.
    with pytest.raises(AssertionError):
        drive(fsm, vocab, '{"name": "fn_add_numbers", "parameters": {"a": 2}}')


def test_all_optional_function_accepts_no_argument(
    vocab: Vocabulary, functions: List[FunctionSchema]
) -> None:
    fsm = JSONFunctionFSM(vocab, functions)
    text = drive(fsm, vocab, '{"name": "fn_all_optional", "parameters": {}}')
    assert json.loads(text)["parameters"] == {}


def test_optional_parameter_can_be_written(
    vocab: Vocabulary, functions: List[FunctionSchema]
) -> None:
    fsm = JSONFunctionFSM(vocab, functions)
    target = '{"name": "fn_opt", "parameters": {"a": 1, "b": "x"}}'
    assert json.loads(drive(fsm, vocab, target))["parameters"] == {"a": 1, "b": "x"}


def test_required_parameters_are_written_in_schema_order(
    vocab: Vocabulary, functions: List[FunctionSchema]
) -> None:
    fsm = JSONFunctionFSM(vocab, functions)
    text = drive(
        fsm,
        vocab,
        '{"name": "fn_add_numbers", "parameters": {"a": 1, "b": 2}}',
    )
    assert list(json.loads(text)["parameters"]) == ["a", "b"]


def test_escaped_function_and_parameter_names(vocab: Vocabulary) -> None:
    definition = {
        "name": 'fn"q',
        "description": "quoted name",
        "parameters": {"a\\b": {"type": "number"}},
    }
    functions = [FunctionSchema.model_validate(definition)]
    fsm = JSONFunctionFSM(vocab, functions)
    target = '{"name": "fn\\"q", "parameters": {"a\\\\b": 1}}'
    parsed = json.loads(drive(fsm, vocab, target))
    assert parsed["name"] == 'fn"q'
    assert parsed["parameters"] == {"a\\b": 1}


def test_string_can_close_with_a_combined_token(vocab: Vocabulary) -> None:
    # Qwen has tokens such as '",' and '"}}' that close a string and contain the
    # following JSON syntax. They must be usable, otherwise the model keeps
    # writing text inside the string until the token cap.
    definition = {
        "name": "fn_two_strings",
        "description": "two strings",
        "parameters": {
            "a": {"type": "string"},
            "b": {"type": "string"},
        },
    }
    functions = [FunctionSchema.model_validate(definition)]
    fsm = JSONFunctionFSM(vocab, functions)
    target = (
        '{"name": "fn_two_strings", "parameters": '
        '{"a": "x", "b": "y"}}'
    )
    text = drive(fsm, vocab, target)
    assert text == target
    assert json.loads(text)["parameters"] == {"a": "x", "b": "y"}


def test_string_value_cap_terminates(vocab: Vocabulary, functions: List[FunctionSchema],
                                     monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fsm_module, "MAX_STRING_TOKENS", 4)
    echo_only = [function for function in functions if function.name == "fn_echo"]
    fsm = JSONFunctionFSM(vocab, echo_only)
    rng = np.random.default_rng(0)
    steps = 0
    while not fsm.is_finished() and steps < 200:
        token = fsm.forced_token()
        if token is None:
            token = fsm.select_token(
                rng.standard_normal(len(vocab.token_to_id)).astype(np.float32)
            )
        fsm.advance(token)
        steps += 1
    assert fsm.is_finished()
    text = "".join(vocab.get_clean_text(token) for token in fsm.generated_tokens)
    assert isinstance(json.loads(text)["parameters"]["text"], str)


def test_number_value_cap_terminates(vocab: Vocabulary, functions: List[FunctionSchema],
                                     monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fsm_module, "MAX_NUMBER_CHARS", 4)
    add_only = [function for function in functions if function.name == "fn_add_numbers"]
    fsm = JSONFunctionFSM(vocab, add_only)
    rng = np.random.default_rng(1)
    steps = 0
    while not fsm.is_finished() and steps < 200:
        token = fsm.forced_token()
        if token is None:
            token = fsm.select_token(
                rng.standard_normal(len(vocab.token_to_id)).astype(np.float32)
            )
        fsm.advance(token)
        steps += 1
    assert fsm.is_finished()
    text = "".join(vocab.get_clean_text(token) for token in fsm.generated_tokens)
    parsed = json.loads(text)
    assert isinstance(parsed["parameters"]["a"], (int, float))
    assert isinstance(parsed["parameters"]["b"], (int, float))


def test_token_budget_scales_with_parameters() -> None:
    from src.__main__ import max_generation_steps
    from src.fsm import MAX_STRING_TOKENS

    definitions: Sequence[dict] = [
        {
            "name": "fn_three_strings",
            "description": "three strings",
            "parameters": {
                name: {"type": "string"} for name in ("a", "b", "c")
            },
        }
    ]
    functions = [FunctionSchema.model_validate(definition) for definition in definitions]
    assert max_generation_steps(functions) >= 3 * MAX_STRING_TOKENS
