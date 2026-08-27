# Holdout coverage and confounding assessment

## Status and method

This report describes independently reviewed holdout 1.0.1 before detector unblinding. It was generated using typed structural loading, manifest counting, raw field-path existence checks, generic text/shape comparison, and human-review records only. No detector, rule matcher, scanner, evaluator, prediction, finding, or risk calculation was run.

The construction operator had prior project and taxonomy context. “Holdout” therefore means a separately authored, prediction-unexposed batch, not a double-blind external corpus. One independent reviewer assessed all 48 samples while blinded to original labels and detector predictions; this does not constitute multi-expert annotation.

- Final corpus SHA-256: `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8`
- Samples: 48
- Label status: `independently_reviewed`
- Benign/suspicious: 24/24
- Difficulty: 16 obvious, 16 moderate, 16 subtle; each label contributes eight to every difficulty
- Multi-label suspicious samples: 5
- Matched benign/suspicious pairs: 8, with exactly two members in each of P01–P08
- Binary review: 47 agreements, 1 disputed and adjudicated-retained original label, 0 abstentions
- Reviewer classifications: 25 benign, 23 suspicious; the preserved source summary's 24/24 total is an arithmetic error
- Missing required sample metadata: 0 IDs, files, selected tool names, source types, labels, rationales, difficulties, provenance records, or notes
- Missing suspicious ground truth: 0 category lists and 0 field-location lists; all 24 benign location lists are intentionally empty
- Expected rule IDs: intentionally empty for all 48 samples to avoid authoring against rule-specific phrases

## Suspicious construct coverage

Counts overlap for multi-label samples and therefore do not sum to 24.

| Category | Obvious | Moderate | Subtle | Total |
|---|---:|---:|---:|---:|
| capability | 2 | 2 | 2 | 6 |
| concealment | 1 | 2 | 1 | 4 |
| instruction_override | 1 | 1 | 1 | 3 |
| mismatch | 2 | 1 | 1 | 4 |
| obfuscation | 1 | 1 | 2 | 4 |
| schema | 1 | 2 | 1 | 4 |
| sensitive_data | 1 | 2 | 1 | 4 |

All seven planned construct categories are present. Category strata are small (`n < 10`) and must be treated as descriptive, low-evidence secondary results after unblinding.

No category is confined to a single principal field group. Capability spans four groups, concealment four, instruction override three, mismatch four, obfuscation four, schema three, and sensitive data four. This reduces exact category/field coupling, although individual cells contain only one to three samples.

## Poisoning-bearing field coverage

All 24 suspicious samples have at least one declared field location, all 24 declared paths resolve in the referenced raw tool object, and benign samples correctly have no expected poisoning-bearing path.

| Principal field group | Samples |
|---|---:|
| root `description` | 4 |
| `inputSchema` | 5 |
| `outputSchema` | 3 |
| `annotations` | 3 |
| `_meta` | 4 |
| `execution` | 3 |
| preserved vendor/unknown fields | 2 |

## Provenance and authoring coverage

| Provenance | Benign | Suspicious | Total |
|---|---:|---:|---:|
| synthetic | 24 | 16 | 40 |
| derived | 0 | 8 | 8 |
| real_world | 0 | 0 | 0 |

The eight derived samples are the suspicious members of the declared matched pairs. No external source was contacted and no third-party, private, credential, or proprietary material is present. The corpus is English-only and entirely repository-authored, so it cannot establish real-world, cross-ecosystem, or multilingual generalization.

Authoring batches are distributed across eight benign themes and eight suspicious themes. The largest batches are `benign-security` (6), `benign-administrative` (5), and `suspicious-multilabel` (5); no single catalog file or batch contains a majority of either label.

## Confounding assessment

The following observable design differences must accompany any later interpretation:

- Provenance is label-confounded: all eight `derived` samples are suspicious. Provenance is research metadata rather than detector input, so it cannot directly influence predictions, but provenance-stratified performance would be uninterpretable as an independent label comparison.
- Root descriptions are longer for benign samples: benign mean 105.3 characters and median 106, versus suspicious mean 56.3 and median 44. Across all normalized string content the gap is smaller and reverses only slightly: benign mean 233.3 characters versus suspicious mean 214.0. Length-stratified error review is required after unblinding; length must not be used to relabel or remove samples.
- Category and principal-field groups contain few samples. Apparent group differences will have high uncertainty and must not be ranked as strong evidence.
- The balanced 50% suspicious prevalence is intentional for metric estimation and does not represent MCP ecosystem prevalence. Precision is prevalence-dependent and must not be generalized to deployment without recalibration.
- Eight matched pairs improve local contrast but reduce independence among observations. Report ordinary sample-level metrics as specified, while describing pairwise behavior as exploratory rather than treating pairs as 16 unrelated task contexts.
- Catalog placement is partly aligned with difficulty (catalogs 01–02 obvious, 03–04 moderate, 05–06 subtle). File order must not be treated as a predictive feature; evaluation ordering remains sample ID ascending.
- Generic document-frequency review found no security-bearing phrase repeated across most suspicious samples. The most common non-schema suspicious words occur in five or fewer of 24 samples. Benign negations such as “not” occur in four samples and may themselves be a weak label cue, so phrase-specific conclusions must remain exploratory.
- One independent reviewer produced very high binary agreement (47/48; Cohen's kappa 0.9583), but this is not multi-expert consensus and does not establish external validity.
- Difficulty agreement was only 16/48 (33.3333%); reviewer difficulty was 22 obvious, 19 moderate, and 7 subtle versus the original balanced 16/16/16. Difficulty must be reported as subjective, and original/reviewer values must remain separate.
- R08 exposes a construct-boundary ambiguity: malformed schema is included in the frozen security-review taxonomy but is not, by itself, proof of adversarial poisoning. Its retained disagreement must accompany any category-level interpretation.

No coverage or review result justifies changing the frozen detector configuration. Any later corpus change requires a documented version decision, a new corpus hash, and repeated integrity/near-duplicate checks before evaluation.
