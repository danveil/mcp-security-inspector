# Day 3D Results Evidence

Scientific status: **PREREGISTERED / CONFIRMATORY** for H0 effectiveness and the planned timing/ablation experiments; **DESCRIPTIVE** for the tabulations derived from those frozen outputs.

This document records what happened. Interpretive explanations are reserved for `discussion-evidence.md`.

## 1. Evaluation setup

| Item | Frozen value |
|---|---|
| Repository commit | `a4abee4661522ac13edb37e1b075186a2ccd7a03` |
| H0 experiment | `exp-20260827T060056391880Z-c514ba03-a660fd6d` |
| H0 artifact SHA-256 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` |
| Detector-source bundle SHA-256 | `197f13414a348ff527c27061aee481c2e3d11ca32198441dcfdb77b6ff8bd227` |
| Corpus | `mcpsec-independent-holdout-metadata` version `1.0.1` |
| Corpus SHA-256 | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| Configuration SHA-256 | `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1` |
| Samples | 48: 24 benign and 24 suspicious |
| Threshold | `MEDIUM` |
| Detector configuration | Full built-in set; no custom rules; no suppressions |
| Review status | Independently reviewed by one reviewer before unblinding |

The effectiveness values below come from the preserved H0 JSON. Percentages were also independently recalculated from the raw confusion counts and matched the artifact values.

## 2. Primary confusion matrix

| Actual / ground truth | Predicted suspicious | Predicted benign | Row total |
|---|---:|---:|---:|
| Suspicious | 5 (TP) | 19 (FN) | 24 |
| Benign | 6 (FP) | 18 (TN) | 24 |
| Column total | 11 | 37 | 48 |

- 5 suspicious samples were correctly detected.
- 19 suspicious samples were missed.
- 18 benign samples were correctly rejected.
- 6 benign samples were falsely flagged.

## 3. Overall effectiveness

| Metric | Artifact value | Independently calculated | Numerator / denominator | Neutral reading |
|---|---:|---:|---:|---|
| Accuracy | 47.92% | 47.92% | 23 / 48 | Correct binary classifications. |
| Precision | 45.45% | 45.45% | 5 / 11 | Flagged samples that were suspicious. |
| Recall | 20.83% | 20.83% | 5 / 24 | Suspicious samples detected. |
| F1 | 28.57% | 28.57% | Harmonic mean | Combined precision/recall summary. |
| False-positive rate | 25.00% | 25.00% | 6 / 24 | Benign samples flagged. |

No discrepancy was found between the independently calculated metrics and the authoritative artifact.

## 4. Statistical uncertainty

| Measure | Point estimate | Numerator | Denominator | Wilson 95% lower | Wilson 95% upper |
|---|---:|---:|---:|---:|---:|
| Accuracy | 47.92% | 23 | 48 | 34.47% | 61.67% |
| Recall | 20.83% | 5 | 24 | 9.24% | 40.47% |
| False-positive rate | 25.00% | 6 | 24 | 12.00% | 44.90% |

These are the preregistered Wilson score intervals stored in H0. With only 48 samples, the interval widths represent substantial uncertainty. Every expected-category and field-location stratum below contains fewer than 10 samples, is especially unstable, and carries the artifact's low-evidence warning.

## 5. Runtime efficiency

The two timing boundaries are reported separately and are not interchangeable.

| Measure | H0 analysis-core | H1 static-end-to-end |
|---|---:|---:|
| Warm-up repetitions | 3 | 1 |
| Measured repetitions | 10 | 5 |
| Samples per repetition | 48 | 48 |
| Timing observations | 480 | 240 |
| Mean per tool | 1.7159 ms | 4.3020 ms |
| Median | 1.5354 ms | 4.0732 ms |
| p95 | 3.2229 ms | 6.3104 ms |
| Minimum | 0.9188 ms | 3.0328 ms |
| Maximum | 5.8537 ms | 7.5676 ms |
| Population standard deviation | 0.7357 ms | 0.9483 ms |
| Mean corpus pass | 82.3637 ms | 206.4941 ms |
| Total measured time | 823.6370 ms | 1032.4706 ms |

H0 measures per-tool analysis after loading and normalization. H1 measures the preserved static end-to-end boundary. H0 and H1 produced equivalent predictions for all 48 samples.

## 6. Development versus holdout

| Metric | Development | Independent holdout | Holdout minus development |
|---|---:|---:|---:|
| Accuracy | 91.25% | 47.92% | -43.33 pp |
| Precision | 90.24% | 45.45% | -44.79 pp |
| Recall | 92.50% | 20.83% | -71.67 pp |
| F1 | 91.36% | 28.57% | -62.79 pp |
| False-positive rate | 10.00% | 25.00% | +15.00 pp |

Development counts were TP 37, TN 36, FP 4, and FN 3. Holdout counts were TP 5, TN 18, FP 6, and FN 19. Recall decreased by 71.67 percentage points and F1 decreased by 62.79 percentage points.

## 7. Category performance

This table groups suspicious samples by expected category and reports their overall binary H0 classification at the `MEDIUM` threshold. Multi-label samples appear in every applicable expected category. This is distinct from the artifact's predicted-family `category_metrics` table.

| Expected category | Samples | Detected | Missed | Detection proportion | Evidence warning |
|---|---:|---:|---:|---:|---|
| Instruction override | 3 | 0 | 3 | 0.00% | Low evidence: n < 10 |
| Concealment | 4 | 0 | 4 | 0.00% | Low evidence: n < 10 |
| Sensitive data | 4 | 2 | 2 | 50.00% | Low evidence: n < 10 |
| Schema | 4 | 3 | 1 | 75.00% | Low evidence: n < 10 |
| Mismatch | 4 | 1 | 3 | 25.00% | Low evidence: n < 10 |
| Obfuscation | 4 | 0 | 4 | 0.00% | Low evidence: n < 10 |
| Capability | 6 | 0 | 6 | 0.00% | Low evidence: n < 10 |

The predicted-family schema metric in H0 records 2/4 schema-family detections; the expected-category binary table records 3/4 samples classified suspicious through any enabled family.

## 8. Field-location performance

| Expected field family | Samples | Detected | Missed | Detection proportion | Evidence warning |
|---|---:|---:|---:|---:|---|
| Description | 4 | 0 | 4 | 0.00% | Low evidence: n < 10 |
| Input schema | 5 | 3 | 2 | 60.00% | Low evidence: n < 10 |
| Output schema | 3 | 1 | 2 | 33.33% | Low evidence: n < 10 |
| Annotations | 3 | 0 | 3 | 0.00% | Low evidence: n < 10 |
| `_meta` | 4 | 1 | 3 | 25.00% | Low evidence: n < 10 |
| Execution | 3 | 0 | 3 | 0.00% | Low evidence: n < 10 |
| Vendor / unknown | 2 | 0 | 2 | 0.00% | Low evidence: n < 10 |

## 9. Difficulty performance

| Frozen author difficulty | TP | TN | FP | FN | Suspicious recall | Total n |
|---|---:|---:|---:|---:|---:|---:|
| Obvious | 2 | 6 | 2 | 6 | 25.00% | 16 |
| Moderate | 2 | 6 | 2 | 6 | 25.00% | 16 |
| Subtle | 1 | 6 | 2 | 7 | 12.50% | 16 |

Independent reviewer exact difficulty agreement was 16/48. Difficulty is therefore retained as a descriptive, subjective annotation and not treated as a stable objective scale.

## 10. False negatives

H0 contains 19 false negatives: 17 had no finding and risk 0; 2 had an informational `CAP-001` finding and risk 2 but remained below the `MEDIUM` classification threshold.

| Sample / tool | Expected category | Expected field | Difficulty | Finding status | Risk | Mechanical classification |
|---|---|---|---|---|---:|---|
| `holdout_s001` / `priority_route_selector` | instruction override | `description` | obvious | none | 0 | semantic paraphrase gap |
| `holdout_s002` / `agenda_context_merger` | instruction override | `inputSchema.properties.planning_context.description` | moderate | none | 0 | semantic paraphrase gap |
| `holdout_s003` / `reference_card_picker` | instruction override | `annotations.routingHint` | subtle | none | 0 | semantic paraphrase gap |
| `holdout_s004` / `private_audit_receipt` | concealment | `description` | obvious | none | 0 | contextual concealment gap |
| `holdout_s005` / `auxiliary_summary_builder` | concealment | `outputSchema.description` | moderate | none | 0 | contextual concealment gap |
| `holdout_s006` / `background_note_compactor` | concealment | `_meta.operatorNarrative` | subtle | none | 0 | contextual concealment gap |
| `holdout_s009` / `account_recovery_card` | sensitive data | `outputSchema.properties.recoveryPhraseEcho.description` | subtle | none | 0 | vocabulary gap |
| `holdout_s010` / `schema_migration_preview` | schema | `inputSchema.properties.processTemplate.description` | obvious | none | 0 | vocabulary gap |
| `holdout_s012` / `document_outline` | capability | `execution.agentCapabilities[0]` | subtle | none | 0 | capability-reasoning gap |
| `holdout_s015` / `unit_ratio_display` | mismatch | `annotations.capabilitySummary` | moderate | none | 0 | cross-field reasoning gap |
| `holdout_s016` / `translation_preview` | capability, mismatch | `execution.operations[1]` | subtle | none | 0 | cross-field reasoning gap |
| `holdout_s017` / `numeric_note_decoder` | obfuscation | `description` | obvious | none | 0 | obfuscation-decoding gap |
| `holdout_s018` / `compact_operator_badge` | concealment, obfuscation | `annotations.operatorLabel` | moderate | none | 0 | obfuscation-decoding gap |
| `holdout_s019` / `entity_encoded_policy` | obfuscation | `_meta.displayDirective` | subtle | none | 0 | obfuscation-decoding gap |
| `holdout_s020` / `vendor_memo_formatter` | obfuscation | `vendorEnvelope.agentMemo` | subtle | none | 0 | obfuscation-decoding gap |
| `holdout_s021` / `workspace_maintenance_agent` | capability | `description` | obvious | none | 0 | capability-reasoning gap |
| `holdout_s022` / `plain_text_preview` | capability, mismatch | `_meta.permissions[0]` | obvious | none | 0 | capability-reasoning gap |
| `holdout_s023` / `meeting_title_case` | capability, sensitive data | `execution.credentialAccess` | moderate | `CAP-001`, informational | 2 | threshold gap |
| `holdout_s024` / `offline_chart_legend` | capability | `vendorExtension.agentPrivileges[0]` | moderate | `CAP-001`, informational | 2 | threshold gap |

## 11. False positives

| Sample / tool | Rule | Triggered field | Short evidence | Risk | Ground-truth rationale summary |
|---|---|---|---|---:|---|
| `holdout_b007` / `token_shape_validator` | `SCH-002` | `input_schema.properties.candidate_token.description` | `token` | 11 | Synthetic/redacted token used for local shape validation; no storage or transmission. |
| `holdout_b008` / `password_policy_linter` | `SEC-001` | `title` | `Password` | 10 | Policy prose excludes real password values. |
| `holdout_b012` / `service_key_name_inventory` | `SEC-001` | `description` | `secrets` | 10 | Identifier aliases only; credentials are neither requested nor returned. |
| `holdout_b015` / `release_command_explainer` | `SCH-002` | `input_schema.properties.command_name.description` | `executable` | 11 | Documentation lookup only; execution metadata denies process launch. |
| `holdout_b020` / `credential_rotation_notice` | `SEC-001` | `title` | `Credential` | 10 | Reminder prose excludes credential values. |
| `holdout_b023` / `secret_scanner_documentation` | `SEC-001` | `title` | `Secret` | 10 | Educational documentation uses placeholders and warns against real secrets. |

`SEC-001` produced 4 of the 6 binary false positives. `SCH-002` produced the other 2.

## 12. Ablation experiment

### Master table

| Configuration | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Full H0 | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without injection | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without concealment | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without sensitive data | 5 | 22 | 2 | 19 | 56.25% | 71.43% | 20.83% | 32.26% | 8.33% |
| Without schema | 3 | 20 | 4 | 21 | 47.92% | 42.86% | 12.50% | 19.35% | 16.67% |
| Without mismatch | 4 | 18 | 6 | 20 | 45.83% | 40.00% | 16.67% | 23.53% | 25.00% |
| Without obfuscation | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without capability | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |

### Deltas from full H0

Metric deltas are ablation minus H0.

| Removed family | ΔTP | ΔTN | ΔFP | ΔFN | Δaccuracy | Δprecision | Δrecall | ΔF1 | ΔFPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Injection | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |
| Concealment | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |
| Sensitive data | 0 | +4 | -4 | 0 | +8.33 pp | +25.97 pp | 0.00 pp | +3.69 pp | -16.67 pp |
| Schema | -2 | +2 | -2 | +2 | 0.00 pp | -2.60 pp | -8.33 pp | -9.22 pp | -8.33 pp |
| Mismatch | -1 | 0 | 0 | +1 | -2.08 pp | -5.45 pp | -4.17 pp | -5.04 pp | 0.00 pp |
| Obfuscation | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |
| Capability | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |

## 13. Reviewer-sensitive observations

- All 48 samples received independent binary review before unblinding: 47 agreements, 1 disagreement, and 0 abstentions.
- Reviewer binary totals were 25 benign and 23 suspicious; frozen ground truth remained 24 benign and 24 suspicious.
- The sole disagreement, R08 / `bounded_result_sampler` (`holdout_s011`), was preserved and adjudicated as suspicious under the frozen schema-security-review construct.
- R08 was a true positive in H0 and contributes to the small schema result.
- Original author difficulty labels were not overwritten. Exact independent difficulty agreement was 16/48.
- Only one independent reviewer was used.

## 14. Results summary

Under the frozen full built-in configuration at `MEDIUM`, H0 classified 23/48 samples correctly. It detected 5/24 suspicious samples and flagged 6/24 benign samples. Analysis-core mean latency was 1.7159 ms per tool; static-end-to-end mean latency was 4.3020 ms per tool. The largest development-to-holdout metric change was recall at -71.67 percentage points. Seventeen of nineteen false negatives contained no finding; two contained informational findings below threshold. In the preregistered ablations, schema removal lost two true positives, mismatch removal lost one true positive, and sensitive-data removal removed four false positives without changing true positives on this corpus.
