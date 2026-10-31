"""ChatML prompt construction for Qwen3 function calling."""

import json
from typing import Any, Dict, List, Optional

from src.models import FunctionSchema

DEFAULT_SYSTEM_PROMPT = (
    "You are a function-calling assistant. Pick the single best function for "
    "the user's request and copy the argument values exactly as they appear "
    "in the request.\n"
    'Answer ONLY with one JSON object: {"name": <function name>, '
    '"parameters": {<argument name>: <value>}}. '
    "Numbers must be JSON numbers, not strings.\n\n"
    "Available tools:\n{tools_json}"
)


class PromptBuilder:
    """Builds the ChatML prompts sent to the model."""

    def __init__(self, system_template: Optional[str] = None) -> None:
        """Initialize the builder with an optional system prompt template."""
        self.system_template = system_template or DEFAULT_SYSTEM_PROMPT

    @staticmethod
    def function_to_json_schema(func: FunctionSchema) -> Dict[str, Any]:
        """Convert a FunctionSchema into an OpenAI/Qwen "tool" dictionary using Pydantic dump."""
        # On extrait la structure propre de la fonction via Pydantic
        func_dict = func.model_dump()

        return {
            "type": "function",
            "function": {
                "name": func_dict["name"],
                "description": func_dict["description"],
                "parameters": {
                    "type": func_dict["parameters"].get("type", "object"),
                    "properties": func_dict["parameters"].get("properties", {}),
                    "required": func_dict["parameters"].get("required", []),
                },
            },
        }

    def build_system_prompt(self, functions: List[FunctionSchema]) -> str:
        """Return the system prompt containing the serialized tool schemas.

        Uses str.replace instead of str.format so the template may contain
        literal JSON braces.
        """
        schemas = [self.function_to_json_schema(fn) for fn in functions]
        tools_json = json.dumps(schemas, separators=(",", ":"), ensure_ascii=False)
        return self.system_template.replace("{tools_json}", tools_json)

    def build_chat_prompt(
        self,
        user_prompt: str,
        functions: List[FunctionSchema],
        system_prompt: Optional[str] = None,
    ) -> str:
        """Return the full ChatML prompt.

        The empty <think> block disables the thinking mode of Qwen3.
        Pass `system_prompt` to reuse an already built system prompt: it only
        depends on `functions`, so rebuilding it for every prompt is wasted work.
        """
        system_text = (
            system_prompt
            if system_prompt is not None
            else self.build_system_prompt(functions)
        )
        return (
            f"<|im_start|>system\n{system_text}<|im_end|>\n"
            f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
            "<|im_start|>assistant\n<think>\n\n</think>\n\n"
        )
