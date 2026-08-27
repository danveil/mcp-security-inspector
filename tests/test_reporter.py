import csv
import io
import json
from pathlib import Path

import pytest
from conftest import make_tool
from rich.console import Console

from mcpsec.cli import analyze
from mcpsec.models import Finding, FindingBudgetStatus, ScanReport, ToolScanResult
from mcpsec.normalizer import normalize_tool
from mcpsec.reporter import (
    neutralize_csv,
    render_terminal,
    report_csv,
    report_json,
    report_sarif,
    serialize,
    terminal_safe,
)


def sample_report(name: str = "tool") -> ScanReport:
    finding = Finding(
        rule_id="TST-001",
        rule_name="Test",
        category="test",
        severity="HIGH",
        confidence=0.8,
        explanation="Suspicious test indicator.",
        evidence="=FORMULA",
        field="description",
        recommendation="Review.",
        score_contribution=10,
    )
    result = ToolScanResult(
        tool=normalize_tool(make_tool(name=name)), findings=[finding], risk_score=8, severity="INFORMATIONAL"
    )
    return ScanReport(application="MCP Tool Security Inspector", version="0.1.0", source="fixture.json", tools=[result])


def bounded_report() -> ScanReport:
    report = sample_report()
    report.tools[0] = report.tools[0].model_copy(update={"findings_detected": 2, "findings_truncated": True})
    report.finding_budget = FindingBudgetStatus(
        per_tool_limit=1,
        report_limit=1,
        evidence_char_limit_per_tool=240,
        findings_detected=2,
        findings_retained=1,
        truncated=True,
    )
    return report


def test_json_machine_readable() -> None:
    assert json.loads(report_json(sample_report()))["tools"][0]["findings"][0]["rule_id"] == "TST-001"


def test_json_has_no_ansi() -> None:
    assert "\x1b" not in report_json(sample_report())


@pytest.mark.parametrize("value", ["=1+1", "+cmd", "-1", "@SUM(A1)", "\tformula", "  =x"])
def test_formula_injection_neutralized(value: str) -> None:
    assert neutralize_csv(value).lstrip().startswith("'")


def test_safe_csv_unchanged() -> None:
    assert neutralize_csv("weather") == "weather"


def test_terminal_untrusted_text_is_literal_ascii() -> None:
    rendered = terminal_safe("[red]\x1b中")
    assert "\\[red]" in rendered
    assert r"\x1b" in rendered
    assert r"\u4e2d" in rendered


def test_csv_is_parseable_and_evidence_neutralized() -> None:
    rows = list(csv.reader(io.StringIO(report_csv(sample_report("=tool")))))
    assert rows[1][0].startswith("'")
    assert rows[1][6].startswith("'")


def test_clean_csv_row(tmp_path: Path) -> None:
    report = analyze(Path("examples/clean_tools.json"))
    rows = list(csv.DictReader(io.StringIO(report_csv(report))))
    assert len(rows) == 2
    assert rows[0]["field"] == rows[0]["evidence"] == rows[0]["recommendation"] == ""
    assert rows[0]["findings_detected"] == rows[0]["findings_retained"] == "0"
    assert rows[0]["findings_truncated"] == "False"


def test_sarif_shape() -> None:
    sarif = json.loads(report_sarif(sample_report()))
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["results"][0]["ruleId"] == "TST-001"


def test_terminal_output() -> None:
    output = io.StringIO()
    render_terminal(sample_report(), Console(file=output, force_terminal=False, width=160))
    assert "MCP Tool Security Inspector" in output.getvalue()
    assert "TST-001" in output.getvalue()


def test_finding_budget_status_is_visible_in_every_report_format() -> None:
    report = bounded_report()
    assert json.loads(report_json(report))["finding_budget"]["truncated"] is True
    csv_rows = list(csv.DictReader(io.StringIO(report_csv(report))))
    assert csv_rows[0]["findings_truncated"] == "True"
    sarif = json.loads(report_sarif(report))
    assert sarif["runs"][0]["properties"]["findingBudget"]["truncated"] is True
    output = io.StringIO()
    render_terminal(report, Console(file=output, force_terminal=False, width=160))
    assert "Finding output bounded" in output.getvalue()
    assert "OUTPUT BOUNDED" in output.getvalue()


@pytest.mark.parametrize("format_name", ["json", "csv", "sarif"])
def test_serialize_formats(format_name: str) -> None:
    assert serialize(sample_report(), format_name)


def test_serialize_unknown() -> None:
    with pytest.raises(ValueError):
        serialize(sample_report(), "html")
