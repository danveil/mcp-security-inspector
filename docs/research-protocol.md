# Research protocol

## Objective and hypotheses

This protocol evaluates whether deterministic static inspection of MCP tool metadata identifies predefined suspicious metadata characteristics while retaining benign metadata. It evaluates detector behavior on labeled metadata, not whether an MCP server is trustworthy or whether its runtime implementation is safe.

The primary hypothesis is that the fixed detector configuration achieves useful binary and category-level discrimination on data that was not used to tune it. The null hypothesis is that observed discrimination on a held-out set is not meaningfully better than chance or an agreed comparison baseline. The repository contains a separately constructed and independently reviewed holdout, but it remains prediction-unexposed and must not be evaluated until the documented clean-checkpoint and pre-unblinding gates are complete.

## Threat-model scope

The unit of analysis is one normalized static MCP tool definition. In scope are tool names, titles, descriptions, input and output schemas, annotations, execution hints, metadata, icons, and preserved unknown fields. The experiment covers metadata indicators such as instruction override, concealment, sensitive-data requests, schema concerns, name/capability mismatch, obfuscation, and high-impact capability context.

Runtime behavior, tool invocation, server compromise, multi-turn interaction, model-specific susceptibility, network attacks, metadata-linked resources, and malicious code execution are out of scope. Evaluation must remain offline. Corpus content is hostile data: it is parsed under normal resource limits, never executed, never fetched, and never sent to a model.

## Development and holdout policy

Every corpus manifest declares exactly one `split`: `development` or `holdout`.

- The bundled 80-sample corpus is the **development/regression split**. Its rules and examples have informed detector implementation, so its TP 37, TN 36, FP 4, and FN 3 result is a regression baseline, not independent test accuracy.
- The **holdout split** is stored separately with different sample IDs and was assembled without running detector predictions. One independent reviewer, blinded to expected labels and detector predictions, reviewed all 48 samples. Final clean-checkpoint freeze remains mandatory before the first scored evaluation.
- Holdout labels must remain concealed from anyone tuning detectors until the detector configuration, threshold, custom rules, suppressions, and evaluation procedure are frozen.
- No detector, rule, threshold, severity, score, suppression, or sample label may be changed in response to holdout results and then reported as if the same holdout remained unseen.

Before unblinding, run:

```bash
mcpsec corpus-check evaluation/corpus/manifest.json path/to/holdout/manifest.json
mcpsec corpus-check evaluation/corpus/manifest.json path/to/holdout/manifest.json --format json --output split-integrity.json
```

Duplicate sample IDs and exact canonical tool content across splits are errors. This phase deliberately does not implement a heuristic near-duplicate algorithm: a reviewer must also compare wording, templates, derived examples, and common source material manually. Any suspected derivation or paraphrase should be treated as contamination until resolved. The integrity report records hashes, not private absolute paths.

## Corpus metadata and labeling

Corpus-level metadata records corpus name/version, split, methodology version/note, label-review status, optional source/license policy, and description. Each sample records:

- a stable ID and bounded local file reference;
- binary and category ground truth with rationale;
- normalized difficulty (`obvious`, `moderate`, or `subtle`);
- optional expected rule IDs and strict dotted field locations;
- provenance origin (`synthetic`, `derived`, or `real_world`) with optional source and derivation notes;
- optional researcher notes.

For backward compatibility, legacy `easy` values normalize to `obvious`, legacy `borderline` values normalize to `moderate`, and omitted provenance normalizes to `synthetic`. New manifests should use the current vocabulary explicitly. Field locations use paths such as `description` or `inputSchema.properties.token.description`, with optional numeric indexes such as `annotations.items[0]`; traversal, slashes, empty segments, and arbitrary bracket expressions are rejected.

The corpus owner controls the manifest. Label changes require documented review, a corpus version increment, and an entry in `evaluation/CHANGELOG.md`. A future holdout should use independent reviewers where feasible, record disagreements before resolution, and set `label_review_status` truthfully. Public or derived metadata must have a documented redistribution/licensing policy; secrets, personal data, and operational exploit material are prohibited.

Holdout 1.0.1 received one complete independent review before detector unblinding. Binary agreement was 47/48 (97.9167%) with no abstentions and Cohen's kappa 0.9583. This is agreement with one reviewer, not multi-expert consensus. The sole binary disagreement concerned whether a negative `maxItems` bound is a schema/data-quality defect or a suspicious schema security-review construct. Adjudication retained the original suspicious label because malformed schema is explicitly within the pre-existing corpus rubric, while documenting that malformed schema alone does not prove malicious intent or active tool poisoning. Original difficulty labels were retained separately from reviewer difficulty; exact difficulty agreement was only 16/48 (33.3333%), demonstrating that this dimension is substantially more subjective.

## Frozen experiment configuration

Before a scored holdout run, freeze and record:

1. application version and Git commit;
2. dirty/clean working-tree state;
3. corpus version and SHA-256 identity;
4. classification threshold;
5. every active built-in detector and built-in rule ID;
6. custom rule-pack identity, active rule IDs, semantic configuration hash, and source-file hash when applicable;
7. exact suppression rule/tool identities and source-file hash when applicable;
8. all other evaluation options.

The configuration SHA-256 is calculated from canonical semantic configuration. Ordering that does not affect meaning—such as rule-list, field-list, pattern-list, or suppression-list order—does not change it. Raw rule and suppression file hashes remain separately available to identify the exact files. Changing a research-relevant setting changes the configuration hash.

## Reproducibility record

Each JSON evaluation artifact contains an experiment ID, UTC timestamp, application version, Git commit when available, dirty-state flag, Python/platform/architecture details, selected dependency versions, corpus split/version/hash, full typed evaluation configuration, configuration hash, a portable invocation representation, timing methodology, and sample count. It excludes usernames, hostnames, environment-variable values, and absolute paths.

The corpus SHA-256 covers normalized research-relevant manifest content and the content of every referenced sample file. Manifest object-key formatting, sample ordering, and set-like metadata ordering do not affect the hash; changing labels, rationales, provenance, split metadata, references, or sample-file content does.

Git metadata may be unavailable in an installed wheel, exported source archive, or environment without Git. This is represented by null fields rather than failing the evaluation. A dirty working tree is reported but not serialized as a diff because diffs may contain private data.

## Outcomes and metrics

A sample is predicted suspicious when any finding is at or above the configured severity threshold. The default threshold is `MEDIUM`. The report includes:

- binary confusion matrix, accuracy, precision, recall, F1, false-positive rate, false-negative rate, and specificity;
- one-vs-rest metrics for every known or observed category;
- structured per-sample ground truth, provenance, difficulty, expected and triggered rule IDs, expected field locations, threshold, findings, and researcher notes;
- mechanically classified failures: `false_positive`, `false_negative_no_finding`, `false_negative_below_threshold`, or `category_mismatch`;
- total, mean, median, minimum, maximum, p95, population standard deviation, mean per-tool time, and mean corpus-pass time across recorded observations;
- Wilson score 95% intervals, with raw numerator and denominator, for accuracy, recall, and false-positive rate;
- binary metrics stratified by expected category, expected field location, difficulty, and ground truth.

Binary failure classes take precedence over category mismatch for the same sample. A false negative with no findings is distinguished from one with findings that all remain below threshold. Full finding records already contain rule ID, category, severity, confidence, field path, evidence, explanation, recommendation, and score contribution.

## Timing methodology

Timing uses the monotonic high-resolution `time.perf_counter()` clock and processes samples in ascending sample-ID order. The configuration records the exact boundary, unmeasured warm-up count, and measured repetition count. Every measured repetition must produce the same typed scan result; inconsistent findings or risk cause the experiment to fail. Warm-ups execute the configured boundary but are excluded from observations and predictions.

The primary `analysis-core` boundary measures `analyze_tools` after the sample has been bounded-loaded and normalized. Its primary latency outcome is mean per-tool analysis time, with median, nearest-rank p95, population standard deviation, minimum, and maximum describing dispersion. It includes built-in detectors selected by the evaluation configuration, custom data-only rules, suppressions, risk calculation, and scan-result construction. The secondary `static-end-to-end` boundary reloads, normalizes, and selects the local static sample inside every repetition, then performs the same analysis; its secondary latency outcome is mean complete corpus-pass time. Both exclude corpus hashing, Git/environment inspection, aggregate metrics, serialization, terminal rendering, networking, and all tool invocation. The default remains zero warm-ups and one measured repetition for a quick regression run; a planned latency experiment must declare its counts before execution.

Timing is machine- and load-dependent. It is neither a hardware-independent benchmark nor a runtime MCP server measurement. Compare latency only when the boundary and recorded runtime environment are identical; even then, interpret the delta as evidence from that environment, not a universal performance claim. The runner does not claim process isolation, CPU pinning, or control of background load.

## Evaluation-only ablation methodology

Ablations answer how predictions and metrics change when selected built-in detector outputs are withheld. They estimate contribution within this detector and corpus configuration; they are not causal proof of a family's importance to real-world attacks. They do not change detector patterns, severities, thresholds, risk weights, fingerprints, baselines, or drift behavior, and they never affect ordinary `scan`. Risk is deterministically recalculated from the remaining findings.

| Family ID | Stable built-in rule IDs | Preset |
|---|---|---|
| `injection` | `PI-001` | `without-injection` |
| `concealment` | `HID-001` | `without-concealment` |
| `sensitive-data` | `SEC-001` | `without-sensitive-data` |
| `schema` | `SCH-001`, `SCH-002` | `without-schema` |
| `mismatch` | `MIS-001` | `without-mismatch` |
| `obfuscation` | `OBF-001`–`OBF-004` | `without-obfuscation` |
| `capability` | `CAP-001` | `without-capability` |

`full` enables every family. Repeatable `--disable-family` and `--disable-rule` selections are unioned with the preset. Unknown identifiers are rejected. Disabling every rule in a family omits its detector from evaluation; disabling one rule in a multi-rule family filters that rule's findings while retaining the others. Therefore, single-rule ablation supports effectiveness analysis but must not be interpreted as the exact compute cost of that sub-rule. There is intentionally no “without fingerprinting” or “without drift” preset: fingerprints and drift are separate static-analysis functions and are not part of detector classification.

## Stratification and uncertainty

Strata are calculated only from manifest ground truth and recorded predictions. Expected-category strata can overlap when a suspicious sample has multiple categories; they are not partitions and their counts must not be summed as a corpus total. Field-location strata likewise can overlap. The report always states available and missing sample counts and emits only populated groups; the current development corpus has no expected field-location annotations, so that dimension is reported honestly as 0 available and 80 missing.

Each group includes raw TP, TN, FP, and FN counts plus the usual derived metrics. Metrics with a zero mathematical denominator are listed as undefined even though their machine-readable numeric compatibility value remains `0.0`. A group with fewer than 10 samples is marked `low_evidence` and carries an explicit warning. This flag is descriptive, not a significance test or exclusion rule.

For a binomial proportion with successes `x`, trials `n`, estimate `p=x/n`, and `z=1.959963984540054`, the 95% Wilson interval is:

```text
centre = (p + z²/(2n)) / (1 + z²/n)
margin = z × sqrt((p(1-p) + z²/(4n))/n) / (1 + z²/n)
```

Accuracy uses `(TP+TN)/(TP+TN+FP+FN)`, recall uses `TP/(TP+FN)`, and false-positive rate uses `FP/(FP+TN)`. A zero denominator is recorded as undefined with null estimate and bounds. No confidence interval is claimed for precision or F1 because those require additional assumptions or a separately declared resampling design.

## Artifact preservation and comparison

Use `--runs-dir evaluation/runs` to write a JSON artifact named `<experiment-id>.json` in addition to the requested display/output. Generated files in that directory are intentionally ignored by Git; copy chosen immutable artifacts to controlled research storage and record their SHA-256 externally when required. CI preserves its development evaluation JSON as a GitHub Actions artifact for 14 days. Neither mechanism publishes data.

`mcpsec compare-experiments A.json B.json` reads the current bounded output schema and reports all configuration differences, enabled rule additions/removals, confusion and metric deltas as B−A, paired prediction changes, and newly introduced or resolved FP/FN sample IDs. Corpus hash, split, sample population, paired ground truth, and classification threshold must match; otherwise the artifacts are incompatible and no paired deltas are calculated. Different application versions, Git commits, dirty state, or other non-ablation settings produce explicit warnings. Latency deltas are emitted only for an identical timing boundary and runtime environment.

Output schema `3.0.0` is intentionally strict. Earlier evaluation artifacts lack the full timing, ablation, uncertainty, and stratification record and are rejected with a clear schema error rather than silently coerced into a misleading comparison. Preserve the original older artifact and rerun the same frozen configuration with the current evaluator if a current comparison is needed.

## Reporting and versioning

Keep development and holdout results separate. A report must state its split, corpus/configuration hashes, label-review status, limitations, and whether suppressions or custom rules were active. Never describe development-corpus results as external test accuracy or real-world attack prevalence.

- Change the corpus version when examples, labels, rationales, provenance, or other research-significant manifest data change intentionally.
- Change the methodology version when labeling, split construction, scoring, or review procedures change.
- Change the built-in or custom rule-pack version when detection behavior changes.
- Change the output schema version when artifact compatibility changes.

Record intentional corpus and metric changes in `evaluation/CHANGELOG.md` and relevant project documentation.

## Post-unblinding policy

After the first holdout result is revealed, archive its artifact and hashes unchanged. Analysis may identify failures, but any detector tuning based on those failures creates a new development iteration. A subsequent independent holdout, or a clearly versioned and honestly described validation set, is required for another unbiased estimate. Never silently relabel a hard case, delete a failure, move a sample between splits, or reuse an exposed holdout as an unseen test set.

Complete and freeze the [experiment-plan template](experiment-plan-template.md) before unblinding. Record every planned full and ablation run in advance; adding a new ablation after seeing holdout outcomes is exploratory and must be labeled as such. Comparison artifacts do not authorize detector tuning against an exposed holdout.

## Limitations

The present project has small, synthetic-heavy, English-only development and holdout corpora constructed around the known taxonomy. They are useful for regression testing, failure inspection, and controlled method evaluation but do not establish generalization to unseen servers, languages, ecosystems, adversaries, or runtime behavior. The holdout has only one independent reviewer; high binary agreement does not establish external validity, and the low difficulty agreement shows substantial subjectivity. Provenance and label-review fields improve auditability but do not themselves guarantee independence or label correctness. Exact hashing detects identical canonical content, not every paraphrase or shared-template relationship, so documented human leakage review remains necessary.
