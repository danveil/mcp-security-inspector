import json
from pathlib import Path

from rich.console import Console

from mcpsec.evaluation.evaluator import evaluate_corpus
from mcpsec.evaluation.reporter import render_terminal, serialize
from mcpsec.models import SuppressionDefinition

ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "evaluation" / "corpus" / "manifest.json"


def test_bundled_corpus_evaluation() -> None:
    report = evaluate_corpus(MANIFEST)
    assert report.metadata.sample_count == 80
    assert report.metadata.corpus_version == "1.0.0"
    assert report.confusion_matrix.model_dump() == {"tp": 37, "tn": 35, "fp": 5, "fn": 3}
    assert report.metrics.f1 > 0.9
    assert {item.category for item in report.category_metrics} >= {"schema", "obfuscation", "mismatch"}
    assert len(report.false_positives) == 5
    assert len(report.false_negatives) == 3
    assert report.timing.minimum_ms >= 0
    assert report.timing.maximum_ms >= report.timing.minimum_ms


def test_evaluation_json_and_csv() -> None:
    report = evaluate_corpus(MANIFEST)
    payload = json.loads(serialize(report, "json"))
    assert payload["confusion_matrix"]["tp"] == 37
    csv_text = serialize(report, "csv")
    assert csv_text.startswith("sample_id,expected,predicted")
    assert "suspicious_001" in csv_text


def test_evaluation_terminal() -> None:
    console = Console(record=True, width=140)
    render_terminal(evaluate_corpus(MANIFEST), console)
    text = console.export_text()
    assert "False Positives (5)" in text
    assert "False Negatives (3)" in text
    assert "instruction_override" in text


def test_unknown_evaluation_format() -> None:
    report = evaluate_corpus(MANIFEST)
    try:
        serialize(report, "xml")
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_suppressions_are_disabled_unless_explicit() -> None:
    baseline = evaluate_corpus(MANIFEST)
    suppression = SuppressionDefinition(
        rule_id="PI-001", justification="Explicit test-only suppression with documented rationale."
    )
    modified = evaluate_corpus(MANIFEST, suppressions=[suppression])
    assert not baseline.metadata.suppressions_applied
    assert modified.metadata.suppressions_applied
    assert modified.confusion_matrix.tp < baseline.confusion_matrix.tp
