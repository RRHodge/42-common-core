"""Incremental-logits provider: fallback to the public SDK API."""

from src.incremental import IncrementalLogits


class _FakeLLM:
    """LLM object without private model attributes (public API only)."""

    def __init__(self) -> None:
        self.calls: list[list[int]] = []

    def get_logits_from_input_ids(self, input_ids: list[int]) -> list[float]:
        self.calls.append(list(input_ids))
        return [0.0, 0.0, 0.0, 0.0]


def test_falls_back_to_the_public_api_when_no_model_is_exposed() -> None:
    llm = _FakeLLM()
    provider = IncrementalLogits(llm, [1, 2])
    assert provider.incremental is False

    first = provider.feed([3])
    assert first.shape == (4,)
    assert llm.calls == [[1, 2, 3]]

    # Forced tokens are accumulated and replayed on the full context by the
    # public API; the fallback must not lose any of them.
    provider.feed([4, 5])
    assert llm.calls[-1] == [1, 2, 3, 4, 5]


def test_empty_feed_on_a_fresh_fallback_is_harmless() -> None:
    llm = _FakeLLM()
    provider = IncrementalLogits(llm, [1])
    logits = provider.feed([])
    assert logits.shape == (4,)
    assert llm.calls == [[1]]
