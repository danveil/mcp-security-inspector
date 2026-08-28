# Formal FYP Development and Research Blueprint

## Document status and authority

This document is a design-only bridge from the preserved **pre-FYP research
prototype / pilot study** to a possible formal undergraduate Final Year
Project (FYP). It is not an approved proposal, preregistration, ethics
application, or authorization to collect data or run an experiment.

**THIS BLUEPRINT IS SUBJECT TO FORMAL SUPERVISOR APPROVAL.**

The repository and its immutable historical artifacts remain authoritative.
Where this blueprint proposes a future change, the proposal does not alter the
meaning of any earlier result.

Repository checkpoint inspected for this blueprint:

| Item | Recorded value |
|---|---|
| Repository | MCP Tool Security Inspector |
| Git commit | `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` |
| Current package version | `0.3.0a1` |
| Current built-in rule-pack version | `2.0.0` |
| Current experiment artifact schema | `3.1.0`, with historical `3.0.0` support |
| Historical confirmatory status | v0.2 H0 pilot evidence, preserved |
| Current detector status | v0.3 post-unblinding exploratory prototype |

This blueprint complements, rather than replaces:

- `docs/captain-technical-map.md`;
- `docs/captains-manual.md`;
- `docs/fyp-handover.md`;
- `docs/disaster-recovery.md`;
- `docs/recovery-manifest.md`; and
- `docs/final-adversarial-review.md`.

### Non-actions during Day 6F

No detector, test, corpus, label, threshold, risk model, suppression, rule,
experiment artifact, or frozen research record was changed to produce this
document. No fresh holdout was created. The exposed 48-sample holdout was not
rerun. No confirmatory experiment or detector tuning was performed.

---

## 1. Starting point inherited by the formal FYP

The future FYP should inherit five deliberately separate bodies of work.
Mixing them would create both engineering confusion and invalid research
claims.

### A. Preserved historical evidence

The v0.2 primary H0 run is the project's historical confirmatory **pilot**
evidence. It evaluated the then-frozen detector once against the independently
reviewed 48-sample holdout under the preregistered MEDIUM threshold and full
built-in configuration.

| Historical v0.2 H0 item | Preserved value |
|---|---:|
| TP / TN / FP / FN | 5 / 18 / 6 / 19 |
| Accuracy | 47.92% |
| Precision | 45.45% |
| Recall | 20.83% |
| F1 | 28.57% |
| False-positive rate | 25.00% |
| Holdout corpus SHA-256 | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| Configuration SHA-256 | `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1` |
| Primary artifact SHA-256 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` |

These numbers must not be overwritten, retroactively relabelled as formal-FYP
confirmation, or recomputed with newer code and then presented as the same
experiment. They answer: “How did the frozen v0.2 pilot detector perform on
that exposed pilot holdout under that frozen protocol?”

The development corpus is also historical evidence: 80 synthetic-heavy
samples, balanced 40 benign / 40 suspicious, used openly during development.
It is not independent confirmation.

The reviewer record is preserved context: one independent reviewer was
blinded to expected labels and detector predictions; agreement was 47/48,
Cohen's kappa was approximately 0.9583, and R08 remained a documented
disagreement. High label agreement supports consistency under the supplied
construct, but it does not establish construct validity, real-world
prevalence, or detector effectiveness.

### B. Current engineering prototype

The current repository is a bounded, deterministic, defensive static
inspector for MCP tool definitions. Its major implemented capabilities are:

- bounded hostile JSON and metadata loading;
- typed validation and Unicode NFC normalization;
- deterministic built-in detector families and data-only custom rules;
- suppressions;
- capped aggregate risk;
- terminal, JSON, CSV, and SARIF reporting with output safety controls;
- canonical fingerprints, baselines, and drift comparison;
- explicit loopback-only `tools/list` retrieval;
- corpus validation, evaluation, comparison, ablation, and timing support;
- historical artifact compatibility; and
- packaging, CLI, security-boundary, and research-integrity tests.

Its static-analysis boundary is an important contribution: the scanner must
not invoke discovered tools, execute metadata, fetch metadata-linked
resources, or send scanned content to a model.

### C. Exploratory v0.3 knowledge

v0.3.0a1 added five post-unblinding exploratory rules: PI-002, HID-002,
SEC-002, OBF-005, and MIS-002. An exploratory rerun on the already exposed
holdout produced:

| Exploratory v0.3 item | Observed value |
|---|---:|
| TP / TN / FP / FN | 11 / 18 / 6 / 13 |
| Accuracy | 60.42% |
| Precision | 64.71% |
| Recall | 45.83% |
| F1 | 53.66% |
| False-positive rate | 25.00% |

This result is useful for generating hypotheses and identifying detector
weaknesses. It cannot confirm generalization because the rules were designed
after inspecting failures on the same holdout. Correct language is:

> On the exposed pilot holdout, the post-unblinding v0.3 exploratory
> configuration detected more labelled suspicious samples than v0.2 while
> the observed false-positive count remained unchanged. Independent
> confirmation on a fresh untouched corpus is required.

### D. Unresolved engineering issues

The most serious known issue is **finding-budget decision coupling**. Current
scan flow derives risk and several downstream decisions from the bounded list
of retained findings. If a global report budget is consumed by earlier tools,
a later tool can have detector matches that are not retained and can therefore
receive risk zero, avoid `--fail-on`, appear unaffected in reports, and be
predicted benign by evaluation. The historical H0 and v0.3 artifacts were
checked and were not affected by their observed finding volumes; the defect
still blocks a future confirmatory candidate.

Other unresolved issues include:

- robust handling of newline transformations in freeze/hash procedures;
- stronger dependency reproducibility;
- privacy-minimized research output choices;
- explicit resource-worst-case validation;
- clearer baseline provenance and suppression governance;
- formalized historical compatibility for the next decision semantics; and
- documentation consistency after any future change.

### E. Unresolved research questions

The pilot does not answer:

- which precisely defined constructs should count as the primary target;
- how the detector performs on independently authored, more realistic,
  untouched data;
- whether observed v0.3 gains generalize;
- how effectiveness changes under adaptive but bounded variations;
- how performance changes under realistic prevalence;
- whether category-level estimates can be made with useful uncertainty;
- what comparison baselines are supported by the literature; or
- what latency claim is defensible under a documented machine protocol.

These are future research decisions, not gaps to repair by rewriting the
pilot.

---

## 2. Candidate FYP framings

### Candidate A — Lightweight static detector for suspicious MCP metadata

**Provisional title:** “Design and Empirical Evaluation of a Deterministic,
Bounded Static Inspector for Supervisor-Defined Suspicious Constructs in MCP
Tool Metadata.”

| Criterion | Assessment |
|---|---|
| Research clarity | Strong if the suspicious constructs are explicitly enumerated before data creation. |
| Alignment | Very strong: it matches loading, normalization, detectors, risk, reports, and resource bounds already implemented. |
| Overclaim risk | Moderate and controllable. “Suspicious constructs” avoids equating every alert with malicious intent. |
| Measurable outcomes | Recall and false-positive rate for a frozen taxonomy; precision/F1 under declared prevalence; latency and robustness as secondary outcomes. |
| Likely scope | One static detector, one frozen configuration, one future untouched corpus, bounded secondary comparisons. |
| Required literature | MCP architecture/security, prompt injection and tool poisoning, static/rule-based security detection, detector evaluation, adversarial robustness. |
| Undergraduate suitability | High: substantial system work plus a tractable empirical evaluation. |
| Weaknesses | The construct remains partly synthetic and rule-defined; static metadata cannot prove runtime behavior or attacker intent. |

### Candidate B — Detection of known tool-poisoning patterns

**Provisional title:** “Detection of Predefined Tool-Poisoning Patterns in
MCP Tool Definitions.”

| Criterion | Assessment |
|---|---|
| Research clarity | Clear only if “tool poisoning” is narrowly operationalized as specific metadata patterns. |
| Alignment | Strong for injection-like, concealment, sensitive-data, mismatch, and obfuscation rules; weaker for generic schema-quality findings. |
| Overclaim risk | High. The current detector observes metadata patterns, not malicious intent or downstream compromise. |
| Measurable outcomes | Pattern-level detection, false alarms, bypass cases, and latency. |
| Likely scope | Narrower detector study; drift and generic schema validation may become peripheral. |
| Required literature | Direct MCP/tool-poisoning work plus indirect prompt injection and agent/tool trust. |
| Undergraduate suitability | Medium to high if the supervisor accepts the operational definition. |
| Weaknesses | Literature may not support a stable taxonomy; broad use of “tool poisoning” could invalidate the construct. |

### Candidate C — Integrity and suspicious-metadata analysis

**Provisional title:** “Integrity Drift and Suspicious-Metadata Analysis for
MCP Tool Definitions.”

| Criterion | Assessment |
|---|---|
| Research clarity | Potentially strong, but combines two distinct questions: content classification and change detection. |
| Alignment | Strong across detectors, canonical fingerprints, baselines, comparison, and reporting. |
| Overclaim risk | Lower for “integrity drift,” provided drift is not called malicious by default. |
| Measurable outcomes | Detection metrics for suspicious constructs; exact drift invariants; rename inference; latency. |
| Likely scope | Larger than A or B and risks becoming two FYPs. |
| Required literature | All Candidate A topics plus software/configuration integrity and drift detection. |
| Undergraduate suitability | Medium: attractive if drift is the supervisor's priority, but must be tightly bounded. |
| Weaknesses | More objectives, more test data, and a difficult combined conclusion. |

### Recommendation for supervisor discussion

Candidate A is the recommended starting point because it most accurately
describes the existing system and leaves intent claims outside the measured
construct. Candidate C is a viable alternative if the supervisor wants
fingerprinting and drift to be central. Candidate B should be used only if the
supervisor approves a narrow operational definition of “tool poisoning.”

The recommendation is not approval. The final title, construct, and scope must
be recorded in the supervisor decision register before engineering freeze.

---

## 3. Construct taxonomy

The unit being observed is a static MCP tool definition: its name,
description, input schema, annotations, `_meta`, and other permitted metadata.
The detector can identify patterns in that representation. It cannot directly
observe server intent, tool execution, runtime side effects, downstream model
behavior, or compromise.

| Construct | Proposed status | Operational boundary and rationale |
|---|---|---|
| Tool poisoning as malicious intent | **OUT OF SCOPE as a directly proven label** | It is a motivating threat class. Metadata alone cannot prove intent or successful poisoning. A future thesis may say that core targets are patterns associated with or relevant to tool poisoning. |
| Prompt-injection-like metadata | **CORE TARGET** | Imperative or policy-overriding text directed at an agent/model in tool metadata. The label describes observable language, not successful model manipulation. |
| Concealment | **CORE TARGET** | Instructions or structures encouraging hiding, non-disclosure, invisibility, or suppression of relevant behavior/content. |
| Sensitive-data instructions | **CORE TARGET when instruction and data action are contextual; SUPPORTING SIGNAL otherwise** | An instruction to reveal, transmit, collect, or expose credentials/secrets is stronger than a harmless mention such as “password strength.” |
| Capability/purpose mismatch | **CORE TARGET** | Cross-field inconsistency between declared purpose/description and powerful or unrelated input capabilities. It is a suspicious consistency defect, not proof the tool will misuse capability. |
| Malformed schema | **SECURITY-QUALITY WARNING** | Invalid or contradictory schema can undermine safe integration, but malformed data alone is not tool poisoning. |
| Privileged/dangerous schema capability | **SUPPORTING SIGNAL or SECURITY-QUALITY WARNING** | A command/path/token field can be legitimate. Context and declared purpose determine whether it contributes to a core mismatch. |
| Obfuscation/encoded representation | **SUPPORTING SIGNAL** | Encoding is common and often benign. If strict bounded decoding reveals a core construct, the decoded construct inherits that core category; encoding alone remains supporting. |
| Integrity drift | **SUPPORTING, SEPARATE OUTCOME** | A deterministic change from an approved baseline. Drift indicates change, not maliciousness, and should not be included in effectiveness labels unless a separate research question defines it. |
| Disclosed powerful capability | **SUPPORTING SIGNAL** | Transparent declaration reduces mismatch but may still justify review. It should not be counted automatically as a malicious finding. |
| Length, whitespace, or unusual representation | **SECURITY-QUALITY WARNING** | Useful for review and resource safety, but weak evidence of a malicious construct. |
| Broad security-sensitive vocabulary | **OUT OF SCOPE as a standalone core label** | Words such as “token,” “secret,” or “system” are too common. They require action and context to become meaningful. |
| Runtime behavior, network side effects, tool output poisoning | **OUT OF SCOPE for this static inspector** | These require sandboxed execution, dynamic observation, or a different research design. |

### Labelling rule

Future corpus labels must refer to a written observable construct definition,
not a hidden assumption about intent. At minimum, each suspicious-labelled
sample should record:

1. the applicable construct;
2. the exact field/location;
3. the observable evidence;
4. why the evidence satisfies the construct;
5. an expected benign hard negative for the same vocabulary or structure; and
6. whether the sample is single-construct or intentionally multi-construct.

Ambiguous samples should permit abstention or adjudication. “Malformed” and
“suspicious” must not be silently collapsed into one label.

---

## 4. Formal threat-model blueprint

### Assets

- the integrity of tool definitions consumed by an MCP host or client;
- the confidentiality of user, system, credential, and environment data;
- the agent's instruction hierarchy and intended decision process;
- the accuracy and trustworthiness of security findings, risk decisions, and
  reports;
- approved baselines and configuration;
- availability of the scanner under hostile metadata; and
- reproducible experiment and historical evidence.

### Trust boundaries

| Boundary | Untrusted side | Trusted side | Required control |
|---|---|---|---|
| File/STDIN to loader | Arbitrary bytes and JSON structure | Bounded internal document | Byte, depth, collection, and metadata limits; strict parsing |
| MCP response to retrieval | Loopback server response | Static tool catalog | Explicit opt-in, loopback-only transport, no redirects/proxies, response limits |
| Raw metadata to normalized model | Aliases, Unicode, field types | Typed normalized tool definition | Alias-conflict rejection, NFC, validation |
| Normalized content to detector | Adversarial strings/schemas | Inert deterministic findings | No execution, no fetched links, bounded traversal/decoding |
| Custom rule/suppression file to engine | User-controlled configuration | Valid data-only configuration | Schema validation, fixed operators, no executable/user regex expressions |
| Detector to decision state | Potentially many matches | Complete bounded decision summary | Streaming/bounded accumulator; decision independent of report retention |
| Decision to report | Hostile evidence text | Terminal/JSON/CSV/SARIF artifact | Escaping, formula neutralization, redaction, truncation metadata |
| Current code to historical artifacts | Older schemas/rule sets | Honest comparison | Recorded schema/rule-pack/config identities; no reinterpretation |
| Baseline to drift decision | Potentially stale or attacker-controlled baseline | Trusted reference state | Provenance, access control, review, hash, explicit trust policy |

### Attacker goals

- influence an agent or model through tool metadata;
- conceal security-relevant instructions or capabilities;
- induce disclosure or transfer of sensitive information;
- present capabilities inconsistent with the declared purpose;
- evade static detection through paraphrase, relocation, Unicode, or encoding;
- exhaust memory, CPU, finding, or reporting resources;
- poison trusted baselines, custom rules, or suppressions;
- cause unsafe display or downstream processing of evidence; or
- exploit time-of-check/time-of-use differences between scanned and executed
  definitions.

### Attacker capabilities

The modeled attacker may control all fields of one or more tool definitions,
including nested schemas and metadata; choose ordering; create large but
bounded documents; use benign-looking vocabulary; introduce field
inconsistencies; use supported encodings and Unicode; and change metadata after
a baseline is created. An adaptive attacker may know public rule behavior.

The model does not assume the attacker can modify the inspector binary,
approved experiment configuration, trusted operating system, or correctly
protected baseline. If those assumptions are relaxed, a different integrity
model is required.

### Trusted components

- the reviewed, pinned inspector build and its dependency environment;
- the frozen built-in rule pack and experiment configuration;
- the Python/runtime/OS boundary to the extent recorded by the protocol;
- securely stored baselines and suppressions after explicit approval;
- corpus manifests and labels after immutable freeze; and
- the independent review and artifact-preservation process.

Trust is conditional, not automatic. A baseline or suppression created from
untrusted state must not be treated as authoritative merely because it has a
valid file format.

### Untrusted inputs

Tool names, descriptions, schemas, annotations, `_meta`, vendor/execution
metadata, server responses, JSON files, custom rules, suppressions, baselines,
artifact files being loaded, report consumers, and text rendered from all
those sources must be treated as hostile data.

### Assumptions

- static metadata is available for inspection before a decision to trust/use
  the tool;
- the scanned bytes correspond to the catalog state the operator intends to
  assess;
- the local analysis environment is not already compromised;
- future labels represent the supervisor-approved observable construct; and
- the future primary corpus remains unseen by detector developers until the
  frozen evaluation.

### Security goals

1. Reject or safely bound malformed and oversized hostile input.
2. Analyze metadata without invoking tools or executing/fetching content.
3. Produce deterministic findings, decisions, hashes, and reports for the
   same normalized input and configuration.
4. Ensure presentation limits never alter detection or classification
   semantics.
5. Make truncation, suppression, and provenance visible.
6. Prevent hostile output from becoming terminal or spreadsheet execution.
7. Preserve honest historical interpretation across versions.
8. Detect the supervisor-approved constructs at measured effectiveness while
   quantifying false alarms and uncertainty.

### Non-goals and out-of-scope attacks

- proving malicious intent;
- proving that an alert causes an LLM to follow the instruction;
- dynamic tool execution or malware analysis;
- remote server crawling or general Internet retrieval;
- protecting a compromised operating system or modified inspector;
- preventing server-side behavior that differs after scanning;
- complete semantic detection of arbitrary natural-language attacks;
- recursively unpacking arbitrary encodings or archives; and
- certifying a tool as safe because no finding was produced.

### Explicit gap handling

- **Adaptive attackers:** evaluate bounded transformations during development
  and maintain bypass limitations; do not claim complete resistance.
- **TOCTOU:** bind scan decisions to a canonical fingerprint; deployment
  integration should require the execution-time definition to match the
  approved fingerprint. Full runtime enforcement is outside current scope.
- **Baseline trust:** record source, creator, time, environment, and approval;
  protect the baseline independently from scanned input.
- **Suppression trust:** require review, narrow scope, reason/owner/expiry where
  policy permits, and an audit trail. A suppression changes policy, not truth.
- **Downstream reports:** treat them as security outputs; escape, neutralize,
  redact, cap, and clearly mark truncation.
- **Resource exhaustion:** keep input, traversal, decoding, evidence, finding,
  and output operations bounded; test adversarial worst cases.
- **Metadata versus runtime:** state throughout the thesis that static metadata
  findings do not establish runtime behavior.

---

## 5. Candidate research questions

The wording below is provisional and must be approved before fresh data is
constructed.

### RQ1 — Primary candidate

**How effectively does a frozen deterministic static inspector identify the
supervisor-defined core suspicious constructs in previously unseen MCP tool
metadata while controlling false positives?**

| Design item | Proposed definition |
|---|---|
| Independent variable | Ground-truth class/construct in the future untouched corpus |
| Dependent variables | Recall and false-positive rate; secondary precision, F1, accuracy, and confidence intervals |
| Controls | Frozen commit, rule pack, threshold, decision semantics, configuration, corpus, label/review protocol, and environment |
| Required evidence | Immutable corpus/labels/reviewer records; configuration and corpus hashes; one raw primary artifact; analysis script/output |
| Main validity threats | Construct validity, synthetic/author bias, prevalence, small N/strata, reviewer disagreement, matched dependence, adaptive evasion |

This is the recommended primary question for supervisor discussion.

### RQ2 — Frozen candidate versus historical implementation

**On the same future untouched corpus, how does the frozen revised detector
compare with the preserved v0.2 implementation for the preregistered primary
metrics?**

| Design item | Proposed definition |
|---|---|
| Independent variable | Detector implementation: historical v0.2 versus future frozen candidate |
| Dependent variables | Paired changes in detections/errors; recall, FPR, precision, F1 with intervals |
| Controls | Same canonical corpus and labels; exact historical environment/container or verified historical wheel; frozen comparison procedure |
| Required evidence | Separate immutable artifacts and identities for both implementations; paired sample outcomes; compatibility checks |
| Main validity threats | Historical-environment reconstruction, changed artifact semantics, construct mismatch, post-hoc choice of baseline |

This can be an optional secondary question. It must not retroactively replace
or modify the historical H0 result.

### RQ3 — Bounded representation robustness

**How stable are the frozen detector's decisions under preregistered,
meaning-preserving metadata transformations and defined adversarial
representations?**

- **Independent variable:** transformation class: whitespace, key order,
  Unicode normalization, bounded encoding, field relocation, or paraphrase
  family.
- **Dependent variables:** decision invariance where expected, recall change,
  new false positives, and bypass count.
- **Controls:** base development cases, transformation generator/version,
  detector/configuration.
- **Evidence:** development-only metamorphic suite plus a separate untouched
  robustness panel if approved.
- **Threats:** whether transformations truly preserve meaning; generator bias;
  tuning leakage.

Treat this as development/diagnostic unless a separately frozen untouched
robustness panel is feasible.

### RQ4 — Integrity-drift capability

**With a trusted baseline, which security-relevant changes in MCP tool
definitions are detected by canonical component comparison, and which changes
remain ambiguous?**

This question fits Candidate C. Its independent variable is controlled
metadata change; outcomes are exact drift component, rename inference, and
false/missed changes. It requires a separately defined ground truth and must
not be mixed into RQ1 labels. Defer unless drift is chosen as a primary FYP
component.

### RQ5 — Bounded performance

**What analysis-core and static end-to-end latency does the frozen inspector
exhibit under a documented single-machine protocol for the future evaluation
corpus and declared resource-bound cases?**

Latency boundary/workload is the independent condition; median, mean, p95,
dispersion, and throughput are dependent outcomes. Machine/runtime/load,
warm-ups, repetitions, and input order are controls. This supports a bounded
“lightweight on the tested setup” statement, not a universal performance
claim.

### Recommended research-question set

- Primary: RQ1.
- Optional effectiveness comparison: RQ2.
- Secondary engineering question: RQ5.
- Diagnostic robustness: RQ3.
- RQ4 only if the supervisor selects Candidate C and reduces another scope
  item.

---

## 6. Objectives

### General objective

To design, implement, and empirically evaluate a deterministic and
resource-bounded static inspector for supervisor-defined suspicious
constructs in MCP tool metadata, without presupposing its effectiveness or
equating static findings with malicious intent.

### Specific objectives

1. **Design:** define and justify a threat model, target-construct taxonomy,
   decision semantics, and bounded static-analysis architecture for MCP tool
   metadata.
2. **Implementation:** remediate decision/presentation coupling and produce a
   tested, versioned candidate whose analysis remains inert, deterministic,
   and resource bounded.
3. **Implementation:** preserve canonical integrity/drift and safe reporting
   capabilities with explicit provenance, suppression, and historical
   compatibility behavior.
4. **Evaluation:** measure the frozen candidate's ability to identify the
   predefined constructs on a future untouched, independently reviewed
   corpus using preregistered metrics and uncertainty intervals.
5. **Evaluation:** characterize bounded latency, failure modes, and—if
   approved—selected robustness/comparison analyses while separating
   confirmatory results from later exploratory work.

Success means that the design and evaluation are rigorous and reproducible;
it does not require the detector to achieve a predetermined metric.

---

## 7. Future fix for finding-budget decision coupling

### Required semantic invariant

For a given normalized catalog, detector/rule pack, suppressions, threshold,
and decision configuration:

> Changing only presentation limits or input order must not change a tool's
> aggregate risk, threshold classification, `--fail-on` decision, affected
> count, or evaluation prediction.

Presentation limits may change which examples are shown. They must not change
what the scanner decided.

### Proposed three-state architecture

| State | Purpose | Must contain | Must not depend on |
|---|---|---|---|
| **Detection state** | Receive every unsuppressed detector event in a bounded/streaming form | Per-tool/rule/category counts (capped with overflow flags), strongest severities, triggered IDs/categories, synergy inputs, deterministic sequence metadata | Report retention budget |
| **Decision state** | Express complete classification semantics | `has_findings`, highest severity, aggregate risk/category, threshold result, fail-on result, affected state, completeness/overflow markers, decision-semantics version | Which findings/evidence were retained for display |
| **Presentation/retention state** | Keep a safe deterministic subset for humans and output formats | Retained findings, original/retained/omitted counts, per-limit truncation reasons, bounded/redacted evidence | Risk or evaluation classification |

Conceptual flow:

    detector events
        -> validate and apply suppressions
        -> bounded decision accumulator
        -> complete DecisionState
        -> deterministic bounded PresentationState
        -> terminal / JSON / CSV / SARIF

The implementation design should prefer detector iterators or a callback/event
sink so that it does not first materialize an unbounded list. If immediate
iterator conversion is too risky, the first remediation may retain existing
detector calls behind strict per-detector generation bounds, but the final
candidate must demonstrate an enforced memory bound.

### Decision accumulator requirements

The accumulator needs only the information used by the risk model. At the
current model this includes finding severity and rule/category identities
needed for caps or synergy calculations. Exact future fields must be derived
from `src/mcpsec/risk.py` during implementation; they must not be guessed from
this blueprint.

It should:

- consume each post-suppression match exactly once;
- preserve sufficient state for the same risk result as an unlimited
  reference calculation on within-limit fixtures;
- use saturating counts where counts above a known cap cannot change risk;
- retain explicit overflow/completeness markers where information is
  intentionally bounded;
- fail closed or return an explicit indeterminate state if a safety limit can
  prevent a complete decision;
- produce deterministic results independent of report budget and catalog
  order; and
- separate redaction/evidence truncation from rule identity and severity.

### Deterministic presentation retention

Presentation remains bounded. A stable policy can select findings by a
documented tuple such as severity rank, rule ID, normalized tool identity,
field path, and stable encounter index. The exact tuple should be approved and
tested. The report must expose:

- detected count if exactly known, otherwise a lower bound plus overflow flag;
- retained count;
- omitted count if exactly known;
- limit type(s) reached; and
- a statement that classification used decision state, not the visible
  subset.

### Downstream behavior

| Consumer | Required source after remediation |
|---|---|
| Risk/category | Decision state |
| `--fail-on` | Decision state/highest unsuppressed severity |
| Affected-tool count | Decision state's `has_findings` |
| Evaluation prediction | Decision state and frozen threshold |
| Confusion matrix | Evaluation predictions, never report-list length |
| Human report details | Presentation state with truncation disclosure |
| SARIF result list | Presentation state; run properties must disclose total/omission semantics |
| Suppression audit | Pre/post suppression counts and policy identity |

### Backward compatibility and identities

This change corrects classification semantics, not just display. Therefore:

- historical schema 3.0.0 and 3.1.0 artifacts must retain their original
  interpretation;
- new artifacts should use a **major artifact-schema revision**, provisionally
  4.0.0, because decision state cannot be reconstructed faithfully from an old
  bounded finding list;
- artifacts should record a `decision_semantics_version` and limits separately
  from report formatting;
- the experiment configuration identity must change because decision
  semantics can change predictions under truncation;
- the built-in rule-pack version need not change for a pipeline-only fix, but
  must change if rule matching/severity/suppression semantics change;
- the package should advance to the next appropriate prerelease under the
  project's pre-1.0 convention. The exact number is a release decision after
  scope is known, not something this blueprint freezes.

### Required tests before freeze

1. A later tool with a high-severity match remains risky after an earlier tool
   exhausts the global report budget.
2. `--fail-on` exits identically with small and large presentation budgets.
3. Evaluation predictions and confusion counts are budget invariant.
4. A tool with all findings omitted is still counted as affected.
5. Tool reordering changes presentation only where documented, never decision
   state.
6. Per-tool, global, and evidence caps are independently exercised.
7. Suppressed findings do not enter decision state; redacted findings still
   contribute their non-sensitive decision attributes.
8. Streaming accumulator equals an unlimited reference implementation for
   generated within-bound cases.
9. Every risk cap and cross-family synergy is preserved.
10. Custom-rule and built-in findings follow identical decision semantics.
11. Worst-case match volume remains within measured memory/time limits.
12. All output formats disclose truncation without inventing exact counts.
13. Old 3.0.0/3.1.0 artifacts load with legacy semantics; new artifacts do not
    masquerade as old results.
14. Comparisons reject incompatible decision semantics unless an explicit
    safe comparison path exists.
15. Corrupt/incomplete 4.x decision state is rejected rather than silently
    treated as benign.

---

## 8. Pre-confirmation engineering gates

Severity here means priority before a future detector freeze, not finding
severity.

### P0 — must fix or formally resolve before freeze

| Gate | Required evidence |
|---|---|
| Decouple decision from finding retention | Architecture and regression/property tests in Section 7; budget-invariance demonstrated |
| Freeze the target construct | Supervisor-approved taxonomy, annotation guide, inclusion/exclusion examples |
| Approve threat model and non-goals | Signed/recorded supervisor decision; metadata/runtime distinction visible |
| Version decision semantics | Package/artifact/config identities unambiguous; old results retain legacy interpretation |
| Preserve historical compatibility | Fixture tests for historical artifacts and comparison rejection where semantics differ |
| Establish a clean reproducible candidate | Pinned environment/constraints, clean Git commit/tag, hashes, build and installed-wheel smoke evidence |
| Pass security and resource gates | Lint, format, strict typing, coverage-gated tests, package build, boundary tests, and approved worst-case resource tests |
| Make freeze files newline robust | Hash exact bytes; enforce/document line-ending policy or use a canonical manifest procedure without rewriting source artifacts |
| Freeze protocol before fresh-corpus unblinding | RQs, metrics, thresholds, exclusions, timing, comparison, and stop conditions preregistered |

### P1 — strongly recommended

| Item | Reason and acceptable disposition |
|---|---|
| Exact dependency locking/constraints | Reduce environment drift beyond minimum version ranges; record platform-specific lock strategy |
| Privacy-minimized research mode | Avoid storing unnecessary raw metadata/evidence; define redaction and raw-artifact access |
| Baseline provenance policy | Make creator/source/fingerprint/approval/trust explicit before claiming integrity monitoring |
| Suppression governance | Require narrow scope, documented rationale, review, and optional expiry/owner |
| Additional resource worst-case benchmarks | Measure nested structures, many tools, many matches, decoding candidates, and output pressure |
| Documentation consistency audit | Align README, manual, CLI help, schemas, threat model, and thesis claims after implementation |
| Historical migration documentation | Explain which fields are comparable and why old metrics must not be regenerated under current logic |
| Cross-platform reproducibility check | At least document Windows reference behavior and, if feasible, one independent environment smoke reproduction |

### P2 — optional or research-question dependent

- cryptographic signing/attestation of baselines and release artifacts;
- a graphical interface or dashboard;
- an additional platform matrix;
- richer suppression workflow/UI;
- multilingual development coverage;
- externally maintained threat-intelligence mappings;
- runtime gateway integration; and
- advanced provenance systems.

P2 work must not delay a defensible bounded FYP or expand the primary
construct without supervisor approval.

---

## 9. Versioning strategy

History should be extended, never rewritten.

| Layer | Preserved/current identity | Future strategy |
|---|---|---|
| Historical v0.2 | Confirmatory pilot baseline and H0 artifact | Keep commit, artifact, hashes, schema, configuration, and narrative immutable. Never regenerate H0 with newer code. |
| v0.3.0a1 | Post-unblinding exploratory candidate | Keep its exploratory designation and dirty-state provenance. Do not promote its exposed-holdout result to confirmation. |
| Engineering remediation | Not yet implemented | Use the next appropriate pre-release. A pipeline-only repair may advance the current pre-release series; construct/rule changes may justify the next pre-1.0 minor line. Supervisor/release review chooses the exact number. |
| Frozen formal-FYP candidate | Future | Create from a clean, fully tested commit; record immutable Git tag, package/wheel hashes, rule-pack version, decision-semantics version, and configuration hash. |
| Future confirmatory evidence | Future | Bind the one primary artifact to the frozen candidate, fresh corpus hash, exact invocation, environment, and preregistration. |

### Identity rules

- **Package version:** changes whenever distributed implementation behavior or
  public interfaces change. Do not reuse `0.3.0a1` for remediated code.
- **Rule-pack version:** changes whenever built-in rule identity, matching,
  severity, or detector-family membership changes. A pure scanner
  decision/presentation fix may leave it unchanged.
- **Configuration identity:** must include everything that can change a
  prediction or experiment interpretation, including threshold, enabled rules,
  custom rules, suppressions, decision-semantics version, and security-
  significant limits. Presentation-only preferences may be separately hashed
  but must not affect the decision hash.
- **Artifact schema:** use a major revision for the new explicit decision
  state, provisionally 4.0.0. Continue to load 3.0.0 and 3.1.0 using their
  historical semantics; do not backfill invented state.
- **Git tags:** use immutable annotated tags only after all freeze gates pass.
  If a tag is wrong, create a corrective tag/release; do not move the original.
- **Experiment ID:** derive or record a unique ID bound to the candidate,
  corpus, configuration, timing protocol, and UTC run—not merely a filename.

Any change after detector freeze that could affect predictions invalidates the
candidate freeze and requires a new version/configuration identity and renewed
approval. Any change after primary unblinding is exploratory unless the
preregistered protocol explicitly permits it.

---

## 10. Development-data strategy

The existing 80-sample development corpus remains useful for regression,
failure reproduction, and historical comparison, but its synthetic-heavy,
English-only, balanced, taxonomy-author-generated character limits external
validity. Future development data may be expanded freely **before detector
freeze** provided its provenance is documented and it remains separate from
the future holdout.

### Development goals

| Weakness | Development response |
|---|---|
| Synthetic-heavy bias | Add approved, legally usable realistic metadata structures or realism-informed synthetic cases; clearly mark provenance |
| English-only bias | Decide with the supervisor whether English remains an explicit scope limit or whether multilingual development is justified |
| Taxonomy-author bias | Ask people who did not write the detector rules to propose examples and benign counterexamples |
| Benign realism | Include ordinary descriptions, administration tools, credentials-management terminology, encodings, long schemas, and disclosed powerful capabilities |
| Suspicious diversity | Vary wording, purpose, field structure, directness, target, and multi-construct interactions |
| Adaptive paraphrases | Use a documented development transformation set; keep it out of the future primary panel |
| Boundary cases | Add near-threshold, ambiguous, malformed-but-benign, and disclosed-capability hard negatives |
| Category coverage | Track a matrix of construct, field location, representation, difficulty, provenance, and language |

### Contamination firewall

1. Maintain separate development and holdout custodians/directories/manifests.
2. Record each development sample's author, date, rationale, source/license,
   construct, and whether it came from a known failure.
3. Search for exact canonical overlap and perform an independent near-
   duplicate review before the holdout is frozen.
4. Never copy a future holdout failure into development until after the
   primary run; then label the copy as post-unblinding exploratory material.
5. Do not expose holdout text, reviewer notes, labels, or predictions to
   detector developers.
6. Do not use future holdout performance to select rules, thresholds,
   suppressions, or stopping points.
7. Version development manifests separately so historical tests remain
   reproducible.

### Data balance inside development

A balanced development corpus is convenient for ensuring both positive and
negative coverage; it must not be used to infer deployment precision.
Development should emphasize **coverage and hard counterexamples**, not mimic
one assumed production prevalence. Keep separate analyses for:

- core suspicious constructs;
- security-quality warnings;
- legitimate powerful tools;
- ambiguous cases;
- multi-construct cases;
- representation transformations; and
- resource-bound cases.

No new samples are created by this blueprint.

---

## 11. Fresh untouched holdout design

A future holdout becomes meaningful only after the candidate detector,
construct, threshold, and primary analysis are frozen. The project must not
construct it during exploratory rule development.

### Mandatory principles

1. **Post-freeze creation:** approve and freeze the detector first.
2. **Independent authorship:** use authors/custodians who have not tuned the
   detector where feasible; provide them the construct guide, not rule regexes
   or known detector blind spots.
3. **Separation:** detector developers receive identifiers/aggregate progress
   only, not content or provisional labels.
4. **Blinded review:** reviewers do not see expected labels or detector
   predictions.
5. **Adjudication:** preserve raw reviewer decisions and resolve disagreements
   through the approved protocol.
6. **Immutable freeze:** freeze sample bytes, manifest, labels, reviewer
   source, and protocol; calculate and record hashes.
7. **Leakage checks:** detector-free exact canonical overlap plus independent
   near-duplicate review across development and holdout.
8. **Preregistration:** freeze metrics, thresholds, exclusions, timing,
   comparison, CIs, and analysis before detector unblinding.
9. **One primary evaluation:** execute once, preserve the raw artifact
   immediately, and never silently overwrite/rerun it.
10. **Separation after unblinding:** all later tuning and reruns are marked
    exploratory.

### Prevalence design options

| Option | Advantage | Cost/risk | Appropriate claim |
|---|---|---|---|
| Balanced controlled panel | Efficient estimates of sensitivity and false-positive behavior with similar positive/negative counts; easy category coverage | Precision/accuracy do not represent deployment prevalence; may be synthetic | Controlled effectiveness under the panel design |
| Prevalence-oriented corpus | Precision and alert burden may better reflect the sampled setting | Requires defensible source population and more samples to obtain enough suspicious cases | Performance for that defined sampling frame, not all MCP ecosystems |
| Dual-panel design | Balanced diagnostic panel plus prevalence-oriented sample separates coverage from alert burden | More author/reviewer effort and analysis; multiplicity/scope | Controlled construct detection plus a separate realism/prevalence estimate |
| Case-control plus prevalence reweighting | Efficient positive collection and scenario-based precision estimates | Depends heavily on externally justified prevalence assumptions | Sensitivity/specificity plus transparent scenario analysis |

The supervisor should choose based on the thesis claim, accessible sampling
frame, resources, and ethics. A 50/50 corpus is not inherently wrong, but its
precision and accuracy must not be described as deployment performance.

### Corpus structure

The final manifest should include stable opaque IDs; split, corpus name and
version; expected class/construct; allowed stratification fields; provenance
category without identities where privacy requires; review status; and
canonical corpus hash. Sample files should not include detector predictions.

Matched pairs can improve hard-negative design, but paired dependence must be
recorded and reflected in statistical interpretation. If independent samples
and matched pairs coexist, declare cluster/pair IDs before analysis.

### Custody and unblinding

Prefer an independent custodian or supervisor-controlled directory for the
final corpus. The evaluator should consume a frozen manifest without allowing
the developer to browse individual content. Logs and filenames must not leak
labels. Unblinding occurs only when the approved primary command runs, and the
resulting artifact is copied to an immutable/read-only evidence location and
hashed.

---

## 12. Reviewer protocol

| Model | Benefit | Cost/limitation | Suitable use |
|---|---|---|---|
| One blinded reviewer | Lowest cost; better than author-only labels | Individual bias cannot be separated; disagreement estimate is fragile | Minimum pilot only, with narrow claims |
| Two independent blinded reviewers | Measures inter-reviewer reliability without discussion contamination | Approximately doubles review effort; disagreements remain unresolved | Practical formal-FYP minimum if feasible |
| Two reviewers plus adjudicator | Preserves independence and produces a reasoned final label | Additional expert/time; adjudicator may introduce own bias | Strong practical protocol |
| Domain-expert review | Better MCP/security interpretation | Expert availability, cost, and possible shared assumptions | Useful reviewer or adjudicator role, not automatically objective truth |

### Recommended practical minimum for supervisor discussion

Use **two independent blinded reviewers**, followed by adjudication of
disagreements by a third qualified person or a pre-appointed supervisor/
adjudicator. If resources make this impossible, record an explicit supervisor
decision to use one reviewer, retain abstentions, narrow conclusions, and
present single-reviewer bias as a major limitation.

### Review packet

Reviewers should receive:

- the approved construct guide with positive/negative boundary examples;
- sample content with random ordering and opaque IDs;
- separate decisions for class, construct, field, confidence/difficulty, and
  abstention;
- no expected labels, detector outputs, rule IDs, threshold, or prior reviewer
  decisions; and
- instructions for recording rationale without modifying the sample.

### Agreement and adjudication

- Report raw binary agreement and Cohen's kappa when its assumptions fit.
- For multiple constructs, report per-construct agreement or an appropriate
  multi-label statistic selected with supervisor/statistical advice.
- Report abstentions and missing decisions.
- Preserve every raw reviewer source and hash before adjudication.
- Adjudication creates a new record linking the original decisions; it never
  overwrites them.
- Difficulty disagreement should be reported separately; it is not the same as
  label disagreement.
- High kappa does not prove the construct is valid, samples are representative,
  or the detector is accurate.

---

## 13. Sample-size and statistics planning

This blueprint deliberately does not invent a sample count. Choosing N before
deciding the estimand and desired uncertainty would create false precision.

### Inputs required before choosing N

| Input | Why it matters |
|---|---|
| Primary outcome(s) | Recall requires enough suspicious cases; FPR requires enough benign cases |
| Plausible recall/FPR | Interval width is widest around moderate probabilities and depends on the anticipated value |
| Desired confidence-interval width | Defines the precision the thesis needs, rather than merely “more samples” |
| Target prevalence/sampling design | Determines positive/negative counts and whether precision is directly interpretable |
| Category-level claims | Each claimed stratum needs enough independent cases; total N can conceal tiny cells |
| Paired comparison plan | Power depends on discordant pairs, not only total sample count |
| Matched/clustered samples | Dependence reduces effective information and changes analysis |
| Reviewer model | More samples multiply review and adjudication workload |
| Time and available metadata | Feasibility may require narrowing claims instead of accepting underpowered strata |
| Anticipated abstention/exclusion | The final analyzable count may be lower than the authored count |

### Questions for supervisor/statistical consultation

1. Is recall the single primary endpoint, or are recall and FPR co-primary?
2. What interval width would be useful for the conclusion?
3. Is the corpus a balanced construct panel or a sample from a defined
   population?
4. Are category-level estimates claims or only diagnostics?
5. Is a paired comparison with v0.2 part of the thesis?
6. Should multiplicity control apply to multiple primary endpoints or
   comparisons?
7. How should matched pairs/clusters be accounted for?
8. Which interval/test is appropriate for paired proportions and small cells?
9. How will reviewer abstentions and exclusions be handled?

### Candidate methods—not final selections

- Wilson or exact binomial intervals for single proportions;
- paired outcome tables and an exact McNemar-style analysis for a genuinely
  paired detector comparison;
- cluster/pair-aware bootstrap intervals if justified and implemented before
  unblinding;
- precision-based sample-size calculation for recall/FPR;
- power analysis for the paired difference only after a defensible discordant-
  pair expectation exists; and
- transparent descriptive reporting where sample size cannot support
  inferential category claims.

N must be approved and justified in the formal methodology. “48 because the
pilot used 48” is not a sufficient reason.

---

## 14. Metric plan

| Metric | Proposed role | Rationale and caveat |
|---|---|---|
| Recall/sensitivity | **PRIMARY** | Missing suspicious constructs is the pilot's main weakness. Define the positive construct and denominator exactly. |
| False-positive rate | **PRIMARY safety endpoint or key SECONDARY** | Quantifies benign tools incorrectly alerted. The supervisor must decide whether it is co-primary or a preregistered guardrail. |
| Precision | **SECONDARY** | Answers how many alerts are true under the corpus sampling prevalence. Not deployment precision for a balanced case-control panel. |
| F1 | **SECONDARY** | Compact balance of precision and recall, but hides asymmetric costs and prevalence dependence. |
| Accuracy | **DIAGNOSTIC** | Easy to understand but misleading under imbalance; never the only primary metric. |
| Specificity | **DIAGNOSTIC** | Equivalent information to 1 − FPR; useful for some audiences but avoid redundant headline claims. |
| 95% confidence intervals | **REQUIRED companion** | Report for primary and important secondary proportions; state method and unit/dependence. |
| Per-construct/category recall | **DIAGNOSTIC unless powered and preregistered** | Locates blind spots; small cells cannot support strong comparative claims. |
| Per-field/difficulty/provenance strata | **DIAGNOSTIC** | Useful failure analysis; high multiplicity and subjective strata require restraint. |
| Analysis-core latency | **SECONDARY engineering** | Measures detector/normalization core under fixed protocol. |
| Static end-to-end latency | **SECONDARY engineering** | Includes safe load/validation/report preparation as defined; excludes network retrieval unless separately studied. |
| Mean, median, p95 | **SECONDARY/DIAGNOSTIC latency** | Median for typical behavior, p95 for tail, mean for total workload; report sample/repetition basis. |

### PR-oriented metrics

If a future corpus reflects an imbalanced sampling frame and the detector
exposes a meaningful ordered score across preregistered thresholds, a
precision-recall curve or average precision may be informative. The current
risk score is a deterministic policy score, not proven probability
calibration. Do not add AUPRC merely because it is available, and do not tune a
threshold on the confirmatory holdout.

### Threshold policy

MEDIUM is the preserved historical threshold, not automatically the future
answer. Any future threshold must be selected using theory, risk policy, and
development-only evidence before holdout construction/unblinding. Alternative
thresholds may be preregistered as secondary sensitivity analysis; the primary
threshold cannot be chosen after seeing holdout results.

---

## 15. Comparison and baseline plan

### Meaningful comparisons

1. **Absolute frozen-candidate effectiveness** is the primary result. A
   detector must be interpretable without relying only on relative gain.
2. **Historical v0.2 on the same fresh corpus** is a useful paired secondary
   baseline if its exact implementation/environment can be reproduced and the
   future construct is compatible. This creates a new comparison; it does not
   change the old H0.
3. **Seven detector-family ablations** can remain preregistered secondary
   contribution analyses. They show dependence on this corpus/configuration,
   not causal real-world importance.
4. **Simple lexical baseline** is meaningful only if the literature or
   methodology motivates a transparent baseline defined and frozen before
   unblinding.
5. **No-decoding baseline** is meaningful if bounded representation decoding
   is an explicit design hypothesis.
6. **Alternative thresholds** belong to preregistered sensitivity analysis,
   not post-hoc selection.
7. **External tools** should be compared only if the literature identifies a
   genuinely comparable, available tool and licenses/configurations permit a
   fair reproducible test. This blueprint invents none.

### Fair-comparison requirements

- same sample bytes and ground truth;
- exact version/commit/configuration for each system;
- comparable decision unit and threshold semantics;
- no tuning on the comparison corpus;
- paired outcome preservation;
- limitations where systems target different constructs; and
- raw artifacts separated and hashed.

The future preregistration must specify which comparisons are inferential,
descriptive, or exploratory and how multiple comparisons will be handled.

---

## 16. Latency benchmark plan

### Environment record

Record machine model/class, CPU, logical cores, RAM, storage where relevant,
OS/build, architecture, Python implementation/version, package/wheel hash,
dependency lock hash, power mode, virtualization, and known background-load
conditions. Avoid usernames, secrets, and unnecessary absolute private paths.

### Workloads and boundaries

| Boundary | Starts | Ends | Includes | Excludes |
|---|---|---|---|---|
| Analysis-core | Validated/loaded input is supplied to normalized analysis | Decision and bounded presentation states are produced | Normalization if the implementation's existing boundary says so, traversal, detectors, suppressions, risk/decision | File/network retrieval and final serialization unless explicitly defined |
| Static end-to-end | Local frozen input processing begins | Selected artifact/report object is ready or safely written, as preregistered | Load, validate, analyze, decision, bounded reporting/serialization | Interactive display and remote retrieval |
| Resource stress | Adversarial within-limit fixture begins | Safe result/rejection | Specified worst-case path | Primary-effectiveness timing |

The exact existing instrumentation must be inspected and documented before
freeze; names alone do not define boundaries.

### Protocol

- choose warm-up and measured repetition counts before unblinding;
- fix corpus order or use a seeded/preregistered order;
- run each boundary separately;
- avoid concurrent quality gates and obvious background load;
- report sample count, repetitions, total invocations, median, mean, p95,
  dispersion, and maximum where useful;
- retain raw duration records, not only summaries;
- state timer and units;
- do not mix retrieval latency into static analysis;
- rerun only according to predefined invalid-run criteria; and
- do not compare machines as though hardware/environment differences were
  detector changes.

### “Lightweight” claim boundary

Evidence may support:

> On the documented reference machine and workload, the frozen inspector
> completed analysis-core/static end-to-end processing within the reported
> distribution and resource limits.

It cannot support “fast on all MCP deployments,” hard real-time suitability,
or cross-machine superiority without broader benchmarking.

---

## 17. Adversarial-robustness plan

### Development robustness tests

These are visible, repeatable, and may guide engineering before freeze:

| Variation | Expected property or question |
|---|---|
| Whitespace and key ordering | Canonical identity/decision should remain stable where JSON meaning is unchanged |
| Unicode NFC-equivalent forms | Normalized fingerprints and lexical decisions should be invariant |
| Unicode confusables/zero-width content | Explicitly test documented coverage and safe failure; do not assume NFC solves confusables |
| Supported encoding | OBF-005 uses strict depth-one bounded decoding; decoded core constructs should be found within limits |
| Unsupported/nested encoding | Must remain inert and bounded; expected misses are documented |
| Field relocation | Test only fields the threat model says are security relevant; relocation outside scanned scope is a declared limitation |
| Paraphrase | Measure known lexical/contextual brittleness with an independently authored development set |
| Benign vocabulary collision | Add hard negatives for “ignore,” “token,” “secret,” “system,” “base64,” commands, paths, and administration contexts |
| Cross-field inconsistency | Vary declared purpose, parameters, annotations, and capability disclosure |
| Multilingual text | Run only if language coverage becomes in scope; otherwise document as unsupported |

Metamorphic tests should state whether a transformation is expected to
preserve **canonical identity**, **security meaning**, **rule output**, or only
**classification**. Those are not interchangeable.

### Untouched robustness evidence

If robustness becomes a formal RQ, create a separate post-freeze panel or
predeclare robustness strata within the fresh holdout. Detector developers
must not see its base cases or transformations. A visible development
transformation suite cannot confirm generalization.

### Bounds

Robustness work remains static, inert, and limited to approved
representations. No recursive/general-purpose decoder, malware unpacker, model
execution, or remote crawler should be introduced merely to improve a
robustness score.

---

## 18. Ethics and data governance

Real-world MCP metadata may contain credentials, personal data, proprietary
descriptions, harmful instructions, or material whose redistribution is not
permitted. “Publicly reachable” does not automatically mean ethically or
legally reusable.

### Questions for the university/supervisor

- Does collection of public tool metadata require ethics review or exemption?
- Is consent required for private/server-owner-supplied metadata?
- What institutional policy applies to credentials, personal data, malicious
  content, or vulnerability disclosure?
- May raw metadata be redistributed in the thesis repository?
- What retention period, storage location, access list, and deletion process
  are required?
- Can reviewers safely be exposed to malicious/instructional content, and what
  briefing/support is necessary?
- When should a discovered live vulnerability be disclosed, to whom, and
  before what publication?

### Data-handling blueprint

| Stage | Minimum control |
|---|---|
| Collection | Written source/license/permission, purpose limitation, no authentication bypass, no secret harvesting |
| Ingestion | Quarantine as inert text; static analysis only; size/resource limits |
| Screening | Detect and isolate credentials/personal data before normal reviewer distribution |
| Storage | Least-access location, encryption/access controls according to university policy, separate identity mapping if needed |
| Labelling/review | Opaque IDs, minimum necessary content, reviewer briefing, no detector predictions |
| Artifact creation | Prefer aggregate outcomes and hashed identities; minimize or redact raw evidence where reproducibility permits |
| Repository publication | Publish only cleared/redacted/licensed content; never expose credentials or private metadata |
| Retention/deletion | Follow approved schedule; document what evidence remains reproducible after redaction |
| Disclosure | Use a supervisor-approved responsible-disclosure path for credible live issues |

Synthetic data remains valuable where real metadata cannot be safely shared,
but its realism limitation must be explicit. A mixed strategy may preserve
privacy while improving structure realism. Ethics approval must not be assumed
by this blueprint.

---

## 19. Literature-review research matrix

This is a search agenda, not a list of citations. Future work must locate and
critically read primary standards, official specifications, peer-reviewed
research, and relevant security guidance. No paper is fabricated here.

| Topic | Why needed | Questions to answer | Thesis support | Claim that depends on it |
|---|---|---|---|---|
| MCP architecture | Establish technical context | What are host, client, server, discovery, tool definitions, transports, and trust assumptions? Which metadata fields are normative? | Introduction, system model | Why tool metadata crosses an agent trust boundary |
| MCP security | Position known controls/gaps | What official security guidance exists? Which attacks concern authorization, metadata, transport, consent, and execution? | Threat model, related work | What MCP risks this static inspector does and does not address |
| Tool poisoning | Define the motivating concept | How is it defined in credible sources? Is intent, metadata manipulation, or successful agent influence required? | Construct validity | Whether “tool poisoning” may appear in title/labels |
| Prompt injection | Distinguish instruction attacks | How do direct attacks work, and which mechanisms transfer to tool metadata? | Detector taxonomy | Why injection-like metadata is security relevant |
| Indirect prompt injection | Explain untrusted context channels | What evidence exists for instructions embedded in retrieved/tool content? How is success measured? | Threat model | Why metadata can influence an agent without user-authored prompts |
| Agent/tool trust | Model authorization and boundaries | How do agents select tools and rely on descriptions/schema? What trust/consent models exist? | Architecture/threat model | Why capability mismatch and metadata integrity matter |
| Static analysis | Justify non-execution approach | What are soundness/completeness trade-offs and common representations? | Design | What static inspection can and cannot infer |
| Rule-based security detection | Motivate deterministic rules | What strengths, explainability benefits, maintenance costs, and evasion limits are established? | Detector design/discussion | Why a rule-based undergraduate prototype is reasonable |
| Schema integrity | Ground schema checks | Which JSON Schema/MCP constraints are normative? What security consequences follow from malformed/ambiguous schemas? | Taxonomy, validation | Why schema findings are quality warnings rather than automatic malicious labels |
| Configuration drift | Frame baselines/fingerprints | How are canonicalization, provenance, approved state, and TOCTOU handled in comparable systems? | Optional drift RQ | What “integrity drift” means and what it does not prove |
| Security-detector evaluation | Choose metrics/protocol | How should recall, FPR, precision, prevalence, uncertainty, paired tests, and leakage be handled? | Methodology | Why the primary metrics and holdout design are defensible |
| Adversarial robustness | Bound adaptive testing | How are transformations, evasion, distribution shift, and adaptive attackers evaluated without leakage? | Robustness plan | What robustness conclusions can be made |
| Human annotation/reliability | Improve labels | Which blinding, adjudication, agreement, abstention, and construct-validity practices fit this task? | Review protocol | Why labels are credible yet still uncertain |
| Reproducible security experiments | Preserve evidence | What artifact, environment, preregistration, and provenance practices are recommended? | Reproducibility | Why the experiment can be independently audited |
| Safe output/CSV/SARIF | Validate reporting controls | Which terminal and spreadsheet injection risks apply, and what does SARIF require? | Implementation | Why reporting is part of the attack surface |

### Literature workflow

For each accepted source, record bibliographic data, source type, method,
population/system, exact construct, result, limitation, and the thesis claim
it supports. Separate authoritative specifications from empirical evidence
and opinion. Search dates and inclusion/exclusion criteria should be
documented if the literature review is systematic enough to imply coverage.

---

## 20. System architecture for the formal FYP

Continuity with the tested prototype is preferable to a rewrite: it preserves
known security boundaries, tests, historical compatibility, and a clear
engineering lineage. Refactor only where a documented defect or approved
research question requires it.

### KEEP

| Component | Why keep |
|---|---|
| `loader.py` and `resource_policy.py` | Bounded hostile-input boundary |
| `normalizer.py` | Typed validation, alias-conflict handling, Unicode NFC |
| `detectors/` and data-only `rules/` | Deterministic/explainable detector architecture |
| `risk.py` mathematical policy | Preserve unless the supervisor approves a separate pre-freeze research/engineering change |
| `fingerprint.py`, `baseline.py`, `compare.py` | Canonical identity and drift lineage |
| `retrieval.py` loopback-only boundary | Explicit opt-in, no redirects/proxies, no invocation |
| `reporter.py` safe formats | Terminal/CSV/SARIF safety is security-critical |
| `evaluation/` artifact and corpus framework | Strong reproducibility base, subject to decision-state schema evolution |
| Historical schema loaders | Prevent present code from rewriting past meaning |

### REFACTOR BEFORE FREEZE

1. Split scan flow into detection, decision, and presentation states.
2. Make decision accumulation bounded and independent of finding retention.
3. Route risk, `--fail-on`, affected counts, and evaluation through decision
   state.
4. Introduce explicit schema/decision-semantics identity and historical
   compatibility tests.
5. Make research freeze/hashing robust to platform newline behavior.
6. Separate privacy-minimized artifact fields from optional protected raw
   evidence.
7. Centralize and document provenance for baselines, suppressions,
   configuration, and artifact creation.
8. Validate resource worst cases against a written budget.

### OPTIONAL EXTENSION

- independently justified lexical/no-decoding baseline;
- approved robustness transformation harness;
- a constrained privacy-safe real-metadata importer;
- baseline approval/provenance fields;
- suppression owner/reason/expiry metadata;
- a second-platform reproduction script; or
- a small read-only results visualization for the thesis.

### DO NOT ADD unless the research question changes

- LLM/ML classifier;
- general MCP gateway or runtime proxy;
- agent/tool execution sandbox;
- recursive/general-purpose decoding;
- remote crawling or malware analysis;
- cloud dashboard/account system;
- automated “fix” or remediation engine;
- broad multilingual detector; or
- large threat-intelligence ingestion.

Every optional extension consumes validation and thesis space. It should enter
scope only through the supervisor decision register.

---

## 21. Future testing strategy

### Test layers

| Layer | Purpose | Representative future coverage |
|---|---|---|
| Unit | Local deterministic functions | Normalization, severity ordering, risk accumulator, retention ranking, hashes |
| Regression | Prevent known defect recurrence | Finding-budget coupling, historical detector cases, output escapes |
| Security boundary | Enforce inert/static trust boundary | No execution/fetch; loopback retrieval; redirects/proxies denied; hostile output neutralized |
| Resource exhaustion | Prove bounded failure | Oversized JSON, deep nesting, many tools/fields/matches, decoding limits, evidence/report pressure |
| Property/invariant | Explore combinations | Budget/order invariance, canonical equivalence, accumulator/reference equivalence, deterministic output |
| Compatibility | Preserve historical truth | Schema 3.0.0/3.1.0 fixtures, legacy rule identity, 4.x rejection/migration |
| CLI | Verify user-visible decisions | Exit codes, `--fail-on`, format options, truncation disclosure, invalid configurations |
| Packaging | Reproduce installed behavior | Build wheel/sdist, metadata, clean-environment install, wheel smoke |
| Research integrity | Prevent leakage/miscomparison | Corpus hashes/overlap, config hash, clean state, artifact identity, comparison compatibility |

### Finding-budget fix matrix

| Scenario | Required invariant |
|---|---|
| Global cap exhausted before final tool | Final tool decision/risk/fail/evaluation unchanged |
| Per-tool cap zero/small | Tool still affected; visible omission declared |
| Evidence limit zero/small | Rule/severity/risk unchanged; evidence safely omitted |
| Different catalog order | Per-tool decisions and aggregate effectiveness identical |
| Findings tie under retention ranking | Stable deterministic selection |
| Many low findings then one critical | Critical decision retained in decision state even if not displayed |
| Suppressed high finding | Does not affect decision; audit count remains correct |
| Redacted sensitive evidence | Decision attributes preserved; output contains no raw secret |
| Risk synergy across omitted details | Aggregate risk matches full reference |
| Custom plus built-in rules | Same suppression/decision/retention pipeline |
| Intentional accumulator saturation | Explicit complete result if mathematically sufficient; otherwise indeterminate/fail-closed |
| Old artifact comparison | Legacy semantics preserved or comparison rejected with reason |

### Property and metamorphic candidates

- NFC-equivalent strings have identical normalized fingerprint and expected
  lexical behavior.
- Object key order does not change canonical hash.
- Adding only presentation budget cannot change decision state.
- Removing a suppression cannot reduce the set of decision-contributing
  matches.
- Increasing a presentation budget cannot remove an already retained finding
  under the chosen stable policy.
- A current artifact round-trip preserves every identity and decision field.
- Invalid or missing decision-semantic fields never default to “benign.”

### Quality gate before candidate freeze

Run from a clean environment:

1. `ruff check .`
2. `ruff format --check .`
3. `mypy src`
4. `python -m pytest --cov=mcpsec --cov-report=term-missing`
5. detector-free corpus integrity checks
6. `python -m build`
7. clean installed-wheel smoke test
8. `git diff --check` and clean-status verification

The future process must inspect tests before broad execution if a test corpus
could expose the final holdout. The fresh holdout should not live where normal
pytest discovery invokes detection.

---

## 22. Future preregistration template

This is an empty template. Values in braces must be resolved and frozen; they
are not supplied by this blueprint.

### Study identity

- Study title: {title}
- Research framing: {approved framing}
- Primary research question: {RQ}
- Secondary questions: {list or none}
- Preregistration version/date/location/hash: {values}
- Supervisor approval reference: {record}

### Construct and threat model

- Core target definition: {definition}
- Supporting/warning constructs: {definitions}
- Positive unit and negative unit: {definitions}
- Inclusion/exclusion boundary: {rules}
- Threat-model version/hash: {identity}
- Declared non-goals: {list}

### Detector freeze

- Package version: {version}
- Git commit and immutable tag: {identity}
- Git dirty state: {must be clean}
- Wheel/source hashes: {hashes}
- Built-in rule-pack version and rule IDs: {identity/list}
- Decision-semantics version: {version}
- Artifact-schema version: {version}
- Threshold: {value}
- Custom rules: {none or frozen identity}
- Suppressions: {none or frozen identity}
- Configuration hash and canonical form: {identity}
- Resource/decision limits: {values}
- Presentation limits: {values, non-decision}

### Corpus and labels

- Corpus name/version/split: {identity}
- Sample count and class/construct counts: {values}
- Sampling/prevalence design: {design}
- Corpus hash: {hash}
- Development/holdout overlap result: {evidence}
- Near-duplicate review: {evidence}
- Label guide version/hash: {identity}
- Review protocol/reviewer roles: {protocol}
- Adjudication protocol and status: {protocol/status}
- Final label manifest hash: {hash}

### Primary analysis

- Primary endpoint(s): {metric(s)}
- Direction/estimand: {definition}
- Confidence-interval method/level: {method}
- Primary decision threshold: {frozen value}
- Unit of analysis and dependence handling: {definition}
- Missing/abstention handling: {rule}
- Exclusion criteria: {objective pre-run criteria}
- Analysis script/version/hash: {identity}
- Multiplicity handling: {rule}

### Secondary/diagnostic analysis

- Secondary metrics: {list}
- Stratifications: {list and claim status}
- Baseline/comparison plan: {systems/configurations}
- Paired statistical method: {if applicable}
- Ablation set and purpose: {list}
- Robustness analysis: {design or none}

### Timing protocol

- Machine/runtime identity: {values}
- Timing boundaries: {definitions}
- Warm-ups/repetitions: {values}
- Corpus order/seed: {value}
- Summary statistics: {list}
- Invalid timing-run criteria: {rules}

### Execution and preservation

- Exact primary command: {command}
- Working directory/environment activation: {safe normalized details}
- Artifact output directory/name: {path/convention}
- Experiment ID procedure: {method}
- UTC timestamp capture: {method}
- Raw artifact preservation/hash procedure: {steps}
- Stop conditions: {conditions}
- Authorized operator/custodian: {roles}

### Fields that must be frozen before unblinding

Every field above that could affect sample inclusion, labels, predictions,
metrics, thresholds, comparisons, timing interpretation, exclusions, or
artifact identity must be frozen. Only purely administrative fields such as
the actual UTC start time and generated experiment ID can be populated during
the run under their predeclared procedure.

---

## 23. Experiment freeze GO / NO-GO checklist

The future primary experiment is **NO-GO** if any critical item is missing.

| Checkpoint | PASS evidence required | Critical |
|---|---|---|
| Research framing approved | Supervisor decision record | Yes |
| Construct frozen | Versioned definition/annotation guide/hash | Yes |
| Threat model approved | Assets, boundaries, goals/non-goals frozen | Yes |
| Research questions/objectives frozen | Preregistration | Yes |
| Finding-budget coupling fixed | Decision/presentation invariance tests | Yes |
| Decision/resource behavior bounded | Worst-case tests and explicit failure semantics | Yes |
| Detector frozen | Clean commit, immutable tag, package/wheel hash | Yes |
| Rule pack and threshold frozen | Versions/list/config hash | Yes |
| Custom rules/suppressions frozen | “None” or exact reviewed identities | Yes |
| Historical compatibility green | Schema/legacy fixture tests | Yes |
| Full quality gates green | Lint, format, mypy, coverage, build, wheel smoke | Yes |
| Dependencies reproducible | Approved lock/constraint and runtime record | Yes |
| Fresh corpus created after freeze | Custodian evidence | Yes |
| Corpus untouched by developer | Access/unblinding record | Yes |
| Cross-split integrity clean | Exact and near-duplicate evidence | Yes |
| Human review complete | Raw blinded reviews, agreement/adjudication | Yes |
| Labels and sample bytes frozen | Immutable hashes | Yes |
| Sampling/prevalence documented | Methodology | Yes |
| Sample-size rationale approved | Precision/power/workload decision | Yes |
| Primary metrics and CIs frozen | Preregistration | Yes |
| Comparison/ablation plan frozen | Preregistration or explicit none | Yes |
| Timing protocol frozen | Boundary, machine, repetitions, summaries | Yes |
| Exclusions and stop rules frozen | Objective rules | Yes |
| Configuration/corpus hashes independently verified | Two-person or scripted audit evidence | Yes |
| Artifact path and no-overwrite behavior ready | Dry run on non-holdout smoke data | Yes |
| Reproducibility metadata ready | Schema validates all required fields | Yes |
| Ethics/data authorization resolved | Required approval/exemption/permissions | Yes if real data/policy requires |
| Repository clean immediately before run | `git status --porcelain` empty | Yes |
| Supervisor authorizes unblinding | Dated approval | Yes |

If a gate fails, record NO-GO and fix it without inspecting predictions.
Changing detector or protocol after the fresh corpus becomes visible requires
a new freeze and, normally, a new untouched corpus.

---

## 24. Post-experiment protocol

### Immediately after the one primary run

1. Stop any automatic retry mechanism.
2. Confirm the command exit state and artifact existence without editing it.
3. Copy/preserve the raw artifact using a no-overwrite operation under the
   approved evidence procedure.
4. Calculate its SHA-256 and record file size, experiment ID, UTC timestamp,
   commit, dirty state, corpus hash, configuration hash, and invocation.
5. Validate artifact schema and internal identities.
6. Set read-only/immutable storage controls where available.
7. Have a second person or independent script verify the recorded hash.
8. Record any operational anomaly before viewing aggregate effectiveness.

If the primary command fails or the artifact is corrupt, follow only the
preregistered stop/recovery criteria. Do not silently rerun. Preserve the
failed artifact/log and obtain supervisor authorization for any replacement
run; label both.

### Primary analysis

- use the preregistered analysis implementation;
- compute only the frozen primary metrics and confidence intervals first;
- preserve sample-level outcomes for paired/diagnostic work in controlled
  storage;
- report denominator and missing/excluded cases;
- verify confusion-matrix arithmetic against the artifact;
- distinguish sampling prevalence from deployment prevalence; and
- publish the primary result regardless of whether it is favorable.

### Secondary and exploratory analysis

Run preregistered secondary metrics, comparisons, ablations, strata, and
timing next, with their declared status. Failure inspection, new categories,
threshold exploration, sample relabelling, detector edits, and new tests are
**post-unblinding exploratory** work. They may be valuable but must be placed
after the primary result and given a new version/commit/artifact identity.

### Preservation rule

Never overwrite raw primary data with a processed summary. Store:

- original artifact and SHA-256;
- immutable corpus/configuration/preregistration identities;
- analysis code and output;
- a machine-readable manifest linking them;
- any anomaly/decision log; and
- later exploratory artifacts in a visibly separate namespace.

---

## 25. Decision tree for unfavorable or ambiguous results

Poor results are scientifically valid results. They do not authorize
retrospective tuning of the frozen primary experiment.

| Observation | Confirmatory response | Allowed later exploratory response | Claim boundary |
|---|---|---|---|
| Recall remains poor | Report estimate/CI and failed constructs; retain frozen result | Analyze FNs, develop hypotheses, create a new version using development data | Detector did not identify many target cases in this corpus |
| FPR remains high | Report alert burden and benign failure classes | Investigate contextual constraints/hard negatives after result is frozen | High FPR limits practical use; do not hide it with a new threshold |
| Latency worsens | Verify protocol/artifact; report distribution and environment | Profile with non-holdout fixtures, optimize a new version | Only tested machine/workload is supported |
| A category fails completely | Report numerator/denominator and wide uncertainty | Treat as a blind-spot hypothesis; consider construct/refactor later | Zero observed recall in that small stratum is not universal impossibility |
| New false-positive class appears | Preserve examples according to privacy policy and quantify | Add post-unblinding regression/development cases | New mitigation cannot modify primary metrics |
| Worse than v0.2 | Verify paired identities and report honestly | Examine which semantic or construct changes caused differences | A newer version is not automatically better |
| Result is inconclusive | Report CI/limitations and avoid binary success/failure | Plan a better-powered independent study if feasible | Absence of evidence is not evidence of effectiveness or ineffectiveness |
| Primary artifact fails validation | Stop, preserve everything, apply preregistered recovery and supervisor decision | Repair framework only on smoke/development inputs | Replacement run must be disclosed and separately identified |
| Labels appear ambiguous after unblinding | Do not silently relabel primary data | Conduct a labelled sensitivity analysis or future improved study | Primary uses frozen labels unless preregistered error correction applies |
| Unexpected budget/decision anomaly | Stop analysis and assess protocol validity | Reproduce on non-holdout fixtures; new candidate/evaluation if required | Do not claim valid effectiveness from semantically compromised output |

### Simple decision sequence

1. **Is the artifact/protocol valid?** If no, preserve and escalate; do not
   reinterpret.
2. **Are primary estimates precise enough for the planned claim?** If no,
   conclude uncertainty.
3. **Did effectiveness meet a predeclared criterion, if one exists?** Report
   yes/no with intervals, not a marketing label.
4. **What explains errors?** Explore only after the primary record is frozen.
5. **Should engineering continue?** Decide using scientific value, practical
   constraints, and supervisor guidance—not by deleting unfavorable evidence.

---

## 26. Thesis evidence map

| Chapter | Current evidence | Future required evidence | Possible figures/tables | Supervisor decisions | Claims allowed |
|---|---|---|---|---|---|
| Introduction | Working bounded prototype; pilot motivation; MCP metadata security problem | Approved problem statement, scope, current literature | MCP trust-boundary diagram; contribution summary | Framing/title; core problem | A static-inspection problem exists and the project proposes a bounded design; no universal prevalence claim |
| Literature Review | Repository concepts and known limitations | Verified sources from Section 19; critical synthesis and gap | Related-work taxonomy; comparison matrix | Review scope; inclusion approach | Claims directly supported by cited specifications/research |
| Methodology | Pilot protocol, corpus/evaluation infrastructure, reviewer lessons | Approved construct/threat model, N rationale, fresh corpus/review, preregistration, ethics | Study flow; holdout firewall; variable/metric table | RQs, sample design, reviewers, statistics, ethics | The future experiment measures the operationalized construct under declared conditions |
| Design / Implementation | Loader, normalizer, 16 rules, risk, reports, baselines, retrieval, tests | Decision-state remediation, version/schema changes, clean freeze evidence | Pipeline/state diagram; detector taxonomy; bounds table | Architecture/refactor scope | The system is deterministic/static/bounded to the enforced and tested extent |
| Results | Historical H0 and exposed exploratory v0.3 evidence | One future raw primary artifact, CIs, approved comparisons/timing | Confusion matrix; CI plot; latency distribution; paired outcome table | Primary/secondary presentation | Exact estimates for the frozen corpus/configuration; v0.3 remains exploratory |
| Discussion | Known FP/FN patterns, threats, Day 6E audit | Interpretation of fresh results, literature comparison, practical implications | Error taxonomy; construct-by-result table | What constitutes acceptable contribution | Evidence-bounded explanations, not proof of intent or real-world generalization |
| Conclusion / Future Work | Engineering and research lineage | Synthesis linked to objectives and honest limitations | Objective-to-evidence table; roadmap | Final claim wording | What was designed, implemented, and observed; no claims beyond sampling/construct |

### Contribution categories to keep separate

- **Engineering contribution:** a deterministic, inert, bounded static
  inspection and integrity framework with safe outputs and reproducible
  artifacts.
- **Methodological contribution:** an explicit construct, freeze, review,
  holdout, and reproducibility protocol for this prototype.
- **Empirical result:** measured performance on the future frozen corpus.
- **Generalization evidence:** only the extent supported by independent
  authorship, sampling frame, N, intervals, and robustness design.

---

## 27. Phase-based FYP timeline

Dates must follow the university calendar. Advancement is gate-based.

### Phase 0 — Supervisor and methodology approval

- **Entry:** this blueprint and preserved Day 6 package are available.
- **Tasks:** agree framing, problem, construct direction, RQs, scope,
  contribution expectations, ethics questions, and meeting cadence.
- **Exit:** written decisions and open issues assigned.
- **Do not:** implement new rules, choose a result target, or create a holdout.

### Phase 1 — Literature and construct refinement

- **Entry:** provisional framing approved.
- **Tasks:** execute literature matrix; define observable constructs, threat
  model, annotation guide, non-goals, and hard-negative boundaries.
- **Exit:** supervisor-approved construct/threat-model versions and thesis
  literature outline.
- **Do not:** use detector behavior to redefine the target after the fact.

### Phase 2 — Engineering remediation

- **Entry:** construct and required engineering gates understood.
- **Tasks:** implement decision/detection/presentation separation, schema and
  version identities, newline/hash robustness, privacy/provenance improvements
  approved as P0/P1; add tests.
- **Exit:** all targeted remediation reviews/tests pass on development data.
- **Do not:** inspect or build the fresh holdout.

### Phase 3 — Development-only testing

- **Entry:** remediated architecture functional.
- **Tasks:** expand approved development data, benign hard negatives, property
  tests, robustness cases, resource tests, profiling, and documentation.
- **Exit:** candidate behavior understood; all rules/thresholds/configuration
  chosen using only development evidence.
- **Do not:** seek interim holdout feedback or stop when metrics “look good.”

### Phase 4 — Detector freeze

- **Entry:** quality/security/resource gates green and supervisor accepts
  candidate.
- **Tasks:** clean build, version/tag, record rule/config/decision identities,
  wheel/hash, historical compatibility, and freeze audit.
- **Exit:** immutable candidate and signed/recorded freeze report.
- **Do not:** change predictions after this phase without restarting freeze and
  holdout process.

### Phase 5 — Untouched holdout construction and review

- **Entry:** detector inaccessible/frozen to independent authors/custodian;
  data/ethics permissions resolved.
- **Tasks:** construct corpus under approved sampling design, blind review,
  adjudicate, check leakage, freeze bytes/labels/reviewer sources, hash.
- **Exit:** independently auditable untouched corpus with developer blindness
  intact.
- **Do not:** run the detector, reveal content to developers, or tailor samples
  to known rule internals.

### Phase 6 — Preregistration

- **Entry:** candidate and corpus are frozen but detector predictions remain
  unseen.
- **Tasks:** finalize N rationale, metrics/CIs, exclusions, comparisons,
  timing, exact command, artifact path, stop/recovery rules; supervisor audit.
- **Exit:** immutable preregistration and GO/NO-GO checklist PASS.
- **Do not:** run previews, individual scans, ablations, or latency on the
  holdout.

### Phase 7 — Primary evaluation

- **Entry:** all critical gates pass and supervisor explicitly authorizes.
- **Tasks:** execute exact command once, preserve/hash artifact, validate
  identity, compute preregistered primary outputs.
- **Exit:** immutable primary evidence and incident/anomaly record.
- **Do not:** rerun silently, tune, suppress, relabel, or change threshold.

### Phase 8 — Analysis

- **Entry:** primary artifact preserved.
- **Tasks:** secondary/diagnostic analyses, CIs, paired comparisons,
  preregistered ablations/timing, then separately marked exploratory failure
  analysis.
- **Exit:** traceable tables/figures and claim-evidence matrix.
- **Do not:** present exploratory modifications as confirmation.

### Phase 9 — Thesis writing

- **Entry:** verified evidence and literature synthesis available.
- **Tasks:** write methods before results where possible; integrate tables,
  limitations, threats, artifact references, and objective mapping.
- **Exit:** supervisor-reviewed thesis with reproducible references and no
  unsupported claim.
- **Do not:** omit poor results, collapse pilot/formal evidence, or call static
  alerts proof of malicious behavior.

### Phase 10 — Viva preparation

- **Entry:** stable thesis draft and artifact package.
- **Tasks:** reproduce safe smoke/quality tests, rehearse architecture,
  metrics, threat model, limitations, bad-result story, and controlled demo;
  prepare backup.
- **Exit:** student can defend every major design and claim without Codex.
- **Do not:** live-scan unknown servers, improvise new results, or memorize
  numbers without understanding denominators.

---

## 28. Scope-creep firewall

| Tempting addition | Default decision | Why / condition for inclusion |
|---|---|---|
| LLM classifier | **Do not add** | Introduces nondeterminism, privacy/cost/model-version issues, new data needs, and a different research question. Add only as an approved comparison/primary design with a new protocol. |
| Machine learning | **Do not add** | Requires training data, feature/model validation, and broader statistics beyond current scope. |
| Real-time proxy | **Do not add** | Adds deployment, concurrency, availability, and TOCTOU enforcement work; current study is static. |
| Agent execution sandbox | **Do not add** | Dynamic behavior/malware containment is a different high-risk system. |
| Remote malware analysis | **Do not add** | Not necessary for metadata constructs and raises serious safety/ethics issues. |
| Full MCP gateway | **Do not add** | Converts a focused inspector into an infrastructure product. |
| Cloud dashboard | **Do not add** | Authentication, tenancy, secrets, hosting, and privacy add little to the core RQ. |
| Large web UI | **Do not add** | Presentation effort does not answer detector effectiveness; a small read-only visualization may be optional. |
| Automatic remediation | **Do not add** | Suspicious findings are uncertain; automatic edits can damage schemas or hide evidence. |
| Recursive/general decoding | **Do not add** | Expands attack surface and resource exhaustion; violates the deliberate depth-one bounded design. |
| Network crawling | **Do not add** | Retrieval scope, consent, redirects, proxies, and hostile remote content become a separate study. |
| Multilingual support | **Defer by default** | Valuable but needs language expertise, constructs, reviewers, and enough data. Make English-only explicit unless approved. |
| Large threat-intelligence integration | **Do not add** | External feeds, freshness, licensing, false attribution, and connectivity undermine deterministic bounded scope. |
| Runtime policy enforcement | **Defer** | Could address TOCTOU/fingerprint binding but requires deployment integration and a separate security evaluation. |
| Signed baselines/releases | **Optional** | Useful provenance hardening if time remains after all P0 gates; not a substitute for construct/evaluation rigor. |

The scope test is: “Is this required to answer an approved RQ or close a P0
validity/security gate?” If not, place it in optional future work.

---

## 29. Supervisor decision register

These decisions materially change the thesis or experiment and must not be
made unilaterally by the student or an AI assistant.

| Decision | Options | Main trade-off | Recommended discussion point | Deadline |
|---|---|---|---|---|
| Research framing | Candidate A, B, or C | Precision of claim versus breadth/features | Start with A; use C only if drift becomes central; avoid broad poisoning claim | Phase 0 |
| Formal title | Intent-neutral suspicious-metadata title; narrow tool-poisoning title; integrity title | Communicability versus construct overclaim | Title must match observable outcomes | Phase 0/1 |
| Core construct | Partition proposed in Section 3; narrower subset | Coverage versus validity/label clarity | Separate core targets from supporting/warnings | Phase 1 |
| MCP/spec revision | Pin current reviewed revision; update before freeze | Current relevance versus semantic drift | Record exact revision and field assumptions | Phase 1 |
| Primary RQ | RQ1; RQ1 plus co-primary constraint; alternative drift RQ | Focus versus breadth | Prefer one effectiveness RQ | Phase 0/1 |
| Secondary RQs | v0.2 comparison, robustness, latency, drift | Additional evidence versus scope/multiplicity | Keep latency; add at most one substantial comparison | Phase 1 |
| Success/decision criterion | Estimation only; minimum recall with FPR guardrail; other | Honest estimation versus binary decision | Do not invent a target from pilot results; justify from use/risk | Before N |
| Finding-budget remediation scope | Pipeline-only fix; broader detector/risk refactor | Lower change risk versus opportunity to redesign | Fix semantics first; avoid simultaneous detector tuning | Phase 2 |
| Risk/severity policy | Preserve; development-only justified revision | Historical continuity versus calibration weakness | If changed, version/configure and justify before freeze | Phase 2/3 |
| Development-data sources | Synthetic, licensed public, private consented, mixed | Realism versus ethics/reproducibility | Prefer documented mixed-source if approvals allow | Before Phase 3 |
| Fresh-holdout design | Balanced, prevalence-oriented, dual panel | Construct precision versus realism/workload | Choose based on claim, not convenience | Before Phase 5 |
| Sample size | Precision-based; power-based paired design; feasibility-limited descriptive | Statistical precision versus workload | Consult on CI width and discordant pairs | Before Phase 5 |
| Reviewers | One; two; two + adjudicator; domain expert | Credibility versus availability | Two independent plus adjudication if feasible | Before Phase 5 |
| Label abstention/adjudication | Allow abstention; force binary; consensus | Honesty versus complete table | Allow abstention with frozen handling | Before review |
| Primary metrics | Recall; recall + FPR; another justified endpoint | Miss cost versus alert burden/multiplicity | Recall primary, FPR co-primary or guardrail | Before preregistration |
| Confidence/statistical method | Wilson/exact; paired exact; cluster/bootstrap | Simplicity versus dependence correctness | Match method to sampling unit and paired design | Before N/preregistration |
| Prevalence interpretation | Panel-only; representative sample; scenario reweighting | Internal coverage versus deployment relevance | Never present 50/50 precision as deployment precision | Methodology |
| Comparison baseline | Absolute only; v0.2; lexical; no-decoding; external literature tool | Interpretability versus implementation/time | v0.2 paired secondary if exact reproduction is sound | Phase 3 |
| Ablations | Seven families; reduced justified set; none | Contribution analysis versus multiplicity | Keep only if linked to design question | Preregistration |
| Real-world data | None; public licensed; private consented; mixed | External validity versus privacy/legal risk | Ask university before collection | Phase 0/1 |
| Ethics route | Approval, exemption, documented not required | Time/compliance versus data scope | Obtain written institutional guidance | Before collection |
| Privacy/artifact policy | Raw protected; redacted public; synthetic public | Reproducibility versus confidentiality | Separate protected raw evidence from publishable artifacts | Before collection |
| Dependency freeze | Constraints/lock; archived wheelhouse; container/environment manifest | Portability versus maintenance/storage | At least exact resolved constraints plus artifact hashes | Before freeze |
| Holdout custodian | Supervisor, independent student/researcher, controlled service | Blindness versus logistics | Developer should not hold readable corpus before run | Before Phase 5 |
| Final scope | Core detector only; + robustness; + drift; + UI | Thesis depth versus scope creep | Protect RQ1 and P0 gates first | Every phase review |
| Preservation/publication | Git documentation checkpoint; checksummed archive; supplementary package | Recoverability versus repository size/privacy | Preserve Day 6 and cited local evidence through reviewed channels | Before unattended gap and submission |

Every decision should record date, participants, choice, rationale, affected
sections/configuration, and whether a renewed freeze is required.

---

## 30. Student ownership plan

The student must be able to demonstrate mastery, not merely run generated
commands.

| Ownership task | Personal activity | Evidence of mastery |
|---|---|---|
| Trace scan pipeline | Follow one harmless tool from raw JSON through loader, normalizer, traversal, detector, suppression, decision, retention, risk, report | Draw and explain the pipeline without notes; identify file/function at each stage |
| Explain detector families | Read all 16 rule identities and representative tests; make benign/suspicious cards | For each family, explain signal, context, severity, hard negative, FP and FN |
| Calculate metrics | Manually recompute H0 and v0.3 confusion metrics | Produce correct arithmetic and explain denominator/meaning |
| Understand uncertainty | Calculate/interpret intervals with a checked tool and compare N scenarios | Explain why 3/3 is weak evidence and why N is not chosen arbitrarily |
| Inspect canonicalization | Canonicalize reordered/NFC examples and verify fingerprints | Predict which edits change tool/component/corpus/config hashes |
| Understand configuration hashing | Trace canonical configuration fields to hash | Explain why threshold, rules, suppressions, and future decision semantics affect identity |
| Reproduce safe tests | Run lint, mypy, selected tests, build, installed-wheel smoke without holdout | Keep a dated command/result log and explain each gate |
| Interpret H0 | Read raw artifact/research evidence without changing it | State TP/TN/FP/FN, metrics, CIs/limits, and correct negative-result conclusion |
| Explain v0.3 limitations | Compare chronology and identities | Say precisely why exposed post-unblinding improvement is exploratory |
| Diagnose a controlled failure | Break a disposable development fixture/config in a branch or lab copy, not frozen evidence | Identify layer, read traceback/artifact, restore via a reviewed fix/test |
| Explain finding-budget defect | Reproduce only on synthetic non-holdout fixtures after implementation | Show why old retention affected decisions and prove new budget invariance |
| Explain future protocol | Rehearse freeze, custodian, review, preregistration, one-run, preservation flow | Pass a mock GO/NO-GO audit and refuse an invalid early holdout scan |
| Defend threat model | Map assets/boundaries/goals/non-goals to code | Answer adaptive attacker, TOCTOU, baseline, suppression, and runtime questions |
| Own literature claims | Maintain annotated source matrix | For every major claim, identify source quality and limitation |
| Own thesis artifacts | Rebuild figures/tables from preserved artifacts | Provide a manifest linking claim, artifact, script, and hash |

### Weekly ownership practice

- explain one module and one test aloud;
- calculate or interpret one research quantity;
- record one limitation and how it constrains wording;
- make one small, reviewed development-only change manually when the formal
  implementation phase begins; and
- update the supervisor decision/action log.

AI assistance, if used, should be treated like an untrusted collaborator:
review diffs, understand tests, cite original sources, and never delegate
scientific responsibility.

---

## 31. “If Codex disappears tomorrow” plan

### What is already recoverable

The six Day 6 documents explain architecture, detectors, research chronology,
recovery, evidence identities, limitations, and adversarial findings. Git
history/tags preserve the tracked engineering checkpoint, while the recovery
manifest identifies local continuity risks. The package exposes standard
Python quality/build commands, and historical artifacts record substantial
provenance.

This remains insufficient while the Day 6 set and selected ignored evidence
are only local/untracked. The mission forbids committing them today; their
preservation is an explicit P0 follow-up requiring review.

### Prioritized self-sufficiency curriculum

1. **Git and recovery:** clone, inspect tags/commits, use clean branches,
   understand tracked/ignored/untracked state, verify hashes, and restore a
   clean environment without destructive guesses.
2. **Python project mechanics:** virtual environments, editable versus wheel
   installs, `pyproject.toml`, imports, pytest, Ruff, mypy, build, and traceback
   reading.
3. **MCP and JSON-RPC concepts:** host/client/server, discovery, tool schema,
   metadata trust, and static versus runtime boundaries.
4. **Pipeline reading:** loader → normalizer → detectors → decision/risk →
   reporting; draw data types and invariants.
5. **Security engineering:** hostile inputs, bounds, canonicalization, output
   injection, suppressions, baselines, TOCTOU, and threat modeling.
6. **Detector ownership:** learn each family/rule/test, then practice writing
   development-only benign counterexamples before any future detector change.
7. **Research method:** development/holdout separation, blinding, review,
   preregistration, contamination, confusion metrics, intervals, prevalence,
   and paired dependence.
8. **Artifact interpretation:** inspect schema/version/config/corpus identity,
   reproduce summaries, and distinguish historical from current semantics.
9. **Controlled implementation:** implement the finding-budget fix in small
   commits with tests and review; do not begin with new detectors.
10. **Viva communication:** rehearse claim/limitation pairs and demonstrate
    that a negative result remains a contribution.

### Minimum independent capability before unblinding

The student should be able to rebuild the frozen wheel, run every non-holdout
gate, explain a failed test, verify corpus/config hashes, audit clean Git state,
construct the exact primary command from the preregistration, and stop when a
GO/NO-GO item fails—without asking an AI system what the result “should” be.

---

## 32. Authoritative future backlog

### BEFORE SUPERVISOR MEETING

- Read all Day 6 documents and prepare a one-page project chronology.
- Bring Candidates A–C, construct taxonomy, RQs, objectives, and open decisions.
- Prepare the Day 6E P0 risk list and finding-budget example.
- List available reviewer/data/ethics resources without collecting data.
- Independently back up the six Day 6 documents and their hashes.
- Inventory H1, ablations, Day 3D/4A/4C, and other local evidence that may be
  cited; do not publish private/unsafe material.
- Ask how/when the Day 6 set and selected evidence should enter a reviewed Git
  checkpoint or checksummed supplementary archive.

### AFTER METHODOLOGY APPROVAL

- Pin the literature search and target MCP specification revision.
- Finalize construct guide, threat model, RQs, objectives, success/estimand
  language, and ethics route.
- Decide whether drift, robustness, or v0.2 comparison is in scope.
- Design the exact decision-state schema and resource invariants.
- Approve dependency, baseline, suppression, privacy, and preservation policy.
- Implement only approved engineering remediation on development data with
  regression/property tests.

### BEFORE DETECTOR FREEZE

- Resolve finding-budget decision coupling and intermediate match bounds.
- Complete all P0 tests, historical compatibility, and documentation.
- Expand and inspect only development data/hard negatives/robustness cases.
- Select threshold, rule pack, risk policy, and configuration using
  development-only evidence.
- Complete sample-size/statistical consultation and future data/review design.
- Pass lint, format, mypy, full coverage suite, build, and wheel smoke.
- Produce exact dependency/environment record.
- Create clean version/tag/wheel/config identities and freeze report.

### AFTER DETECTOR FREEZE

- Transfer holdout work to approved independent authors/custodian.
- Construct no samples personally unless the approved design assigns a
  blinded role compatible with independence.
- Conduct blinded reviews and adjudication; preserve originals.
- Run detector-free overlap and independent near-duplicate audit.
- Freeze corpus/labels/reviewer sources and hashes.
- Do not scan, preview, time, ablate, or browse the holdout.

### BEFORE PRIMARY EVALUATION

- Complete immutable preregistration.
- Verify every Section 23 critical gate.
- Dry-run artifact paths and commands only on designated smoke/development
  fixtures.
- Record supervisor authorization.
- Confirm clean Git/environment and no-overwrite artifact behavior.
- Have custodian provide the frozen manifest through the approved procedure.

### AFTER PRIMARY EVALUATION

- Preserve and hash raw artifact immediately.
- Compute preregistered primary metrics/CIs, then secondary analyses.
- Report unfavorable and inconclusive results unchanged.
- Separate failure analysis and every detector modification as
  post-unblinding exploratory work.
- Build thesis claim-evidence map, tables, figures, and supplementary manifest.
- Archive reproducibility materials according to ethics/privacy policy.

### OPTIONAL FUTURE WORK

- separately confirmed multilingual constructs;
- runtime fingerprint enforcement/TOCTOU integration;
- signed baseline/release provenance;
- broader multi-ecosystem external validation;
- approved comparison with a literature-supported external detector;
- small privacy-safe results visualization;
- new independent replication; or
- dynamic analysis as an entirely separate project.

---

## 33. P0 coverage from the final adversarial review

Every P0/P0-planning item in `docs/final-adversarial-review.md` is addressed,
assigned to supervisor decision, or explicitly deferred. “Addressed” means the
blueprint contains a required future control; it does not mean the future work
has already been completed.

| Day 6E item | Blueprint disposition | Location / gate |
|---|---|---|
| R01 — exposed holdout reused as fresh evidence | **ADDRESSED IN BLUEPRINT** | Sections 1C, 11, 23–25, 27: v0.3 stays exploratory; genuinely untouched one-run corpus required |
| R02 — poisoning label conflates intent and warnings | **REQUIRES SUPERVISOR DECISION** | Sections 2–3, 29: partitioned observable construct must be approved |
| R03 — finding retention changes decisions | **ADDRESSED IN BLUEPRINT design; implementation still P0** | Sections 7, 8, 21, 23 |
| R04 — low H0 recall | **ADDRESSED AS HISTORICAL RESULT/P0 planning** | Sections 1A, 5, 14, 25: recall primary; bad result remains publishable |
| R05 — H0 25% FPR/review burden | **REQUIRES SUPERVISOR METRIC/GUARDRAIL DECISION** | Sections 5, 13–14, 29 |
| R07 — synthetic-heavy corpus | **ADDRESSED IN DATA PLAN** | Sections 10–11 and ethics controls in 18 |
| R08 — balanced prevalence distorts precision | **REQUIRES SAMPLING DECISION** | Sections 11, 13–15, 29: balanced/prevalence/dual options |
| R09 — N=48/wide intervals | **ADDRESSED IN PROSPECTIVE PLANNING** | Section 13; no invented N |
| R10 — matched-pair dependence | **REQUIRES STATISTICAL DECISION** | Sections 11, 13, 15, 29 |
| R11 — author/taxonomy rule-shaped data | **ADDRESSED IN DATA CUSTODY PLAN** | Sections 10–12, 23, 27 |
| R12 — one reviewer | **REQUIRES FEASIBILITY/REVIEWER DECISION** | Section 12 recommends two independent plus adjudication |
| R14 — exact checks miss near duplicates | **ADDRESSED IN LEAKAGE PLAN** | Sections 10–11, 23 require independent near-duplicate review |
| R15 — uncalibrated severity/risk/bands | **REQUIRES SUPERVISOR DECISION** | Sections 7, 9, 14, 29: justify/preserve or revise only on development data before freeze |
| R23 — Day 6 files untracked | **EXPLICITLY DEFERRED BY DAY 6F NO-COMMIT RULE; immediate preservation required** | Sections 31–32: independent backup now, reviewed documentation checkpoint later |
| R24 — cited local supporting evidence ignored | **REQUIRES SUPERVISOR/PUBLICATION DECISION** | Sections 29, 32: inventory and checksummed supplementary archive if cited |
| R31 — suppressions can hide findings/post-hoc use | **ADDRESSED IN PROTOCOL** | Sections 4, 8, 22–23: primary uses none or preregistered exact identity; governance P1 product work |
| R34 — “security scanner” implies assurance | **ADDRESSED IN FRAMING/COMMUNICATION** | Sections 2–4 and objectives use “bounded static inspector”; absence of findings never certifies safety |
| R35 — real-data ethics/privacy/legal risk | **REQUIRES INSTITUTIONAL DECISION BEFORE COLLECTION** | Sections 18, 23, 29 |

### Seven grouped P0 priorities

| Day 6E grouped priority | Coverage |
|---|---|
| Preserve Day 6 set | Sections 29, 31, 32; deferred from Git only because this mission prohibits commit |
| Preserve selected local evidence | Sections 29 and 32; supervisor decides what will be cited/archived |
| Refine construct | Sections 2–4, Phase 1 gate |
| Resolve finding-budget coupling | Sections 7, 8, 21, Phase 2 gate |
| Approve statistical method | Sections 13–15, 22–23, supervisor register |
| Approve data/review plan | Sections 10–13, 18, 23, supervisor register |
| Freeze cleanly | Sections 9, 21–24, Phases 4–7 |

No P0 is silently treated as complete. In particular, a written design is not
evidence that the budget defect, preservation, independent data, review, or
formal approval has occurred.

---

## 34. Blueprint authorization boundary

This document authorizes no implementation, collection, tuning, unblinding,
evaluation, release, or publication action. The next safe action is supervisor
review of the framing, construct, RQs, P0 gates, and decision register, plus a
separate preservation decision for the currently untracked Day 6 package.

**THIS BLUEPRINT IS SUBJECT TO FORMAL SUPERVISOR APPROVAL.**

**NO FRESH HOLDOUT WAS CREATED.**

**NO CONFIRMATORY EXPERIMENT WAS RUN.**

**THE EXPOSED HOLDOUT WAS NOT RERUN.**

**NO DETECTOR TUNING WAS PERFORMED.**

**NO DETECTOR, CORPUS, LABEL, THRESHOLD, RISK MODEL, OR FROZEN RESEARCH
EVIDENCE WAS MODIFIED DURING DAY 6F.**
