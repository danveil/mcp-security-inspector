from conftest import make_tool

from mcpsec.detectors.mismatch import MismatchDetector, categories
from mcpsec.normalizer import normalize_tool


def test_category_mapping() -> None:
    assert {"weather", "shell"} <= categories("weather shell command")


def test_weather_shell_mismatch() -> None:
    schema = {"type": "object", "properties": {"shell_command": {}, "filesystem_path": {}}}
    tool = normalize_tool(make_tool(name="weather", description="Get weather.", inputSchema=schema))
    assert MismatchDetector().detect(tool)[0].rule_id == "MIS-001"


def test_terminal_command_is_aligned() -> None:
    schema = {"type": "object", "properties": {"command": {}}}
    tool = normalize_tool(make_tool(name="terminal", description="Run a shell command.", inputSchema=schema))
    assert MismatchDetector().detect(tool) == []


def test_no_high_impact_schema_is_clean() -> None:
    assert MismatchDetector().detect(normalize_tool(make_tool())) == []


def test_generic_query_is_not_inferred_as_database() -> None:
    schema = {"type": "object", "properties": {"query": {"type": "string"}}}
    tool = normalize_tool(make_tool(name="document_helper", inputSchema=schema))
    assert MismatchDetector().detect(tool) == []
