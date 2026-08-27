# Detector-free near-duplicate and leakage review

## Boundary

This is a construction-author review of development corpus 1.0.0 against final reviewed holdout 1.0.1. The author had prior project and taxonomy context, so this is not an external blind leakage review. It used canonical structural loading, exact normalized-content hashing, generic character-sequence similarity, token-set Jaccard similarity, and value-stripped JSON shape comparison. It did not import or run detectors, inspect predictions, calculate findings or risk, or use rule-specific patterns. Independent label review was completed separately; it did not claim a second cross-split leakage analysis.

## Exact checks

- Development identity: `a22de0126d2cf0b00c99ded46687b70dc6f417382a0a11c5ae4a9cad8f6d6f47`, 80 samples
- Final holdout identity: `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8`, 48 samples
- Duplicate sample IDs: none
- Exact normalized content across splits: none
- Exact full value-stripped object shapes across splits: none
- Machine-readable integrity result: `integrity-report.json`, with empty `errors` and `warnings`

## Highest generic text similarities

These are screening statistics, not semantic leakage scores. Character similarity can be high for short generic descriptions even when the security-bearing metadata and object structures differ.

| Development | Holdout | Description sequence | All-text sequence | Token Jaccard | Review |
|---|---|---:|---:|---:|---|
| suspicious_031 | holdout_s008 | 0.648 | 0.386 | 0.179 | Generic “format/display” greeting wording; holdout construct is elsewhere in `_meta` and is not copied. |
| suspicious_030 | holdout_s022 | 0.586 | 0.321 | 0.087 | Short display-task wording only; distinct task and metadata shape. |
| benign_037 | holdout_s013 | 0.579 | 0.325 | 0.121 | Both use caller-supplied/read wording; distinct image/environment-map context. |
| benign_002 | holdout_s023 | 0.541 | 0.351 | 0.059 | Generic conversion phrasing; different domain and capability metadata. |
| suspicious_032 | holdout_s019 | 0.538 | 0.258 | 0.100 | Short “create/format” text; distinct policy and preserved-metadata structure. |
| suspicious_032 | holdout_s009 | 0.531 | 0.290 | 0.120 | Generic creation verb only; distinct recovery/output-schema context. |
| benign_012 | holdout_b020 | 0.523 | 0.340 | 0.116 | Both are intentionally benign credential-policy controls, but wording and schemas are independently authored. |
| benign_005 | holdout_s010 | 0.521 | 0.315 | 0.114 | Incidental read/preview wording; unrelated calendar and schema-migration tasks. |
| benign_037 | holdout_s016 | 0.519 | 0.388 | 0.097 | Caller-supplied content wording; distinct translation/execution metadata. |
| suspicious_039 | holdout_b016 | 0.511 | 0.430 | 0.133 | Shared database/permission vocabulary used as an intentional benign hard negative; no copied sentence or structure. |

The maximum observed description sequence similarity is 0.648, maximum all-text sequence similarity among the listed candidates is 0.430, and maximum token Jaccard among the top 20 candidates is 0.200. Manual inspection found no copied poisoning phrase, encoded payload, complete schema, or attack template across the split boundary.

## Internal matched pairs and template risk

P01–P08 are intentional within-holdout contrasts and are declared in provenance and the review ledger. Each pair shares only a broad task context; the suspicious member changes inert metadata to introduce the target construct. These pairs are not cross-split leakage, but later reporting must acknowledge their dependence.

Repeated catalog envelopes (`tools` arrays and ordinary JSON Schema scaffolding) are required by the MCP metadata format. Full shape comparison found no exact development/holdout match, while manual inspection found no holdout fixture copied wholesale from a development fixture. Short generic verbs such as “format,” “display,” “preview,” and “supplied” recur across ordinary tool descriptions and are not treated as substantive duplication.

## Decision

Decision: no sample requires removal or rewriting for cross-split duplication. Adjudication changed review metadata but did not change any tool fixture, wording, label, category, field path, or difficulty, so the manual content judgments remain applicable. The lack of a second independent cross-split leakage reviewer remains a documented limitation. Repeat all checks if any fixture or research-relevant manifest field changes.
