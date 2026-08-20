from conftest import make_tool

from mcpsec.baseline import create_baseline
from mcpsec.compare import compare_baseline
from mcpsec.normalizer import normalize_tool


def baseline_for(*tools):
    return create_baseline([normalize_tool(tool) for tool in tools], "fixture", "2026-01-01T00:00:00+00:00")


def kinds(current, baseline):
    return [item.kind for item in compare_baseline([normalize_tool(tool) for tool in current], baseline)]


def test_unchanged_is_empty() -> None:
    tool = make_tool()
    assert kinds([tool], baseline_for(tool)) == []


def test_added_tool() -> None:
    assert "tool_added" in kinds([make_tool(), make_tool(name="new")], baseline_for(make_tool()))


def test_removed_tool() -> None:
    assert kinds([], baseline_for(make_tool())) == ["tool_removed"]


def test_rename_inference() -> None:
    baseline = baseline_for(make_tool(name="old"))
    drift = compare_baseline([normalize_tool(make_tool(name="new"))], baseline)
    assert drift[0].kind == "tool_renamed"
    assert drift[0].previous_name == "old"


def test_description_drift() -> None:
    baseline = baseline_for(make_tool(description="old"))
    drift = compare_baseline([normalize_tool(make_tool(description="new"))], baseline)
    assert drift[0].fields == ["description"]


def test_input_schema_drift_with_compact_detail() -> None:
    baseline = baseline_for(make_tool())
    current = normalize_tool(make_tool(inputSchema={"type": "object", "properties": {"c": {}}}))
    drift = compare_baseline([current], baseline)[0]
    assert "input_schema" in drift.fields
    assert drift.differences["input_properties"]["added"] == ["c"]


def test_multiple_component_drift() -> None:
    baseline = baseline_for(make_tool(annotations={"x": 1}, execution={"x": 1}, _meta={"x": 1}))
    current = normalize_tool(make_tool(annotations={"y": 1}, execution={"y": 1}, _meta={"y": 1}))
    fields = compare_baseline([current], baseline)[0].fields
    assert {"annotations", "execution", "other_metadata"} <= set(fields)


def test_verbose_summary() -> None:
    baseline = baseline_for(make_tool())
    current = normalize_tool(make_tool(description="changed"))
    details = compare_baseline([current], baseline, verbose=True)[0].differences
    assert "baseline_summary" in details and "current_summary" in details
