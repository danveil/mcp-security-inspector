from __future__ import annotations

from collections import defaultdict

from mcpsec.baseline import _summary
from mcpsec.fingerprint import fingerprint_tool
from mcpsec.models import BaselineFile, BaselineTool, Drift, Fingerprints, ToolDefinition

HASH_FIELDS = {
    "description_sha256": "description",
    "input_schema_sha256": "input_schema",
    "output_schema_sha256": "output_schema",
    "annotations_sha256": "annotations",
    "execution_sha256": "execution",
    "metadata_sha256": "other_metadata",
}

RenameSignature = tuple[str, str, str | None, str, str, str]


def _rename_signature(value: Fingerprints) -> RenameSignature:
    return (
        value.description_sha256,
        value.input_schema_sha256,
        value.output_schema_sha256,
        value.annotations_sha256,
        value.execution_sha256,
        value.metadata_sha256,
    )


def _changed(old: Fingerprints, new: Fingerprints) -> list[str]:
    return [label for attr, label in HASH_FIELDS.items() if getattr(old, attr) != getattr(new, attr)]


def _detail(old: BaselineTool, tool: ToolDefinition, fields: list[str], verbose: bool) -> dict[str, object]:
    current = _summary(tool)
    details: dict[str, object] = {"changed_fields": fields}
    if verbose:
        details["baseline_summary"] = old.summary
        details["current_summary"] = current
    else:
        for key in (
            "input_properties",
            "output_properties",
            "annotation_keys",
            "execution_keys",
            "metadata_keys",
            "unknown_keys",
        ):
            old_value = old.summary.get(key, [])
            new_value = current.get(key, [])
            before = set(old_value if isinstance(old_value, list) else [])
            after = set(new_value if isinstance(new_value, list) else [])
            if before != after:
                details[key] = {"added": sorted(after - before), "removed": sorted(before - after)}
    return details


def compare_baseline(tools: list[ToolDefinition], baseline: BaselineFile, verbose: bool = False) -> list[Drift]:
    current = {tool.name: tool for tool in tools}
    previous = {tool.name: tool for tool in baseline.tools}
    current_fingerprints = {name: fingerprint_tool(tool) for name, tool in current.items()}
    drifts: list[Drift] = []
    removed = set(previous) - set(current)
    added = set(current) - set(previous)

    # Conservative rename inference: each component signature must identify exactly one old and one new tool.
    removed_by_signature: dict[RenameSignature, list[str]] = defaultdict(list)
    added_by_signature: dict[RenameSignature, list[str]] = defaultdict(list)
    for old_name in removed:
        removed_by_signature[_rename_signature(previous[old_name].fingerprints)].append(old_name)
    for new_name in added:
        added_by_signature[_rename_signature(current_fingerprints[new_name])].append(new_name)

    paired_added: set[str] = set()
    paired_removed: set[str] = set()
    for old_name in sorted(removed):
        signature = _rename_signature(previous[old_name].fingerprints)
        old_candidates = removed_by_signature[signature]
        new_candidates = added_by_signature.get(signature, [])
        if len(old_candidates) == 1 and len(new_candidates) == 1:
            new_name = new_candidates[0]
            paired_removed.add(old_name)
            paired_added.add(new_name)
            drifts.append(Drift(kind="tool_renamed", tool_name=new_name, previous_name=old_name, fields=["name"]))

    for name in sorted(removed - paired_removed):
        drifts.append(Drift(kind="tool_removed", tool_name=name))
    for name in sorted(added - paired_added):
        drifts.append(Drift(kind="tool_added", tool_name=name))
    for name in sorted(set(current) & set(previous)):
        new_fp = current_fingerprints[name]
        old = previous[name]
        if old.fingerprints.full_sha256 != new_fp.full_sha256:
            fields = _changed(old.fingerprints, new_fp)
            drifts.append(
                Drift(
                    kind="tool_changed",
                    tool_name=name,
                    fields=fields,
                    differences=_detail(old, current[name], fields, verbose),
                )
            )
    return drifts
