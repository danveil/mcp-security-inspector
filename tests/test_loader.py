import json
from pathlib import Path

import pytest
from conftest import make_tool

from mcpsec.constants import MAX_INPUT_BYTES
from mcpsec.exceptions import InputError
from mcpsec.loader import extract_tools, load_json, load_tools


def test_single_tool() -> None:
    assert extract_tools(make_tool())[0]["name"] == "calculator"


def test_tool_array() -> None:
    assert len(extract_tools([make_tool(), make_tool(name="two")])) == 2


def test_direct_tools_response() -> None:
    assert len(extract_tools({"tools": [make_tool()]})) == 1


def test_jsonrpc_tools_list_response() -> None:
    payload = {"jsonrpc": "2.0", "result": {"tools": [make_tool()]}}
    assert extract_tools(payload)[0]["name"] == "calculator"


@pytest.mark.parametrize("payload", [{}, {"result": {}}, "text", 7, None])
def test_unsupported_shape(payload: object) -> None:
    with pytest.raises(InputError):
        extract_tools(payload)


@pytest.mark.parametrize("payload", [{"tools": {}}, {"tools": ["bad"]}, {"result": {"tools": 1}}])
def test_invalid_collection(payload: object) -> None:
    with pytest.raises(InputError):
        extract_tools(payload)


def test_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(InputError, match="Invalid JSON"):
        load_json(path)


def test_utf8_bom(tmp_path: Path) -> None:
    path = tmp_path / "bom.json"
    path.write_text(json.dumps(make_tool()), encoding="utf-8-sig")
    assert load_tools(path)[0]["name"] == "calculator"


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(InputError, match="Cannot read"):
        load_json(tmp_path / "missing.json")


def test_size_limit(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / "large.json"
    path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(Path, "stat", lambda self: type("S", (), {"st_size": MAX_INPUT_BYTES + 1})())
    with pytest.raises(InputError, match="exceeds"):
        load_json(path)
