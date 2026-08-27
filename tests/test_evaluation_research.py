import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from typer.testing import CliRunner

from mcpsec.cli import app
from mcpsec.evaluation.ablation import resolve_ablation
from mcpsec.evaluation.evaluator import evaluate_corpus
from mcpsec.evaluation.integrity import compare_corpus_splits, corpus_sha256
from mcpsec.evaluation.models import (
    CorpusSplit,
    FailureType,
    GitMetadata,
    IntegrityIssueKind,
    RuntimeEnvironment,
    TimingMode,
)
from mcpsec.evaluation.research import (
    build_evaluation_configuration,
    build_timing_configuration,
    collect_git_metadata,
    collect_runtime_environment,
    configuration_sha256,
)
from mcpsec.exceptions import CorpusValidationError
from mcpsec.models import RuleDefinition, Severity, SuppressionDefinition

ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "evaluation" / "corpus" / "manifest.json"
runner = CliRunner()


def write_corpus(
    root: Path,
    *,
    split: str,
    sample_id: str,
    tool: dict[str, object],
    expected: str = "benign",
    categories: list[str] | None = None,
) -> Path:
    root.mkdir()
    (root / "tool.json").write_text(json.dumps(tool), encoding="utf-8")
    manifest = {
        "corpus_name": f"{split}-test-corpus",
        "corpus_version": "1.0.0",
        "split": split,
        "methodology_version": "1.0.0",
        "methodology_note": "A deterministic research test corpus methodology.",
        "label_review_status": "single_reviewer",
        "description": "A sufficiently descriptive research test corpus.",
        "samples": [
            {
                "id": sample_id,
                "file": "tool.json",
                "source_type": "tool_definition",
                "expected": expected,
                "categories": categories or [],
                "rationale": "A sufficiently descriptive sample rationale.",
            }
        ],
    }
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def test_corpus_hash_is_order_stable_and_content_sensitive(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.json").write_text(json.dumps({"name": "a", "description": "Safe A."}), encoding="utf-8")
    (corpus / "b.json").write_text(json.dumps({"name": "b", "description": "Safe B."}), encoding="utf-8")
    samples = [
        {
            "id": "sample_001",
            "file": "a.json",
            "source_type": "tool_definition",
            "expected": "benign",
            "categories": [],
            "rationale": "An ordinary safe sample for hashing.",
            "expected_rule_ids": ["SEC-001", "PI-001"],
        },
        {
            "id": "sample_002",
            "file": "b.json",
            "source_type": "tool_definition",
            "expected": "benign",
            "categories": [],
            "rationale": "A second ordinary sample for hashing.",
        },
    ]
    payload = {
        "corpus_name": "hash-test",
        "corpus_version": "1.0.0",
        "description": "A sufficiently descriptive hash test corpus.",
        "samples": samples,
    }
    manifest = corpus / "manifest.json"
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    first = corpus_sha256(manifest)

    payload["samples"] = list(reversed(samples))
    samples[0]["expected_rule_ids"] = ["PI-001", "SEC-001"]
    manifest.write_text(json.dumps(payload, indent=4), encoding="utf-8")
    assert corpus_sha256(manifest) == first

    payload["description"] = "A changed but still sufficiently descriptive hash test corpus."
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    changed_manifest = corpus_sha256(manifest)
    assert changed_manifest != first

    (corpus / "a.json").write_text(json.dumps({"name": "a", "description": "Changed."}), encoding="utf-8")
    assert corpus_sha256(manifest) != changed_manifest


def test_configuration_hash_is_semantic_and_order_stable() -> None:
    rule = RuleDefinition(
        id="TST-001",
        name="Test rule",
        category="schema",
        fields=["description", "name"],
        patterns=["second", "first"],
        severity=Severity.MEDIUM,
        confidence=0.8,
        score=10,
        recommendation="Review the metadata.",
    )
    suppressions = [
        SuppressionDefinition(rule_id="PI-001", tool="alpha", justification="Approved test rationale."),
        SuppressionDefinition(rule_id="SEC-001", justification="Approved global test rationale."),
    ]
    first = build_evaluation_configuration(
        threshold=Severity.MEDIUM,
        corpus_split=CorpusSplit.development,
        ablation=resolve_ablation(),
        timing=build_timing_configuration(mode=TimingMode.analysis_core, warmup_repetitions=0, measured_repetitions=1),
        rules=[rule],
        suppressions=suppressions,
        custom_rule_pack_name="research",
        custom_rule_pack_version="1.0.0",
        custom_rule_file_sha256="a" * 64,
        suppression_file_sha256="b" * 64,
    )
    reordered_rule = rule.model_copy(
        update={"fields": list(reversed(rule.fields)), "patterns": list(reversed(rule.patterns))}
    )
    second = build_evaluation_configuration(
        threshold=Severity.MEDIUM,
        corpus_split=CorpusSplit.development,
        ablation=resolve_ablation(),
        timing=build_timing_configuration(mode=TimingMode.analysis_core, warmup_repetitions=0, measured_repetitions=1),
        rules=[reordered_rule],
        suppressions=list(reversed(suppressions)),
        custom_rule_pack_name="research",
        custom_rule_pack_version="1.0.0",
        custom_rule_file_sha256="c" * 64,
        suppression_file_sha256="d" * 64,
    )
    assert configuration_sha256(first) == configuration_sha256(second)

    changed = first.model_copy(update={"suspicious_threshold": Severity.HIGH})
    assert configuration_sha256(changed) != configuration_sha256(first)


def test_git_metadata_clean_dirty_and_unavailable(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    commit = "a" * 40

    def clean_git(arguments: list[str], working_directory: Path) -> str | None:
        assert working_directory == tmp_path.resolve()
        return commit if arguments[0] == "rev-parse" else ""

    monkeypatch.setattr("mcpsec.evaluation.research._run_git", clean_git)
    assert collect_git_metadata(tmp_path) == GitMetadata(commit=commit, dirty=False)

    def dirty_git(arguments: list[str], working_directory: Path) -> str | None:
        return commit if arguments[0] == "rev-parse" else " M src/file.py"

    monkeypatch.setattr("mcpsec.evaluation.research._run_git", dirty_git)
    assert collect_git_metadata(tmp_path).dirty is True
    monkeypatch.setattr("mcpsec.evaluation.research._run_git", lambda arguments, working_directory: None)
    assert collect_git_metadata(tmp_path) == GitMetadata()


def test_git_metadata_without_git_executable(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr("mcpsec.evaluation.research.shutil.which", lambda executable: None)
    assert collect_git_metadata(tmp_path) == GitMetadata()


def test_runtime_metadata_does_not_capture_environment_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MCPSEC_RESEARCH_TEST_SECRET", "must-not-appear")
    monkeypatch.setattr("mcpsec.evaluation.research.platform.processor", lambda: "")
    environment = collect_runtime_environment()
    serialized = json.dumps(environment.model_dump(mode="json"))
    assert "must-not-appear" not in serialized
    assert "MCPSEC_RESEARCH_TEST_SECRET" not in serialized
    assert environment.processor is None


def test_evaluation_artifact_contains_research_identity_and_failure_context() -> None:
    fixed_time = datetime(2026, 8, 27, 12, 34, 56, tzinfo=UTC)
    environment = RuntimeEnvironment(
        python_version="3.12.test",
        platform_system="TestOS",
        platform_release="1",
        machine="test-machine",
        dependency_versions={"pydantic": "test"},
    )
    report = evaluate_corpus(
        MANIFEST,
        git_metadata=GitMetadata(commit="a" * 40, dirty=False),
        runtime_environment=environment,
        timestamp_factory=lambda: fixed_time,
        invocation=["mcpsec", "evaluate", str(MANIFEST.resolve()), "--format", "json"],
    )
    metadata = report.metadata
    assert metadata.corpus_split == CorpusSplit.development
    assert metadata.label_review_status == "single_reviewer"
    assert metadata.corpus_methodology_version == "1.0.0"
    assert len(metadata.corpus_sha256) == 64
    assert len(metadata.configuration_sha256) == 64
    assert metadata.experiment_id.startswith("exp-20260827T123456")
    assert metadata.git.commit == "a" * 40 and metadata.git.dirty is False
    assert metadata.invocation[2] == "manifest.json"
    assert str(ROOT.resolve()) not in json.dumps(report.model_dump(mode="json"))
    assert all(item.provenance.origin_type == "synthetic" for item in report.samples)
    assert all(item.difficulty.value in {"obvious", "moderate", "subtle"} for item in report.samples)
    assert {item.failure_type for item in report.false_positives} == {FailureType.false_positive}
    assert {item.failure_type for item in report.false_negatives} == {FailureType.false_negative_below_threshold}
    assert all(item.triggered_rule_ids == sorted(set(item.triggered_rule_ids)) for item in report.samples)


def test_false_negative_without_any_finding_is_classified(tmp_path: Path) -> None:
    manifest = write_corpus(
        tmp_path / "development",
        split="development",
        sample_id="suspicious_001",
        tool={"name": "calculator", "description": "Adds two numbers.", "inputSchema": {"type": "object"}},
        expected="suspicious",
        categories=["instruction_override"],
    )
    result = evaluate_corpus(
        manifest,
        git_metadata=GitMetadata(),
        timestamp_factory=lambda: datetime(2026, 8, 27, tzinfo=UTC),
    )
    assert result.false_negatives[0].failure_type == FailureType.false_negative_no_finding
    assert result.false_negatives[0].findings == []


def test_cross_split_integrity_detects_duplicate_ids_and_exact_content(tmp_path: Path) -> None:
    tool = {"name": "same", "description": "The same normalized tool content."}
    development = write_corpus(tmp_path / "development", split="development", sample_id="sample_001", tool=tool)
    holdout = write_corpus(tmp_path / "holdout", split="holdout", sample_id="sample_001", tool=tool)
    report = compare_corpus_splits(development, holdout)
    assert not report.passed
    assert {item.kind for item in report.errors} == {
        IntegrityIssueKind.duplicate_sample_id,
        IntegrityIssueKind.exact_normalized_content,
    }
    assert report.warnings == []


def test_cross_split_integrity_passes_distinct_corpora_and_cli_json(tmp_path: Path) -> None:
    development = write_corpus(
        tmp_path / "development",
        split="development",
        sample_id="development_001",
        tool={"name": "alpha", "description": "Adds numbers."},
    )
    holdout = write_corpus(
        tmp_path / "holdout",
        split="holdout",
        sample_id="holdout_001",
        tool={"name": "beta", "description": "Formats dates."},
    )
    report = compare_corpus_splits(development, holdout)
    assert report.passed
    result = runner.invoke(app, ["corpus-check", str(development), str(holdout), "--format", "json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["errors"] == []


def test_cross_split_cli_fails_on_exact_overlap(tmp_path: Path) -> None:
    tool = {"name": "same", "description": "The same normalized tool content."}
    development = write_corpus(tmp_path / "development", split="development", sample_id="development_001", tool=tool)
    holdout = write_corpus(tmp_path / "holdout", split="holdout", sample_id="holdout_001", tool=tool)
    result = runner.invoke(app, ["corpus-check", str(development), str(holdout), "--format", "json"])
    assert result.exit_code == 1
    assert json.loads(result.stdout)["errors"][0]["kind"] == "exact_normalized_content"


def test_cross_split_integrity_requires_declared_split_roles(tmp_path: Path) -> None:
    development = write_corpus(
        tmp_path / "development",
        split="development",
        sample_id="development_001",
        tool={"name": "alpha"},
    )
    not_holdout = write_corpus(
        tmp_path / "not-holdout",
        split="development",
        sample_id="sample_002",
        tool={"name": "beta"},
    )
    with pytest.raises(CorpusValidationError, match="holdout manifest"):
        compare_corpus_splits(development, not_holdout)
