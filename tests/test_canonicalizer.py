import pytest
from conftest import make_tool

from mcpsec.canonicalizer import canonical_json, canonical_tool, canonical_value
from mcpsec.exceptions import InputError
from mcpsec.normalizer import normalize_tool


def test_key_order_is_deterministic() -> None:
    assert canonical_json({"z": 1, "a": 2}) == '{"a":2,"z":1}'


def test_nested_key_order() -> None:
    assert canonical_json({"x": {"b": 1, "a": 2}}) == '{"x":{"a":2,"b":1}}'


def test_array_order_preserved() -> None:
    assert canonical_json([2, 1]) == "[2,1]"


def test_unicode_nfc_equivalent() -> None:
    assert canonical_json("é") == canonical_json("e\u0301")


def test_unicode_not_ascii_escaped() -> None:
    assert "é" in canonical_json("é")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_rejected(value: float) -> None:
    with pytest.raises(InputError):
        canonical_json(value)


def test_unsupported_value_rejected() -> None:
    with pytest.raises(InputError):
        canonical_value({1, 2})


def test_source_excluded_from_tool_canonicalization() -> None:
    a = normalize_tool(make_tool(), "a")
    b = normalize_tool(make_tool(), "b")
    assert canonical_tool(a) == canonical_tool(b)


def test_absent_raw_source_preserves_prior_canonical_shape() -> None:
    tool = normalize_tool(make_tool())
    expected = tool.model_dump(exclude={"source", "provenance"}, mode="json")
    assert canonical_tool(tool) == canonical_json(expected)


def test_user_supplied_raw_source_is_security_significant() -> None:
    first = normalize_tool(make_tool(source={"catalog": "one"}))
    second = normalize_tool(make_tool(source={"catalog": "two"}))
    assert canonical_tool(first) != canonical_tool(second)
