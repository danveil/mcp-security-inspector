import json
from pathlib import Path

import pytest

from mcpsec.baseline import load_baseline
from mcpsec.evaluation.comparison import load_evaluation_artifact
from mcpsec.evaluation.loader import load_manifest
from mcpsec.exceptions import CorpusValidationError, ExperimentArtifactError, InputError, RuleValidationError
from mcpsec.loader import load_json, load_tools
from mcpsec.resource_policy import StrictJsonError, strict_json_loads
from mcpsec.rules.loader import load_rule_pack
from mcpsec.suppressions import load_suppressions


@pytest.mark.parametrize(
    "payload, key",
    [
        ('{"name":"first","name":"second"}', "name"),
        ('{"outer":{"safe":1,"safe":2}}', "safe"),
    ],
)
def test_duplicate_json_keys_are_rejected_at_any_depth(payload: str, key: str) -> None:
    with pytest.raises(StrictJsonError, match=rf"duplicate object key.*{key}"):
        strict_json_loads(payload)


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_json_numbers_are_rejected(constant: str) -> None:
    with pytest.raises(StrictJsonError, match=rf"non-finite number {constant}"):
        strict_json_loads(f'{{"value":{constant}}}')


def test_valid_ordinary_unicode_json_is_accepted() -> None:
    assert strict_json_loads('{"message":"Café 東京","value":1.25}') == {
        "message": "Café 東京",
        "value": 1.25,
    }


def test_large_bounded_valid_json_is_accepted(tmp_path: Path) -> None:
    path = tmp_path / "large-valid.json"
    description = "x" * 90_000
    path.write_text(
        json.dumps({"name": "large", "description": description, "inputSchema": {"type": "object"}}),
        encoding="utf-8",
    )
    assert load_tools(path)[0]["description"] == description


@pytest.mark.parametrize(
    "payload",
    [
        '{"name":"safe","name":"changed","inputSchema":{"type":"object"}}',
        '{"name":"safe","inputSchema":{"type":"object","type":"array"}}',
        '{"name":"safe","inputSchema":{"type":"object"},"value":NaN}',
        '{"name":"safe","inputSchema":{"type":"object"},"value":Infinity}',
        '{"name":"safe","inputSchema":{"type":"object"},"value":-Infinity}',
    ],
)
def test_scan_input_uses_strict_json(payload: str, tmp_path: Path) -> None:
    path = tmp_path / "scan.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(InputError, match="Invalid JSON input"):
        load_json(path)


def test_manifest_uses_strict_json(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text('{"corpus_name":"one","corpus_name":"two"}', encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="duplicate object key"):
        load_manifest(path)


def test_baseline_uses_strict_json(tmp_path: Path) -> None:
    path = tmp_path / "baseline.json"
    path.write_text('{"format_version":"1.0","format_version":"2.0"}', encoding="utf-8")
    with pytest.raises(InputError, match="duplicate object key"):
        load_baseline(path)


def test_experiment_artifact_uses_strict_json(tmp_path: Path) -> None:
    path = tmp_path / "artifact.json"
    path.write_text('{"metadata":{},"metadata":{}}', encoding="utf-8")
    with pytest.raises(ExperimentArtifactError, match="duplicate object key"):
        load_evaluation_artifact(path)


@pytest.mark.parametrize("kind", ["rules", "suppressions"])
def test_json_configuration_files_use_strict_json(kind: str, tmp_path: Path) -> None:
    path = tmp_path / f"{kind}.json"
    path.write_text(f'{{"{kind}":[],"{kind}":[]}}', encoding="utf-8")
    with pytest.raises(RuleValidationError, match="duplicate object key"):
        if kind == "rules":
            load_rule_pack(path)
        else:
            load_suppressions(path, set())
