from __future__ import annotations

import platform
import re
import shutil
import subprocess
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from mcpsec.detectors import BUILTIN_DETECTORS
from mcpsec.evaluation.integrity import canonical_sha256
from mcpsec.evaluation.models import (
    CorpusSplit,
    EvaluationConfiguration,
    GitMetadata,
    RuntimeEnvironment,
    SuppressionIdentity,
)
from mcpsec.models import RuleDefinition, Severity, SuppressionDefinition
from mcpsec.rules import RULE_EXPLANATIONS

DEPENDENCY_DISTRIBUTIONS = (
    "httpx2",
    "jsonschema",
    "mcp",
    "pydantic",
    "PyYAML",
    "rich",
    "typer",
)


def _run_git(arguments: list[str], working_directory: Path) -> str | None:
    executable = shutil.which("git")
    if executable is None:
        return None
    try:
        completed = subprocess.run(  # noqa: S603 - fixed git subcommands; no shell or metadata execution
            [executable, *arguments],
            cwd=working_directory,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=3,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def collect_git_metadata(working_directory: Path | None = None) -> GitMetadata:
    directory = (working_directory or Path.cwd()).resolve()
    commit = _run_git(["rev-parse", "--verify", "HEAD"], directory)
    if commit is None or re.fullmatch(r"[0-9a-fA-F]{40,64}", commit) is None:
        return GitMetadata()
    status = _run_git(["status", "--porcelain", "--untracked-files=normal"], directory)
    return GitMetadata(commit=commit.casefold(), dirty=None if status is None else bool(status))


def collect_runtime_environment() -> RuntimeEnvironment:
    dependencies: dict[str, str] = {}
    for distribution in DEPENDENCY_DISTRIBUTIONS:
        try:
            dependencies[distribution] = version(distribution)
        except PackageNotFoundError:
            dependencies[distribution] = "unavailable"
    processor = platform.processor().strip() or None
    return RuntimeEnvironment(
        python_version=platform.python_version(),
        platform_system=platform.system(),
        platform_release=platform.release(),
        machine=platform.machine(),
        processor=processor,
        dependency_versions=dependencies,
    )


def _semantic_custom_rules(rules: list[RuleDefinition]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for rule in rules:
        payload = rule.model_dump(mode="json")
        payload["fields"] = sorted(payload["fields"])
        payload["patterns"] = sorted(payload["patterns"])
        normalized.append(payload)
    return sorted(normalized, key=lambda item: str(item["id"]))


def build_evaluation_configuration(
    *,
    threshold: Severity,
    corpus_split: CorpusSplit,
    rules: list[RuleDefinition],
    suppressions: list[SuppressionDefinition],
    custom_rule_pack_name: str | None,
    custom_rule_pack_version: str | None,
    custom_rule_file_sha256: str | None,
    suppression_file_sha256: str | None,
) -> EvaluationConfiguration:
    custom_configuration = _semantic_custom_rules(rules)
    return EvaluationConfiguration(
        suspicious_threshold=threshold,
        corpus_split=corpus_split,
        builtin_detector_ids=[
            f"{detector.__class__.__module__}.{detector.__class__.__qualname__}" for detector in BUILTIN_DETECTORS
        ],
        builtin_rule_ids=list(RULE_EXPLANATIONS),
        custom_rule_pack_name=custom_rule_pack_name,
        custom_rule_pack_version=custom_rule_pack_version,
        custom_rule_ids=[rule.id for rule in rules if rule.enabled],
        custom_rule_configuration_sha256=(canonical_sha256(custom_configuration) if rules else None),
        custom_rule_file_sha256=custom_rule_file_sha256,
        suppressions=[SuppressionIdentity(rule_id=item.rule_id, tool=item.tool) for item in suppressions],
        suppression_file_sha256=suppression_file_sha256,
        options={"evidence_redacted": False, "static_analysis_only": True},
    )


def configuration_sha256(configuration: EvaluationConfiguration) -> str:
    payload = configuration.model_dump(
        mode="json",
        exclude={"custom_rule_file_sha256", "suppression_file_sha256"},
    )
    return canonical_sha256(payload)


def utc_now() -> datetime:
    return datetime.now(UTC)


def experiment_id(timestamp: datetime, corpus_digest: str, configuration_digest: str) -> str:
    normalized = timestamp.astimezone(UTC)
    stamp = normalized.strftime("%Y%m%dT%H%M%S%fZ")
    return f"exp-{stamp}-{corpus_digest[:8]}-{configuration_digest[:8]}"
