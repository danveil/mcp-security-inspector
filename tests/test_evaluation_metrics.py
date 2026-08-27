import pytest

from mcpsec.evaluation.metrics import calculate_metrics, confusion, safe_ratio, timing_statistics
from mcpsec.evaluation.models import ConfusionMatrix


def test_all_binary_metrics() -> None:
    metrics = calculate_metrics(ConfusionMatrix(tp=8, tn=9, fp=1, fn=2))
    assert metrics.accuracy == pytest.approx(0.85)
    assert metrics.precision == pytest.approx(8 / 9)
    assert metrics.recall == pytest.approx(0.8)
    assert metrics.f1 == pytest.approx(2 * (8 / 9) * 0.8 / ((8 / 9) + 0.8))
    assert metrics.false_positive_rate == pytest.approx(0.1)
    assert metrics.false_negative_rate == pytest.approx(0.2)
    assert metrics.specificity == pytest.approx(0.9)


def test_confusion_counts_every_quadrant() -> None:
    assert confusion([True, False, False, True], [True, False, True, False]) == ConfusionMatrix(tp=1, tn=1, fp=1, fn=1)


def test_confusion_rejects_different_lengths() -> None:
    with pytest.raises(ValueError, match="equal lengths"):
        confusion([True], [])


def test_zero_division_is_safe() -> None:
    metrics = calculate_metrics(ConfusionMatrix(tp=0, tn=0, fp=0, fn=0))
    assert set(metrics.model_dump().values()) == {0.0}
    assert safe_ratio(1, 0) == 0


def test_timing_statistics() -> None:
    timing = timing_statistics([4.0, 1.0, 3.0, 2.0, 10.0], sample_count=5)
    assert timing.observation_count == 5
    assert timing.sample_count == 5
    assert timing.measured_repetitions == 1
    assert timing.total_ms == 20
    assert timing.mean_ms == 4
    assert timing.median_ms == 3
    assert timing.minimum_ms == 1
    assert timing.maximum_ms == 10
    assert timing.p95_ms == 10
    assert timing.standard_deviation_ms == pytest.approx(3.1622776601683795)
    assert timing.mean_per_tool_ms == 4
    assert timing.mean_corpus_pass_ms == 20


def test_empty_timing_statistics() -> None:
    timing = timing_statistics([])
    assert timing.observation_count == 0
    assert timing.sample_count == 0
    assert timing.measured_repetitions == 1
    assert set(timing.model_dump(exclude={"observation_count", "sample_count", "measured_repetitions"}).values()) == {
        0.0
    }


def test_timing_statistics_requires_complete_repetitions() -> None:
    with pytest.raises(ValueError, match="sample_count multiplied"):
        timing_statistics([1.0, 2.0, 3.0], sample_count=2, measured_repetitions=2)
    with pytest.raises(ValueError, match="at least 1"):
        timing_statistics([], measured_repetitions=0)
