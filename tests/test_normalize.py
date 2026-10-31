"""Normalization of regex/replacement artifacts produced by the small model."""

from src.__main__ import _simplify_regex, coerce_parameters
from src.models import FunctionSchema


def test_simplifies_a_redundant_group_and_trailing_whitespace_matcher() -> None:
    assert _simplify_regex(r"([0-9]+)\s") == "[0-9]+"
    assert _simplify_regex(r"([aeiouAEIOU])") == "[aeiouAEIOU]"
    assert _simplify_regex(r"([a-z]+)\s*") == "[a-z]+"
    assert _simplify_regex(r"\d+") == r"\d+"
    assert _simplify_regex(r"cat") == "cat"


def test_does_not_strip_meaningful_groups() -> None:
    assert _simplify_regex(r"(abc)") == "(abc)"
    assert _simplify_regex(r"(abc)\s") == r"(abc)\s"
    assert _simplify_regex(r"([0-9]+)?") == r"([0-9]+)?"


def test_coerce_normalizes_regex_and_replacement_values() -> None:
    schema = FunctionSchema.model_validate(
        {
            "name": "f",
            "description": "d",
            "parameters": {
                "source_string": {"type": "string"},
                "regex": {"type": "string"},
                "replacement": {"type": "string"},
            },
        }
    )
    result = coerce_parameters(
        {
            "source_string": "Hello 34 I'm 233 years old",
            "regex": r"([0-9]+)\s",
            "replacement": " *",
        },
        schema,
    )
    assert result == {
        "source_string": "Hello 34 I'm 233 years old",
        "regex": "[0-9]+",
        "replacement": "*",
    }
