"""Schema normalization tests (flat/standard notation, required, returns)."""

from src.models import FunctionSchema


def test_flat_notation_without_required_means_all_required() -> None:
    schema = FunctionSchema.model_validate(
        {
            "name": "f",
            "description": "d",
            "parameters": {"a": {"type": "number"}, "b": {"type": "string"}},
        }
    )
    assert schema.parameters.required == ["a", "b"]


def test_standard_notation_without_required_means_all_required() -> None:
    schema = FunctionSchema.model_validate(
        {
            "name": "f",
            "description": "d",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}},
            },
        }
    )
    assert schema.parameters.required == ["a"]


def test_explicit_empty_required_means_no_required_parameter() -> None:
    flat = FunctionSchema.model_validate(
        {
            "name": "f",
            "description": "d",
            "parameters": {"a": {"type": "number"}, "required": []},
        }
    )
    standard = FunctionSchema.model_validate(
        {
            "name": "g",
            "description": "d",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}},
                "required": [],
            },
        }
    )
    assert flat.parameters.required == []
    assert standard.parameters.required == []


def test_returns_is_optional() -> None:
    schema = FunctionSchema.model_validate({"name": "f", "description": "d"})
    assert schema.returns.type == "string"
