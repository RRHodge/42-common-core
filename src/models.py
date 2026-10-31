"""Data models for function definitions, test prompts, and execution results.

All models inherit from Pydantic BaseModel to enforce strict data validation,
type casting, and schema integrity as mandated by project requirements.
Fields use typing.Annotated for idiomatic Pydantic v2 metadata declarations.
"""

from typing import Annotated, Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ParameterProperty(BaseModel):
    """Schema for an individual parameter property in a function definition."""

    model_config = ConfigDict(extra="ignore")

    type: Annotated[
        str,
        Field(description="Data type of parameter (e.g., 'string', 'number', 'boolean')."),
    ]
    description: Annotated[
        Optional[str],
        Field(default="", description="Human-readable description of the parameter."),
    ]


class FunctionParameters(BaseModel):
    """Schema for the parameters object in a function definition."""

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def _accept_flat_format(cls, data: Any) -> Any:
        """Normalize both notations and make ``required`` unambiguous.

        - ``{"a": {...}}`` (flat) is rewritten as an object schema;
        - a missing ``required`` list means *every* declared parameter is
          required (the project rule);
        - an explicit ``"required": []`` means *no* parameter is required, so a
          function with only optional parameters can be called with no argument.
        """
        if not isinstance(data, dict):
            return data
        if "properties" not in data:
            flat = {k: v for k, v in data.items() if isinstance(v, dict)}
            if flat:
                required = data.get("required")
                if required is None:
                    required = list(flat)
                return {
                    "type": "object",
                    "properties": flat,
                    "required": required,
                }
            return data
        normalized = dict(data)
        if normalized.get("required") is None:
            normalized["required"] = list(normalized.get("properties") or {})
        return normalized

    type: Annotated[
        str,
        Field(
            default="object",
            description="Container type for parameters, usually 'object'.",
        ),
    ]
    properties: Annotated[
        Dict[str, ParameterProperty],
        Field(
            default_factory=dict,
            description="Dictionary mapping parameter names to property schemas.",
        ),
    ]
    required: Annotated[
        List[str],
        Field(
            default_factory=list,
            description="List of parameter names required for function execution.",
        ),
    ]


class FunctionReturns(BaseModel):
    """Schema for the return value of a function."""

    model_config = ConfigDict(extra="ignore")

    type: Annotated[
        str,
        Field(
            default="string",
            description="Data type of the return value (e.g., 'string', 'number', 'boolean').",
        ),
    ]
    description: Annotated[
        Optional[str],
        Field(default="", description="Human-readable description of the return value."),
    ]


class FunctionSchema(BaseModel):
    """Complete schema definition for an executable tool function."""

    model_config = ConfigDict(extra="ignore")

    name: Annotated[str, Field(description="Unique identifier for the function, used in calls.")]
    description: Annotated[
        str,
        Field(description="Description of what the function does."),
    ]
    parameters: Annotated[
        FunctionParameters,
        Field(
            default_factory=FunctionParameters,
            description="Parameters accepted by the function.",
        ),
    ]
    returns: Annotated[
        FunctionReturns,
        Field(
            default_factory=FunctionReturns,
            description="Schema for the return value of the function.",
        ),
    ]


class PromptSchema(BaseModel):
    """Input prompt schema from the test dataset."""

    model_config = ConfigDict(extra="ignore")

    prompt: Annotated[
        str,
        Field(description="Natural language request prompt to be processed by the LLM."),
    ]


class FunctionResult(BaseModel):
    """Validated output structure representing an LLM function call result."""

    model_config = ConfigDict(extra="ignore")

    prompt: Annotated[
        str,
        Field(description="Original natural language input prompt."),
    ]
    name: Annotated[
        str,
        Field(description="Name of the function selected by the LLM."),
    ]
    parameters: Annotated[
        Dict[str, Any],
        Field(
            default_factory=dict,
            description="Extracted key-value argument dictionary.",
        ),
    ]
