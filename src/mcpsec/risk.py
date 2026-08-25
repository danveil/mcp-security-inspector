from __future__ import annotations

import math
from collections import defaultdict

from mcpsec.models import Finding, Severity


def severity_for_score(score: int) -> Severity:
    if score >= 80:
        return Severity.CRITICAL
    if score >= 60:
        return Severity.HIGH
    if score >= 40:
        return Severity.MEDIUM
    if score >= 20:
        return Severity.LOW
    return Severity.INFORMATIONAL


def calculate_risk(findings: list[Finding]) -> tuple[int, Severity]:
    """Deduplicate rules, confidence-adjust, cap categories, and combine them."""
    categories: dict[str, float] = defaultdict(float)
    ids = {finding.rule_id for finding in findings}
    # A detector may encounter the same indicator in several fields. A single
    # rule contributes its strongest category score once, so duplicated output
    # cannot change a tool's risk merely through repetition.
    unique: dict[tuple[str, str], Finding] = {}
    for item in findings:
        key = (item.category, item.rule_id)
        current = unique.get(key)
        candidate_score = item.score_contribution * item.confidence
        current_score = current.score_contribution * current.confidence if current else -1
        if candidate_score > current_score:
            unique[key] = item
    for item in unique.values():
        categories[item.category] += min(item.score_contribution, 35) * item.confidence
    capped = [min(value, 35) for value in categories.values()]
    combined = 100 * (1 - math.prod(1 - value / 100 for value in capped))
    if {"PI-001", "HID-001"} <= ids:
        combined += 10
    if "HID-001" in ids and "SEC-001" in ids:
        combined += 7
    score = min(100, max(0, round(combined)))
    return score, severity_for_score(score)
