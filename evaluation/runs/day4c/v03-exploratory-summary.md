# v0.3 Post-Unblinding Exploratory Summary

Scientific status: **POST-UNBLINDING EXPLORATORY HOLDOUT RESULT**. This is not H0 v2, independent validation, a new holdout, or confirmatory evidence.

## Frozen inputs

- Git HEAD: `a4abee4661522ac13edb37e1b075186a2ccd7a03`; Day 4B worktree intentionally dirty.
- Original v0.2 H0 SHA-256: `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80`.
- Day 3C SHA-256: `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f`.
- v0.3 P0 IDs: `PI-002`, `HID-002`, `SEC-002`, `OBF-005`, and `MIS-002`.
- Threshold: `MEDIUM`; `CAP-001` remains informational; no custom rules or suppressions.
- No detector, severity, threshold, risk, corpus, or suppression change was made during Day 4C.

## Separate regression results

| Dataset | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Existing development | 37 | 36 | 4 | 3 | 91.25% | 90.24% | 92.50% | 91.36% | 10.00% |
| New exploratory fixtures | 18 | 18 | 0 | 0 | 100.00% | 100.00% | 100.00% | 100.00% | 0.00% |

These datasets were not pooled. The authored exploratory fixture result measures intended-mechanism coverage only.

## POST-UNBLINDING EXPLORATORY HOLDOUT RESULT

| Version | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Frozen v0.2 H0 | 5 | 18 | 6 | 19 | 47.92% | 45.45% | 20.83% | 28.57% | 25.00% |
| Frozen v0.3 exploratory | 11 | 18 | 6 | 13 | 60.42% | 64.71% | 45.83% | 53.66% | 25.00% |

The paired change is `+6 TP`, `0 TN`, `0 FP`, and `-6 FN`. Recovered original FNs are `holdout_s003`, `holdout_s004`, `holdout_s015`, `holdout_s022`, `holdout_s023`, and `holdout_s024`. No original TP or TN changed to an error. No original FP was resolved.

## Mechanism interpretation

- `PI-002` recovered one of three original instruction-priority misses (`s003`).
- `HID-002` recovered one direct contextual-concealment miss (`s004`).
- `MIS-002` recovered four cases across annotations, metadata, execution, vendor data, and below-threshold capability context (`s015`, `s022`, `s023`, `s024`).
- `SEC-002` recovered no holdout FN and added misleading MEDIUM findings to benign `b012` and `b020`, increasing each risk score from 10 to 23.
- `OBF-005` recovered all four authored encoded fixtures but none of the four encoded holdout misses. The representations decoded, but the decoded semantic gate did not qualify them.
- Thirteen suspicious samples still have no finding at all; none of the remaining FNs is merely below MEDIUM.

## Performance and reproducibility

- Analysis-core: three warm-ups, ten measurements, 480 observations, mean `1.5531 ms/tool`, p95 `2.1840 ms`.
- Static-end-to-end: one warm-up, five measurements, 240 observations, mean `3.4837 ms/tool`, p95 `4.0936 ms`.
- Both boundaries are below the Day 4A engineering guardrails.
- Environment: Python 3.12.13, Windows 11, `httpx2 2.12.0`, `jsonschema 4.26.0`, `mcp 2.1.1`, `pydantic 2.13.4`, `PyYAML 6.0.3`, `rich 14.3.4`, and `typer 0.27.1`.

## Quality and security

- Focused OBF/representation tests: 42 passed.
- Full suite: 417 passed; coverage 93.17%.
- Ruff, format check, strict mypy, and `git diff --check`: passed.
- The Day 4B package build and clean-wheel smoke were reused because Day 4C made no source correctness change.
- Depth one, strict UTF-8, printable threshold, candidate/input/output/retained-text bounds, inert evidence, and no-execution/no-network behavior remain enforced.

## Recommendation

**B. Accept with documented limitations.**

The implementation is suitable as a v0.3 exploratory candidate because it preserves development behavior, passes all safety/quality gates, remains within performance guardrails, recovers six old FNs, and introduces no new binary error on the exposed set. Acceptance must carry the unchanged 25% FPR, two amplified benign SEC risks, zero exposed-set OBF recovery, thirteen no-finding FNs, synthetic/English-heavy evidence, and complete post-unblinding status. Do not bump the package version during Day 4C.

## Day 4D input

- Accepted candidate mechanisms: scoped local context infrastructure; narrow PI-002/HID-002 coverage; path-preserving capability extraction; corroborated MIS-002; bounded inert representation decoding as a safety architecture.
- Unresolved mechanisms: coordinated SEC negation/title/document context; decoded-text semantic qualification; recovery-phrase/process-template vocabulary; uncorroborated capability combinations; remaining PI/HID paraphrases.
- Fresh-holdout requirements: new authors, independent blinded label review, balanced benign hard negatives, representation variants with independently authored decoded semantics, aligned administrator/simulation counterexamples, nested-field balance, frozen corpus/config/source hashes, and one preregistered evaluation.
- Contamination risks: do not reuse Day 3 holdout text, Day 3 failure sentences, Day 4 exploratory fixtures, known v0.3 trigger wording, or v0.3 predictions during construction or adjudication.
- Candidate confirmatory question: *At the preregistered MEDIUM threshold, does frozen v0.3 improve recall over frozen v0.2 without increasing false-positive rate on a newly authored, independently reviewed, untouched MCP metadata holdout?*

THE V0.3 HOLDOUT RESULT IS POST-UNBLINDING EXPLORATORY EVIDENCE.

THE ORIGINAL V0.2 H0 REMAINS THE ONLY CONFIRMATORY RESULT FROM THAT HOLDOUT.

NO DETECTOR TUNING WAS PERFORMED AFTER OBSERVING THE V0.3 HOLDOUT RESULT.

IMPROVED GENERALIZATION, IF ANY, HAS NOT YET BEEN INDEPENDENTLY CONFIRMED.
