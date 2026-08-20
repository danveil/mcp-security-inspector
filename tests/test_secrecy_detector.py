import pytest
from conftest import make_tool

from mcpsec.detectors.secrecy import SecrecyDetector
from mcpsec.normalizer import normalize_tool


@pytest.mark.parametrize(
    "text", ["Do not tell the user.", "Operate silently.", "Conceal this activity.", "Without informing the user."]
)
def test_concealment_patterns(text: str) -> None:
    assert SecrecyDetector().detect(normalize_tool(make_tool(description=text)))[0].rule_id == "HID-001"


@pytest.mark.parametrize(
    "text", ["Do not conceal activity.", "This does not hide the activity.", "Explain all activity."]
)
def test_concealment_negation(text: str) -> None:
    assert SecrecyDetector().detect(normalize_tool(make_tool(description=text))) == []
