import json
from pathlib import Path

import pytest

from mcpsec.evaluation.loader import load_corpus, load_manifest
from mcpsec.evaluation.models import CorpusSplit, Difficulty, ProvenanceOrigin
from mcpsec.exceptions import CorpusValidationError


def write_manifest(tmp_path: Path, samples: list[dict[str, object]]) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(
            {
                "corpus_name": "test-corpus",
                "corpus_version": "1.0.0",
                "description": "A sufficiently descriptive test corpus.",
                "samples": samples,
            }
        ),
        encoding="utf-8",
    )
    return path


def sample(sample_id: str = "sample_001", file: str = "tool.json") -> dict[str, object]:
    return {
        "id": sample_id,
        "file": file,
        "source_type": "tool_definition",
        "expected": "benign",
        "categories": [],
        "rationale": "This is an ordinary benign test tool.",
    }


def test_valid_single_tool_corpus(tmp_path: Path) -> None:
    (tmp_path / "tool.json").write_text(
        json.dumps({"name": "safe", "description": "Safe.", "inputSchema": {"type": "object"}}),
        encoding="utf-8",
    )
    manifest, loaded = load_corpus(write_manifest(tmp_path, [sample()]))
    assert manifest.corpus_version == "1.0.0"
    assert manifest.split == CorpusSplit.development
    assert loaded[0].tool.name == "safe"


def test_research_metadata_and_legacy_difficulty_migration(tmp_path: Path) -> None:
    value = sample()
    value.update(
        {
            "difficulty": "borderline",
            "field_locations": ["description", "inputSchema.properties.token.description"],
            "provenance": {
                "origin_type": "derived",
                "source_reference": "public-fixture-001",
                "derivation_notes": "Identifiers were replaced with harmless synthetic values.",
            },
        }
    )
    path = write_manifest(tmp_path, [value])
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw.update(
        {
            "split": "holdout",
            "methodology_version": "1.2.0",
            "methodology_note": "Labels were frozen before this evaluation run.",
            "label_review_status": "independently_reviewed",
            "source_license_policy": "Only redistributable public fixtures are accepted.",
        }
    )
    path.write_text(json.dumps(raw), encoding="utf-8")
    manifest = load_manifest(path)
    assert manifest.split == CorpusSplit.holdout
    assert manifest.samples[0].difficulty == Difficulty.moderate
    assert manifest.samples[0].provenance.origin_type == ProvenanceOrigin.derived


@pytest.mark.parametrize("location", ["", ".description", "inputSchema..token", "inputSchema/token", "items[bad]"])
def test_invalid_field_location_is_rejected(tmp_path: Path, location: str) -> None:
    value = sample()
    value["field_locations"] = [location]
    with pytest.raises(CorpusValidationError, match="field_locations"):
        load_manifest(write_manifest(tmp_path, [value]))


@pytest.mark.parametrize(
    ("manifest_mutation", "sample_mutation", "message"),
    [
        ({"split": "training"}, {}, "split"),
        ({}, {"difficulty": "ambiguous"}, "difficulty"),
        ({}, {"provenance": {"origin_type": "borrowed"}}, "origin_type"),
    ],
)
def test_invalid_research_enums_are_rejected(
    tmp_path: Path,
    manifest_mutation: dict[str, object],
    sample_mutation: dict[str, object],
    message: str,
) -> None:
    value = sample()
    value.update(sample_mutation)
    path = write_manifest(tmp_path, [value])
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw.update(manifest_mutation)
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(CorpusValidationError, match=message):
        load_manifest(path)


@pytest.mark.parametrize(
    ("mutations", "message"),
    [
        ({"expected": "unknown"}, "expected"),
        ({"expected": "suspicious", "categories": []}, "require at least one"),
        ({"categories": ["schema"]}, "benign samples cannot"),
        ({"expected": "suspicious", "categories": ["not_real"]}, "unknown categories"),
    ],
)
def test_invalid_ground_truth(tmp_path: Path, mutations: dict[str, object], message: str) -> None:
    value = sample()
    value.update(mutations)
    with pytest.raises(CorpusValidationError, match=message):
        load_manifest(write_manifest(tmp_path, [value]))


def test_duplicate_sample_ids(tmp_path: Path) -> None:
    with pytest.raises(CorpusValidationError, match="unique"):
        load_manifest(write_manifest(tmp_path, [sample(), sample()]))


def test_empty_corpus(tmp_path: Path) -> None:
    with pytest.raises(CorpusValidationError, match="at least 1"):
        load_manifest(write_manifest(tmp_path, []))


def test_missing_sample_file(tmp_path: Path) -> None:
    with pytest.raises(CorpusValidationError, match="Sample sample_001"):
        load_corpus(write_manifest(tmp_path, [sample(file="missing.json")]))


def test_path_escape_rejected(tmp_path: Path) -> None:
    with pytest.raises(CorpusValidationError, match="escapes"):
        load_corpus(write_manifest(tmp_path, [sample(file="../outside.json")]))


def test_catalog_requires_valid_tool_selection(tmp_path: Path) -> None:
    (tmp_path / "tool.json").write_text(
        json.dumps(
            [
                {"name": "one", "inputSchema": {"type": "object"}},
                {"name": "two", "inputSchema": {"type": "object"}},
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(CorpusValidationError, match="tool_name is required"):
        load_corpus(write_manifest(tmp_path, [sample()]))


def test_named_catalog_selection(tmp_path: Path) -> None:
    (tmp_path / "tool.json").write_text(
        json.dumps(
            [
                {"name": "one", "inputSchema": {"type": "object"}},
                {"name": "two", "inputSchema": {"type": "object"}},
            ]
        ),
        encoding="utf-8",
    )
    value = sample()
    value["tool_name"] = "two"
    _, loaded = load_corpus(write_manifest(tmp_path, [value]))
    assert loaded[0].tool.name == "two"


def test_malformed_manifest(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="Cannot load"):
        load_manifest(path)
