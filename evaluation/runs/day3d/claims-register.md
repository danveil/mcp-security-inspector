# Day 3D Claims Register

Claims are scoped to the frozen repository commit, artifacts, and 48-sample independently reviewed synthetic/derived holdout. H0 is **PREREGISTERED / CONFIRMATORY**; failure explanations are **POST-UNBLINDING DESCRIPTIVE**; E1–E8 are **POST-UNBLINDING EXPLORATORY HYPOTHESES — NOT VALIDATED**.

## Supported claims

| Claim | Evidence | Qualification | Source artifact / section |
|---|---|---|---|
| The frozen detector achieved 20.83% recall on the 48-sample independently reviewed synthetic holdout. | TP 5, FN 19; 5/24 = 20.83%. | Applies to the frozen full configuration at `MEDIUM`. | H0 `confusion_matrix`, `metrics`; `results-evidence.md` §3. |
| The H0 false-positive rate was 25.00%. | FP 6, TN 18; 6/24 = 25.00%. | Balanced synthetic/derived corpus; not deployment prevalence. | H0; `results-evidence.md` §3. |
| H0 contained 19 false negatives and 6 false positives. | Preserved H0 error arrays and confusion matrix. | Binary classification errors under the preregistered threshold. | H0; `results-evidence.md` §§10–11. |
| Seventeen of nineteen H0 false negatives produced no finding. | 17 error records have no finding/risk 0; s023–s024 have informational `CAP-001`. | Mechanical observation; cause is interpreted separately. | H0 `false_negatives`; Day 3C §Failure inventory. |
| H0 and H1 produced equivalent predictions for all 48 samples. | Preserved comparison performed in Day 3B. | Timing boundaries differ; latency values are not equivalent. | H0/H1 artifacts; `results-evidence.md` §5. |
| The without-schema ablation lost two true positives and the without-mismatch ablation lost one. | H0 TP=5; without-schema TP=3; without-mismatch TP=4. | Descriptive, corpus-specific family removal. | Ablation artifacts; `tables.md` Tables 12–13. |
| `SEC-001` caused four of six binary false positives in H0. | b008, b012, b020, b023 trigger `SEC-001`. | Does not establish its real-world FP rate or justify deletion. | H0 `false_positives`; `results-evidence.md` §11. |
| The holdout evaluation was tied to frozen corpus and configuration hashes. | Corpus SHA `c514…a2d8`; config SHA `a660…f9a1`; H0 SHA `3307…1b80`. | Reproducibility identity, not external validity. | H0 metadata; Day 3B inventory. |

## Supported with qualification

| Claim | Evidence | Required qualification | Source artifact / section |
|---|---|---|---|
| The prototype is computationally lightweight under the measured local methodology. | Mean 1.7159 ms/tool analysis-core and 4.3020 ms/tool static-end-to-end. | Machine/background-load dependent; boundaries differ; no service-level or throughput guarantee. | H0/H1 `timing`; `results-evidence.md` §5. |
| Development performance did not transfer to the independent holdout. | Recall -71.67 pp and F1 -62.79 pp from development to H0. | Describes these corpora; does not estimate population generalization. | Development result and H0; `results-evidence.md` §6. |
| The results are consistent with lexical or semantic brittleness. | 17/19 FNs had no finding; Day 3C maps paraphrase/vocabulary/context gaps. | Post-unblinding interpretation, not a randomized causal conclusion. | Day 3C §§Failure taxonomy, Detector-family analysis. |
| Schema provided the strongest observed category-level detection. | 3/4 schema-labelled suspicious samples were classified suspicious; removal lost 2 TPs. | n=4, multi-label binary grouping; one TP is reviewer-disputed R08. | H0 strata/ablations; Day 3C §§Schema, Reviewer disagreement. |
| The sensitive-data family was the largest observed FP source. | Four of six binary FPs; removal reduced FP from 6 to 2. | Corpus-specific; removal was not validated as an improved detector. | H0 and without-sensitive-data artifact. |
| CAP-001 acts as contextual triage evidence in H0. | s023–s024 received informational findings/risk 2 but no binary classification. | Description of the frozen scoring behavior, not a universal capability. | H0 false negatives; Day 3C §Capability. |
| The evaluation process is reproducible. | Frozen Git, detector-source, corpus, configuration, and artifact hashes; deterministic predictions. | Wall-clock timings remain environment dependent; ignored artifacts need preserved storage. | Day 3B inventory; H0 metadata; `discussion-evidence.md` validity matrix. |
| The independent review provides useful label assurance. | 48/48 reviewed blind to original labels/predictions; 47 agreements, one disagreement, no abstentions. | Only one independent reviewer; difficulty agreement 16/48; disagreement preserved. | Holdout `review-ledger.md`, `reviewer-source.md`. |

## Not supported

| Claim | Evidence gap | Qualification / acceptable replacement | Source artifact / section |
|---|---|---|---|
| The detector generalizes to real-world MCP servers. | No real-world holdout samples or representative server sampling. | Say “on this independently reviewed synthetic/derived holdout.” | `discussion-evidence.md` threats matrix. |
| The detector provides production-grade protection. | Recall 20.83%, FPR 25.00%; no deployment or operational validation. | Describe it as a research prototype and static-analysis framework. | H0; `discussion-evidence.md` research-question answer. |
| The detector detects most tool-poisoning attacks. | It detected 5/24 suspicious holdout samples. | State the observed known-pattern scope and exact count. | H0 confusion matrix. |
| Any E1–E8 change will improve unseen performance. | No implementation or new untouched evaluation exists. | Label each proposal post-unblinding exploratory and unvalidated. | Day 3C §Improvement hypotheses; `discussion-evidence.md`. |
| The family ablations measure universal causal importance. | Single small, correlated synthetic corpus; removal effects are configuration dependent. | Call them preregistered within-design, descriptive, corpus-specific contribution analyses. | Seven ablation artifacts. |
| Difficulty caused the observed errors. | Difficulty is subjective and exact reviewer agreement was 16/48. | Report descriptive difficulty strata only. | H0 strata; review ledger. |

## Prohibited / misleading claims

| Claim | Why misleading | Correct formulation | Source artifact / section |
|---|---|---|---|
| “The detector achieved 91% accuracy overall.” | 91.25% was development-corpus accuracy; H0 holdout accuracy was 47.92%. | Report development and holdout separately. | `results-evidence.md` §6. |
| “The independent holdout was real-world.” | It was predominantly repository-authored synthetic/derived metadata. | “Independently reviewed synthetic/derived holdout.” | Holdout manifest/README. |
| “Removing sensitive-data detection improved the validated model.” | The ablation was not a newly validated model, and the exposed holdout cannot confirm a post-hoc change. | “Within this ablation, removal reduced four FPs with no TP change.” | Without-sensitive-data artifact; Table 13. |
| “The schema family detected malicious intent in R08.” | R08 is a malformed-schema construct with reviewer disagreement; the finding establishes schema invalidity/security-review signal, not intent. | Preserve the construct-validity distinction. | Day 3C §Reviewer disagreement. |
| “Zero ablation effect means a detector family has no value.” | Zero binary change on one corpus can coexist with informational findings or value on other data. | State the exact within-corpus binary delta. | Ablation artifacts; Day 3C family analysis. |
| “The experiment proves the detector is fast and accurate.” | It observed low local latency but limited H0 effectiveness; “proves” overstates evidence. | Report both timing boundaries and H0 metrics with scope. | H0/H1; research-question answer. |
| “The holdout can confirm E1–E8 after implementation.” | It has been exposed and used to motivate those hypotheses. | Use a new untouched holdout for confirmatory evaluation. | Day 3C/3D scientific-status map. |

## Register rule

Any statement about performance must identify the corpus/split and configuration. Any statement based on Day 3C must be called post-unblinding descriptive. Any prospective detector change must be called **POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED.**
