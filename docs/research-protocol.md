# Research protocol

## Objective and hypotheses

This protocol evaluates whether deterministic static inspection of MCP tool metadata identifies predefined suspicious metadata characteristics while retaining benign metadata. It evaluates detector behavior on labeled metadata, not whether an MCP server is trustworthy or whether its runtime implementation is safe.

The primary hypothesis is that the fixed detector configuration achieves useful binary and category-level discrimination on data that was not used to tune it. The null hypothesis is that observed discrimination on a held-out set is not meaningfully better than chance or an agreed comparison baseline. This repository does not yet contain the independently created holdout split required to test that hypothesis.

## Threat-model scope

The unit of analysis is one normalized static MCP tool definition. In scope are tool names, titles, descriptions, input and output schemas, annotations, execution hints, metadata, icons, and preserved unknown fields. The experiment covers metadata indicators such as instruction override, concealment, sensitive-data requests, schema concerns, name/capability mismatch, obfuscation, and high-impact capability context.

Runtime behavior, tool invocation, server compromise, multi-turn interaction, model-specific susceptibility, network attacks, metadata-linked resources, and malicious code execution are out of scope. Evaluation must remain offline. Corpus content is hostile data: it is parsed under normal resource limits, never executed, never fetched, and never sent to a model.

## Development and holdout policy

Every corpus manifest declares exactly one `split`: `development` or `holdout`.

- The bundled 80-sample corpus is the **development/regression split**. Its rules and examples have informed detector implementation, so its TP 37, TN 36, FP 4, and FN 3 result is a regression baseline, not independent test accuracy.
- A future **holdout split** must be assembled and labeled independently of detector tuning, assigned different sample IDs, stored in a separate manifest, and frozen before the first scored evaluation.
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
- total, mean, median, minimum, maximum, and p95 single-pass detector time.

Binary failure classes take precedence over category mismatch for the same sample. A false negative with no findings is distinguished from one with findings that all remain below threshold. Full finding records already contain rule ID, category, severity, confidence, field path, evidence, explanation, recommendation, and score contribution.

## Timing methodology

Current timing is a single wall-clock measurement around `analyze_tools` for each already-loaded sample using `time.perf_counter()`. Loading, hashing, Git inspection, environment collection, serialization, and terminal rendering are excluded. These measurements are machine-dependent diagnostics, not a statistically controlled latency benchmark. Repeated trials, warm-up policy, process isolation, uncertainty intervals, and latency comparisons are deliberately deferred.

## Reporting and versioning

Keep development and holdout results separate. A report must state its split, corpus/configuration hashes, label-review status, limitations, and whether suppressions or custom rules were active. Never describe development-corpus results as external test accuracy or real-world attack prevalence.

- Change the corpus version when examples, labels, rationales, provenance, or other research-significant manifest data change intentionally.
- Change the methodology version when labeling, split construction, scoring, or review procedures change.
- Change the built-in or custom rule-pack version when detection behavior changes.
- Change the output schema version when artifact compatibility changes.

Record intentional corpus and metric changes in `evaluation/CHANGELOG.md` and relevant project documentation.

## Post-unblinding policy

After the first holdout result is revealed, archive its artifact and hashes unchanged. Analysis may identify failures, but any detector tuning based on those failures creates a new development iteration. A subsequent independent holdout, or a clearly versioned and honestly described validation set, is required for another unbiased estimate. Never silently relabel a hard case, delete a failure, move a sample between splits, or reuse an exposed holdout as an unseen test set.

## Limitations

The present project has only a small, synthetic, English-oriented development corpus partly constructed around the known taxonomy. It is useful for regression testing, failure inspection, and method rehearsal. It does not establish generalization to unseen servers, languages, ecosystems, adversaries, or runtime behavior. Provenance and label-review fields improve auditability but do not themselves guarantee independence or label correctness. Exact hashing detects identical canonical content, not every paraphrase or shared-template relationship, so human leakage review remains mandatory.
