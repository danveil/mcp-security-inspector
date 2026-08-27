# Pre-registered holdout experiment plan

## Status and study identity

- Study title: Independent holdout evaluation of deterministic MCP tool-poisoning metadata detection
- Plan version: 1.0.1
- Protocol decisions recorded before sample authoring: 2026-08-27T00:28:09Z
- Pre-construction implementation checkpoint: `997c5fcf11a6f0800dceb022426cc32e0d522e04`
- Checkpoint state when protocol decisions were recorded: clean
- Review/freeze amendment recorded: 2026-08-27; no detector or experiment setting changed
- Current freeze status: **configuration and reviewed corpus frozen; final clean Git checkpoint and Day 3A audit pending**
- Research question: How effectively does the lightweight deterministic prototype detect known MCP tool-poisoning patterns on unseen metadata?
- Primary hypothesis: The frozen detector configuration discriminates independently authored holdout samples containing known tool-poisoning constructs from benign metadata with similar security and administrative vocabulary.
- Null hypothesis: The frozen configuration does not provide useful discrimination beyond the agreed descriptive baseline on this holdout.
- Confirmatory analysis: one primary full-detector holdout evaluation after review and commit
- Exploratory analyses: the seven pre-registered detector-family ablations listed below, run only after the primary artifact is preserved

This plan contains no detector predictions or holdout performance results. The final holdout corpus evaluation must not run during construction or review.

## Corpus and isolation

- Development manifest: `evaluation/corpus/manifest.json`, version 1.0.0, split `development`
- Holdout manifest: `evaluation/holdout/manifest.json`, final reviewed version 1.0.1, split `holdout`
- Constructed size and balance: 48 samples; 24 benign and 24 suspicious
- Final reviewed holdout SHA-256: `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8`
- Label-review status: `independently_reviewed`; one blinded reviewer, 47 agreements, one adjudicated retained disagreement, and no abstentions
- Provenance/license policy: repository-authored synthetic or transparently derived inert metadata, distributed under MIT; no secrets, personal data, proprietary material, or fetched metadata
- Exact-overlap control: passed with no errors or warnings; retained in `evaluation/holdout/integrity-report.json`
- Near-duplicate control: detector-free construction-author review retained in `evaluation/holdout/near-duplicate-review.md`; no sample content changed during adjudication
- Coverage and confounding assessment: `evaluation/holdout/coverage-report.md`
- Label access before unblinding: corpus author/reviewer only; detector maintainers must not tune against the holdout

## Frozen primary detector configuration

- Application version: 0.2.0
- Built-in rule pack: `builtin` 1.0.0
- Corpus split: `holdout`
- Classification threshold: `MEDIUM`
- Ablation preset: `full`
- Enabled detector families: `capability`, `concealment`, `injection`, `mismatch`, `obfuscation`, `schema`, `sensitive-data`
- Enabled stable rule IDs: `CAP-001`, `HID-001`, `MIS-001`, `OBF-001`, `OBF-002`, `OBF-003`, `OBF-004`, `PI-001`, `SCH-001`, `SCH-002`, `SEC-001`
- Disabled detector families/rule IDs: none
- Custom rules: none
- Suppressions: none
- Static-analysis-only option: enabled
- Evidence redaction in authoritative research artifact: disabled
- Primary timing mode: `analysis-core`
- Warm-up repetitions per sample: 3
- Measured repetitions per sample: 10
- Sample order: sample ID ascending
- Frozen semantic configuration SHA-256: `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1`

The configuration hash above was calculated through the existing typed configuration builder. The final corpus hash was calculated through structural loading and canonical hashing after independent review and adjudication. No detector was run to obtain either value. A final clean research checkpoint cannot be claimed while the corpus/review files are uncommitted or the working tree is dirty.

## Planned runs

| Run ID | Order | Purpose | Configuration | Timing mode | Warm-ups | Measured repetitions |
|---|---:|---|---|---|---:|---:|
| H0 | 1 | Primary confirmatory classification and latency | full | analysis-core | 3 | 10 |
| H1 | 2 | Secondary local static workflow latency | full | static-end-to-end | 1 | 5 |
| A1 | 3 | Exploratory component contribution | without-injection | analysis-core | 0 | 1 |
| A2 | 4 | Exploratory component contribution | without-concealment | analysis-core | 0 | 1 |
| A3 | 5 | Exploratory component contribution | without-sensitive-data | analysis-core | 0 | 1 |
| A4 | 6 | Exploratory component contribution | without-schema | analysis-core | 0 | 1 |
| A5 | 7 | Exploratory component contribution | without-mismatch | analysis-core | 0 | 1 |
| A6 | 8 | Exploratory component contribution | without-obfuscation | analysis-core | 0 | 1 |
| A7 | 9 | Exploratory component contribution | without-capability | analysis-core | 0 | 1 |

Ablation results are exploratory component-contribution evidence, not causal estimates of real-world attack importance. Ablation latency is not a confirmatory outcome.

## Outcomes and analysis

- Primary classification outcomes: precision, recall, F1, false-positive rate, and raw TP/TN/FP/FN
- Secondary classification outcomes: accuracy, false-negative rate, specificity, and per-category one-vs-rest metrics
- Planned strata: expected category, expected poisoning-bearing field location, difficulty, and benign/suspicious ground truth
- Uncertainty: Wilson score 95% intervals for accuracy, recall, and false-positive rate, always presented with raw counts
- Precision/F1 intervals: omitted because no resampling design is pre-registered
- Small-stratum rule: report all populated groups; mark `n < 10` low evidence and do not rank them as strong comparative results
- Multi-label rule: category and field-location strata may overlap and must not be summed as corpus totals
- Zero denominators: retain the evaluator's numeric compatibility value of 0.0 and explicitly mark the metric undefined
- Multiple comparisons: the primary binary outcomes are confirmatory; category, field, difficulty, and ablation findings are secondary/exploratory and interpreted descriptively

## Latency analysis

- Primary latency statistic: mean per-tool `analysis-core` time from H0
- Secondary latency statistics: median, nearest-rank p95, population standard deviation, minimum, maximum, and mean corpus-pass time
- Secondary boundary: mean complete corpus-pass time from H1 `static-end-to-end`
- Eligibility: latency comparisons require the same recorded runtime environment and timing boundary
- Limitation: results are machine/background-load dependent; no CPU pinning or process isolation is claimed

## Stopping and failure rules

- Run H0 exactly once after the reviewed holdout hash and clean Git checkpoint are frozen.
- Preserve the complete H0 JSON artifact before running H1 or any ablation.
- Do not rerun H0 because the result is unfavorable.
- A rerun is permitted only after a documented technical failure that prevented a valid artifact, such as process interruption or artifact-write failure; preserve the failed-run record and explanation.
- Stop before evaluation if corpus-check fails, independent review remains incomplete, the corpus hash differs from this plan, the working tree is dirty, or configuration hash differs from the value above.

## Artifact handling

- Planned authoritative destination: `evaluation/runs/` plus immutable external research storage
- Output schema: 3.0.0
- Record SHA-256 for every retained JSON artifact
- Comparison direction: later run minus H0 (`B - A`)
- Retention: retain H0, H1, and all declared ablation artifacts unchanged through project examination and the institution's required retention period
- Do not commit generated run artifacts automatically and do not publish them without an explicit review decision

## Post-unblinding policy

After H0 is produced, retain it exactly as generated. Errors may be analyzed, but detector, threshold, severity, risk, suppression, sample, or label changes informed by H0 are post-unblinding exploratory work. The holdout is no longer independent evidence for a detector modified in response to its failures. Any later confirmatory claim requires a new untouched holdout; otherwise the follow-up must be labeled exploratory. Never silently relabel, remove, or rewrite a difficult sample.

## Pre-unblinding blindness attestation

As of the 2026-08-27 review freeze:

- no final holdout evaluation has been run;
- no detector predictions were shown to the independent reviewer;
- no sample wording was changed in response to detector results;
- no holdout triggered-rule output was inspected; and
- no threshold, rule, severity, suppression, risk, or detector setting was tuned from holdout results.

The only adjudication used the pre-existing construct rubric, research protocol, and documented schema-security taxonomy. The holdout remains prediction-unexposed and is ready for Day 3A pre-unblinding audit after the user reviews this diff and creates the clean research checkpoint.

## Results — intentionally blank until authorized unblinding

- Authorized unblinding date/person:
- H0 experiment ID and artifact SHA-256:
- Primary results:
- Secondary results:
- Deviations:
- Confirmatory conclusion:
