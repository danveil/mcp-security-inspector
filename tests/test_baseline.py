from pathlib import Path

import pytest
from conftest import make_tool

from mcpsec.baseline import create_baseline, load_baseline, write_baseline
from mcpsec.exceptions import InputError
from mcpsec.normalizer import normalize_tool


def test_create_baseline() -> None:
    baseline = create_baseline([normalize_tool(make_tool())], "fixture", "2026-01-01T00:00:00+00:00")
    assert baseline.application_version == "0.2.0"
    assert baseline.format_version == "1.0"
    assert baseline.created_at.startswith("2026")
    assert baseline.tools[0].name == "calculator"


def test_summary_excludes_description_and_values() -> None:
    baseline = create_baseline([normalize_tool(make_tool(description="secret value"))], "fixture")
    serialized = baseline.model_dump_json()
    assert "secret value" not in serialized


def test_summary_contains_property_names() -> None:
    baseline = create_baseline([normalize_tool(make_tool())], "fixture")
    assert baseline.tools[0].summary["input_properties"] == ["a", "b"]


def test_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "baseline.json"
    baseline = create_baseline([normalize_tool(make_tool())], "fixture")
    write_baseline(baseline, path)
    assert load_baseline(path) == baseline


def test_invalid_baseline(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(InputError, match="Invalid baseline"):
        load_baseline(path)


def test_timestamp_generated() -> None:
    assert "+00:00" in create_baseline([], "fixture").created_at


def test_baseline_file_size_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "large.json"
    path.write_text('{"data":"more than twenty bytes"}', encoding="utf-8")
    monkeypatch.setattr("mcpsec.baseline.MAX_BASELINE_BYTES", 20)
    with pytest.raises(InputError, match="byte limit"):
        load_baseline(path)
