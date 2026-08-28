# v0.3 New-Rule Contribution and Ablation

“Suspicious side” and “benign side” count affected ground-truth samples; they are not causal real-world TP/FP estimates. “Binary change” is established by disabling only that rule under the same frozen configuration. No sample contained two new P0 rules simultaneously.

## Contribution by dataset

| Dataset | Rule | Findings / unique samples | Suspicious side | Benign side | Overlap existing rule | Binary changes | Evidence/risk only |
|---|---|---:|---:|---:|---:|---:|---:|
| Development | PI-002 | 0 / 0 | 0 | 0 | 0 | 0 | 0 |
| Development | HID-002 | 1 / 1 | 1 | 0 | 1 | 0 | 1 |
| Development | SEC-002 | 3 / 3 | 3 | 0 | 3 | 0 | 3 |
| Development | OBF-005 | 0 / 0 | 0 | 0 | 0 | 0 | 0 |
| Development | MIS-002 | 1 / 1 | 1 | 0 | 1 | 0 | 1 |
| Exploratory fixtures | PI-002 | 4 / 4 | 4 | 0 | 0 | 4 | 0 |
| Exploratory fixtures | HID-002 | 3 / 3 | 3 | 0 | 0 | 3 | 0 |
| Exploratory fixtures | SEC-002 | 4 / 4 | 4 | 0 | 4 | 0 | 4 |
| Exploratory fixtures | OBF-005 | 4 / 4 | 4 | 0 | 0 | 4 | 0 |
| Exploratory fixtures | MIS-002 | 3 / 3 | 3 | 0 | 2 | 3 | 0 |
| Exposed holdout | PI-002 | 1 / 1 | 1 | 0 | 0 | 1 | 0 |
| Exposed holdout | HID-002 | 1 / 1 | 1 | 0 | 0 | 1 | 0 |
| Exposed holdout | SEC-002 | 2 / 2 | 0 | 2 | 2 | 0 | 2 |
| Exposed holdout | OBF-005 | 0 / 0 | 0 | 0 | 0 | 0 | 0 |
| Exposed holdout | MIS-002 | 4 / 4 | 4 | 0 | 2 | 4 | 0 |

Development affected IDs are `suspicious_015` (HID-002), `suspicious_017`, `suspicious_019`, `suspicious_037` (SEC-002), and `suspicious_013` (MIS-002). All were already binary-positive through existing rules.

Holdout affected IDs are `holdout_s003` (PI-002), `holdout_s004` (HID-002), `holdout_b012`/`holdout_b020` (SEC-002), and `holdout_s015`/`s022`/`s023`/`s024` (MIS-002). OBF-005 produced no holdout finding.

## Individual-rule exploratory ablation

| Disabled rule | Development ΔTP/ΔFP | Fixture ΔTP/ΔFP | Holdout ΔTP/ΔFP | Holdout recall delta | Holdout F1 delta |
|---|---:|---:|---:|---:|---:|
| PI-002 | 0 / 0 | -4 / 0 | -1 / 0 | -4.17 pp | -3.66 pp |
| HID-002 | 0 / 0 | -3 / 0 | -1 / 0 | -4.17 pp | -3.66 pp |
| SEC-002 | 0 / 0 | 0 / 0 | 0 / 0 | 0.00 pp | 0.00 pp |
| OBF-005 | 0 / 0 | -4 / 0 | 0 / 0 | 0.00 pp | 0.00 pp |
| MIS-002 | 0 / 0 | -3 / 0 | -4 / 0 | -16.67 pp | -15.82 pp |

All holdout ablations retain TN 18, FP 6, and FPR 25%. The full matrix is `11/18/6/13`; without PI-002 or HID-002 it is `10/18/6/14`; without MIS-002 it is `7/18/6/17`; without SEC-002 or OBF-005 it is unchanged.

## Explainability audit

| Rule | Representative | Path/evidence quality | Human-review assessment |
|---|---|---|---|
| PI-002 | `holdout_s003` | `annotations.routingHint`; authority excerpt; HIGH; score 23 | Clear rule, category, path, evidence, explanation, recommendation, and contribution. |
| HID-002 | `holdout_s004` | `description`; “keep its existence out of the user-facing”; HIGH; score 22 | Clear concealment relation and observer context. |
| SEC-002 | `holdout_b012` | `description`; coordinated negated phrase; MEDIUM; score 15 | Technically explainable but substantively incorrect: the evidence itself says values are neither requested nor returned. |
| OBF-005 | fixture `v03_s_012` | `metadata.payload`; encoding, original Base64, decoded text, signal; MEDIUM; score 14 | Strongest evidence contract; original and decoded content are both visible and bounded. No holdout example fired. |
| MIS-002 | `holdout_s015` | `description <-> annotations.capabilitySummary`; purpose, capability, corroborator; MEDIUM; score 16 | Clear cross-field reasoning. Very long multi-capability evidence can approach the global evidence cap, but primary paths remain visible. |

All new findings expose stable rule ID/name, category/family, severity, confidence, field path, evidence, explanation, recommendation, and risk contribution. OBF-005 additionally exposes encoding and decoded evidence; MIS-002 exposes both purpose and capability paths. The principal explainability defect is not missing fields but SEC-002 presenting negated benign text as a positive handling action.

## Mechanism-level conclusion

- Credential context: did not reduce any known SEC FP; two were amplified.
- PI-002: recovered one independently authored priority miss; two remain.
- HID-002: recovered one concealment miss; two direct plus one encoded concealment case remain.
- OBF-005: decoding infrastructure worked, but semantic qualification recovered zero exposed cases.
- MIS-002: strongest P0 result, recovering four cross-field/threshold cases without a new binary FP in this exposed set.

These observations are tied to small, exposed, synthetic-heavy samples and do not estimate real-world causal importance.
