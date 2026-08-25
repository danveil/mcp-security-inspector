import pytest
from conftest import make_tool

from mcpsec.constants import MAX_NESTING_DEPTH, MAX_TEXT_LENGTH
from mcpsec.exceptions import InputError
from mcpsec.normalizer import normalize_tool, normalize_tools


def test_aliases_and_known_fields() -> None:
    tool = normalize_tool(make_tool(input_schema={"type": "object"}, inputSchema=None))
    assert tool.input_schema == {}


def test_unknown_fields_preserved() -> None:
    tool = normalize_tool(make_tool(future={"x": 1}))
    assert tool.unknown_fields == {"future": {"x": 1}}


def test_unicode_nfc() -> None:
    tool = normalize_tool(make_tool(description="Cafe\u0301"))
    assert tool.description == "Café"


def test_source_preserved() -> None:
    assert normalize_tool(make_tool(), "fixture").source == "fixture"


def test_meta_alias() -> None:
    assert normalize_tool(make_tool(_meta={"x": 1})).metadata == {"x": 1}


def test_output_and_icons() -> None:
    tool = normalize_tool(make_tool(outputSchema={"type": "object"}, icons=[{"src": "data:"}]))
    assert tool.output_schema == {"type": "object"}
    assert tool.icons[0]["src"] == "data:"


@pytest.mark.parametrize(
    "raw, message",
    [
        ({}, "name"),
        (make_tool(name=""), "name"),
        (make_tool(name=3), "name"),
        (make_tool(description=3), "description"),
        (make_tool(title=3), "title"),
        (make_tool(inputSchema=[]), "inputSchema"),
        (make_tool(icons=["bad"]), "icons"),
        (make_tool(_meta=[]), "_meta"),
    ],
)
def test_invalid_fields(raw: dict[str, object], message: str) -> None:
    with pytest.raises(InputError, match=message):
        normalize_tool(raw)


def test_duplicate_names() -> None:
    with pytest.raises(InputError, match="Duplicate"):
        normalize_tools([make_tool(), make_tool()])


def test_description_is_bounded() -> None:
    tool = normalize_tool(make_tool(description="x" * (MAX_TEXT_LENGTH + 5)))
    assert len(tool.description) == MAX_TEXT_LENGTH


def test_deeply_nested_metadata_is_rejected() -> None:
    nested: dict[str, object] = {}
    current = nested
    for _ in range(MAX_NESTING_DEPTH + 1):
        child: dict[str, object] = {}
        current["child"] = child
        current = child
    with pytest.raises(InputError, match="nesting"):
        normalize_tool(make_tool(_meta=nested))


def test_duplicate_keys_after_normalization_are_rejected() -> None:
    with pytest.raises(InputError, match="duplicate keys"):
        normalize_tool(make_tool(_meta={"Café": 1, "Cafe\u0301": 2}))
