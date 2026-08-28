# Frozen v0.2 H0 versus v0.3 Exploratory Comparison

This comparison pairs two immutable artifacts for the same exposed 48-sample corpus. The built-in comparison CLI rejected the old artifact because its pre-v0.3 enabled-rule registry is not internally complete under the current registry (`Experiment artifact ablation sets are internally inconsistent`). Therefore, the paired comparison below was calculated directly by exact sample ID from the two preserved artifacts; neither corpus was rescanned for this calculation.

## Aggregate change

| Metric | v0.2 H0 | v0.3 exploratory | Delta |
|---|---:|---:|---:|
| TP | 5 | 11 | +6 |
| TN | 18 | 18 | 0 |
| FP | 6 | 6 | 0 |
| FN | 19 | 13 | -6 |
| Accuracy | 47.92% | 60.42% | +12.50 pp |
| Precision | 45.45% | 64.71% | +19.25 pp |
| Recall | 20.83% | 45.83% | +25.00 pp |
| F1 | 28.57% | 53.66% | +25.09 pp |
| FPR | 25.00% | 25.00% | 0.00 pp |

Prediction changes are only `s003`, `s004`, `s015`, `s022`, `s023`, and `s024`, all FN to TP. Original FPs resolved: none. New FPs introduced: none. Previously correct samples broken: none.

## Category comparison

“Binary” counts any MEDIUM-or-higher finding on a sample carrying the expected category. “Same-category” requires the expected detector category itself. Every stratum has fewer than ten samples and is low evidence.

| Expected category | Total | v0.2 binary | v0.3 binary | Binary delta | v0.2 same-category | v0.3 same-category |
|---|---:|---:|---:|---:|---:|---:|
| Instruction override | 3 | 0 | 1 | +1 | 0 | 1 |
| Concealment | 4 | 0 | 1 | +1 | 0 | 1 |
| Sensitive data | 4 | 2 | 3 | +1 | 2 | 2 |
| Schema | 4 | 3 | 3 | 0 | 2 | 2 |
| Mismatch | 4 | 1 | 3 | +2 | 1 | 3 |
| Obfuscation | 4 | 0 | 0 | 0 | 0 | 0 |
| Capability | 6 | 0 | 3 | +3 | 2 | 2 |

The sensitive-data and capability binary gains come from `MIS-002` on multi-category samples, not from better same-family coverage. Obfuscation remains 0/4 on the exposed set.

## Field-location comparison

| Expected field family | Total suspicious | v0.2 detected | v0.3 detected | Delta |
|---|---:|---:|---:|---:|
| Description | 4 | 0 | 1 | +1 |
| inputSchema | 5 | 3 | 3 | 0 |
| outputSchema | 3 | 1 | 1 | 0 |
| Annotations | 3 | 0 | 2 | +2 |
| `_meta` / metadata | 4 | 1 | 2 | +1 |
| Execution | 3 | 0 | 1 | +1 |
| Vendor/unknown | 2 | 0 | 1 | +1 |

The result is consistent with useful detection broadening beyond input-schema-heavy v0.2 behavior, especially through PI-002/MIS-002 path preservation. It does not establish population-level robustness for any field family.

## Difficulty comparison

| Difficulty | v0.2 TP/FN | v0.2 recall | v0.3 TP/FN | v0.3 recall | FPR old/new |
|---|---:|---:|---:|---:|---:|
| Obvious | 2/6 | 25.00% | 4/4 | 50.00% | 25.00% / 25.00% |
| Moderate | 2/6 | 25.00% | 5/3 | 62.50% | 25.00% / 25.00% |
| Subtle | 1/7 | 12.50% | 2/6 | 25.00% | 25.00% / 25.00% |

Difficulty is descriptive and subjective: the independent reviewer agreed with the original difficulty on only 16/48 samples.

## Regression inventory

- Original TP to new FN: none.
- Original TN to new FP: none.
- Original correct sample receiving a new P0 finding: none.
- Benign risk amplification: `b012` and `b020`, each `10 -> 23` from new `SEC-002` findings while remaining false positives.
- All 13 remaining FNs have no finding and risk 0; none is below threshold.
