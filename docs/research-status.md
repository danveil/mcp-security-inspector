# Public research status

## Chronology

The project followed this sequence:

1. An 80-sample synthetic development corpus informed detector development and regression testing.
2. Detector v0.2 and its MEDIUM-threshold experiment configuration were frozen.
3. A separate 48-sample holdout was independently reviewed while the reviewer was blinded to detector predictions.
4. The first confirmatory holdout experiment, v0.2 H0, was run once and preserved unchanged.
5. Post-unblinding failure analysis identified missed constructs and false positives.
6. Five v0.3 rules were designed and implemented after the holdout was exposed.
7. The v0.3 detector was compared on that same exposed holdout for exploratory diagnosis only.
8. Day 5 engineering hardened hostile-input handling, resource bounds, artifact compatibility, and reproducibility.
9. Package `0.3.0a1`, built-in rule pack `2.0.0`, is the public alpha checkpoint.

## Results and interpretation

The current development regression result is TP 37, TN 36, FP 4, FN 3: 91.25% accuracy, 90.24% precision, 92.50% recall, 91.36% F1, and 10.00% false-positive rate. The development corpus was visible during detector work, so these values are regression evidence, not generalization accuracy.

The authoritative v0.2 H0 result is:

| TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |

The v0.3 comparison on the already exposed holdout is:

| TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 18 | 6 | 13 | 60.42% | 64.71% | 45.83% | 53.66% | 25.00% |

The v0.3 result is **post-unblinding exploratory evidence**. It does not demonstrate generalization and must not be presented as a second confirmatory holdout. A new untouched, independently reviewed, preregistered holdout is required before making a confirmatory v0.3 generalization claim.

## Evidence status

The original v0.2 H0 remains the authoritative first confirmatory result. Its JSON, the Day 3C failure analysis, and the authentic Day 4C exploratory artifact are tracked as immutable evidence with hashes documented in the [reproducibility guide](reproducibility.md). The original holdout is permanently exposed for this detector-development lineage and must not be reused as fresh validation data.

The corpora remain synthetic-heavy, English-oriented, small, and prevalence-balanced. Static metadata analysis does not measure runtime implementation behavior, server compromise, multi-turn behavior, or real deployment prevalence. See [limitations](limitations.md).
