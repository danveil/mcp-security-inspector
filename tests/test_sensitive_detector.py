import pytest
from conftest import make_tool

from mcpsec.detectors.sensitive_data import SensitiveDataDetector
from mcpsec.normalizer import normalize_tool


@pytest.mark.parametrize(
    "term", ["password", "API key", "access token", "private key", "cookie", "environment variable", "secret"]
)
def test_sensitive_terms(term: str) -> None:
    findings = SensitiveDataDetector().detect(normalize_tool(make_tool(description=f"Accept a {term}.")))
    assert findings[0].rule_id == "SEC-001"


def test_schema_property_name() -> None:
    tool = normalize_tool(
        make_tool(inputSchema={"type": "object", "properties": {"refresh_token": {"type": "string"}}})
    )
    assert SensitiveDataDetector().detect(tool)[0].field.startswith("input_schema")


def test_legitimate_context_lowers_severity() -> None:
    tool = normalize_tool(make_tool(name="password_manager", description="Password manager credential rotation."))
    finding = SensitiveDataDetector().detect(tool)[0]
    assert finding.severity == "LOW"
    assert finding.score_contribution == 6
