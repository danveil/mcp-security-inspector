# Day 4A Exploratory Improvement Design

Scientific status: **POST-UNBLINDING EXPLORATORY DESIGN — NOT IMPLEMENTED OR VALIDATED.**

## Workspace verification

| Check | Result |
|---|---|
| Repository | `C:\Users\afiq hakiki\Documents\csprojects\mcp-tool-security-inspector` |
| Git HEAD | `a4abee4661522ac13edb37e1b075186a2ccd7a03` |
| Expected HEAD | Exact match |
| Tracked worktree at entry | Clean |
| Day 4A output | Ignored `evaluation/runs/day4a/` only |

## Day 3 evidence verification

| Evidence | Expected SHA-256 | Verified result |
|---|---|---|
| Authoritative H0 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` | Exact match |
| Day 3C failure analysis | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` | Exact match |

H0 remains TP 5, TN 18, FP 6, and FN 19 at the `MEDIUM` threshold. No prediction-producing command was run during Day 4A. The Day 3D evidence pack was used only as a secondary synthesis source.

## Root-cause priorities

### Primary design answer

The smallest defensible deterministic v0.3 improvement set is:

1. **Local context and negation logic for sensitive-data matching**, plus a new action-linked sensitive-value rule.
2. **Construct-derived phrase grammars for instruction priority and concealment**, each under a new stable rule ID.
3. **One bounded representation recognizer inside the existing obfuscation family**, limited to four explicit encodings and depth one.
4. **One shared structured capability extractor used by the existing capability and mismatch detectors**, plus one corroborated purpose/capability contradiction rule.

This set addresses four distinct observations rather than optimizing a single score: six primary paraphrase/concealment FNs, four primary obfuscation FNs, five primary capability/cross-field FNs plus two below-threshold capability cases, and four SEC false positives. Counts overlap across multi-label mechanisms and must not be added as projected recovered samples. Actual benefit is unknown until implementation and separate exploratory evaluation.

The set stays within the FYP premise: fixed grammars, bounded transformations, transparent paths/evidence, no model calls, no embeddings, no execution, and asymptotically linear scanning over already-normalized metadata.

### Why threshold reduction is not P0

Seventeen of nineteen H0 false negatives had no finding and risk 0. Only `holdout_s023` and `holdout_s024` had informational findings below `MEDIUM`. Lowering the threshold could affect at most that observed minority while increasing exposure to informational capability noise. It cannot recover a sample for which no detector emits a finding. The P0 design therefore improves signal generation and context before any future threshold study. The production default remains `MEDIUM`.

### P0 candidate overview

| Candidate | Frozen target evidence | Current mechanical limitation | Exploratory benefit | Primary risk | Complexity / runtime |
|---|---|---|---|---|---|
| Cross-field purpose/capability consistency | s012, s015, s016, s021–s024; capability, cross-field, and threshold mechanisms | `MIS-001` compares purpose only with input schema; `CAP-001` concatenates fields, loses paths, uses a narrow grammar, and stays informational | Recover corroborated contradictions across description, schemas, annotations, metadata, execution, and vendor fields | Legitimate admin, orchestration, simulation, and documentation tools | High / one additional fixed-grammar field pass |
| Bounded encoding recognition | s017–s020; four primary obfuscation-decoding FNs | `OBF-004` checks only root-description Base64 blocks of at least 80 characters and does not inspect decoded text | Recognize four explicit representation families and expose risky decoded text as inert evidence | Benign encoded examples, identifiers, hashes, binary garbage | Medium-high / tightly capped decoding |
| Injection/concealment paraphrase coverage | s001–s006; six primary FNs | `PI-001` and `HID-001` require narrow literal phrases despite correct traversal | Cover reusable authority/conflict and visibility/omission constructs | Policy prose, UI behavior, privacy, accessibility, educational text | Medium / fixed regular-expression grammars |
| Credential context and negation | Four `SEC-001` FPs; vocabulary misses including recovery/output and credential-access language | First keyword wins; context is a short tool-name/description allow-list; local negation, value actions, and field importance are absent | Reduce context-free FPs while retaining or strengthening actual value handling | Over-suppression of genuine credential requests | Medium / bounded sentence/window checks |

## Proposed v0.3 architecture

### Existing real flow

`loader` → `normalizer` → `ToolDefinition` → ordered `BUILTIN_DETECTORS` → suppressions → capped risk → inert report.

The evaluator invokes the same `analyze_tools` path. Binary evaluation is based on whether any finding severity meets the configured threshold; risk score is reported but is not the binary classifier. This makes finding gates and severities—not a blanket risk adjustment—the correct P0 control points.

### Minimal v0.3 extension

```text
normalized ToolDefinition (unchanged)
        |
        +-- existing field-addressable traversal
        |       +-- local context windows -> PI/HID/SEC rules
        |       +-- bounded representation helper -> OBF-005
        |       +-- structured capability signals with paths
        |                    +-- CAP-001 triage (unchanged severity)
        |                    +-- MIS-002 corroborated contradiction
        |
        +-- existing Finding model and deterministic ordering
        +-- existing suppressions and risk engine
        +-- existing reporters/evaluator
```

No second scanner, detector interface, model, network path, or executable decoder is introduced. New helpers remain pure functions called by existing detector classes. The existing `Finding` schema is sufficient: decoded or cross-field evidence is serialized deterministically into the current `evidence` string, and paired paths are serialized into the current `field` string. This avoids changing experiment artifact schema 3.0.0 in P0.

### Required invariants

- Detectors consume normalized values and never mutate `ToolDefinition`.
- Every new traversal has stable field and candidate ordering.
- No metadata value is executed, fetched, imported, rendered as HTML, or passed to a model.
- Original and transformed evidence are bounded and terminal-safe.
- Resource limits cause explicit bounded behavior; security-significant content is not silently truncated.
- Existing scanners, custom literal rules, suppressions, fingerprints, baselines, and transport remain compatible.

### Explainability contract

Every new finding must retain the existing required fields: stable rule ID, detector family/category, field path, original evidence, explanation, recommendation, severity, confidence, and score contribution. A decoded finding additionally records encoding type and bounded decoded evidence inside the inert evidence string. A cross-field finding records both the declared-purpose path and capability path. Redaction must cover original and transformed evidence together. No new rule may emit only an opaque aggregate score or `field="multiple"` when exact contributing paths are known.

## P0 improvements

### Cross-field consistency

#### Current limitation and target

`MismatchDetector` extracts categories from name/title/description and only `input_schema`. It ignores output schema, annotations, `_meta`, execution data, and vendor/unknown fields for consistency. `PermissionsDetector` concatenates every field into one blob, returns `field="multiple"`, and recognizes only seven narrow verb phrases. It cannot show where a contradiction occurred or distinguish an aligned administrative purpose from an unrelated capability.

The P0 target is the seven Day 3C cases associated with capability, cross-field, and threshold mechanisms. This is a target set, not a promise to recover seven samples.

#### Capability representation

Introduce an internal immutable `CapabilitySignal` with:

- stable category;
- source field path;
- matched original evidence;
- local negation/safety state;
- destructive flag;
- confidence tier based on grammar specificity.

Use these stable categories:

| Category | Minimum deterministic concept |
|---|---|
| `filesystem_read` | read/open/list file or directory |
| `filesystem_write` | create/write/modify/overwrite file or directory |
| `file_delete` | delete/remove file, directory, folder, or path |
| `process_execution` | start/launch/run process, command, script, executable, or program |
| `outbound_network` | send/post/upload/request/connect to remote/network/API endpoint |
| `database_read` | query/read/select database, table, row, or record |
| `database_write` | insert/update/delete/modify database, table, row, or record |
| `credential_access` | read/access/collect/request credential, password, token, key, or authentication store |
| `secret_output` | return/echo/expose/transmit credential or secret value |
| `destructive_operation` | explicit destructive/reset/purge behavior not fully represented above |

The extractor must return each signal separately with its path; it must not concatenate text across fields. Fixed verb/object grammars may allow limited intervening words, inflection, and underscore/hyphen normalization. Results are sorted by `(field, category, evidence)`.

#### Declared-purpose representation

Do not treat every category word in a description as authorization. Extract two transparent purpose properties from name/title/description:

1. **Explicitly aligned high-impact purpose**, requiring a capability-specific purpose grammar such as a terminal/command runner, database administrator, credential manager, network client, or file editor.
2. **Narrow/low-impact purpose cues**, such as formatter, display, preview, summary, calculator, legend, title, read-only lookup, offline renderer, plan-only, or simulation.

The list must be small, reviewed, and backed by benign counterexamples. Absence of an aligned purpose is not sufficient by itself.

#### MIS-002 corroboration gate

Emit `MIS-002` only when all three layers hold:

1. A high-impact `CapabilitySignal` is present with a concrete field path.
2. No explicit aligned purpose authorizes that category.
3. At least one corroborator exists:
   - narrow/low-impact purpose plus a destructive or credential/secret capability;
   - an explicit `offline`/`local-only` purpose plus outbound network;
   - destructive capability plus wording that removes confirmation or consent;
   - two or more unrelated high-impact categories under a narrow purpose;
   - a hidden/withheld side-effect signal plus a high-impact capability.

Field-local negation or safety language such as “does not execute,” “simulation only,” or “produces a plan without applying it” cancels only the matching local capability. A disclaimer in one field must not globally suppress a contradictory positive declaration elsewhere.

The finding should contain both sides, for example:

- `field`: `description <-> execution.operations[1]`
- `evidence`: `purpose[description]=...; capability[execution.operations[1]]=process_execution; corroborator=narrow_purpose`

Provisional severity should be `MEDIUM` only after this gate and `HIGH` only for a separately tested destructive-plus-concealment combination. No uncorroborated capability becomes binary suspicious.

#### Impact assessment

- **Expected recall benefit:** addresses five primary capability/cross-field FNs and supplies a principled path for two threshold cases; actual recovery unknown.
- **FP risk:** high without corroboration, reduced to medium by aligned-purpose and local-negation gates.
- **Runtime:** one deterministic scan of existing text fields plus small-set comparisons; expected linear cost.
- **Explainability:** improves over `CAP-001` by preserving category and both field paths.
- **Files/families:** `permissions.py` supplies structured extraction; `mismatch.py` emits `MIS-002`; family remains `mismatch`.
- **Scope:** fully deterministic and rule-based.

#### Required tests

- Every capability category with path preservation in description, schemas, annotations, metadata, execution, and unknown fields.
- Same capability in aligned admin purpose remains clean under `MIS-002`.
- Dry-run, plan-only, simulation-only, and field-local negation cases remain clean.
- Contradictory disclaimers in one field do not suppress positive capabilities in another.
- One narrow purpose plus one destructive capability, two unrelated capabilities, offline-plus-network, and credential access unrelated to purpose trigger.
- Deterministic ordering under reordered mapping keys.
- Existing `CAP-001` fixtures retain informational severity and expected evidence semantics.

### Bounded encoding

#### Current limitation and target

`OBF-004` searches only `tool.description` for a valid Base64 token of at least 80 characters. It validates bytes but does not interpret text. It cannot recognize decimal character codes, HTML numeric entities, hexadecimal byte sequences, or shorter Base64 in nested fields. The target is the four primary obfuscation-decoding FNs without creating a general codec engine.

#### Explicit recognized forms

Only these forms are in P0:

1. Numeric HTML entities: contiguous `&#DD;` or `&#xHH;` sequences.
2. Hex bytes with explicit byte separators or prefixes (`AA BB`, `0xAA`, or `\xAA` forms); arbitrary hashes/UUIDs are excluded.
3. Decimal character codes with explicit separators and valid bounded code points.
4. Base64 with strict alphabet/padding validation and a lower minimum than `OBF-004`.

No URL decoding, compression, archives, ROT variants, arbitrary charset guessing, encryption, or recursive decoding.

#### Proposed hard limits

| Limit | P0 value | Rationale |
|---|---:|---|
| Maximum encoded candidate input | 512 characters | Bounds regex capture and decode allocation. |
| Minimum decoded text | 8 characters | Avoid tiny color/number fragments. |
| Maximum decoded candidate output | 512 Unicode characters | Bounds evidence and downstream matching. |
| Maximum candidates per field | 4 | Prevent one field from dominating work. |
| Maximum candidates per tool | 32 | Bounds total decode attempts. |
| Maximum retained decoded text per tool | 4,096 characters | Bounds downstream scans. |
| Decode depth | exactly 1 | Prevent nested recursion and decode chains. |
| Byte decoders | strict UTF-8 only | No arbitrary codec guessing. |
| Printable-text ratio | at least 90% | Reject binary garbage; allow ordinary whitespace only. |

Recognition remains linear and fail-closed: malformed data, invalid padding, invalid code points, NULs, disallowed controls, invalid UTF-8, excessive output, and low printable ratio are not passed to semantic matching. An over-limit recognized candidate produces one bounded informational review finding rather than being silently decoded or truncated.

#### OBF-005 gate

`OBF-005` should mean **bounded decoded high-risk text**, not merely “some bytes decoded.” Emit a `MEDIUM` finding only when:

1. the candidate matches one exact format;
2. decoding passes every bound;
3. decoded text contains a reusable instruction-priority, concealment, sensitive-value-action, or high-impact capability signal; and
4. surrounding original-field context is not an educational/example-only use without a direct action.

Safe printable Base64, numeric-entity tutorials, protocol examples, color bytes, hashes, and binary fixtures must not become `MEDIUM`. A benign recognized representation may remain finding-free; an explicit candidate-limit event may be informational.

Evidence is serialized within the existing model:

`encoding=html_numeric; original=&#...; decoded=...; decoded_signal=concealment`

Both excerpts are separately capped before the existing 240-character evidence cap. C0 controls, ESC, bidi, and invisible characters are escaped as code points. The original field path remains the finding path.

#### Impact assessment

- **Expected recall benefit:** directly addresses one failed representation per each of four observed obfuscation cases; no recovery is assumed.
- **FP risk:** medium, controlled by strict recognition, printable text, high-risk decoded signal, and educational-context checks.
- **Runtime:** at most 32 attempts and 4 KiB of retained decoded text per tool; no recursive pass.
- **Explainability:** improves through format, original evidence, decoded evidence, decoded signal, and original path.
- **Files/family:** a small pure `representations.py` helper plus `ObfuscationDetector`; family remains `obfuscation`.
- **Scope:** data-only, deterministic, bounded, and non-executable.

#### Required tests

- Positive tests for each exact format in root, schema, annotations, metadata, execution, and unknown fields.
- Invalid padding, odd hex, invalid entity/code point, NUL/control output, binary bytes, invalid UTF-8, and low-printability rejection.
- Exactly-one-depth behavior for encoded text that decodes to another encoding.
- Per-field, per-tool, input, output, and retained-text limits.
- Candidate-limit behavior is explicit and deterministic.
- Original/decoded evidence escaping, redaction, field path, and ordering.
- Benign Base64, numeric-entity documentation, hex colors/digests, decimal-code utilities, and protocol examples.

### Paraphrase coverage

#### Instruction-priority grammar: PI-002

`PI-002` covers the underlying construct “metadata claims authority over conflicting agent/user guidance.” It must require concepts from multiple columns in one sentence or bounded local window:

| Concept | Reusable normalized lexicon |
|---|---|
| Authority/precedence | `govern`, `controlling`, `binding`, `authoritative`, `take precedence`, `rank before/ahead`, `supersede`, `yield to` |
| Instruction object | `directive`, `policy`, `guidance`, `instruction`, `metadata`, `tool entry`, `operating rule` |
| Conflict/target context | `agent`, `assistant`, `model`, `user`, `conversation`, `when ... conflict`, `regardless of`, `even if`, `over ... guidance` |

Allowed variation is limited to inflection, hyphen/underscore/whitespace normalization, optional determiners, and a bounded number of intervening words. At least one authority relation and one agent/guidance conflict context are mandatory. A standalone “authoritative source” or ordinary record-ranking phrase does not trigger.

Suppressions remain local: explicit negation (“must not supersede user instructions”), educational/security-warning context, or quoted unsafe examples without a subsequent direct action. Do not copy exposed sentences into regexes.

#### Concealment grammar: HID-002

`HID-002` covers the construct “material activity is intentionally excluded from user/operator visibility.” Require a concealment action and visibility/disclosure object in one sentence or bounded window:

| Concept | Reusable normalized lexicon |
|---|---|
| Omission action | `omit`, `withhold`, `exclude`, `leave out`, `keep ... out`, `show/display only`, `suppress notice` |
| Material object | `activity`, `operation`, `side effect`, `existence`, `action`, `access`, `transfer` |
| Observer/disclosure | `user-facing`, `operator-visible`, `audit`, `notice`, `mention`, `report`, `explanation`, `view` |

At least two concept groups are required, including observer/disclosure context. Privacy redaction, accessibility/UI collapsing with an accessible details path, quiet-hours notifications, removal of irrelevant fields, and explicit “must not omit” language are benign contexts unless a direct hidden operation is also declared.

#### Impact assessment

- **Expected recall benefit:** addresses three primary instruction-paraphrase and three primary concealment FNs; actual recovery unknown.
- **FP risk:** medium-high for broad policy/visibility vocabulary; multi-concept and context gates are mandatory.
- **Runtime:** fixed compiled grammars over the same per-field traversal; low incremental cost.
- **Explainability:** stable rule ID, matched phrase, field path, construct explanation, and recommendation.
- **Files/families:** `injection.py` / injection and `secrecy.py` / concealment.
- **Scope:** deterministic rule grammar, not general NLP.

#### Required benign counterexamples

- PI: legal/policy precedence documentation unrelated to agents; sorting/routing records by priority; an authoritative reference without conflicting guidance; explicit safety precedence favoring user/system rules.
- HID: collapsible UI with discoverable details; privacy-preserving redaction; notification quiet hours; omission of irrelevant fields; “do not withhold notice.”
- Both: training quotations, security warnings, negated unsafe phrases, and concepts split across separate fields must not be concatenated into a match.

### Credential context

#### Current limitation

`SensitiveDataDetector` returns the first match from `all_text_fields`. `LEGITIMATE` examines only name plus description for a short allow-list and merely changes severity/score. It does not relate the sensitive term to an action, value, negation, documentation purpose, field type, or contradictory positive signal elsewhere.

#### Two-level strategy

Keep `SEC-001` as lexical credential terminology, but refine its existing severity decision:

- Demote to `LOW` when a same-sentence or tightly bounded context establishes documentation, reminder, identifier-name-only, synthetic/redacted/placeholder data, or explicit refusal to accept/store/return/transmit values.
- Do not globally suppress the term. Preserve a low explainable triage finding unless existing safe-context policy supports no finding.
- A benign cue in one field cannot suppress a positive action in another field.

Add `SEC-002` for action-linked sensitive-value handling. It requires:

1. a sensitive concept (`credential`, password, token, private/API key, secret, authentication store, recovery phrase, cookie, authorization value);
2. a value action within the same field/window (`provide`, `enter`, `collect`, `access`, `read`, `store`, `send`, `return`, `echo`, `expose`, `transmit`, `required`); and
3. no closer local negation applying to that action.

Input/output property names receive higher field importance only when an action/required relation or value-bearing description is present. A title-only word cannot produce `SEC-002`. Tool-wide logic evaluates all matches before selecting findings so field order cannot decide classification.

Decision outline:

| Sensitive term | Positive value action | Benign/negative local context | Result |
|---|---|---|---|
| No | — | — | No SEC finding |
| Yes | No | Yes | `SEC-001` LOW or suppressed by explicit policy |
| Yes | No | No | `SEC-001` lexical triage; provisional LOW unless field is value-bearing |
| Yes | Yes | No | `SEC-002` MEDIUM; optional accompanying `SEC-001` is deduplicated normally |
| Yes | Yes | Yes | Resolve closest scoped relation; contradictory fields preserve the positive `SEC-002` |

#### Impact assessment

- **Expected FP benefit:** directly targets four observed `SEC-001` binary FPs and title/first-match brittleness.
- **Expected recall benefit:** reusable vocabulary/action links cover recovery output and credential-store access mechanisms; actual recovery unknown.
- **FP risk:** medium through documentation, validators, security training, placeholders, and legitimate credential managers.
- **False-negative risk:** overbroad negation; controlled by same-field/sentence scope and contradictory-positive preservation.
- **Runtime:** collect and sort bounded matches over existing fields; low-to-medium incremental cost.
- **Explainability:** show term, action, local context decision, and exact field.
- **Files/family:** `sensitive_data.py`; family remains `sensitive-data`.
- **Scope:** transparent deterministic gating, not NLP.

#### Required tests

- Positive credential input, access, storage, transmission, return, and secret-output relations.
- “Does not accept,” “never stores,” “no credential values,” synthetic/redacted tokens, identifier names only, rotation reminders, policy, and documentation.
- Title-only term with safe description remains below `MEDIUM`.
- Benign title/description plus contradictory schema/execution value action still emits `SEC-002`.
- Closest-negation behavior, mapping-order invariance, all-field traversal, evidence redaction, and first-match elimination.

## Capability strategy

`CAP-001` must remain `INFORMATIONAL`. Capability alone is not poisoning, and the current evaluator classifies by finding severity, so blanket promotion to `MEDIUM` would immediately turn every matched legitimate administrator tool into a suspicious prediction.

P0 strengthening occurs through `MIS-002`, where capability evidence becomes binary-relevant only when purpose contradiction and a corroborator are both present. `CAP-001` should consume the same structured capability extractor so its vocabulary and evidence paths improve, but its severity and triage role remain unchanged.

`CAP-002` is a **P1**, not P0, candidate for corroborated high-impact capability when purpose is unclear rather than explicitly contradictory. It may emit `MEDIUM` only for a reviewed conjunction such as:

- destructive category plus explicit no-confirmation/no-consent wording;
- credential access plus outbound transmission;
- outbound network plus concealment finding;
- three unrelated high-impact categories without an administrative purpose;
- destructive operation plus hidden or low-salience placement and no safety control.

The gate must use existing findings or structured signals, never the total risk score alone. Aligned admin purpose, explicit confirmation, dry-run/plan-only behavior, and field-local negation prevent escalation. P1 acceptance requires its own hard negatives and cannot be slipped into `CAP-001`.

## Schema construct-boundary strategy

R08 demonstrates that invalid schema and malicious influence are different constructs. `SCH-001` correctly identifies malformed JSON Schema requiring security/compatibility review, but that alone does not establish poisoning intent. These signals should not automatically contribute equally to a binary tool-poisoning claim.

### Minimal decision

- Keep schema validation and `SCH-001`; do not delete or relabel R08.
- Do not change `SCH-001` severity or evaluator behavior inside the P0 detector-improvement patch.
- In v0.3 reporting language, describe `schema` findings as schema-security/compatibility findings unless corroborated by a poisoning indicator.
- Treat a machine-readable separation as P2 because the existing `Finding` and evaluation artifact schemas do not include a finding domain.

### P2 machine-readable design, if approved separately

Add a stable finding domain such as `tool_poisoning` versus `schema_security`, preserve `SCH-001` in the latter, report both, and define poisoning classification using only the appropriate domain. This would require a deliberate `Finding` schema change, experiment output-schema version change, reporter/evaluator changes, compatibility migration, updated protocol, and new confirmatory design. It must not be approximated by silently lowering `SCH-001` or altering H0.

`SCH-002` remains a capability/schema indicator and should gain local negation/context only after the shared capability/context helpers exist. It is P1 to prevent scope expansion in the P0 patch.

## Proposed rule IDs

| ID | Family | Proposed semantics | Provisional threshold relevance | Status |
|---|---|---|---|---|
| `PI-002` | injection | Authority/precedence claim over conflicting agent/user guidance | HIGH after multi-concept gate | P0 exploratory |
| `HID-002` | concealment | Intentional omission from user/operator-visible disclosure | HIGH after multi-concept gate | P0 exploratory |
| `SEC-002` | sensitive-data | Sensitive value linked to collection/access/storage/transmission/output action | MEDIUM after scoped-negation gate | P0 exploratory |
| `MIS-002` | mismatch | Declared-purpose versus path-specific high-impact capability contradiction with corroboration | MEDIUM; HIGH only for reviewed destructive+concealment conjunction | P0 exploratory |
| `OBF-005` | obfuscation | Strict bounded decoding reveals a reusable high-risk textual signal | MEDIUM after decode and context gates | P0 exploratory |
| `CAP-002` | capability | Multiple corroborated high-impact capabilities without explicit contradiction | MEDIUM under strict conjunction | P1 exploratory |

Existing IDs are retained for existing semantics. `PI-002`, `HID-002`, `SEC-002`, `MIS-002`, and `OBF-005` must be registered in their current detector families for evaluation ablation and `mcpsec explain`. `CAP-002` is not registered until its P1 design and hard-negative suite are approved. No new ID is assigned for the deferred schema reporting domain.

## FP-risk analysis

At least these counterexample classes are mandatory before a new rule may reach `MEDIUM`:

| Rule | Naive-trigger benign counterexamples | Required protection |
|---|---|---|
| `PI-002` | policy precedence documentation; routing/sorting priority; authoritative reference data; user/system-safety precedence | agent/guidance conflict relation, local negation, education/quotation gate |
| `HID-002` | collapsible UI; privacy redaction; quiet-hours notifications; omission of irrelevant fields; accessibility summaries | material-operation plus observer/disclosure relation, local safety/negation gate |
| `SEC-002` | credential documentation; rotation reminder; redacted/synthetic validator; identifier-name inventory; legitimate password manager | sensitive-term/action relation, same-window negation, field-aware contradictory-positive check |
| `MIS-002` | explicit dry-run planner; declared admin tool; network simulation; broad orchestration platform; policy document listing forbidden capabilities | aligned-purpose grammar, local negation/simulation, corroboration, two-path evidence |
| `OBF-005` | safe Base64 content; encoded documentation example; HTML entity tutorial; hex color/digest; decimal code-point converter; protocol payload | strict format, printable/UTF-8 limits, decoded high-risk cue, original educational context |
| `CAP-002` | admin console; deployment orchestrator with confirmation; disaster-recovery tool; simulation-only network test; documented batch operations | multiple-signal conjunction, aligned purpose, consent/safety controls; P1 only |

Risk review must include false negatives from over-suppression. A negative statement in one field cannot cancel an affirmative request in another, and educational context cannot suppress a quoted phrase followed by a direct action.

## Decoding threat model

| Threat | Failure mode | P0 control | Required verification |
|---|---|---|---|
| Oversized encoded text | Excessive regex/decode allocation | 512-character candidate; explicit over-limit review event | boundary tests at 511/512/513 and long recognized sequences |
| Many candidates | CPU amplification | 4 per field, 32 per tool, deterministic first-over-limit notification | 32/33 candidate test and stable ordering |
| Nested encodings | Recursive work and hidden chains | decode depth exactly 1; decoded text is never re-decoded | Base64-to-hex/Base64 test remains one pass |
| Decode explosion | Output larger than input expectation | no compression; maximum 512 decoded characters and 4 KiB retained/tool | expansion and total-budget tests |
| Binary garbage | Misleading evidence/control output | strict UTF-8, ≥90% printable, reject NUL/disallowed controls | invalid UTF-8, random bytes, control-heavy fixtures |
| Parser confusion | Broad format guessing or ambiguous tokens | four explicit recognizers; hex requires separators/prefixes; strict Base64 validation | hashes, UUIDs, colors, malformed padding remain benign |
| Unicode normalization surprises | Different raw/normalized interpretations | NFC exactly once after decoding; record whether normalization changed; escape invisible/bidi code points | combining-form and bidi/zero-width tests |
| Terminal/report injection | Decoded ANSI or spreadsheet-like evidence | safe escaped excerpt then existing reporter defenses; redaction applies to both excerpts | terminal literal and CSV neutralization regression |
| Cross-detector mutation | Decoded content replaces source metadata | immutable result object; transformed text never written into `ToolDefinition` | fingerprint before/after and equality tests |

The decoder must never import code, evaluate templates, open paths, fetch URLs, decompress archives, spawn processes, invoke tools, or select a codec based on payload guesses.

## Exploratory fixture plan

### Data-source separation

| Source | Role in v0.3 | Scientific label | Rules |
|---|---|---|---|
| Existing `evaluation/corpus/` | Regression and development comparison | **DEVELOPMENT** | Existing ground truth preserved; intentional metric changes documented. |
| New `evaluation/exploratory/v0_3/` | Mechanism and hard-negative development | **EXPLORATORY** | New wording; independently reviewed where practical; never called holdout. |
| Exposed `evaluation/holdout/` | Optional descriptive comparison after implementation | **POST-UNBLINDING EXPLORATORY** | H0 preserved; no relabeling/tuning; result kept separate. |

Because the current `CorpusSplit` enum supports only `development` and `holdout`, the new exploratory manifest can use machine split `development` while its corpus name, methodology note, run inventory, and report heading explicitly label it **EXPLORATORY**. Adding a new artifact split is not required for P0. The three result sets must never be pooled into one confusion matrix or “overall” score.

### Proposed size and coverage

Create 18 benign hard negatives and 18 suspicious exploratory samples—small enough for review and large enough to cover each mechanism. Do not copy exposed holdout strings.

| Mechanism | Benign | Suspicious | Design intent |
|---|---:|---:|---|
| Instruction priority | 3 | 3 | Precedence/reference/routing negatives versus agent-guidance conflicts. |
| Concealment | 3 | 3 | UI/privacy/quiet-mode negatives versus hidden material operations. |
| Credential context | 4 | 3 | Documentation, aliases, redaction, reminders versus value collection/output. |
| Purpose/capability | 4 | 5 | Admin, simulation, dry-run, declared capability versus corroborated contradiction. |
| Encodings | 4 | 4 | Safe Base64/entity/hex/decimal examples versus one new risky payload per format. |
| **Total** | **18** | **18** | 36 new exploratory samples. |

Vary fields across description, input/output schema, annotations, `_meta`, execution, and unknown/vendor data. Include obvious, moderate, and subtle labels only as descriptive author annotations. Every sample needs provenance, rationale, expected category/field, matched-pair note if applicable, and explicit statement that wording was authored from the construct rather than copied from the exposed holdout.

### Example concepts, not fixture text

- Instruction benign: data-source authority, record sort order, explicit rule that user/system guidance remains controlling.
- Concealment benign: collapsed details with a visible expansion path, secret-value redaction, muted notifications with audit history.
- Credential benign: placeholder format validator, credential alias catalog, rotation calendar, authentication documentation that accepts no values.
- Capability benign: declared database administrator with confirmation, offline network simulator, plan-only file migration, command documentation index.
- Encoding benign: printable public example, numeric-entity tutorial, hex color/byte documentation, decimal code-point conversion.
- Suspicious concepts should express the same constructs with entirely new objects, verbs, tools, field locations, and sentence structures.

## Performance budget

Historical H0 timing is 1.7159 ms/tool analysis-core and 4.3020 ms/tool static-end-to-end on the recorded local machine. These numbers are not formal preregistered v0.3 limits.

Use an exploratory engineering guardrail under comparable local conditions:

- analysis-core mean target: no more than 3.4318 ms/tool (2× historical H0 mean);
- analysis-core p95 observation target: no more than 6.4458 ms/tool (2× historical H0 p95);
- static-end-to-end mean reference: no more than 8.6040 ms/tool where the same boundary is measured;
- decoder hard bounds must hold even for maximal accepted candidates;
- repeated outputs must have identical ordered findings, evidence, paths, severity, and risk.

Measure development and exploratory corpora separately with warm-ups excluded and repeated observations. Do not place hard wall-clock assertions in ordinary CI; they are environment-flaky. Use the experiment timing engine and report machine/background-load limitations. A guardrail breach triggers profiling and scope reduction, not silent benchmark relaxation.

## Exact file/change map

This is the proposed 4B map. No listed file was changed during Day 4A.

| File/module | Smallest intended 4B change | Tests affected/added | Security invariant |
|---|---|---|---|
| `src/mcpsec/detectors/base.py` | Add pure bounded local-window/sentence helpers and safe transformed-evidence formatting; do not change traversal return types. | Existing injection/secrecy tests; new boundary/escaping tests. | Values remain field-separated; no mutation; deterministic paths. |
| `src/mcpsec/detectors/injection.py` | Factor existing match selection into a pure helper; add multi-concept `PI-002` grammar with local negation/education gate. | Extend `test_injection_detector.py`. | Fixed built-in regex only; no user regex; no cross-field concatenation. |
| `src/mcpsec/detectors/secrecy.py` | Add multi-concept `HID-002` grammar with observer/disclosure requirement. | Extend `test_secrecy_detector.py`. | Same-field context only; transparent evidence. |
| `src/mcpsec/detectors/sensitive_data.py` | Evaluate all sorted matches; add scoped benign/negative context; add action-linked `SEC-002`; retain `SEC-001` as lexical triage. | Extend `test_sensitive_detector.py`. | No global disclaimer suppression; order invariance. |
| `src/mcpsec/detectors/representations.py` (new) | Pure depth-one recognizers/decoders with dataclass result and explicit limits for numeric entities, hex, decimal, Base64. | New `test_representations.py`. | Data only; strict UTF-8; no execution/network/decompression/recursion. |
| `src/mcpsec/detectors/obfuscation.py` | Call bounded helper across `all_text_fields`; add `OBF-005` only for decoded high-risk text; preserve OBF-001–004 behavior. | Extend `test_obfuscation.py`. | Original field/evidence retained; controls escaped; budgets explicit. |
| `src/mcpsec/detectors/permissions.py` | Replace blob-only internal matching with exported structured capability signals; render existing `CAP-001` from those signals without severity promotion. | Add `test_permissions_detector.py` or focused cases in existing detector tests. | Capability alone remains informational; every signal has a path. |
| `src/mcpsec/detectors/mismatch.py` | Reuse structured signals; add aligned-purpose/narrow-purpose grammars and corroborated `MIS-002`. Preserve `MIS-001` input-schema behavior. | Extend `test_mismatch_detector.py`; add cross-field cases. | No binary finding without contradiction plus corroboration. |
| `src/mcpsec/rules/builtin.py` | Add rationale, benign trigger, and recommendation entries for five P0 IDs. | CLI explain/list tests. | Every rule explains legitimate triggers and review guidance. |
| `src/mcpsec/evaluation/ablation.py` | Register P0 IDs under existing families; no new preset. | Update `test_experiment_engine.py` family/rule-set expectations. | Evaluation and ordinary scan use identical detectors; configuration hash reflects new IDs. |
| `tests/test_injection_detector.py` | Suspicious phrase-family cases, benign precedence cases, negation, field separation, order. | Existing file. | Regression plus counterexamples. |
| `tests/test_secrecy_detector.py` | Visibility/omission cases and UI/privacy/quiet-mode negatives. | Existing file. | No weakening of education/negation checks. |
| `tests/test_sensitive_detector.py` | Context matrix, all-field ordering, contradictory fields, SEC-001/002 behavior. | Existing file. | No first-match classification; scoped negation only. |
| `tests/test_obfuscation.py` and new `tests/test_representations.py` | Four formats, every bound, binary garbage, depth, escaping, safe examples. | Existing + new. | Decoder threat-model enforcement. |
| `tests/test_mismatch_detector.py` and capability tests | Category extraction, purpose alignment, corroboration, paired paths, admin/dry-run negatives. | Existing + optional focused new file. | Powerful capability is not automatically malicious. |
| `tests/test_risk.py` | Regression only unless a reviewed new synergy is proposed later. | Existing file. | Caps, deduplication, order invariance remain exact. |
| `tests/test_experiment_engine.py` | New rule IDs in family resolution and configuration identity; deterministic repetitions. | Existing file. | Artifact configuration enumerates exact active rules. |
| `tests/test_cli.py` | `list-rules`/`explain` coverage for new IDs and stable output. | Existing file. | Inert output and known-ID validation. |
| `evaluation/exploratory/v0_3/` (new) | Add 18 benign and 18 suspicious construct-derived exploratory fixtures and manifest. | Corpus loader/check plus exploratory evaluation. | Explicit exploratory status; no copied holdout wording. |
| `tests/test_evaluation.py` | Preserve development regression and transparently update only intentional metric changes after review. | Existing file. | No hidden baseline adjustment. |
| `docs/detection-rules.md`, `docs/architecture.md`, `docs/evaluation-methodology.md`, `README.md`, `evaluation/CHANGELOG.md` | After behavior stabilizes, document IDs, bounds, exploratory status, metric changes, and exposed-holdout limitation. | Documentation review/build if configured. | Claims match enforcement; H0 remains authoritative. |
| `src/mcpsec/__init__.py`, `pyproject.toml` | Bump to `0.3.0` only after 4B acceptance, not during initial coding. | Version CLI/baseline/smoke tests. | Version identity matches artifacts and wheel. |

P0 should not require changes to `scanner.py`, `models.py`, `risk.py`, `normalizer.py`, `loader.py`, reporters, retrieval, fingerprints, baselines, canonicalizer, corpus hashing, or evaluation artifact schema. A discovered need to modify one of these is a scope-review checkpoint, not an automatic expansion.

## 4B implementation sequence

| Stage | Objective | Files / new IDs | Tests | Acceptance criteria | Effort |
|---|---|---|---|---|---|
| 1. Context primitives | Add deterministic local windows, scoped negation, and safe evidence helpers without detector behavior changes. | `base.py`; no ID | Existing PI/HID/SEC regression plus helper boundaries | Existing detector outputs byte-for-byte equivalent before later stages; strict mypy/Ruff. | Small |
| 2. Credential context | Remove first-match dependence, demote proven benign lexical context, and add action-linked handling. | `sensitive_data.py`, `builtin.py`; `SEC-002` | Context matrix, field order, title-only, contradictory fields, benign hard negatives | Positive value handling reaches MEDIUM; documentation/redaction/alias cases do not; SEC existing positives reviewed. | Medium |
| 3. Phrase families | Add construct-derived authority and visibility grammars. | `injection.py`, `secrecy.py`, `builtin.py`; `PI-002`, `HID-002` | Suspicious variants and at least four benign classes each; no cross-field concatenation | New constructs trigger with exact paths; all benign counterexamples and legacy cases pass. | Medium |
| 4. Bounded representations | Implement four recognizers, depth-one decode, budgets, safe rendering, and decoded-risk gate. | new `representations.py`, `obfuscation.py`, `builtin.py`; `OBF-005` | Format positives, safe encodings, 511/512/513, 32/33 candidates, binary/control/recursion cases | Every threat-model limit enforced; safe encodings below MEDIUM; evidence contains bounded original and decoded forms. | Medium-high |
| 5. Capability normalization | Produce stable categories and paths; make CAP-001 consume them without severity change. | `permissions.py`; no new P0 ID | Ten categories, paths, negation, admin/simulation negatives, legacy CAP | CAP-001 stays informational; stable ordered evidence; no blanket escalation. | Medium |
| 6. Cross-field consistency | Add purpose alignment, narrow-purpose cues, and three-layer corroboration. | `mismatch.py`, `builtin.py`; `MIS-002` | Each corroborator; aligned admin, dry-run, simulation, denial, mapping order | Finding identifies both fields; no uncorroborated capability reaches MEDIUM. | High |
| 7. Registration and fixtures | Register family IDs and build independent exploratory development data. | `ablation.py`, `evaluation/exploratory/v0_3/`, experiment/CLI tests | Family resolution, corpus-check, 18+18 fixture review | Exact active IDs recorded; corpus is labeled exploratory; no cross-split duplicate/exact overlap. | Medium-high |
| 8. Regression and performance | Run full quality gates, development metrics, exploratory metrics, build/wheel smoke, and comparable timing. | Tests, docs/CHANGELOG after results; version files only at acceptance | Ruff, format, strict mypy, coverage suite, build, wheel smoke, deterministic repeat, timing | No invariant regression; every metric change documented; analysis mean within engineering guardrail or scope reviewed. | High |
| 9. Schema-domain decision | Decide whether machine-readable schema/poisoning separation warrants a new artifact schema. Not part of P0 4B. | Potential `models.py`, evaluator/reporter/protocol; no ID | Migration/compatibility and construct tests if approved | Separate design approval and new evaluation protocol. | Deferred/P2 |

Stage gates are sequential. If a stage materially raises benign false positives, violates the decoder threat model, changes unrelated fingerprints/baselines, or breaches the performance guardrail, stop and narrow that stage before continuing. Do not consult exposed-holdout predictions during per-pattern implementation.

## P0/P1/P2/Do-not-build matrix

| Priority | Change | Research value / observed target | FP risk | Complexity | Runtime | FYP scope fit |
|---|---|---|---|---|---|---|
| P0 | Scoped SEC context + `SEC-002` | Four observed FPs; sensitive-value vocabulary/action gap | Medium | Medium | Low-medium | Excellent |
| P0 | `PI-002` and `HID-002` phrase families | Six primary FNs; two families with zero detection | Medium-high | Medium | Low | Excellent |
| P0 | Bounded four-format decode + `OBF-005` | Four primary FNs; entire expected category missed | Medium | Medium-high | Bounded medium | Good |
| P0 | Structured capability signals + `MIS-002` | Five primary FNs plus two threshold cases | High | High | Medium | Good if tightly gated |
| P1 | `CAP-002` multi-signal escalation | Cases with no clear purpose contradiction but strong compound capability | High | High | Low after shared signals | Moderate |
| P1 | Context-aware `SCH-002` | Two schema vocabulary FPs | Medium | Medium | Low | Good |
| P1 | More field-aware sensitive/output constructs | Recovery output and special schema vocabulary | Medium | Medium | Low | Good |
| P1 | First-match/evidence-quality cleanup outside SEC | Better deterministic evidence selection | Low | Low-medium | Low | Good |
| P2 | Machine-readable schema-security vs poisoning domain | R08 construct validity | Low detection risk, high migration risk | High ecosystem change | Low | Research-method scope |
| P2 | Native `exploratory` corpus split | Clearer artifact semantics | Low | Medium schema change | None | Optional |
| P2 | Multilingual phrase corpora/rules | External-validity expansion | High | High | Medium | Later study |
| DO NOT BUILD | Blanket `CAP-001` promotion | Addresses only two below-threshold cases superficially | Very high | Low | None | Violates evidence |
| DO NOT BUILD | Global threshold reduction | 17/19 FNs had no finding | High | Low | None | Wrong mechanism |
| DO NOT BUILD | Holdout-sentence regex memorization | Apparent exposed-set gain | Extreme scientific bias | Low | Low | Invalid research |
| DO NOT BUILD | Unbounded/recursive/arbitrary codec engine | Broader decoding | Severe security/DoS | High | Unbounded | Violates premise |
| DO NOT BUILD | LLM/embedding classifier in v0.3 | Semantic coverage | Privacy, nondeterminism, cost | Very high | High | Changes project premise |
| DO NOT BUILD | Remove SEC from exposed ablation | Post-hoc F1 gain | Missed real sensitive handling | Low | Lower | Invalid inference |
| DO NOT BUILD | Relabel R08 or edit old holdout/H0 | Cleaner result | Research-integrity failure | Low | None | Prohibited |

## Success criteria

Exploratory v0.3 success is mechanism- and invariant-based, not a target H0 F1:

1. Every new suspicious exploratory fixture triggers its intended new rule with the correct field/evidence.
2. Every paired benign hard negative remains below `MEDIUM`, including at least three counterexample types per rule.
3. Legacy detector unit tests and production defaults remain valid or any intentional change is explicitly reviewed and documented.
4. Development results are reported separately; no unexplained loss of a prior true positive or new false positive is accepted.
5. The new exploratory corpus is reported separately and never called holdout.
6. An optional old-holdout rerun is labeled **POST-UNBLINDING EXPLORATORY**. Improved recall and non-worsened FPR are useful observations, not acceptance thresholds.
7. Repeated scans produce identical ordered findings, paths, evidence, severity, score contributions, and risk.
8. Decoder limits, input invariants, fingerprints, baselines, suppressions, resource caps, terminal/CSV safety, package build, and wheel smoke tests pass.
9. Comparable analysis-core mean remains within the 2× engineering guardrail or the added scope is reduced/reviewed.
10. Every behavior and metric change is recorded without overwriting v0.2/H0 evidence.

Do not define success as “F1 must exceed X on the exposed holdout.” That would reward direct optimization against known test errors.

### 4C measurement plan

Report three independent result blocks:

| Block | Required label | Measures |
|---|---|---|
| Existing development corpus | **DEVELOPMENT** | Confusion matrix, accuracy, precision, recall, F1, FPR, per-rule changes, timing, regression inventory |
| New v0.3 fixtures | **EXPLORATORY** | Same metrics plus intended-rule coverage and benign hard-negative pass rate |
| Old 48-sample corpus, if authorized | **POST-UNBLINDING EXPLORATORY** | Same metrics, paired prediction changes versus preserved H0, resolved/introduced FP/FN, explicit nonconfirmatory warning |

Also measure no-finding versus below-threshold FNs, rule/family contribution, field paths, candidate-limit events, deterministic repetition, analysis-core timing, and static-end-to-end timing where useful. Never pool the three blocks into one score.

## Confirmatory-evaluation requirement

Any claim that v0.3 generalizes better requires a **new untouched holdout** authored without testing wording against v0.3, independently reviewed while blinded to detector predictions, frozen with corpus/configuration/source hashes, preregistered, and evaluated once after a clean pre-unblinding audit.

The original 48-sample holdout has been exposed. It may be used only for:

- post-unblinding exploratory comparison;
- regression understanding;
- paired error analysis explicitly labeled exploratory.

It can never again supply independent confirmatory evidence for any modified detector.

## What remains unchanged

Unless a separately approved scope review establishes necessity, 4B must not change:

- authoritative H0/H1/ablation artifacts or the Day 3 reports;
- original holdout samples, manifest, labels, review records, hash, or Git history;
- default `MEDIUM` threshold;
- `CAP-001` informational severity;
- scanner orchestration and detector interface;
- capped/deduplicated risk formula and bounds;
- loader formats, 10 MiB input boundary, node/tool/string/nesting limits;
- NFC normalization, alias conflict rejection, unknown-field preservation, duplicate-name rejection;
- canonical JSON, fingerprints, baseline formats, and drift behavior;
- custom-rule data-only literal matching and suppression semantics;
- MCP `tools/list`-only, loopback-only, no-proxy, no-redirect transport boundary;
- reporter terminal escaping, HTML inertness, and spreadsheet-formula neutralization;
- corpus hashing and cross-split integrity logic;
- experiment artifact schema 3.0.0 and comparison semantics during P0;
- static default behavior: no tool invocation, command execution, metadata URL retrieval, icon download, or model submission.

## Zero-mutation verification

Final verification after the report audit recorded:

| Check | Final result |
|---|---|
| Git HEAD | `a4abee4661522ac13edb37e1b075186a2ccd7a03` — exact and unchanged |
| Tracked status entries | 0 — clean |
| H0 SHA-256 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` — exact |
| Day 3C SHA-256 | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` — exact |
| Tracked Day 4A files | 0 |
| Day 4A output status | Ignored under `evaluation/runs/day4a/` |
| `git diff --check` | No output |

## Final recommendation

Proceed to Day 4B with the four P0 workstreams, in staged order, only after treating this report as a design—not a validation result. The implementation should add five stable P0 rule IDs (`PI-002`, `HID-002`, `SEC-002`, `MIS-002`, `OBF-005`), keep `CAP-001` informational, preserve `MEDIUM`, avoid risk-engine changes, and defer machine-readable schema-domain separation and `CAP-002` to later review.

The most important discipline is to develop against the existing development corpus plus new construct-derived exploratory fixtures, not against the exposed 48 samples. Any old-holdout rerun belongs to 4C and must be labeled post-unblinding exploratory. Any generalization claim requires a new untouched holdout.

NO DETECTOR MODIFICATION WAS PERFORMED DURING DAY 4A.

ALL PROPOSED CHANGES ARE POST-UNBLINDING EXPLORATORY DESIGNS.
