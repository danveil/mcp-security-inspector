from __future__ import annotations

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
    drifts: list[Drift] = []
    removed = set(previous) - set(current)
    added = set(current) - set(previous)

    # Conservative rename inference: exactly one removed/new pair with identical components except full hash/name.
    paired_added: set[str] = set()
    paired_removed: set[str] = set()
    for old_name in sorted(removed):
        old_fp = previous[old_name].fingerprints
        candidates = []
        for new_name in sorted(added):
            new_fp = fingerprint_tool(current[new_name])
            if all(getattr(old_fp, attr) == getattr(new_fp, attr) for attr in HASH_FIELDS):
                candidates.append(new_name)
        if len(candidates) == 1:
            new_name = candidates[0]
            paired_removed.add(old_name)
            paired_added.add(new_name)
            drifts.append(Drift(kind="tool_renamed", tool_name=new_name, previous_name=old_name, fields=["name"]))

    for name in sorted(removed - paired_removed):
        drifts.append(Drift(kind="tool_removed", tool_name=name))
    for name in sorted(added - paired_added):
        drifts.append(Drift(kind="tool_added", tool_name=name))
    for name in sorted(set(current) & set(previous)):
        new_fp = fingerprint_tool(current[name])
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
