from __future__ import annotations

from collections import defaultdict

from mcpsec.evaluation.metrics import calculate_metrics, confusion
from mcpsec.evaluation.models import (
    MIN_STRATUM_SAMPLE_COUNT,
    CorpusLabel,
    SampleEvaluation,
    StratificationDimension,
    StratificationReport,
    StratifiedGroup,
)
from mcpsec.evaluation.uncertainty import uncertainty_for_matrix


def _undefined_metrics(tp: int, tn: int, fp: int, fn: int) -> list[str]:
    undefined: list[str] = []
    if tp + fp == 0:
        undefined.append("precision")
    if tp + fn == 0:
        undefined.extend(["recall", "false_negative_rate"])
    if 2 * tp + fp + fn == 0:
        undefined.append("f1")
    if fp + tn == 0:
        undefined.extend(["false_positive_rate", "specificity"])
    return sorted(undefined)


def _values(sample: SampleEvaluation, dimension: StratificationDimension) -> list[str]:
    if dimension == StratificationDimension.expected_category:
        return sample.expected_categories
    if dimension == StratificationDimension.field_location:
        return sample.expected_field_locations
    if dimension == StratificationDimension.difficulty:
        return [sample.difficulty.value]
    return [sample.expected.value]


def stratify_samples(
    samples: list[SampleEvaluation],
    *,
    minimum_sample_count: int = MIN_STRATUM_SAMPLE_COUNT,
) -> list[StratificationReport]:
    if minimum_sample_count < 1:
        raise ValueError("minimum_sample_count must be at least 1")
    reports: list[StratificationReport] = []
    for dimension in StratificationDimension:
        groups: defaultdict[str, list[SampleEvaluation]] = defaultdict(list)
        available_ids: set[str] = set()
        for sample in samples:
            values = _values(sample, dimension)
            if values:
                available_ids.add(sample.sample_id)
            for value in sorted(set(values)):
                groups[value].append(sample)
        strata: list[StratifiedGroup] = []
        for value in sorted(groups):
            members = groups[value]
            matrix = confusion(
                [item.expected == CorpusLabel.suspicious for item in members],
                [item.predicted == CorpusLabel.suspicious for item in members],
            )
            low_evidence = len(members) < minimum_sample_count
            strata.append(
                StratifiedGroup(
                    dimension=dimension,
                    value=value,
                    sample_count=len(members),
                    confusion_matrix=matrix,
                    metrics=calculate_metrics(matrix),
                    uncertainty=uncertainty_for_matrix(matrix),
                    low_evidence=low_evidence,
                    warning=(
                        f"Low evidence: fewer than {minimum_sample_count} samples in this stratum."
                        if low_evidence
                        else None
                    ),
                    undefined_metrics=_undefined_metrics(matrix.tp, matrix.tn, matrix.fp, matrix.fn),
                )
            )
        reports.append(
            StratificationReport(
                dimension=dimension,
                available_sample_count=len(available_ids),
                missing_sample_count=len(samples) - len(available_ids),
                groups=strata,
            )
        )
    return reports
