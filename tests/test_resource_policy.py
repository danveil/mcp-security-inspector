from pathlib import Path

import pytest

import mcpsec.resource_policy as policy
from mcpsec.resource_policy import ResourcePolicyError, load_bounded_yaml, validate_structure


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "policy.yml"
    path.write_text(text, encoding="utf-8")
    return path


def test_structure_node_count_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(policy, "MAX_STRUCTURE_NODES", 3)
    with pytest.raises(ResourcePolicyError, match="node limit"):
        validate_structure({"items": [1, 2]}, label="Input")


def test_yaml_node_expansion_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(policy, "MAX_YAML_NODES", 4)
    with pytest.raises(ResourcePolicyError, match="node expansion limit"):
        load_bounded_yaml(_write(tmp_path, "items: [one, two, three]\n"), max_bytes=1_024, label="Policy")


def test_yaml_nesting_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(policy, "MAX_YAML_DEPTH", 1)
    with pytest.raises(ResourcePolicyError, match="nesting"):
        load_bounded_yaml(_write(tmp_path, "outer:\n  inner:\n    value: true\n"), max_bytes=1_024, label="Policy")


def test_yaml_scalar_size_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(policy, "MAX_YAML_SCALAR_LENGTH", 4)
    with pytest.raises(ResourcePolicyError, match="scalar"):
        load_bounded_yaml(_write(tmp_path, "value: oversized\n"), max_bytes=1_024, label="Policy")
