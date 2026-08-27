# Evaluation methodology

## Research objective

Evaluate whether deterministic static metadata inspection identifies known suspicious patterns in MCP tool definitions while measuring mistakes on realistic benign wording. The experiment evaluates the implemented heuristics, not the trustworthiness of an MCP server.

## Inputs

The bundled corpus contains 80 harmless synthetic MCP tool definitions selected from small JSON catalogs. Forty are labeled benign and forty suspicious. It is explicitly the `development` split: detector development has been informed by these examples, so it is not an independent test set. No holdout corpus is included in this phase. The manifest records split and methodology metadata plus sample ID, source type, selected tool, binary/category ground truth, rationale, normalized difficulty, provenance, optional expected stable rule IDs, and optional expected field locations. No example contains a real secret, operational exploit, network dependency, or executable payload.

## Independent variable

The controlled independent variable is the security characteristic expressed by static tool metadata: ordinary metadata, borderline legitimate wording, instruction-priority language, concealment, sensitive fields, malformed or privileged schemas, capability mismatch, obfuscation, or high-impact permissions.

## Dependent variables

- Accuracy, precision, recall, F1, false-positive rate, false-negative rate, and specificity.
- One-vs-rest precision, recall, and F1 for each detector category.
- Total, mean, median, minimum, maximum, p95, population standard deviation, per-tool mean, and corpus-pass mean for the declared timing boundary.
- Wilson 95% intervals with raw counts for accuracy, recall, and false-positive rate.
- Binary metrics and raw confusion counts stratified by expected category, expected field location, difficulty, and ground truth.

Timings use `time.perf_counter()` and vary by hardware, operating system, Python build, and background load. They are diagnostic measurements, not hardware-independent benchmarks.

## Ground truth

Labels were assigned manually from the intended meaning of each synthetic definition. A suspicious label means the metadata intentionally models a pattern that warrants review; it does not mean a tool is malicious. Category labels describe the modeled characteristic, not necessarily the exact rule that must trigger. Benign borderline cases intentionally include legitimate authentication, privacy, administration, permission, backup, quotation, and encoded-fixture terminology.

Ground-truth changes require a corpus version update and an entry in `evaluation/CHANGELOG.md`. Manifest validation rejects duplicate IDs, invalid labels or splits, unknown categories, inconsistent benign/category labels, malformed field locations, path traversal, missing files, ambiguous catalog selection, and malformed tool definitions. Legacy `easy`/`borderline` difficulty values normalize to `obvious`/`moderate`; new manifests should use `obvious`, `moderate`, or `subtle` explicitly.

## Experimental procedure

From the repository root:

```bash
python -m pip install -e ".[dev]"
mcpsec evaluate evaluation/corpus/manifest.json
mcpsec evaluate evaluation/corpus/manifest.json --format json --output evaluation-result.json
mcpsec evaluate evaluation/corpus/manifest.json --format csv --output evaluation-samples.csv
mcpsec evaluate evaluation/corpus/manifest.json --timing-warmups 3 --timing-repetitions 10 --runs-dir evaluation/runs
mcpsec evaluate evaluation/corpus/manifest.json --timing-mode static-end-to-end --timing-repetitions 10
mcpsec evaluate evaluation/corpus/manifest.json --ablation without-schema --runs-dir evaluation/runs
mcpsec evaluate evaluation/corpus/manifest.json --disable-rule SCH-001 --disable-family capability
mcpsec compare-experiments evaluation/runs/EXPERIMENT-A.json evaluation/runs/EXPERIMENT-B.json
```

The default experiment uses every built-in rule, a `MEDIUM` binary threshold, no suppressions, the `analysis-core` boundary, zero warm-ups, and one measured repetition. A sample is predicted suspicious when it has at least one finding at or above that threshold. Category evaluation records all finding categories, including informational capability context. Custom rules are opt-in with `--rules`. Suppressions are excluded unless `--suppressions` is explicitly provided, and the report records whether they were applied.

`analysis-core` measures per-sample detector/rule/suppression/risk processing after bounded loading and normalization. `static-end-to-end` additionally includes bounded local file loading, normalization, and tool selection in each repetition. Warm-ups execute but are not recorded. Samples are ordered by stable ID, and every measured repetition must return identical findings and risk. Timings use `time.perf_counter()` and remain dependent on hardware, operating system, Python build, and background load; they do not measure server or tool runtime.

Ablation presets and repeatable rule/family exclusions are evaluation-only. The report records the exact enabled and disabled detector, family, and stable rule-ID sets, and its configuration hash changes with the selection. Remaining findings go through the unchanged risk calculation. Ordinary scans, detector definitions, fingerprints, baselines, and drift are unaffected.

For repeatability, JSON output records an experiment ID, application and output-schema versions, Git commit/dirty state when available, selected platform/dependency versions, UTC timestamp, portable invocation, corpus split/version/SHA-256, full active configuration and its SHA-256, sample count, suppression identities, timing observations, uncertainty, strata, and classification threshold. It excludes usernames, hostnames, environment-variable values, absolute paths, and Git diff content. Expected-category and field-location groups may overlap; missingness is explicit, and groups with fewer than 10 samples are marked low evidence. Wilson intervals are reported only for accuracy, recall, and FPR, with null bounds when the denominator is zero.

Preserved artifacts use output schema `3.0.0`. `compare-experiments` rejects mismatched corpus/split/sample/ground-truth/threshold identities, reports B−A paired changes for compatible runs, warns about version or non-ablation differences, and withholds latency deltas unless timing boundary and runtime environment match. Older artifact schemas are rejected rather than silently upgraded. See the [research protocol](research-protocol.md) and complete the [experiment-plan template](experiment-plan-template.md) before a holdout run.

Before a future holdout run, compare the frozen manifests with `mcpsec corpus-check DEVELOPMENT HOLDOUT`. Duplicate IDs and exact canonical tool content are errors. No automatic near-duplicate heuristic is claimed in this phase; a human reviewer must also inspect paraphrases, derivations, and shared templates. The complete split, freezing, unblinding, labeling, timing, and versioning procedure is in the [research protocol](research-protocol.md).

## Bundled-corpus baseline

Development corpus version 1.0.0 currently yields TP 37, TN 36, FP 4, and FN 3: accuracy 91.25%, precision 90.24%, recall 92.50%, F1 91.36%, FPR 10.00%, FNR 7.50%, and specificity 90.00%. These values are calculated by the evaluator and asserted as a regression baseline. They are not holdout accuracy and must be updated transparently if rules or ground truth change.

## Limitations

The development corpus is small, synthetic, English-oriented, and partly constructed around the documented taxonomy. It is suitable for regression testing and reproducible undergraduate research exercises, but it is not representative prevalence data and does not establish real-world accuracy. Samples do not measure runtime implementation behavior, multi-turn attacks, server compromise, social context, or unseen-language generalization. Detector tuning against this corpus can overfit; independent holdout construction and review remain future work.
