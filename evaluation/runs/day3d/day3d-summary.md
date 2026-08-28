# Day 3 Master Summary

## Day 3 sequence

| Phase | Purpose | Outcome |
|---|---|---|
| 3A — Pre-unblinding audit | Verify frozen identities, cleanliness, review, protocol, and readiness without detector execution. | Day 3B was authorized only after critical gates passed. |
| 3B — Independent evaluation | Run the single authoritative H0, secondary timing, seven preregistered ablations, and development comparison. | H0 and secondary artifacts were preserved with hashes. |
| 3C — Deep failure analysis | Explain frozen errors without changing detector, corpus, labels, threshold, or H0. | All 19 FNs and 6 FPs were inventoried; descriptive mechanisms and E1–E8 were separated. |
| 3D — Evidence synthesis | Convert frozen results and discussion into thesis/viva evidence. | Seven ignored Markdown evidence files were created; no experiment or source modification occurred. |

## Frozen identities

| Identity | Value |
|---|---|
| Git commit | `a4abee4661522ac13edb37e1b075186a2ccd7a03` |
| H0 experiment | `exp-20260827T060056391880Z-c514ba03-a660fd6d` |
| H0 SHA-256 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` |
| Detector-source bundle SHA-256 | `197f13414a348ff527c27061aee481c2e3d11ca32198441dcfdb77b6ff8bd227` |
| Holdout SHA-256 | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| H0 configuration SHA-256 | `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1` |
| Day 3C SHA-256 | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` |

## Primary H0 result

The full built-in detector at `MEDIUM`, with no custom rules or suppressions, produced TP 5, TN 18, FP 6, and FN 19 on 48 independently reviewed synthetic/derived samples. Accuracy was 47.92%, precision 45.45%, recall 20.83%, F1 28.57%, and FPR 25.00%. Wilson 95% intervals were 34.47–61.67% for accuracy, 9.24–40.47% for recall, and 12.00–44.90% for FPR.

## Runtime result

Analysis-core timing averaged 1.7159 ms/tool (median 1.5354 ms, p95 3.2229 ms; 480 observations). Static-end-to-end timing averaged 4.3020 ms/tool (median 4.0732 ms, p95 6.3104 ms; 240 observations). The boundaries are distinct and machine/background-load dependent. Predictions were equivalent across H0 and H1.

## Development–holdout gap

Development versus holdout changes were accuracy -43.33 pp, precision -44.79 pp, recall -71.67 pp, F1 -62.79 pp, and FPR +15.00 pp. The largest gap was recall. This is a descriptive within-project comparison and not a population generalization estimate.

## Dominant observations

- **False negatives:** 17/19 had no finding and risk 0; only 2 were informational findings below threshold. The largest mutually exclusive primary group was obfuscation-decoding at 4/19, while vocabulary and semantic-scope tags overlapped broadly in Day 3C.
- **False positives:** `SEC-001` caused 4/6 binary FPs through credential/security vocabulary in benign policy, documentation, reminder, or identifier contexts. `SCH-002` caused 2/6 through benign privileged-looking schema words.
- **Strongest observed family:** Schema had the strongest small expected-category result (3/4 binary detections) and lost two unique TPs when removed, while also causing two FPs. R08 materially qualifies this result.
- **Weakest observed binary contributions:** Injection, concealment, obfuscation, and capability removals made no binary difference on this corpus. Capability still contributed informational findings in two below-threshold FNs.

## Research conclusion

The lightweight deterministic prototype ran with low measured local latency but had limited holdout effectiveness. It detected 5/24 suspicious samples and falsely flagged 6/24 benign samples. The project nevertheless provides a strong reproducible engineering and evaluation framework: static bounded inspection, stable identities, independent review, repeated timing, ablation, stratification, uncertainty, artifact comparison, and transparent failure analysis. These contributions must be reported separately from detection performance.

No real-world generalization or production-readiness claim is supported. The corpus is synthetic/derived, English-oriented, balanced at 50% suspicious, small overall and within strata, partly matched-pair dependent, and reviewed by one independent reviewer.

## Future exploratory direction

E1–E8 cover deterministic semantic variants, credential context, bounded common-encoding recognition, cross-field purpose/capability comparison, normalized capability grammar, output/schema awareness, corroborated capability escalation, and a malformed-schema reporting distinction. Every proposal is **POST-UNBLINDING EXPLORATORY HYPOTHESIS — NOT VALIDATED.** A changed detector must be separately versioned and evaluated against a new untouched, independently reviewed holdout.

## Scientific status

- H0 effectiveness: **PREREGISTERED / CONFIRMATORY**.
- H1 and seven planned ablations: **PREREGISTERED / CONFIRMATORY within the experiment design**, with descriptive corpus-specific interpretation.
- Day 3C failure taxonomy: **POST-UNBLINDING DESCRIPTIVE ANALYSIS**.
- E1–E8: **POST-UNBLINDING EXPLORATORY HYPOTHESES — NOT VALIDATED**.

The authoritative H0 result has not been replaced, rerun, or modified during Day 3D. No detector, source, test, corpus, label, threshold, risk, or authoritative experiment artifact was changed.
