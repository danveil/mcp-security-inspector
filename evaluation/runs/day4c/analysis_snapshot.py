from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent
NEW_RULES = ("PI-002", "HID-002", "SEC-002", "OBF-005", "MIS-002")
H0_PATH = ROOT.parent / "exp-20260827T060056391880Z-c514ba03-a660fd6d.json"


def load(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def indexed(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {sample["sample_id"]: sample for sample in report["samples"]}


FULL_FILES = {
    "development": "development-full.json",
    "exploratory_fixtures": "exploratory-fixtures-full.json",
    "exposed_holdout": "post-unblinding-exploratory-holdout-full-analysis-core.json",
}
ABLATION_PREFIXES = {
    "development": "development",
    "exploratory_fixtures": "exploratory-fixtures",
    "exposed_holdout": "post-unblinding-exploratory-holdout",
}


def contribution(dataset: str) -> dict[str, Any]:
    full = load(FULL_FILES[dataset])
    full_samples = indexed(full)
    result: dict[str, Any] = {}
    for rule in NEW_RULES:
        affected = [
            sample for sample in full["samples"] if any(item["rule_id"] == rule for item in sample["findings"])
        ]
        ablated = indexed(load(f"{ABLATION_PREFIXES[dataset]}-without-{rule.casefold()}.json"))
        binary_changes = sorted(
            sample["sample_id"]
            for sample in affected
            if sample["predicted"] != ablated[sample["sample_id"]]["predicted"]
        )
        evidence_only = sorted(sample["sample_id"] for sample in affected if sample["sample_id"] not in binary_changes)
        overlaps_existing = sorted(
            sample["sample_id"]
            for sample in affected
            if any(item not in NEW_RULES for item in sample["triggered_rule_ids"])
        )
        overlaps_new = sorted(
            sample["sample_id"]
            for sample in affected
            if len(set(sample["triggered_rule_ids"]) & set(NEW_RULES)) > 1
        )
        result[rule] = {
            "finding_count": sum(
                1 for sample in affected for item in sample["findings"] if item["rule_id"] == rule
            ),
            "unique_samples": len(affected),
            "sample_ids": sorted(sample["sample_id"] for sample in affected),
            "suspicious_samples": sorted(
                sample["sample_id"] for sample in affected if sample["expected"] == "suspicious"
            ),
            "benign_samples": sorted(sample["sample_id"] for sample in affected if sample["expected"] == "benign"),
            "overlap_existing": overlaps_existing,
            "overlap_other_new": overlaps_new,
            "binary_changes": binary_changes,
            "evidence_only": evidence_only,
            "ablation_matrix": load(f"{ABLATION_PREFIXES[dataset]}-without-{rule.casefold()}.json")[
                "confusion_matrix"
            ],
            "full_matrix": full["confusion_matrix"],
        }
    assert set(full_samples) == set(indexed(full))
    return result


def expected_category_counts(report: dict[str, Any]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for category in (
        "instruction_override",
        "concealment",
        "sensitive_data",
        "schema",
        "mismatch",
        "obfuscation",
        "capability",
    ):
        samples = [sample for sample in report["samples"] if category in sample["expected_categories"]]
        result[category] = {
            "detected_binary": sum(sample["predicted"] == "suspicious" for sample in samples),
            "detected_category": sum(category in sample["predicted_categories"] for sample in samples),
            "total": len(samples),
        }
    return result


def field_family(path: str) -> str:
    if path.startswith("description"):
        return "description"
    if path.startswith(("inputSchema", "input_schema")):
        return "inputSchema"
    if path.startswith(("outputSchema", "output_schema")):
        return "outputSchema"
    if path.startswith("annotations"):
        return "annotations"
    if path.startswith(("_meta", "metadata")):
        return "_meta"
    if path.startswith("execution"):
        return "execution"
    return "vendor/unknown"


def field_counts(report: dict[str, Any]) -> dict[str, dict[str, int]]:
    result = {
        name: {"detected": 0, "total": 0}
        for name in ("description", "inputSchema", "outputSchema", "annotations", "_meta", "execution", "vendor/unknown")
    }
    for sample in report["samples"]:
        if sample["expected"] != "suspicious":
            continue
        families = {field_family(path) for path in sample["expected_field_locations"]}
        for family in families:
            result[family]["total"] += 1
            result[family]["detected"] += sample["predicted"] == "suspicious"
    return result


def difficulty_counts(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for difficulty in ("obvious", "moderate", "subtle"):
        samples = [sample for sample in report["samples"] if sample["difficulty"] == difficulty]
        suspicious = [sample for sample in samples if sample["expected"] == "suspicious"]
        benign = [sample for sample in samples if sample["expected"] == "benign"]
        tp = sum(sample["predicted"] == "suspicious" for sample in suspicious)
        tn = sum(sample["predicted"] == "benign" for sample in benign)
        result[difficulty] = {
            "tp": tp,
            "tn": tn,
            "fp": len(benign) - tn,
            "fn": len(suspicious) - tp,
            "recall": tp / len(suspicious),
            "fpr": (len(benign) - tn) / len(benign),
        }
    return result


h0 = json.loads(H0_PATH.read_text(encoding="utf-8"))
v03 = load(FULL_FILES["exposed_holdout"])
h0_samples = indexed(h0)
v03_samples = indexed(v03)

prediction_changes = [
    {
        "sample_id": sample_id,
        "expected": h0_samples[sample_id]["expected"],
        "old": h0_samples[sample_id]["predicted"],
        "new": v03_samples[sample_id]["predicted"],
        "old_rules": h0_samples[sample_id]["triggered_rule_ids"],
        "new_rules": v03_samples[sample_id]["triggered_rule_ids"],
        "old_risk": h0_samples[sample_id]["risk_score"],
        "new_risk": v03_samples[sample_id]["risk_score"],
    }
    for sample_id in sorted(h0_samples)
    if h0_samples[sample_id]["predicted"] != v03_samples[sample_id]["predicted"]
]

original_fns = [
    {
        "sample_id": sample_id,
        "new_prediction": v03_samples[sample_id]["predicted"],
        "recovered": v03_samples[sample_id]["predicted"] == "suspicious",
        "new_rules": sorted(set(v03_samples[sample_id]["triggered_rule_ids"]) & set(NEW_RULES)),
        "all_rules": v03_samples[sample_id]["triggered_rule_ids"],
        "below_threshold": v03_samples[sample_id]["failure_type"] == "false_negative_below_threshold",
        "risk": v03_samples[sample_id]["risk_score"],
    }
    for sample_id in sorted(h0_samples)
    if h0_samples[sample_id]["expected"] == "suspicious" and h0_samples[sample_id]["predicted"] == "benign"
]

original_fps = [
    {
        "sample_id": sample_id,
        "old_rules": h0_samples[sample_id]["triggered_rule_ids"],
        "new_rules": v03_samples[sample_id]["triggered_rule_ids"],
        "resolved": v03_samples[sample_id]["predicted"] == "benign",
        "old_risk": h0_samples[sample_id]["risk_score"],
        "new_risk": v03_samples[sample_id]["risk_score"],
        "findings": [
            {
                "rule": item["rule_id"],
                "field": item["field"],
                "severity": item["severity"],
                "evidence": item["evidence"],
            }
            for item in v03_samples[sample_id]["findings"]
        ],
    }
    for sample_id in sorted(h0_samples)
    if h0_samples[sample_id]["expected"] == "benign" and h0_samples[sample_id]["predicted"] == "suspicious"
]

benign_risk_increases = [
    {
        "sample_id": sample_id,
        "old": h0_samples[sample_id]["risk_score"],
        "new": v03_samples[sample_id]["risk_score"],
        "delta": v03_samples[sample_id]["risk_score"] - h0_samples[sample_id]["risk_score"],
        "new_rules": sorted(set(v03_samples[sample_id]["triggered_rule_ids"]) - set(h0_samples[sample_id]["triggered_rule_ids"])),
    }
    for sample_id in sorted(h0_samples)
    if h0_samples[sample_id]["expected"] == "benign"
    and v03_samples[sample_id]["risk_score"] > h0_samples[sample_id]["risk_score"]
]

representatives: dict[str, Any] = {}
representative_sources = {
    "PI-002": (v03, "holdout_s003"),
    "HID-002": (v03, "holdout_s004"),
    "SEC-002": (v03, "holdout_b012"),
    "MIS-002": (v03, "holdout_s015"),
    "OBF-005": (load(FULL_FILES["exploratory_fixtures"]), "v03_s_012"),
}
for rule, (report, sample_id) in representative_sources.items():
    sample = indexed(report)[sample_id]
    representatives[rule] = next(item for item in sample["findings"] if item["rule_id"] == rule)

summary = {
    "comparison": {
        "old_matrix": h0["confusion_matrix"],
        "new_matrix": v03["confusion_matrix"],
        "old_metrics": h0["metrics"],
        "new_metrics": v03["metrics"],
        "metric_delta": {
            key: v03["metrics"][key] - h0["metrics"][key]
            for key in ("accuracy", "precision", "recall", "f1", "false_positive_rate")
        },
        "prediction_changes": prediction_changes,
    },
    "contributions": {dataset: contribution(dataset) for dataset in FULL_FILES},
    "original_fns": original_fns,
    "original_fps": original_fps,
    "regressions": {
        "tp_to_fn": [
            item["sample_id"]
            for item in prediction_changes
            if item["expected"] == "suspicious" and item["old"] == "suspicious" and item["new"] == "benign"
        ],
        "tn_to_fp": [
            item["sample_id"]
            for item in prediction_changes
            if item["expected"] == "benign" and item["old"] == "benign" and item["new"] == "suspicious"
        ],
        "benign_risk_increases": benign_risk_increases,
    },
    "category": {"old": expected_category_counts(h0), "new": expected_category_counts(v03)},
    "field": {"old": field_counts(h0), "new": field_counts(v03)},
    "difficulty": {"old": difficulty_counts(h0), "new": difficulty_counts(v03)},
    "representative_findings": representatives,
    "environment": v03["metadata"]["environment"],
    "analysis_timing": v03["timing"],
    "static_timing": load("post-unblinding-exploratory-holdout-full-static-end-to-end.json")["timing"],
}

print(json.dumps(summary, indent=2, ensure_ascii=True))
