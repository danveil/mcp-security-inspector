# Day 3D Discussion Evidence

This document interprets the frozen Day 3B results using the Day 3C failure analysis. It does not replace H0, validate a detector change, or claim population-level generalization.

## Evidence-status map

| Evidence | Scientific status |
|---|---|
| Primary H0 effectiveness | **PREREGISTERED / CONFIRMATORY** |
| H1 timing-boundary run | **PREREGISTERED / CONFIRMATORY** secondary timing evidence |
| Seven planned family ablations | **PREREGISTERED / CONFIRMATORY within the experiment design**; interpretation is descriptive and corpus-specific |
| Day 3C failure taxonomy | **POST-UNBLINDING DESCRIPTIVE ANALYSIS** |
| E1–E8 improvement ideas | **POST-UNBLINDING EXPLORATORY HYPOTHESES — NOT VALIDATED** |

## A. Development–holdout generalization gap

Development accuracy was 91.25% and holdout accuracy was 47.92%; recall moved from 92.50% to 20.83% and F1 from 91.36% to 28.57%. The observed gap is evidence that development performance did not transfer to this independently reviewed synthetic holdout under the frozen configuration. It is consistent with development examples and rule vocabularies being more closely aligned than the holdout's paraphrases and metadata placements. It is not a statistical estimate of performance across real MCP servers, and the term “overfitting” should be used as a plausible interpretation rather than a proven causal diagnosis.

## B. Lexical and semantic coverage

Seventeen of nineteen false negatives produced no detector finding and risk 0. Only two produced an informational finding below `MEDIUM`. Within this corpus, that distribution points more strongly to rule coverage and semantic interpretation gaps than to the classification threshold alone. The broad detector traversed much of the preserved metadata, but the narrow deterministic grammars did not map many observed phrases to findings. Lowering the threshold could affect the two `CAP-001` cases; it would not recover the 17 no-finding cases.

## C. Instruction-override paraphrases

All three expected instruction-override samples were missed. They used authority and ranking concepts such as metadata governing a conflicting request, ranking ahead of conversation guidance, and an authoritative operating policy. `PI-001` is centered on more literal forms such as ignoring, disregarding, overriding, following, prioritizing, or obeying instructions. The result illustrates a semantic-paraphrase boundary: the security construct was present under the frozen labels, while the exact deterministic phrase grammar was absent.

## D. Contextual concealment

All four expected concealment samples were missed. The samples expressed omission from user-facing explanation, exclusion from an operator-visible account, or presentation of only a benign prefix alongside encoded content. `HID-001` recognizes a narrower literal vocabulary such as “do not tell,” “hide,” “silently,” or “keep it secret from.” This corpus therefore exposes a gap between literal secrecy terms and contextual narratives about visibility, reporting, and omission.

## E. Sensitive-data context

`SEC-001` caused four of six binary false positives. The triggers were security words in titles or descriptions—`Password`, `secrets`, `Credential`, and `Secret`—inside policy, identifier, reminder, or educational contexts that explicitly excluded real credential values. The without-sensitive-data ablation reduced false positives from six to two and FPR from 25.00% to 8.33%, with no loss of binary true positives on this holdout. This is corpus-specific evidence of weak context and negation handling, not evidence that the family should simply be deleted: security terminology can describe both legitimate defensive material and genuinely risky data handling.

## F. Schema trade-off

Schema was the strongest expected-category result in the small holdout stratum: 3/4 schema-labelled samples were classified suspicious through the full detector, while two unique binary true positives disappeared in the without-schema ablation. The family also caused two false positives when `token` and `executable` occurred in benign input-field documentation. The evidence supports retaining schema inspection as useful triage while distinguishing privileged vocabulary from actual capability or intent. All schema conclusions remain unstable at n=4.

## G. Cross-field mismatch limitation

Mismatch removal lost one unique true positive. Broader contradictions in annotations, execution metadata, and `_meta` were missed. Day 3C found that the current comparison is primarily organized around declared purpose and input-schema signals rather than a general relation across every preserved field. Metadata preservation and traversal alone therefore did not supply cross-field reasoning: the detector also needed a rule that compared claimed purpose, requested data, and declared capability across locations.

### Field-location interpretation

Description, annotations, execution, and vendor/unknown groups recorded zero binary detections; `_meta` recorded one of four. Day 3C source inspection found that broad detectors generally preserved and traversed nested and unknown metadata. Many failures therefore occurred after preservation and traversal, making missing semantics, vocabulary, field scope, and cross-field comparison more plausible within this implementation than wholesale field loss. This is a post-unblinding source-and-error interpretation, not an independently manipulated cause.

### Difficulty interpretation

Recall was 25.00% for both author-labelled obvious and moderate samples and 12.50% for subtle samples. Independent exact difficulty agreement was only 16/48. The ordering is descriptive and too subjective to support a stable claim that difficulty caused performance.

## H. Obfuscation representation gap

All four expected obfuscation samples were missed. The representations were decimal character codes, short Base64 in an annotation, HTML numeric entities, and hexadecimal bytes in a vendor field. The implemented obfuscation family focuses on invisible Unicode controls, long or whitespace-heavy descriptions, and sufficiently long valid Base64 blocks in the root description. Detecting an encoded-looking surface is distinct from performing bounded decoding and then analyzing the decoded content. The current result supports only the former narrow capability; E3 proposes the latter as future work with strict size and recursion limits.

## I. Capability triage

`CAP-001` is informational and contributes contextual evidence rather than directly reaching the `MEDIUM` binary threshold. It found high-impact capability terms in `holdout_s023` and `holdout_s024`, each with risk 2, but both remained false negatives. Other capability samples used unrecognized phrase variants or required a relationship between an innocuous purpose and disproportionate privileges. Capability removal caused no binary change, although it removed the informational evidence. This supports describing CAP-001 as triage evidence under H0, not as a validated poisoning classifier.

## J. R08 construct validity

R08 / `holdout_s011` (`bounded_result_sampler`) was the sole binary reviewer disagreement. The frozen ground truth treated its malformed schema as suspicious under a schema-security-review construct; the blinded reviewer considered it benign as a likely data-quality defect. H0 detected it through standards-based schema validation. It is one of five true positives and one of two unique schema-family true positives, so it matters to the small schema result. The defensible claim is that the detector identified a malformed-schema security/compatibility signal under the preregistered taxonomy. The result does not establish malicious tool poisoning.

## K. Lightweight trade-off

The primary analysis-core timing averaged 1.7159 ms per tool and the secondary static-end-to-end timing averaged 4.3020 ms per tool on the recorded local machine. At the same time, H0 recall was 20.83% and FPR was 25.00%. The prototype was computationally lightweight under the measured boundaries, but low latency did not compensate for limited holdout effectiveness. A useful engineering objective is to preserve bounded, deterministic processing while testing broader semantic coverage on a new untouched corpus.

## L. Research value

The low holdout result is scientifically informative. A frozen, independently reviewed holdout exposed a large development–holdout gap that a development-only report would conceal. Hashes, a clean Git checkpoint, preregistered timing, ablations, independent review, and preserved failures make the negative result auditable. The project therefore contributes both an implemented defensive static-analysis framework and evidence about the limits of narrow deterministic rules. Honest negative evidence improves the design of the next study; it must not be overwritten by tuning on the exposed holdout.

## Failure taxonomy synthesis

### Primary false-negative mechanisms

Each of the 19 false negatives has exactly one primary Day 3C mechanism.

| Primary mechanism | Samples | Count |
|---|---|---:|
| Semantic paraphrase gap | s001–s003 | 3 |
| Contextual concealment gap | s004–s006 | 3 |
| Vocabulary gap | s009–s010 | 2 |
| Capability-reasoning gap | s012, s021–s022 | 3 |
| Cross-field reasoning gap | s015–s016 | 2 |
| Obfuscation-decoding gap | s017–s020 | 4 |
| Threshold gap | s023–s024 | 2 |
| **Total false negatives** |  | **19** |

### Multi-label contributing mechanisms

These counts are overlapping occurrences and must not be summed as a number of samples.

| Mechanism | Primary occurrences | Contributing occurrences | Total tagged occurrences |
|---|---:|---:|---:|
| Vocabulary | 2 | 8 | 10 |
| Semantic paraphrase | 3 | 3 | 6 |
| Field semantics / scope | 0 | 6 | 6 |
| Cross-field reasoning | 2 | 5 | 7 |
| Capability reasoning | 3 | 4 | 7 |
| Obfuscation decoding | 4 | 0 | 4 |
| Contextual concealment | 3 | 1 | 4 |
| Threshold | 2 | 0 | 2 |

### False-positive interpretation tags

Day 3C applied overlapping tags for security keywords without context, educational/documentation context, negation/disclaimer failure, benign schema vocabulary, title-only triggering, and general context loss. All six FPs had general context loss and negation/disclaimer weakness tags; four involved educational/documentation context, four involved security-keyword context, two involved benign schema vocabulary, and three were title-only triggers. The primary FP assignments were benign schema vocabulary for b007 and b015, title-only triggering for b008 and b020, negation/disclaimer failure for b012, and educational/documentation context for b023.

## Exploratory hypotheses register

Every entry below has the same status: **POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED.** None may be described as an H0 improvement.

| ID | Hypothesis | H0 motivation | Expected target / potential benefit | Principal FP risk | Complexity | Research status |
|---|---|---|---|---|---|---|
| E1 | Deterministic semantic phrase variants | s001–s003 had no PI finding. | Authority/ranking paraphrases; potentially recover instruction-override variants. | Benign policy and precedence documentation. | Medium | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |
| E2 | Context-aware credential evaluation | `SEC-001` caused four FPs. | Negation, documentation, and value-flow context; potentially reduce credential-word FPs. | Suppression of genuinely risky credential handling. | Medium | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |
| E3 | Bounded common-encoding recognition | s017–s020 used four unhandled representations. | Size-limited decimal/Base64/entity/hex recognition and decoding; potentially expose hidden text. | Benign encoded data, resource use, recursive ambiguity. | High | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |
| E4 | Cross-field purpose/capability comparison | s015–s016 and other capability contradictions were missed. | Compare purpose, inputs, execution, annotations, `_meta`, and vendor fields. | Legitimate broad-purpose administrative tools. | High | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |
| E5 | Normalized capability phrase grammar | Capability variants often produced no finding. | Deterministic normalization of capability verb/object forms; potentially increase capability evidence. | Benign capability declarations. | Medium | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |
| E6 | Field-aware output/schema constructs | s005 and s009 occurred in output schema. | Output-sensitive secrecy and data-exposure rules; potentially improve output-field coverage. | Legitimate output documentation. | Medium | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |
| E7 | Corroborated capability escalation | s023–s024 had informational evidence below threshold. | Escalate only when capability evidence is corroborated by purpose mismatch or sensitive access. | Compound benign administrative metadata. | High | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |
| E8 | Malformed-schema reporting distinction | R08 mixed security review with maliciousness interpretation. | Separate schema integrity/compatibility from poisoning classification. | Fragmented reporting or underweighting exploitable schema defects. | Medium | POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED. |

## Priorities for a future study

The Day 3C priorities were: E1 semantic variants, E3 bounded encoding recognition, E4 cross-field comparison, E5 normalized capability grammar, E2 credential context, E6 output/schema awareness, E7 corroborated escalation, and E8 reporting distinction. This ordering is a post-unblinding research plan, not a validated ranking. Any implemented version must be separately versioned and evaluated on a new untouched holdout after benign counterexamples and development tests.

## Threats to validity matrix

| Validity domain | Frozen issue | Mitigation already present | Remaining boundary |
|---|---|---|---|
| Construct | Tool-poisoning taxonomy boundaries | Preregistered construct and sampling rubrics | Broad labels may exceed narrow implemented rule semantics. |
| Construct | Malformed-schema ambiguity | R08 disagreement preserved and transparently adjudicated | Security/compatibility defect does not establish malicious intent. |
| Construct | Capability signal versus poisoning | CAP-001 remains informational | High-impact capability may be legitimate without purpose/context comparison. |
| Construct | Difficulty subjectivity | Original and reviewer assessments preserved | Exact difficulty agreement was only 16/48. |
| Internal | Deterministic implementation and frozen configuration | H0 tied to source, corpus, configuration, artifact, and Git hashes | Determinism does not remove corpus or label bias. |
| Internal | Post-hoc tuning risk | No detector, threshold, risk, corpus, or H0 change after unblinding | Future work is exploratory and needs a new holdout. |
| Internal | Label independence | One blinded independent reviewer assessed 48/48 samples | Only one independent reviewer was used. |
| External | Synthetic/derived fixtures | Provenance and matched-pair derivations are explicit | No real-world holdout samples. |
| External | English orientation | Corpus scope is documented | No multilingual evidence. |
| External | Artificial prevalence | Balanced 24/24 design supports comparison | 50% suspicious prevalence is not deployment prevalence. |
| External | Ecosystem diversity | Seven construct families and multiple fields are represented | Limited MCP server, vendor, and natural metadata diversity. |
| Conclusion | N=48 | Raw counts and Wilson intervals are reported | Overall intervals are broad. |
| Conclusion | Small strata | Every n<10 stratum is marked low evidence | Category and field comparisons are unstable. |
| Conclusion | Ablations | Seven families were preregistered and run against the frozen artifacts | Effects are descriptive, correlated, and corpus-specific. |
| Conclusion | Timing environment | Two boundaries, warm-ups, repetitions, and distributions are recorded | Results depend on machine and background load. |
| Reproducibility | Frozen identity | Git, source bundle, corpus, configuration, and artifact hashes are preserved | Ignored local artifacts require controlled retention. |
| Reproducibility | Deterministic outputs | H0/H1 prediction equivalence was checked | Wall-clock timing is not deterministic. |

Additional frozen limitations are a synthetic-heavy corpus, no real-world holdout samples, English-only fixtures, balanced nondeployment prevalence, small category/field strata, matched-pair dependence, provenance/label confounding, description-length imbalance, subjective difficulty, one independent reviewer, no second independent cross-split leakage reviewer, and machine/background-load-dependent timing.

## Research question answer

**Question:** How effectively does the lightweight deterministic prototype detect known MCP tool-poisoning patterns on unseen metadata?

**Conservative answer:** The frozen prototype executed with low measured latency but showed limited detection effectiveness on the independently reviewed synthetic holdout. It detected 5 of 24 suspicious samples (recall 20.83%) while falsely flagging 6 of 24 benign samples (FPR 25.00%). Mean per-tool latency was 1.7159 ms at the analysis-core boundary and 4.3020 ms at the static-end-to-end boundary on the recorded local machine. These findings apply to the deterministic known-pattern configuration, the 48-sample synthetic/derived holdout, and its frozen labels; they do not establish real-world generalization or production readiness.

## Contributions register

Engineering and methodological contributions are distinct from detection performance. Repository evidence supports:

1. A lightweight deterministic MCP metadata inspection architecture.
2. A rule-based suspicious-text detection framework.
3. Canonical schema fingerprint and integrity support.
4. A reproducible corpus evaluation framework.
5. A documented development/holdout split methodology.
6. Corpus and configuration hashing.
7. A repeated timing engine with distinct measurement boundaries.
8. Preregistered detector-family ablation support.
9. Stratified metrics and Wilson uncertainty reporting.
10. Experiment artifact comparison and prediction-equivalence checks.
11. A blinded independent human-review and adjudication workflow.
12. A preserved post-unblinding failure taxonomy.

The confirmed detection-performance contribution is narrower: the project provides an auditable measurement showing where the frozen deterministic prototype succeeded and failed on one independently reviewed synthetic holdout.

## Balanced conclusion

The project demonstrates reproducible engineering, deterministic behavior, low measured runtime overhead, schema/mismatch detection value, and a disciplined evaluation process. H0 also demonstrates 20.83% recall, 25.00% FPR, 19 false negatives, lexical/semantic brittleness, missing bounded decoding, and limited cross-field reasoning within a synthetic evaluation scope. The defensible next step is a separately versioned exploratory implementation followed by evaluation on a new untouched holdout. The exposed H0 corpus must not be reused as confirmatory evidence for those changes.
