from conftest import make_tool

from mcpsec.detectors.schema import SchemaDetector, schema_error
from mcpsec.normalizer import normalize_tool


def test_valid_schema() -> None:
    assert schema_error({"type": "object"}) is None


def test_malformed_schema() -> None:
    assert schema_error({"type": 7}) is not None


def test_schema_detector_reports_malformed() -> None:
    tool = normalize_tool(make_tool(inputSchema={"type": 7}))
    assert "SCH-001" in {item.rule_id for item in SchemaDetector().detect(tool)}


def test_privileged_single_parameter() -> None:
    tool = normalize_tool(
        make_tool(inputSchema={"type": "object", "properties": {"shell_command": {"type": "string"}}})
    )
    finding = next(item for item in SchemaDetector().detect(tool) if item.rule_id == "SCH-002")
    assert finding.severity == "MEDIUM"


def test_privileged_combination_is_high() -> None:
    schema = {"type": "object", "properties": {"command": {}, "environment": {}, "password": {}}}
    finding = next(
        item
        for item in SchemaDetector().detect(normalize_tool(make_tool(inputSchema=schema)))
        if item.rule_id == "SCH-002"
    )
    assert finding.severity == "HIGH"


def test_output_schema_is_validated() -> None:
    tool = normalize_tool(make_tool(outputSchema={"type": 1}))
    assert any(item.field == "output_schema" for item in SchemaDetector().detect(tool))
