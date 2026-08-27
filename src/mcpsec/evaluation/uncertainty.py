from __future__ import annotations

import math

from mcpsec.evaluation.models import ConfusionMatrix, ProportionInterval, UncertaintyReport

WILSON_Z_95 = 1.959963984540054


def wilson_interval(numerator: int, denominator: int) -> ProportionInterval:
    if numerator < 0 or denominator < 0 or numerator > denominator:
        raise ValueError("Wilson interval counts require 0 <= numerator <= denominator")
    if denominator == 0:
        return ProportionInterval(numerator=numerator, denominator=denominator, defined=False)
    estimate = numerator / denominator
    z_squared = WILSON_Z_95**2
    adjustment = z_squared / denominator
    center = (estimate + adjustment / 2) / (1 + adjustment)
    margin = (
        WILSON_Z_95
        * math.sqrt((estimate * (1 - estimate) + z_squared / (4 * denominator)) / denominator)
        / (1 + adjustment)
    )
    return ProportionInterval(
        numerator=numerator,
        denominator=denominator,
        estimate=estimate,
        lower=0.0 if numerator == 0 else max(0.0, center - margin),
        upper=1.0 if numerator == denominator else min(1.0, center + margin),
        defined=True,
    )


def uncertainty_for_matrix(matrix: ConfusionMatrix) -> UncertaintyReport:
    return UncertaintyReport(
        accuracy=wilson_interval(matrix.tp + matrix.tn, matrix.tp + matrix.tn + matrix.fp + matrix.fn),
        recall=wilson_interval(matrix.tp, matrix.tp + matrix.fn),
        false_positive_rate=wilson_interval(matrix.fp, matrix.fp + matrix.tn),
    )
