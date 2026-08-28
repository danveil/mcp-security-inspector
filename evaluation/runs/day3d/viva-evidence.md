# Day 3D Viva Evidence

Use exact counts first, then state scope and limitations. H0 is preregistered/confirmatory; Day 3C explanations are post-unblinding descriptive; E1–E8 are unvalidated future-work hypotheses.

## Core questions

### Q1. Why did development accuracy exceed 90% while holdout accuracy was below 50%?

Development accuracy was 91.25%, while holdout accuracy was 47.92%; recall fell from 92.50% to 20.83%. Day 3C found that many holdout samples used paraphrases, contextual narratives, cross-field relations, and encoded representations outside the narrow rule grammars. This is evidence of a corpus-specific transfer gap and possible lexical/semantic over-specialization, not proof of population-level overfitting.

### Q2. Does this mean the project failed?

No, but the detection claim must be narrow. H0 showed limited effectiveness: 5/24 suspicious samples detected and 6/24 benign samples flagged. The project still delivered a deterministic static-analysis architecture, reproducible evaluation, frozen identities, timing, ablation, stratification, independent review, and an honest failure taxonomy. Its value includes learning precisely where the prototype is insufficient.

### Q3. Why did you not modify the detector after seeing H0?

Changing rules, thresholds, or labels after unblinding would tune to the test evidence and invalidate H0 as an independent checkpoint. H0 was therefore preserved byte-for-byte. Improvements are separated as exploratory hypotheses and require a new untouched holdout.

### Q4. Why is the holdout no longer reusable for confirmatory evaluation?

Its outcomes, false positives, false negatives, strata, and ablation effects are now known and directly motivated E1–E8. Reusing it to validate those changes would introduce feedback from test data into model development. It remains useful for descriptive regression, not as independent confirmatory evidence.

### Q5. Why use deterministic rules instead of an LLM?

The project prioritizes local, reproducible, bounded static analysis that never invokes tools or sends hostile catalog content to a model. Deterministic rules provide stable IDs, explainable evidence, fixed resource controls, and low latency. H0 also demonstrates the trade-off: narrow rules can be semantically brittle.

### Q6. What does “lightweight” mean in your project?

It refers to bounded local static analysis and measured runtime, not high accuracy. Mean per-tool latency was 1.7159 ms at analysis-core and 4.3020 ms static-end-to-end on the recorded machine. The claim is qualified by timing boundaries and environment dependence.

### Q7. Why were obfuscation samples missed?

The four samples used decimal character codes, short Base64 in annotations, HTML numeric entities, and hexadecimal vendor metadata. The frozen detector focuses on invisible Unicode, unusually long/whitespace-heavy descriptions, and long valid Base64 in root descriptions. General bounded decoding was not implemented.

### Q8. Why did SEC-001 generate false positives?

It matched `Password`, `secrets`, `Credential`, and `Secret` in benign policy, identifier, reminder, and educational contexts. The rule recognized security vocabulary but did not fully incorporate negation, documentation intent, or whether secret values were actually requested or returned. Four of six H0 FPs came from this rule.

### Q9. What did the ablation study show?

On this corpus, removing schema lost two TPs, removing mismatch lost one TP, and removing sensitive data removed four FPs without changing TPs. Injection, concealment, obfuscation, and capability removal caused no binary change; capability did remove informational findings. These are preregistered within-design observations, not universal causal importance scores or validated redesigns.

### Q10. What is the significance of R08?

R08 / `bounded_result_sampler` was the only binary reviewer disagreement. Frozen ground truth treated malformed schema as suspicious under the preregistered schema-security construct; the reviewer saw a likely data-quality defect. It was an H0 TP and materially affects the small schema result. It supports a schema-integrity finding, not proof of malicious intent.

### Q11. What would you improve next?

The frozen evidence motivates deterministic phrase variants, context-aware credential handling, bounded encoding recognition, cross-field purpose/capability comparison, normalized capability grammar, output-aware rules, corroborated capability escalation, and a separate schema-integrity reporting class. All are post-unblinding exploratory hypotheses, not validated improvements.

### Q12. How would you evaluate an improved version fairly?

Version and freeze the revised detector, add suspicious and benign development tests, preregister configuration and metrics, construct and independently review a new untouched holdout, hash every identity, then run one authorized primary evaluation. The current exposed holdout can be used only for descriptive regression.

### Q13. Can this system be deployed as production MCP security?

Not on the current evidence. Recall was 20.83% and FPR 25.00% on a small synthetic/derived holdout, with no real-world deployment study. It is a research prototype and can support explainable triage, but production protection would require broader validation and layered controls.

### Q14. What is the strongest contribution of the project?

The strongest defensible contribution is the reproducible research and engineering framework: bounded deterministic inspection, stable findings, frozen corpus/config/source identities, independent review, repeated timing, ablation, uncertainty, artifact comparison, and transparent negative-result analysis.

### Q15. What is the most important limitation?

The most important empirical limitation is poor transfer to the independent holdout: only 5/24 suspicious samples were detected. The most important scope limitation is that the 48 samples are synthetic/derived and do not establish real-world performance.

## Potential examiner challenges

### “If your recall is only 20.83%, why is this useful?”

It is not sufficient as a standalone detector. It remains useful as an explainable bounded prototype, a reproducible evaluation platform, and evidence identifying specific coverage gaps. The honest result prevents unsupported deployment claims and creates a defensible next-study design.

### “Is your 91.25% development accuracy evidence of overfitting?”

The 71.67-point recall drop is consistent with over-specialization to development vocabulary, but this experiment did not isolate causality. I therefore report a development–holdout transfer gap and use “overfitting” only as a qualified interpretation.

### “Why should malformed schema count as tool poisoning?”

It should not automatically imply maliciousness. The preregistered taxonomy treated malformed schema as a schema-security-review signal; R08 exposes construct ambiguity. A future version should distinguish schema integrity/compatibility from poisoning classification.

### “Why is your corpus synthetic?”

Synthetic inert metadata enabled controlled constructs, matched pairs, safe distribution, and reproducibility without invoking tools or exposing private data. The trade-off is external validity; the report explicitly makes no real-world generalization claim.

### “Why is one independent reviewer sufficient?”

One blinded reviewer materially improves on author-only labels and produced 47/48 binary agreement, but it is not sufficient for strong label-validity claims. The limitation is frozen and reported; a larger study should use multiple independent reviewers and formal adjudication.

### “Could your false positives make the system unusable?”

A 25.00% FPR on this balanced holdout is substantial and would create triage burden. Deployment usability was not tested. The result motivates context-aware rules and operational validation, but those changes are unvalidated.

### “Why not simply use an LLM classifier?”

An LLM could broaden semantics but adds nondeterminism, prompt-injection exposure, data-governance questions, cost, and reproducibility challenges. A fair comparison would require a separate protocol. The deterministic approach deliberately tests how far bounded local rules can go; H0 documents its limits.

### “How do you know the latency measurements are reliable?”

The plan fixed two boundaries, excluded warm-ups, used 10 and 5 measured repetitions, and recorded observation counts, mean, median, p95, min, max, and standard deviation. H0/H1 predictions were equivalent. The numbers are reproducible records for one local environment, not hardware-independent guarantees.

### “Did you tune anything after seeing the holdout?”

No. H0, source, corpus, labels, threshold, risk configuration, and Day 3C report identities remained frozen. Day 3D created only ignored synthesis documents. E1–E8 are explicitly post-unblinding exploratory hypotheses.

### “Why should I trust a negative result?”

The evaluation used an exact Git checkpoint, frozen detector-source/corpus/configuration identities, a preserved H0 artifact hash, an independently reviewed holdout, raw counts, uncertainty intervals, and preregistered secondary analyses. The low performance is preserved rather than edited, which is the central integrity safeguard.

### “Which result should appear in the abstract?”

Use H0, not development performance: 20.83% recall, 25.00% FPR, and low measured latency on the 48-sample independently reviewed synthetic/derived holdout. State that real-world generalization and production readiness were not established.
