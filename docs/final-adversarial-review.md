# Day 6E Final Adversarial Examination

> **Mode:** read-only hostile review / FYP red team
> **Repository checkpoint:** `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`
> **Package / rule pack:** `0.3.0a1` / `builtin 2.0.0`
> **Scientific status:** pre-FYP research prototype and pilot study
> **Review date:** 2026-08-28

This review asks the hardest defensible questions about the project. It does not
replace the technical map, Captain's Manual, handover, disaster-recovery guide,
or immutable research evidence. It treats the repository as authoritative and
separates an engineering defect from a detector-design limitation and from a
research question.

The principal conclusion is deliberately mixed:

- the repository is a substantial, carefully bounded engineering prototype and
  an unusually honest pilot-research record;
- the first prediction-unexposed pilot result found poor effectiveness at the
  frozen threshold;
- the v0.3 result is useful post-unblinding diagnosis, not confirmation;
- the target construct still mixes poisoning-like intent with broader
  security-review conditions;
- no final FYP effectiveness conclusion is currently supportable; and
- a finding-budget decision-coupling issue must be resolved before the next
  detector freeze.

No command in Day 6E invoked a tool, executed metadata, ran a detector against
the exposed holdout, or produced new predictions.

## 1. Repository and evidence basis

| Item | Verified state |
|---|---|
| Git root | `C:\Users\afiq hakiki\Documents\csprojects\mcp-tool-security-inspector` |
| HEAD | `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` |
| Existing worktree state at start | Only the five expected untracked Day 6 documents |
| H0 artifact | `evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json` |
| H0 file SHA-256 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` |
| Day 3C SHA-256 | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` |
| Day 4C primary SHA-256 | `d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b` |
| Holdout | v1.0.1, 48 samples, 24 benign/24 suspicious, now exposed |
| Holdout semantic SHA-256 | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| H0 configuration SHA-256 | `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1` |

The review used preserved artifacts and source inspection only. Parsing an
existing JSON artifact is not a detector evaluation. The H0 artifact contains
16 retained findings in total, at most two per sample, and no truncated sample.
The tracked v0.3 exploratory artifact contains 24 retained findings, at most two
per sample, and no truncated sample. Therefore the newly identified
finding-budget concern did not alter either preserved result.

## 2. Five review-panel perspectives

| Perspective | Strongest aspect | Weakest aspect | Likely challenge | Evidence that supports or weakens the answer |
|---|---|---|---|---|
| **A. FYP examiner** | The student can show a complete problem-to-prototype-to-negative-result-to-exploration chronology. | The formal FYP question, construct, primary estimand, and success criterion are not yet finalized. | “What exact claim will your final thesis test that this pilot has not already answered?” | `docs/fyp-handover.md` explicitly calls the work pre-FYP and requires supervisor-approved scope and a new holdout. |
| **B. Security researcher** | The inert boundary, bounded parsing, no-tool-call invariant, safe decoding, and loopback restrictions are concrete. | Fixed English lexical/context rules are adaptively bypassable, while several labels describe review-worthiness rather than adversarial intent. | “Are you detecting attacks, unsafe metadata, or merely vocabulary?” | Detector source shows fixed regex/context grammars; H0 shows 17/19 false negatives had no finding; R08 shows construct ambiguity. |
| **C. Research-methodology reviewer** | H0 was frozen, independently reviewed, run once, preserved exactly, and not replaced by the better v0.3 number. | N=48, matched dependence, one reviewer, synthetic authorship, multiple outcomes, and a vague null limit inference. | “What was the preregistered primary estimand and what result would count as practically useful?” | The plan preregisters several primary outputs but no minimum acceptable recall/FPR or formal decision rule. |
| **D. Open-source maintainer** | Typed modules, stable rule IDs, strict mypy, broad tests, package build, and explicit security invariants make maintenance tractable. | The alpha still has a decision-affecting finding-budget coupling, no exact dependency lock, and untracked continuity documents. | “Can a large hostile catalog change exit status or risk merely by ordering findings?” | `scanner.py:77-80` and `cli.py:155-161` show decisions use retained findings; limit tests do not assert decision preservation. |
| **E. Reproducibility reviewer** | Corpus/config hashes, Git state, runtime metadata, artifact schemas, exact evidence hashes, and historical warnings are unusually strong for a student prototype. | Hashes are not signatures; CRLF alters several identities; ignored analyses and Day 6 documents are not preserved by Git; v0.3 came from a dirty tree. | “Can another person reconstruct the exact v0.3 source and all secondary evidence from the tag alone?” | Day 6D demonstrated an LF-safe clean rebuild but documented missing locks, local-only files, and dirty v0.3 provenance. |

## 3. Problem-definition and terminology challenge

### What the project actually detects

The implementation detects **predefined suspicious or security-relevant
constructs in MCP tool-definition metadata**. It does not observe publisher
intent, server code, tool calls, runtime side effects, host prompt construction,
or user harm. A rule match therefore establishes only that a static construct
satisfied that rule's conditions.

“Tool poisoning” is defensible for metadata deliberately used to manipulate
agent selection, override instructions, conceal material behavior, or
misrepresent capability. It is less precise when applied to:

- a malformed JSON Schema;
- an openly disclosed administrative capability;
- credential vocabulary in legitimate security software;
- invisible formatting used for a valid language; or
- an accidental mismatch caused by poor documentation.

Those can be security-review findings without being poisoning.

### Relationship to prompt injection

Tool-description poisoning can be understood as a tool-bound form of indirect
prompt injection when untrusted tool metadata enters model context. The
distinguishing feature is the provenance and lifecycle boundary—discovered tool
metadata—rather than a completely different linguistic mechanism. Capability
mismatch, malformed schema, and drift are related metadata-integrity concerns,
not necessarily prompt injection.

### Recommended precise vocabulary

Use the following hierarchy:

1. **MCP tool-definition metadata:** the unit of static analysis.
2. **Suspicious metadata construct:** the broad, intent-neutral label for a rule
   condition that warrants review.
3. **Agent-influence construct:** instruction override or concealment language
   that could influence model/host behavior.
4. **Capability/declaration inconsistency:** a cross-field purpose-versus-schema
   concern.
5. **Schema-security or compatibility finding:** malformed or unexpectedly
   privileged schema content.
6. **Metadata poisoning attempt:** reserve this for cases where evidence and
   study design support deliberate manipulative use; the current detector alone
   cannot assign that intent.

The most academically precise one-sentence description is:

> MCP Tool Security Inspector is a deterministic, bounded, offline-first static
> metadata inspector that flags predefined suspicious MCP tool-definition
> constructs and canonical metadata drift for human review without invoking
> tools.

### Is the scope too broad or too narrow?

It is **too broad as one validity construct** because poisoning, schema quality,
capability review, concealment, and sensitive-data handling do not all imply the
same threat or ground-truth criterion. It is **narrow as an operational security
control** because it is English-oriented, static, rule-based, host-agnostic, and
does not evaluate runtime behavior, authentication, permissions, or multi-turn
effects. The engineering scope is coherent; the scientific construct needs
partitioning.

## 4. Reconstructed threat model

### Trusted components

- the reviewed `mcpsec` source, Python runtime, dependencies, and operating
  environment;
- the operator selecting the correct input, policy, baseline, and output path;
- the integrity of the machine and local filesystem;
- trusted copies of expected hashes, Git refs, and research protocols;
- the human reviewer who interprets findings rather than treating them as
  automatic proof; and
- host-side controls—authentication, least privilege, confirmation, sandboxing,
  and audit logging—which remain outside this package.

These are assumptions, not guarantees. A compromised dependency, altered
baseline, malicious suppression file, or untrusted expected hash can defeat the
meaning of otherwise correct analysis.

### Untrusted inputs and surfaces

- tool names, titles, descriptions, schemas, annotations, execution hints,
  icons, `_meta`/metadata, source data, and unknown fields;
- catalog JSON and JSON-RPC envelopes;
- opt-in loopback MCP server responses and pagination cursors;
- custom rule packs, suppression files, and baseline files;
- filenames and source paths shown in reports;
- historical experiment artifacts presented for comparison; and
- all generated terminal, JSON, CSV, and SARIF content when consumed downstream.

### Attacker capabilities

An attacker may choose metadata text, Unicode, nesting, field placement,
representations, tool order, number of fields/tools, capability wording,
schemas, and benign-looking context within enforced limits. If the attacker
controls a loopback service, it can send malformed, slow, paginated, or large
responses within transport constraints. If it controls local policy files or
the baseline store, it may suppress findings or redefine expected state.

### Assumptions under attack

| Assumption | Challenge |
|---|---|
| The analyzed catalog is the catalog later used by the host. | No binding prevents time-of-check/time-of-use replacement after scanning. |
| A trusted operator selects trustworthy suppressions and baselines. | The files are validated structurally, not authenticated or approved cryptographically. |
| Fixed English context windows approximate the target relations. | Adaptive paraphrase, translation, field splitting, homoglyphs, or unsupported encodings can evade them. |
| Input bounds adequately bound computation. | Findings are fully materialized before output retention; a high-match document may still consume substantial memory/CPU. |
| Loopback narrows network risk sufficiently. | A hostile local process remains untrusted, and `fetch` performs network/session initialization even though analysis is static. |
| Downstream report viewers treat strings as data. | JSON/SARIF consumers or spreadsheet transformations may introduce their own injection/rendering risk. |
| Trusted hashes are independently available. | A digest stored beside a modified artifact can be replaced with it; a hash is not an origin signature. |
| A rule finding maps cleanly to the corpus label. | R08 and credential/schema false positives show label/rule construct mismatch. |

### Security goals

- never invoke a scanned tool or execute metadata;
- reject ambiguous or oversized hostile inputs;
- preserve security-significant fields rather than silently discard them;
- emit deterministic, explainable, bounded findings;
- make metadata change detectable through canonical fingerprints;
- protect terminal and spreadsheet sinks from obvious injection;
- keep retrieval explicit, loopback-only, bounded, no-proxy, and no-redirect; and
- preserve experiment and historical identities sufficiently for audit.

### Non-goals and out-of-scope attacks

- proving a server or publisher malicious;
- runtime implementation verification, sandboxing, malware analysis, or exploit
  execution;
- authentication/OAuth correctness, authorization, least privilege, or host
  confirmation UX;
- arbitrary remote MCP discovery, stdio server spawning, icon/schema URL
  fetching, or general SSRF scanning;
- complete prompt-injection or multilingual semantic detection;
- model behavior, multi-turn attacks, tool-result poisoning, or host prompt
  composition;
- signed publisher provenance or tamper-proof baseline storage; and
- deployment prevalence or production accuracy estimation.

### Missing statements that should enter a future threat model

1. Define the time-of-check/time-of-use boundary between inspection and host use.
2. State who may create/approve suppressions and baselines and how rollback is
   prevented.
3. Distinguish an attacker controlling metadata from one controlling the local
   machine, Python environment, or report viewer.
4. Define whether denial of service during detection is a security goal, not
   merely input rejection.
5. State how multi-server catalogs, duplicate semantic tools, and catalog order
   are handled.
6. Define downstream report retention, access control, and sensitive-metadata
   handling.
7. State the assumed MCP specification revision and host interpretation.
8. State that open rules enable adaptive evasion and that secrecy is not a
   defense.
9. Define the operational response to a finding and the cost of false negatives
   versus false positives.
10. Separate poisoning, unsafe declaration, and schema-quality constructs.

## 5. Detector-design challenge

### Design-level limitations

- **Rule dependence:** fixed patterns are deterministic and explainable but
  brittle against paraphrase, translation, punctuation, homoglyphs, long-range
  relations, and new MCP fields.
- **Context approximation:** sentence-bounded windows and scoped negation reduce
  simple false positives but do not provide semantic understanding.
- **Cross-field coverage:** mismatch rules use a finite capability/purpose
  vocabulary. A truthful broad tool may look mismatched; an attacker can use an
  unseen description.
- **Representation coverage:** `OBF-005` intentionally decodes only four
  depth-one formats under strict budgets. Nested, compressed, encrypted,
  fragmented, or novel encodings remain invisible.
- **Schema scope:** JSON Schema validity is a compatibility/security-quality
  check, not maliciousness detection. Valid schemas may expose dangerous
  behavior; invalid schemas may be accidental.
- **Sensitive-data scope:** credential words and actions are common in benign
  password, authentication, recovery, and security tools.
- **Unicode scope:** NFC removes canonical spelling variance but does not solve
  compatibility characters, confusables, homoglyphs, or all bidirectional
  deception.

### Severity, weight, and threshold challenge

The repository hard-codes finding severities, confidence values, score
contributions, category caps, two synergies, risk bands, and a `MEDIUM`
classification threshold. They are versioned and deterministic, but the
repository does not establish that they are empirically calibrated to harm,
review cost, or deployment prevalence.

The risk formula has a probability-like complement product:

`100 * (1 - product(1 - category_score/100))`

but its inputs are heuristic contributions, not calibrated probabilities.
Calling the result “probability of maliciousness” would be wrong. A category is
capped at 35, so many serious findings in one category cannot alone produce a
MEDIUM aggregate-risk band. At the same time, one MEDIUM finding creates a
suspicious evaluation label even if aggregate risk remains INFO or LOW. This is
two distinct decision systems, not a contradiction only if documentation and
users keep them separate.

The `MEDIUM` threshold is defensible as a frozen pilot choice; it is not yet
defensible as an optimal operating point. Lowering it after H0 would be
post-hoc—and would not recover the 17 false negatives with no finding.

### Implementation defect: output budget changes security decisions

This is the most important new Day 6E finding.

1. `scanner.analyze_tools()` detects and suppresses findings.
2. `scanner._retain_findings()` then applies per-tool, evidence, and global
   report capacity.
3. `scanner.py:80` calculates aggregate risk from **retained** findings.
4. `cli.py:155-161` calculates `--fail-on` from **retained** findings.
5. `evaluation/evaluator.py:180` predicts suspicious from **retained** findings.
6. The terminal counts a tool as affected using `bool(result.findings)`.

Consequences:

- once earlier tools consume the 2,048-report capacity, a later tool may have
  `findings_detected > 0` but zero retained findings, risk 0, no fail-on exit,
  and a benign evaluation prediction;
- attacker-controlled catalog order can influence risk and exit semantics;
- the terminal's “Clean” count can include tools whose findings were detected
  but fully truncated; and
- the output budget is no longer just an output-safety control—it becomes part
  of classification.

This is an **implementation defect**, not merely a research limitation. The
limits and truncation flags are valuable, and deterministic severity-first
retention is sensible for display, but display retention should not silently
erase the security decision. No change is made in Day 6E. The preserved H0 and
v0.3 artifacts were unaffected because neither contains a truncated sample.

### Credible resource-exhaustion gap requiring testing

The 64/2,048 limits are applied after detector outputs are materialized and
sorted. A hostile document near the 100,000-node bound could create many
matching fields and therefore many `Finding` objects before retention. The
source proves post-detection retention; this audit did not benchmark worst-case
memory or CPU. Classify this as a **credible implementation/security question**
until adversarial tests establish a bound or an incremental strategy is
designed.

### Classification

| Issue | Classification | Reason |
|---|---|---|
| Fixed English regex/context rules miss paraphrases | Design limitation | Expected tradeoff of deterministic lexical analysis |
| Schema validity included under poisoning umbrella | Research construct question | Implementation does what it declares; label meaning needs refinement |
| Uncalibrated weights/severities/threshold | Research question / design limitation | Frozen identities exist, but empirical/operational justification is absent |
| Retained budget controls risk, fail-on, and labels | Implementation defect | Output capacity should not silently change detection decisions |
| Findings materialized before retention | Implementation/security question | Current limits may not bound intermediate work sufficiently |
| `--redact` leaves original tool metadata/source | Documented design limitation | README states evidence-only redaction; name can still mislead users |
| Open-source patterns permit evasion | Design limitation | Transparency is necessary for audit; security must not rely on secrecy |

## 6. Development-corpus challenge

The 80 samples—40 benign and 40 suspicious—are sufficient for deterministic
regression coverage of authored constructs. They are not sufficient to estimate
external detector performance.

Major challenges:

- all samples are synthetic and visible during design;
- the taxonomy and detector authorship create circularity risk;
- 50/50 balance makes class coverage convenient but does not resemble expected
  deployment prevalence;
- obvious suspicious language may reward the same lexicons used to author it;
- benign hard negatives exist, which is a strength, but cannot reproduce the
  diversity of real vendor documentation;
- there is one review lineage rather than independent external authorship; and
- TP 37/TN 36/FP 4/FN 3 (91.25% accuracy) is in-sample regression behavior, not
  a generalization estimate.

Likely impact: development metrics overestimated transfer. H0 recall falling
from 92.50% development to 20.83% on separately authored pilot data is direct
evidence of that gap. The correct use of the corpus is mechanism regression,
boundary testing, and preventing accidental behavior changes.

## 7. Holdout and human-review challenge

### What the holdout can support

The 48-sample, prediction-unexposed, separately authored, independently reviewed
pilot holdout can support:

- a reproducible measurement of the frozen v0.2 detector on those 48 samples;
- discovery of a development-to-holdout transfer gap;
- corpus-bounded failure taxonomy and hypothesis generation;
- descriptive Wilson intervals under their assumptions; and
- evidence that one blinded reviewer mostly applied the frozen binary rubric
  similarly to the original labels.

It cannot support:

- real-world MCP prevalence or production accuracy;
- multilingual, cross-vendor, cross-host, or adaptive-adversary generalization;
- independent confirmation of v0.3;
- precise category ranking from strata of roughly 3–6;
- causal family importance;
- objective malicious intent; or
- multi-expert label consensus.

### Construction threats

- **N=48:** estimates remain wide; each label class has only 24 cases.
- **24/24 balance:** useful experimentally, unrepresentative operationally;
  precision and alert workload will change with prevalence.
- **Synthetic and English-only:** vendor noise, terminology, extension fields,
  localization, and genuine mistakes are absent.
- **Repository authorship:** the construction operator knew the taxonomy and
  project, even though predictions were not seen.
- **Matched pairs:** eight pairs improve controlled contrast but reduce
  independence; ordinary binomial intervals do not model this clustering.
- **Confounding:** all eight `derived` samples are suspicious; benign root
  descriptions averaged 105.3 characters versus 56.3 for suspicious ones.
- **Small, overlapping strata:** category and field percentages are descriptive,
  not stable rankings.
- **Difficulty:** original 16/16/16 balance was not independently reproduced.

### Human review

Observed facts:

- 48/48 reviewed while blinded to expected labels and detector predictions;
- 47 binary agreements, one disagreement, no abstentions;
- reviewer classifications 25 benign/23 suspicious;
- raw agreement 97.9167%;
- Cohen's kappa approximately 0.9583;
- difficulty agreement 16/48 (33.3333%);
- one independent reviewer only; and
- R08/`holdout_s011` original suspicious, reviewer benign, original retained
  under the frozen malformed-schema security-review rubric.

Kappa near 0.9583 establishes **very high agreement beyond chance under this
two-rater/marginal-label calculation**. It does not establish 95.83% label
accuracy, reviewer expertise, construct truth, malicious intent, external
validity, or consensus. The original label source is not itself an independent
reviewer in the same sense as an external panel. R08 demonstrates a meaningful
boundary problem: malformed schema can warrant security review without proving
poisoning. The low difficulty agreement shows that subgroup labels are much
less stable than the binary rubric.

Adjudication retaining the original R08 label is procedurally defensible because
the rule existed before predictions. It is also a source of possible
adjudication bias because the project owner interpreted its own construct. The
correct response is preservation and qualification—not declaring either party
wrong.

## 8. H0 challenge

### Authoritative result

| TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |

Wilson 95% intervals:

- accuracy: 34.47%–61.67%;
- recall: 9.24%–40.47%; and
- FPR: 12.00%–44.90%.

### Hostile interpretation

On a balanced set, a classifier predicting every sample benign would obtain 50%
accuracy, 0% recall, and 0% FPR. H0 accuracy was 47.92%, so accuracy alone does
not show useful discrimination. It would still be wrong to call this “worse
than random” without defining a random baseline and inferential test. Because
the corpus is exactly balanced, accuracy equals the mean of recall and
specificity here; it remains prevalence-sensitive outside this design.

F1 is useful for summarizing precision/recall tradeoff but hides true negatives
and is prevalence-sensitive. FPR is essential for review workload but not
enough: recall/FNR, specificity, raw counts, uncertainty, operational costs, and
deployment prevalence scenarios are also needed.

The most serious performance fact is 19/24 suspicious samples missed, with
17/19 false negatives producing no finding. This means threshold adjustment
cannot solve the main gap. A 25% FPR among benign pilot samples also implies
substantial review burden.

### Methodological weaknesses in H0 framing

- The null phrase “does not provide useful discrimination beyond the agreed
  descriptive baseline” is not tied to a numeric baseline, hypothesis test, or
  decision rule.
- Several outcomes are called primary; no single primary estimand or minimum
  practically important recall/FPR was chosen.
- No prospective precision/power rationale for N=48 is documented.
- Wilson intervals assume independent binomial trials, while eight matched pairs
  introduce dependence.
- Precision and F1 intervals were intentionally omitted, which is honest but
  limits uncertainty claims.
- Multiple strata and ablations are secondary, but readers can still cherry-pick
  favorable small cells.

### Is the result useful?

Yes, as an honest, reproducible negative pilot. It falsifies an optimistic
reading of development performance, reveals lexical transfer and false-positive
problems, and demonstrates a research workflow that did not discard an
unfavorable result. It does not establish an effective production detector. Its
publication value depends on framing, venue, literature context, and whether
the engineering/method contribution is sufficiently novel; it is certainly
valuable for an undergraduate pilot and thesis-method foundation.

Defensible conclusion:

> The frozen v0.2 prototype showed low sensitivity and substantial benign alert
> burden on one small controlled pilot holdout. The result is scientifically
> useful as a reproducible negative finding and failure-discovery checkpoint,
> not evidence of operational effectiveness.

## 9. v0.3 post-unblinding challenge

| TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 18 | 6 | 13 | 60.42% | 64.71% | 45.83% | 53.66% | 25.00% |

Relative to H0 on the same exposed 48 samples, six known false negatives became
true positives and no original false positive was removed. Four recoveries came
from `MIS-002`, one from `PI-002`, and one from `HID-002`. `SEC-002` recovered no
holdout true positive and amplified findings on known benign cases; `OBF-005`
recovered no exposed encoded case. Thirteen suspicious samples still had no
finding.

This does **not** prove improved generalization because:

- Day 3 failures informed Day 4 hypotheses;
- the same exposed sample population was reused;
- the five rules and 36 mechanism fixtures were authored post-unblinding;
- the observed gains are concentrated in three new rules;
- no fresh independently authored/reviewed test exists; and
- the artifact records `dirty=true`, commit/application/rule-pack metadata from
  the earlier state, while its configuration contains the 16-rule candidate.

The dirty artifact is authentic and valuable, but a clean commit alone cannot
reconstruct the exact uncommitted source. Recorded rule IDs and configuration
hash reduce ambiguity; they do not fully replace a source snapshot.

Safe learning:

> The v0.3 implementations operationalize five post-H0 hypotheses. On authored
> mechanism fixtures they exercise the intended gates, and on the already
> exposed holdout three new rules recovered six known cases while all six known
> false positives remained. This is diagnostic evidence of mechanism behavior
> and unresolved failure modes, not an independent estimate of transfer.

## 10. Ablation challenge

The seven preregistered family ablations are legitimate paired **within-corpus
descriptions**. H0 ablation matrices were:

| Removed family | TP | TN | FP | FN | Recall | FPR | Careful reading |
|---|---:|---:|---:|---:|---:|---:|---|
| Injection | 5 | 18 | 6 | 19 | 20.83% | 25.00% | No binary change on this corpus/threshold |
| Concealment | 5 | 18 | 6 | 19 | 20.83% | 25.00% | No binary change |
| Sensitive data | 5 | 22 | 2 | 19 | 20.83% | 8.33% | Four H0 false positives depended on this family |
| Schema | 3 | 20 | 4 | 21 | 12.50% | 16.67% | Removed two TPs and two FPs |
| Mismatch | 4 | 18 | 6 | 20 | 16.67% | 25.00% | Removed one TP |
| Obfuscation | 5 | 18 | 6 | 19 | 20.83% | 25.00% | No binary change |
| Capability | 5 | 18 | 6 | 19 | 20.83% | 25.00% | INFO findings were below MEDIUM |

Limitations:

- N=48 makes one- or two-sample changes unstable.
- Families are not statistically or semantically independent.
- Capability extraction supports mismatch logic; obfuscation reuses injection,
  concealment, and capability signals; risk has cross-family synergies.
- Removing output does not isolate causal importance in real deployments.
- No correction or inferential plan exists for seven family comparisons.
- Each ablation used one timing repetition, so apparent compute differences are
  noise-prone and should not be ranked.
- “No binary change” does not mean a family is useless; it may alter findings,
  explanations, risk, or other corpora below the chosen threshold.

Safe wording:

> With all other recorded settings held constant on this pilot corpus, removing
> family X changed these specific predictions/findings. This describes
> corpus- and threshold-dependent contribution; it does not estimate causal
> real-world protection.

## 11. Latency-claim challenge

Preserved H0 `analysis-core`:

- 3 warm-ups per sample, 10 measured repetitions;
- 480 observations;
- mean 1.7159 ms/tool;
- nearest-rank p95 3.2229 ms; and
- mean 82.3637 ms per 48-sample corpus pass.

Existing H1 `static-end-to-end`:

- 1 warm-up per sample, 5 measured repetitions;
- 240 observations;
- mean 4.3020 ms/tool;
- nearest-rank p95 6.3104 ms; and
- mean 206.4941 ms per 48-sample corpus pass.

“Static-end-to-end” includes local bounded file loading, normalization, sample
selection, analysis, suppressions, risk, and result construction. It excludes
corpus hashing, Git/environment collection, aggregate metrics, serialization,
terminal/SARIF rendering, networking, process startup, and tool invocation.
Calling it complete CLI or deployment latency would be misleading.

The results come from one runtime/machine/background-load condition, without
CPU pinning, process isolation, multiple machines, concurrency, memory
measurement, maximum-size inputs, or real server/host integration. Repeated
observations of the same 48 samples are correlated; p95 is a measurement
distribution, not a population guarantee for arbitrary tools. Python/runtime,
caches, filesystem, power mode, and antivirus can materially affect these small
times.

Safe wording:

> In the recorded local environment, the frozen static analysis completed the
> small pilot fixtures in low single-digit milliseconds per tool at the declared
> boundaries. These measurements demonstrate lightweight local execution in
> that setup, not deployment suitability or hardware-independent latency.

## 12. Reproducibility challenge

### What is strong

- H0 records a clean Git commit, corpus/configuration hashes, package/rule-pack
  identities, runtime/dependency metadata, timing boundary, invocation,
  timestamp, sample records, and exact results.
- The H0, Day 3C, Day 4C, and reviewer-source files have independently recorded
  SHA-256 identities.
- Artifact loading checks internal consistency rather than merely parsing JSON.
- Current comparison distinguishes hard incompatibility from warnings and
  withholds timing deltas across different boundary/environment records.
- Day 6D rebuilt a Git-only checkpoint on Windows/Python 3.12.13 and passed 472
  tests, 92.95% coverage, Ruff, format, strict mypy, build, wheel smoke, version,
  help, and inert demo checks.

### Ranked reproducibility risks

| Rank | Risk | Severity | Why it matters |
|---:|---|---|---|
| 1 | Day 6 documents and significant secondary analyses are untracked/ignored | **P0 preservation** | A clone/tag does not contain the knowledge base, H1/ablations, or most Day 4 supporting evidence. This Day 6E document is also outside the existing recovery manifest until preserved separately. |
| 2 | Windows CRLF conversion changes reviewer and corpus hashes | **P1 high** | An ordinary `core.autocrlf=true` checkout can look normal yet fail identities. Only three primary artifacts are `-text`. |
| 3 | No exact dependency lock/constraints file | **P1 high** | Future resolution can select different minor/patch runtime packages and major dev tools; exact reconstruction from Git alone is impossible. |
| 4 | v0.3 exploratory artifact came from a dirty working tree | **P1 high** | The recorded commit is not the exact source. Configuration/rule identities help but do not reconstruct the diff. |
| 5 | Ignored run artifacts have no single checksummed archive | **P1 high if cited** | H1 and ablation files exist locally but can be lost silently; `git status` does not show ignored data. |
| 6 | GitHub Actions and build backend are moving references/ranges | **P2 medium** | `actions/checkout@v4`, `setup-python@v5`, and unbounded Hatchling minor/major behavior may drift. |
| 7 | Python metadata supports `>=3.12` while CI tests 3.12 only | **P2 medium** | Later Python versions are accepted without evidence. macOS is not exercised. |
| 8 | Local refs are not a live remote/release verification | **P2 medium** | Local `origin/main` and tag alignment does not prove current GitHub branch, release assets, or source-archive state. |

### Git and dirty state are necessary but insufficient

A Git commit identifies tracked content. A boolean dirty flag says ordinary
tracked/untracked status existed, but it does not store the diff, ignored files,
dependency wheels, OS state, or external services. It also depends on Git being
available to metadata collection. Day 4C is the canonical example:
`dirty=true` honestly warns that its commit does not reconstruct the candidate.

### Immediate preservation implication

The six pre-existing Day 6 documents plus this final review should be reviewed,
hashed, and backed up independently before relying on GitHub. Because Day 6E is
not authorized to modify prior documents or commit, `recovery-manifest.md`
cannot be updated here. That is an explicit residual preservation gap, not a
reason to alter the manifest silently.

## 13. Hashing and integrity challenge

### What each hash proves

| Identity | It can establish | It cannot establish |
|---|---|---|
| File SHA-256 | Exact bytes match a trusted expected digest | Who created the file, whether it is true/safe, or whether both file and digest were replaced |
| Tool fingerprint | Canonically represented normalized metadata is unchanged under this implementation/version | Publisher identity, runtime behavior, safety, or absence of semantically equivalent evasion |
| Component fingerprint | Which represented component changed | Whether the change is benign, malicious, authorized, or complete relative to an external server |
| Corpus hash | Manifest semantics plus referenced path/content identities match | Independent authorship, label truth, representativeness, or lack of paraphrase leakage |
| Configuration hash | Recorded semantic settings/rules match | That settings are optimal, code behaved correctly, or the run was blind |
| Experiment ID | Timestamped corpus/config prefix names one run | Authenticity, uniqueness against deliberate forgery, or scientific validity |

### Integrity change detection versus maliciousness detection

Hashing answers “is this represented object identical to the trusted reference?”
It does not answer “is this object malicious?” A malicious catalog can have a
perfectly stable hash. A benign authorized update changes its hash. A trusted
baseline and review process give a hash operational meaning.

### Canonicalization and newline caveat

Tool fingerprints canonicalize normalized tool objects, so object-key order,
JSON whitespace, and NFC-equivalent spelling do not change the logical tool
identity. Lists remain ordered and meaningful content changes do change it.

Corpus identity is different: it canonicalizes the manifest model but includes
SHA-256 of decoded referenced file text. Newline conversion therefore changes
those file digests. Day 6D reproduced this on Windows. This behavior is
deterministic, but checkout policy becomes part of identity and must be hardened
or prominently controlled.

SHA-256 collision is not a practical risk for this project under ordinary
assumptions. The practical risks are wrong trust anchor, changed line endings,
altered canonicalization/version semantics, and unsigned replacement—not a
cryptanalytic collision.

## 14. Static-analysis security-boundary challenge

### What remains inert

Source inspection supports the central invariant:

- static scanning reads JSON, validates/normalizes it, traverses text, applies
  fixed logic, and emits data;
- custom rules are bounded literal strings, not user regex or executable
  expressions;
- representation decoding is strict, depth one, bounded, and never executed;
- metadata/icon/schema references are not followed;
- baselines hash and summarize metadata without invoking tools; and
- no catalog is sent to a model.

### Where “static” can be misunderstood

The `fetch` command is an explicit network acquisition path. It creates an MCP
client session, sends initialization/listing requests needed for `tools/list`,
and saves/normalizes metadata. It does not call advertised tools, but the total
operation is not “no network.” “Static” describes the analyzed object and lack
of tool execution, while file scanning remains the offline default.

The retrieval boundary is unusually strong: explicit HTTP(S), loopback-only,
localhost resolution checking and pinning, no credentials in URLs, no redirect,
`trust_env=False`, cumulative response limit, timeout, page/cursor/tool limits,
and post-response validation. A malicious local server is still untrusted and
can attack the parser or availability within those bounds.

Filesystem interaction also exists:

- scan/report commands read user-selected files and may overwrite an explicitly
  selected output path;
- baseline creation writes a timestamped baseline and records its source;
- comparison reads an untrusted baseline;
- evaluation writes artifacts when requested.

These are ordinary controlled I/O, not metadata execution. The threat model
should say so rather than implying the process is purely memory-only.

### Residual static-boundary risks

- dependency/supply-chain compromise can violate all source-level assurances;
- a `$ref` can remain an inert unresolved schema reference and validation does
  not prove referenced semantics;
- time-of-check/time-of-use catalog replacement is not prevented;
- a compromised baseline/suppression store can change review outcomes;
- local output files can retain sensitive metadata; and
- report viewers can mishandle inert strings after `mcpsec` safely serializes
  them.

## 15. Output-safety challenge

| Path | Current mitigation | Residual risk |
|---|---|---|
| Terminal | ESC/control escaping, ASCII backslash replacement, Rich markup escaping, bounded evidence | Newlines/tabs can still alter layout; fully truncated tools can be counted “clean”; huge tool metadata is not shown but source names may leak |
| JSON | Typed JSON serialization, no ANSI control sequences from renderer | Full original tool metadata and source remain, including under `--redact`; downstream HTML/log viewers must escape it |
| CSV | NUL removal, leading tab/CR and formula-prefix neutralization, standard CSV quoting | Downstream transformations may strip the apostrophe; application-specific formula syntax may evolve; sensitive evidence remains unless redacted |
| SARIF | JSON encoding, fixed severity mapping, bounded findings | Tool name/evidence/source URI remain hostile and possibly private; third-party SARIF viewers define final rendering safety |

`--redact` replaces finding evidence excerpts only. It does not redact the
copied `ToolDefinition`, report source, tool name, schema, metadata, or
recommendation. README documents this correctly, but the option name can create
a false privacy expectation. A future interface should distinguish “evidence
redaction” from “metadata-minimized report.”

Other residual concerns:

- reports can become sensitive research/operational records and need access,
  retention, encryption, and deletion policy;
- SARIF `artifactLocation.uri` can reveal an absolute private path supplied as
  source;
- baseline `source` can also retain a local path;
- evidence truncation can remove exculpatory context and must remain visible;
- JSON/SARIF are data-safe only if consumers treat text as text; and
- no digital signature authenticates a report.

## 16. Resource-limit challenge

### Existing controls

| Control | Current value | Failure reduced | Limit behavior |
|---|---:|---|---|
| Catalog/baseline bytes | 10 MiB | Oversized file/memory use | Reject |
| Rule/suppression bytes | 1 MiB | Config parsing abuse | Reject |
| Text/key length | 100,000 characters | Huge scalar work/output | Reject |
| Nesting/nodes | 64 / 100,000 | Deep recursion and structural bombs | Reject |
| Static tools | 1,000 | Catalog fan-out | Reject |
| Retrieval pages/tools | 100 / up to 1,000 (500 default) | Infinite pagination/fan-out | Reject |
| YAML aliases/nodes | 50 / 10,000 | Alias expansion/cycles | Reject |
| Rules/suppressions | 200 / 500 | Policy fan-out | Reject |
| Findings | 64/tool, 2,048/report | Report size and analyst overload | Deterministically retain and mark truncation |
| Retained evidence | 8,192 chars/tool; 240-char excerpts | Report/memory leakage | Truncate/stop retention and mark |
| Decode | 512 input/output, 4 candidates/field, 32/tool, 4,096 retained chars | Decode expansion and semantic explosion | Skip/record bounded INFO issue |

The numbers are plausible engineering ceilings, not empirically derived safe
maxima. A future security case should justify them through complexity analysis
and adversarial tests.

### Can an attacker exploit truncation?

Yes, under current decision coupling. Earlier high-volume tools can consume the
global retained budget so later findings no longer affect risk, `--fail-on`, or
evaluation classification. Catalog order is attacker-controlled input. Within a
tool, findings are severity-first and deterministic, which is preferable to
arbitrary dropping, but the evidence loop stops at the first item that would
exceed the evidence budget instead of considering whether later shorter items
could fit.

Determinism is valuable for reproducibility, but deterministic unfairness is
still a problem. Truncation may introduce measurement bias if corpora or
categories systematically generate more findings or longer evidence. The H0
did not truncate, so its metrics are not affected.

### Finding budget is not a full compute budget

The scanner builds every detector's finding list before retention. Input bounds
place an outer ceiling on document size, but there is no explicit intermediate
finding count/work budget. A future test should measure a maximally repetitive
100,000-node catalog and prove acceptable time/memory or move to bounded
incremental detection while preserving decision semantics.

## 17. Historical artifact-comparison challenge

Supporting schema `3.0.0` and current schema `3.1.0` is necessary because H0 and
Day 4C are historical evidence. Current code validates sample identities,
counts, predictions, findings, metrics, uncertainty, strata, timing,
configuration hashes, experiment IDs, and finding budgets where present.

Important limits:

- internal consistency is not authenticity; a sophisticated editor can rewrite
  an artifact and recompute all unkeyed internal hashes;
- authenticity depends on external file hashes/Git or a future signature;
- current-pack artifacts are checked against the current registry, while a
  historical pack lacks a complete executable registry in source;
- historical samples' risk is rechecked using the current
  `calculate_risk()` function. A future risk-model change could make authentic
  old artifacts fail unless migration/registry behavior is versioned;
- the loader uses current Pydantic models/defaults to represent both schemas,
  so future schema evolution needs explicit fixtures and migration policy;
- Day 4C claims old package/rule-pack metadata while holding a dirty 16-rule
  configuration. The warning is essential and must never be “corrected” in
  place; and
- users can ignore `comparable_with_warning` and quote paired deltas as if the
  treatments were independently confirmed.

Comparison must be invalidated when corpus hash, split, sample population,
paired ground truth, or threshold differs. Different code/rule identities,
dirty state, configuration, timing boundary, or environment must at least
qualify interpretation. Latency requires an exact boundary/environment match,
but even then background-load differences remain.

## 18. Baseline and drift challenge

The subsystem appropriately answers “what represented metadata changed?” It
does not answer “why did it change?” or “is it malicious?”

Strengths:

- normalized canonical full and component SHA-256 identities;
- raw descriptions/schema values omitted from baseline summaries;
- exact-name change/add/remove detection;
- conservative rename inference only for a unique old/new exact component
  signature; and
- bounded, strictly loaded baseline files.

Limits:

- a renamed **and edited** tool is add+remove, not inferred rename;
- duplicate/ambiguous component signatures suppress rename inference;
- benign documentation/version/schema maintenance creates drift;
- an attacker can generate constant churn to create alert fatigue;
- a compromise of both catalog and unprotected baseline can erase apparent
  drift;
- hashes do not authenticate the publisher or approval event;
- rollback to an older but valid baseline is not detected by the format;
- host/runtime capability can change without metadata drift; and
- source/path and canonicalization-version semantics affect stored identity.

Appropriate claim:

> Baseline comparison provides deterministic canonical metadata change
> detection and field-level triage when the baseline store and approval process
> are trusted.

Inappropriate claim:

> A matching baseline proves the current server is safe or unchanged at runtime.

## 19. Project-positioning challenge

From least to most likely to mislead:

1. **Metadata inspector** — safest; accurately emphasizes human review.
2. **Research prototype** — safe but too generic unless paired with function.
3. **Static analyzer** — accurate if “MCP tool-definition metadata” and inert
   scope are stated.
4. **Lightweight detector** — acceptable with corpus/status qualification;
   “lightweight” is supported only in the recorded environment.
5. **Tool-poisoning detector** — potentially overbroad because several rules are
   security/schema review signals and malicious intent is not observed.
6. **Security scanner** — most likely to imply comprehensive or production-grade
   assurance.

Recommended public/FYP positioning:

> A pre-FYP defensive research prototype for deterministic, bounded static
> inspection and drift detection of MCP tool-definition metadata. It emits
> explainable review indicators; it does not certify tools or observe runtime
> behavior.

## 20. Contribution assessment

“Novelty” cannot be established from the repository alone; it requires a
systematic literature and related-tool review. The classifications below assess
what this project has actually demonstrated, not priority over prior work.

| Candidate contribution | Classification | Adversarial assessment |
|---|---|---|
| Bounded, inert MCP metadata inspection architecture | **STRONG CONTRIBUTION** | Substantially implemented and security tested; research novelty still unknown |
| Stable-ID rule-based suspicious metadata detection | **MODERATE CONTRIBUTION** | Explainable implementation exists, but H0 effectiveness is poor and construct is broad |
| Canonical tool/component fingerprints | **MODERATE CONTRIBUTION** | Useful application of established canonical hashing; no independent drift-effectiveness study |
| Baseline change and conservative rename analysis | **SUPPORTING ENGINEERING** | Coherent feature; trusted-storage/longitudinal evaluation remains absent |
| Reproducible MCP security evaluation engine | **STRONG CONTRIBUTION** | Typed corpus/config identity, uncertainty, ablation, runtime metadata, and comparison are strong |
| One independently reviewed pilot holdout | **MODERATE CONTRIBUTION** | Better than author labels alone; limited by one reviewer, synthetic authorship, matched/confounded design |
| Honest frozen negative H0 and post-unblinding separation | **STRONG CONTRIBUTION** | Strong research practice and learning value; not proof of detector effectiveness |
| Day 3 failure taxonomy and v0.3 hypothesis trace | **MODERATE CONTRIBUTION** | Grounded mechanism discovery; post-unblinding by definition |
| Strict bounded one-layer decoding | **SUPPORTING ENGINEERING** | Safe implementation combination; no exposed-holdout recovery and no novelty claim |
| Historical artifact self-consistency/comparison | **STRONG CONTRIBUTION** | Valuable preservation machinery with explicit warnings; authenticity/migration gaps remain |
| Heuristic aggregate risk score | **NOT YET ESTABLISHED** as research contribution | Deterministic but not calibrated or validated as a meaningful risk measure |
| Improved v0.3 generalization | **NOT YET ESTABLISHED** | No fresh untouched holdout |
| Production MCP security protection | **NOT YET ESTABLISHED** | H0, scope, and residual implementation risks rule out the claim |

## 21. Ten strongest and ten weakest aspects

### Strongest aspects, ranked

1. **Scientific honesty:** unfavorable H0 was preserved as authoritative and not
   replaced by v0.3.
2. **Explicit inert boundary:** no scanned tool execution, model submission, or
   metadata-linked fetch.
3. **Strict hostile-input handling:** duplicate JSON keys, non-finite numbers,
   structure, YAML, retrieval, and decoding are bounded.
4. **Reproducible evidence identity:** corpus/config/artifact/Git/runtime records
   make many hidden differences visible.
5. **Typed deterministic architecture:** clear modules, stable IDs, fixed order,
   normalized data, and repeat-consistency checks.
6. **Broad engineering verification:** 472 tests, 92.95% coverage, strict typing,
   lint/format, build, and installed-wheel smoke at the preserved checkpoint.
7. **Independent blinded label review:** imperfect but preserved fully,
   including disagreement and difficulty divergence.
8. **Canonical fingerprints and drift:** meaningful support for the original
   metadata-change FYP idea.
9. **Output/retrieval defense in depth:** terminal/CSV hardening plus an unusually
   narrow loopback transport.
10. **Continuity documentation:** technical map, teaching manual, handover,
    recovery process, and this adversarial review help the student own the work.

### Weakest aspects, ranked

| Rank | Weakness | Severity | Threatens FYP? | Supervisor discussion? | Must address before future confirmation? | Can only be acknowledged? |
|---:|---|---|---|---|---|---|
| 1 | No fresh independent evidence for v0.3 | Critical research | Yes, for effectiveness conclusion | Yes | Yes—new protocol/holdout | Current exploratory status must also be acknowledged |
| 2 | Retained-finding budget controls risk, exit, and evaluation label | High implementation | Yes, if candidate behavior is studied | Yes | Yes | No; decision semantics need resolution |
| 3 | Target label conflates poisoning, schema quality, capability review, and suspiciousness | High construct | Yes | Yes | Yes—refine/partition construct | R08 remains a limitation |
| 4 | H0 recall 20.83% and FPR 25% | High effectiveness | Yes, for production claims | Yes | Cannot “fix” H0; future candidate/evidence needed | Yes as historical fact |
| 5 | Synthetic, English, small, balanced, matched/confounded corpora | High external/conclusion validity | Yes | Yes | Data/statistical plan needed | Some limits will remain |
| 6 | Fixed lexical/context rules are adaptively bypassable | High design | Yes, depending on question | Yes | Define accepted scope and comparison | Yes; completeness is impossible |
| 7 | One reviewer and only 16/48 difficulty agreement | Medium-high label validity | Yes for subgroup claims | Yes | Stronger review plan needed | Historical limitation remains |
| 8 | Uncalibrated severity, score, synergy, and MEDIUM threshold | Medium-high design/method | Yes for risk/operational claims | Yes | Justify/freeze prospectively | Historical choices stay frozen |
| 9 | Reproducibility gaps: untracked/ignored records, CRLF, no exact lock, dirty v0.3 | High preservation | Yes if evidence is lost/misreconstructed | Yes | Preserve and harden before next freeze | Dirty historical provenance remains |
| 10 | Evidence-only redaction and downstream report/privacy assumptions | Medium security/privacy | Not for narrow pilot, yes for real catalogs | Yes before real data | Define privacy/output policy | Current documented caveat can be acknowledged |

## 22. The 50 hardest viva questions

These questions deliberately go beyond recall of architecture. “Repository
evidence” means evidence for the answer's factual basis, not proof that the
broader scientific claim is true.

### 1. What is your falsifiable target construct?

- **Best defensible answer:** The current pilot target is whether a tool
  definition contains a frozen rubric's suspicious security-review constructs,
  not whether the publisher is malicious. A formal FYP should partition
  agent-influence poisoning from schema quality and disclosed capability review,
  then define observable inclusion/exclusion rules before data creation.
- **Dangerous answer to avoid:** “Anything my detector flags is tool poisoning.”
- **Repository evidence:** Holdout README label rubric; `docs/tool-poisoning.md`;
  R08 adjudication; seven categories.
- **Confidence:** **HIGH**

### 2. Why is malformed schema in the same ground truth as concealment?

- **Best defensible answer:** It was included under a broad pre-existing
  “security-review construct” taxonomy because invalid schemas can produce
  inconsistent client behavior. The pilot preserved that decision, but R08
  shows it should not be equated with malicious poisoning. A future protocol
  should report schema quality separately or justify the combined outcome.
- **Dangerous answer to avoid:** “Malformed schemas are attacks.”
- **Repository evidence:** `SCH-001` rationale, holdout README, review ledger,
  R08.
- **Confidence:** **HIGH**

### 3. How can you label malicious intent from synthetic metadata alone?

- **Best defensible answer:** I cannot. Labels identify authored constructs under
  a rubric. The detector is intent-neutral and requires human/contextual review.
  Claims about maliciousness would require provenance, threat intelligence,
  runtime evidence, or another validated method.
- **Dangerous answer to avoid:** “Suspicious wording proves intent.”
- **Repository evidence:** Threat model out-of-scope statement; tool-poisoning
  documentation; finding explanations.
- **Confidence:** **HIGH**

### 4. Is tool-description poisoning really distinct from indirect prompt injection?

- **Best defensible answer:** It is a specialized provenance and lifecycle case:
  untrusted content arrives through a discovered tool definition. The linguistic
  mechanism may be indirect prompt injection, while capability mismatch/schema
  findings are adjacent metadata-integrity concerns. I should not claim an
  entirely independent phenomenon without literature support.
- **Dangerous answer to avoid:** “They are completely unrelated attacks.”
- **Repository evidence:** Tool metadata boundary and prompt/tool terminology in
  the Captain's Manual.
- **Confidence:** **MEDIUM** pending literature synthesis

### 5. On what theory were the 16 rules selected?

- **Best defensible answer:** They operationalize seven repository-defined
  constructs through explicit lexical, contextual, schema, consistency,
  capability, and bounded-representation checks. Selection is traceable to the
  threat taxonomy and Day 3 failure hypotheses, but it is not a complete or
  literature-proven ontology. A formal study needs a construct-to-literature-
  to-rule traceability matrix.
- **Dangerous answer to avoid:** “These are all possible poisoning patterns.”
- **Repository evidence:** Detector registry, `RULE_EXPLANATIONS`, Day 4A/4C
  records, handover backlog.
- **Confidence:** **HIGH** about provenance; **LOW** about completeness

### 6. Why should `PI-001` be HIGH and `CAP-001` only INFO?

- **Best defensible answer:** The design treats explicit model-priority
  manipulation as stronger evidence of unsafe influence, while openly disclosed
  capability is often legitimate and mainly supports triage/cross-field logic.
  These severities are defensible heuristics, not empirically calibrated harm
  estimates.
- **Dangerous answer to avoid:** “HIGH means an 86% probability of attack.”
- **Repository evidence:** `injection.py`, `permissions.py`, builtin rationales,
  risk documentation.
- **Confidence:** **HIGH** about implementation, **MEDIUM** about rationale

### 7. Why use a probability-like risk aggregation for non-probability inputs?

- **Best defensible answer:** The complement-product is a bounded heuristic that
  increases with independent categories without linear explosion. Confidence
  and scores are engineering weights, not probabilities; the result is
  prioritization metadata. A future operational claim would require calibration
  or a different interpretation.
- **Dangerous answer to avoid:** “A risk score of 60 means a 60% chance of
  compromise.”
- **Repository evidence:** `risk.py` and `docs/risk-scoring.md`.
- **Confidence:** **HIGH**

### 8. Why was MEDIUM chosen, and what makes it optimal?

- **Best defensible answer:** It was frozen prospectively for this pilot and
  separates INFO/LOW context signals from stronger review findings. The project
  has not shown it is optimal. Future operating-point selection needs
  preregistered costs/targets and untouched data; post-H0 threshold tuning cannot
  revise H0.
- **Dangerous answer to avoid:** “MEDIUM gave the best holdout F1.”
- **Repository evidence:** Holdout plan/configuration hash; H0 artifact; 17
  no-finding false negatives.
- **Confidence:** **HIGH**

### 9. Why do finding severity and aggregate risk produce two different decisions?

- **Best defensible answer:** Severity represents one rule's review urgency;
  aggregate risk combines distinct categories for presentation. Evaluation and
  `--fail-on` use individual severity. The separation is documented, but it is
  cognitively risky and requires explicit UI/claim language.
- **Dangerous answer to avoid:** “They are equivalent.”
- **Repository evidence:** `scanner.py`, `risk.py`, `cli.py`,
  `evaluation/evaluator.py`.
- **Confidence:** **HIGH**

### 10. Can output limits change whether a tool is considered suspicious?

- **Best defensible answer:** Yes, in the current alpha. Risk, fail-on, terminal
  affected count, and evaluation prediction use retained findings; the global
  report budget can leave later detected findings unretained. This is a Day 6E
  implementation defect to resolve before another freeze. H0/v0.3 artifacts had
  no truncation and are unaffected.
- **Dangerous answer to avoid:** “The limit only changes display.”
- **Repository evidence:** `scanner.py:77-80`, `cli.py:155-161`,
  `evaluator.py:163-180`; artifact finding counts.
- **Confidence:** **HIGH**

### 11. Can an attacker use catalog ordering to influence the result?

- **Best defensible answer:** Under report-budget exhaustion, yes. Tools retain
  input order, and earlier findings consume global capacity. Deterministic order
  makes runs reproducible but does not make the security decision order-neutral.
- **Dangerous answer to avoid:** “Determinism prevents manipulation.”
- **Repository evidence:** `scanner.analyze_tools()` loop and shared
  `findings_retained`.
- **Confidence:** **HIGH**

### 12. Do your resource limits bound detection memory, or only output?

- **Best defensible answer:** They strongly bound input and retained output, but
  detector findings are materialized before retention. Worst-case intermediate
  finding allocation has not been demonstrated as safely bounded in practice.
  It requires adversarial measurement or a bounded incremental design.
- **Dangerous answer to avoid:** “The 2,048 finding limit caps all memory.”
- **Repository evidence:** Finding list comprehension at `scanner.py:74`,
  retention at lines 77 onward.
- **Confidence:** **HIGH** about code path, **MEDIUM** about exploitability

### 13. Why NFC rather than NFKC or confusable detection?

- **Best defensible answer:** NFC gives stable canonical equivalence without
  compatibility-folding characters that may be intentionally distinct. It is a
  normalization choice, not a complete anti-obfuscation solution. Confusables
  and compatibility characters remain future research/design questions.
- **Dangerous answer to avoid:** “NFC prevents Unicode spoofing.”
- **Repository evidence:** `normalizer.py`, `canonicalizer.py`, `OBF-001`.
- **Confidence:** **HIGH**

### 14. Does publishing regexes make the detector useless against adaptive attackers?

- **Best defensible answer:** It makes evasion easier, but hiding patterns would
  not provide robust security and would harm auditability. The detector is a
  transparent review aid; adaptive robustness must be measured on unseen
  paraphrases/representations or compared with other approaches.
- **Dangerous answer to avoid:** “Attackers will not read the source.”
- **Repository evidence:** Open detector modules, H0 no-finding false negatives,
  explicit limitations.
- **Confidence:** **HIGH**

### 15. What happens with Malay, Mandarin, Arabic, or mixed-language metadata?

- **Best defensible answer:** Most semantic rules are English-oriented and may
  miss them; Unicode presentation checks may still fire. Current corpora are
  English-only, so no multilingual effectiveness claim exists.
- **Dangerous answer to avoid:** “Regex works for any language.”
- **Repository evidence:** Fixed English patterns and frozen limitation.
- **Confidence:** **HIGH**

### 16. Can splitting a relation across fields bypass contextual rules?

- **Best defensible answer:** Yes. Text values are intentionally not concatenated
  to avoid false relationships, so a priority term in one field and conflict
  target in another may not match. That is a precision/coverage tradeoff.
- **Dangerous answer to avoid:** “All fields are scanned, so cross-field attacks
  cannot bypass it.”
- **Repository evidence:** `all_text_fields()` and per-value local matching;
  architecture documentation.
- **Confidence:** **HIGH**

### 17. Why retain `OBF-005` if it recovered no encoded holdout case?

- **Best defensible answer:** It implements a bounded safety mechanism and passes
  authored suspicious/benign representation tests. On the exposed holdout it
  recovered no case, so its external contribution is unconfirmed. Retention as
  an exploratory candidate is defensible; claiming effectiveness is not.
- **Dangerous answer to avoid:** “It solved obfuscation because its fixtures pass.”
- **Repository evidence:** Representation tests, Day 4C contribution report,
  tracked artifact.
- **Confidence:** **HIGH**

### 18. Did `SEC-002` make the detector worse?

- **Best defensible answer:** On the exposed holdout it recovered no true
  positive and added findings to two already-false-positive benign cases. That
  is an unfavorable diagnostic observation, not a universal verdict. Its
  authored mechanism fixtures work, but future hard negatives and untouched
  evidence are required.
- **Dangerous answer to avoid:** “It improved security because more findings are
  always better.”
- **Repository evidence:** Day 4C failure-recovery and rule-contribution records.
- **Confidence:** **HIGH**

### 19. Are v0.3 gains mostly one rule memorizing known failures?

- **Best defensible answer:** Four of six recovered cases came from `MIS-002`,
  with one each from `PI-002` and `HID-002`. The rules were designed from abstract
  failure mechanisms rather than copied strings, but concentration plus exposed
  reuse means overfitting cannot be excluded.
- **Dangerous answer to avoid:** “The gains are broad across all five new rules.”
- **Repository evidence:** Day 4C recovery map and tracked sample predictions.
- **Confidence:** **HIGH**

### 20. Why does disclosed high capability not make a sample suspicious at MEDIUM?

- **Best defensible answer:** `CAP-001` is INFO because capability alone is often
  legitimate. It supports triage and cross-field contradiction but should not
  blanket-label administrative tools. Whether the corpus's `capability` ground
  truth aligns with that threshold is itself a construct issue.
- **Dangerous answer to avoid:** “Any powerful tool is malicious.”
- **Repository evidence:** `permissions.py`, holdout capability category,
  threshold semantics.
- **Confidence:** **HIGH**

### 21. How did you determine that 80 development samples were enough?

- **Best defensible answer:** They were enough to exercise authored regression
  mechanisms, not statistically justified as a representative sample. No power
  or saturation argument supports external inference.
- **Dangerous answer to avoid:** “Eighty is a large dataset.”
- **Repository evidence:** Development README and methodology limitations.
- **Confidence:** **HIGH**

### 22. How did author awareness of rules bias the corpora?

- **Best defensible answer:** Development examples can mirror rule vocabulary;
  holdout authors knew the taxonomy/project even without predictions; v0.3
  fixtures were explicitly mechanism-authored after unblinding. This likely
  makes regression performance optimistic and requires independent authorship
  or source sampling in a future study.
- **Dangerous answer to avoid:** “Blinding predictions removed all author bias.”
- **Repository evidence:** Corpus provenance and holdout independence statement.
- **Confidence:** **HIGH**

### 23. Are your benign negatives realistic enough to estimate alert fatigue?

- **Best defensible answer:** They deliberately include security,
  administration, credentials, privacy, and quotation hard negatives, which is a
  strength. They remain synthetic and cannot estimate the frequency/diversity
  of real benign metadata, so operational alert fatigue is unknown.
- **Dangerous answer to avoid:** “Six false positives means real users will see
  exactly 25%.”
- **Repository evidence:** Holdout sampling rubric and coverage report.
- **Confidence:** **HIGH**

### 24. In what sense was the holdout independent?

- **Best defensible answer:** It was a separate prediction-unexposed batch, not
  run through the detector before freeze, and reviewed by one blinded external
  human. It was still repository-authored by someone with taxonomy knowledge;
  it was not double-blind or externally sampled.
- **Dangerous answer to avoid:** “It was fully independent.”
- **Repository evidence:** Holdout README and coverage-report boundary.
- **Confidence:** **HIGH**

### 25. Are Wilson intervals valid with eight matched pairs?

- **Best defensible answer:** The recorded intervals use ordinary binomial
  denominators and are transparent, but matched/derived dependence can reduce
  effective information and is not modeled. A future protocol should obtain
  statistical advice and use cluster/paired methods or more independent sources.
- **Dangerous answer to avoid:** “Wilson automatically handles paired samples.”
- **Repository evidence:** Uncertainty implementation, matched-pair disclosure,
  handover statistics questions.
- **Confidence:** **MEDIUM** pending formal statistical design

### 26. What happens to precision when suspicious prevalence is 1% rather than 50%?

- **Best defensible answer:** It can drop sharply because most inputs are benign.
  H0 sensitivity/specificity can illustrate scenarios only under strong
  transportability assumptions; the balanced holdout's 45.45% precision is not
  deployable prevalence evidence.
- **Dangerous answer to avoid:** “Precision stays 45.45%.”
- **Repository evidence:** 24/24 design, metric definitions, limitations.
- **Confidence:** **HIGH**

### 27. Why N=48 and what precision was targeted?

- **Best defensible answer:** The pilot balanced practical construction/review
  effort and category coverage; it did not document a prospective interval
  width/power calculation. That is a limitation. Future N must follow the chosen
  primary estimand and acceptable interval width/effect.
- **Dangerous answer to avoid:** “N=48 is statistically significant.”
- **Repository evidence:** Plan, Wilson intervals, handover supervisor questions.
- **Confidence:** **HIGH**

### 28. Which outcome was truly primary?

- **Best defensible answer:** The full-detector configuration was primary, with
  TP/TN/FP/FN, precision, recall, F1, and FPR listed as primary outputs; accuracy
  was secondary in the historical plan. No single primary metric/minimum effect
  was selected, so future work must define one or a decision rule to prevent
  metric cherry-picking.
- **Dangerous answer to avoid:** “Whichever metric improved most.”
- **Repository evidence:** `docs/holdout-experiment-plan.md`.
- **Confidence:** **HIGH**

### 29. Was the null hypothesis actually testable?

- **Best defensible answer:** It was directionally stated but “useful
  discrimination beyond the agreed descriptive baseline” lacks a numerical
  baseline, test, alpha, or practical threshold. H0 is best called a frozen
  descriptive confirmatory pilot, not a definitive null-hypothesis test.
- **Dangerous answer to avoid:** “The null was statistically rejected.”
- **Repository evidence:** Historical plan and absence of a formal test.
- **Confidence:** **HIGH**

### 30. Did H0 perform worse than the trivial all-benign classifier?

- **Best defensible answer:** Its 47.92% accuracy was lower than the 50% accuracy
  of all-benign on this exactly balanced corpus, but it detected five suspicious
  constructs while incurring six false positives. That comparison shows accuracy
  alone is inadequate; it does not prove “worse than random” without a defined
  statistical baseline.
- **Dangerous answer to avoid:** “Yes, therefore every contribution is useless.”
- **Repository evidence:** H0 matrix and 24/24 balance.
- **Confidence:** **HIGH**

### 31. Is an honest negative pilot publishable?

- **Best defensible answer:** It can be valuable if the research question,
  related work, method, artifact preservation, and failure analysis contribute
  knowledge. Publication novelty/venue fit cannot be inferred from code. For an
  FYP, an honest negative result plus rigorous engineering is defensible.
- **Dangerous answer to avoid:** “Any negative result is automatically
  publishable.”
- **Repository evidence:** Frozen H0, Day 3C, reproducibility chain.
- **Confidence:** **LOW** for publication outcome, **HIGH** for scientific value

### 32. Does kappa 0.9583 validate the detector?

- **Best defensible answer:** No. It compares one independent reviewer's binary
  labels with original labels. It says nothing about detector predictions and
  does not prove label truth, expertise, or external validity.
- **Dangerous answer to avoid:** “The reviewer showed the detector is 95.83%
  correct.”
- **Repository evidence:** Review ledger and kappa calculation.
- **Confidence:** **HIGH**

### 33. Why was R08 not relabeled after disagreement?

- **Best defensible answer:** The original frozen rubric explicitly included
  malformed-schema security review, and adjudication occurred without detector
  output. Preserving the original plus reviewer disagreement avoids silent
  outcome-driven relabeling. Future work should refine the construct rather than
  rewrite history.
- **Dangerous answer to avoid:** “The reviewer was wrong.”
- **Repository evidence:** R08 ledger/source and corpus version 1.0.1.
- **Confidence:** **HIGH**

### 34. Can you defend difficulty-stratified claims with 16/48 agreement?

- **Best defensible answer:** Only as descriptive results using original frozen
  labels, with explicit subjectivity and tiny denominators. Difficulty is not a
  reliable objective ordering here.
- **Dangerous answer to avoid:** “Subtle samples objectively measure harder
  attacks.”
- **Repository evidence:** Reviewer 22/19/7 versus original 16/16/16.
- **Confidence:** **HIGH**

### 35. Why isn't v0.3's recall increase evidence of improved generalization?

- **Best defensible answer:** The same holdout failures directly informed the
  candidate, so the sample is no longer unseen for the design process. The
  increase is an exposed paired diagnostic; generalization requires a fresh
  untouched population.
- **Dangerous answer to avoid:** “Recall doubled, so generalization improved.”
- **Repository evidence:** Day 3C→Day 4A→Day 4B→Day 4C chronology.
- **Confidence:** **HIGH**

### 36. Can the dirty v0.3 artifact be reproduced exactly?

- **Best defensible answer:** Not from its recorded commit alone. Its full
  configuration, rule identities, runtime, and exact artifact are preserved,
  but the uncommitted source diff is not embedded in the tracked artifact. It is
  authentic exploratory evidence with a reproducibility warning.
- **Dangerous answer to avoid:** “The commit fully identifies it.”
- **Repository evidence:** `dirty=true` and old package/rule-pack metadata in
  Day 4C.
- **Confidence:** **HIGH**

### 37. What does 100% on the 36 v0.3 construct fixtures prove?

- **Best defensible answer:** It proves the current implementation recognizes the
  authored intended mechanisms and benign counterexamples in that development
  set. It does not estimate unseen performance because fixtures were created for
  those mechanisms post-unblinding.
- **Dangerous answer to avoid:** “v0.3 is 100% accurate.”
- **Repository evidence:** Exploratory manifest status and Day 4B/4C records.
- **Confidence:** **HIGH**

### 38. Do family ablations identify causal protective value?

- **Best defensible answer:** No. They withhold selected outputs in the same
  detector/corpus and report paired prediction changes. Families overlap and
  share helpers; the observed delta is treatment/corpus/threshold-specific.
- **Dangerous answer to avoid:** “Sensitive-data rules cause all false
  positives.”
- **Repository evidence:** Ablation implementation and H0 ablation matrices.
- **Confidence:** **HIGH**

### 39. Why not use ablation timing to rank efficient rules?

- **Best defensible answer:** Each H0 ablation used one measured repetition and
  family filtering does not necessarily isolate sub-rule compute. Background
  noise can exceed tiny differences. It was not a confirmatory timing outcome.
- **Dangerous answer to avoid:** “The family with the lowest one-run mean is
  fastest universally.”
- **Repository evidence:** Plan's 0 warm-up/1 repetition ablations and protocol.
- **Confidence:** **HIGH**

### 40. Does 1.7159 ms prove deployment suitability?

- **Best defensible answer:** No. It is analysis-core time on small static pilot
  samples in one environment, excluding acquisition, reporting, network,
  process startup, host integration, and maximum-size inputs. It supports a
  lightweight-local-execution claim only.
- **Dangerous answer to avoid:** “Production scans always take under 2 ms.”
- **Repository evidence:** H0 timing definition and recorded environment.
- **Confidence:** **HIGH**

### 41. Do hashes prove artifact authenticity?

- **Best defensible answer:** A matching digest proves equality to a trusted
  digest. Authenticity depends on how that digest/Git reference was obtained.
  Unkeyed hashes stored beside data can be replaced together.
- **Dangerous answer to avoid:** “SHA-256 proves the result is genuine and safe.”
- **Repository evidence:** Recovery manifest's unsigned warning and external
  digest list.
- **Confidence:** **HIGH**

### 42. Why can Windows line endings change a semantic corpus hash?

- **Best defensible answer:** The corpus identity canonicalizes the manifest
  model but includes SHA-256 of referenced decoded file text, so LF→CRLF changes
  the content digest. Day 6D reproduced this. Use an LF-safe checkout now and
  consider versioned hardening before formal research.
- **Dangerous answer to avoid:** “Line endings never affect canonical hashes.”
- **Repository evidence:** `evaluation/integrity.py:28-62` and disaster-recovery
  audit.
- **Confidence:** **HIGH**

### 43. Can your exact environment be reconstructed months later?

- **Best defensible answer:** The artifacts record resolved direct dependency
  versions and the project has major-bounded runtime dependencies, but Git has
  no exact lock/constraints set. A compatible rebuild is plausible; an exact
  resolver result is not guaranteed.
- **Dangerous answer to avoid:** “`pyproject.toml` reproduces every exact package.”
- **Repository evidence:** `pyproject.toml` and Day 6D dependency audit.
- **Confidence:** **HIGH**

### 44. Could future code reinterpret historical risk incorrectly?

- **Best defensible answer:** Current tests protect real H0/Day 4C fixtures and
  recorded rule sets, but artifact validation recalculates sample risk using the
  current risk function. A future risk change needs versioned historical
  semantics/migration tests or old artifacts may fail or be misinterpreted.
- **Dangerous answer to avoid:** “Supporting schema 3.0 guarantees all future
  compatibility.”
- **Repository evidence:** `evaluation/comparison.py:119-137` imports current
  `calculate_risk`.
- **Confidence:** **HIGH**

### 45. Is loopback `fetch` truly static?

- **Best defensible answer:** Analysis remains static and no advertised tool is
  invoked. The acquisition command is nevertheless networked and initializes an
  MCP client to list tools. “Offline static” applies to file scan; “static” for
  fetch means metadata-only/no tool execution.
- **Dangerous answer to avoid:** “The program never uses a network.”
- **Repository evidence:** `retrieval.py` and `SECURITY.md`.
- **Confidence:** **HIGH**

### 46. Does `--redact` make a JSON report safe to share?

- **Best defensible answer:** No. It redacts finding evidence excerpts only.
  Original tool definitions and source can remain. Sharing requires a separate
  privacy review or metadata-minimizing export.
- **Dangerous answer to avoid:** “Redact removes all secrets and paths.”
- **Repository evidence:** `detectors/base.py:15-19`, `reporter.py:16-17`,
  README privacy caveat.
- **Confidence:** **HIGH**

### 47. Can baseline drift prove compromise?

- **Best defensible answer:** No. It proves canonical represented metadata
  differs from a trusted baseline. Authorization, publisher provenance, runtime
  behavior, and baseline storage integrity determine the security meaning.
- **Dangerous answer to avoid:** “Any changed fingerprint is malicious.”
- **Repository evidence:** `fingerprint.py`, `baseline.py`, `compare.py`,
  limitations.
- **Confidence:** **HIGH**

### 48. What is actually novel?

- **Best defensible answer:** The repository demonstrates a particular
  integration of bounded MCP metadata inspection, explainable rules, canonical
  drift, safe sinks/retrieval, and reproducible historical evaluation. Whether
  any component or combination is novel relative to published work/tools
  remains a literature-review question.
- **Dangerous answer to avoid:** “No one has ever built an MCP security scanner.”
- **Repository evidence:** Implemented architecture; handover literature gaps.
- **Confidence:** **LOW** on novelty, **HIGH** on implemented combination

### 49. What ethics change when you add real-world catalogs?

- **Best defensible answer:** Real metadata may contain secrets, personal data,
  proprietary schemas, identifying URLs, or vulnerable-service details.
  Supervisor/ethics approval, lawful sourcing, consent/license, minimization,
  encryption, access/retention/deletion, disclosure, and safe non-invocation
  procedures must be set before collection.
- **Dangerous answer to avoid:** “Publicly reachable means ethically reusable.”
- **Repository evidence:** Current synthetic-only policy and no-live-data
  boundary.
- **Confidence:** **HIGH**

### 50. Is the project ready to become the final FYP?

- **Best defensible answer:** It is ready to preserve as an alpha and use as a
  pre-FYP foundation. It is not ready for a final effectiveness conclusion or a
  new confirmatory run. First resolve the construct and finding-budget semantics,
  obtain supervisor-approved statistics/data/review protocol, preserve
  dependencies/evidence, freeze one candidate cleanly, and create a genuinely
  untouched holdout.
- **Dangerous answer to avoid:** “The software is finished, so the FYP is done.”
- **Repository evidence:** Handover P0 plan, this audit, and exposed-holdout
  status.
- **Confidence:** **HIGH**

## 23. Mock-viva failure conditions

| Statement that would seriously weaken the viva | Corrected statement |
|---|---|
| “My detector has 91.25% accuracy.” | “91.25% is visible development-regression accuracy; H0 on the pilot holdout was 47.92%.” |
| “v0.3 proves the detector improved.” | “v0.3 improved point estimates on exposed data; fresh confirmation does not exist.” |
| “The reviewer validated the detector.” | “One blinded reviewer assessed labels, not detector predictions.” |
| “Kappa means the labels are 95.83% correct.” | “Kappa indicates very high binary agreement under this two-rating setup, not truth.” |
| “Hashes prove the tool is safe.” | “Hashes detect identity change relative to a trusted digest.” |
| “Regex detects tool poisoning.” | “Fixed rules detect selected suspicious metadata constructs and are bypassable.” |
| “A malformed schema is malicious.” | “It is a schema security/compatibility finding; intent is unknown.” |
| “The holdout was fully independent.” | “It was prediction-unexposed and independently reviewed, but repository-authored with taxonomy knowledge.” |
| “Accuracy below 50% proves worse than random.” | “It underperformed a trivial all-benign accuracy baseline on this balanced corpus; no random-baseline test was preregistered.” |
| “FPR stayed 25%, so v0.3 is safe.” | “All six known false positives remained; operational alert burden is unresolved.” |
| “OBF-005 solves encoded attacks.” | “It safely handles four bounded one-layer representations; unseen coverage is unconfirmed.” |
| “Static means the program never uses a network.” | “File scan is offline; explicit fetch uses loopback MCP discovery but never calls tools.” |
| “Redaction makes reports shareable.” | “It redacts evidence excerpts only; original metadata/source remain.” |
| “The report limit only shortens output.” | “Current alpha decisions use retained findings; Day 6E flags this as a defect.” |
| “Tests prove there are no vulnerabilities.” | “Tests support specified behavior; untested defects, bypasses, and external validity risks remain.” |
| “The v0.3 dirty flag is irrelevant.” | “It preserves authentic provenance and limits exact source reconstruction.” |
| “Wilson intervals solve the small sample.” | “They show binomial uncertainty but do not create more evidence or model matched dependence.” |
| “Ablation proves a family causes protection.” | “It describes paired within-corpus contribution when outputs are removed.” |
| “Millisecond latency proves production readiness.” | “It shows lightweight execution on small fixtures in one recorded environment.” |
| “This is already my completed FYP.” | “It is a strong pre-FYP prototype/pilot awaiting supervisor-approved formal confirmation.” |

## 24. Novelty challenge

Repository inspection can establish implementation, not global novelty. The
project combines:

- deterministic MCP tool-metadata traversal;
- explainable static rules;
- canonical fingerprints and drift;
- bounded hostile input/decoding/output/retrieval;
- typed corpus evaluation and artifact comparison; and
- explicit preservation of negative and post-unblinding evidence.

Possible categories:

| Category | Defensible current position |
|---|---|
| Novel research claim | **Not established.** Requires systematic related-work search and precise differentiator. |
| Novel implementation combination | **Plausible but unproven.** The integrated MCP-specific combination is substantial. |
| Educational engineering | **Clearly established.** The repository demonstrates security/research engineering breadth. |
| Reproducibility contribution | **Strong within the project.** Need compare with existing evaluation frameworks before claiming novelty. |
| Application of established techniques | **Clearly present.** Regex/static analysis, JSON Schema validation, SHA-256, Wilson intervals, SARIF, and baselines are established methods. |

Literature review must investigate MCP security scanners and host controls,
tool-poisoning/indirect-injection taxonomies, static API/schema analysis,
software supply-chain metadata drift, rule-based versus learned injection
detection, adversarial text normalization/decoding, security corpus design,
human annotation, and reproducible detector evaluation. Do not claim “first,”
“novel,” or “state of the art” until that work is complete.

## 25. Undergraduate FYP scope challenge

**Current assessment: appropriately substantial as a pre-FYP foundation, but
too large if every future idea is included in one undergraduate FYP.**

The repository already spans protocol ingestion, hostile parsing, 16 rules,
risk, output safety, fingerprints/drift, retrieval, CLI/packaging, corpora,
statistics, ablation, comparison, and reproducibility. The remaining scientific
work—construct refinement, fresh data, reviewers, statistical planning, one
frozen study, analysis, and thesis—is itself a full FYP.

A defensible formal scope is one primary question, for example:

> Under a supervisor-approved suspicious-metadata construct, how does one frozen
> deterministic detector perform on a genuinely untouched, independently
> reviewed corpus, and what precision/recall/FPR uncertainty results?

Scope-creep triggers:

- adding an LLM/learned/hybrid classifier without making comparison the core
  question;
- runtime sandboxing or dynamic tool invocation;
- arbitrary remote crawling/authentication;
- multilingual coverage across many languages;
- browser GUI/dashboard/mobile application;
- signed provenance infrastructure and a full supply-chain system;
- broad MCP resources/prompts/tool-results analysis;
- real-time host integration across multiple agent products;
- large-scale real-world crawling; or
- repeated detector redesign while the future holdout is being constructed.

The supervisor should choose whether the FYP emphasizes detector effectiveness,
metadata drift, safe architecture, or a bounded method comparison. Trying to
claim all four equally will dilute the thesis.

## 26. Ethics and responsible-security review

### Current prototype

- It does not execute suspicious content or advertised tools.
- It does not fetch icon/schema/vendor resources.
- Opt-in retrieval is loopback-only and metadata-listing-only.
- Corpora are inert, synthetic, and contain no real secrets.
- Open patterns have dual-use evasion value, but transparency supports audit and
  the repository contains no operational exploit execution.

### Future real-world work

Before collecting real metadata:

1. obtain supervisor and institutional ethics/method approval where applicable;
2. define lawful source, license, terms-of-service, consent, and redistribution;
3. avoid unauthorized probing and never invoke discovered tools;
4. minimize collection and strip/store secrets, identifiers, personal data, and
   private paths under an approved protocol;
5. encrypt data and backups; restrict access and define retention/deletion;
6. preserve provenance without unnecessarily identifying vulnerable operators;
7. establish responsible disclosure for credible vulnerabilities;
8. separate public corpus examples from sensitive raw evidence;
9. document reviewer confidentiality and consent; and
10. perform safe publication review so bypass examples teach defense without
    becoming an operational abuse guide.

The inspector itself could be used to test wording until rules no longer fire.
That does not justify hiding the code; it reinforces that the detector cannot be
the only control and that adaptive evaluation is required.

## 27. Final risk register

Likelihood and impact are qualitative project judgments for prioritization, not
measured probabilities.

| ID | Risk | Category | Likelihood | Impact | Current mitigation | Future mitigation | FYP relevance | Priority |
|---|---|---|---|---|---|---|---|---|
| R01 | Exposed holdout reused as “fresh” v0.3 validation | Research integrity | High | Critical | Status repeated in artifacts/docs | New access protocol and genuinely untouched holdout | Invalidates central conclusion | P0 |
| R02 | Poisoning label conflates intent, schema quality, and capability review | Construct validity | High | High | Intent-neutral wording; R08 preserved | Supervisor-approved partitioned construct/rubric | Defines what thesis measures | P0 |
| R03 | Finding retention budget changes risk, fail-on, affected count, and labels | Implementation/security | Medium under ordinary input; attacker-controllable | High | Truncation counts are explicit | Decouple complete decision state from bounded display; regression/adversarial tests | Candidate behavior may be order-dependent | P0 |
| R04 | Low H0 recall leaves most suspicious constructs undetected | Effectiveness | Observed | High | Honest H0/failure taxonomy | Freeze a justified candidate; fresh confirmation | Core pilot result and motivation | Historical/P0 planning |
| R05 | H0 25% FPR creates high review burden | Effectiveness/usability | Observed | High | FP analysis and hard negatives | Predefine acceptable FPR; realistic benign evidence | Operational viability | P0 methodology |
| R06 | Fixed English lexical/context rules are adaptively bypassed | Detector design | High | High | Explainability, bounded context, limitations | Unseen paraphrase/adaptive/multilingual evaluation or approved alternative | Bounds claims | P1 |
| R07 | Synthetic-heavy corpora fail to represent vendor/ecosystem noise | External validity | High | High | Provenance and limitation declared | Licensed/ethical mixed-source or independently authored data | Generalization | P0 data plan |
| R08 | 50% suspicious prevalence distorts precision/accuracy intuition | External/conclusion validity | High | High | Raw counts, FPR, specificity reported | Prevalence scenarios or representative sampling | Deployment claims | P0 methodology |
| R09 | N=48 yields wide intervals and tiny strata | Conclusion validity | High | High | Wilson intervals and low-evidence flags | Prospective sample-size/precision plan | Strength of inference | P0 |
| R10 | Matched pairs violate simple independence assumptions | Statistical design | Medium-high | Medium-high | Pair construction disclosed | Cluster/paired analysis advice; more independent sources | Interval/comparison validity | P0 |
| R11 | Corpus author/taxonomy knowledge creates rule-shaped data | Internal/construct validity | High | High | Split/exposure chronology disclosed | Separate independent authorship and leakage controls | Generalization credibility | P0 |
| R12 | Single reviewer does not establish consensus or truth | Label validity | High | Medium-high | Full blinded record and disagreement | Qualified multiple reviewers/adjudication plan | Ground-truth credibility | P0/P1 |
| R13 | Difficulty labels are unstable (16/48 agreement) | Subgroup validity | Observed | Medium | Original/reviewer values preserved | Operational definition or remove as inferential stratum | Viva/subgroup claims | P1 |
| R14 | Exact hash/leakage checks miss paraphrases/shared templates | Split integrity | Medium | High | Generic/manual near-duplicate review | Independent second leakage reviewer and preregistered thresholds | Future holdout independence | P0 |
| R15 | Severities, confidence, scores, synergies, and risk bands are uncalibrated | Risk model | High | High for operational claims | Deterministic/versioned/documented | Threat/cost rationale, sensitivity/calibration on development before freeze | Defending design choices | P0/P1 |
| R16 | Findings materialized before retention permit intermediate CPU/memory load | Resource security | Medium | High | Input/node/text bounds and fixed regex | Worst-case adversarial profiling/tests; bounded incremental design | Security-boundary correctness | P1 |
| R17 | `--redact` is mistaken for complete report sanitization | Privacy/usability | Medium-high | High with real data | README says evidence-only | Rename/clarify mode; metadata-minimized export; privacy tests | Future real data | P1 |
| R18 | JSON/SARIF/CSV consumers render hostile strings unsafely | Output supply chain | Medium | Medium-high | JSON encoding, CSV neutralization, bounded evidence | Consumer guidance/tests and retention policy | Operational integration | P1 |
| R19 | Source/baseline/report paths leak private filesystem information | Privacy | Medium | Medium | Research invocation normalizes paths | Portable/minimized source identifiers for sharable output | Research artifact sharing | P1 |
| R20 | Baseline is altered or rolled back with catalog | Integrity/provenance | Medium | High | Strict bounded load; duplicate names rejected | Signed/approved baseline envelope, trusted storage, anti-rollback | Drift claim validity | P1 |
| R21 | No exact dependency lock prevents exact rebuild | Reproducibility/supply chain | High over time | High | Major-bounded runtime; artifact versions; clean snapshot | Reviewed constraints/lock and offline/archive policy | Formal experiment reproducibility | P1 |
| R22 | CRLF checkout changes reviewer/corpus identities | Reproducibility/integrity | High on default Windows Git | High | LF-safe recovery instructions; three evidence files `-text` | Versioned `.gitattributes`/hash policy hardening | Recovery and future freeze | P1 |
| R23 | Day 6 knowledge files remain untracked | Preservation | High until action | Critical if laptop lost | Local hashes and recovery warning | Reviewed documentation checkpoint plus independent archive | Student continuity | P0 |
| R24 | H1, ablations, Day 3D/4A/4B/4C support files are ignored/local-only | Preservation | High until action | High if cited | Inventory and some hashes exist locally | Checksummed supplementary archive policy | Thesis evidence traceability | P0/P1 |
| R25 | v0.3 artifact's dirty source cannot be reconstructed from commit | Reproducibility/research status | Certain historical fact | High for confirmation | Dirty flag, exact artifact/config/rules preserved | Never upgrade status; future run from clean freeze on fresh data | v0.3 claim boundary | Historical |
| R26 | Unkeyed hashes/internal checks are mistaken for authenticity | Integrity/provenance | Medium | High | Git and external digest documentation | Signed tag/release/archive or independently held manifest | Evidence trust | P1 |
| R27 | Future risk/schema changes break or reinterpret 3.0 artifacts | Historical compatibility | Medium over time | High | Real historical fixtures/tests and schema checks | Versioned historical semantic registry/migrations | Preservation of H0 | P1 |
| R28 | Millisecond timing is generalized across machines/workloads | Conclusion validity | Medium-high | Medium-high | Environment/boundary metadata and warnings | Cross-machine controlled benchmark only if research requires it | Performance claim | P1/P2 |
| R29 | Malicious loopback process attacks retrieval availability/parser | Network/input security | Medium | Medium-high | DNS pinning, no redirects/proxies, timeout/byte/page/tool limits | Continue adversarial transport tests; keep opt-in | Static-boundary defense | P1 |
| R30 | MCP specification evolution changes field semantics | Technical/construct drift | High over FYP timeline | Medium-high | Unknown fields preserved; spec target documented | Pin/review spec revision before protocol; version semantics | Future relevance | P1 |
| R31 | Suppressions hide genuine findings or are used post-hoc | Governance/research integrity | Medium | High | Known IDs, exact scope, justification, config identity | Approval/expiry policy; none in confirmatory primary | Result integrity | P0 protocol/P1 product |
| R32 | Custom literal rules create false confidence or policy drift | Configuration | Medium | Medium | Data-only, bounded, collision checked, hashed | Rule ownership/version/review and benign tests | Reproducible organization policy | P1 |
| R33 | Current artifact comparison warnings are ignored | Research interpretation | Medium | High | Explicit compatibility enum/warnings | Fail-closed modes for formal workflows and reporting checklist | Prevents false paired claims | P1 |
| R34 | Public label “security scanner” implies production assurance | Communication | High | High | Alpha/research limitations documented | Use precise “bounded static metadata inspector” wording | Viva/release ethics | P0 communication |
| R35 | Real-world collection exposes secrets, PII, license, or vulnerable operators | Ethics/privacy/legal | Medium if future data added | Critical | Current corpora synthetic; no remote collection | Approval, minimization, lawful sourcing, access/retention/disclosure protocol | Future formal dataset | P0 before collection |

## 28. GO / NO-GO assessment

| Decision | Verdict | Rationale |
|---|---|---|
| Preserve the engineering prototype as `v0.3.0a1` | **GO** | It is a meaningful alpha checkpoint with strong safety/reproducibility engineering and honest limitations. Preservation does not imply deployment readiness. |
| Use it as a pre-FYP prototype/pilot foundation | **GO** | It supplies architecture, a negative confirmatory pilot, failure hypotheses, teaching material, and a concrete future study design. |
| Use current evidence for a final FYP effectiveness/generalization conclusion | **NO-GO** | v0.3 lacks untouched evidence; H0 shows weak effectiveness; construct/sample/statistical limitations are material. |
| Begin a future supervisor-approved confirmatory study immediately | **NO-GO—NOT YET** | First resolve P0 construct, budget semantics, statistical/data/review protocol, preservation, and clean freeze gates. |
| Use the alpha as a standalone production security control | **NO-GO** | H0 performance, adaptive bypasses, output-budget defect, uncalibrated risk, and static-only scope make that unsafe. |

### What must happen first

1. Supervisor approves one precise research question and target construct.
2. Resolve and test finding-budget versus decision semantics before selecting the
   candidate.
3. Select one candidate and freeze rule IDs, severities, threshold, risk,
   dependencies, canonicalization, artifact schema, and configuration before
   future holdout access.
4. Predefine one primary estimand/decision criterion, sample size, uncertainty,
   matched/cluster treatment, multiplicity, and practical recall/FPR targets.
5. Approve independent data authorship/source, licensing/ethics, prevalence,
   languages, categories, leakage controls, and reviewer qualifications/count.
6. Create, review, hash, and gate a genuinely untouched holdout without exposing
   it to detector maintainers.
7. Run release/security quality gates from a clean reproducible checkpoint.
8. Execute one preregistered primary evaluation under a documented retry policy.

## 29. Remaining priorities

### P0 — before formal confirmation or leaving the project unattended

1. **Preserve the Day 6 set.** Independently back up and later review/checkpoint
   the technical map, manual, handover, disaster-recovery guide, recovery
   manifest, and this adversarial review. Add this document's hash to the
   independent archive inventory without rewriting historical manifests in
   place.
2. **Preserve selected local evidence.** Decide whether H1, seven H0 ablations,
   Day 3D, Day 4A, and Day 4C supporting files will be cited; if yes, create a
   reviewed checksummed supplementary archive.
3. **Refine the construct.** Separate agent-influence poisoning, sensitive-data
   behavior, declaration mismatch, obfuscation, malformed schema, and disclosed
   capability as supervisor-approved outcomes.
4. **Resolve finding-budget decision coupling.** Risk, `--fail-on`, terminal
   affected counts, and evaluation predictions must not silently become benign
   solely because output capacity was exhausted. Add regression/adversarial
   tests before any candidate freeze.
5. **Approve statistical method.** Define primary estimand, practical success
   threshold, N/precision/power, dependence handling, prevalence interpretation,
   and multiplicity.
6. **Approve data and review plan.** Use genuinely untouched sources/authors,
   explicit leakage rules, adequate reviewer qualifications/count, abstention,
   adjudication, license, and ethics.
7. **Freeze cleanly.** One candidate, clean commit, exact versions/configuration,
   no custom rules/suppressions unless preregistered, full quality gates, and a
   one-run/retry protocol.

### P1 — before stronger engineering or operational claims

- prove worst-case intermediate finding CPU/memory behavior;
- adopt a reviewed constraints/lock/environment snapshot strategy;
- harden line-ending behavior for research inputs or track the checkout policy
  in versioned documentation;
- define metadata-minimized reporting and report retention/access controls;
- protect baseline approval/provenance and consider anti-rollback/signing;
- strengthen historical risk/schema migration semantics;
- add independent realistic benign/suspicious development material;
- improve multilingual/adaptive bypass testing if in scope;
- add a second independent leakage/review perspective;
- pin or periodically audit CI actions/build tooling;
- verify live remote/tag/release assets and preserve distributable hashes; and
- correct the two known Day 6 documentation issues in a later authorized docs
  change: stale Day 6A release status and missing `--baseline` in one map command.

### P2 — optional, scope-controlled future work

- controlled cross-machine and maximum-size performance studies;
- macOS testing only if support is claimed;
- longitudinal real catalog drift study;
- signed release/SBOM/provenance work;
- multilingual expansion;
- separately scoped LLM/learned/hybrid comparison;
- additional MCP primitives or host integrations;
- richer reporting/dashboards; and
- broader real-world ecosystem sampling after ethics/license approval.

## 30. Final preservation and mutation statement

Day 6E created only `docs/final-adversarial-review.md`. It did not edit any
existing documentation or any path under `src/`, `tests/`, `rules/`, or
`evaluation/`. The review used source inspection and already preserved
artifacts; it did not create predictions.

**THE EXPOSED HOLDOUT WAS NOT RERUN.**

**NO DETECTOR TUNING WAS PERFORMED.**

**NO FRESH CONFIRMATORY EXPERIMENT WAS CREATED.**

**NO DETECTOR, CORPUS, LABEL, THRESHOLD, RISK MODEL, OR FROZEN RESEARCH
EVIDENCE WAS MODIFIED DURING DAY 6E.**
