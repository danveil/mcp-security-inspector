from mcpsec.models import Finding, Severity
from mcpsec.risk import calculate_risk, severity_for_score


def item(rule_id: str = "X-001", category: str = "x", score: float = 20, confidence: float = 1) -> Finding:
    return Finding(
        rule_id=rule_id,
        rule_name="test",
        category=category,
        severity="MEDIUM",
        confidence=confidence,
        explanation="test",
        evidence="test",
        field="description",
        recommendation="review",
        score_contribution=score,
    )


def test_empty_score() -> None:
    assert calculate_risk([]) == (0, Severity.INFORMATIONAL)


def test_confidence_adjustment() -> None:
    assert calculate_risk([item(score=20, confidence=0.5)])[0] == 10


def test_category_cap() -> None:
    assert calculate_risk([item(score=35), item(score=35)])[0] == 35


def test_multiple_categories_combine_without_simple_sum() -> None:
    assert calculate_risk([item(category="a"), item(category="b")])[0] == 36


def test_override_concealment_synergy() -> None:
    score = calculate_risk([item("PI-001", "a"), item("HID-001", "b")])[0]
    assert score == 46


def test_sensitive_concealment_synergy() -> None:
    score = calculate_risk([item("SEC-001", "a"), item("HID-001", "b")])[0]
    assert score == 43


def test_score_cap() -> None:
    findings = [item(category=str(index), score=35) for index in range(20)]
    assert calculate_risk(findings)[0] <= 100


def test_bands() -> None:
    assert [severity_for_score(x) for x in (0, 20, 40, 60, 80)] == [
        Severity.INFORMATIONAL,
        Severity.LOW,
        Severity.MEDIUM,
        Severity.HIGH,
        Severity.CRITICAL,
    ]
