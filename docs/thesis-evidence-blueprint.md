# Thesis Evidence, Table and Figure Blueprint

> **Day 6L status:** evidence-mapping/design document grounded at Git commit
> `a93e016203c9877d2cf59df859821d3a590b2c3a`. It is not a final thesis and
> creates no new scientific evidence. Faculty structure, title, construct,
> research questions and formal methodology remain subject to supervisor approval.

## 1. Scientific status taxonomy and visual labels

Every thesis claim, table, figure and metric must use exactly one primary status.

| Code | Caption label | Status | Meaning | Permitted role |
|---|---|---|---|---|
| A | **[DEVELOPMENT]** | Development evidence | Visible data used for regression, debugging or design | Engineering feedback and in-sample behavior; never generalization |
| B | **[PILOT H0]** | Pilot confirmatory evidence | Frozen v0.2 configuration evaluated once on the independently reviewed pilot holdout | Authoritative first pilot result and uncertainty, not final FYP/deployment performance |
| C | **[EXPLORATORY—POST-UNBLINDING]** | Post-unblinding exploratory evidence | Analysis or detector results influenced by exposed H0 failures | Hypothesis/mechanism generation; never confirmation or superiority |
| D | **[ENGINEERING]** | Implementation/engineering evidence | Source, tests, security boundaries, build and deterministic behavior | Claims about this implementation, not detection effectiveness |
| E | **[HUMAN REVIEW]** | Review/annotation evidence | Blinded reviewer judgments, agreement and adjudication | Label consistency/ambiguity evidence, not detector validity |
| F | **[FUTURE FORMAL—NOT YET AVAILABLE]** | Future formal-FYP evidence | Supervisor-approved evidence that has not been produced | Placeholders only; no numbers or conclusions |

Captions must begin or end with the label. If one asset combines statuses, use
separate panels/rows and label each; never use a vague umbrella such as “evaluation
results.” Suggested styling when figures are eventually generated: blue=A,
dark navy=B, amber/dashed=C, grey=D, purple=E, empty outline/hatching=F. Colour
must never be the only status cue.

> **DO NOT CROSS THESE SCIENTIFIC BOUNDARIES**
>
> Development ≠ generalization. Pilot ≠ final FYP. Exploratory ≠ confirmatory.
> Hash integrity ≠ safety/authenticity. Reviewer agreement ≠ detector validity.
> Reproducibility ≠ independent replication. A static finding ≠ malicious intent.
> A balanced test set ≠ deployment prevalence. Low measured latency ≠ production
> readiness. A rule-family ablation ≠ universal causal importance.

## 2. Thesis chapter evidence map

The seven-chapter structure is a working blueprint; replace it if faculty guidance
requires another format.

| Chapter | Purpose | Evidence needed/current repository material | Missing / must wait | Overclaim to avoid |
|---|---|---|---|---|
| 1 — Introduction | Define problem, motivation, scope, questions and contributions | Project scope in README/SECURITY; pilot motivation and honest status in `research-status.md`, proposal seed and handover | Approved title, construct, RQs/objectives, current adoption/security literature | “MCP tools are generally malicious” or “the detector solves MCP security” |
| 2 — Literature Review | Establish concepts, prior work, gap and evaluation norms | `fyp-literature-workbook.md` supplies topics/search plans, not citations | Verified primary/peer-reviewed sources; defensible novelty/gap | Calling any contribution novel or state of the art without review |
| 3 — Methodology | Define construct, threat model, data, review, freeze, metrics and analysis | Pilot protocol, holdout plan, corpus manifests, review ledger, evaluator, formal blueprint | Supervisor-approved formal protocol, sample-size/statistical plan, ethics, new holdout/review/preregistration | Presenting pilot procedures as already approved formal FYP methodology |
| 4 — System Design / Implementation | Explain inert bounded architecture, rules, risk, identity, reporting and known defect | `src/`, tests, Captain map/manual, research code walkthrough, adversarial review | P0 decision/retention remediation and frozen formal candidate | Depicting future corrected architecture as implemented |
| 5 — Results | Report observations by status with counts, intervals and provenance | Development matrix, H0 artifact, reviewer record, timing, ablations, Day 3C, Day 4C exploratory artifact | Future formal artifact and approved comparisons | Mixing A/B/C or calling pilot/exploratory numbers final performance |
| 6 — Discussion | Interpret transfer gap, errors, validity, engineering value and limitations | Day 3C, adversarial review, handover, formal blueprint, preserved artifacts | Literature-backed comparison and future formal evidence | Generalizing beyond sampled synthetic/English/balanced data |
| 7 — Conclusion / Future Work | Answer approved RQs at supported scope and state next work | Current pilot conclusions and formal backlog | Formal results, supervisor decisions and completed P0 gates | Production readiness, comprehensive attack coverage or validated v0.3 improvement |

## 3. Claim-to-evidence traceability matrix

`Formal action` uses **No** only when the claim is already a factual statement
about this repository/evidence. All general effectiveness/novelty claims require
future action and/or literature.

| ID | Candidate claim | Status | Required evidence and exact source | Metric / derivation | Table / figure | Safe wording | Forbidden wording | Formal action? |
|---|---|---|---|---|---|---|---|---|
| C01 | Scanner is static and does not invoke scanned tools | D | `SECURITY.md`; `loader.py`, `scanner.py`, retrieval tests | source/test invariant | T01, F01 | “Static scan paths treat metadata as inert data.” | “The whole system performs no I/O.” | No |
| C02 | Hostile input is bounded and strictly parsed | D | `resource_policy.py`, loader/strict-JSON tests | byte/depth/node/string/tool limits | T04, F02 | “The implementation enforces documented parsing/resource bounds.” | “Resource exhaustion is impossible.” | No |
| C03 | Analysis is deterministic for fixed supported input/config | D | normalizer, registry, scanner, risk, canonicalizer tests | stable ordering/hashes | T04, F03 | “Deterministic invariants are implemented and regression tested.” | “Outputs are identical on every future platform/version.” | No |
| C04 | Seven built-in families expose 16 stable rule IDs in v0.3 | D | detector registry; `rules/builtin.py`; rule tests | identity/count | T05, F04 | “Current rule pack contains seven families and 16 IDs.” | “Sixteen validated attack types are detected.” | No |
| C05 | Custom rules remain data-only and suppressions are explicit | D | rules/suppression loaders and tests | validation/collision/scope behavior | T06 | “Operator policy is bounded, literal and identity-recorded.” | “Custom rules cannot be misconfigured.” | No |
| C06 | Fingerprints support metadata identity/drift comparison | D | canonicalizer, fingerprint, baseline, compare and tests | SHA-256 component/full identities | T07, F05 | “Hashes support change comparison against an approved baseline.” | “A matching hash proves safety or authenticity.” | No |
| C07 | Terminal/CSV/JSON/SARIF output has inert-handling controls | D | `reporter.py`, `test_reporter.py` | escaping/formula/truncation tests | T08 | “Output controls reduce identified rendering risks.” | “All downstream consumers are safe.” | No |
| C08 | Development corpus contains 80 balanced samples | A | `evaluation/corpus/manifest.json`, corpus hash | 40 benign + 40 suspicious | T09 | “The visible development corpus is balanced 40/40.” | “It represents deployment prevalence.” | No |
| C09 | Current development regression matrix is 37/36/4/3 | A | `evaluation/runs/day4c/development-full.json`; README; evaluation regression test | matrix/standard metrics | T10, F08 | “On visible development data, observed accuracy was 91.25%.” | “Detector accuracy is 91.25%.” | No |
| C10 | Development recall/FPR were 92.50%/10.00% | A | same artifact/test | 37/40; 4/40 | T10, F08 | “Development-regression recall/FPR were…” | “Expected real-world recall/FPR are…” | No |
| C11 | Pilot holdout contains 48 balanced samples | B | holdout manifest/coverage report; corpus hash | 24/24 | T09 | “The pilot holdout was balanced and synthetic/derived.” | “The holdout models natural prevalence.” | No |
| C12 | Frozen H0 matrix is 5/18/6/19 | B | authoritative H0 JSON SHA `3307…` | raw matrix | T11, F09 | “The frozen pilot H0 produced…” | “Final detector performance is…” | No |
| C13 | H0 recall was 20.83% with substantial uncertainty | B | H0 metrics/uncertainty | 5/24; Wilson 95% 9.24–40.47% | T12, F10 | “Observed pilot recall was 20.83% (Wilson 95% CI 9.24–40.47%).” | “Recall is exactly 20.83% generally.” | No |
| C14 | H0 FPR was 25.00% | B | H0 metrics/uncertainty | 6/24; Wilson 95% 12.00–44.90% | T12, F10 | “Observed pilot FPR was 25.00%…” | “One quarter of all alerts are false.” | No |
| C15 | Development-to-H0 point estimates collapsed | A+B, separately labelled | development and H0 artifacts | recall −71.67 points; accuracy −43.33 points (descriptive) | T13, F08 | “Point estimates were substantially lower on the pilot holdout.” | “The exact gap proves universal overfitting.” | No |
| C16 | H0 had 19 false negatives | B | H0 sample records; Day 3C | count and failure types | T14, F11 | “Nineteen of 24 suspicious pilot samples were missed.” | “The same attacks will always be missed.” | No |
| C17 | H0 had six false positives | B | H0 sample records; Day 3C | 6/24 benign | T15, F11 | “Six benign pilot samples crossed the threshold.” | “Operational alert burden is exactly 25%.” | No |
| C18 | Post-hoc failure taxonomy explains observed H0 errors | C (descriptive) | `day3c-deep-failure-analysis.md` SHA `deb97…` | taxonomy counts from frozen samples | T14/T15, F11 | “Post-unblinding analysis categorized observed failures…” | “The taxonomy was preregistered or complete.” | No |
| C19 | H0 analysis-core timing was low on recorded host | B | H0 primary artifact | mean 1.716, median 1.535, p95 3.223 ms/tool | T17, F12 | “On the recorded Windows environment…” | “The detector is universally real-time.” | No |
| C20 | H0 static-end-to-end timing includes loading/normalization | B | `exp-…060157…cde99024.json` | mean 4.302, median 4.073, p95 6.310 ms/tool | T17, F12 | “The preserved secondary boundary measured…” | “End-to-end deployment latency is guaranteed.” | No |
| C21 | One blinded reviewer agreed on 47/48 labels | E | reviewer source SHA `857b…`; review ledger | 97.9167% agreement | T18, F13 | “One reviewer showed high binary agreement with frozen labels.” | “Labels were independently proven correct.” | No |
| C22 | Reviewer kappa was approximately 0.9583 | E | review ledger arithmetic | `(Po−Pe)/(1−Pe)` | T18, F13 | “Agreement beyond chance was high for these marginals.” | “Labels are 95.83% accurate.” | No |
| C23 | Difficulty labels had weak exact agreement | E | review ledger | 16/48 = 33.33% | T18, F13 | “Difficulty was subjective and unstable.” | “Difficulty strata are objective ground truth.” | No |
| C24 | R08 exposes construct ambiguity | E+B | review ledger, coverage report, Day 3C | one binary disagreement | T18 | “Malformed schema was retained under the frozen security-review construct.” | “Reviewer was wrong” or “malformed means malicious.” | No |
| C25 | v0.3 exposed-holdout matrix is 11/18/6/13 | C | Day 4C primary SHA `d5d84…` | raw matrix/metrics | T20, F14 | “Post-unblinding exploratory analysis produced…” | “v0.3 validated improvement.” | No |
| C26 | v0.3 recall/F1 point estimates exceeded H0 on exposed data | C | H0 + Day 4C | +25.00/+25.09 percentage points | T20, F14 | “Point estimates increased on the same exposed corpus.” | “v0.3 generalizes better.” | No |
| C27 | v0.3 did not reduce the six historical FPs | C | Day 4C matrix/sample records | FP stayed 6; FPR stayed 25% | T20, F14 | “All six binary false positives remained in aggregate.” | “v0.3 solved false positives.” | No |
| C28 | OBF-005 safely recognizes bounded depth-one representations | D+A/C diagnostic | representations source/tests; exploratory fixtures | bounds/test outcomes; not holdout recovery claim | T05, F04 | “Bounded recognition is implemented and mechanism-tested.” | “It detects obfuscation generally.” | No |
| C29 | Family ablations reveal corpus-specific contribution patterns | B secondary | seven `exp-*` ablation artifacts | matrix deltas versus H0 | T16, F15 | “Removing family X changed outcomes on this pilot corpus.” | “Family X causes real-world detection.” | No |
| C30 | Historical artifacts were unaffected by retention truncation | B+C | H0/Day4C artifacts; adversarial review | H0 16 findings; v0.3 24; max 2/sample; far below 64/2,048/8,192 caps | T21 | “No preserved sample/result reached retention limits.” | “The P0 defect cannot matter.” | No |
| C31 | Current finding budget can alter semantic decisions after exhaustion | D limitation | scanner/risk/CLI/evaluator source; adversarial review | code-path trace, not H0 effect | T21, F06/F07 | “Presentation retention is currently coupled to decisions.” | “H0 was invalidated by truncation.” | Yes—fix before formal freeze |
| C32 | Clean-room engineering recovery succeeds on one Windows setup | D | Day 6K report | 472 tests, 92.95%, build/smoke | T22, F16 | “Day 6K reproduced installation/tests/build on Windows.” | “The study is independently replicated.” | No |
| C33 | Frozen evidence identities can be recovered | D | recovery manifest, Day 6K hashes/tag | exact SHA/corpus/config identities | T22, F17 | “Recorded files matched expected identities.” | “Hashes prove authenticity/safety.” | No |
| C34 | Current evidence does not establish v0.3 generalization | C/F | research status, artifacts, exposure chronology | absence of untouched evaluation | T23, F18 | “Fresh independent confirmation remains future work.” | “The lack of proof means v0.3 is ineffective.” | Yes |
| C35 | Formal effectiveness is not yet known | F | formal blueprint/proposal | blank future matrix/CIs | T24, F19 | “Formal-FYP effectiveness evidence is not yet available.” | Any fabricated expected result | Yes |
| C36 | Prototype is not production-ready as a standalone control | B+D limitation | H0, static scope, P0, adversarial review | low recall/FPR + residual risks | T23 | “Current evidence does not support production assurance.” | “The scanner secures MCP deployments.” | Yes if future claim desired |

## 4. Verified current pilot evidence inventory

| Evidence block | Status | N / matrix | Metrics | Authoritative source |
|---|---|---|---|---|
| Development regression | A | N=80; TP37 TN36 FP4 FN3 | accuracy 91.25%; precision 90.24%; recall 92.50%; F1 91.36%; FPR 10.00% | `evaluation/runs/day4c/development-full.json`, README, regression test |
| Frozen v0.2 H0 | B | N=48; TP5 TN18 FP6 FN19 | accuracy 47.92%; precision 45.45%; recall 20.83%; F1 28.57%; FPR 25.00% | `evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json` |
| Human review | E | N=48; 47 agreements, 1 disagreement, 0 abstentions | raw 97.9167%; κ≈0.9583; difficulty exact 16/48 | reviewer source/ledger |
| v0.3 exposed exploratory | C | N=48; TP11 TN18 FP6 FN13 | accuracy 60.42%; precision 64.71%; recall 45.83%; F1 53.66%; FPR 25.00% | Day 4C primary artifact |

### Preserved H0 timing

| Boundary | Warm-ups / measured repetitions | Observations | Mean | Median | P95 | Status |
|---|---:|---:|---:|---:|---:|---|
| Analysis-core | 3 / 10 | 480 | 1.716 ms/tool | 1.535 ms/tool | 3.223 ms/tool | B — primary timing |
| Static-end-to-end | 1 / 5 | 240 | 4.302 ms/tool | 4.073 ms/tool | 6.310 ms/tool | B — secondary timing |

Both boundaries were recorded on Windows/Python 3.12.13 and are sensitive to
hardware, runtime and background load. They are not universal latency guarantees.

## 5. Table blueprint

`Populatable` means values can be derived now without new detector execution.

| ID / priority | Title; purpose / chapter | Status | Rows/columns and source/calculation | Populatable / formal placeholder | Safe interpretation / avoid |
|---|---|---|---|---|---|
| T01 P0 | System scope and non-goals; Ch1/4 | D | assets, inputs, outputs, exclusions; SECURITY/README/source | yes / no | Defines bounded scope; avoid claiming full MCP protection |
| T02 P0 | Threat model and trust boundaries; Ch3 | D + future approval | actor, asset, boundary, threat, mitigation, residual; blueprint/source | partial / approved construct pending | Explains assumed attacker/data; avoid implying runtime-behavior coverage |
| T03 P0 | Construct taxonomy; Ch3 | D + F | construct, core/support/warning/out-of-scope, operational definition; formal blueprint | partial / supervisor decision | Separates poisoning-like signals from quality warnings; avoid malicious-intent equivalence |
| T04 P1 | Hostile-input/resource controls; Ch4 | D | layer, limit, enforcement, failure, test; resource policy/tests | yes / no | Documents enforced bounds; avoid “DoS impossible” |
| T05 P0 | Built-in rules/families; Ch4 | D | 16 IDs, family, mechanism, severity, limitation; detectors/registry | yes / no | Describes implementation; avoid validated-attack taxonomy claim |
| T06 P1 | Configuration/custom rules/suppressions; Ch3/4 | D | field, validation, identity, scope, risk; loaders/tests | yes / future governance | Data-only design; avoid assuming safe operator choices |
| T07 P1 | Fingerprint/baseline/drift semantics; Ch4 | D | identity type, included data, interpretation, test | yes / no | Change detection; avoid authenticity/safety inference |
| T08 P1 | Output/report security controls; Ch4 | D | format, escaping/redaction/truncation, residual risk | yes / no | Mitigations in this implementation; avoid downstream-consumer assurance |
| T09 P0 | Dataset composition and exposure; Ch3/5 | A+B+C | split, N, class balance, provenance, status, hash; manifests | yes / fresh formal row blank | Makes split/exposure explicit; avoid prevalence claims |
| T10 P1 | Development confusion matrix/metrics; Ch5 | A | 2×2 counts + metric table; development artifact | yes / no | Regression behavior only; avoid headline detector accuracy |
| T11 P0 | Frozen pilot H0 confusion matrix; Ch5 | B | actual/predicted 2×2; H0 artifact | yes / no | Primary pilot counts; avoid final-FYP label |
| T12 P0 | H0 metrics and Wilson intervals; Ch5 | B | metric, numerator/denominator, %, 95% CI; H0 | yes / no | Observed pilot estimates with uncertainty; avoid exact/general rates |
| T13 P0 | Development vs H0 point estimates; Ch5/6 | A+B separated | accuracy/precision/recall/F1/FPR and percentage-point difference | yes / no | Descriptive transfer gap; avoid formal paired significance/causality |
| T14 P0 | False-negative taxonomy; Ch5/6 | C descriptive | mechanism, count, field, difficulty caveat, rule/finding state; Day 3C/H0 | yes / future taxonomy preregistration | Explains pilot misses post hoc; avoid exhaustive taxonomy |
| T15 P0 | False-positive taxonomy; Ch5/6 | C descriptive | sample class, mechanism/rule, count, construct ambiguity; Day 3C | yes / future taxonomy preregistration | Describes observed collisions; avoid deployment burden estimate |
| T16 P1 | Seven H0 family ablations; Ch5/6 | B secondary | preset, removed family, TP/TN/FP/FN, recall/FPR delta; seven artifacts | yes / future approved ablations | Corpus-specific contribution; avoid universal causal importance |
| T17 P0 | H0 latency summary; Ch5 | B | boundary, environment, warm-ups/reps, N observations, mean/median/p95 | yes / future benchmark row blank | Measured host performance; avoid universal lightweight claim |
| T18 P0 | Independent-review method/agreement; Ch3/5 | E | blinding, N, margins, agreement/kappa, R08, difficulty | yes / formal reviewer row blank | Consistency/ambiguity; avoid detector or truth validation |
| T19 P1 | H0 uncertainty/strata evidence; Ch5 | B | category/field/difficulty, denominator, estimate, low-evidence flag | partial now / formal required | Descriptive small strata; avoid ranking tiny groups confidently |
| T20 P0 | H0 vs v0.3 exposed exploratory; Ch5/6 | B+C visibly separated | matrices/metrics, status, config, exposure, deltas | yes / no | Diagnostic change on exposed data; avoid superiority/generalization |
| T21 P0 | Finding-budget P0 and artifact impact; Ch4/6 | D limitation + B/C audit | current coupling, cap, artifact finding totals/max, historical impact | yes / remediation proof future | Defect exists but artifacts below caps; avoid hiding or invalidating H0 |
| T22 P1 | Reproducibility evidence; Ch3/6/appx | D | clone/install/Ruff/mypy/472 tests/coverage/build/smoke/hashes/tag/config | yes / formal snapshot later | Engineering/evidence recovery; avoid independent replication claim |
| T23 P0 | Threats to validity; Ch6 | mixed | threat, category, current mitigation, remaining risk, formal mitigation | yes / update after formal study | Makes limitations auditable; avoid checklist-as-proof |
| T24 P0 | Future formal results template; Ch5 | F | N/distribution/matrix/metrics/CIs/runtime approved comparisons—all blank | no / **TO BE POPULATED ONLY AFTER APPROVED RUN** | Prevents fabrication; avoid filling from pilot/exposed data |

Recommended final thesis selection: roughly 12–16 main-body tables, moving detailed
rule, ablation, provenance and error records to appendices. Do not use all 24 merely
because they are available.

## 6. Figure blueprint

No figure image or plotting script is created during Day 6L.

| ID / priority | Title / type / chapter | Status and source | Axes/grouping/annotations | Caption message; allowed / forbidden interpretation | Current/future |
|---|---|---|---|---|---|
| F01 P0 | MCP metadata inspection context; component diagram; Ch1/4 | D; README/source | no axes; host/client/server/tool/inspector/operator; static boundary | Inspector examines definitions without tool invocation; not full MCP runtime security | current |
| F02 P0 | Trust boundaries/threat model; data-flow diagram; Ch3 | D+F; source/formal blueprint | metadata/config/baseline/report boundaries; mark optional loopback | Shows hostile inputs and trusted decisions; not a sandbox guarantee | partial/future approval |
| F03 P0 | Actual scan pipeline; flow diagram; Ch4 | D; loader→normalizer→scanner→reporter | annotate validation, suppression, retention and current coupling | Source-grounded current architecture; not future corrected state | current |
| F04 P1 | Rule taxonomy; hierarchy/radial map; Ch4 | D; registry/rules | seven families → 16 IDs; colour by signal type, not performance | Implementation organization; not validated attack coverage | current |
| F05 P1 | Fingerprint/baseline/drift flow; process diagram; Ch4 | D | canonical tool → component hashes → baseline → drift | Supports integrity comparison; not proof of safety/intent | current |
| F06 P0 | Current finding-budget coupling; causal flow; Ch4/6 | D limitation | detection → retention → risk/fail-on/evaluation; warning edge | Explains known defect; does not imply historical truncation | current |
| F07 P0 | Future corrected decision architecture; design diagram; Ch4/future | F | detection summary → decision; separate presentation reservoir | Proposed target only; must say NOT IMPLEMENTED | future |
| F08 P0 | Development vs pilot metrics; grouped dot/bar chart; Ch5 | A+B | x=metric; y=%; groups `[DEVELOPMENT]`, `[PILOT H0]`; N labels | Point estimates differ sharply; not statistical proof of universal overfit | current |
| F09 P0 | H0 confusion matrix; annotated heatmap; Ch5 | B; H0 | x=predicted, y=ground truth; raw counts + row % | Pilot N=48 matrix; not deployment prevalence | current |
| F10 P0 | H0 estimates with Wilson intervals; forest/dot plot; Ch5 | B | x=%; rows accuracy/recall/FPR; 95% CI and denominators | Uncertainty is substantial; do not show F1 CI unless approved/calculated | current |
| F11 P0 | H0 failure mechanisms; horizontal bars or alluvial; Ch5/6 | C descriptive; Day 3C | x=count; y=taxonomy; FN/FP panels, fields annotated | Post-hoc descriptive taxonomy; not preregistered prevalence | current |
| F12 P1 | H0 latency by boundary; interval/dot summary; Ch5 | B | x=milliseconds; groups core/end-to-end; mean/median/p95, reps | Recorded host/boundary timing; no cross-machine universal claim | current |
| F13 P1 | Reviewer agreement; 2×2 matrix + difficulty inset; Ch5 | E | binary cross-tab; difficulty 3×3; N/κ annotation | High binary, low difficulty agreement; not detector validation | current |
| F14 P0 | v0.2 H0 vs v0.3 exposed exploratory; paired metric dots; Ch5/6 | B+C | x=metric; y=%; v0.3 amber/dashed; exposure warning box | Exploratory point-estimate change only; not validated improvement | current optional |
| F15 P1 | H0 family ablations; delta plot; Ch5/6 | B secondary | x=recall/FPR delta; y=removed family; raw matrices linked | Corpus-specific sensitivity; not universal causation | current optional |
| F16 P1 | Clean-room reproducibility levels; staircase; Ch3/6 | D; Day 6K | levels 1–5; pass/qualified/not-yet | Levels 1–4 verified/qualified; Level 5 absent | current |
| F17 P0 | Evidence provenance chain; directed lineage; Ch3/appx | mixed | corpus→manifest→review→config→artifact→hash→metric→asset→claim | Shows traceability and human decisions; not truth/authenticity proof | current |
| F18 P0 | Research chronology/status; timeline; Ch1/6 | mixed | v0.2 freeze/H0/analysis/v0.3/release/Day6/future; status labels | Prevents confirmatory/exploratory mixing | current |
| F19 P0 | Future formal evaluation pipeline; gated flow; Ch3 | F | approval→P0→freeze→untouched review→preregister→one run→preserve→analyze | Design only; no formal result exists | future |
| F20 P1 | Threats-to-validity map; layered diagram; Ch6 | mixed/F | construct/internal/external/conclusion/reproducibility layers | Visual index to T23; not mitigation-completeness proof | current + future update |

Recommended main-body visual set: 8–12 figures. P0 candidates are F01/F02/F03,
F08–F11, F17–F19; use F06/F07 if the P0 remains central to implementation.

## 7. Results chapter blueprint

| Section | Report now / cannot report | Required assets | Statistics | Safe conclusion |
|---|---|---|---|---|
| 5.1 Dataset/evaluation identity | Current corpus names/versions/hashes, splits, N and exposure; not future sample details | T09, F18 | counts/proportions | Readers can distinguish development, pilot and exploratory evidence. |
| 5.2 Development regression | 37/36/4/3 and metrics labelled A; not generalization | T10, optional F08 panel | counts, rates, existing Wilson if used with A label | Rules behave strongly on visible regression data. |
| 5.3 Pilot H0 primary result | H0 matrix, metrics, Wilson accuracy/recall/FPR | T11/T12, F09/F10 | raw counts, denominators, N=48, 95% Wilson | Frozen configuration transferred poorly on this pilot sample, especially recall. |
| 5.4 Pilot error analysis | 19 FN, 6 FP, redacted taxonomy, fields/rules; post-hoc label | T14/T15, F11 | counts and denominators; small strata flagged | Failures reveal construct/mechanism gaps and benign collisions in this corpus. |
| 5.5 Pilot ablations | Seven secondary matrices/deltas; not causal universality | T16, F15 | raw counts and descriptive deltas | Some family removals changed this pilot configuration's outcomes. |
| 5.6 Runtime | Two H0 boundaries and full protocol/environment | T17, F12 | mean, median, p95, observations, warmups/reps | Static analysis was fast on the recorded host; portability is untested. |
| 5.7 Human review | Blinding, 47/48, κ, R08, 16/48 difficulty | T18, F13 | cross-tabs, agreement and kappa | Binary consistency was high; difficulty/construct ambiguity remains. |
| 5.8 v0.3 diagnostic | 11/18/6/13 with prominent C label and exposure chronology | T20, F14 | counts/rates; existing CIs optional but clearly exploratory | Point estimates increased on exposed data while all six FPs remained. |
| 5.9 Formal-FYP result | **Nothing now** | T24/F19 placeholders | approved estimands/CIs only after run | “Evidence not yet available” until supervisor-approved evaluation. |

Do not make v0.3 a continuation of the H0 primary subsection without an explicit
post-unblinding break. If faculty prefers pilot work outside Chapter 5, move 5.2–5.8
to a “Pre-study/Pilot” chapter or appendix by supervisor decision.

## 8. Discussion blueprint

| Theme | Evidence / possible interpretation | Limitation | Literature needed | Future formal evidence |
|---|---|---|---|---|
| Development-to-pilot collapse | A recall 92.50% vs B 20.83%; rules fit visible constructs better than separate pilot constructs | synthetic, authored data; descriptive gap | overfitting/transfer, detector evaluation | untouched candidate evaluation |
| Recall limitation | B 19/24 suspicious missed; 17 with no finding documented in Day 3C | fixed English rules and finite taxonomy | static/signature detection and adversarial adaptation | broader approved corpus/robustness strata |
| False positives | B 6/24 benign; credential/schema vocabulary collisions | balanced synthetic benign set | alert burden, base-rate effects | realistic prevalence/benign metadata |
| Construct ambiguity | R08 and schema/security-quality findings | intent not observable from static metadata | construct validity/tool poisoning definitions | supervisor-approved operational taxonomy |
| Lexical/adaptive bypass | source shows fixed patterns; H0 paraphrase/field failures | no adaptive attacker study | prompt injection/obfuscation robustness | preregistered development robustness + untouched data |
| Synthetic-heavy data | manifests/provenance | ecosystem/vendor noise absent | dataset representativeness | ethical, licensed mixed-source data if approved |
| Balanced 50/50 corpus | N24/24 | precision/accuracy not deployment estimates | prevalence/PR evaluation | justified prevalence or scenario analysis |
| English-only | corpus language | multilingual claims unsupported | multilingual NLP/security studies | only if explicitly in scope and designed |
| One reviewer | E evidence | no panel/consensus; qualifications limited | annotation/reviewer design | two reviewers/adjudicator or approved minimum |
| Difficulty subjectivity | 16/48 exact | subgroup labels unstable | human factors/difficulty operationalization | redefine or keep descriptive only |
| Latency practicality | B medians/p95 on one Windows host | environment-dependent; small static fixtures | benchmarking methodology | frozen multi-boundary protocol/hardware disclosure |
| v0.3 exploratory change | C recall 45.83%, F1 53.66%, same six FP | same exposed holdout shaped rules; dirty provenance | post-selection/confirmatory practice | fresh untouched evaluation after freeze |
| No generalization proof | no F evidence exists | absence does not prove failure | external validity/replication | formal independent result |
| P0 budget coupling | D code trace; artifacts below caps | attacker/order can affect future decisions under exhaustion | resource-safe analysis/design | fixed architecture + invariance/adversarial tests |
| Reproducibility strengths | D clean clone/tests/build/hashes/history | no exact lock/signed authenticity; not replication | reproducible security research | formal environment/lock/evidence freeze |
| Operational readiness | H0 low recall/FPR + static scope + P0 | no user/deployment study | operational detector evaluation | acceptance criteria, realistic data, usability/cost study if in scope |

## 9. Error-analysis presentation standard

Error analysis is **[EXPLORATORY—POST-UNBLINDING] DESCRIPTIVE** unless its taxonomy
and procedure were frozen before a future primary run.

### Required aggregate structure

| Field | Requirement |
|---|---|
| Error identity | Stable sample alias/ID; no unnecessary full payload |
| Binary outcome | FN or FP, expected/predicted and threshold |
| Mechanism family | Predefined or explicitly post-hoc taxonomy label |
| Expected construct | Intent-neutral category and field location |
| Trigger state | Rule IDs/severity, below-threshold finding, or no finding |
| Metadata field | Description/schema/annotation/vendor metadata etc. |
| Difficulty | Report only as original/reviewer values with 16/48 caveat |
| Example | Short abstract/redacted fragment; never credentials or long directives |
| Interpretation | Mechanism hypothesis, not proof of attacker intent |
| Remedy status | Hypothesis/future work; never rewrite H0 prediction |

Use one aggregate FN table and one FP table in the main text; place per-sample
records in an appendix if ethically appropriate. Report all 19/6 counts before
selecting examples. Avoid “representative” examples chosen only to dramatize the
system.

## 10. Confusion-matrix and metric standard

### Layout

```text
                         Predicted suspicious   Predicted benign
Ground-truth suspicious           TP                   FN
Ground-truth benign               FP                   TN
```

Show raw counts in every cell. Row-normalized percentages may appear underneath,
but never replace counts. Use the same axis orientation and colour scale for:

- development `[DEVELOPMENT]`: TP37/FN3; FP4/TN36; N=80;
- H0 `[PILOT H0]`: TP5/FN19; FP6/TN18; N=48;
- v0.3 `[EXPLORATORY—POST-UNBLINDING]`: TP11/FN13; FP6/TN18; N=48;
- formal `[FUTURE FORMAL—NOT YET AVAILABLE]`: blank cells.

### Thesis-wide metric formatting

| Measure | Format |
|---|---|
| Counts | integer with denominator, e.g. `5/24` |
| Accuracy/precision/recall/F1/FPR | two decimal percentage places in prose/tables; retain full precision in extraction data |
| Wilson interval | `estimate% (95% Wilson CI lower%–upper%; numerator/denominator)` |
| N | always in caption/table heading; class denominators where relevant |
| Latency | milliseconds to three decimals; boundary, unit, environment, warmups/repetitions and observations stated |
| Deltas | percentage points (`pp`), never ambiguous “percent improvement” |
| Missing/undefined | em dash plus footnote; never zero unless metric definition returns/means zero and is disclosed |

Existing H0 intervals suitable for current reporting:

- accuracy 47.92% (95% Wilson CI 34.47–61.67%; 23/48);
- recall 20.83% (95% Wilson CI 9.24–40.47%; 5/24);
- FPR 25.00% (95% Wilson CI 12.00–44.90%; 6/24).

Do not invent precision/F1 intervals merely for visual symmetry. Say “observed
recall in this 48-sample pilot…” rather than “recall is 20.83%.” Strata of 3–6
samples require raw counts, a low-evidence flag and restrained descriptive prose.

## 11. Latency, review and ablation plans

### Latency

T17 should disclose Python 3.12.13, Windows 11 record, artifact/config identity,
boundary definitions, N=48, warmups/repetitions and observation count. F12 should
show median and p95 prominently with mean as a secondary marker. Do not connect
the two boundaries as if paired observations were directly comparable without
the protocol. Cross-machine claims require a future frozen benchmark plan.

### Human review

Method table: reviewer count/role, blinding to original labels and detector
predictions, static-only material, allowed abstention, source preservation and
adjudication. Agreement table: 2×2 margins, 47/48, chance agreement 0.5, κ≈0.9583,
R08, and difficulty cross-tab/16/48. F13 may combine binary and difficulty panels.
The evidence supports consistency/ambiguity analysis—not detector performance,
label truth, expert consensus or external validity.

### Ablations

| Removed family | TP/TN/FP/FN | Recall | FPR | Descriptive H0 observation |
|---|---|---:|---:|---|
| Injection | 5/18/6/19 | 20.83% | 25.00% | no binary change |
| Concealment | 5/18/6/19 | 20.83% | 25.00% | no binary change |
| Sensitive data | 5/22/2/19 | 20.83% | 8.33% | four pilot FPs depended on family at threshold |
| Schema | 3/20/4/21 | 12.50% | 16.67% | two TP and two FP contributions removed |
| Mismatch | 4/18/6/20 | 16.67% | 25.00% | one TP contribution removed |
| Obfuscation | 5/18/6/19 | 20.83% | 25.00% | no binary change |
| Capability | 5/18/6/19 | 20.83% | 25.00% | INFO signals remained below MEDIUM |

Each used one measured analysis-core repetition and is secondary/corpus-specific.
Report matrices with deltas; do not rank families as universally important or
claim causality beyond this configuration/sample.

## 12. v0.3 exploratory presentation safeguards

If included, place this box immediately beside T20/F14:

> **POST-UNBLINDING · EXPLORATORY · DIAGNOSTIC · NOT CONFIRMATORY**
>
> The v0.3 rules were designed after H0 failures were inspected and were then
> evaluated descriptively on the same exposed 48-sample holdout. The comparison
> may identify mechanism hypotheses but cannot estimate untouched generalization
> or establish superiority. All six H0 false positives remained.

Permitted sentence: “On the exposed pilot corpus, the v0.3 configuration's
observed recall was 45.83% versus 20.83% for H0, while FPR remained 25.00%.”

Prohibited: “v0.3 improved/validated/generalized/outperformed the detector,”
unless the words explicitly refer only to descriptive point estimates on exposed
data. Never place v0.3 in an unlabeled leaderboard.

## 13. Future formal-FYP placeholders

> **TO BE POPULATED ONLY AFTER SUPERVISOR-APPROVED FORMAL EVALUATION.**

### Formal data/review template

| Field | Future value |
|---|---|
| Corpus name/version/hash | `[NOT YET AVAILABLE]` |
| Frozen detector Git/rule/config identity | `[NOT YET AVAILABLE]` |
| Sample N and provenance | `[NOT YET AVAILABLE—NO SAMPLE SIZE INVENTED]` |
| Label distribution/prevalence rationale | `[NOT YET AVAILABLE]` |
| Reviewer protocol/agreement/adjudication | `[NOT YET AVAILABLE]` |
| Ethics/privacy approval or determination | `[NOT YET AVAILABLE]` |

### Formal result template

| Expected \ predicted | Suspicious | Benign |
|---|---:|---:|
| Suspicious | `[TP]` | `[FN]` |
| Benign | `[FP]` | `[TN]` |

| Metric | Numerator/denominator | Estimate | Approved uncertainty |
|---|---|---|---|
| Accuracy | `[ ]/[ ]` | `[ ]` | `[ ]` |
| Precision | `[ ]/[ ]` | `[ ]` | `[approved method]` |
| Recall | `[ ]/[ ]` | `[ ]` | `[Wilson 95% if preregistered]` |
| F1 | derived | `[ ]` | `[only if method preregistered]` |
| FPR/specificity | `[ ]/[ ]` | `[ ]` | `[Wilson 95% if preregistered]` |
| Runtime | `[boundary; observations]` | `[mean/median/p95]` | environment disclosure |

Approved ablation/comparison and robustness rows remain absent until the
methodology explicitly approves them. Blank is scientifically preferable to a
pilot number presented as future evidence.

## 14. Future comparison plan

| Comparison category | Scientific purpose | Conditions before inclusion | Status |
|---|---|---|---|
| Frozen revised detector vs historical v0.2 H0 | contextual historical baseline | preserve H0; do not imply paired fresh comparison across different exposure/version contexts | candidate secondary |
| Frozen detector vs simple keyword-only baseline | test value beyond minimal lexical matching | define/freeze baseline before unblinding; identical data/threshold outcome definition | candidate primary/secondary by supervisor |
| Full detector vs approved family/rule ablation | contribution analysis | preregister exact set and multiple-comparison interpretation | secondary |
| Full detector vs no-decoding baseline | isolate bounded representation recognition | only if decoding is in approved RQ | secondary |
| Alternative static heuristic baseline | compare design complexity | implement/test/freeze without using future holdout | optional |
| Alternative threshold | sensitivity/operating point | development-only selection and preregistered formal role | diagnostic; not post-hoc primary |
| External published system | contextual/empirical comparison | credible literature, compatible construct/input/output, lawful reproducibility | literature-dependent, not currently selected |

No competitor performance or formal effect size exists yet.

## 15. Threat-model and architecture figure specifications

### F02 — formal threat model

Actors/components: untrusted MCP server; tool metadata/catalog; MCP client/agent;
operator; static inspector; custom rule pack; suppression policy; approved
baseline; optional loopback retrieval transport; terminal/JSON/CSV/SARIF report;
report consumer. Mark boundaries at file/network input, configuration, baseline,
detector, output and research artifact. Show attacker goals (influence, conceal,
solicit data, misrepresent capability, exhaust resources) and non-goals (runtime
tool behavior, remote malware analysis, all prompt injection, full MCP gateway).

Use different boxes for “tool-poisoning-like/suspicious metadata construct” and
“broader security-quality warning.” Do not place a padlock implying the agent is
secured by the inspector.

### F03 — current architecture

```text
INPUT → STRICT PARSING → VALIDATION → NORMALIZATION → RULE FAMILIES
      → SUPPRESSION → FINDING MATERIALIZATION → RETENTION/BUDGET
      → RISK / AFFECTED / --fail-on / EVALUATION DECISION → REPORTING

NORMALIZED TOOL → CANONICALIZATION → FINGERPRINT → BASELINE/DRIFT
```

This order must show that retained findings currently feed semantic decisions.
Finding materialization also occurs before retention, so output budgets are not a
complete intermediate compute bound.

### F07 — proposed corrected architecture

```text
DETECTION STATE (bounded/streamed complete decision facts)
                 ↓
DECISION STATE (risk, threshold, fail-on, affected/predicted)
                 ↓
PRESENTATION / RETENTION STATE (bounded details/evidence)
```

Caption: **[FUTURE FORMAL—NOT YET IMPLEMENTED]**. A separate arrow may send
detection facts to a deterministic presentation reservoir. Do not visually merge
this with F03 or imply completion.

## 16. P0 finding-budget thesis handling

Document it in four places:

1. Ch4 current architecture and implementation limitation (F06/T21);
2. Ch3 formal engineering freeze gate;
3. Ch6 threats to validity and adversarial resource behavior;
4. Ch7 future work only if still unresolved—otherwise describe and test the fix.

Verified historical impact statement:

- H0: 16 total findings, at most 2/sample, at most 53 evidence characters/sample;
- v0.3 exploratory: 24 findings, at most 2/sample, at most 277 evidence
  characters/sample;
- limits: 64 findings/tool, 2,048/report, 8,192 retained evidence characters/tool.

Therefore the preserved H0/v0.3 results were below the retention limits and were
not affected by truncation. The defect nevertheless permits future hostile/large
inputs to change risk, affected counts, `--fail-on` and evaluation predictions
after exhaustion. State both facts; neither hide it nor claim it invalidated H0.

## 17. Reproducibility evidence plan

T22 should separate three columns:

| Engineering reproduction | Preserved-evidence verification | Experimental replication |
|---|---|---|
| clean clone, install, Ruff, mypy, 472 tests, 92.95%, wheel/sdist, clean-wheel smoke | H0/Day3C/Day4C/reviewer SHA; three corpus hashes; config identities; tag target; arithmetic | fresh candidate, untouched data, independent governance and approved protocol—**not available** |

Recommended appendix: exact recovery commands and expected identities, linked to
`clean-room-reproducibility-drill.md`. Main text should report one concise table
and explain that unkeyed hashes support identity/integrity against trusted
expected values, not independent authenticity.

## 18. Claims requiring external literature

The repository proves facts about this project; it cannot establish ecosystem
importance, theoretical foundations, prior-art gaps or novelty. Use the existing
literature workbook as a search ledger and verify every source before citation.

| Topic | Why needed / chapter | Search terms | Preferred source |
|---|---|---|---|
| MCP architecture/specification | Define protocol roles/metadata accurately; Ch1/2 | Model Context Protocol architecture tools/list tool schema | official specification/docs, versioned |
| MCP security guidance/threats | Establish broader attack surface and scope; Ch1/2 | MCP security tool metadata trust boundary | official security docs, credible advisories/research |
| Tool poisoning | Define target construct and distinguish intent/effect; Ch1–3 | LLM agent tool poisoning malicious tool description | primary research/technical reports with methods |
| Prompt injection | Place direct metadata instructions in established theory; Ch2 | prompt injection LLM agents taxonomy | peer-reviewed/primary research |
| Indirect prompt injection | Explain untrusted external instructions; Ch2 | indirect prompt injection tool output metadata | peer-reviewed/primary research |
| Agent/tool trust and capability control | Motivate metadata/capability mismatch; Ch2/3 | LLM agent tools trust least privilege capability | security/agent research |
| Static analysis foundations | Justify inert deterministic inspection and limits; Ch2/4 | static security analysis soundness completeness tradeoff | textbooks/surveys/peer-reviewed research |
| Rule/signature-based detection | Explain interpretability/evasion/maintenance trade-offs; Ch2/6 | signature rule based intrusion detection false positives evasion | peer-reviewed survey/empirical work |
| Schema integrity/validation | Ground malformed/privileged schema warnings; Ch2/3 | JSON Schema security validation API schema integrity | official standard + security research |
| Configuration drift/integrity monitoring | Situate fingerprints/baselines; Ch2/4 | configuration drift canonical hash security monitoring | standards/peer-reviewed/authoritative guidance |
| Security-detector evaluation | Justify matrix, recall/FPR, prevalence and splits; Ch3/5 | security detector evaluation precision recall false positive rate holdout | methodological papers/texts |
| Small-sample uncertainty/Wilson intervals | Support interval choice/interpretation; Ch3/5 | Wilson score interval binomial proportion small sample | statistical primary/textbook source |
| Human annotation/inter-rater agreement | Explain blinding/kappa and limitations; Ch3/5 | Cohen kappa inter-rater reliability annotation bias | original method + modern methodological guidance |
| Adversarial robustness | Design paraphrase/Unicode/relocation tests; Ch2/3/6 | adversarial robustness NLP rule detector paraphrase Unicode | peer-reviewed empirical research |
| Reproducible security research | Ground artifact/version/environment practices; Ch3/6 | reproducible cybersecurity experiments artifact provenance | research methods/venue guidelines |
| Software supply-chain/provenance | Qualify hashes/tags/signatures; Ch2/6 | software artifact provenance signed release reproducible build | standards/authoritative guidance |
| Dataset shift/external validity | Interpret development-to-pilot collapse; Ch2/6 | dataset shift external validity security classifier | methodological/peer-reviewed work |
| Base rates/operational alert burden | Explain balanced prevalence and precision; Ch2/6 | base rate fallacy intrusion detection precision prevalence | security detection research/textbooks |

Do not cite the repository as evidence for general MCP adoption, attack prevalence,
state of the art, novelty, or accepted statistical practice.

## 19. Claims supported directly by repository evidence

These factual claims do not require an external citation, although the thesis
should cite a repository version/artifact path:

1. Current package/version, CLI entry point and rule-pack identity.
2. Static scan paths do not invoke supplied tools.
3. Optional retrieval is explicit, bounded and loopback-only.
4. Strict JSON rejects duplicate keys/non-finite values.
5. Document/depth/node/text/tool bounds are implemented.
6. Unicode NFC normalization and deterministic canonicalization are implemented.
7. Seven families and 16 current built-in rule IDs exist.
8. Custom rules are bounded literal data and collision checked.
9. Suppressions use exact rule/optional tool scopes.
10. Risk calculation is deterministic/capped but currently retention-coupled.
11. Terminal/CSV/JSON/SARIF formats and output controls exist.
12. Tool/component fingerprints and baseline drift comparison exist.
13. Development corpus is 80 samples and produced 37/36/4/3 in its recorded run.
14. H0 artifact contains 5/18/6/19 and the stated metrics/CIs/timing.
15. Day 3C contains the preserved post-unblinding failure analysis.
16. One reviewer produced 47/48 agreement and κ≈0.9583; difficulty agreement was 16/48.
17. v0.3 exposed exploratory artifact contains 11/18/6/13.
18. All six H0 binary false positives remained in the v0.3 exploratory matrix.
19. Seven historical ablation artifacts and their matrices are preserved.
20. Critical artifacts/corpora/configurations have the recorded hashes.
21. `v0.3.0a1` remains an annotated historical tag at `3744710...`.
22. Day 6K clean-room engineering checks passed on the recorded Windows setup.
23. Historical H0/v0.3 artifacts stayed far below finding/evidence retention caps.
24. No fresh untouched v0.3 confirmatory artifact exists in the repository.

## 20. Caption writing guide

### Figure caption templates

1. **F01:** “**[ENGINEERING]** MCP tool-definition inspection context in version
   0.3.0a1. The static scan path reads metadata without invoking discovered tools;
   optional loopback retrieval is shown separately.”
2. **F03:** “**[ENGINEERING]** Current scan pipeline from strict parsing to report
   rendering. Retained findings currently feed risk and decision outputs; the
   diagram describes implemented behavior, not the proposed remediation.”
3. **F08:** “**[DEVELOPMENT + PILOT H0]** Observed metric point estimates for the
   visible development corpus (N=80) and frozen pilot holdout (N=48). The groups
   have different scientific roles and do not estimate deployment performance.”
4. **F09:** “**[PILOT H0]** Confusion matrix for the frozen v0.2 pilot evaluation
   (N=48; 24 suspicious/24 benign): TP=5, TN=18, FP=6, FN=19.”
5. **F10:** “**[PILOT H0]** Observed accuracy, recall and FPR with Wilson 95%
   intervals for the 48-sample pilot; denominators are 48, 24 and 24.”
6. **F11:** “**[EXPLORATORY—POST-UNBLINDING]** Descriptive taxonomy of H0 false
   negatives and false positives derived after result exposure; counts are
   corpus-specific and the taxonomy was not the primary preregistered analysis.”
7. **F12:** “**[PILOT H0]** Analysis-core and static-end-to-end latency summaries
   on the recorded Windows/Python environment, with protocol-specific warm-ups,
   repetitions, medians and p95 values.”
8. **F13:** “**[HUMAN REVIEW]** Binary and difficulty agreement for one blinded
   reviewer over 48 pilot samples. Binary κ≈0.9583 does not validate the detector.”
9. **F14:** “**[EXPLORATORY—POST-UNBLINDING; NOT CONFIRMATORY]** v0.2 H0 and v0.3
   point estimates on the same exposed 48-sample corpus; v0.3 was designed after
   H0 inspection and cannot establish improved generalization.”
10. **F19:** “**[FUTURE FORMAL—NOT YET AVAILABLE]** Proposed supervisor-gated
    formal evaluation workflow. No corpus, matrix or result is implied.”

### Table caption templates

1. **T01:** “**[ENGINEERING]** Implemented scope, security boundaries and explicit
   non-goals of MCP Tool Security Inspector 0.3.0a1.”
2. **T05:** “**[ENGINEERING]** Current built-in detector families and stable rule
   identities; entries are implementation mechanisms, not validated attack classes.”
3. **T09:** “**[DEVELOPMENT/PILOT/EXPLORATORY]** Composition, exposure status and
   identity of the three preserved corpora.”
4. **T10:** “**[DEVELOPMENT]** Confusion counts and metrics on the visible balanced
   80-sample development corpus; values are regression evidence.”
5. **T11:** “**[PILOT H0]** Raw confusion matrix for the frozen v0.2 pilot primary
   evaluation (N=48).”
6. **T12:** “**[PILOT H0]** Primary observed metrics, denominators and Wilson 95%
   intervals for the independently reviewed pilot holdout.”
7. **T16:** “**[PILOT H0—SECONDARY]** Outcome matrices after removing each
   preregistered detector family; effects are specific to this corpus/configuration.”
8. **T18:** “**[HUMAN REVIEW]** Blinded review design and agreement for 48 pilot
   samples, including the preserved R08 disagreement and difficulty instability.”
9. **T20:** “**[EXPLORATORY—POST-UNBLINDING]** Descriptive v0.2/v0.3 comparison on
   the exposed pilot holdout; the table is not evidence of formal superiority.”
10. **T24:** “**[FUTURE FORMAL—NOT YET AVAILABLE]** Blank result structure to be
    populated only from the preserved artifact after an approved formal run.”

## 21. Safe result-sentence templates

These sentences may be adapted only if the cited numbers and scientific-status
labels remain intact.

1. “On the visible 80-sample development corpus, the recorded configuration
   produced TP=37, TN=36, FP=4 and FN=3; this is development evidence, not an
   estimate of performance on unseen deployment data.”
2. “The frozen v0.2 pilot H0 used an independently reviewed, balanced 48-sample
   holdout containing 24 benign and 24 suspicious definitions.”
3. “The v0.2 pilot produced TP=5, TN=18, FP=6 and FN=19.”
4. “Observed pilot accuracy was 47.92%, precision 45.45%, recall 20.83%, F1
   28.57% and false-positive rate 25.00%.”
5. “The Wilson 95% interval for pilot recall was 9.24%–40.47%, illustrating the
   uncertainty associated with 24 suspicious samples.”
6. “Performance dropped substantially from visible development data to the
   independent pilot holdout, providing evidence of weak transfer under this
   corpus design.”
7. “Nineteen of 24 suspicious pilot samples were missed at the preregistered
   MEDIUM threshold.”
8. “Six of 24 benign pilot samples were classified as suspicious, corresponding
   to an observed FPR of 25.00%.”
9. “Failure categories derived after H0 exposure are diagnostic, post-hoc
   interpretations rather than preregistered confirmatory outcomes.”
10. “The recorded analysis-core pilot timing had a median of 1.5354 ms per tool
    and p95 of 3.2229 ms per tool on the recorded environment.”
11. “The static-end-to-end boundary was slower than analysis-core in the recorded
    protocol, as expected because it includes additional processing.”
12. “One blinded reviewer agreed with 47 of 48 binary labels, with no abstentions.”
13. “Cohen’s κ was approximately 0.9583 for binary labels, indicating very high
    agreement between that reviewer and the frozen labels in this sample.”
14. “Difficulty agreement was only 16 of 48, showing that difficulty judgments
    were less stable than binary labels.”
15. “The preserved R08 disagreement was adjudicated without rewriting the
    reviewer’s original response.”
16. “After H0 exposure, v0.3 produced TP=11, TN=18, FP=6 and FN=13 on the same
    corpus; this is explicitly exploratory evidence.”
17. “The exposed-corpus v0.3 rerun increased observed recall from 20.83% to
    45.83%, but cannot establish improved generalization because the design was
    informed by the exposed H0 failures.”
18. “Observed v0.3 FPR remained 25.00% on the exposed corpus, and all six H0
    binary false positives remained false positives.”
19. “Family-ablation changes describe dependence within this corpus and frozen
    configuration; they do not establish real-world causality or family value.”
20. “A future formal claim requires a supervisor-approved construct, remediated
    decision semantics, a frozen detector/configuration and a genuinely untouched
    evaluation corpus.”

## 22. Forbidden or unsafe claims

| Unsafe statement | Why it must not be used |
|---|---|
| “The detector accurately detects tool poisoning.” | Pilot recall was 20.83%, and the target construct includes broader suspicious/security-quality signals. |
| “The detector is 91.25% accurate.” | 91.25% is visible development-corpus accuracy, not independent generalization evidence. |
| “The system has 47.92% real-world accuracy.” | H0 is a small, balanced, synthetic-heavy pilot, not a deployment sample. |
| “The detector generalizes to unseen MCP servers.” | One pilot corpus cannot support this broad population claim. |
| “v0.3 improved generalization.” | v0.3 was designed and rerun after H0 exposure on the same corpus. |
| “v0.3 is validated.” | No fresh untouched confirmatory evaluation exists. |
| “The project is state of the art.” | No systematic comparison against literature-supported alternatives establishes this. |
| “This is the first MCP security detector.” | Novelty requires a defensible literature review; the repository cannot prove priority. |
| “The tool is production-ready.” | Pilot effectiveness, remaining P0 decision coupling and limited external validation contradict this. |
| “Millisecond latency proves real-time suitability.” | Timing is machine/protocol dependent and does not cover all integration or workload conditions. |
| “FPR is the percentage of alerts that are wrong.” | FPR is FP/(FP+TN); the false-discovery proportion is FP/(TP+FP). |
| “κ≈0.9583 proves detector accuracy.” | κ measures reviewer/label agreement, not detector performance. |
| “The review proves the labels are objectively true.” | One reviewer and one adjudication process cannot establish objective ground truth. |
| “Malformed schemas are malicious tool poisoning.” | Malformation may be accidental; it is a security-quality warning unless the construct says otherwise. |
| “A matching hash proves the data are trustworthy.” | A hash proves byte identity relative to a known value, not truth, provenance or benign intent. |
| “The scanner never uses the network.” | Optional explicit loopback retrieval exists; the accurate claim concerns default static analysis and its restrictions. |
| “Resource bounds make denial of service impossible.” | Bounds reduce exposure; they do not prove absence of all resource-exhaustion paths. |
| “Seven families cover MCP attacks.” | They cover defined static metadata patterns, not the universe of MCP or runtime attacks. |
| “The 16 rules are 16 validated attack types.” | Rule identities are implementation mechanisms and may overlap constructs. |
| “Ablation proves family X causes detection success.” | The effect is conditional on this corpus, threshold, interactions and rule implementation. |
| “A 50/50 holdout reflects deployment prevalence.” | It was balanced for evaluation and is explicitly not prevalence-representative. |
| “English results apply to all languages.” | All fixtures are English-only. |
| “Independent review means expert consensus.” | Only one independent reviewer was used. |
| “Reproducible means scientifically replicated.” | Reproduction of bytes/execution is not independent replication of conclusions. |
| “Future formal results should exceed v0.3.” | No future outcome may be presumed or fabricated. |
| “No finding means the tool is safe.” | Static pattern non-detection is not a safety proof and says little about runtime behavior. |
| “Every finding represents malicious intent.” | Findings are signals; intent needs context and may be benign. |

## 23. Supervisor decision register

| Decision | Main options | Evidence needed | Deadline |
|---|---|---|---|
| Final framing | suspicious metadata; known poisoning patterns; integrity plus metadata analysis | literature and construct fit | before proposal approval |
| Core construct | narrow poisoning; layered taxonomy | operational definitions and examples | before data design |
| Primary research question | effectiveness; robustness; integrity drift | measurable variables and available scope | before preregistration |
| P0 remediation acceptance | redesign decision state; defer formal confirmation | implementation/test evidence | before detector freeze |
| Formal detector version | remediated v0.3 descendant; another approved candidate | version/rule/config identities | before corpus creation |
| Threshold | retain MEDIUM; preregister another threshold | development-only rationale | before freeze |
| Holdout prevalence | balanced; deployment-informed; dual reporting | intended estimand and feasible sampling | before sample creation |
| Sample size | CI-width or power-informed N | expected rates, precision target, workload | before sample creation |
| Sample authorship | independent; mixed; student with controls | contamination and feasibility assessment | before sample creation |
| Review protocol | two reviewers; two plus adjudicator; domain expert | cost, expertise and reliability goal | before review begins |
| Primary metrics | recall/FPR; precision/recall; F1 | harm model and prevalence | before unblinding |
| Statistical method | Wilson intervals; paired comparison method | design and denominators | before preregistration |
| Comparison baseline | historical v0.2; simple lexical; approved external tool | comparability and literature support | before freeze |
| Real-world metadata | exclude; public; approved private | ethics, privacy, licence and storage review | before collection |
| Multilingual scope | English only; bounded added languages | expertise and data availability | before corpus design |
| Latency claim | recorded feasibility only; bounded “lightweight” claim | benchmark protocol and environments | before writing claims |
| Final thesis scope | detector only; detector plus integrity drift | time and research-question alignment | proposal approval |

## 24. Evidence provenance and immutability

### Provenance-chain specification

```text
research question + preregistration
        ↓ frozen identities
source commit + rule pack + configuration + threshold
        ↓ static evaluation
corpus bytes + labels + review record + corpus hash
        ↓ immutable raw artifact
confusion counts + timing observations + environment metadata
        ↓ reproducible analysis script/formula
tables + figures + confidence intervals
        ↓ bounded interpretation
thesis claims with scientific-status labels
```

Human judgment enters at construct definition, sample authorship, labelling,
review/adjudication, failure taxonomy and interpretation. Hashes and deterministic
code preserve identity; they do not turn those judgments into objective truth.

### Immutability rules

1. Never edit a preserved raw experiment artifact to improve presentation.
2. Store a SHA-256 before deriving tables or figures.
3. Derive display assets from a copy/read-only input and record the input hash.
4. Do not overwrite a primary-run artifact; corrections create a new, labelled
   analysis artifact with a provenance link.
5. Keep confirmatory and post-unblinding exploratory directories and captions
   visibly distinct.
6. Preserve reviewer source separately from adjudicated labels.
7. Freeze corpus, labels, exclusions, threshold and configuration before the
   primary run.
8. Record scripts, package versions and command lines used for transformation.
9. If a source identity does not match, stop rather than silently regenerate.
10. Any later tuning starts a new exploratory phase and cannot revise H0.

### Future figure-generation workflow

1. Select the registered artifact and verify its SHA-256.
2. Validate artifact schema and historical rule/configuration identity.
3. Run a version-controlled, non-mutating extraction script.
4. Emit a machine-readable intermediate table with denominators and units.
5. Check counts against raw confusion cells and timing observation counts.
6. Generate SVG/PNG/PDF deterministically where practical.
7. Review labels, scientific-status banner, axis scales and uncertainty display.
8. Record source hash, script commit and output hash in an asset manifest.
9. Link—not duplicate—the authoritative result in thesis working notes.

### Figure reproducibility checklist

- [ ] Source artifact path and SHA-256 recorded.
- [ ] Artifact scientific status shown.
- [ ] Extraction/generation command recorded.
- [ ] Script commit and dependency versions recorded.
- [ ] All denominators and units shown.
- [ ] Axis starts/scales cannot visually exaggerate differences.
- [ ] Confidence intervals shown where registered.
- [ ] Colors remain distinguishable in grayscale/color-vision deficiency.
- [ ] Caption states corpus, N, version and confirmatory/exploratory status.
- [ ] Output hash and creation UTC recorded.

### Table reproducibility checklist

- [ ] Every number traces to a named artifact field or documented formula.
- [ ] TP/TN/FP/FN totals equal N.
- [ ] Metric denominators are explicit.
- [ ] Rounding occurs only for display; calculations retain full precision.
- [ ] Missing/not-applicable values are not converted to zero.
- [ ] Confidence-interval method and level are named.
- [ ] Timing boundary, warm-ups, repetitions and observation count are shown.
- [ ] Post-hoc rows are labelled exploratory/diagnostic.
- [ ] Table source hash and generation script are recorded.
- [ ] Manual transcription receives an independent check.

## 25. Interpreting future formal outcomes

### Priority of results

- **Primary:** preregistered effectiveness metrics and confidence intervals for
  the untouched formal corpus at the frozen threshold.
- **Secondary:** registered latency and approved comparisons/ablations.
- **Diagnostic:** category/field/difficulty strata and failure taxonomy.
- **Exploratory:** any analysis proposed after unblinding.

### If results are poor or inconclusive

Preserve the primary artifact immediately and report the preregistered outcome.
Do not change labels, threshold, exclusions or detector and rerun under the same
confirmatory name. Discuss uncertainty and construct/corpus limitations. Move any
fix or new hypothesis into a clearly named post-unblinding exploratory phase. A
negative result can still support conclusions about feasibility, limitations,
failure modes and required future work.

### If results are strong

Do not upgrade the claim beyond the sampled construct and population. Report raw
counts, uncertainty and prevalence. Check leakage, exclusions, review agreement
and artifact identity before celebrating point estimates. Avoid “solves,”
“production-ready,” “all attacks” and “state of the art” unless independent
evidence specifically supports them.

## 26. Threats-to-validity evidence table

| Threat | Current evidence | Mitigation/transparent treatment | Residual limitation |
|---|---|---|---|
| Construct ambiguity | seven families include poisoning-like and security-quality signals | freeze layered construct taxonomy | intent cannot be inferred from text alone |
| Synthetic-heavy data | corpus documentation and fixtures | diversify future development/holdout authorship | realism remains sampling-dependent |
| English-only content | fixture inspection/documentation | limit claims or add approved multilingual design | no current multilingual evidence |
| Balanced prevalence | 24/24 pilot | report conditional rates and state sampling design | precision differs under deployment prevalence |
| Small N | H0 N=48 | Wilson intervals; raw counts | wide uncertainty, especially strata |
| Small strata | category groups around 3–6 | label as diagnostic | percentages can be unstable |
| Matched-pair dependence | corpus design records | use paired-aware analysis if making paired claims | samples may not be independent |
| Provenance/label confounding | author-designed taxonomy/fixtures | independent authorship/review where feasible | reviewer independence does not erase design bias |
| Description-length imbalance | Day 3 evidence | measure/report; improve development design | may cue lexical rules |
| Subjective difficulty | 16/48 agreement | treat as diagnostic | difficulty strata are weak evidence |
| One reviewer | review record | future two-reviewer minimum for discussion | κ reflects only one comparison |
| Adaptive attacker | static bounded rules | development robustness suite | open-world bypass remains possible |
| Metadata/runtime gap | system statically inspects metadata | explicit non-goal | runtime behavior is not evaluated |
| Decision-budget coupling | source audit; artifacts below caps | fix before formal freeze and regression-test | present release semantics remain flawed at caps |
| Timing environment | artifact runtime metadata | fixed protocol and transparent machine record | cross-machine performance not established |
| Post-unblinding v0.3 | chronological Git/research record | label exploratory; require fresh holdout | same corpus cannot reconfirm v0.3 |
| Statistical multiplicity | many strata/ablations possible | preregister primary endpoints | secondary patterns remain hypothesis-generating |
| Reproducibility drift | hashes, commit/config identities | clean-room and manifest checks | reproducibility is not external validity |

## 27. Contribution-to-evidence map

| Potential contribution | Evidence available now | Claim boundary |
|---|---|---|
| Bounded deterministic metadata scanner | source, tests, wheel/CLI smoke, technical map | engineering implementation, not effectiveness |
| Multi-family suspicious-metadata rule set | 16 stable built-in rule IDs and tests | implemented coverage of defined patterns only |
| Canonical fingerprints and drift comparison | canonicalization/baseline/compare source and tests | deterministic identity/drift aid, not authenticity |
| Safe output handling | reporter source and injection/redaction tests | implemented defenses under tested conditions |
| Reproducible evaluation framework | artifact schema, corpus/config hashes, run metadata | supports repeatability/provenance, not replication |
| Independently reviewed pilot study | review records and H0 artifact | one small synthetic-heavy pilot |
| Transparent negative/limited H0 result | preserved matrix, CIs and failure evidence | scientifically useful feasibility evidence |
| Post-hoc rule-design hypotheses | Day 4 design and exposed rerun | exploratory only |
| Research continuity package | Day 6 documents/recovery checks | handover evidence, not detector validation |
| Formal FYP outcome | not available | no claim until approved untouched study exists |

## 28. Thesis asset inventory and priorities

| Asset class | Core assets | Availability | Priority |
|---|---|---|---|
| Tables | T01, T05, T09, T11, T12, T18, T20, T21, T23 | source/artifacts available | essential |
| Tables | T10, T13–T17, T22 | available but contextual/secondary | supporting |
| Tables | T24 formal-results shell | structure only; values unavailable | future |
| Figures | F01, F03, F09, F10, F12, F13, F14, F16, F18 | specifications and inputs available | essential |
| Figures | F04–F08, F11, F15, F17 | available/supporting | supporting |
| Figures | F19–F20 | design only | future |
| Equations | accuracy, precision, recall, F1, FPR, specificity, Wilson interval | definitions available | essential |
| Appendices | rule catalogue, commands, artifact manifest, reviewer protocol, preregistration template | available/partly future | essential |
| Artifact references | H0, static timing, Day 3C, v0.3, ablations | preserved with identities | essential |
| Code references | loader, normalizer, detectors, risk, fingerprint, evaluation, reporter, CLI | available at checkpoint | essential |
| Dataset references | development, exposed pilot holdout, exploratory fixtures | available with status labels | essential |
| Review references | reviewer source, adjudication, agreement record | preserved | essential |
| Formal holdout/results | new untouched corpus and primary artifact | **not available** | future gate |

The recommended main thesis should use roughly 8–12 core tables and 7–10 core
figures, moving inventories, verbose matrices and diagnostic breakdowns to
appendices. The exact count is a writing decision, not a target to inflate.

## 29. Viva drill: point to the evidence

| Examiner question | Defensible answer | Evidence anchor |
|---|---|---|
| What does the system inspect? | MCP tool-definition metadata and schema-like fields, statically. | T01; `src/mcpsec/normalizer.py` |
| Does it execute tools? | No on the static scan path; retrieval only requests loopback `tools/list`. | F01; `src/mcpsec/retrieval.py` |
| What is the target? | Defined suspicious metadata constructs, with poisoning-like core signals separated from quality warnings. | construct taxonomy; T03 |
| How many rules exist? | Sixteen built-in identities across seven families in 0.3.0a1. | T05; rule registry |
| Why rules rather than an LLM? | Determinism, auditability, bounded offline analysis and stable evidence; effectiveness remains empirical. | architecture/rationale; tests |
| What was H0? | A frozen v0.2 pilot on 48 independently reviewed balanced samples. | H0 artifact; T11–T12 |
| What were the raw H0 results? | TP=5, TN=18, FP=6, FN=19. | H0 artifact hash; F09 |
| Why was recall low? | Most suspicious constructs did not match frozen rule representations; post-hoc taxonomies describe, not prove, causes. | Day 3C; F11 |
| What does 25% FPR mean? | Six of 24 benign samples were flagged. | T12; metric equation |
| Why not report development accuracy as success? | The development corpus was visible and used during engineering. | T09–T10 |
| Is v0.3 better? | It had higher observed recall on the exposed corpus, but no valid generalization comparison. | T20; red-line box |
| Why preserve a poor result? | It is the honest primary outcome and informed bounded future hypotheses. | immutable H0 artifact; research status |
| What does κ≈0.9583 mean? | High binary label agreement between one reviewer and frozen labels, not detector accuracy. | review record; T18 |
| What was R08? | The one binary disagreement, preserved and adjudicated under the frozen construct. | reviewer source/adjudication |
| Why are hashes important? | They bind claims to exact bytes/configuration; they do not prove truth. | T07; recovery manifest |
| Why MEDIUM? | It was frozen before H0 and must not be changed after seeing outcomes. | H0 configuration artifact |
| What is the P0 defect? | Retention caps can currently alter risk/decision semantics after finding storage is exhausted. | T21; source audit |
| Did P0 corrupt H0? | Recorded maxima were far below caps, so preserved H0/v0.3 were unaffected. | artifact-impact calculation |
| What must change? | Separate detection/decision state from bounded presentation retention and test invariants. | F18; formal blueprint |
| Can attackers bypass it? | Yes; static pattern detection is inherently incomplete, especially against adaptive representations. | threats table |
| Is a finding proof of malice? | No, it is a reviewable signal with possible benign explanations. | claim C04; unsafe-claim table |
| Is the tool production-ready? | No; it is a pre-FYP research prototype/pilot with a known P0 and limited validation. | research status; Day 6E |
| What makes the work reproducible? | commits, hashes, schema/config/rule identities, runtime metadata and preserved raw artifacts. | provenance chain; T23 |
| What formal evidence is missing? | An approved frozen candidate and fresh independently reviewed untouched holdout. | T24; F19 |
| What is your strongest contribution today? | A transparent bounded engineering prototype plus preserved, honestly reported pilot evidence and recovery chain. | contribution map |

## 30. Future formal evidence-freeze procedure

1. Obtain supervisor approval for framing, construct, questions and threat model.
2. Resolve the finding-budget decision coupling and add invariant/regression tests.
3. Complete development-only robustness and engineering gates.
4. Freeze source commit, package version, rule-pack version and rule identities.
5. Freeze threshold, suppressions, custom-rule policy and configuration hash.
6. Approve holdout sampling, prevalence, size and authorship protocol.
7. Create the holdout only after detector freeze; prevent developer inspection.
8. Conduct blinded independent review/adjudication and freeze labels.
9. Record corpus name/version/hash and reviewer-source identity.
10. Freeze preregistration, metrics, intervals, exclusions, timing and stop rules.
11. Verify clean Git/environment/artifact destination and pass GO/NO-GO gates.
12. Execute exactly one primary evaluation and immediately preserve/hash raw output.
13. Derive preregistered results; label every later analysis or modification
    post-unblinding exploratory.

## 31. Ready-for-thesis checklist

### Scientific framing

- [ ] I can state the problem without equating suspicion with malicious intent.
- [ ] The formal construct taxonomy is supervisor-approved.
- [ ] Core targets, supporting signals and quality warnings are distinct.
- [ ] Research questions are measurable and do not presume success.
- [ ] General and specific objectives separate design, implementation and evaluation.
- [ ] The threat model names assets, boundaries, capabilities, assumptions and non-goals.
- [ ] Runtime behavior is not claimed from metadata-only evidence.
- [ ] Novelty wording is supported by a completed literature review.

### Engineering evidence

- [ ] The scan pipeline can be traced to specific source modules.
- [ ] All built-in rule IDs/families and their limits can be explained.
- [ ] Static analysis and optional retrieval boundaries are accurately described.
- [ ] Canonicalization, hashes and drift semantics can be defended.
- [ ] Output-injection and privacy limitations are documented.
- [ ] Finding-budget decision coupling is fixed before formal freeze.
- [ ] The fix has cap-boundary, order, CLI and evaluation regression tests.
- [ ] Resource bounds and deterministic truncation behavior are tested.
- [ ] Historical artifact compatibility remains intact.
- [ ] Package/wheel smoke and full quality gates pass.

### Data and review

- [ ] Development, pilot, exploratory and future formal data are never conflated.
- [ ] Future holdout authorship and contamination controls are documented.
- [ ] Sample-size rationale is supervisor/statistics informed.
- [ ] Prevalence choice and resulting estimand are stated.
- [ ] Labels follow a written operational guide.
- [ ] Reviewers are blinded to predictions and expected labels where applicable.
- [ ] Disagreements/abstentions/adjudication are preserved.
- [ ] Corpus bytes, labels and review source are frozen and hashed.

### Experiment and statistics

- [ ] Detector commit/rule pack/configuration/threshold are frozen.
- [ ] Primary and secondary metrics are preregistered.
- [ ] Metric equations and denominators are correct.
- [ ] Confidence-interval method is selected before unblinding.
- [ ] Category analyses are explicitly secondary/diagnostic.
- [ ] Timing boundary, warm-ups, repetitions and summaries are frozen.
- [ ] Exclusion, comparison, ablation and stop rules are frozen.
- [ ] Environment and invocation metadata are captured.
- [ ] Raw primary artifact destination is immutable and ready.
- [ ] Supervisor GO approval is recorded before execution.

### Results and discussion

- [ ] Raw confusion counts precede rounded metrics.
- [ ] Every result table/figure traces to an artifact hash.
- [ ] Confirmatory and exploratory outputs are visually labelled.
- [ ] Negative/inconclusive outcomes have not triggered retrospective tuning.
- [ ] Uncertainty and small-stratum caveats accompany percentages.
- [ ] Development results are not described as generalization.
- [ ] v0.3 exposed results remain exploratory in every chapter.
- [ ] Ablations are described as corpus-dependent contribution analyses.
- [ ] Reviewer agreement is not presented as detector validation.
- [ ] Strong results, if any, remain bounded to the sampled construct/population.

### Preservation and viva readiness

- [ ] Critical source/corpus/config/artifact hashes have been reverified.
- [ ] Figure and table generation commands are recorded.
- [ ] Captions include N, version, corpus and scientific status.
- [ ] Private paths/identifiers are minimized in newly generated thesis assets.
- [ ] Repository, independent backup and recovery procedure are current.
- [ ] I can manually calculate H0 accuracy, precision, recall, F1 and FPR.
- [ ] I can explain P0 impact and why historical artifacts were unaffected.
- [ ] I can point to evidence for each central claim without relying on memory.
- [ ] I can name the strongest limitations before an examiner does.
- [ ] I can state exactly which formal evidence does not yet exist.

## 32. Blueprint boundary and zero-fabrication declaration

This document is a thesis-evidence design and traceability plan. It does not
constitute a thesis result, new experiment, literature review or supervisor
approval. All formal-result cells remain deliberately blank. Existing numbers
are transcribed only from preserved repository evidence and retain their original
development, pilot or post-unblinding status.

No exposed holdout was rerun to create this blueprint. No detector experiment was
executed. No formal-FYP result, sample size, performance value or novelty claim
was fabricated. No detector, corpus, label, threshold, risk model or frozen
research evidence was modified.
