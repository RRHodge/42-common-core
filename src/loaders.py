"""Data loading and saving utilities for JSON inputs and output results.

Provides robust file reading, JSON parsing, and Pydantic validation for
function definitions, test prompts, and execution results.
Handles missing files, malformed JSON, and validation errors gracefully.
"""

import json
from pathlib import Path
from typing import List, Union

from pydantic import ValidationError

from src.models import FunctionResult, FunctionSchema, PromptSchema


def load_function_definitions(filepath: Union[str, Path]) -> List[FunctionSchema]:
    """Load and validate function definitions from a JSON file.

    Args:
        filepath: Path to the functions_definition.json file.

    Returns:
        List of validated FunctionSchema objects.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If JSON is malformed or structure is invalid.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Function definitions file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON in {path}: {exc}") from exc

    if not isinstance(raw_data, list):
        raise ValueError(
            f"Expected a JSON list of function definitions in {path}, got {type(raw_data).__name__}"
        )

    validated_functions: List[FunctionSchema] = []
    seen_names: set[str] = set()
    for idx, entry in enumerate(raw_data):
        try:
            func = FunctionSchema.model_validate(entry)
            if func.name in seen_names:
                raise ValueError(
                    f"Duplicate function name '{func.name}' in {path}"
                )
            seen_names.add(func.name)
            validated_functions.append(func)
        except ValidationError as exc:
            raise ValueError(
                f"Validation error in function definition at index {idx} in {path}:\n{exc}"
            ) from exc

    return validated_functions


def load_test_prompts(filepath: Union[str, Path]) -> List[PromptSchema]:
    """Load and validate test prompts from a JSON file.

    Args:
        filepath: Path to the function_calling_tests.json file.

    Returns:
        List of validated PromptSchema objects.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If JSON is malformed or structure is invalid.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Test prompts file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON in {path}: {exc}") from exc

    if not isinstance(raw_data, list):
        raise ValueError(
            f"Expected a JSON list of test prompts in {path}, got {type(raw_data).__name__}"
        )

    validated_prompts: List[PromptSchema] = []
    for idx, entry in enumerate(raw_data):
        try:
            if isinstance(entry, str):
                entry = {"prompt": entry}
            prompt_obj = PromptSchema.model_validate(entry)
            validated_prompts.append(prompt_obj)
        except ValidationError as exc:
            raise ValueError(
                f"Validation error in prompt at index {idx} in {path}:\n{exc}"
            ) from exc

    return validated_prompts


def save_function_results(
    filepath: Union[str, Path],
    results: List[FunctionResult],
) -> None:
    """Save function execution results to a formatted JSON file.

    Args:
        filepath: Output target path for function_calling_results.json.
        results: List of validated FunctionResult objects.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    dumped_data = [res.model_dump() for res in results]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(dumped_data, f, indent=2, ensure_ascii=False)
