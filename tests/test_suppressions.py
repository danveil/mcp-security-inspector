from pathlib import Path

import pytest
from conftest import make_tool

from mcpsec.exceptions import RuleValidationError
from mcpsec.models import SuppressionDefinition
from mcpsec.normalizer import normalize_tool
from mcpsec.scanner import analyze_tools, is_suppressed
from mcpsec.suppressions import load_suppressions


def write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "suppressions.yml"
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_suppression(tmp_path: Path) -> None:
    values = load_suppressions(
        write(tmp_path, "suppressions:\n  - rule_id: SEC-001\n    justification: Legitimate reviewed context.\n"),
        {"SEC-001"},
    )
    assert values[0].justification == "Legitimate reviewed context."


def test_invalid_rule_id(tmp_path: Path) -> None:
    with pytest.raises(RuleValidationError, match="Unknown"):
        load_suppressions(
            write(tmp_path, "suppressions:\n  - rule_id: BAD-001\n    justification: Legitimate reviewed context.\n"),
            {"SEC-001"},
        )


def test_missing_justification(tmp_path: Path) -> None:
    with pytest.raises(RuleValidationError, match="justification"):
        load_suppressions(write(tmp_path, "suppressions:\n  - rule_id: SEC-001\n"), {"SEC-001"})


def test_scope_matching() -> None:
    suppression = SuppressionDefinition(
        rule_id="SEC-001", tool="approved_auth", justification="Reviewed legitimate authentication tool."
    )
    assert is_suppressed("SEC-001", "approved_auth", [suppression])
    assert not is_suppressed("SEC-001", "other", [suppression])


def test_scanner_applies_scoped_suppression() -> None:
    tool = normalize_tool(make_tool(name="approved_auth", description="requests a password"))
    unsuppressed = analyze_tools([tool], source="test")
    suppression = SuppressionDefinition(
        rule_id="SEC-001", tool="approved_auth", justification="Reviewed legitimate authentication workflow."
    )
    suppressed = analyze_tools([tool], source="test", suppressions=[suppression])
    assert [item.rule_id for item in unsuppressed.tools[0].findings] == ["SEC-001"]
    assert suppressed.tools[0].findings == []


def test_suppression_file_size_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mcpsec.suppressions.MAX_SUPPRESSION_FILE_BYTES", 20)
    with pytest.raises(RuleValidationError, match="byte limit"):
        load_suppressions(
            write(tmp_path, "suppressions:\n  - rule_id: SEC-001\n    justification: Legitimate context.\n"),
            {"SEC-001"},
        )


def test_suppression_count_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("mcpsec.suppressions.MAX_SUPPRESSIONS", 1)
    payload = (
        "suppressions:\n"
        "  - rule_id: SEC-001\n"
        "    justification: First legitimate reviewed context.\n"
        "  - rule_id: HID-001\n"
        "    justification: Second legitimate reviewed context.\n"
    )
    with pytest.raises(RuleValidationError, match="exceeds 1 entries"):
        load_suppressions(write(tmp_path, payload), {"SEC-001", "HID-001"})
