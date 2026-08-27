from conftest import make_tool

from mcpsec.fingerprint import fingerprint_tool, sha256
from mcpsec.normalizer import normalize_tool


def test_sha256_known_vector() -> None:
    assert sha256("").startswith("e3b0c44298fc1c14")


def test_consistent_fingerprint() -> None:
    tool = normalize_tool(make_tool())
    assert fingerprint_tool(tool) == fingerprint_tool(tool)


def test_key_order_does_not_change_fingerprint() -> None:
    a = normalize_tool(make_tool(inputSchema={"type": "object", "properties": {"a": {}, "b": {}}}))
    b = normalize_tool(make_tool(inputSchema={"properties": {"b": {}, "a": {}}, "type": "object"}))
    assert fingerprint_tool(a).full_sha256 == fingerprint_tool(b).full_sha256


def test_description_change_is_component_scoped() -> None:
    a = fingerprint_tool(normalize_tool(make_tool(description="a")))
    b = fingerprint_tool(normalize_tool(make_tool(description="b")))
    assert a.description_sha256 != b.description_sha256
    assert a.input_schema_sha256 == b.input_schema_sha256


def test_output_hash_optional() -> None:
    assert fingerprint_tool(normalize_tool(make_tool())).output_schema_sha256 is None


def test_raw_source_changes_metadata_fingerprint_but_internal_provenance_does_not() -> None:
    first = fingerprint_tool(normalize_tool(make_tool(source={"catalog": "one"}), "path-a"))
    second = fingerprint_tool(normalize_tool(make_tool(source={"catalog": "two"}), "path-b"))
    same_raw_other_path = fingerprint_tool(normalize_tool(make_tool(source={"catalog": "one"}), "path-c"))
    assert first.metadata_sha256 != second.metadata_sha256
    assert first.full_sha256 != second.full_sha256
    assert first == same_raw_other_path
