# Day 3D Figure Specifications

These are reproducible design specifications, not generated figures. All plots must label the holdout as independently reviewed and synthetic/derived, retain zero-valued groups, and cite the frozen source artifacts.

## Figure 1 — Development versus holdout effectiveness

- **Research purpose:** Show the descriptive transfer gap between the development corpus and frozen H0.
- **Exact source data:** `tables.md`, Table 6; development {accuracy 91.25%, precision 90.24%, recall 92.50%, F1 91.36%}; holdout {47.92%, 45.45%, 20.83%, 28.57%}.
- **X-axis:** Accuracy, precision, recall, F1.
- **Y-axis:** Percentage, fixed 0–100%.
- **Grouping:** Two adjacent bars per metric: development and independent holdout.
- **Caption:** *Development and independent-holdout effectiveness under their frozen evaluations; the holdout contained 48 independently reviewed synthetic/derived samples.*
- **Interpretation boundary:** This is a within-project descriptive comparison, not a population generalization estimate or proof of a single causal mechanism.
- **Avoid:** Truncated y-axis, 3-D bars, omitting the holdout scope, mixing FPR into the same “higher is better” scale, or calling development accuracy overall performance.

## Figure 2 — Holdout confusion matrix

- **Research purpose:** Make the 5 TP, 19 FN, 18 TN, and 6 FP distribution unambiguous.
- **Exact source data:** H0 `confusion_matrix`; `tables.md`, Table 2.
- **X-axis:** Predicted suspicious, predicted benign.
- **Y-axis:** Actual suspicious, actual benign.
- **Grouping:** 2×2 heatmap with raw count annotations and explicit TP/FN/FP/TN labels.
- **Caption:** *Confusion matrix for the full built-in detector at the MEDIUM threshold on the 48-sample holdout.*
- **Interpretation boundary:** Counts describe this balanced holdout; the apparent cell proportions do not represent deployment prevalence.
- **Avoid:** Reversing axes without labels, using percentages without raw counts, color scales that hide 19 FN, or normalizing rows and then labeling values as counts.

## Figure 3 — Expected-category detection proportions

- **Research purpose:** Compare overall binary detection across the seven expected suspicious categories.
- **Exact source data:** `tables.md`, Table 7: instruction override 0/3; concealment 0/4; sensitive data 2/4; schema 3/4; mismatch 1/4; obfuscation 0/4; capability 0/6.
- **X-axis:** Expected category.
- **Y-axis:** Detected proportion, fixed 0–100%.
- **Grouping:** One bar per category; annotate every bar with `detected/n` and `n<10`.
- **Caption:** *Binary detection proportion by expected category; multi-label samples contribute to each applicable category and all groups have low evidence.*
- **Interpretation boundary:** This uses overall binary classification, not family-specific `category_metrics`; tiny and overlapping groups are descriptive only.
- **Avoid:** Ranking without sample sizes, confidence-looking smooth curves, removing zero bars, treating categories as independent, or claiming schema superiority beyond this corpus.

## Figure 4 — Field-location detection proportions

- **Research purpose:** Display where suspicious evidence was located and how often its sample crossed the binary threshold.
- **Exact source data:** `tables.md`, Table 8: description 0/4; input schema 3/5; output schema 1/3; annotations 0/3; `_meta` 1/4; execution 0/3; vendor/unknown 0/2.
- **X-axis:** Aggregated expected field family.
- **Y-axis:** Detected proportion, fixed 0–100%.
- **Grouping:** One bar per field family with TP/FN labels.
- **Caption:** *Binary detection by expected metadata field family on the frozen holdout; every field stratum contains fewer than ten samples.*
- **Interpretation boundary:** Field grouping does not by itself distinguish traversal, rule scope, vocabulary, or cross-field reasoning.
- **Avoid:** Presenting tiny groups as stable estimates, omitting `vendor/unknown`, or treating zero detection as proof that the loader discarded the field.

## Figure 5 — Ablation F1 comparison

- **Research purpose:** Show corpus-specific F1 after each preregistered family removal.
- **Exact source data:** H0 28.57%; without injection 28.57%; concealment 28.57%; sensitive data 32.26%; schema 19.35%; mismatch 23.53%; obfuscation 28.57%; capability 28.57%. Source: preserved ablation JSON files and `tables.md`, Table 12.
- **X-axis:** Full and seven family-removal configurations.
- **Y-axis:** F1 percentage, fixed 0–100%.
- **Grouping:** One bar per configuration; full H0 visually distinguished but not exaggerated.
- **Caption:** *F1 under the full detector and seven preregistered family-removal ablations on the same frozen holdout.*
- **Interpretation boundary:** Higher ablated F1 is not validation of a detector improvement and does not justify post-hoc family deletion; effects are correlated and corpus-specific.
- **Avoid:** Truncated y-axis, causal “importance” labels, hiding equal bars, or labeling the without-sensitive-data result as a new primary model.

## Figure 6 — False-negative primary mechanisms

- **Research purpose:** Summarize the mutually exclusive Day 3C primary classifications for all 19 FNs.
- **Exact source data:** `tables.md`, Table 14: semantic paraphrase 3; contextual concealment 3; vocabulary 2; capability reasoning 3; cross-field reasoning 2; obfuscation decoding 4; threshold 2.
- **X-axis:** Primary failure mechanism.
- **Y-axis:** False-negative count, fixed integer scale starting at zero.
- **Grouping:** One bar per primary mechanism; label total `n=19` and scientific status “post-unblinding descriptive.”
- **Caption:** *Primary post-unblinding failure mechanism assigned to each of the 19 H0 false negatives.*
- **Interpretation boundary:** Primary assignments are analytical classifications, not preregistered causal findings; overlapping contributing tags belong in a separate table.
- **Avoid:** Adding multi-label counts to the 19 primary cases, pie-chart precision unsupported by the small n, or presenting taxonomy labels as validated causal mechanisms.

## Figure 7 — Runtime latency summary

- **Research purpose:** Compare latency distributions at the two preregistered timing boundaries without implying boundary equivalence.
- **Exact source data:** H0 analysis-core {n=480, min 0.9188, median 1.5354, mean 1.7159, p95 3.2229, max 5.8537 ms}; H1 static-end-to-end {n=240, min 3.0328, median 4.0732, mean 4.3020, p95 6.3104, max 7.5676 ms}. Raw timing observations are not stored individually, so a true histogram/violin plot cannot be reconstructed from these summaries.
- **X-axis:** Timing boundary.
- **Y-axis:** Milliseconds per tool, starting at zero.
- **Grouping:** Summary-range plot with min–max whisker and separate median, mean, and p95 markers; annotate observation counts and repetition counts.
- **Caption:** *Recorded per-tool runtime summaries for analysis-core (3 warm-ups, 10 measured repetitions) and static-end-to-end (1 warm-up, 5 measured repetitions) on the local evaluation machine.*
- **Interpretation boundary:** The boundaries include different work; timings are machine/background-load dependent and are not throughput or production-service guarantees.
- **Avoid:** Fabricated distributions, box plots without quartiles, joining summary markers into a trend line, or merging both boundaries into one average.
