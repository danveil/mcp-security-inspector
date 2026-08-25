from __future__ import annotations

import math
import statistics

from mcpsec.evaluation.models import ClassificationMetrics, ConfusionMatrix, TimingStatistics


def safe_ratio(numerator: int | float, denominator: int | float) -> float:
    return numerator / denominator if denominator else 0.0


def calculate_metrics(matrix: ConfusionMatrix) -> ClassificationMetrics:
    total = matrix.tp + matrix.tn + matrix.fp + matrix.fn
    precision = safe_ratio(matrix.tp, matrix.tp + matrix.fp)
    recall = safe_ratio(matrix.tp, matrix.tp + matrix.fn)
    return ClassificationMetrics(
        accuracy=safe_ratio(matrix.tp + matrix.tn, total),
        precision=precision,
        recall=recall,
        f1=safe_ratio(2 * precision * recall, precision + recall),
        false_positive_rate=safe_ratio(matrix.fp, matrix.fp + matrix.tn),
        false_negative_rate=safe_ratio(matrix.fn, matrix.fn + matrix.tp),
        specificity=safe_ratio(matrix.tn, matrix.tn + matrix.fp),
    )


def confusion(actual: list[bool], predicted: list[bool]) -> ConfusionMatrix:
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted labels must have equal lengths")
    return ConfusionMatrix(
        tp=sum(expected and observed for expected, observed in zip(actual, predicted, strict=True)),
        tn=sum(not expected and not observed for expected, observed in zip(actual, predicted, strict=True)),
        fp=sum(not expected and observed for expected, observed in zip(actual, predicted, strict=True)),
        fn=sum(expected and not observed for expected, observed in zip(actual, predicted, strict=True)),
    )


def timing_statistics(values_ms: list[float]) -> TimingStatistics:
    if not values_ms:
        return TimingStatistics(total_ms=0, mean_ms=0, median_ms=0, minimum_ms=0, maximum_ms=0, p95_ms=0)
    ordered = sorted(values_ms)
    p95_index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return TimingStatistics(
        total_ms=sum(ordered),
        mean_ms=statistics.fmean(ordered),
        median_ms=statistics.median(ordered),
        minimum_ms=ordered[0],
        maximum_ms=ordered[-1],
        p95_ms=ordered[p95_index],
    )
