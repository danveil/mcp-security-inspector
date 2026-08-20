import json
from pathlib import Path

from typer.testing import CliRunner

from mcpsec.cli import app

runner = CliRunner()
ROOT = Path(__file__).parents[1]


def invoke(*args: str):
    return runner.invoke(app, list(args))


def test_help() -> None:
    result = invoke("--help")
    assert result.exit_code == 0
    assert "Defensive static analysis" in result.stdout


def test_version() -> None:
    result = invoke("--version")
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_clean_scan_table() -> None:
    result = invoke("scan", str(ROOT / "examples" / "clean_tools.json"))
    assert result.exit_code == 0
    assert "Clean: 2" in result.stdout


def test_suspicious_scan_json() -> None:
    result = invoke("scan", str(ROOT / "examples" / "suspicious_tools.json"), "--format", "json")
    assert result.exit_code == 0
    assert json.loads(result.stdout)["tools"]


def test_fail_on_high() -> None:
    result = invoke("scan", str(ROOT / "examples" / "suspicious_tools.json"), "--fail-on", "high")
    assert result.exit_code == 1


def test_clean_does_not_fail_threshold() -> None:
    result = invoke("scan", str(ROOT / "examples" / "clean_tools.json"), "--fail-on", "medium")
    assert result.exit_code == 0


def test_redact_json() -> None:
    result = invoke("scan", str(ROOT / "examples" / "suspicious_tools.json"), "--format", "json", "--redact")
    assert "[REDACTED: untrusted evidence]" in result.stdout


def test_write_report(tmp_path: Path) -> None:
    output = tmp_path / "report.sarif"
    result = invoke(
        "scan", str(ROOT / "examples" / "suspicious_tools.json"), "--format", "sarif", "--output", str(output)
    )
    assert result.exit_code == 0
    assert json.loads(output.read_text(encoding="utf-8"))["version"] == "2.1.0"


def test_invalid_json_exit_code(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")
    result = invoke("scan", str(path))
    assert result.exit_code == 2


def test_baseline_and_unchanged_compare(tmp_path: Path) -> None:
    source = ROOT / "examples" / "clean_tools.json"
    baseline = tmp_path / "baseline.json"
    assert invoke("baseline", str(source), "--output", str(baseline)).exit_code == 0
    result = invoke("compare", str(source), "--baseline", str(baseline))
    assert result.exit_code == 0
    assert "No tool-definition drift" in result.stdout


def test_changed_compare(tmp_path: Path) -> None:
    baseline = tmp_path / "baseline.json"
    invoke("baseline", str(ROOT / "examples" / "clean_tools.json"), "--output", str(baseline))
    result = invoke("compare", str(ROOT / "examples" / "changed_tools.json"), "--baseline", str(baseline))
    assert result.exit_code == 0
    assert "tool_changed" in result.stdout and "tool_added" in result.stdout


def test_fingerprint_command() -> None:
    result = invoke("fingerprint", str(ROOT / "examples" / "clean_tools.json"))
    assert result.exit_code == 0
    assert len(json.loads(result.stdout)["calculator"]["full_sha256"]) == 64


def test_rules_list() -> None:
    result = invoke("rules", "list")
    assert result.exit_code == 0
    assert "PI-001" in result.stdout


def test_rules_validate() -> None:
    result = invoke("rules", "validate", str(ROOT / "rules" / "default_rules.yml"))
    assert result.exit_code == 0
    assert "Valid: 2" in result.stdout


def test_explain() -> None:
    result = invoke("explain", "SEC-001")
    assert result.exit_code == 0
    assert "Possible benign usage" in result.stdout


def test_unknown_explain() -> None:
    assert invoke("explain", "NOPE").exit_code == 2


def test_demo() -> None:
    result = invoke("demo")
    assert result.exit_code == 0
    assert "metadata_test_only" in result.stdout


def test_custom_rules_fire() -> None:
    result = invoke(
        "scan",
        str(ROOT / "examples" / "suspicious_tools.json"),
        "--rules",
        str(ROOT / "rules" / "default_rules.yml"),
    )
    assert result.exit_code == 0
    assert "CUS-001" in result.stdout
