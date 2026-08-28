# Day 3D Thesis Table Pack

All percentages are calculated from preserved artifacts. “pp” means percentage points. Expected-category and field-family groups are descriptive; multi-label samples can appear in more than one category.

## Table 1 — Holdout composition

| Property | Value |
|---|---|
| Corpus | `mcpsec-independent-holdout-metadata` |
| Version / split | `1.0.1` / `holdout` |
| Review status | `independently_reviewed` |
| Total | 48 |
| Frozen benign / suspicious | 24 / 24 |
| Reviewer benign / suspicious | 25 / 23 |
| Binary agreements / disagreements / abstentions | 47 / 1 / 0 |
| Raw binary agreement | 97.9167% |
| Cohen's kappa | approximately 0.9583 |
| Corpus SHA-256 | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |

*Suggested caption: Composition and independent-review status of the frozen 48-sample synthetic/derived holdout.*

## Table 2 — Primary confusion matrix

| Actual / ground truth | Predicted suspicious | Predicted benign | Total |
|---|---:|---:|---:|
| Suspicious | 5 TP | 19 FN | 24 |
| Benign | 6 FP | 18 TN | 24 |
| Total | 11 | 37 | 48 |

*Suggested caption: Confusion matrix for the preregistered full detector at the MEDIUM threshold on the independent holdout.*

## Table 3 — Primary effectiveness metrics

| Metric | Value | Numerator / denominator | Neutral interpretation |
|---|---:|---:|---|
| Accuracy | 47.92% | 23 / 48 | Correct classifications among all samples. |
| Precision | 45.45% | 5 / 11 | Suspicious samples among flagged samples. |
| Recall | 20.83% | 5 / 24 | Detected suspicious samples. |
| F1 | 28.57% | — | Harmonic mean of precision and recall. |
| False-positive rate | 25.00% | 6 / 24 | Flagged benign samples. |

*Suggested caption: Primary effectiveness metrics from authoritative experiment H0.*

## Table 4 — Wilson 95% intervals

| Measure | Estimate | Numerator | Denominator | Lower | Upper |
|---|---:|---:|---:|---:|---:|
| Accuracy | 47.92% | 23 | 48 | 34.47% | 61.67% |
| Recall | 20.83% | 5 | 24 | 9.24% | 40.47% |
| False-positive rate | 25.00% | 6 | 24 | 12.00% | 44.90% |

*Suggested caption: Preregistered Wilson score 95% intervals for the principal holdout proportions.*

## Table 5 — Runtime performance

| Measure | Analysis-core H0 | Static-end-to-end H1 |
|---|---:|---:|
| Warm-ups / measured repetitions | 3 / 10 | 1 / 5 |
| Observations | 480 | 240 |
| Mean per tool | 1.7159 ms | 4.3020 ms |
| Median | 1.5354 ms | 4.0732 ms |
| p95 | 3.2229 ms | 6.3104 ms |
| Minimum / maximum | 0.9188 / 5.8537 ms | 3.0328 / 7.5676 ms |
| Population standard deviation | 0.7357 ms | 0.9483 ms |
| Mean corpus pass | 82.3637 ms | 206.4941 ms |

*Suggested caption: Runtime summaries at the preregistered analysis-core and static-end-to-end timing boundaries.*

## Table 6 — Development versus holdout

| Metric | Development | Holdout H0 | Holdout − development |
|---|---:|---:|---:|
| Accuracy | 91.25% | 47.92% | -43.33 pp |
| Precision | 90.24% | 45.45% | -44.79 pp |
| Recall | 92.50% | 20.83% | -71.67 pp |
| F1 | 91.36% | 28.57% | -62.79 pp |
| False-positive rate | 10.00% | 25.00% | +15.00 pp |

*Suggested caption: Descriptive metric comparison between the frozen development corpus and independently reviewed holdout.*

## Table 7 — Category performance

| Expected category | n | Detected | Missed | Binary detection proportion | Warning |
|---|---:|---:|---:|---:|---|
| Instruction override | 3 | 0 | 3 | 0.00% | n < 10 |
| Concealment | 4 | 0 | 4 | 0.00% | n < 10 |
| Sensitive data | 4 | 2 | 2 | 50.00% | n < 10 |
| Schema | 4 | 3 | 1 | 75.00% | n < 10 |
| Mismatch | 4 | 1 | 3 | 25.00% | n < 10 |
| Obfuscation | 4 | 0 | 4 | 0.00% | n < 10 |
| Capability | 6 | 0 | 6 | 0.00% | n < 10 |

*Suggested caption: Overall binary detection by expected suspicious category; multi-label samples contribute to each applicable category.*

## Table 8 — Field-location performance

| Expected field family | n | Detected | Missed | Detection proportion | Warning |
|---|---:|---:|---:|---:|---|
| Description | 4 | 0 | 4 | 0.00% | n < 10 |
| Input schema | 5 | 3 | 2 | 60.00% | n < 10 |
| Output schema | 3 | 1 | 2 | 33.33% | n < 10 |
| Annotations | 3 | 0 | 3 | 0.00% | n < 10 |
| `_meta` | 4 | 1 | 3 | 25.00% | n < 10 |
| Execution | 3 | 0 | 3 | 0.00% | n < 10 |
| Vendor / unknown | 2 | 0 | 2 | 0.00% | n < 10 |

*Suggested caption: Binary detection by aggregated expected metadata field family.*

## Table 9 — Difficulty performance

| Author difficulty | TP | TN | FP | FN | Suspicious recall | n |
|---|---:|---:|---:|---:|---:|---:|
| Obvious | 2 | 6 | 2 | 6 | 25.00% | 16 |
| Moderate | 2 | 6 | 2 | 6 | 25.00% | 16 |
| Subtle | 1 | 6 | 2 | 7 | 12.50% | 16 |

*Suggested caption: Descriptive performance by frozen author difficulty; independent exact difficulty agreement was 16/48.*

## Table 10 — False-negative summary

| ID | Tool | Category | Field | Difficulty | Finding / risk | Primary mechanism |
|---|---|---|---|---|---|---|
| s001 | `priority_route_selector` | instruction override | description | obvious | none / 0 | semantic paraphrase |
| s002 | `agenda_context_merger` | instruction override | input schema | moderate | none / 0 | semantic paraphrase |
| s003 | `reference_card_picker` | instruction override | annotations | subtle | none / 0 | semantic paraphrase |
| s004 | `private_audit_receipt` | concealment | description | obvious | none / 0 | contextual concealment |
| s005 | `auxiliary_summary_builder` | concealment | output schema | moderate | none / 0 | contextual concealment |
| s006 | `background_note_compactor` | concealment | `_meta` | subtle | none / 0 | contextual concealment |
| s009 | `account_recovery_card` | sensitive data | output schema | subtle | none / 0 | vocabulary |
| s010 | `schema_migration_preview` | schema | input schema | obvious | none / 0 | vocabulary |
| s012 | `document_outline` | capability | execution | subtle | none / 0 | capability reasoning |
| s015 | `unit_ratio_display` | mismatch | annotations | moderate | none / 0 | cross-field reasoning |
| s016 | `translation_preview` | capability, mismatch | execution | subtle | none / 0 | cross-field reasoning |
| s017 | `numeric_note_decoder` | obfuscation | description | obvious | none / 0 | obfuscation decoding |
| s018 | `compact_operator_badge` | concealment, obfuscation | annotations | moderate | none / 0 | obfuscation decoding |
| s019 | `entity_encoded_policy` | obfuscation | `_meta` | subtle | none / 0 | obfuscation decoding |
| s020 | `vendor_memo_formatter` | obfuscation | vendor | subtle | none / 0 | obfuscation decoding |
| s021 | `workspace_maintenance_agent` | capability | description | obvious | none / 0 | capability reasoning |
| s022 | `plain_text_preview` | capability, mismatch | `_meta` | obvious | none / 0 | capability reasoning |
| s023 | `meeting_title_case` | capability, sensitive data | execution | moderate | `CAP-001` info / 2 | threshold |
| s024 | `offline_chart_legend` | capability | vendor | moderate | `CAP-001` info / 2 | threshold |

*Suggested caption: Compact inventory of all 19 H0 false negatives, separating 17 no-finding cases from two below-threshold informational cases.*

## Table 11 — False-positive summary

| ID | Tool | Rule | Field | Evidence | Risk | Benign rationale |
|---|---|---|---|---|---:|---|
| b007 | `token_shape_validator` | `SCH-002` | input schema | `token` | 11 | Synthetic/redacted local shape validation. |
| b008 | `password_policy_linter` | `SEC-001` | title | `Password` | 10 | Policy prose; no values. |
| b012 | `service_key_name_inventory` | `SEC-001` | description | `secrets` | 10 | Alias names only; no credentials. |
| b015 | `release_command_explainer` | `SCH-002` | input schema | `executable` | 11 | Documentation lookup; process launch denied. |
| b020 | `credential_rotation_notice` | `SEC-001` | title | `Credential` | 10 | Reminder prose; no values. |
| b023 | `secret_scanner_documentation` | `SEC-001` | title | `Secret` | 10 | Educational text and placeholders. |

*Suggested caption: All six H0 false positives and the lexical evidence recorded by the authoritative artifact.*

## Table 12 — Detector-family ablation

| Configuration | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Full | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without injection | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without concealment | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without sensitive data | 5 | 22 | 2 | 19 | 56.25% | 71.43% | 20.83% | 32.26% | 8.33% |
| Without schema | 3 | 20 | 4 | 21 | 47.92% | 42.86% | 12.50% | 19.35% | 16.67% |
| Without mismatch | 4 | 18 | 6 | 20 | 45.83% | 40.00% | 16.67% | 23.53% | 25.00% |
| Without obfuscation | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Without capability | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |

*Suggested caption: Preregistered family-removal ablations on the frozen holdout; results are corpus-specific.*

## Table 13 — Ablation deltas

| Removed family | ΔTP | ΔTN | ΔFP | ΔFN | Δaccuracy | Δprecision | Δrecall | ΔF1 | ΔFPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Injection | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |
| Concealment | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |
| Sensitive data | 0 | +4 | -4 | 0 | +8.33 pp | +25.97 pp | 0.00 pp | +3.69 pp | -16.67 pp |
| Schema | -2 | +2 | -2 | +2 | 0.00 pp | -2.60 pp | -8.33 pp | -9.22 pp | -8.33 pp |
| Mismatch | -1 | 0 | 0 | +1 | -2.08 pp | -5.45 pp | -4.17 pp | -5.04 pp | 0.00 pp |
| Obfuscation | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |
| Capability | 0 | 0 | 0 | 0 | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |

*Suggested caption: Change in holdout counts and metrics after removing each detector family, relative to full H0.*

## Table 14 — Failure taxonomy

### False-negative primary mechanisms

| Primary mechanism | Count | Share of 19 FNs |
|---|---:|---:|
| Semantic paraphrase | 3 | 15.79% |
| Contextual concealment | 3 | 15.79% |
| Vocabulary | 2 | 10.53% |
| Capability reasoning | 3 | 15.79% |
| Cross-field reasoning | 2 | 10.53% |
| Obfuscation decoding | 4 | 21.05% |
| Threshold | 2 | 10.53% |
| **Total** | **19** | **100.00%** |

### False-positive primary mechanisms

| Primary mechanism | Samples | Count |
|---|---|---:|
| Benign schema vocabulary | b007, b015 | 2 |
| Title-only trigger | b008, b020 | 2 |
| Negation/disclaimer failure | b012 | 1 |
| Educational/documentation context | b023 | 1 |
| **Total** |  | **6** |

*Suggested caption: Post-unblinding descriptive primary failure taxonomy; overlapping contributing tags are reported separately in the discussion evidence.*
