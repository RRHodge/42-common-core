"""Logit-mask tests: a forbidden token must never win the argmax."""

import numpy as np

from src.logit_masker import select_best_token


def _mask(size: int = 10, allowed: tuple[int, ...] = (2, 5)) -> np.ndarray:
    mask = np.full(size, -np.inf, dtype=np.float32)
    mask[list(allowed)] = 0.0
    return mask


def test_nan_on_a_forbidden_position_cannot_win() -> None:
    mask = _mask()
    logits = np.zeros(10, dtype=np.float32)
    logits[0] = np.nan
    logits[2] = 1.0
    assert select_best_token(logits, mask, {2, 5}) == 2


def test_all_allowed_logits_at_minus_infinity_fall_back_to_an_allowed_id() -> None:
    mask = _mask()
    logits = np.full(10, -np.inf, dtype=np.float32)
    assert select_best_token(logits, mask, {2, 5}) in {2, 5}


def test_padded_logits_are_ignored() -> None:
    mask = _mask()
    logits = np.zeros(13, dtype=np.float32)
    logits[5] = 9.0
    assert select_best_token(logits, mask, {2, 5}) == 5


def test_mask_is_not_mutated() -> None:
    mask = _mask()
    logits = np.zeros(10, dtype=np.float32)
    select_best_token(logits, mask, {2, 5})
    assert np.isinf(mask[0])
    assert mask[2] == 0.0
