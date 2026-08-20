import base64

import pytest
from conftest import make_tool

from mcpsec.detectors.obfuscation import ObfuscationDetector, escaped_invisible
from mcpsec.normalizer import normalize_tool


@pytest.mark.parametrize("char", ["\u200b", "\u200c", "\u200d", "\u2060", "\ufeff"])
def test_zero_width(char: str) -> None:
    finding = ObfuscationDetector().detect(normalize_tool(make_tool(description=f"a{char}b")))[0]
    assert finding.rule_id == "OBF-001"
    assert "U+" in finding.evidence


@pytest.mark.parametrize("char", ["\u202e", "\u2066", "\u2069"])
def test_bidi_is_high(char: str) -> None:
    finding = ObfuscationDetector().detect(normalize_tool(make_tool(description=f"a{char}b")))[0]
    assert finding.severity == "HIGH"


def test_invisible_escape_helper() -> None:
    assert "ZERO WIDTH SPACE" in escaped_invisible("x\u200by")


def test_long_description() -> None:
    ids = {item.rule_id for item in ObfuscationDetector().detect(normalize_tool(make_tool(description="x" * 12_001)))}
    assert "OBF-002" in ids


def test_extreme_whitespace() -> None:
    findings = ObfuscationDetector().detect(normalize_tool(make_tool(description="a" + " " * 101 + "b")))
    assert "OBF-003" in {item.rule_id for item in findings}


def test_valid_base64_block() -> None:
    encoded = base64.b64encode(b"A" * 80).decode()
    findings = ObfuscationDetector().detect(normalize_tool(make_tool(description=encoded)))
    assert "OBF-004" in {item.rule_id for item in findings}


def test_short_text_clean() -> None:
    assert ObfuscationDetector().detect(normalize_tool(make_tool())) == []
