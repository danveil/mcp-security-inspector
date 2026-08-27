import pytest
from conftest import make_tool

from mcpsec.detectors.permissions import PermissionsDetector, capability_signals, capability_signals_for_text
from mcpsec.normalizer import normalize_tool


@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("Read files from the selected path.", "filesystem_read"),
        ("Overwrite files in the workspace.", "filesystem_write"),
        ("Delete directories from storage.", "file_delete"),
        ("Launch a local process.", "process_execution"),
        ("Upload data to a remote endpoint.", "outbound_network"),
        ("Query records in the database.", "database_read"),
        ("Update rows in a database.", "database_write"),
        ("Access passwords from the authentication store.", "credential_access"),
        ("Return secret values to the caller.", "secret_output"),
        ("Wipe data from the system.", "destructive_operation"),
    ],
)
def test_structured_capability_categories(text: str, category: str) -> None:
    assert category in {item.category for item in capability_signals_for_text(text, "description")}


def test_structured_capabilities_preserve_nested_paths() -> None:
    tool = normalize_tool(make_tool(_meta={"operations": ["Launch a local process."]}))
    signal = next(item for item in capability_signals(tool) if item.category == "process_execution")
    assert signal.field == "metadata.operations[0]"


@pytest.mark.parametrize(
    ("overrides", "expected_field"),
    [
        (
            {"inputSchema": {"type": "object", "description": "Launch a local process."}},
            "input_schema.description",
        ),
        (
            {"outputSchema": {"type": "object", "description": "Return secret values."}},
            "output_schema.description",
        ),
        ({"annotations": {"operation": "Delete files from storage."}}, "annotations.operation"),
        ({"execution": {"operation": "Upload data to a remote endpoint."}}, "execution.operation"),
        ({"vendor": {"operation": "Query records in the database."}}, "unknown_fields.vendor.operation"),
    ],
)
def test_structured_capabilities_cover_all_metadata_containers(
    overrides: dict[str, object], expected_field: str
) -> None:
    tool = normalize_tool(make_tool(**overrides))
    assert expected_field in {item.field for item in capability_signals(tool)}


def test_structured_capability_order_is_deterministic() -> None:
    first = normalize_tool(make_tool(_meta={"z": "Launch a local process.", "a": "Upload data to a remote endpoint."}))
    second = normalize_tool(make_tool(_meta={"a": "Upload data to a remote endpoint.", "z": "Launch a local process."}))
    assert capability_signals(first) == capability_signals(second)


@pytest.mark.parametrize(
    "text",
    [
        "Does not execute commands.",
        "Simulation only: upload data to a remote endpoint.",
        "Dry-run mode would delete files from storage.",
        "Produces a plan without writing files.",
    ],
)
def test_nonoperative_capability_context_is_clean(text: str) -> None:
    assert capability_signals_for_text(text, "description") == ()


def test_cap_001_remains_informational() -> None:
    tool = normalize_tool(make_tool(description="Delete files from storage."))
    finding = PermissionsDetector().detect(tool)[0]
    assert finding.rule_id == "CAP-001"
    assert finding.severity == "INFORMATIONAL"
