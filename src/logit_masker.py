"""Module for ultra-fast vectorised logit masking and constrained decoding."""

import re
import numpy as np
from typing import Dict, List, Set, Union
from src.vocabulary import Vocabulary


class LogitMasker:
    """Pre-allocates and caches vectorised NumPy masks for FSM states."""

    def __init__(self, vocab_size: int) -> None:
        """Initialize the masker with vocabulary size.

        Args:
            vocab_size: Total size of the model vocabulary.
        """
        self.vocab_size: int = vocab_size
        self._mask_cache: Dict[str, np.ndarray] = {}

    def get_mask(self, state_key: str, allowed_token_ids: Union[List[int], Set[int]]) -> np.ndarray:
        """Retrieve or create a cached NumPy logit mask for a given state.

        Args:
            state_key: Unique identifier for the FSM state.
            allowed_token_ids: Token IDs permitted in this state.

        Returns:
            NumPy array of shape (vocab_size,) with 0.0 for allowed tokens and -inf for disallowed tokens.
        """
        if state_key not in self._mask_cache:
            mask = np.full(self.vocab_size, -np.inf, dtype=np.float32)
            if allowed_token_ids:
                mask[list(allowed_token_ids)] = 0.0
            self._mask_cache[state_key] = mask
        return self._mask_cache[state_key]

    def clear_cache(self) -> None:
        """Clear all cached state masks."""
        self._mask_cache.clear()


class StaticTokenSets:
    """Pre-computes the static token IDs needed by the FSM.

    Only the numeric alphabet is kept: the other JSON punctuation is handled by
    the literal prefix index in `JSONFunctionFSM`, so scanning the vocabulary for
    it would be dead work at start-up.
    """

    def __init__(self, vocab: Vocabulary) -> None:
        """Pre-compute static token sets at initialization.

        Args:
            vocab: Instantiated Vocabulary object.
        """
        self.vocab: Vocabulary = vocab
        self.digits: List[int] = [
            tid for tid, text in vocab.id_to_token.items()
            if re.fullmatch(r"[0-9.\-]+", text)
        ]


def select_best_token(
    logits: np.ndarray,
    mask: np.ndarray,
    allowed_ids: Union[Set[int], List[int], None] = None,
) -> int:
    """Apply logit mask and select the highest probability token ID using vectorised argmax.

    Args:
        logits: Raw logit array from model output.
        mask: Pre-computed NumPy logit mask.
        allowed_ids: Allowed token IDs, used as a last-resort fallback when every
            allowed logit is ``-inf`` (an argmax over an all--inf array would
            otherwise return a forbidden index).

    Returns:
        Selected token ID, always one of the allowed IDs when they are known.
    """
    scores = np.asarray(logits, dtype=np.float32)
    size = mask.shape[0]
    if scores.shape[0] < size:
        raise ValueError(
            f"Logits shorter ({scores.shape[0]}) than the mask ({size})"
        )
    # The model may output more logits than vocab.json has entries (padding): ignore the extra ones.
    masked = scores[:size] + mask
    # A NaN on a forbidden position would win the argmax and break the JSON.
    masked[mask != 0] = -np.inf
    best = int(np.argmax(masked))
    if allowed_ids and mask[best] != 0:
        best = int(next(iter(allowed_ids)))
    return best
