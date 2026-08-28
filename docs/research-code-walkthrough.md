# Research Code Walkthrough and Source Ownership

> **Training status:** Repository-grounded source-reading guide created at
> `21ce6192e082ec7152b10bf9b7a9232237bc562b`. It does not change or evaluate
> detectors. Synthetic examples are **TRAINING ONLY — NOT RESEARCH DATA**.
>
> **Authority rule:** source defines implementation behavior; tests define
> protected behavior; frozen artifacts define historical results. Documentation
> is orientation, not an override of code or evidence.

## 1. How to use this walkthrough

For each behavior, open the named file and answer: who calls this symbol, what
data enters/leaves, which invariant it protects, which test would fail, and what
research claim depends on it. Do not memorize line numbers; locate symbols with
`rg -n "symbol" src tests`.

## 2. Critical code surface

The walkthrough inspected 30 source modules plus the corresponding test groups,
rules, manifests and two frozen JSON artifacts. These 33 primary symbols form
the ownership core.

| File / symbol | Role and calls | Input → output / important state | Invariant, purpose, tests, and failure risk |
|---|---|---|---|
| `cli.py::scan` | Typer command; calls `analyze`, renderer/serializer, then fail-on | CLI options → report/output/exit | Static command coordination. `test_cli.py`; bad change can alter exit or expose unsafe output. |
| `cli.py::analyze` | Loads custom rules/suppressions; calls `analyze_file` | paths/options → `ScanReport` | One resolved config for scan. Rules/suppression tests; misunderstanding: it is not detector logic itself. |
| `resource_policy.py::strict_json_loads` | Used by every bounded JSON loader | text → Python JSON value | Reject duplicate keys and non-finite numbers. `test_strict_json.py`; ambiguity if weakened. |
| `resource_policy.py::validate_structure` | Traverses loaded values | JSON-like value → success/error | Depth/node/text bounds. `test_resource_policy.py`; hostile memory/work growth if broken. |
| `loader.py::load_json/load_tools` | Bounded file load and shape extraction | path → raw tool mappings | 10 MiB, valid shape, ≤1,000 tools. `test_loader.py`; not normalization yet. |
| `normalizer.py::normalize_tool(s)` | Alias validation, NFC, typed conversion | raw mapping(s) → `ToolDefinition` list | Required object `inputSchema`, unique names, unknown-field preservation. `test_normalizer.py`; silent alias loss changes security meaning. |
| `models.py::ToolDefinition` | Canonical typed metadata model | validated fields | Extra fields forbidden in model; vendor fields carried via `unknown_fields`. Model/normalizer tests. |
| `detectors/base.py::all_text_fields` | Deterministic broad field/key traversal | tool → `(path,text)` list | Nested security-relevant metadata stays visible. Detector traversal tests; ordering/path regressions affect evidence. |
| `detectors/base.py::poisoning_text_fields` | Text-value traversal for injection/concealment | tool → selected `(path,text)` | Avoids unintended key matching while covering nested values. Injection/secrecy tests. |
| `detectors/base.py::bounded_context/has_local_pattern` | Sentence/local relation and negation scope | text/span → context/boolean | Prevent cross-field/sentence overreach. Context tests; broad negation could suppress real signals. |
| `detectors/base.py::finding` + `models.py::Finding` | Constructs bounded typed evidence | rule data → `Finding` | Stable rule/category/severity/confidence/score/path. Reporter/rule tests; fields feed research artifacts. |
| `detectors/__init__.py::BUILTIN_DETECTORS` | Production family registry | seven detector instances | Stable execution set/order. Experiment registry test; omission silently changes behavior. |
| `rules/builtin.py::RULE_EXPLANATIONS` | Public metadata for 16 IDs | ID → explanation tuple | Stable explainability and collision namespace. CLI/rule tests; not detector execution. |
| `scanner.py::analyze_tools` | Main analysis orchestration | normalized tools/config → `ScanReport` | Detect → suppress → retain → risk. Scanner-limit tests. Current P0: decision uses retained state. |
| `scanner.py::_retain_findings` | Severity-first deterministic output reservoir | findings/capacity → retained findings | 64/tool, 2,048/report, 8,192 evidence chars/tool. `test_scanner_limits.py`; presentation should not define future semantics. |
| `risk.py::calculate_risk` | Rule deduplication, confidence, category caps, synergy | findings → `(0..100, Severity)` | Deterministic order-independent capped risk. `test_risk.py`; finding severity is distinct. |
| `suppressions.py::load_suppressions` + `scanner.is_suppressed` | Data-only suppressions | bounded file + known IDs → validated scopes/filter decision | Exact rule/tool scope and justification. `test_suppressions.py`; global misuse hides evidence. |
| `rules/loader.py::load_rule_pack` | Bounded JSON/safe-YAML custom configuration | path → typed `RulePack` | ≤200 rules, allowed fields, literal patterns, limits. `test_rules.py`; never executable regex/code. |
| `rules/loader.py::validate_custom_rule_ids/CustomRuleDetector` | Collision gate and custom execution | definitions/tool → findings | Unique IDs; case-insensitive literal containment. Rule tests; collision corrupts identity. |
| `representations.py::decode_representations` | Strict depth-one textual decoding | sorted text fields → `DecodedBatch` | 512 input/output, 4/field, 32/tool, 4,096 retained, printable UTF-8. `test_representations.py`. |
| `obfuscation.py::ObfuscationDetector.detect` | OBF-001…005 execution and semantic gate | tool → findings | Decode does not execute/fetch/recurse. Obfuscation tests; unsupported forms remain FNs. |
| `canonicalizer.py::canonical_json/canonical_tool` | Stable selected representation | JSON/tool → canonical string | sorted object keys, preserved array order, NFC, finite numbers, provenance excluded. Canonicalizer tests. |
| `fingerprint.py::fingerprint_tool` | Full/component SHA-256 | normalized tool → `Fingerprints` | Security-significant source included; internal provenance excluded. Fingerprint tests. |
| `baseline.py::create_baseline/load_baseline` | Stores fingerprints plus privacy-conscious summary | tools/file → `BaselineFile` | Bounded, unique tools; summary omits values/descriptions. Baseline tests. |
| `compare.py::compare_baseline` | Added/removed/changed/conservative rename | current tools + baseline → `Drift[]` | Rename only one-old/one-new equal component signature. Compare tests; drift ≠ compromise. |
| `reporter.py::render_terminal/serialize` | Common `ScanReport` to table/JSON/CSV/SARIF | report → inert output | terminal escaping, CSV formula neutralization, budget visibility. `test_reporter.py`. |
| `evaluation/loader.py::load_corpus` | Bounded manifest/sample loading | manifest → typed manifest + samples | split/paths/labels/tool selection validated. Evaluation-loader tests. |
| `evaluation/evaluator.py::evaluate_corpus` | Full experiment engine | manifest/config/timing → `EvaluationReport` | threshold prediction, findings, metrics, strata, timing, identities. Experiment tests; also contains P0 coupling. |
| `evaluation/metrics.py::confusion/calculate_metrics/timing_statistics` | Binary and timing arithmetic | labels/matrix/observations → typed metrics | Safe zero denominator; explicit repetitions. Metric tests. |
| `evaluation/uncertainty.py::wilson_interval` | Wilson 95% interval | numerator/denominator → interval | Count/denominator preserved; zero handled. Experiment uncertainty tests. |
| `evaluation/ablation.py::resolve_ablation` | Resolves families/rules/detectors | preset/disabled IDs → `ResolvedAblation` | Unknown IDs rejected; exact enabled identities recorded. Ablation tests. |
| `evaluation/research.py::build_evaluation_configuration/configuration_sha256` | Semantic experiment identity | resolved settings → config/hash | Custom rule semantics, suppressions, timing and resolved rules bind identity. Research tests. |
| `evaluation/comparison.py::load_evaluation_artifact/compare_experiments` | Historical validation and paired comparison | artifact(s) → validated report/comparison | Supports 3.0.0/3.1.0; self-consistency before deltas. Historical experiment tests. |

Common misunderstandings: the explanation registry is not the detector registry;
aggregate risk is not the evaluation threshold; `--redact` is not whole-report
privacy; a hash is not authenticity/safety; and opt-in loopback retrieval means
the project is static by default, not universally zero-network.

## 3. Trace mission 1 — CLI to scan report

Safe documented command:

```powershell
mcpsec scan src/mcpsec/resources/mixed_tools.json --format json --fail-on high
```

1. Typer dispatches `cli.scan(file, format, rules, suppressions, redact, fail_on,
   output)`.
2. `cli.analyze` resolves custom rules and known suppression IDs, then calls
   `scanner.analyze_file`.
3. `loader.load_tools` uses `load_bounded_json` → `strict_json_loads` and
   `validate_structure`, then `extract_tools` selects an accepted catalog shape.
4. `normalizer.normalize_tools` produces unique typed `ToolDefinition` objects.
5. `scanner.analyze_tools` invokes each `BUILTIN_DETECTORS` member and optional
   `CustomRuleDetector`.
6. Each detector yields typed `Finding` objects; exact suppressions remove some.
7. `_retain_findings` creates deterministic presentation output; current code
   passes that retained list to `calculate_risk`.
8. `ToolScanResult` and `FindingBudgetStatus` become one `ScanReport`.
9. `reporter.report_json` serializes the model. Other formats use the same report.
10. `--fail-on high` checks retained finding severities and exits 1 if any is
    HIGH/CRITICAL; input errors exit 2 and internal failures exit 3.

**Captain must be able to explain this path without notes.**

## 4. Trace mission 2 — one harmless tool through the analyzer

**TRAINING ONLY:** `{"name":"weather_lookup","description":"Returns a city forecast.","inputSchema":{"type":"object","properties":{"city":{"type":"string"}}}}`

| State | Actual code transition | Conceptual result |
|---|---|---|
| Raw input | strict JSON/file loader | untrusted mapping with original keys/strings |
| Validated input | resource policy + `extract_tools` | bounded catalog of mappings |
| Normalized data | `normalize_tool` | NFC `ToolDefinition`, alias-resolved schema, preserved unknowns |
| Detector input | field traversals and schema/capability helpers | deterministic paths such as `description` and schema keys/values |
| Detection state | detector-local lists | likely no built-in findings for this harmless example |
| Retained findings | `_retain_findings` | bounded presentation subset; empty here |
| Decision/risk state | `calculate_risk(retained)` today | score 0 / INFORMATIONAL; currently coupled to retention |
| Presentation | `ScanReport` → renderer | “No indicators detected” / structured empty findings |

Correct future model: detection state feeds decision state independently, while
presentation receives a bounded retained subset. Current code collapses them by
calculating decisions from retained findings after capacity is applied.

## 5. Trace missions 3–8 — representative and v0.3 rules

### Mission 3 — SCH-001 end to end

- **Registration:** `SchemaDetector()` is in `detectors/__init__.py::BUILTIN_DETECTORS`;
  `RULE_EXPLANATIONS["SCH-001"]` supplies CLI explanation metadata.
- **Input:** `SchemaDetector.detect` receives normalized input/output schemas.
- **Mechanism:** `schema_error` selects the declared/default JSON Schema dialect
  and calls `jsonschema` validator `check_schema`.
- **Finding:** invalid schema produces MEDIUM `SCH-001`, confidence .98, score 14,
  field `input_schema` or `output_schema` through `base.finding`.
- **Downstream:** scanner suppression/retention/risk/reporting apply normally.
- **Direct tests:** `test_schema_detector.py::{test_malformed_schema,
  test_schema_detector_reports_malformed,test_output_schema_is_validated}` plus
  R08 historical artifact compatibility tests.
- **Boundary:** it identifies schema invalidity, not attacker intent, runtime
  exploitability or all semantic misuse. Vendor/draft mismatch can create a FP;
  a valid but dangerous schema is a possible FN for this rule.

### Mission 4 — PI-002

`InjectionDetector` is registered as the injection family. For each
`poisoning_text_fields` value, `instruction_priority_signal` finds three elements
inside `bounded_context`: authority language, an instruction/policy object, and a
conflict target involving agent/user/conversation guidance. Scoped
`PRIORITY_NEGATION` and `is_educational_reference` can reject the relation. The
returned `TextSignal` spans the earliest/latest matched elements; `finding`
creates HIGH PI-002 (confidence .84, score 23). Tests are
`test_instruction_priority_construct`, benign counterexamples, scoped negation,
educational scoping, and nested traversal in `test_injection_detector.py`.

PI-002 was added after H0 showed authority/paraphrase misses. It intentionally
does not treat generic CSS/data priority as agent instruction authority. Novel
phrasing, other languages or relations spread outside the bounded context can be
missed. Its exposed-holdout result is post-unblinding exploratory, not
confirmatory validation.

### Mission 5 — HID-002

`SecrecyDetector.detect` traverses poisoning text values. `concealment_signal`
requires an omission action (`omit`, `withhold`, etc.), material activity and an
observer/report/disclosure concept inside bounded sentence context. Local
negation—with coordinated-clause handling—prevents some false matches. It emits
HIGH HID-002 (confidence .85, score 22). `test_secrecy_detector.py` covers the
construct, benign omission/UI examples, sentence-scoped negation and coordinated
negation. Unlike PI rules, HID-002 concerns withheld visibility, not instruction
priority. It does not join phrases across fields and can miss euphemisms or
multilingual concealment.

### Mission 6 — SEC-002

`SensitiveDataDetector` uses broad `all_text_fields`. `sensitive_action_signal`
locates a credential/security term and a handling action within a 96-character
bounded context, rejecting locally negated actions and safe placeholder/redacted
contexts. SEC-001 still records terminology (LOW in legitimate/benign context,
otherwise MEDIUM); an accepted action additionally emits MEDIUM SEC-002
(confidence .84, score 15). Tests cover active actions, benign terminology,
field-local disclaimers, unrelated negation and deterministic mapping order.

The v0.3 exposed evaluation retained all six historical binary FPs in aggregate.
Repository artifacts support that observation, but not a universal causal claim
about SEC-002. SEC-001’s historical four FPs and SCH-002’s two remained relevant;
the exact v0.3 per-sample rule record must be consulted before attributing any
individual outcome.

### Mission 7 — MIS-002

`MismatchDetector._purpose_capability_mismatch` builds purpose from
name/title/description and obtains structured `CapabilitySignal` objects from all
text fields. A capability must be unaligned with fixed purpose patterns and have
independent corroboration: narrow/offline purpose, sensitive/destructive
capability, multiple unrelated capabilities, no-confirmation language, or
concealment. Evidence records purpose field, capability field/category and
corroborator; field paths are cross-field (`purpose <-> capability`). It emits
MEDIUM, or HIGH for destructive concealment. `test_mismatch_detector.py` covers
corroborated cases, aligned/simulation negatives, cross-field disclaimers,
coordinated negation and non-corroborating negated concealment.

This is relational rather than one keyword. Day 4C recovered known exposed
failures, but those are diagnostic recoveries on data that shaped the rule—not
generalization gains.

### Mission 8 — OBF-005

`ObfuscationDetector.detect` calls `decode_representations(all_text_fields(tool))`.
`representations.py` recognizes numeric HTML entities, prefixed/separated hex
bytes, decimal character codes and strict Base64. Candidates are sorted,
overlaps removed, and decoded exactly once. Actual bounds are:

- candidate input ≤512 characters; decoded output 8–512 characters;
- ≤4 candidates per field and ≤32 attempts per tool;
- ≤4,096 retained decoded characters;
- valid Unicode/UTF-8, no NUL, ≥90% permitted printable text.

Accepted text is checked with fixed injection-priority, concealment,
sensitive-action and high-impact-capability signals. A match produces MEDIUM
OBF-005 (confidence .88, score 14); a budget issue can produce INFORMATIONAL
OBF-005 with explicit reason. Tests in `test_representations.py` prove exact
formats, boundaries and depth one; `test_obfuscation.py` covers high-risk/safe
decodes, no recursion, educational context and redaction. No decoder executes,
decompresses, imports, fetches or invokes anything. Bounded one-step recognition
limits expansion, interpretation and FP surface; unsupported/nested/encrypted
forms are intentionally outside coverage.

## 6. Trace missions 9–15 — configuration, identity, reporting and decisions

### Mission 9 — custom rules

CLI `--rules` → `load_rule_pack` selects strict bounded JSON or `SafeLoader` YAML
→ Pydantic `RuleDefinition`/`RulePackMetadata` validation → limits of 1 MiB,
200 rules, 32 patterns/rule, nine fields, 256 characters/pattern → allowed field
roots → `validate_custom_rule_ids` rejects duplicates and built-in collisions →
`CustomRuleDetector` performs case-insensitive **literal** containment over
traversed fields. It is appended after built-ins in `analyze_tools`.

For experiments, CLI records custom pack name/version, semantic rule definitions,
and source-file SHA-256; `build_evaluation_configuration` and
`configuration_sha256` bind semantic identity. Invalid files raise
`RuleValidationError`/CLI input exit. `test_rules.py`, CLI custom-rule tests and
`test_evaluation_research.py` protect this boundary. Do not add executable
expressions or user regexes.

### Mission 10 — suppressions

CLI `--suppressions` → `load_suppressions` uses bounded strict JSON/safe YAML →
requires only a top-level list, ≤500 items, known rule IDs, unique `(rule,tool)`
scopes and a 10–1,000 character justification → `scanner.is_suppressed` matches
exact rule ID and either exact tool name or global `None` → suppressed findings
are removed before retention/risk/reporting.

There is no sentence/context suppression language: scope is only rule and
optional tool. Detector-local sentence/negation logic is separate. Experiments
record suppression identities and file hash; H0 used none. Tests are
`test_suppressions.py`, evaluation’s explicit-suppression test and CLI identity
tests. An undocumented/global suppression can hide true evidence and change the
configuration hash and metrics.

### Mission 11 — fingerprint and baseline

Normalized `ToolDefinition` → `canonical_tool` excludes internal provenance,
includes raw `source` when supplied, NFC-normalizes strings, sorts object keys,
preserves arrays and serializes compact finite JSON → `fingerprint.sha256` uses
UTF-8 SHA-256 → `fingerprint_tool` creates full plus description/input/output/
annotations/execution/metadata component hashes. `create_baseline` pairs these
with a summary of property/key names, not descriptions/default/example values;
`write_baseline` persists JSON and `load_baseline` performs bounded strict load.

Tests: canonicalizer, fingerprint and baseline suites. A hash supports selected
identity/integrity comparison. It does not prove safety, benignness, authorship,
authenticity without a trusted binding, or absence of poisoning.

### Mission 12 — drift

`cli.compare` loads current normalized tools and a baseline, then
`compare_baseline` indexes exact names/fingerprints. Unique removed/added pairs
with the same six-component signature become `tool_renamed`; ambiguous groups do
not. Remaining differences become `tool_added`, `tool_removed`, or
`tool_changed` with component fields and optional structural summary details.
CLI renders a drift table. `test_compare.py` covers every kind and ambiguity.
This integrity path asks “what changed?”; detectors ask “what configured signal
is present?” Neither alone proves compromise.

### Mission 13 — reporting

`ScanReport` is the common source of truth. `render_terminal` escapes untrusted
controls/Rich markup with `terminal_safe`; `report_json` dumps the typed model;
`report_csv` uses `neutralize_csv` to prefix formula-like cells; `report_sarif`
maps findings to SARIF 2.1.0 and includes budget state. `serialize` dispatches
structured formats. `test_reporter.py` covers parseability, no ANSI, formula
injection, terminal literalness, SARIF and budget visibility.

Presentation should consume a completed decision/result model. It should never
silently decide whether a tool is affected; the current retained-list coupling
violates that desired separation upstream.

### Mission 14 — finding budgets and the P0 defect

`resource_policy.py` defines 64 findings/tool, 2,048/report and 8,192 retained
evidence characters/tool. In `scanner.py`:

1. lines around `analyze_tools` materialize all detector findings and suppress;
2. `_retain_findings` sorts severity-first and applies tool/report/evidence caps;
3. `calculate_risk(retained)` computes risk from the presentation subset;
4. `ToolScanResult.findings` contains retained findings and records detected count.

Consequences: `reporter.render_terminal` affected counts use
`bool(result.findings)`; `cli.scan --fail-on` scans retained findings; and
`evaluation/evaluator.py` recomputes/report-caps retained findings then predicts
suspicious from their severities. After capacity exhaustion, detected findings
can yield risk zero, “clean,” no fail-on exit and benign prediction.

Desired future flow:

```text
DETECTION STATE (bounded rule/category/severity facts)
        |
        v
DECISION STATE (risk, classification, fail-on, affected count)
        |
        v
PRESENTATION / RETENTION STATE (bounded detailed findings/evidence)
```

Current flow passes retained presentation details into decision calculation.
Likely remediation surface: `scanner.py`, `models.py`, `risk.py`, `cli.py`,
`reporter.py`, `evaluation/evaluator.py`, `evaluation/models.py`, artifact schema/
comparison and configuration/version identity. Required tests: decision/risk/
fail-on/affected/evaluation invariance across tiny versus large presentation
budgets; later-tool and catalog-order cases; synergy/dedup under overflow;
deterministic retention; artifact round trip/backward compatibility; full
development regression. Existing `test_scanner_limits.py` exposes truncation but
does not require decision independence. Do not fix it in this mission.

### Mission 15 — `--fail-on`

Typer parses `FailSeverity` (`medium`, `high`, `critical`). After output,
`cli.scan` converts it to `Severity` and exits 1 if any **retained finding** has
equal/higher `SEVERITY_RANK`; clean/no qualifying finding exits 0. It does not
compare aggregate risk.

- **Training A:** one retained HIGH PI-002 and `--fail-on high` → output then exit
  1, even if aggregate risk band is LOW.
- **Training B:** a later HIGH finding detected after global retention capacity
  is exhausted → current retained list can be empty, so exit 0: the P0 defect.

`test_cli.py::{test_fail_on_high,test_clean_does_not_fail_threshold}` protects
normal cases; future overflow-specific exit tests are required.

## 8. Trace missions 16–20 — evaluation, statistics and ablation

### Mission 16 — corpus to prediction

`evaluation.loader.load_corpus` reads a bounded manifest, verifies its declared
split and sample references, loads each sample and selects the named tool. The
typed sample carries a ground-truth label but the analyzer receives only the tool
definition. `evaluation.evaluator.evaluate_corpus` resolves the exact detectors,
threshold, custom-rule and suppression configuration; performs configured
warm-ups; times measured repetitions; and uses `_analyze_sample` to produce a
prediction. A sample is suspicious when any retained finding meets the configured
severity threshold. That retained-list dependency is part of the P0 coupling,
not a preferred architecture.

Predictions plus expected labels feed `metrics.confusion`; findings and sample
metadata feed stratification; timing observations feed `timing_statistics`;
research helpers bind Git/runtime/corpus/configuration identities; finally the
typed report is serialized as one immutable experiment artifact. This mission did
not execute that path.

### Mission 17 — manually own the H0 metrics

For the frozen v0.2 H0: TP=5, TN=18, FP=6, FN=19, total=48.

| Metric | Arithmetic | Result | Meaning here |
|---|---:|---:|---|
| Accuracy | `(5+18)/48` | 47.92% | Correct decisions among all tools. |
| Precision | `5/(5+6)` | 45.45% | Suspicious predictions that were truly suspicious. |
| Recall | `5/(5+19)` | 20.83% | Suspicious tools detected. |
| Specificity | `18/(18+6)` | 75.00% | Benign tools correctly left benign. |
| False-positive rate | `6/(6+18)` | 25.00% | Benign tools incorrectly flagged. |
| F1 | `2*5/(2*5+6+19)` | 28.57% | Precision/recall harmonic balance. |

The arithmetic lives in `evaluation/metrics.py`; the authoritative values live
in the frozen H0 artifact. A poor result is useful evidence about prototype
effectiveness. It is not permission to rewrite the primary experiment.

### Mission 18 — Wilson intervals

`evaluation/uncertainty.py::wilson_interval` converts a count and denominator to
a bounded 95% interval. Unlike a naive `p ± 1.96*sqrt(...)`, Wilson behaves better
for small N and proportions near zero or one. It still cannot create information:
N=48 yields broad uncertainty, and strata containing only 3–6 examples are
especially weak. The artifact preserves numerator/denominator so readers can
audit the interval. Zero denominators are handled explicitly.

### Mission 19 — latency ownership

`evaluation/evaluator.py` distinguishes two boundaries:

- `analysis-core`: normalized tool analysis, excluding file/catalog loading;
- `static-end-to-end`: bounded static loading plus normalization and analysis.

Warm-ups are discarded; measured repetitions are retained. `timing_statistics`
reports mean, median and nearest-rank p95. Repetitions reduce incidental noise but
do not make results portable across machines, Python versions or background load.
The preregistered historical primary used three warm-ups and ten analysis-core
measurements; secondary timing used one warm-up and five static-end-to-end
measurements. Do not change boundaries after seeing results.

### Mission 20 — family ablations

`evaluation/ablation.py::resolve_ablation` maps a named preset to exact disabled
families/rule IDs and records what remains enabled. The seven historical family
ablations are without injection, concealment, sensitive-data, schema, mismatch,
obfuscation and capability. The full configuration remains primary; ablations are
secondary contribution probes. “Removing family X changed Y on this corpus” does
not establish real-world causation or universal importance.

## 9. Trace missions 21–26 — artifact and evidence ownership

### Mission 21 — artifact creation

`evaluation.research.build_evaluation_configuration` creates a semantic config
record; `configuration_sha256` hashes its canonical representation. The evaluator
adds application/rule-pack versions, Git commit and dirty state, corpus identity,
runtime/platform, timing protocol, invocation, UTC timestamp and experiment ID.
`evaluation.models.EvaluationReport` validates the result before JSON output.
These fields answer “what exactly ran, on what data, under what conditions?”

### Mission 22 — hashing and Windows newline risk

Canonical hashes protect semantic JSON identities, while file SHA-256 protects
exact bytes. They answer different questions. Git checkout conversion such as
global `core.autocrlf=true` can change LF to CRLF and therefore change byte hashes
even when text looks identical. Recovery guidance uses an LF-safe clone:

```powershell
git clone -c core.autocrlf=false https://github.com/danveil/mcp-security-inspector
```

Never “repair” a mismatch by editing frozen evidence. First distinguish canonical
corpus/configuration hashing from byte-level file hashing, verify the commit/tag,
and inspect newline policy. A hash proves identity relative to an expected value;
it does not prove safety, authorship or maliciousness.

### Mission 23 — historical schema compatibility

Current experiment artifacts use schema `3.1.0`; comparison/loading deliberately
supports historical `3.0.0`. `evaluation.comparison.load_evaluation_artifact`
validates internal counts, metrics, identities and rule-set information before
comparison. Historical rule identities must remain historical: current code must
not pretend an old artifact was generated by the current detector. Removing this
compatibility would break reproducible interpretation; silently upgrading values
would rewrite history.

### Mission 24 — v0.2 H0 evidence

Authoritative artifact:
`evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json`.
Expected file SHA-256:
`3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80`.
It records the first confirmatory result within this pilot: 5/18/6/19 and the
metrics in Mission 17. Documentation interprets it; the artifact owns the result.

### Mission 25 — v0.3 exposed exploratory evidence

Authoritative artifact:
`evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json`.
Expected SHA-256:
`d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b`.
It records TP=11, TN=18, FP=6, FN=13; accuracy 60.42%, precision 64.71%, recall
45.83%, F1 53.66%, FPR 25%. Because rule design followed inspection of exposed
H0 failures, this is post-unblinding exploratory evidence—not fresh confirmation
or proof of improved generalization.

### Mission 26 — optional loopback retrieval

`cli.fetch` is explicit opt-in. `retrieval.fetch_local_catalog` permits only
explicit HTTP(S) loopback destinations, rejects credentials/fragments, pins and
revalidates resolved loopback addresses, disables environment proxies and
redirects, performs only MCP initialization and paginated `tools/list`, and never
invokes tools. It applies timeout, 10 MiB response, 100-page and tool-count bounds
(default 500, maximum 1,000). The retrieved catalog still enters the normal static
pipeline. `test_retrieval.py` owns SSRF, pagination and resource-boundary cases.

## 10. Source and test ownership maps

The 33-row **Critical code surface** table in section 2 is the source ownership
table: each row names the primary owner, caller/data flow, invariant, test group
and consequence. Use this test map to connect boundary behavior to protection.

| Behavior to protect | Primary tests | Regression if ownership disappears |
|---|---|---|
| Hostile/oversized JSON and structure | `test_resource_policy.py`, `test_loader.py` | Excessive work/memory or ambiguous catalog input. |
| Duplicate JSON keys | `test_strict_json.py` | Last-key-wins ambiguity hides security-significant data. |
| NaN/Infinity rejection | `test_strict_json.py`, canonicalizer tests | Non-portable values break canonical identity. |
| Alias conflicts and tool-name collisions | `test_normalizer.py` | Conflicting fields silently selected; results attach to wrong tool. |
| Depth/node/string/tool bounds | resource-policy and loader limit tests | Resource exhaustion or nondeterministic truncation. |
| Local sentence/negation scoping | injection, secrecy and sensitive-data tests | Unrelated benign text suppresses or triggers signals. |
| Built-in registry and stable IDs | rule registry/experiment tests | Silent detector-pack drift or identity collision. |
| Strict bounded decoding | `test_representations.py`, `test_obfuscation.py` | Recursive expansion, garbage findings or missed supported encodings. |
| Deterministic finding retention | `test_scanner_limits.py` | Order-dependent reports and unstable evidence. |
| Risk caps/dedup/synergy | `test_risk.py` | Scores exceed bounds or duplicate rules inflate decisions. |
| Custom-rule validation/collisions | `test_rules.py` | Executable/regex configuration or identity corruption. |
| Suppression scope/known IDs | `test_suppressions.py` | Accidental global hiding or dead suppression entries. |
| Canonical fingerprints | canonicalizer/fingerprint tests | Equivalent metadata hashes differently or an important change is invisible. |
| Baseline privacy and rename conservatism | baseline/compare tests | Raw values leak or unrelated add/remove inferred as rename. |
| Terminal/CSV/SARIF safety | `test_reporter.py` | Escape/control/formula injection or invalid structured output. |
| Loopback-only retrieval | `test_retrieval.py` | SSRF, redirect/proxy escape or resource overrun. |
| Confusion metrics and zero denominators | evaluation metric tests | Incorrect results or divide-by-zero behavior. |
| Wilson interval arithmetic | uncertainty/experiment tests | Misstated confidence or lost denominators. |
| Artifact 3.0.0/3.1.0 compatibility | historical experiment/comparison tests | Old evidence rejected or reinterpreted. |
| Corpus/configuration identities | research/corpus integrity tests | Non-equivalent experiments compared as equivalent. |

### Trust boundaries

| Boundary | Untrusted side | Trusted enforcement | Residual risk |
|---|---|---|---|
| File → loader | bytes, JSON/YAML structure | bounded reads, strict parser, structure limits | Supported hostile input still consumes bounded work. |
| Raw mapping → model | aliases, names, nested metadata | normalizer/model validators | Semantic deception can remain syntactically valid. |
| Tool metadata → detectors | all text/schema/vendor fields | inert traversal and deterministic rules | Rule bypasses and benign collisions remain possible. |
| Custom config → detector | rule/suppression files | data-only schemas, literal matching, known IDs and caps | Broad authorized suppressions can hide findings. |
| Retrieval endpoint → catalog | loopback HTTP server | address checks, no proxy/redirect, body/page/tool limits | A malicious local service remains hostile input. |
| Findings → report consumer | attacker-controlled names/evidence | escaping, neutralization, truncation, redaction | Consumers must still treat strings as data. |
| Baseline → drift decision | possibly stale/untrusted baseline | schema validation and component hashes | A compromised baseline can legitimize malicious state. |
| Artifact → research claim | copied/edited/mismatched file | schema/self-consistency and expected hashes | Hash expectations need trustworthy provenance. |

### Data-state model

```text
raw bytes → parsed hostile JSON/YAML → bounded validated catalog
→ normalized typed tools → detector-produced facts
→ suppression-filtered detection state → decision state
→ retained presentation state → terminal / JSON / CSV / SARIF

canonical normalized tools → fingerprints → baseline → drift records
corpus + frozen config → predictions → matrix/metrics → experiment artifact
```

Do not confuse states: validation is not normalization; a finding is not aggregate
risk; report retention is not detection; drift is not maliciousness; a prediction
is not ground truth; an artifact is evidence, not a universal conclusion.

### Research claim to implementation traceability

| Claim/evidence question | Code/data owner | What may honestly be said |
|---|---|---|
| Static and inert by default | loader, detectors, CLI; retrieval is separate opt-in | Scans do not execute supplied tools or metadata. |
| Deterministic rule set | registry, rules, scanner, canonical config | Same bounded input/config should produce stable findings. |
| Lightweight on tested setup | evaluator timing + artifact metadata | Report measured context; do not claim universal speed. |
| H0 effectiveness | frozen v0.2 artifact | Report exact pilot metrics and uncertainty. |
| v0.3 exploratory change | five rule implementations + Day 4C artifact | Better values on exposed corpus, not confirmed generalization. |
| Reproducibility | Git/rule/corpus/config hashes and schema | Recorded materials and protocol are identifiable. |
| Integrity drift | canonicalizer/fingerprint/baseline/compare | Security-significant changes can be reported; intent is not inferred. |
| Resource safety | input/retention/decoding/retrieval limits | Work/output is bounded at documented layers. |

## 11. Reading route and ownership checkpoints

### Top 15 files, tiered

1. **Orientation:** `README.md`, `src/mcpsec/cli.py`, `src/mcpsec/models.py`.
2. **Input pipeline:** `resource_policy.py`, `loader.py`, `normalizer.py`.
3. **Analysis:** `detectors/base.py`, one representative detector,
   `detectors/__init__.py`, `scanner.py`, `risk.py`.
4. **Identity/output:** `canonicalizer.py`, `fingerprint.py`, `baseline.py`,
   `compare.py`, `reporter.py`.
5. **Research:** `evaluation/evaluator.py`, then loader, metrics, uncertainty,
   ablation, research and comparison as one subsystem.

Do not advance tiers until you can state inputs, outputs, invariants, callers and
tests for the current tier.

### Top 20 symbols — “I can explain…”

- `strict_json_loads`: duplicate/non-finite rejection.
- `validate_structure`: depth/node/string budgets.
- `load_tools`: accepted catalog shapes and count limit.
- `normalize_tool`: alias/NFC/unknown-field behavior.
- `all_text_fields`: deterministic nested traversal.
- `bounded_context`: local linguistic scope.
- `BUILTIN_DETECTORS`: seven-family execution identity.
- `Finding`: stable detector evidence model.
- `decode_representations`: strict, depth-one bounded decoding.
- `analyze_tools`: detection-to-retention orchestration.
- `_retain_findings`: deterministic presentation reservoir.
- `calculate_risk`: dedup, confidence, caps and synergy.
- `load_rule_pack`: data-only custom policy.
- `is_suppressed`: exact scope filtering.
- `canonical_json`: semantic serialization.
- `fingerprint_tool`: tool/component identity.
- `compare_baseline`: drift/rename inference.
- `render_terminal`/`serialize`: inert output.
- `evaluate_corpus`: experiment orchestration.
- `load_evaluation_artifact`: historical validation/compatibility.

## 12. Break-it exercises — predict before reading answers

All snippets are **TRAINING ONLY — NOT RESEARCH DATA**. Do not add them to frozen
corpora. For each, predict the enforcing module, result and security reason.

1. Give strict JSON two `description` keys.
2. Put `NaN` in an annotation.
3. Nest schema objects beyond the maximum depth.
4. Supply both `inputSchema` and a conflicting accepted alias.
5. Repeat the same normalized tool name twice.
6. Put “ignore previous instructions” in a nested vendor metadata value.
7. Put “do not ignore previous instructions” in a benign explanatory sentence.
8. Encode a suspicious instruction once as Base64.
9. Encode Base64 inside Base64 and expect recursive decoding.
10. Supply more than four valid decoded candidates in one field.
11. Give a custom rule a built-in rule ID.
12. Give a custom rule a regular-expression-looking pattern.
13. Suppress one rule for one tool and scan another tool with the same rule.
14. Change only object-key order, then fingerprint.
15. Reorder an array inside a schema, then fingerprint.
16. Change only a tool description after baseline creation.
17. Put `=HYPERLINK(...)` in attacker evidence and export CSV.
18. Request retrieval from a public IP or via a redirect from loopback.
19. Compare a valid 3.0.0 historical artifact with current 3.1.0 support.
20. Exhaust the global finding retention budget before a later suspicious tool.

## 13. Find-it-in-the-repository drills

Use `rg -n`, open the source, then write the answer before consulting section 25.

1. Where is the 10 MiB document limit? Hint: `MAX_*BYTES`.
2. Where are duplicate keys rejected? Hint: `object_pairs_hook`.
3. Which function resolves schema aliases? Hint: normalizer.
4. Where is Unicode NFC applied? Hint: `_normalize`.
5. Which list fixes built-in detector order? Hint: package `__init__`.
6. Where are all 16 explanations registered? Hint: `RULE_EXPLANATIONS`.
7. Which helper creates typed findings? Hint: detector base.
8. Where is sentence-local context bounded? Hint: context helper.
9. Where are depth-one decoders registered? Hint: representations.
10. Where is OBF-005's semantic gate? Hint: obfuscation detector.
11. Where are custom rule ID collisions rejected? Hint: loader validation.
12. Where is exact suppression scope applied? Hint: scanner.
13. Where are finding caps enforced? Hint: `_retain_findings`.
14. Where is category synergy added to risk? Hint: risk module.
15. Which function creates canonical JSON? Hint: canonicalizer.
16. Where is baseline rename inference restricted? Hint: compare.
17. Which helpers neutralize terminal/CSV output? Hint: reporter.
18. Where are redirects/environment proxies disabled? Hint: retrieval.
19. Where does evaluation turn severities into a binary prediction? Hint: evaluator.
20. Where is F1 calculated? Hint: metrics.
21. Where is Wilson 95% implemented? Hint: uncertainty.
22. Where are seven family ablations resolved? Hint: ablation.
23. Where is configuration identity hashed? Hint: research.
24. Where are schema 3.0.0 and 3.1.0 accepted? Hint: comparison/models.
25. Which files own authoritative H0 and v0.3 results? Hint: `evaluation/runs`.

## 14. Debugging routes

| Symptom | Inspect/run | Do not change blindly |
|---|---|---|
| Detector does not trigger | trace field traversal → local context → detector condition; run focused detector test | Broaden regex/keywords or severity. |
| Unexpected false positive | inspect evidence path, sentence scope, hard-negative test | Add global suppression or weaken rule. |
| Risk category unexpected | list finding IDs/scores/confidence/categories; inspect `risk.py` | Equate highest severity with aggregate risk. |
| Fingerprint changed | compare canonical component JSON and array order/NFC | Edit baseline or expected hash first. |
| Corpus hash changed | verify commit, file bytes/newlines and corpus-hash procedure | Normalize frozen files or update recorded hash. |
| Experiment comparison rejected | validate schema, corpus/config/rule-set identities and sample IDs | Force comparison of non-equivalent runs. |
| Historical artifact will not load | inspect artifact schema and self-consistency error; run focused compatibility test | Rewrite the artifact as current schema. |
| Custom rule rejected | inspect allowed fields, caps, unique ID and literal pattern | Add executable regex support. |
| Suppression does not work | verify known exact ID, exact tool scope and normalized name | Make it global without documented justification. |
| Output truncated | inspect `FindingBudgetStatus`, tool/report/evidence caps | Raise all limits or interpret retained list as full detection. |

For general suite/mypy/build failures: reproduce with the narrowest command, read
the first causal error, inspect configuration and environment, then run the full
documented gate. Never delete tests, weaken types/resource bounds, regenerate
frozen evidence or tune a detector just to make a check green.

## 15. Safe-change design exercises

These are paper designs only; implementation requires supervisor/project approval.

1. Separate bounded decision summaries from retained finding details.
2. Add an overflow-specific `--fail-on` regression without changing detector rules.
3. Add risk invariance tests across presentation budgets.
4. Improve error wording for duplicate JSON keys without exposing hostile content.
5. Add a supported historical artifact fixture while preserving its original rule identity.
6. Add a report-level privacy mode that does not alter scan semantics.
7. Add a resource worst-case benchmark using generated test data, not research corpora.
8. Add baseline provenance fields with backward-compatible loading.
9. Add a new output renderer consuming only the common report model.
10. Add documentation for an existing limit and prove the source/test agree.

For every proposal specify: threat, invariant, modules, typed-model/schema effect,
version/configuration identity effect, regression tests, compatibility, and why no
frozen evidence needs rewriting.

## 16. Code-reading viva questions

### Straightforward (1–10)

1. What is the scan entry point and which function performs orchestration?
2. Why are parsing, validation and normalization separate?
3. Where is the built-in detector set frozen in code?
4. What is the difference between a finding severity and aggregate risk?
5. Why does canonical JSON sort object keys but preserve array order?
6. What does a suppression match?
7. Why are custom patterns literal rather than user regex?
8. What makes decoding inert?
9. What does a baseline store and deliberately omit?
10. Which output formats share the same report model?

### Intermediate (11–20)

11. Trace PI-002 from text traversal to a typed finding.
12. Explain how local context reduces cross-sentence false matches.
13. Explain the relationship among OBF-005, decoding budgets and semantic gates.
14. Why can an invalid schema finding be a security-quality warning rather than proof of attack?
15. How does conservative rename inference avoid overclaiming identity?
16. What happens when evidence characters exceed the per-tool budget?
17. How are threshold predictions calculated in evaluation?
18. Why do configuration hashes include resolved rule identities?
19. Why is loopback retrieval still a trust boundary?
20. Why is FPR 25% equivalent to 6/24 in H0?

### Difficult (21–30)

21. Demonstrate the finding-budget decision-coupling defect without running H0.
22. Design a bounded detection-state summary that preserves risk and fail-on semantics.
23. Which schema/version identities could change when that P0 is fixed, and why?
24. Why can two byte-distinct files have the same semantic corpus identity—or not?
25. Explain how `core.autocrlf` can break exact research preservation.
26. Why is v0.3's higher recall not confirmatory evidence?
27. What prevents current code from silently reinterpreting a 3.0.0 artifact?
28. Explain how one benign vocabulary collision can affect precision and FPR differently.
29. Which claims survive if the corpus is synthetic, English-only and balanced 50/50?
30. If a future untouched run is poor, what may and may not be changed afterward?

## 17. Whiteboard drills

1. Draw raw bytes → report, naming every trust boundary.
2. Draw current versus desired finding-budget architecture.
3. Draw a seven-detector registry feeding suppression, decision and presentation.
4. Draw how canonical tool components combine into full/component fingerprints.
5. Draw baseline old/new states and conservative rename inference.
6. Draw expected/predicted labels as a 2×2 confusion matrix and place 5/18/6/19.
7. Draw corpus identity + config identity + code identity → experiment identity.
8. Draw confirmatory v0.2 branching to post-unblinding v0.3 exploratory work.
9. Draw loopback retrieval controls around a hostile local MCP server.
10. Draw artifact 3.0.0 and 3.1.0 entering one validation/comparison boundary.

## 18. Critical invariants register

| Invariant | Enforced by | Test owner | Why / consequence if broken |
|---|---|---|---|
| Scanned tools are never invoked | static pipeline; retrieval only `tools/list` | CLI/retrieval tests | Execution would cross the project’s central safety boundary. |
| Metadata-linked resources are not fetched | loader/detectors do no URL dereference | boundary tests/review | Attacker-controlled network access/SSRF. |
| JSON ambiguity is rejected | `strict_json_loads` | strict JSON tests | Hidden duplicate/non-finite semantics. |
| Security-significant content is not silently discarded on input | resource policy rejects overflow/conflicts | policy/normalizer tests | False clean result from truncated input. |
| Traversal/order is deterministic | sorted fields/registries/retention | detector/scanner tests | Unstable findings, hashes or artifacts. |
| Built-in IDs are stable and unique | registry/explanation/custom collision checks | rule/research tests | Evidence cannot identify detector behavior. |
| Custom configuration is data-only | typed loader + literal containment | custom-rule tests | Configuration becomes code execution/ReDoS surface. |
| Decoding is depth-one, bounded, strict, inert | representation budgets/validators | representation tests | Expansion attack or unintended execution. |
| Risk stays deterministic and capped | `calculate_risk` | risk tests | Order/duplicates manipulate classification. |
| Presentation escaping is inert | reporter helpers | reporter tests | Terminal/spreadsheet injection. |
| Canonical hashes are stable for equivalent objects | canonicalizer | fingerprint tests | Baseline/corpus/config identity drift. |
| Retrieval stays opt-in and loopback-only | URL/address checks and transport policy | retrieval tests | Remote scanning and SSRF. |
| Historical artifacts keep their own rule identity | compatibility loader/models | historical tests | Retrospective rewriting of results. |
| Primary results are not tuned after unblinding | research protocol/artifact preservation | integrity docs/checks | Invalid confirmatory claim. |
| Future decisions must not depend on report retention | **not yet enforced; P0 design gate** | future overflow invariance tests | Findings disappear semantically under output pressure. |

## 19. Version and evidence chronology

1. **v0.2 frozen pilot:** detector/configuration and independently reviewed
   holdout were frozen before H0.
2. **H0 primary evaluation:** produced 5 TP, 18 TN, 6 FP, 19 FN. This remains
   authoritative first confirmatory evidence within the pilot.
3. **Failure analysis:** the exposed results revealed missed paraphrases,
   contextual patterns, representations and mismatch cases.
4. **v0.3 exploratory design/implementation:** PI-002, HID-002, SEC-002, MIS-002
   and OBF-005 were added after unblinding.
5. **Exploratory rerun:** produced 11/18/6/13 on the same exposed holdout; it
   generated hypotheses, not fresh confirmation.
6. **Hardening/release:** security, compatibility, packaging and research-status
   work produced package `0.3.0a1`, rule pack `2.0.0`, artifact schema `3.1.0`.
7. **Historical tag:** `v0.3.0a1` remains at
   `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`.
8. **Day 6 preservation:** later documentation commits preserve maps, handover,
   recovery and FYP plans. Current HEAD is later than, and must not be confused
   with, the release tag.

## 20. Examiner traps and corrections

| Trap / weak answer | Strong correction grounded in this repository |
|---|---|
| “It detects malicious MCP servers.” | It statically flags predefined suspicious/security-quality constructs in tool definitions; it does not prove intent or inspect runtime behavior. |
| “MCP metadata is executable.” | Metadata influences an agent’s choices and prompts, so it is a trust boundary; this scanner treats it as inert data. |
| “Every malformed schema is tool poisoning.” | SCH findings can be security-quality warnings; malformed does not prove maliciousness. |
| “The hash proves the corpus is safe.” | A matching hash proves identity against a trusted expected value, not safety/authorship. |
| “Finding severity equals risk.” | Findings have local severity; `risk.py` aggregates capped/deduplicated evidence into tool risk. |
| “MEDIUM is the risk threshold.” | Evaluation uses finding-severity threshold; aggregate risk is a separate output. |
| “No finding means no attack.” | It means no supported rule produced retained evidence; bypasses and P0 overflow are limitations. |
| “Regex is more intelligent than literal matching.” | Custom rules deliberately use bounded literal data; built-ins use reviewed deterministic logic. |
| “Base64 decoding handles all obfuscation.” | Only strict, printable, bounded depth-one representations are supported. |
| “Redaction makes reports anonymous.” | It reduces selected evidence exposure; names/structure/provenance may remain privacy-relevant. |
| “Loopback means trusted.” | A local service is still hostile; transport constraints only reduce SSRF scope. |
| “25% FPR means 25% of alerts are false.” | FPR is FP/all benign = 6/24; false discovery share is 6/11 and relates to precision. |
| “47.92% accuracy means the project failed.” | It is an honest pilot effectiveness result plus an engineering/reproducibility contribution. |
| “v0.3 doubled recall, so it generalizes.” | v0.3 was designed after viewing H0 and rerun on exposed data; fresh untouched confirmation is required. |
| “Ablation proves family X causes detection.” | It measures contribution on this corpus/configuration only. |
| “κ≈0.9583 validates detector accuracy.” | Kappa describes reviewer/label agreement, not detector validity or generalization. |
| “Synthetic balanced data models deployment.” | It controls a pilot evaluation; prevalence, language and realism limit deployment claims. |
| “The tag should move to latest docs.” | Release tags are immutable historical identities; later documentation belongs to later commits. |
| “We can fix a hash mismatch by saving the file.” | Investigate commit, exact bytes and newline conversion; never rewrite frozen evidence automatically. |
| “Output caps only affect display.” | Currently they also affect risk/fail-on/affected/evaluation semantics; that is the documented P0. |

## 21. Self-assessment checkpoints

Mark an item only after explaining it aloud and locating its owner without this
manual.

### MCP and security (1–10)

- [ ] I can distinguish MCP host, client, server and discovered tool.
- [ ] I can explain why descriptions/schemas/annotations are a trust boundary.
- [ ] I can distinguish prompt injection, tool poisoning and capability mismatch.
- [ ] I can explain why suspicious does not prove malicious intent.
- [ ] I can state the project’s static-analysis and non-invocation boundary.
- [ ] I can draw the loopback retrieval trust boundary.
- [ ] I can explain concealment, sensitive-data and obfuscation signals.
- [ ] I can explain malformed schema as a security-quality warning.
- [ ] I can name important bypass/false-positive classes.
- [ ] I can describe baseline/suppression trust risks.

### Input and analysis implementation (11–22)

- [ ] I can trace CLI → loader → normalizer → scanner → reporter.
- [ ] I can explain duplicate-key and non-finite rejection.
- [ ] I can locate depth/node/string/tool limits.
- [ ] I can explain NFC and alias-conflict handling.
- [ ] I can distinguish key/value and poisoning field traversals.
- [ ] I can name all seven families and 16 rule IDs.
- [ ] I can trace PI-002, HID-002, SEC-002, MIS-002 and OBF-005.
- [ ] I can explain local context/negation scope.
- [ ] I can explain strict depth-one decoding and every major bound.
- [ ] I can explain literal custom rules and exact suppressions.
- [ ] I can calculate aggregate risk from a simple set of findings.
- [ ] I can demonstrate the finding-budget P0 on paper.

### Identity, drift and output (23–31)

- [ ] I can explain canonical JSON and array-order sensitivity.
- [ ] I can distinguish file/tool/component/corpus/configuration hashes.
- [ ] I can predict which metadata change changes a fingerprint.
- [ ] I can trace baseline creation and comparison.
- [ ] I can explain conservative rename inference.
- [ ] I can explain terminal escaping and CSV formula neutralization.
- [ ] I can explain redaction and truncation limitations.
- [ ] I can locate reporter format dispatch.
- [ ] I can explain why hashes need trusted expected provenance.

### Evaluation and statistics (32–42)

- [ ] I can trace manifest → prediction → confusion matrix → artifact.
- [ ] I can calculate H0 accuracy, precision, recall, F1 and FPR manually.
- [ ] I can distinguish FPR from false-discovery proportion.
- [ ] I can explain Wilson intervals intuitively.
- [ ] I can explain why N=48 and tiny strata limit certainty.
- [ ] I can distinguish analysis-core from static-end-to-end timing.
- [ ] I can explain warm-ups, repetitions, median and p95.
- [ ] I can explain all seven ablations without making causal claims.
- [ ] I can explain configuration and experiment identities.
- [ ] I can explain schema 3.0.0/3.1.0 compatibility.
- [ ] I can locate and authenticate both primary historical artifacts.

### Research ownership (43–52)

- [ ] I can state v0.2 H0 counts and metrics accurately.
- [ ] I can state v0.3 exploratory counts and metrics accurately.
- [ ] I can explain why H0 remains confirmatory within the pilot.
- [ ] I can explain why v0.3 cannot confirm generalization.
- [ ] I can distinguish development, holdout and exploratory work.
- [ ] I can state the principal corpus limitations.
- [ ] I can explain reviewer blinding, disagreement and kappa limits.
- [ ] I can explain why a new untouched holdout needs preregistration.
- [ ] I can respond honestly to a poor future primary result.
- [ ] I can state what must remain frozen after unblinding.

## 22. Seven-day ownership overlay (30–45 minutes/day)

| Day | Read/trace | Produce evidence of ownership |
|---|---|---|
| 1 | CLI, loader, resource policy, normalizer | Draw pipeline; answer drills 1–5. |
| 2 | detector base, registry, PI-002/HID-002/SEC-002 | Explain local context; predict exercises 6–7. |
| 3 | MIS-002, representations, OBF-005, risk/scanner | Draw decoding bounds and P0 current/desired flows. |
| 4 | custom rules, suppressions, reporter, retrieval | Explain data-only and output/SSRF boundaries. |
| 5 | canonicalization, fingerprint, baseline, compare | Predict exercises 14–16; draw component hashes. |
| 6 | evaluation loader/evaluator/metrics/uncertainty/ablation | Recalculate H0; answer viva 17–20. |
| 7 | frozen artifacts, compatibility, research docs | Defend v0.2/v0.3 distinction in a 10-minute mock viva. |

## 23. Break-it answer key

1. **Duplicate key:** `resource_policy.strict_json_loads`; reject the document.
   Accepting it creates parser-dependent, last-key-wins ambiguity.
2. **NaN:** strict JSON constant handler/canonicalizer; reject non-finite input.
   JSON identities must be portable and deterministic.
3. **Excess depth:** `validate_structure`; reject once the depth bound is crossed,
   preventing unbounded recursive work rather than silently truncating content.
4. **Conflicting alias:** `normalizer.normalize_tool`; reject instead of choosing
   one schema and discarding security-significant content.
5. **Duplicate normalized name:** `normalize_tools`; reject because findings,
   suppressions and baselines depend on unambiguous identity.
6. **Nested injection value:** `poisoning_text_fields` and injection detector;
   nested values are deliberately traversed and may produce PI evidence.
7. **Benign negation/reference:** `bounded_context`, local patterns and educational
   reference checks should prevent a naive phrase hit; inspect hard negatives.
8. **One Base64 layer:** `decode_representations` may emit a bounded candidate;
   OBF-005 still requires suspicious decoded semantics.
9. **Nested Base64:** no recursive decode. Depth-one is an intentional expansion
   and predictability boundary, so the second layer remains uninterpreted.
10. **Candidate overflow:** representations retain no more than four candidates
    per field and record truncation/bounded state deterministically.
11. **Built-in collision:** `validate_custom_rule_ids` rejects it; otherwise
    artifacts cannot identify which behavior the ID represented.
12. **Regex-looking custom pattern:** it remains literal text, not executable
    regex. The loader enforces allowed fields/length/counts.
13. **Tool-scoped suppression:** `scanner.is_suppressed` removes only the exact
    rule/tool match; the other tool’s finding remains.
14. **Object-key reorder:** `canonical_json` sorts keys, so the semantic
    fingerprint remains equal.
15. **Array reorder:** array order is preserved, so the fingerprint changes; the
    project does not assume arbitrary arrays are sets.
16. **Description change:** full and description component fingerprints change;
    `compare_baseline` reports component drift, not malicious intent.
17. **CSV formula:** reporter neutralization prefixes dangerous cell content so a
    spreadsheet treats it as data. JSON/SARIF remain escaped structured strings.
18. **Public/redirect target:** retrieval rejects non-loopback targets and does
    not follow redirects or environment proxies.
19. **Historical 3.0.0:** compatibility loader validates it using its supported
    historical schema/rule context; it is not rewritten as 3.1.0.
20. **Global retention exhaustion:** current `scanner`/CLI/evaluator can make a
    later detected tool appear risk-zero/clean/benign. This is the P0; future
    decision summaries must be independent from retained details.

## 24. Repository-drill answer key

1. `src/mcpsec/resource_policy.py`, document byte constants.
2. `resource_policy.strict_json_loads`, duplicate-aware pairs hook.
3. `src/mcpsec/normalizer.py::normalize_tool` and alias helpers.
4. `normalizer._normalize` (and canonicalization normalization).
5. `src/mcpsec/detectors/__init__.py::BUILTIN_DETECTORS`.
6. `src/mcpsec/rules/builtin.py::RULE_EXPLANATIONS`.
7. `src/mcpsec/detectors/base.py::finding`.
8. `detectors/base.py::bounded_context` and `has_local_pattern`.
9. `src/mcpsec/representations.py::decode_representations` and decoder helpers.
10. `src/mcpsec/detectors/obfuscation.py::ObfuscationDetector.detect`.
11. `src/mcpsec/rules/loader.py::validate_custom_rule_ids`.
12. `src/mcpsec/scanner.py::is_suppressed`.
13. `scanner.py::_retain_findings` and resource-policy constants.
14. `src/mcpsec/risk.py::calculate_risk`.
15. `src/mcpsec/canonicalizer.py::canonical_json`.
16. `src/mcpsec/compare.py::compare_baseline`.
17. `src/mcpsec/reporter.py`, terminal-safe and spreadsheet-safe helpers.
18. `src/mcpsec/retrieval.py`, client construction/response/address checks.
19. `src/mcpsec/evaluation/evaluator.py::_analyze_sample`/threshold logic.
20. `src/mcpsec/evaluation/metrics.py::calculate_metrics`.
21. `src/mcpsec/evaluation/uncertainty.py::wilson_interval`.
22. `src/mcpsec/evaluation/ablation.py::resolve_ablation`.
23. `src/mcpsec/evaluation/research.py::configuration_sha256`.
24. `src/mcpsec/evaluation/comparison.py` plus evaluation models/constants.
25. H0 and Day 4C paths in Trace Missions 24–25.

## 25. Code-reading viva model answer points

1. `cli.scan` parses/coordinates; `cli.analyze` resolves policy;
   `scanner.analyze_file/analyze_tools` owns analysis.
2. Parsing establishes syntax, validation establishes safe/bounded shape, and
   normalization resolves aliases/NFC into the typed detector contract.
3. `detectors/__init__.py::BUILTIN_DETECTORS`; configuration records the resolved
   family/rule identity for research reproducibility.
4. Severity belongs to one finding; risk combines deduplicated weighted evidence,
   confidence, category caps and synergy into a capped tool score/band.
5. JSON objects are unordered mappings, while array order can be semantically
   significant. Sorting both would invent equivalence.
6. A validated suppression matches exact known rule ID and optional exact tool
   name; it is not sentence-local semantic negation.
7. Literal patterns keep configuration data-only, bounded and resistant to user
   regex execution/ReDoS; sophisticated logic belongs in reviewed built-ins.
8. Decoders operate on strings only, accept strict supported forms, never recurse,
   execute, import, dereference or access the network, and enforce hard budgets.
9. Baseline stores tool/component fingerprints and minimal summaries; it avoids
   raw descriptions/values. It supports comparison, not authenticity.
10. Terminal, JSON, CSV and SARIF all consume `ScanReport`; renderer-specific
    escaping must not change decisions.
11. PI-002 traverses poisoning text values, searches bounded/local instruction
    priority semantics and creates a typed finding; tests include suspicious and
    benign/context counterexamples.
12. `bounded_context` limits related patterns to local sentence/span context,
    reducing matches assembled from unrelated text or negation elsewhere.
13. OBF-005 is not “decoded text exists.” The bounded decoder yields candidates;
    the obfuscation detector requires suspicious decoded semantics before finding.
14. Schema invalidity can weaken interoperability/security assurance without
    demonstrating attacker intent; label it a warning/finding, not proof.
15. Rename inference requires one removed and one added tool with matching
    component signature, avoiding many-to-many guesses.
16. Retention truncates evidence/details deterministically and records budget
    status. Today that retained subset also wrongly influences decisions.
17. Evaluation predicts suspicious if an applicable retained finding meets the
    configured severity threshold; aggregate risk is not the threshold.
18. Resolved identities distinguish configurations that use the same headline
    threshold but different actual detector behavior.
19. Local servers can be malicious. Address pinning, no redirect/proxy and bounds
    reduce SSRF/resource risk but do not make response content trusted.
20. There were 24 benign labels and 6 false positives: `6/(18+6)=25%`.
21. Generate bounded synthetic tools or mocked detector findings that exceed
    retention before a later high-severity fact; compare detected counts with
    risk, affected count, fail-on and evaluator prediction. Never use H0.
22. Store compact per-tool/per-category/rule decision facts or incremental risk
    accumulators independent of detailed evidence; separately retain deterministic
    finding details under output budgets.
23. Likely minor behavior release plus artifact-schema/config identity change;
    rule pack changes only if rule behavior changes. Maintain old artifact loading
    and explicitly distinguish old/new decision semantics.
24. Semantic canonical hashing can ignore object-key order; byte hashing cannot.
    Corpus infrastructure defines exactly which representation is authoritative.
25. Checkout conversion changes LF bytes to CRLF, breaking file SHA even when the
    visible text is equivalent; clone with `core.autocrlf=false` for exact recovery.
26. The old holdout and its errors were visible before rule design. Reusing it can
    measure exploratory fit but cannot estimate untouched generalization.
27. Artifact loader validates supported schema plus self-described rule/config
    identity and internal counts rather than applying only current defaults.
28. One benign collision adds FP: precision denominator predicted positives grows,
    and FPR numerator among benign grows; exact effect depends on existing counts.
29. Claims about deterministic engineering, measured pilot behavior and identified
    construct coverage survive; deployment prevalence, multilingual/real-world and
    broad generalization claims do not.
30. Preserve raw artifact and preregistered analysis first. Later tuning is allowed
   only as clearly post-unblinding exploratory work, never as a replacement result.

## 26. Construct-to-code research traceability

These are implemented operational signals, not individually validated universal
constructs.

| Construct/signal | Rule family / implementation | Representative test | Pilot metric/evidence | Limitation |
|---|---|---|---|---|
| Instruction override/priority | PI-001/002; `detectors/injection.py` | priority construct + benign/scoped-negation tests | contributes to binary H0/Day 4C predictions and injection ablation | lexical/contextual paraphrases, language and relocation can bypass. |
| Concealment/withholding | HID-001/002; `secrecy.py` | material withholding and UI/negation negatives | concealment-family ablation | legitimate privacy/quiet behavior can collide. |
| Sensitive-value instructions | SEC-001/002; `sensitive_data.py` | action and credential-manager hard negatives | six aggregate historical FPs remained in v0.3 | legitimate security tooling uses the same vocabulary. |
| Schema security quality | SCH-001/002; `schema.py` | malformed/output schema and privileged parameter tests | schema-family outcomes/ablation | invalid/privileged does not prove poisoning. |
| Purpose/capability mismatch | MIS-001/002; `mismatch.py` | corroborated/aligned/cross-field tests | exposed exploratory recoveries and mismatch ablation | stated metadata cannot prove runtime behavior. |
| Obfuscation/representation | OBF-001…005; `obfuscation.py`, `representations.py` | bounds, depth-one, safe decode tests | exposed exploratory OBF-005 observations/ablation | unsupported encodings and semantic bypass remain. |
| High-impact capability | CAP-001; `permissions.py` | structured categories and non-operative negatives | capability ablation/diagnostic findings | powerful capability can be legitimate administration. |
| Integrity drift | canonicalizer/fingerprint/baseline/compare | key-order, component drift, rename ambiguity tests | engineering feature, not H0 poisoning metric | trusted baseline and TOCTOU remain external assumptions. |

## 27. Exact top-15 file ownership

| Tier | File | Why the captain must know it |
|---|---|---|
| 1 | `src/mcpsec/cli.py` | Command orchestration, exits, formats and explicit retrieval/evaluation entry points. |
| 1 | `src/mcpsec/resource_policy.py` | Central hostile-input and resource-boundary constants/helpers. |
| 1 | `src/mcpsec/loader.py` | Accepted static catalog shapes and bounded acquisition. |
| 1 | `src/mcpsec/normalizer.py` | Raw-to-typed security contract, aliases and NFC. |
| 1 | `src/mcpsec/detectors/base.py` | Shared traversal, context and finding construction semantics. |
| 1 | `src/mcpsec/detectors/__init__.py` | Production detector registry and order. |
| 1 | `src/mcpsec/scanner.py` | Detector/suppression/retention/risk orchestration and P0 coupling. |
| 1 | `src/mcpsec/risk.py` | Aggregate risk semantics distinct from finding severity. |
| 2 | `src/mcpsec/representations.py` | Bounded depth-one decoding security design. |
| 2 | `src/mcpsec/reporter.py` | Common report conversion and output injection defenses. |
| 2 | `src/mcpsec/canonicalizer.py` | Stable semantic serialization underpinning identity. |
| 2 | `src/mcpsec/fingerprint.py` | Full/component SHA-256 definitions. |
| 2 | `src/mcpsec/compare.py` | Drift and conservative rename semantics. |
| 2 | `src/mcpsec/evaluation/evaluator.py` | Prediction, timing, strata and artifact assembly pipeline. |
| 3 | `src/mcpsec/evaluation/comparison.py` | Historical schema validation and experiment comparison. |

The remaining detector files, evaluation metrics/research/uncertainty/ablation,
custom-rule/suppression loaders, retrieval, models and tests are **know where to
find** dependencies of these fifteen—not unimportant code.

## 28. High-value named tests

- Hostile bounds: `test_structure_node_count_is_bounded`,
  `test_size_limit`, `test_static_tool_count_is_bounded`.
- Ambiguous values: strict JSON duplicate-key tests and
  `test_canonicalizer::test_non_finite_rejected`.
- Context: `test_bounded_context_stays_in_sentence`,
  `test_instruction_negation_is_scoped_to_its_sentence`, and mismatch disclaimer/
  coordinated-negation tests.
- Decoding: `test_exact_supported_representations_decode_once`, all explicit
  candidate/output/retained bounds, and `test_depth_is_exactly_one`.
- Identity/drift: `test_key_order_is_deterministic`,
  `test_description_change_is_component_scoped`, `test_rename_inference`, and
  three ambiguity tests.
- Reporting: `test_formula_injection_neutralized`,
  `test_terminal_untrusted_text_is_literal_ascii`, and
  `test_finding_budget_status_is_visible_in_every_report_format`.
- Evaluation: `test_confusion_counts_every_quadrant`,
  `test_zero_division_is_safe`, `test_timing_statistics_requires_complete_repetitions`,
  and `test_wilson_intervals_include_counts_and_handle_zero_denominators`.
- History: `test_real_historical_h0_loads_and_compares_to_day4c` and
  `test_corrupted_real_historical_h0_is_rejected`.

## 29. Ownership conclusions and open engineering observation

No contradiction was found between the inspected source and the frozen H0/v0.3
status documents used for this walkthrough. The important implementation
observation remains the already documented P0: output retention is materially
coupled to risk, affected counts, fail-on and evaluator predictions. The current
tests make truncation visible but do not enforce decision invariance. That issue
belongs in future approved engineering work before another confirmatory freeze;
it was not repaired here.

The walkthrough also makes two boundaries easy to miss: suppressions have exact
rule/tool scope rather than sentence semantics, and “static by default” coexists
with a separate, explicit, constrained loopback `tools/list` retrieval path.
