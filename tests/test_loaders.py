"""Loader tests: validation, duplicates, prompts and output writing."""

import json
from pathlib import Path

import pytest

from src.loaders import (
    load_function_definitions,
    load_test_prompts,
    save_function_results,
)
from src.models import FunctionResult


def test_duplicate_function_names_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "functions.json"
    path.write_text(
        json.dumps(
            [
                {"name": "f", "description": "first"},
                {"name": "f", "description": "second"},
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Duplicate function name"):
        load_function_definitions(path)


def test_prompts_accept_plain_strings(tmp_path: Path) -> None:
    path = tmp_path / "tests.json"
    path.write_text(json.dumps(["hello", {"prompt": "world"}]), encoding="utf-8")
    prompts = load_test_prompts(path)
    assert [prompt.prompt for prompt in prompts] == ["hello", "world"]


def test_results_are_written_as_json(tmp_path: Path) -> None:
    path = tmp_path / "out" / "results.json"
    save_function_results(
        path,
        [FunctionResult(prompt="p", name="f", parameters={"a": 1})],
    )
    assert json.loads(path.read_text(encoding="utf-8")) == [
        {"prompt": "p", "name": "f", "parameters": {"a": 1}}
    ]
