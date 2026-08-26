from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Any

from mcpsec.canonicalizer import canonical_json
from mcpsec.evaluation.loader import LoadedSample, load_corpus, load_manifest, resolve_sample_path
from mcpsec.evaluation.models import (
    CorpusIdentity,
    CorpusManifest,
    CorpusSplit,
    CrossSplitIntegrityReport,
    IntegrityIssue,
    IntegrityIssueKind,
    IntegritySeverity,
)
from mcpsec.exceptions import CorpusValidationError
from mcpsec.fingerprint import fingerprint_tool
from mcpsec.resource_policy import MAX_INPUT_BYTES, ResourcePolicyError, read_bounded_text


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path, *, max_bytes: int = MAX_INPUT_BYTES, label: str = "Research input") -> str:
    try:
        content = read_bounded_text(path, max_bytes=max_bytes, label=label)
    except (OSError, UnicodeError, ResourcePolicyError) as exc:
        raise CorpusValidationError(f"Cannot hash {label.casefold()}: {exc}") from exc
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _normalized_manifest_payload(manifest: CorpusManifest) -> dict[str, Any]:
    payload = manifest.model_dump(mode="json")
    samples = payload["samples"]
    for sample in samples:
        for key in ("categories", "expected_rule_ids", "field_locations"):
            sample[key] = sorted(sample[key])
    payload["samples"] = sorted(samples, key=lambda sample: sample["id"])
    return payload


def corpus_sha256(manifest_path: Path, manifest: CorpusManifest | None = None) -> str:
    active_manifest = manifest or load_manifest(manifest_path)
    root = manifest_path.resolve().parent
    referenced_files: dict[str, str] = {}
    for entry in active_manifest.samples:
        relative = entry.file.replace("\\", "/")
        if relative not in referenced_files:
            referenced_files[relative] = sha256_file(
                resolve_sample_path(root, entry.file),
                max_bytes=MAX_INPUT_BYTES,
                label=f"Corpus sample file {relative}",
            )
    payload = {
        "manifest": _normalized_manifest_payload(active_manifest),
        "files": [{"path": relative, "sha256": referenced_files[relative]} for relative in sorted(referenced_files)],
    }
    return canonical_sha256(payload)


def _identity(path: Path, manifest: CorpusManifest) -> CorpusIdentity:
    return CorpusIdentity(
        corpus_name=manifest.corpus_name,
        corpus_version=manifest.corpus_version,
        split=manifest.split,
        corpus_sha256=corpus_sha256(path, manifest),
        sample_count=len(manifest.samples),
    )


def _content_index(samples: list[LoadedSample]) -> dict[str, list[str]]:
    index: defaultdict[str, list[str]] = defaultdict(list)
    for sample in samples:
        index[fingerprint_tool(sample.tool).full_sha256].append(sample.entry.id)
    return {digest: sorted(ids) for digest, ids in index.items()}


def compare_corpus_splits(development_path: Path, holdout_path: Path) -> CrossSplitIntegrityReport:
    development_manifest, development_samples = load_corpus(development_path)
    holdout_manifest, holdout_samples = load_corpus(holdout_path)
    if development_manifest.split != CorpusSplit.development:
        raise CorpusValidationError("The development manifest must declare split='development'")
    if holdout_manifest.split != CorpusSplit.holdout:
        raise CorpusValidationError("The holdout manifest must declare split='holdout'")

    errors: list[IntegrityIssue] = []
    development_ids = {sample.entry.id for sample in development_samples}
    holdout_ids = {sample.entry.id for sample in holdout_samples}
    for sample_id in sorted(development_ids & holdout_ids):
        errors.append(
            IntegrityIssue(
                severity=IntegritySeverity.error,
                kind=IntegrityIssueKind.duplicate_sample_id,
                development_sample_ids=[sample_id],
                holdout_sample_ids=[sample_id],
                explanation="A sample ID appears in both development and holdout splits.",
            )
        )

    development_content = _content_index(development_samples)
    holdout_content = _content_index(holdout_samples)
    for digest in sorted(set(development_content) & set(holdout_content)):
        errors.append(
            IntegrityIssue(
                severity=IntegritySeverity.error,
                kind=IntegrityIssueKind.exact_normalized_content,
                development_sample_ids=development_content[digest],
                holdout_sample_ids=holdout_content[digest],
                normalized_content_sha256=digest,
                explanation="Exact canonical tool content appears in both development and holdout splits.",
            )
        )

    return CrossSplitIntegrityReport(
        development=_identity(development_path, development_manifest),
        holdout=_identity(holdout_path, holdout_manifest),
        errors=errors,
        warnings=[],
    )
