"""Prompt-builder tests: one system prompt per function list."""

from src.models import FunctionSchema
from src.prompts import PromptBuilder
from tests.helpers import FUNCTIONS


def test_reusing_the_system_prompt_gives_the_same_chat_prompt() -> None:
    functions = [FunctionSchema.model_validate(definition) for definition in FUNCTIONS]
    builder = PromptBuilder()
    system_prompt = builder.build_system_prompt(functions)

    without_cache = builder.build_chat_prompt("hello", functions)
    with_cache = builder.build_chat_prompt("hello", functions, system_prompt)

    assert with_cache == without_cache
    assert "<|im_start|>user\nhello<|im_end|>" in with_cache
    assert '"fn_add_numbers"' in system_prompt
