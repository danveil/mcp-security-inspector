from pathlib import Path

import pytest
from conftest import make_tool

from mcpsec.exceptions import RuleValidationError
from mcpsec.normalizer import normalize_tool
from mcpsec.rules.loader import CustomRuleDetector, load_rules

VALID = """
rules:
  - id: TST-001
    name: Test rule
    category: test
    fields: [description]
    patterns: [send a copy]
    severity: HIGH
    confidence: 0.8
    score: 10
    recommendation: Review.
"""


def write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "rules.yml"
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_rule(tmp_path: Path) -> None:
    assert load_rules(write(tmp_path, VALID))[0].id == "TST-001"


def test_custom_rule_matches_literal(tmp_path: Path) -> None:
    detector = CustomRuleDetector(load_rules(write(tmp_path, VALID)))
    assert detector.detect(normalize_tool(make_tool(description="SEND A COPY now")))[0].rule_id == "TST-001"


def test_custom_rule_no_match(tmp_path: Path) -> None:
    detector = CustomRuleDetector(load_rules(write(tmp_path, VALID)))
    assert detector.detect(normalize_tool(make_tool())) == []


def test_disabled_rule(tmp_path: Path) -> None:
    detector = CustomRuleDetector(
        load_rules(
            write(tmp_path, VALID.replace("recommendation: Review.", "recommendation: Review.\n    enabled: false"))
        )
    )
    assert detector.detect(normalize_tool(make_tool(description="send a copy"))) == []


@pytest.mark.parametrize(
    "text",
    [
        "[]",
        "rules: {}",
        "rules: []\nother: true",
        "rules:\n  - id: bad\n",
        VALID.replace("TST-001", "TST-001\n  - id: TST-001"),
        VALID.replace("fields: [description]", "fields: [unsupported]"),
        VALID.replace("patterns: [send a copy]", "patterns: []"),
        VALID.replace("score: 10", "score: 99"),
        VALID.replace("confidence: 0.8", "confidence: 2"),
    ],
)
def test_invalid_rule_files(tmp_path: Path, text: str) -> None:
    with pytest.raises(RuleValidationError):
        load_rules(write(tmp_path, text))


def test_unsafe_python_yaml_is_rejected(tmp_path: Path) -> None:
    payload = "rules: !!python/object/apply:os.system ['echo unsafe']"
    with pytest.raises(RuleValidationError):
        load_rules(write(tmp_path, payload))
