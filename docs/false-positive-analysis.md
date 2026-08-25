# False-positive and false-negative analysis

Heuristic metadata inspection must infer risk from short, context-poor text. Words such as “password,” “silently,” “administrator,” and “ignore” occur in both legitimate documentation and suspicious model-directed instructions. A false positive is therefore not necessarily a broken rule; it is evidence that the rule needs context or analyst review.

For every binary error, `mcpsec evaluate` records the sample ID, expected and predicted labels, risk score, complete typed findings, rule IDs, fields, evidence excerpts, explanations, and recommendations. Category confusion matrices expose errors that a single binary score can hide.

## Corpus 1.0.0 observations

The current five false positives are deliberately retained:

- `benign_027`: the generic schema property `record` is interpreted as a database capability and mismatches a missing-field reader (`MIS-001`).
- `benign_028`: “silently” describes a user-enabled accessibility operation but triggers concealment (`HID-001`).
- `benign_030`: privacy redaction “suppress disclosure” is mistaken for hiding activity (`HID-001`).
- `benign_031`: a quoted attack phrase used in safety training triggers instruction override (`PI-001`).
- `benign_035`: a harmless encoded-looking documentation fixture triggers `OBF-004`.

The three false negatives are also retained:

- `suspicious_036`: extreme whitespace triggers low-severity `OBF-003`, below the default medium binary threshold.
- `suspicious_038` and `suspicious_039`: declared high-impact permissions trigger informational `CAP-001`, which provides context but is not a maliciousness verdict.

These cases show why category results and evidence should accompany binary metrics. Automatically raising all capability findings would improve recall on this corpus but would also classify many legitimate administration tools as suspicious. Likewise, suppressing every quoted phrase could miss a genuinely active instruction embedded in quoted text.

## Rule-adjustment procedure

1. Reproduce the error and confirm the ground truth independently.
2. Identify the smallest explainable context distinction.
3. Estimate the effect on both recall and precision; never optimize one metric alone.
4. Add a counterexample for the intended behavior.
5. Run the complete corpus and unit suite.
6. Record material rule or ground-truth changes in the relevant changelog and bump the rule-pack or corpus version.

Justified suppressions are appropriate for locally reviewed, stable exceptions. They should not be used in baseline research evaluation because they can conceal detector errors; evaluation requires explicit `--suppressions` and records that state.
