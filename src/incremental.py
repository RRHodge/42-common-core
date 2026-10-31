"""Optional incremental decoding with a KV cache on top of the provided SDK.

The public ``llm_sdk`` API only exposes ``get_logits_from_input_ids``, which
re-runs the whole sequence for every generated token.  When the SDK object
exposes its underlying transformers model (``_model``/``_device``), this module
keeps the KV cache and forwards only the new tokens.  If that private API is not
available (or changes), it falls back transparently to the public method.
"""

from typing import Any, List, Optional

import numpy as np


class IncrementalLogits:
    """Return next-token logits while reusing a KV cache across calls."""

    def __init__(self, llm: Any, prompt_ids: List[int]) -> None:
        """Store the prompt and detect whether the incremental path is usable."""
        self._llm = llm
        self._model: Any = getattr(llm, "_model", None)
        self._device: Any = getattr(llm, "_device", None)
        self._prompt_ids: List[int] = list(prompt_ids)
        self._context: List[int] = list(prompt_ids)
        self._past: Any = None
        self._last_logits: Optional[np.ndarray] = None
        self._incremental: bool = self._model is not None and self._device is not None

    @property
    def incremental(self) -> bool:
        """Whether the KV-cache path is currently active."""
        return self._incremental

    def feed(self, token_ids: List[int]) -> np.ndarray:
        """Consume newly generated tokens and return the logits for the next one.

        The first call forwards the prompt and the first batch of forced tokens
        together; later calls forward only the tokens appended since the
        previous call.  On any failure, the provider switches to the public SDK
        method for the rest of the generation.
        """
        tokens = list(token_ids)
        self._context.extend(tokens)
        if self._incremental:
            try:
                return self._cached_forward(tokens)
            except Exception:  # private API changed or unsupported model
                self._incremental = False
                self._past = None
                self._last_logits = None
        logits = self._llm.get_logits_from_input_ids(self._context)
        return np.asarray(logits, dtype=np.float32)

    def _cached_forward(self, tokens: List[int]) -> np.ndarray:
        """Forward only `tokens`, using the existing KV cache if any."""
        if self._past is None:
            input_ids = self._prompt_ids + tokens
        else:
            input_ids = tokens
        if not input_ids:
            if self._last_logits is None:
                input_ids = self._prompt_ids
            else:
                return self._last_logits

        import torch  # imported lazily: tests do not need the model stack

        input_tensor = torch.tensor(
            [input_ids], device=self._device, dtype=torch.long
        )
        with torch.no_grad():
            outputs = self._model(
                input_ids=input_tensor,
                past_key_values=self._past,
                use_cache=True,
            )
        past = getattr(outputs, "past_key_values", None)
        if past is None:
            raise RuntimeError("The model did not return a KV cache")
        self._past = past
        logits = outputs.logits[0, -1].float().cpu().numpy()
        self._last_logits = np.asarray(logits, dtype=np.float32)
        return self._last_logits
