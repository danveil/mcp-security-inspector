# FYP Technical Handover and Research Resumption Guide

> **Project status: PRE-FYP RESEARCH PROTOTYPE / PILOT STUDY**
> Repository checkpoint inspected: `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`
> Package: `0.3.0a1` | built-in rule pack: `builtin` `2.0.0`
> Prepared for Day 6C research continuity; no fresh experiment was created or run.

This document is the continuity layer between the repository map in
[`captain-technical-map.md`](captain-technical-map.md), the teaching material in
[`captains-manual.md`](captains-manual.md), and a future supervisor-approved FYP.
It answers a different question from those documents:

> If the original student returns months later with limited memory, what is the
> scientific state, what must be protected, and what sequence makes it safe to
> resume formal research?

The repository is authoritative. If this document ever disagrees with code,
Git history, or an immutable artifact, stop and investigate instead of editing
the evidence to make the documents agree.

---

## 1. Executive handover to future me

MCP Tool Security Inspector is a defensive Python prototype for deterministic
static analysis of Model Context Protocol (MCP) tool definitions. An MCP tool
definition contains untrusted metadata such as a name, description, JSON Schema,
annotations, execution/vendor fields, and extension metadata. That text and
structure may influence how an AI host or agent understands and chooses a tool.
The project investigates whether a lightweight, explainable, bounded rule system
can identify suspicious metadata and metadata drift without executing any tool.

The engineering prototype already includes hostile-input loading, normalization,
seven detector families, 16 stable rule identities, deterministic risk scoring,
bounded representation decoding, data-only custom rules and suppressions,
terminal/JSON/CSV/SARIF reporting, canonical fingerprints, baselines and drift,
loopback-only opt-in `tools/list` retrieval, and a reproducible evaluation engine.
It is intentionally static: it must not invoke tools, execute metadata, follow
metadata-linked resources, or submit catalog content to a model.

The research pilot already produced three different kinds of evidence:

1. **Development/regression evidence.** The 80-sample development corpus reports
   strong in-sample results, but it was visible during detector work.
2. **The authoritative first confirmatory result.** The frozen v0.2 detector was
   evaluated once on the prediction-unexposed, independently reviewed 48-sample
   holdout. Performance was poor, especially recall. That negative result is the
   principal confirmatory result of the pilot and must remain unchanged.
3. **Post-unblinding exploratory evidence.** The holdout failures informed five
   v0.3 rules. Reusing the now-exposed holdout produced better point estimates,
   but that comparison is diagnostic only and cannot show improved
   generalization.

What remains unresolved is the central formal-FYP question: whether a frozen
revised detector transfers to genuinely unseen, independently prepared MCP
metadata while controlling false positives and processing cost. Answering that
requires supervisor approval, a justified method, a new untouched corpus, a
fresh preregistration, independent blinded review, and one protected evaluation.
The current repository is therefore a strong **engineering and pilot-research
foundation**, not a completed FYP and not a production-ready detector.

### Resume in one sentence

Preserve the historical evidence, use the existing corpora only for their
declared development or historical purposes, agree on the formal methodology
with the supervisor, freeze the next detector and protocol, and only then create
and evaluate a genuinely new holdout.

---

## 2. Original research problem reconstructed

### 2.1 Problem

MCP standardizes how an AI host discovers and communicates with servers that
offer tools. A discovered tool definition is more than a neutral function
signature: its descriptions, schemas, annotations, and extensions tell the host
what the tool supposedly does and how it should be used. This creates a trust
boundary. A compromised or deceptive publisher can place manipulative,
concealed, inconsistent, sensitive-data-seeking, obfuscated, or malformed
content in metadata. The metadata may be accidental, ambiguous, or malicious;
the presence of a suspicious construct does not prove intent.

The project calls the adversarial use of tool metadata **tool poisoning**. It is
related to prompt injection because metadata can contain instruction-like text,
but it is specifically attached to a tool definition and its discovery context.
The project does not claim to detect all prompt injection, all malicious tools,
or runtime behavior. It inspects static declarations.

### 2.2 Proposed approach

Investigate a lightweight deterministic pre-use inspection layer that:

- treats all publisher-controlled metadata as hostile data;
- normalizes common MCP aliases without discarding unknown fields;
- traverses all relevant text-bearing fields with stable paths;
- applies explicit lexical, contextual, schema, consistency, capability, and
  bounded-decoding rules;
- emits explainable findings rather than a hidden model score;
- calculates a capped aggregate risk for triage;
- fingerprints canonicalized metadata for later drift detection; and
- records corpus, code, configuration, timing, and artifact identities for
  reproducible research.

This is a decision-support mechanism. A finding means “review this construct,”
not “malice proven.”

### 2.3 Why rule-based static detection was chosen

The prototype prioritizes determinism, auditability, offline operation, low
cost, privacy, bounded resource use, stable rule identity, and reproducible
experiments. Fixed rules make it possible to explain exactly why a result
occurred and to hash the resolved configuration. They also have a known cost:
paraphrases, non-English content, distant semantic relationships, and unseen
representations can bypass narrow rules. The v0.2 H0 recall of 20.83% is direct
evidence of that semantic-coverage limitation.

An LLM classifier might be a future comparison condition, but it is not a drop-in
improvement. It changes privacy, determinism, latency, cost, model/version drift,
prompt-injection exposure, and reproducibility. Such a comparison needs a new
research question and threat model rather than being silently added to this
prototype.

### 2.4 Why schema hashing and drift matter

A tool can appear safe when first approved and later change its description,
input/output schema, annotations, execution hints, or vendor metadata. Canonical
component fingerprints answer “what changed?” without storing all raw metadata
inside a baseline. This supports the original FYP idea of detecting metadata or
schema drift between an approved state and a later discovery. Drift is evidence
of change requiring review; it does not by itself prove compromise.

### 2.5 Four layers that must remain separate

| Layer | What exists | What it can establish |
|---|---|---|
| **Problem** | Untrusted MCP metadata may influence agent/tool decisions and may drift | A security-relevant trust boundary worth studying |
| **Proposed approach** | Deterministic bounded static inspection plus fingerprints | A testable design hypothesis, not effectiveness by itself |
| **Engineering implementation** | Python package, CLI, rules, risk, reports, baselines, retrieval, evaluation | The prototype implements stated mechanisms and safety boundaries |
| **Research evaluation** | Development, H0, failure analysis, exploratory v0.3 artifacts | Corpus-bounded measurements with different scientific statuses |

---

## 3. Exact current system state

The current source checkpoint is commit
`374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`. Local Git currently has an
annotated `v0.3.0a1` tag at this commit, and the locally stored `origin/main`
tracking ref resolves to the same commit. This is a statement about local refs;
it is not a fresh network verification of GitHub availability.

| Property | Current state | Repository authority |
|---|---|---|
| Package | `mcp-tool-security-inspector` `0.3.0a1`; Python `>=3.12` | `pyproject.toml`, `src/mcpsec/__init__.py` |
| Built-in rule pack | `builtin` `2.0.0` | `src/mcpsec/constants.py` |
| Evaluation binary threshold | `MEDIUM` by default | `src/mcpsec/evaluation/evaluator.py`, `src/mcpsec/cli.py` |
| Current artifact schema | `3.1.0`; historical `3.0.0` supported | `src/mcpsec/evaluation/models.py`, `comparison.py` |
| Detector registry | 7 families, 16 stable rule IDs | `src/mcpsec/detectors/__init__.py`, `src/mcpsec/rules/builtin.py` |
| Injection | `PI-001`, `PI-002` | `detectors/injection.py` |
| Concealment | `HID-001`, `HID-002` | `detectors/secrecy.py` |
| Sensitive data | `SEC-001`, `SEC-002` | `detectors/sensitive_data.py` |
| Schema | `SCH-001`, `SCH-002` | `detectors/schema.py` |
| Mismatch | `MIS-001`, `MIS-002` | `detectors/mismatch.py` |
| Obfuscation | `OBF-001` through `OBF-005` | `detectors/obfuscation.py`, `representations.py` |
| Capability | `CAP-001` only; there is no `CAP-002` | `detectors/permissions.py` |
| Reports | Terminal, JSON, CSV, SARIF | `src/mcpsec/reporter.py`, `cli.py` |
| Baselines/drift | Full and component SHA-256 fingerprints; add/remove/change and conservative rename inference | `canonicalizer.py`, `fingerprint.py`, `baseline.py`, `compare.py` |
| Custom rules | Strict data-only JSON/YAML; literal patterns, bounded counts/lengths, collision checks | `src/mcpsec/rules/loader.py`, `models.py` |
| Suppressions | Known rule ID, optional exact tool scope, written justification; data-only | `src/mcpsec/suppressions.py` |
| Bounded decoding | Depth one; numeric HTML entities, separated/prefixed hex bytes, decimal character codes, strict Base64 | `detectors/representations.py`, `obfuscation.py` |
| Retrieval | Explicit opt-in loopback HTTP(S) `tools/list`; no redirects or environment proxies; no tool calls | `src/mcpsec/retrieval.py` |
| Historical comparison | Validates recorded identities/rule sets and rejects incompatible comparisons; does not reinterpret old results as current | `src/mcpsec/evaluation/comparison.py` |

### 3.1 Important resource ceilings

The source currently enforces, among other limits: 10 MiB scan/baseline input,
1 MiB rule and suppression files, 100,000-character strings, depth 64, 100,000
structure nodes, 1,000 static tools, 100 retrieval pages, 200 custom rules, 500
suppressions, 64 retained findings per tool, 2,048 retained findings per report,
and 8,192 retained evidence characters per tool. `OBF-005` separately limits a
candidate and decoded output to 512 characters, four candidates per field, 32
per tool, and 4,096 retained decoded characters per tool. These are security
controls, not test conveniences.

### 3.2 Risk and threshold nuance

The evaluator predicts “suspicious” when at least one retained detector finding
has severity `MEDIUM` or higher. This frozen H0 classification threshold is not
the same as aggregate tool risk. `risk.py` separately confidence-adjusts and
deduplicates findings, caps category contributions, combines categories, applies
two documented synergies, and maps the final score to severity bands. A MEDIUM
finding can therefore classify an evaluation sample as suspicious even if its
aggregate risk score is below the MEDIUM risk band. Never silently conflate the
two mechanisms.

### 3.3 Testing state

The most recent preserved Day 5C verification reported **472 passing tests,
92.95% coverage, Ruff lint/format success, strict mypy success, package build
success, and a fresh installed-wheel smoke success**. That is an historical
verification of commit lineage, not a new Day 6C run. Test count and coverage
show exercised behavior; they do not prove absence of vulnerabilities or
real-world detector effectiveness.

---

## 4. Research chronology and evidence classes

### 4.1 Status vocabulary

- **Development evidence:** data was visible during design/tuning. Useful for
  regression, debugging, and mechanism checks; not independent generalization.
- **Confirmatory evidence:** a preregistered frozen configuration was evaluated
  on prediction-unexposed reviewed data. In this pilot, this means v0.2 H0 only.
- **Post-unblinding forensic analysis:** analysis of H0 failures after predictions
  were known. Useful for explanation and hypothesis formation.
- **Post-unblinding exploratory evidence:** candidate changes or comparisons
  informed by exposed results. Useful for design clues, not confirmation.
- **Engineering verification:** tests, type/lint/build/smoke and boundary audits.
  It supports implementation correctness, not detector generalization.

### 4.2 Chronological timeline

| Date/checkpoint | What changed | Exposure/scientific status | Evidence and permitted conclusion |
|---|---|---|---|
| 2026-08-20, `cb44017692498f65d94a74660a44663b41b3099d` | Initial repository version | Pre-research foundation | Project history only |
| 2026-08-25, `eac0341c8da027755265f7345ec3b296b3979565` | Added reproducible v0.2 evaluation material | Development evidence | Early repeatable prototype evaluation, not independent generalization |
| 2026-08-27, `47750760f030628bbbba83e71528f2ce81cb16f0` | Hardened FYP development baseline: hostile-input, retrieval, reporting, test and packaging controls | Pre-unblinding engineering verification | A safer development baseline existed before H0 |
| 2026-08-27, `7d9ab8115dfdfa349f983a643765b6d9a6a78cea` | Added research protocol, corpus identity/integrity, metadata and reproducibility foundation | Pre-unblinding methodology | The project began recording scientific identities and split policy |
| 2026-08-27, `997c5fcf11a6f0800dceb022426cc32e0d522e04` | Added experiment engine, uncertainty, stratification, ablations and comparison | Pre-unblinding methodology/engineering | Frozen experiments and compatible historical comparisons became possible |
| 2026-08-27, `a4abee4661522ac13edb37e1b075186a2ccd7a03` | Froze independently reviewed holdout 1.0.1 and experiment plan | **Pre-unblinding freeze** | Holdout identity, review, labels, H0 threshold/configuration became fixed |
| Day 3A | Audited clean checkpoint, corpus/config hashes, blindness, preregistration and quality readiness | Pre-unblinding gate | Repository evidence was consistent with a safe H0 run; no prediction produced during the audit |
| Day 3B | Ran the primary v0.2 H0 once on the 48-sample holdout | **Authoritative first confirmatory evidence** | The frozen detector performed poorly on this controlled holdout; exact artifact must remain immutable |
| Day 3C | Analyzed H0 false negatives, false positives, categories and ablations | **Post-unblinding forensic analysis** | Failure mechanisms and hypotheses may be described; the holdout became permanently exposed |
| Day 3D | Created results/discussion tables, claims and viva evidence from preserved results | Post-H0 synthesis, not a new experiment | Secondary documentation supports reporting; much of this bundle is local/ignored |
| Day 4A | Designed bounded hypotheses from Day 3C failures | **Post-unblinding exploratory design** | Five P0 candidates were justified; no confirmation occurred |
| Day 4B / `b1a5d4c92797f630a5aed8b19dec3da21085fa76` | Implemented/froze v0.3 exploratory candidate and 36 construct fixtures | Post-unblinding engineering/development | Mechanisms work on authored fixtures; no independent generalization claim |
| Day 4C | Re-ran the already exposed holdout and performed exploratory comparisons | **Post-unblinding exploratory evidence only** | Six known FNs changed to TP; FPs persisted; result cannot confirm v0.3 |
| Endgame-0 / Day 5A | Froze and adversarially audited candidate, research identity, artifact/history handling and boundaries | Engineering/security audit | Found remediation needs without rewriting H0 |
| Day 5B / `0651313cb9fe650f3004e849de7d14000343cacf` | Hardened reproducibility/safety; preserved authentic H0, Day 3C and Day 4C artifacts | Engineering remediation | Current code safely retains historical evidence; changes were not a retrospective H0 tune |
| Day 5C | Re-ran full release quality gates and verified immutable hashes | Engineering verification | 472 tests and build gates passed; scientific labels remained unchanged |
| Day 5D / `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` | Added public-alpha release, research-status and reproducibility documentation | Documentation/release checkpoint | Package `0.3.0a1`, rule pack `2.0.0`, with explicit exploratory limits |
| Day 6A | Created untracked `docs/captain-technical-map.md` | Knowledge extraction | Repository architecture and research map; no experiment |
| Day 6B | Created untracked `docs/captains-manual.md` | Knowledge extraction | Student teaching/viva manual; no experiment |
| Day 6C | Creates this untracked handover | Research continuity | Future resumption protocol; no fresh evidence |

The three primary tracked evidence files were added to Git during Day 5
hardening so they could be preserved byte-for-byte. Their later commit date does
not change when or under what exposure state the experiments occurred.

---

## 5. AUTHORITATIVE FIRST CONFIRMATORY RESULT — v0.2 H0

> **This is the authoritative first confirmatory result of the pilot. Do not
> replace it with a later, more favorable number.**

Artifact:
`evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json`

Artifact SHA-256:
`3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80`

| TP | TN | FP | FN | N |
|---:|---:|---:|---:|---:|
| 5 | 18 | 6 | 19 | 48 |

| Accuracy | Precision | Recall | F1 | FPR |
|---:|---:|---:|---:|---:|
| 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |

The primary timing boundary was `analysis-core`, with three warm-ups and ten
measured repetitions: 480 observations, mean 1.7159 ms/tool and mean 82.3637
ms/corpus pass in the recorded environment. These timings are reproducibility
metadata for that machine/run, not a universal performance guarantee.

### 5.1 Why it is authoritative

Before this run, the holdout had been frozen as version 1.0.1, independently
reviewed without expected labels or detector predictions, and checked for
cross-split exact overlap. The primary detector configuration was full built-in
v0.2 rules, `MEDIUM` threshold, no custom rules, and no suppressions. The
artifact records clean Git commit
`a4abee4661522ac13edb37e1b075186a2ccd7a03`, holdout hash
`c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8`,
and configuration hash
`a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1`.
It was the first preregistered prediction-producing access to that reviewed
holdout.

### 5.2 What it demonstrates

- On this 48-sample controlled synthetic/derived holdout, v0.2 detected only
  five of 24 suspicious samples.
- Six of 24 benign samples were predicted suspicious.
- The strong development result did not transfer to the independent pilot
  holdout.
- The experiment and preservation workflow can report an unfavorable result
  without deleting, relabeling, or post-hoc selecting another H0.
- The failure pattern generated specific falsifiable hypotheses for later work.

### 5.3 What it does not demonstrate

- It is not a deployment-prevalence or real-world accuracy estimate.
- It does not prove that every missed construct is malicious in reality.
- It does not prove that all rule-based approaches fail.
- It does not prove runtime MCP tools are safe or unsafe.
- It does not validate v0.3.
- It does not justify retrospectively changing the threshold, labels, or primary
  result.

The poor performance is scientifically valuable because it is an honest test of
transfer under the pilot design. Replacing it with v0.3 would erase the causal
fact that H0 failures informed the v0.3 rules.

---

## 6. Development result

The current 80-sample development/regression corpus result is:

| TP | TN | FP | FN | N |
|---:|---:|---:|---:|---:|
| 37 | 36 | 4 | 3 | 80 |

| Accuracy | Precision | Recall | F1 | FPR |
|---:|---:|---:|---:|---:|
| 91.25% | 90.24% | 92.50% | 91.36% | 10.00% |

This is useful regression evidence: it says the current detector still behaves
as expected on the project-authored development examples. It is not proof of
generalization because the examples, labels, categories, and failure modes were
visible during design. The balanced 40/40 composition is a controlled test
choice, not an estimate that half of deployed MCP tools are suspicious.

---

## 7. v0.3 exposed-holdout exploratory result

> **POST-UNBLINDING EXPLORATORY ONLY.**

Artifact:
`evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json`

Artifact SHA-256:
`d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b`

| TP | TN | FP | FN | N |
|---:|---:|---:|---:|---:|
| 11 | 18 | 6 | 13 | 48 |

| Accuracy | Precision | Recall | F1 | FPR |
|---:|---:|---:|---:|---:|
| 60.42% | 64.71% | 45.83% | 53.66% | 25.00% |

Its corresponding `analysis-core` record used the same three/ten timing plan and
reported mean 1.5531 ms/tool in that environment. Because this is a dirty,
post-unblinding exploratory run, the timing difference is descriptive and must
not be promoted to a confirmed speed improvement.

The artifact authentically records schema `3.0.0`, application `0.2.0`, built-in
pack `1.0.0`, commit `a4abee...`, `dirty=true`, the 16-rule resolved identity,
and configuration hash
`3cee3f4d1bf73637498ea876d5c26c0b8bf8bab40b6be03284fc9ec5da839323`.
Those apparently old version fields are not to be rewritten: the run occurred
from the uncommitted exploratory implementation before package/rule-pack version
corrections. Current compatibility code validates its own recorded identities.

The result cannot establish improved generalization because Day 3C exposed the
holdout predictions and failure mechanisms, and Day 4A used those mechanisms to
design v0.3. The data influenced the candidate. A defensible statement is:

> On the already exposed v1.0.1 holdout, the v0.3 exploratory candidate changed
> six v0.2 false negatives to true positives while the six false positives
> remained. This supports further investigation of specific mechanisms on known
> cases; it does not independently demonstrate improved generalization.

---

## 8. Human review state

| Review fact | Frozen record |
|---|---:|
| Samples reviewed | 48 / 48 |
| Agreements | 47 |
| Disagreements | 1 |
| Abstentions | 0 |
| Raw binary agreement | 97.9167% |
| Cohen's kappa | approximately 0.9583 |
| Reviewer totals | 25 benign / 23 suspicious |
| Original ground truth | 24 benign / 24 suspicious |
| Exact difficulty agreement | 16 / 48 |
| Independent reviewers | 1 |

The reviewer was blinded to the original expected labels and detector
predictions and reviewed static metadata. The original source is preserved at
`evaluation/holdout/reviewer-source.md`, SHA-256
`857b20b5e138e67e7f684cb3784bfb0cd97831ff4a4cefdae6b6d6128465489c`.
The source summary said 24/24, but its 48 individual decisions total 25/23. The
ledger corrects only that arithmetic summary; it does not alter an individual
judgment.

### R08

`R08` maps to `holdout_s011`, `bounded_result_sampler`. The frozen original label
was suspicious because a negative `maxItems` fell inside the preregistered
malformed-schema security-review construct. The blinded reviewer labeled it
benign, judging it more likely a data-quality/schema defect than a security
issue. Adjudication retained the original suspicious label under the already
frozen construct while preserving the reviewer label, 3/5 confidence, rationale,
and disagreement.

The correct interpretation is not “the reviewer was wrong” and not “malformed
schema proves maliciousness.” It is: **R08 is suspicious under the pilot's
broader schema-security-review taxonomy; malformed schema alone does not prove
malicious intent.**

Kappa near 0.9583 shows very high binary agreement beyond chance expected from
the observed label marginals for this one review. It does not establish label
truth, expert consensus, sample independence, detector performance, or external
validity. Difficulty agreement of only 16/48 shows that “obvious,” “moderate,”
and “subtle” are especially subjective descriptive labels.

---

## 9. Corpus inventory and permitted use

| Corpus | Identity and size | Origin/review | Exposure | Allowed use | Prohibited use |
|---|---|---|---|---|---|
| Development | `evaluation/corpus/manifest.json`; `mcpsec-synthetic-metadata` v1.0.0; 80 samples, 40 benign/40 suspicious; semantic SHA-256 `a22de0126d2cf0b00c99ded46687b70dc6f417382a0a11c5ae4a9cad8f6d6f47` | Repository-authored synthetic; single reviewer | Visible throughout detector design | Regression, debugging, rule tests, development metrics, safe engineering profiling | Independent accuracy, real-world prevalence, generalization proof |
| Independently reviewed holdout | `evaluation/holdout/manifest.json`; `mcpsec-independent-holdout-metadata` v1.0.1; 48 samples, 24 benign/24 suspicious; semantic SHA-256 `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` | Repository-authored synthetic and transparently paired-derived inert metadata; one blinded independent reviewer; one preserved disagreement | Prediction-unexposed through H0; permanently exposed after Day 3B/3C | Preserve H0, historical analysis, teaching, explicitly post-unblinding descriptive comparison, detector-free integrity checking | Fresh confirmation, tuning then claiming independent validation, silent relabeling, replacing H0 |
| v0.3 exploratory constructs | `evaluation/exploratory/v0_3/manifest.json`; `mcpsec-v0.3-construct-exploratory-development` v1.0.0; 36 samples, 18 benign/18 suspicious; semantic SHA-256 `4209b93750ac4fd1a6445af13d891fa49954e0ba5e1b939d6c52b955060fbba4` | Repository-authored after unblinding from Day 4A abstract constructs; single reviewer; statements not copied from holdout according to manifest | Exposed development data by design | Intended-mechanism regression, boundary tests, exploratory engineering | Holdout/generalization evidence, pooling with H0, “100% proves effectiveness” |

Any research-significant corpus change needs a new corpus version, documented
reason, updated changelog, new semantic hash, renewed review as appropriate, and
a clear statement about exposure. Never edit a frozen corpus in place because a
result is inconvenient.

---

## 10. Research artifact inventory

Mutability labels mean:

- **IMMUTABLE:** preserve exact bytes and hash. Derive new analysis in a new file.
- **VERSIONED:** changes are possible only as a named new version/protocol with
  new identities; never silently edit history.
- **REGENERABLE:** may be recreated from approved development inputs and a known
  checkpoint, but timing can vary. This label never authorizes treating an
  exposed-holdout rerun as confirmation.
- **DOCUMENTATION:** explanatory record; update with normal review while keeping
  historical status and numbers honest.

| Path/artifact | Purpose and scientific status | SHA-256/identity | Mutability |
|---|---|---|---|
| `evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json` | Original v0.2 H0; authoritative first confirmatory result | `3307c28d...71b80` | **IMMUTABLE** |
| `evaluation/runs/day3c-deep-failure-analysis.md` | Post-unblinding forensic analysis of H0 errors and ablations | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` | **IMMUTABLE** tracked evidence |
| `evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json` | Authentic v0.3 comparison on exposed holdout | `d5d84dc3...806b` | **IMMUTABLE** exploratory evidence |
| `evaluation/holdout/reviewer-source.md` | Original blinded reviewer report | `857b20b5...489c` | **IMMUTABLE** |
| `evaluation/holdout/review-ledger.md` | Mapping, agreement, R08 adjudication and difficulty record | Frozen with holdout 1.0.1 | **IMMUTABLE** review record; a correction needs an appended/versioned protocol |
| `evaluation/holdout/manifest.json` and holdout catalog files | Exact H0 sample population/ground truth | corpus `c514ba03...a2d8` | **IMMUTABLE** as v1.0.1; future changes require a new corpus version |
| `evaluation/holdout/integrity-report.json`, `near-duplicate-review.md`, `coverage-report.md` | Detector-free split integrity and coverage/confounding records | Bound to holdout freeze | **IMMUTABLE** for v1.0.1 |
| `docs/holdout-experiment-plan.md` | Preregistered H0 threshold, full detector, timing, outputs and post-unblinding policy | configuration `a660fd6d...f9a1` recorded by H0 | **IMMUTABLE** as H0 plan; use a new plan/version later |
| `evaluation/corpus/manifest.json` and catalogs | Development corpus | corpus `a22de012...d6f47` | **VERSIONED**; current v1.0.0 remains frozen for historical metrics |
| `evaluation/exploratory/v0_3/manifest.json` and catalogs | Post-unblinding mechanism fixtures | v1.0.0, 36 samples; corpus `4209b937...ba4` | **VERSIONED** development material |
| `evaluation/runs/day3d/` | Results tables, figure specifications, claims/discussion/viva evidence derived from H0 | No single frozen bundle hash; currently local and ignored | **DOCUMENTATION**; important continuity material, not guaranteed by Git |
| `evaluation/runs/day4a/day4a-exploratory-improvement-design.md` | Post-H0 design rationale and rejected ideas | Local and ignored | **DOCUMENTATION**; preserve separately if relied on |
| `evaluation/runs/day4b/*.json` | Development/exploratory performance and timing during implementation | Local and ignored | **REGENERABLE** from a named checkpoint for development only; exact timing is environment-specific |
| `evaluation/runs/day4c/*.md` and non-allowlisted JSON | Contribution maps, comparisons, ablations and local analyses | Local and ignored except the one tracked primary exploratory artifact | **DOCUMENTATION/REGENERABLE** exploratory; never upgrade to confirmatory |
| `evaluation/runs/day3b-artifact-inventory.json` | Local H0 run inventory | Local and ignored | **DOCUMENTATION** |
| `evaluation/runs/README.md` | Names and hashes the three tracked immutable evidence files | Tracked | **DOCUMENTATION** with evidence-integrity role |
| `docs/research-status.md` | Public scientific-status boundary | Tracked | **DOCUMENTATION** |
| `docs/reproducibility.md` | Checkpoint, evidence hashes and safe verification commands | Tracked | **DOCUMENTATION** |
| `docs/releases/v0.3.0a1.md` | Public-alpha release notes and claims boundary | Tracked | **DOCUMENTATION** |
| `docs/captain-technical-map.md` | Day 6A repository map | Current SHA-256 `c65600a4d838f0d2d6364682493f7354a27fd113b9c49ec4eb99d4e4bd923e8c`; untracked | **DOCUMENTATION**; local loss risk until intentionally archived |
| `docs/captains-manual.md` | Day 6B teaching/viva manual | Current SHA-256 `c93fabe9c020ef6826244e058f5650bcce43fde209280c53da39beaa1c470a1e`; untracked | **DOCUMENTATION**; local loss risk until intentionally archived |
| `docs/fyp-handover.md` | Day 6C research continuity guide | Currently untracked | **DOCUMENTATION**; local loss risk until intentionally archived |

The ignored Day 3D/Day 4A/Day 4B/Day 4C local bundle is useful but not guaranteed
to exist in a fresh clone. Before leaving the project for months, the student and
supervisor should decide which non-primary analyses deserve a reviewed,
versioned archive. Do not solve this by indiscriminately committing every timing
or generated run.

---

## 11. Commit and version landmarks

| Commit | Message | Repository-grounded meaning |
|---|---|---|
| `47750760f030628bbbba83e71528f2ce81cb16f0` | `chore: establish hardened FYP development baseline` | Added major input/retrieval/resource/reporting/test/build hardening before H0 |
| `7d9ab8115dfdfa349f983a643765b6d9a6a78cea` | `feat: add FYP research reproducibility foundation` | Added protocol, corpus identity/integrity, research metadata and evaluation foundations |
| `997c5fcf11a6f0800dceb022426cc32e0d522e04` | `feat: add FYP experiment engine` | Added planned experiment, timing, ablation, uncertainty, stratification and historical comparison machinery |
| `a4abee4661522ac13edb37e1b075186a2ccd7a03` | `research: freeze independently reviewed holdout` | Pre-unblinding holdout 1.0.1, review ledger/source, integrity material and experiment plan freeze |
| `b1a5d4c92797f630a5aed8b19dec3da21085fa76` | `feat: freeze v0.3 exploratory detector candidate` | Post-unblinding five-rule candidate, bounded representation helper, exploratory corpus, tests and candidate version |
| `0651313cb9fe650f3004e849de7d14000343cacf` | `fix: harden v0.3 alpha reproducibility and safety` | Day 5 remediation: historical compatibility, strict/bounded safety, output limits, immutable evidence archive and regression tests |
| `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` | `docs: prepare v0.3.0a1 alpha release` | Current release/research-status documentation checkpoint; locally tagged `v0.3.0a1` |

Do not infer scientific status from commit order alone. The H0 and Day 4C files
were committed later for preservation, but their internal timestamps, Git state,
resolved rules, hashes, and the chronology above determine their status.

---

## 12. What was learned from the H0 failure

The Day 3C report is a diagnosis, not permission to rewrite H0.

- **17 of 19 false negatives had no finding and risk 0.** Most misses were rule
  coverage/semantic interpretation gaps, not merely a threshold problem.
- **2 of 19 false negatives (`s023`, `s024`) had `CAP-001` only**, at
  INFORMATIONAL severity and risk 2, below the `MEDIUM` binary threshold.
- **Obfuscation/decoding was the largest single primary mechanism: 4 of 19 FNs.**
  Decimal codes, short Base64 in annotations, HTML entities, and hex bytes did
  not fit v0.2's narrow representation rule.
- There were **six false positives**. `SEC-001` accounted for four and `SCH-002`
  for two.
- Benign credential/security vocabulary—documentation, policy, validation,
  rotation and redaction language—was a major false-positive source.
- Instruction-priority and concealment paraphrases were often outside direct
  lexical patterns.
- Capability descriptions needed purpose/capability consistency reasoning;
  blanket capability severity was not justified.
- `SCH-001` made a real security/compatibility contribution, but R08 showed the
  construct boundary between malformed metadata and malicious poisoning.

The correct causal story is:

```text
frozen v0.2 + independent holdout
    -> low recall and six false positives
    -> post-unblinding Day 3C mechanisms
    -> bounded Day 4A hypotheses
    -> exploratory v0.3 candidate
```

It is not:

```text
v0.3 result replaces the original H0
```

---

## 13. v0.3 design rationale and remaining uncertainty

| Rule | H0 gap addressed | Design and safety principle | Current evidence | Unknown |
|---|---|---|---|---|
| `PI-002` | Indirect instruction-authority/precedence paraphrases missed by `PI-001` | Require a bounded local relationship among authority/priority, an instruction object, and a conflict target; account for local negation and educational context | Authored construct tests passed; recovered one known exposed-holdout FN | Transfer to unseen paraphrases, other languages, and distant/cross-field relations |
| `HID-002` | Concealment phrasing without direct “hide/do not tell” lexemes | Require omission action, material operation, and observer/disclosure concept in local context; preserve field paths | Authored construct tests passed; recovered one known exposed-holdout FN | Broader visibility semantics and false positives in privacy/UI language |
| `SEC-002` | `SEC-001` keyword FPs and missed active sensitive-value handling | Require sensitive term locally related to collect/access/store/send/return-like action; scoped negation/safe contexts; no global disclaimer suppression | Authored fixtures passed; recovered no exposed TP and added misleading findings to two existing benign FPs | A robust context model for security products, recovery flows, outputs, and vocabulary |
| `OBF-005` | Four encoded-representation H0 misses | Recognize four explicit textual representations, decode one layer with strict UTF-8/printability/size/count budgets, keep output inert, require a fixed high-risk semantic gate | Strong boundary and authored construct tests; recovered zero exposed encoded cases | Unseen representation distribution, semantics outside fixed gates, useful coverage without recursive risk |
| `MIS-002` | Undeclared/contradictory high-impact capability, including two `CAP-001`-only cases | Require structured capability plus unaligned purpose and an independent corroborator; use stable paths; avoid one-signal escalation | Authored fixtures passed; recovered four known exposed FNs | Vocabulary completeness and false positives for legitimate broad/admin tools |

### Why `CAP-002` was deferred

`CAP-001` intentionally remains INFORMATIONAL because a powerful declared
capability can be legitimate. Day 4A considered a `CAP-002` for corroborated
high-impact capability where purpose is unclear rather than explicitly
contradictory, but classified it P1/high false-positive risk. It was not
registered because its design and hard-negative suite were not approved.
`MIS-002` was the bounded P0 route: capability becomes binary-relevant only with
purpose contradiction and corroboration. Future work must not create `CAP-002`
as a blanket promotion or simply lower the global threshold.

---

## 14. What v0.3 did not solve

> **Thirteen exposed suspicious samples still had no finding. All six original
> false positives remained.**

- `SEC-002` added misleading findings to two already false-positive benign
  samples (`b012` and `b020`).
- Scoped credential handling did not resolve the exposed sensitive-data hard
  negatives.
- `OBF-005` recovered zero exposed encoded holdout cases.
- `SEC-002` recovered no true positive on that exposed comparison.
- Better point estimates came from one recovery each by `PI-002`/`HID-002` and
  four by `MIS-002`; this is concentrated, not broad proof of semantic coverage.
- Fixed lexical/context grammars remain bypassable through unseen paraphrases,
  non-English metadata, unsupported representations, and relationships outside
  bounded windows.

These are useful future research clues. They suggest studying construct
definition, contextual security vocabulary, purpose/capability representation,
field-aware schema meaning, and independent data design. They do not authorize
memorizing the 13 known failures or adding holdout-sentence regexes.

---

## 15. Formal FYP resumption protocol: the first week

This sequence intentionally ends with an approved plan, not a new holdout run.
The supervisor may reject or substantially change the pilot methodology.

### Day 1 — Verify repository and reconstruct the environment

1. Obtain the repository from the known remote or a verified local archive.
2. Confirm the Git root, current commit, branches, tags, and worktree state.
3. Compare the expected checkpoint and immutable artifact hashes in this guide
   with the files actually present.
4. Create a new Python 3.12+ virtual environment and install development
   dependencies from `pyproject.toml`.
5. Do **not** run `evaluate` or `scan` on `evaluation/holdout/`.
6. Record any missing untracked Day 6 documents or ignored local analyses before
   doing other work.

Decision gate: if H0, holdout, or reviewer hashes disagree, stop research work
and follow the disaster-recovery section. Do not “repair” an identity by updating
the documented hash.

### Day 2 — Relearn the system and evidence

Read, in order:

1. `README.md` and `docs/research-status.md` for public scope and status.
2. `docs/fyp-handover.md` for continuity and next steps.
3. `docs/captain-technical-map.md` for module/evidence locations.
4. Relevant chapters of `docs/captains-manual.md`, especially the scan pipeline,
   detectors, risk, research method, H0, v0.3, testing, and claims.
5. The authoritative files: `docs/research-protocol.md`,
   `docs/holdout-experiment-plan.md`, `evaluation/runs/README.md`, H0 JSON, Day
   3C report, review ledger, and v0.3 checkpoint.

At the end, explain aloud: the system boundary, 16 rules, H0 matrix, why v0.3 is
exploratory, and why a fresh holdout is required. If this cannot be done without
notes, continue studying before modifying code.

### Day 3 — Reproduce safe development checks

Run ordinary engineering gates and only declared development evaluation. Review
tests/commands before execution if the repository has changed since this guide.

```powershell
ruff check .
ruff format --check .
mypy src
python -m pytest --cov=mcpsec --cov-report=term-missing
python -m build
python scripts/smoke_wheel.py dist/<wheel-file>.whl

# Development/regression corpus only:
mcpsec evaluate evaluation/corpus/manifest.json --format json --runs-dir evaluation/runs

# Harmless static demo input:
mcpsec scan examples/mixed_tools.json
```

Generated runs are ignored by default. Name and record the source commit and
dirty state before interpreting any development change. Do not present a newly
generated development result as evidence that the historical checkpoint was
exactly reproduced unless dependencies and environment are also comparable.

### Day 4 — Methodology review with the supervisor

Bring the supervisor discussion pack below. Present the unfavorable H0 first,
then the exploratory v0.3 result and limitations. Ask whether the FYP should:

- retain a deterministic static-rule detector as the primary intervention;
- compare v0.2 and a frozen revised version on the same fresh samples;
- include or exclude LLM/learned baselines;
- focus on effectiveness, drift integrity, safe design, or a narrower construct;
- use balanced classes or estimated deployment prevalence;
- require multiple reviewers and what adjudication method to use; and
- define an acceptable FPR, recall target, latency boundary, and uncertainty
  analysis before seeing new outcomes.

Document decisions, unresolved questions, and required institutional/ethical or
data/licensing review. Do not assume that the existing pilot plan is automatically
the formal methodology.

### Day 5 — Freeze the approved formal research plan

Only after supervisor feedback:

1. Write a new versioned protocol and research question.
2. Define the detector candidate and comparison conditions.
3. Freeze stable rule IDs, rule-pack version, risk model, binary threshold,
   suppressions/custom rules, canonicalization, timing boundaries, metrics, and
   analysis plan.
4. Justify sample design and reviewer count; do not choose them merely because
   they are convenient.
5. Define leakage controls, authorship separation, blinding, adjudication, and
   what happens after the single primary run.
6. Commit a clean code/protocol checkpoint and record its SHA.
7. Obtain supervisor sign-off **before** fresh holdout construction exposes any
   predictions to authors or detector developers.

The first week succeeds when the formal plan is approved and frozen—not when a
new favorable metric is produced.

---

## 16. Supervisor discussion pack

| Topic to bring | Concise position | Why supervisor input is needed |
|---|---|---|
| Existing prototype | A safe static inspector, drift system, CLI and evaluation framework already exist | Decide whether engineering scope is sufficient or should be narrowed/expanded for FYP outcomes |
| Pilot status | This is pre-FYP pilot work, not a completed thesis | Agree how prior work may be incorporated, disclosed and credited under university rules |
| v0.2 H0 | First frozen holdout result: recall 20.83%, F1 28.57%, FPR 25% | Decide how the negative result frames the formal motivation and baseline |
| v0.3 candidate | Five post-unblinding rules improved known-case point estimates but did not remove FPs | Decide whether v0.3, a further revised candidate, or another comparison is the formal intervention |
| Exposed holdout | The old 48 samples cannot confirm any detector informed by Day 3 failures | Approve the independence/leakage rules and need for genuinely untouched data |
| Fresh confirmation design | Freeze first, preregister, independently author/review, hash, run once | Approve the protocol and determine whether it is feasible within FYP time/resources |
| Synthetic-heavy evidence | Existing corpora are safe and controllable but not real-world representative | Decide whether licensed real metadata, expert-authored scenarios, or both are required |
| Human review | One blinded reviewer gave high binary agreement but is not consensus | Choose reviewer qualifications/count, training, disagreement handling and reporting |
| Label construct | R08 shows “suspicious security-review metadata” is broader than malicious poisoning | Refine the target construct and labeling rubric before formal data creation |
| Metrics | Accuracy is prevalence-sensitive; recall, precision, F1, FPR and intervals all matter | Preregister primary/secondary metrics and what “acceptable” means |
| Statistical design | N=48 and tiny strata produced wide uncertainty | Obtain sample-size/precision/power guidance and select comparison tests appropriately |
| Timing | Analysis-core and static-end-to-end answer different questions | Approve boundary, warm-ups, repetitions, hardware control and reporting |
| Method retained or changed | Rules offer explainability but poor semantic transfer; alternatives change scope | Decide whether the study is improvement, comparison, feasibility, or design research |
| Scope boundaries | Static metadata only; no tool invocation, remote crawling, or runtime sandboxing | Keep the FYP achievable and ethically/safely bounded |
| Thesis framing | Strongest current contributions are safe engineering, reproducibility and honest negative evidence | Decide the primary contribution and chapter emphasis rather than over-selling accuracy |
| Publication/release status | Local refs show `v0.3.0a1` and `origin/main` at HEAD, but no Day 6C network verification occurred | Decide archive/release expectations, authorship and preservation before formal submission |

Prepare a one-page meeting summary containing the H0 matrix, the v0.3 status
warning, corpus table, candidate question, and the decisions requested. Do not
lead with the favorable development number.

---

## 17. Candidate future research question

Repository evidence supports discussing, but not yet declaring, a question such
as:

> **Candidate for supervisor approval:** Does a frozen revised lightweight
> rule-based detector improve detection of previously unseen MCP
> tool-metadata-security constructs, relative to the frozen v0.2 baseline, while
> maintaining a supervisor-defined acceptable false-positive rate and processing
> latency?

“Generalize better” is conceptually appropriate but must be operationalized. It
cannot mean merely scoring higher on the exposed holdout. “Acceptable” also
requires a threshold defined before the results are seen.

### 17.1 Candidate variables

| Element | Candidate operationalization | Decision needed |
|---|---|---|
| Independent variable | Frozen detector configuration/version: historical v0.2 baseline versus one preregistered revised candidate | Whether comparison is paired on the same fresh sample set and whether current v0.3 is the candidate |
| Primary dependent variable | Recall or F1 on suspicious samples, chosen before evaluation | Which is primary and what minimum meaningful difference is relevant |
| Safety dependent variable | False-positive rate among benign samples | Maximum acceptable FPR and interval width |
| Other effectiveness outcomes | TP/TN/FP/FN, precision, accuracy, specificity, FN rate, category/field/difficulty strata | Which are secondary/exploratory and multiplicity handling |
| Efficiency outcome | Analysis-core latency; optionally static-end-to-end latency | Boundary, hardware controls, repetitions and summary statistic |
| Explanatory outcomes | Rule/family contributions and failure taxonomy after unblinding | Keep secondary; do not choose the primary configuration from these results |

### 17.2 Controls

- The exact same fresh sample population and labels for a paired version
  comparison, if approved.
- One frozen binary threshold per preregistered condition; `MEDIUM` is the pilot
  default but is not automatically the formal choice.
- No unplanned custom rules or suppressions.
- Recorded rule-pack, code commit, dirty state, configuration hash and corpus
  hash.
- Identical loading/normalization/reporting path and timing boundary.
- Same machine, power mode and background-load policy for latency.
- Blinded review and authorship/leakage controls established before predictions.
- One primary run, with post-run analyses labeled as such.

### 17.3 Principal threats

Synthetic sample realism, rule-author knowledge, label ambiguity, English-only
lexicons, matched-pair dependence, balanced prevalence, small category strata,
reviewer count, multiple metric selection, environment-dependent latency, and
overfitting to abstract constructs inferred from the old holdout all threaten the
candidate question. These must be handled in the protocol, not hidden in the
discussion after results appear.

---

## 18. Future confirmatory experiment blueprint — design only

> **Do not create a corpus or run this blueprint until it is approved.**

### Phase A — Approve construct and protocol

1. Define the target: malicious tool poisoning, suspicious metadata requiring
   review, schema-security defects, or an explicitly partitioned combination.
   R08 shows why this distinction matters.
2. Select the formal comparison and primary estimand: absolute revised-detector
   performance, paired difference from v0.2, or both.
3. Justify sample size, prevalence, categories, provenance, languages, and
   reviewer count.
4. Preregister inclusion/exclusion, abstention, adjudication, leakage, metric,
   uncertainty, timing, ablation, and stopping rules.

### Phase B — Freeze the detector before holdout work

1. Complete all detector changes on development material only.
2. Add suspicious cases and benign hard negatives for every correctness change.
3. Run lint, typing, coverage, build, installed-wheel smoke, resource-boundary
   tests and declared development evaluation.
4. Freeze package/rule-pack versions, exact 16-or-later rule set, threshold,
   severities, risk model, custom/suppression state, canonicalization and
   evaluation schema at a clean Git commit.
5. Generate and preserve a semantic configuration hash without any holdout
   predictions.

### Phase C — Construct genuinely untouched evidence

1. Use authors who have not inspected detector regex/predictions where feasible,
   or document unavoidable overlap and add independent external sources.
2. Do not copy, paraphrase, or systematically mutate the exposed 48 holdout
   sentences. Abstract category rubrics may only be used as allowed by the
   approved protocol; known failure wording must not become the new test.
3. Separate sample authorship, original labeling, and independent review roles
   where feasible.
4. Record origin, licensing/redistribution, derivation, category, field path and
   rationale without secrets, private data, or operational exploit content.
5. Run only detector-free validation: strict manifest parsing, totals, duplicate
   IDs, exact canonical overlap, normalized-content overlap and documented manual
   near-duplicate review.
6. Freeze a corpus version and semantic SHA-256 before any prediction-producing
   access.

### Phase D — Blinded independent review

1. Give reviewer(s) randomized inert samples and a frozen rubric, without
   original labels, detector output, rule IDs, or expected findings.
2. Record classification, categories, exact field paths, confidence, difficulty,
   rationale and abstention.
3. Calculate agreement only after all judgments are locked.
4. Adjudicate disagreements under a written rule; preserve original and reviewer
   judgments rather than overwriting them.
5. If adjudication changes ground truth, issue a new corpus version/hash before
   detector execution and document who decided and why.

### Phase E — Pre-run gate

Verify a clean repository, exact detector commit, frozen corpus/config hashes,
no prediction artifacts, supported environment, artifact destination, metadata
recording, preregistered commands and a signed supervisor gate. If any critical
identity fails, do not run.

### Phase F — One primary evaluation

1. Run the exact preregistered command once against the new holdout.
2. Preserve the raw JSON bytes immediately in a non-normalizing archive.
3. Calculate and record its file hash.
4. Do not rerun merely because performance is poor.
5. If a genuine technical failure invalidates the run, preserve the failed run,
   document the failure and obtain protocol-level authorization before any
   replacement; do not silently select the best artifact.

### Phase G — Analysis after freeze

Report the full confusion matrix, preregistered metrics, Wilson or other approved
intervals, stratum denominators, timing methodology, provenance and limitations.
Only after preserving the primary result should predictions, errors and planned
ablations be inspected. Any new detector change begins a new post-unblinding
development lineage and requires yet another untouched holdout for confirmation.

### Leakage controls specific to this repository

- Treat `evaluation/holdout/`, H0 sample predictions, Day 3C, Day 4A and Day 4C
  as exposed design information.
- Do not use old holdout IDs, names, phrases, matched pairs, exact field layouts,
  or known bypass transformations as templates for the new test set.
- Keep future holdout content outside ordinary detector-debugging paths and
  developer IDE/search scope where feasible.
- Do not run broad tests that automatically scan the new holdout.
- Record every person who can access labels, metadata and predictions.
- Keep a blinded reviewer package separate from expected labels and detector
  output.
- Archive a detector-free cross-split leakage report before unblinding.

---

## 19. Sample-size and statistics questions for the supervisor

No statistically justified future sample size can be inferred merely from the
pilot's convenient N=48. Resolve these questions before deciding N:

1. What is the primary estimand: revised recall, FPR, F1, or paired change from
   v0.2?
2. What minimum effect or precision would be educationally/research relevant?
3. How narrow should the 95% interval be for recall and FPR?
4. Will the corpus remain balanced for controlled evaluation, approximate a
   realistic prevalence, or report both through stratified/reweighted analysis?
5. How many suspicious samples are needed in each target category to avoid
   meaningless 3–6-sample percentages?
6. How should matched or paired samples be analyzed without assuming all items
   are independent?
7. If v0.2 and revised predictions are paired on each sample, should a paired
   test such as McNemar's method be used, and what assumptions/discordant-pair
   count are required?
8. If data sources/authors differ, is an independent comparison more defensible?
9. How will multiple metrics, strata and ablations be separated into primary,
   secondary and exploratory analyses?
10. How many independent reviewers are feasible, and is agreement with the
    original author the right statistic versus inter-reviewer agreement?
11. How are abstentions, “uncertain,” and construct-boundary cases handled?
12. Are Wilson intervals sufficient for binomial proportions, and how should
    paired differences be interval-estimated?
13. What latency quantity matters: median, mean, tail percentile, throughput, or
    total catalog time?
14. How many warm-ups and repetitions are justified, and how will autocorrelation,
    caching, thermal state and background load be controlled?
15. Should a small pilot of the *data-collection procedure* be allowed without
    exposing the eventual confirmatory samples?

These decisions require methodological justification because changing N,
prevalence, primary metric, or comparison after seeing predictions can bias the
conclusion. A statistician or methods adviser should review the plan if
available.

---

## 20. FYP-quality threats to validity

### 20.1 Construct validity

| Threat | Why it matters | Current mitigation | Future mitigation |
|---|---|---|---|
| “Suspicious metadata” versus malicious tool poisoning | A rule may correctly flag a schema/security concern without proving hostile intent; R08 demonstrates this | Claims and R08 disagreement are preserved; rules emit review findings | Refine/partition constructs, publish the rubric, include intent-agnostic security-quality labels where appropriate |
| Rule/label circularity | Samples authored from expected rules can make detection tautological | Development and exploratory fixtures are explicitly labeled, kept separate from H0 | Independent authorship, abstract construct rubric, blinded review, and unseen linguistic/structural variation |
| Proxy vocabulary | Terms such as password, admin, token or hidden may proxy the label instead of the intended relation | Benign hard negatives and contextual v0.3 rules | Expand domain-realistic hard negatives and perform feature/lexicon confounding audits before freeze |
| Difficulty labels | “Obvious/moderate/subtle” had only 16/48 exact agreement | Original and reviewer difficulty kept separately | Use operational definitions, multiple reviewers, or treat difficulty as descriptive/exploratory only |
| Static metadata scope | Runtime behavior, server implementation and host policy are not observed | Scope is explicit; tools are never invoked | Frame conclusions as metadata inspection; create a separately approved runtime study if needed |
| Regex/context representation | Fixed patterns approximate semantics and are bypassable | Explainable bounded grammar and negative tests | Compare alternative representations under a new protocol; report bypass tests without claiming completeness |

### 20.2 Internal validity

| Threat | Why it matters | Current mitigation | Future mitigation |
|---|---|---|---|
| Post-unblinding detector changes | Known H0 failures influenced v0.3, invalidating reuse for confirmation | v0.3 is prominently exploratory; H0 retained | New untouched holdout after detector freeze |
| Exposed holdout leakage | Old phrases/layouts could enter future tests or rules | Post-unblinding policy and hashes documented | Separate authors/reviewers, access log, no copying, detector-free leakage audit |
| Researcher is developer/label author | Expectations can influence implementation and labels | Independent single reviewer and transparent provenance | Role separation, multiple reviewers, supervisor-approved rubric and adjudication |
| Configuration drift | Threshold/rules/suppressions can change outcomes | Semantic configuration hash, stable IDs and artifact metadata | Clean preregistered commit, exact command, automated pre-run gate |
| Parser/canonicalization drift | Same bytes could be interpreted differently over versions | Strict parsing, schema version and canonical hashes | Version canonicalization/parser identity and test old fixtures at freeze |
| Test execution accidentally evaluates holdout | Predictions may leak before the gate | Holdout access policy; deliberate experiment CLI | Keep fresh holdout out of broad test discovery; audit tests before run |
| Artifact selection | Repeating until a favorable run creates hidden researcher degrees of freedom | Original H0 preserved; one-run policy | Predefine failure/retry rules and preserve every attempted artifact |

### 20.3 External validity

| Threat | Why it matters | Current mitigation | Future mitigation |
|---|---|---|---|
| Synthetic-heavy corpora | Authored examples may be cleaner and more rule-shaped than real metadata | No real-world claim; provenance declared | Add legally redistributable real or independently derived metadata, with privacy/license review |
| No real-world holdout samples | Deployment distributions, vendor styles and noise are absent | Explicit limitation | Supervisor-approved mixed-source untouched holdout |
| English orientation | Fixed English lexicons may fail on multilingual metadata | Limitation documented | Multilingual research question/corpus or explicit English-only scope |
| Balanced 50% suspicious prevalence | Precision/accuracy differ under deployment prevalence | Raw confusion counts and FPR reported | Report prevalence-specific scenarios or representative sampling; keep sensitivity/specificity separate |
| Small category/field strata | A percentage from 3–6 samples is unstable | Denominators and Wilson intervals retained | Larger justified strata or avoid inferential stratum claims |
| Matched-pair dependence | Treating paired variants as independent exaggerates effective evidence | Matched construction disclosed | Use cluster/paired analysis and more independent sources |
| Description-length/provenance confounding | Detector may exploit superficial author/source differences | Coverage and confounding review exists | Match/measure length and source, diversify authors, perform preregistered confound checks |
| MCP evolution | Tool fields/annotations/transport behavior may change | Unknown fields preserved; static scope versioned | Pin MCP/spec version in the formal study and review current standard before protocol freeze |

### 20.4 Conclusion validity

| Threat | Why it matters | Current mitigation | Future mitigation |
|---|---|---|---|
| Small N and wide intervals | H0 point estimates may look more precise than they are | Wilson intervals in artifacts/manual | Power/precision planning and raw denominators |
| Multiple outcomes/ablations | Selecting the best metric or family after results inflates claims | Primary full configuration preregistered; ablations secondary | Name one primary outcome and control/label multiplicity |
| Zero-denominator metrics | Precision or stratum metrics may be undefined | Typed metric handling | Predefine reporting conventions; never convert undefined to favorable zero/one |
| Timing noise | Machine/background load can dominate small latency differences | Boundary/runtime metadata and comparability checks | Fixed hardware/power/load, repetitions, robust summaries, environment record |
| Historical incompatibility | Comparing different schemas/rule packs as if identical can misattribute change | Loader validates recorded rule sets and warns/rejects incompatibility | Freeze comparison contract and interpret provenance warnings |
| Practical versus statistical significance | A numerical increase may still leave unacceptable recall/FPR | Full confusion matrix and limitations | Predefine minimum practical thresholds and report both effect/uncertainty |

---

## 21. Claims register for future writing

### 21.1 Safe to claim

- “The project implements deterministic defensive static analysis of MCP tool
  metadata and does not invoke scanned tools.”
- “The current alpha has seven detector families and 16 stable built-in rule
  identities.”
- “The project supports bounded hostile-input handling, inert reporting,
  canonical fingerprints, baselines/drift, and reproducible evaluation
  artifacts.”
- “The 80-sample development corpus result is TP 37, TN 36, FP 4, FN 3.”
- “The authoritative v0.2 H0 result on the 48-sample pilot holdout is TP 5,
  TN 18, FP 6, FN 19.”
- “The first pilot holdout revealed a substantial transfer/generalization gap
  relative to development data.”
- “Seventeen of 19 H0 false negatives produced no finding.”
- “Five v0.3 rules were designed after H0 unblinding.”
- “The exposed-holdout v0.3 comparison is post-unblinding exploratory.”
- “A fresh untouched holdout is required for a new confirmatory claim.”

### 21.2 Claim with qualification

| Qualified claim | Required qualification |
|---|---|
| “The detector finds tool-poisoning indicators.” | It finds fixed suspicious metadata constructs for review; a finding does not prove malicious intent or runtime compromise |
| “H0 is confirmatory.” | It is the first preregistered result for this controlled synthetic/derived pilot holdout, not universal or deployment confirmation |
| “Independent review supports the labels.” | One blinded reviewer agreed on 47/48 binary labels; this is not multi-expert consensus or proof of truth |
| “v0.3 improved performance.” | It improved point estimates on authored development mechanisms and the already exposed holdout; generalization remains unconfirmed |
| “Schema validation contributes to security.” | Invalid/inconsistent schemas are security/compatibility signals; malformed schema alone is not malicious poisoning |
| “The system is reproducible.” | Code/corpus/config/artifact identities and commands are recorded; exact timing still depends on environment, and local ignored analyses need archival decisions |
| “The prototype is secure by design.” | It enforces important boundaries and was tested; it is an alpha prototype with bypass and implementation risk, not a certification |
| “The project is an FYP foundation.” | It is pre-FYP pilot work; final scope/methodology/evidence need supervisor approval |

### 21.3 Do not claim; use the correction

| Dangerous claim | Correct wording |
|---|---|
| “v0.3 generalizes better.” | “v0.3 scored better on known post-unblinding cases; a new untouched holdout is needed to test generalization.” |
| “The detector detects MCP tool poisoning reliably.” | “The prototype deterministically flags selected metadata constructs, but H0 recall was 20.83% and FPR 25% on the pilot holdout.” |
| “The detector is production ready.” | “`0.3.0a1` is a defensive alpha/research prototype with documented limitations.” |
| “91.25% development accuracy proves effectiveness.” | “91.25% is regression performance on visible development data and does not prove transfer.” |
| “47.92% is real-world accuracy.” | “47.92% is accuracy on a balanced 48-sample synthetic/derived pilot holdout.” |
| “The holdout represents real-world prevalence.” | “The 24/24 balance was a controlled design choice, not a prevalence estimate.” |
| “Kappa 0.9583 proves 95.83% label accuracy.” | “Kappa indicates very high agreement beyond chance with one reviewer; it does not establish label truth.” |
| “R08 proves a malicious tool.” | “R08 is a malformed-schema security-review construct; malicious intent is not established.” |
| “Tests prove there are no vulnerabilities.” | “The release gates exercise many correctness/security boundaries; residual defects and bypasses remain possible.” |
| “The rules cannot be bypassed.” | “The rules are bounded and explainable but can miss new phrasing, languages, structures and representations.” |
| “Lowering the threshold fixes recall.” | “Seventeen of 19 H0 FNs had no finding, so threshold-only change cannot address the main gap; any threshold change also needs new configuration identity and confirmation.” |
| “OBF-005 solves obfuscation.” | “OBF-005 safely handles four one-layer formats on authored fixtures; it recovered no exposed encoded holdout case and intentionally rejects broader decoding.” |
| “All metadata findings are attacks.” | “Findings are triage indicators; benign documentation, admin tools, privacy language and malformed data can trigger review.” |
| “The project is my completed FYP.” | “The project is a pre-FYP prototype/pilot that provides engineering and methodological groundwork for a supervisor-approved FYP.” |

---

## 22. Potential thesis mapping

This is a planning map, not thesis text.

| Chapter | Already available | Needs formal FYP work | Needs supervisor approval | Missing evidence |
|---|---|---|---|---|
| **1 — Introduction** | MCP metadata trust-boundary problem, tool-poisoning motivation, static-inspection scope, pilot limitations | Current problem statement, objectives, scope, contributions and terminology aligned to final question | Final research question, objectives and contribution framing | Evidence that the final problem/scope is academically appropriate and current |
| **2 — Literature Review** | Repository suggests key topics and design tradeoffs | Systematic search, inclusion/exclusion method, critical synthesis, comparison with prior MCP/agent/security/static-analysis work | Review breadth, databases, date range, quality method | Credible cited evidence; the repository intentionally contains no complete literature review |
| **3 — Methodology** | Pilot protocol, split rules, hashing, blinded review, H0 plan, metrics, timing, uncertainty, artifact schema | New formal protocol, sample-size rationale, construct definition, data provenance, reviewer plan, statistical comparison and ethical/licensing handling | Every major design choice and preregistration | Genuinely untouched corpus and approved analysis plan |
| **4 — System Design and Implementation** | Architecture, threat model, 16 rules, risk, canonicalization, baselines, resource/output safety, evaluation engine, tests | Update diagrams/traceability for the frozen formal detector; justify any approved changes | Whether current v0.3 or another candidate is in scope | Evidence for changes made after this checkpoint and final test verification |
| **5 — Results and Discussion** | Development results, authoritative H0, Day 3C, exploratory v0.3, threats and claims discipline | Present historical pilot separately; analyze future primary result once; compare according to preregistration; discuss uncertainty and failure cases | Which historical results belong in thesis and whether called pilot/baseline | Fresh confirmatory result; justified statistical comparison; external-validity evidence |
| **6 — Conclusion/Future Work** | Honest contribution and limitation candidates | Answer the approved question without overreach; distinguish engineering, effectiveness and generalization | Final contribution wording and recommendations | Depends on the formal study outcome; must not be prewritten as success |

The pilot's strongest possible role is not to be hidden. It can motivate the
formal study, document why the detector was revised, and provide a historical
baseline. The formal results chapter must keep the pilot H0, post-unblinding
v0.3 comparison, and future confirmation in separately labeled evidence blocks.

---

## 23. Literature-review gaps and search questions

The repository establishes engineering choices and pilot observations; it does
not provide a complete scholarly literature review. Do not invent citations.
Search and critically synthesize at least these topics:

### MCP and agent trust

- What security assumptions do current MCP specifications make about hosts,
  clients, servers, tool discovery, annotations and user consent?
- Which MCP metadata fields can influence host UI, model-visible context, tool
  selection or authorization decisions?
- How have MCP security guidance and specification versions changed since this
  `0.3.0a1` checkpoint?
- What responsibility belongs to host, client, server, publisher and user?
- How do other tool/plugin protocols authenticate publishers and maintain
  metadata integrity?

### Tool poisoning and prompt injection

- How is tool poisoning defined relative to direct and indirect prompt
  injection, supply-chain compromise and malicious plugins?
- What real incidents or peer-reviewed demonstrations involve adversarial tool
  metadata rather than only untrusted document content?
- What threat actors, access paths and consequences are empirically supported?
- How do systems prevent untrusted metadata from being treated as high-priority
  instructions?

### Static and rule-based security analysis

- When do deterministic rules outperform or complement learned classifiers?
- What are established techniques for lexical/contextual rule evaluation,
  taint-like metadata traversal, schema linting and cross-field consistency?
- How should false positives, bypassability and rule maintenance be measured?
- What explainability and reproducibility advantages justify fixed rules?
- What hybrid architectures keep an LLM or semantic model outside the trusted
  decision path, and how are their privacy/cost/drift risks evaluated?

### Schema integrity and drift

- How are canonical JSON, Unicode normalization and semantic hashes used in
  software supply-chain/configuration integrity?
- What changes should component fingerprints detect, and which harmless
  reorderings should be equivalent?
- What techniques exist for signed catalogs, provenance, transparency logs and
  baseline attestation?
- How reliable is rename inference when only component hashes are available?

### Adversarial metadata and representation

- Which Unicode controls, encodings, nested schemas and vendor extensions create
  interpretation differentials in agents or UIs?
- How do security tools bound decoding without allowing resource exhaustion or
  excessive false positives?
- What multilingual/paraphrase datasets are appropriate for metadata-security
  evaluation?

### Evaluation methodology

- What is accepted practice for training/development/holdout isolation in
  security detectors?
- How should post-unblinding detector revisions be validated?
- How should synthetic security corpora be constructed and their realism tested?
- Which sample-size, interval and paired-comparison methods suit binary detector
  results with small strata/matched data?
- How many reviewers and what agreement/adjudication process are defensible for
  subjective security labels?
- How should latency be benchmarked for static analyzers?

For every source, record publication type, date, threat model, dataset,
comparator, outcomes, limitations and relevance to the exact proposed FYP. Avoid
a literature chapter that is only a glossary of MCP and prompt injection.

---

## 24. Conservative future engineering backlog — do not implement automatically

Every detector change below is development work. If made before the formal
confirmatory run, it must finish before detector freeze and receive a new
rule-pack/configuration identity. If made after the run, it begins a new
post-unblinding lineage.

### P0 — required before a future confirmatory experiment

1. **Supervisor-approved construct and question.** Decide what “suspicious” means
   and whether schema quality is a separate outcome.
2. **Select one detector candidate.** Decide whether current `0.3.0a1` is frozen
   as-is or whether limited development changes are justified. Do not keep
   changing it during holdout preparation.
3. **Freeze identities.** Clean commit, package/rule-pack version, stable rules,
   threshold, severities, risk, canonicalization, custom/suppression state,
   artifact schema and semantic configuration hash.
4. **Complete release gates.** Ruff, formatting, strict mypy, full coverage,
   build, installed-wheel smoke, deterministic development evaluation and
   boundary tests.
5. **Approve data plan.** Sample-size rationale, prevalence/classes, categories,
   source/licensing, English/multilingual scope, authorship separation and exact
   leakage rules.
6. **Approve human-review plan.** Reviewer count/qualification, blinding package,
   rubric, confidence/abstention, agreement and adjudication.
7. **Create a future-holdout gate.** Detector-free integrity, corpus hash,
   configuration hash, pre-run blindness audit, exact commands, artifact
   destination and one-run/retry policy.
8. **Archive continuity material.** Decide which currently untracked/ignored Day
   6 and secondary research documents need a reviewed versioned backup before
   relying on them.

### P1 — strong FYP engineering/research improvements, if they serve the question

- Investigate context-aware `SCH-002` handling with legitimate administrative
  schema hard negatives; keep malformed-schema reporting scientifically
  distinct from malicious intent.
- Study sensitive-data action/context modeling using diverse development
  examples, especially recovery, documentation, redaction, password managers,
  outputs and vendor fields.
- Review `MIS-002` purpose vocabulary and false positives on legitimate broad
  orchestration/admin tools without memorizing old holdout cases.
- Consider `CAP-002` only through a separate approved design and extensive benign
  counterexamples; never blanket-promote `CAP-001`.
- Add independently authored development constructs, including realistic style,
  field placement and negative examples, before freeze.
- Add a safe documented future-holdout access gate that prevents accidental
  broad-test discovery, without hiding history or weakening developer access
  controls.
- Improve experiment archive manifests and external backup instructions so
  selected ignored analyses are not silently lost.
- Produce a traceability matrix from research construct to rule, test, corpus
  stratum, metric and threat to validity.

### P2 — useful future work

- Multilingual metadata and locale-aware evaluation.
- Legally redistributable real-world catalog sampling and provenance study.
- Multiple independent reviewers or expert-panel comparison.
- Signed baseline/catalog envelopes and publisher provenance.
- Longitudinal drift evaluation across versioned MCP catalogs.
- Separately scoped comparison with learned/LLM/hybrid classifiers, including
  privacy, cost, prompt-injection and model-drift controls.
- CI support for detector-free corpus integrity and development experiments,
  while keeping fresh holdout predictions outside ordinary CI.
- Broader static semantics for outputs, vendor extensions and host-policy
  annotations, if current MCP specifications justify them.

### Rejected or out of scope unless the formal research question changes

- Reusing the exposed holdout as fresh validation.
- Relabeling R08 or deleting difficult samples to improve metrics.
- Copying known holdout phrases into rules or a new test corpus.
- Globally lowering the threshold after seeing results.
- Blanket promotion of capability findings.
- Unbounded, recursive, arbitrary codec/decompression handling.
- User-controlled regex, executable rule expressions, imports or templates.
- Invoking scanned tools, starting supplied commands, or runtime exploitation.
- Fetching icons or metadata-linked remote content.
- General remote crawling, redirects, environment proxies, or authenticated
  server discovery under the static inspector's scope.
- Sending private tool catalogs to an LLM as an undocumented classifier.
- Treating every attractive feature idea as necessary for an undergraduate FYP.

---

## 25. DO NOT MODIFY WITHOUT A NEW VERSIONED PROTOCOL

The following scientific assets are protected. “New protocol” means a written
reason, new version/identity, approved analysis role, tests, changelog and—where
effectiveness is claimed—a new untouched evaluation. It never means overwriting
the old bytes.

| Protected asset | Why it is protected | Required future treatment |
|---|---|---|
| H0 JSON and hash | It is the unique authoritative first confirmatory result | Preserve byte-for-byte; create separate derived analysis |
| Holdout 1.0.1 samples and labels | They define the exact H0 population and have been exposed | Never edit in place; any correction becomes a new corpus version and cannot restore blindness |
| Reviewer source, ledger and R08 adjudication | They preserve blinding, disagreement and construct ambiguity | Append/version corrections; keep original judgments visible |
| Corpus and artifact hashes | They detect identity change | Investigate mismatch; do not update expected hash to fit altered data |
| H0 `MEDIUM` threshold | Selected before H0; changing it after results is post-hoc | Preserve H0; a new threshold gets a new configuration hash and fresh validation |
| Risk model | Aggregate findings/risk and historical outputs depend on it | Version semantics and rule pack/config; keep old artifact interpretation intact |
| Rule identities, severities and resolved registry | They define experimental treatment and finding meaning | Stable IDs for stable semantics; new/changed semantics require versioning and tests |
| Canonicalization/normalization | Tool, component, corpus and configuration identities depend on deterministic interpretation | Version and migration analysis; do not silently change old hashes |
| H0 configuration identity `a660fd6d...f9a1` | Links threshold, full rule set, no custom rules/suppressions and timing | Never recalculate it from current rules; preserve recorded v0.2 configuration |
| Experiment artifact schemas `3.0.0`/`3.1.0` | Historical artifacts must remain self-describing | Add a new schema version; do not rewrite old artifacts as current |
| Tracked Day 3C and Day 4C evidence | Records post-unblinding reasoning and authentic dirty-state provenance | Derive new notes separately; preserve hashes |

Changes to code can be legitimate. The rule is that old evidence keeps its old
identity and scientific status. A revised detector is a new candidate, not a
retrospective correction to H0.

---

## 26. Disaster scenarios and recovery decision trees

### 26.1 Local repository is lost

```text
Can the known remote be reached?
  yes -> clone it -> fetch tags -> verify HEAD/tag -> verify three evidence hashes
        -> identify missing untracked/ignored Day 6 and analysis files
  no  -> locate a verified offline clone/archive -> verify .git and hashes
        -> create a second backup before changing anything
No verified copy exists?
  -> document loss honestly; do not reconstruct “exact” evidence from memory
```

The Day 6 documents and many secondary run analyses are currently untracked or
ignored. A fresh clone may not contain them. After supervisor/student review,
archive them intentionally or maintain a separate checksummed backup; Day 6C
does not commit them.

### 26.2 GitHub repository is lost

```text
Is a local clone with .git intact available?
  yes -> make a read-only backup -> verify HEAD, tag and artifacts
        -> create a replacement remote under approved ownership
        -> push branches/tags without rewriting history
  no  -> restore from another verified clone/bundle/archive
No Git history survives?
  -> preserve files and hashes as a damaged archive; do not invent commit IDs
```

### 26.3 Virtual environment is lost

This is recoverable and expected. Delete/recreate only the exact `.venv` after
verifying its path; never delete the repository. Use Python 3.12+, create a new
environment, install `.[dev]`, and run release gates. Do not copy a stale
site-packages directory or treat a new dependency resolution as identical to the
old runtime without recording versions.

### 26.4 H0 artifact is missing

```text
Is the tracked path absent only in the working tree?
  -> inspect Git status and HEAD -> restore exact bytes from trusted commit/tag
     without rerunning the detector -> verify SHA-256 3307c28d...71b80
Is it absent from the remote but present in another verified clone/backup?
  -> restore exact bytes -> verify hash -> document restoration provenance
No exact bytes survive?
  -> report evidence loss; do NOT rerun the exposed holdout and call it H0
```

### 26.5 An important hash mismatches

```text
Stop -> record path, observed hash, expected hash, Git commit and dirty status
     -> compare file bytes/status with trusted commit/tag or redundant backup
     -> decide whether this is corruption, line-ending transformation, or an
        intentional new version
If corruption -> restore exact trusted bytes and reverify
If intentional -> preserve old version; assign/document a new identity
Never -> change the expected hash merely to make the gate pass
```

The `.gitattributes` marks primary evidence non-text to avoid line-ending
normalization, but external editors/cloud tools can still alter bytes.

### 26.6 A corpus was accidentally modified

Do not reset or overwrite blindly. Save the diff and working-tree status. If the
change is accidental and the old corpus is protected, recover exact files from a
trusted commit after confirming targets and verify the semantic hash. If a
correction is substantively needed, preserve the old corpus and propose a new
version, review and protocol. Modified old holdout data cannot become unseen
again.

### 26.7 The exposed holdout was accidentally rerun

Preserve/log the event and generated artifact as local post-unblinding activity.
Do not replace H0, do not call the new run confirmation, and do not tune then use
the same holdout. Since this particular holdout is already exposed, another run
does not restore or add independent evidence. If a *future fresh* holdout is
accidentally evaluated early, treat it as exposed and replace the confirmation
plan with a genuinely new untouched set.

### 26.8 Detector changed before preregistration

```text
Has any future holdout prediction occurred?
  no -> classify changes as development -> test on development data -> review
        -> freeze a new version/config -> preregister before holdout work
  yes -> candidate and holdout are post-unblinding relative to each other
        -> preserve as exploratory -> obtain another untouched holdout
```

Do not hide uncommitted changes or use `dirty=false` metadata if the tree was
dirty.

### 26.9 Supervisor changes the methodology

Preserve this pilot as history. Write a new formal protocol/version explaining
what changed, why, and which old evidence remains relevant. Revisit variables,
corpora, review, statistics, timing, tooling and claims. Do not retrofit H0 to
the new method or imply the old plan had always contained the change.

### 26.10 An independent reviewer is unavailable

Do not self-review and label it independent. Delay the freeze or recruit an
approved replacement. Record reviewer role/qualification, training, access,
blinding and conflicts. If only one reviewer is feasible, obtain supervisor
approval and retain it as a limitation. Never fabricate agreement or consensus.

### 26.11 Package dependencies changed

```text
Recreate environment from supported pyproject ranges
  -> record Python/OS/dependency versions
  -> run strict parsing/security tests and full development gates
  -> compare behavior on development corpora only
Any result/config behavior changed?
  yes -> treat runtime as a new reproducibility identity; investigate and freeze
  no  -> document compatible reconstruction; timing still needs new metadata
```

Do not weaken a resource limit or test merely to accept a new dependency.

---

## 27. Future environment reconstruction

These commands reflect repository-supported Python/PowerShell workflows. Review
the README and `pyproject.toml` in the checked-out commit because dependencies
may change months later.

```powershell
# 1. Obtain history and tags.
git clone https://github.com/danveil/mcp-security-inspector
cd mcp-security-inspector
git fetch --tags

# 2. Inspect before checkout or installation.
git rev-parse --show-toplevel
git status --porcelain
git log -1 --oneline
git tag --list

# 3. For the preserved alpha checkpoint, inspect/check out the known tag.
git show --no-patch v0.3.0a1
git checkout v0.3.0a1
git rev-parse HEAD

# 4. Create an isolated Python 3.12+ environment.
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"

# 5. Engineering verification. No holdout evaluation.
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m mypy src
.\.venv\Scripts\python.exe -m pytest --cov=mcpsec --cov-report=term-missing
.\.venv\Scripts\python.exe -m build
.\.venv\Scripts\python.exe scripts\smoke_wheel.py dist\<wheel-file>.whl

# 6. Safe static demonstration on bundled examples.
.\.venv\Scripts\mcpsec.exe scan examples\clean_tools.json
.\.venv\Scripts\mcpsec.exe scan examples\mixed_tools.json --format json --output report.json
.\.venv\Scripts\mcpsec.exe fingerprint examples\clean_tools.json
.\.venv\Scripts\mcpsec.exe baseline examples\clean_tools.json --output baseline.json
.\.venv\Scripts\mcpsec.exe compare examples\changed_tools.json --baseline baseline.json --verbose

# 7. Development evaluation only, after confirming the manifest split.
.\.venv\Scripts\mcpsec.exe evaluate evaluation\corpus\manifest.json --format json --runs-dir evaluation\runs
```

If returning to active development rather than reproducing the alpha tag, create
an approved branch from the chosen main checkpoint. Do not develop while in a
detached tag checkout. Keep generated `.venv`, caches, builds, reports,
baselines and ordinary run artifacts untracked.

The sample MCP server is a harmless development fixture; it is not the inspector
web UI and is not necessary for static file scanning. `mcp dev` may open the
upstream MCP development sandbox, while this project remains primarily a CLI.
Never start a command supplied inside scanned metadata.

---

## 28. I HAVE RETURNED TO THIS PROJECT — WHAT DO I DO?

### Repository and evidence

- [ ] I obtained the repository from a trusted remote/archive.
- [ ] I verified the Git root, HEAD, branch, tags and worktree status.
- [ ] I know whether I am reproducing `v0.3.0a1` or starting new development.
- [ ] I verified the H0, Day 3C, Day 4C and reviewer-source hashes.
- [ ] I confirmed the holdout corpus hash/status without producing predictions.
- [ ] I recorded which untracked/ignored Day 6 and analysis files survived.
- [ ] I created a second safe backup before major formal-FYP work.

### Relearn the project

- [ ] I read the README, research status and reproducibility guide.
- [ ] I read this handover.
- [ ] I can use the technical map to locate each major subsystem.
- [ ] I reviewed the Captain's Manual sections I cannot explain from memory.
- [ ] I can state the 16 rules, seven families and static-only trust boundary.
- [ ] I can explain finding severity versus aggregate risk versus evaluation
  threshold.
- [ ] I can explain canonical fingerprints and baseline drift.

### Own the scientific record

- [ ] I can reconstruct H0: TP 5, TN 18, FP 6, FN 19.
- [ ] I can state H0 accuracy/precision/recall/F1/FPR.
- [ ] I know why H0 is authoritative despite poor performance.
- [ ] I can explain why the 91.25% development result is not generalization.
- [ ] I can explain why v0.3's 45.83% recall is exploratory.
- [ ] I understand R08 and the single-reviewer limitation.
- [ ] I know the old holdout is permanently exposed.
- [ ] I will not modify or regenerate immutable evidence.

### Reconstruct and verify safely

- [ ] I created a fresh Python 3.12+ virtual environment.
- [ ] I installed `.[dev]` from the checked-out repository.
- [ ] Lint, format, strict typing, tests, build and wheel smoke pass or failures
  are documented.
- [ ] I used only example/development data for debugging.
- [ ] I recorded environment/version differences from the historical checkpoint.

### Meet the supervisor before designing the next test

- [ ] I prepared the supervisor discussion pack and pilot chronology.
- [ ] I presented the poor H0 result before the favorable exploratory result.
- [ ] We agreed whether the current rules-based scope remains appropriate.
- [ ] We refined the target construct and candidate research question.
- [ ] We discussed sample size, prevalence, sources, reviewers and statistics.
- [ ] We agreed scope boundaries, ethical/licensing handling and thesis framing.
- [ ] I documented decisions and unresolved questions.

### Freeze the future method

- [ ] The detector candidate is final before holdout access.
- [ ] The rule pack, threshold, risk, configuration and code commit are frozen.
- [ ] Primary/secondary metrics, intervals and timing are preregistered.
- [ ] The untouched-sample authorship and leakage plan is approved.
- [ ] Reviewer blinding/adjudication and corpus-version rules are approved.
- [ ] Pre-run integrity, artifact destination and single-run rules are approved.
- [ ] A clean checkpoint and supervisor authorization exist.
- [ ] Only then will fresh corpus work begin under the approved protocol.

---

## 29. Viva defense core: 15 propositions

1. **Why static rules?** They provide deterministic, offline, explainable,
   versionable and bounded analysis appropriate to a pre-use metadata gate. H0
   also honestly reveals their semantic-coverage cost.
2. **Why not an LLM classifier?** It changes the research intervention and adds
   privacy, nondeterminism, cost, latency, model drift and prompt-injection
   concerns. It may be a separate comparator, not an undocumented patch.
3. **Why inspect metadata at all?** Tool definitions influence discovery and
   selection; publisher-controlled descriptions, schemas and extensions cross a
   trust boundary before runtime invocation.
4. **Why MEDIUM?** It was the preregistered H0 binary threshold and distinguishes
   informational capability inventory from binary suspicious findings. It is
   preserved for historical validity, not claimed universally optimal.
5. **Why hash/canonicalize schemas?** Deterministic canonical identities make
   semantically equivalent ordering stable and expose changes to security-
   relevant components for baseline drift and reproducibility.
6. **Why is H0 poor performance still valuable?** It is a frozen independent
   test that falsified the expectation suggested by development results and
   identified precise coverage and false-positive mechanisms.
7. **Why is v0.3 exploratory?** H0 predictions and Day 3C failure mechanisms
   directly informed its five new rules; the reused holdout is no longer
   independent of the candidate.
8. **Why a fresh holdout?** Only genuinely prediction-unexposed data can estimate
   transfer after the revised detector is frozen. Repeating the old set measures
   known-case behavior.
9. **Why bounded depth-one decoding?** It covers four explicit representations
   while keeping work, output and interpretation deterministic. Recursion adds
   multiplicative cost, false positives and arbitrary stopping.
10. **Why no tool invocation?** Metadata is hostile and the project asks a static
    pre-use question. Invocation would add side effects, authorization and
    runtime-sandbox threats outside the scope.
11. **Why can a finding be benign?** Rules detect review indicators, not intent.
    Security documentation, legitimate admin capability, privacy redaction and
    malformed schemas may be valid hard negatives or quality findings.
12. **Why is one reviewer a limitation despite kappa 0.9583?** Kappa measures
    agreement with one review's marginal labels, not objective truth or
    multi-expert consensus; difficulty agreement was only 16/48.
13. **Why not lower the threshold after H0?** Seventeen FNs had no finding, so it
    misses the main mechanism. More importantly, post-hoc selection would create
    a new configuration requiring fresh confirmation.
14. **What is the strongest contribution?** A defensible combination of safe
    deterministic metadata inspection, canonical drift identities,
    reproducibility infrastructure, and an honest evidence chain from negative
    H0 to bounded exploratory design—not a production-accuracy claim.
15. **Can attackers bypass it?** Yes. Fixed rules can miss new language,
    structure, encoding and cross-field semantics. The system reduces and
    explains selected risks; it does not prove completeness.

---

## 30. Continuity notes before leaving the project

### 30.1 Files that a fresh clone should preserve

The current locally stored `origin/main` and `v0.3.0a1` refs both identify
`374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`. Tracked code, corpora, release
documents, the H0 artifact, Day 3C report and primary Day 4C artifact should be
recoverable from that history if the remote truly contains those refs.

### 30.2 Files currently at local-loss risk

At Day 6C, `docs/captain-technical-map.md`, `docs/captains-manual.md` and this
handover are untracked. The Day 3D evidence bundle and most Day 4A/B/C secondary
artifacts are ignored. `git status` does not display ignored files. Future-you
must not assume GitHub contains these simply because they exist locally.

Recommended future action, after review and outside Day 6C: choose a deliberate
archive policy. Options include a reviewed documentation commit for Day 6 files,
a checksummed research archive for selected secondary analyses, or both. Keep
machine-specific/generated timing runs out unless the protocol explicitly
selects them.

### 30.3 Research signoff statement

The project should be described on return as:

> A pre-FYP defensive static-analysis prototype with a reproducible pilot study.
> Its authoritative v0.2 holdout result showed poor generalization on the pilot
> corpus. A v0.3 candidate was developed and explored after unblinding, but no
> fresh confirmatory evaluation exists. Formal FYP continuation requires
> supervisor-approved scope, methodology and an untouched evaluation.

---

## 31. Cross-document consistency audit

Audited documents:

- `README.md`
- `docs/research-status.md`
- `docs/reproducibility.md`
- `docs/captain-technical-map.md`
- `docs/captains-manual.md`
- `docs/fyp-handover.md`

### 31.1 Consistent scientific facts

| Fact | Audit result |
|---|---|
| H0 matrix and metrics | Consistent: 5/18/6/19; 47.92%, 45.45%, 20.83%, 28.57%, 25.00% |
| H0 artifact hash | Consistent: `3307c28d...71b80` |
| v0.3 exposed result | Consistent: 11/18/6/13; 60.42%, 64.71%, 45.83%, 53.66%, 25.00% |
| v0.3 artifact hash | Consistent: `d5d84dc3...806b` |
| Current versions | Consistent: package `0.3.0a1`, built-in rule pack `2.0.0`, current artifact schema `3.1.0` |
| Holdout identity/status | Consistent: v1.0.1, 48/24/24, hash `c514ba03...a2d8`, independently reviewed, now exposed |
| Scientific status | Consistent: v0.2 H0 is authoritative first confirmatory result; v0.3 is post-unblinding exploratory |
| Fresh-confirmation requirement | Consistent: new untouched, independently reviewed, preregistered holdout required |
| Development status | Consistent: visible regression evidence, not generalization |

Historical H0/Day 4C artifacts record schema `3.0.0` and rule pack `1.0.0` while
current code uses schema `3.1.0` and rule pack `2.0.0`. This is expected historical
identity, not inconsistency. Likewise Day 4C's `dirty=true`, application `0.2.0`
metadata is authentic provenance and must not be modernized.

### 31.2 Reported inconsistencies or stale statements

1. **Release-state snapshot:** `docs/captain-technical-map.md` line 711 says that
   at Day 6A inspection the push, `v0.3.0a1` tag and GitHub prerelease were
   incomplete. At Day 6C, local Git shows `main` and locally stored
   `origin/main` both at `3744710` and an annotated local `v0.3.0a1` tag at the
   same commit. The Day 6A sentence remains a time-stamped historical snapshot;
   it is stale as a current local-state description. Day 6C did not perform a
   network fetch or independently confirm a GitHub release page.
2. **CLI example:** `docs/captain-technical-map.md` line 833 shows
   `mcpsec compare examples/mixed_tools.json baseline.json`. The implemented CLI
   requires the baseline as the `--baseline` option. `README.md` and
   `docs/captains-manual.md` contain the correct form, for example
   `mcpsec compare examples/changed_tools.json --baseline baseline.json --verbose`.

No existing document was silently rewritten during this audit. Neither issue
changes the scientific numbers or status.

---

## 32. Day 6C preservation declaration

This handover is documentation only. It does not authorize a new experiment,
does not turn historical artifacts into current ones, and does not change the
scientific status of any corpus.

**NO FRESH CONFIRMATORY EXPERIMENT WAS CREATED OR RUN.**

**THE EXPOSED HOLDOUT WAS NOT USED FOR NEW CONFIRMATORY EVIDENCE.**

**NO DETECTOR, CORPUS, LABEL, THRESHOLD, RISK MODEL, OR FROZEN RESEARCH EVIDENCE
WAS MODIFIED DURING DAY 6C.**
