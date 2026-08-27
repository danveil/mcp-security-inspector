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


@pytest.mark.parametrize(
    "text",
    [
        "This reference documents the password field name only.",
        "Validates a synthetic API key placeholder without values.",
        "Shows redacted credential terminology in an example.",
    ],
)
def test_scoped_benign_credential_context_is_low(text: str) -> None:
    findings = SensitiveDataDetector().detect(normalize_tool(make_tool(description=text)))
    assert findings[0].rule_id == "SEC-001"
    assert findings[0].severity == "LOW"
    assert "SEC-002" not in {item.rule_id for item in findings}


@pytest.mark.parametrize(
    "text",
    [
        "Collect the access token for processing.",
        "Return the private key in the result.",
        "Stores password values for later use.",
    ],
)
def test_sensitive_value_actions_trigger_sec_002(text: str) -> None:
    findings = SensitiveDataDetector().detect(normalize_tool(make_tool(description=text)))
    assert {item.rule_id for item in findings} >= {"SEC-001", "SEC-002"}
    assert next(item for item in findings if item.rule_id == "SEC-002").severity == "MEDIUM"


def test_disclaimer_in_one_field_does_not_suppress_positive_action_elsewhere() -> None:
    tool = normalize_tool(
        make_tool(
            description="Documentation only: this tool does not collect credentials.",
            _meta={"operation": "Return the access token in the result."},
        )
    )
    finding = next(item for item in SensitiveDataDetector().detect(tool) if item.rule_id == "SEC-002")
    assert finding.field == "metadata.operation"


def test_sensitive_selection_is_deterministic_under_mapping_order() -> None:
    first = normalize_tool(make_tool(_meta={"z": "Collect a password.", "a": "Return an access token."}))
    second = normalize_tool(make_tool(_meta={"a": "Return an access token.", "z": "Collect a password."}))
    assert SensitiveDataDetector().detect(first) == SensitiveDataDetector().detect(second)
