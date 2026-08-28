# Day 4C Failure-Recovery Map

## Original 19 false negatives

| Original FN | Day 3C primary mechanism | v0.3 result | Recovered | Responsible P0 rule | Finding below MEDIUM? | Explanation |
|---|---|---|---|---|---|---|
| `holdout_s001` | Semantic paraphrase | Benign; no finding; risk 0 | No | — | No | Semicolon separates the governing-directive object from the later yield relation, so the local PI-002 concept gate is incomplete. |
| `holdout_s002` | Semantic paraphrase | Benign; no finding; risk 0 | No | — | No | “Rank guidance ahead” is reached, but “surrounding conversation” does not satisfy the required guidance target grammar. |
| `holdout_s003` | Semantic paraphrase | Suspicious; risk 19 | Yes | `PI-002` | No | Annotation authority claim is matched with exact path `annotations.routingHint`. |
| `holdout_s004` | Contextual concealment | Suspicious; risk 19 | Yes | `HID-002` | No | “Keep its existence out of the user-facing...” supplies omission, material existence, and observer context. |
| `holdout_s005` | Contextual concealment | Benign; no finding; risk 0 | No | — | No | The inflected “omitting” form is outside the fixed omission grammar. |
| `holdout_s006` | Contextual concealment | Benign; no finding; risk 0 | No | — | No | “Outside the operator-visible account” lacks the required fixed omission relation. |
| `holdout_s009` | Vocabulary gap | Benign; no finding; risk 0 | No | — | No | Private recovery-phrase output remains outside SEC vocabulary/action semantics. |
| `holdout_s010` | Vocabulary gap | Benign; no finding; risk 0 | No | — | No | Unrestricted `processTemplate` remains outside schema/capability vocabulary. |
| `holdout_s012` | Capability reasoning | Benign; no finding; risk 0 | No | — | No | Structured capabilities are present, but the purpose is not in the narrow-purpose list and no approved MIS-002 corroborator fires. |
| `holdout_s015` | Cross-field reasoning | Suspicious; risk 13 | Yes | `MIS-002` | No | Annotation database mutation conflicts with display-only purpose and retains both paths. |
| `holdout_s016` | Cross-field reasoning | Benign; no finding; risk 0 | No | — | No | “Write ... to a database” and “post ... to an external service” fall outside the exact structured capability forms. |
| `holdout_s017` | Obfuscation decoding | Benign; no finding; risk 0 | No | — | No | Decimal codes decode to `hide the action`, but decoded text lacks observer/disclosure context required by the semantic gate. |
| `holdout_s018` | Obfuscation decoding | Benign; no finding; risk 0 | No | — | No | Base64 decodes to source-authored `auxiliary step omutted`; it does not satisfy a high-risk decoded grammar. |
| `holdout_s019` | Obfuscation decoding | Benign; no finding; risk 0 | No | — | No | Entities decode to `withholdnotice`; raw separator loss and absence of a material-operation object prevent the semantic gate. |
| `holdout_s020` | Obfuscation decoding | Benign; no finding; risk 0 | No | — | No | Hex decodes to `keep it out of view`, but the pronoun does not satisfy the material-object grammar. |
| `holdout_s021` | Capability reasoning | Benign; no finding; risk 0 | No | — | No | Capabilities are partly normalized, but the separate no-confirmation field is not a local corroborator and purpose is not narrow. |
| `holdout_s022` | Capability reasoning | Suspicious; risk 13 | Yes | `MIS-002` | No | Metadata deletion and compound capabilities contradict the preview purpose. |
| `holdout_s023` | Threshold gap | Suspicious; risk 15 | Yes | `MIS-002` plus `CAP-001` | No | Cross-field contradiction supplies a MEDIUM finding; CAP-001 remains informational. |
| `holdout_s024` | Threshold gap | Suspicious; risk 15 | Yes | `MIS-002` plus `CAP-001` | No | Vendor capability contradiction supplies a MEDIUM finding without promoting CAP-001. |

## Recovery by primary Day 3C mechanism

| Mechanism | Original FNs | Recovered | Remaining | Recovery rate |
|---|---:|---:|---:|---:|
| Semantic paraphrase gap | 3 | 1 | 2 | 33.33% |
| Contextual concealment gap | 3 | 1 | 2 | 33.33% |
| Vocabulary gap | 2 | 0 | 2 | 0.00% |
| Capability-reasoning gap | 3 | 1 | 2 | 33.33% |
| Cross-field reasoning gap | 2 | 1 | 1 | 50.00% |
| Obfuscation-decoding gap | 4 | 0 | 4 | 0.00% |
| Threshold gap | 2 | 2 | 0 | 100.00% |

## Original six false positives

| Original FP | H0 rule | v0.3 findings | Resolved | New finding | Scoped context/negation outcome |
|---|---|---|---|---|---|
| `holdout_b007` | `SCH-002` | `SCH-002` on schema `token`; risk 11 | No | No | SEC scope is irrelevant; P1 schema context was intentionally not implemented. |
| `holdout_b008` | `SEC-001` | `SEC-001` on description `password`; risk 10 | No | No | “Without accepting” and a separate boolean safety declaration remain outside the scoped benign grammar. |
| `holdout_b012` | `SEC-001` | `SEC-001` + `SEC-002`; risk 23 | No | Yes, `SEC-002` | Coordinated `neither requested nor returned` negation is not recognized and the FP is amplified. |
| `holdout_b015` | `SCH-002` | `SCH-002` on negated `executable`; risk 11 | No | No | P1 schema negation was intentionally deferred. |
| `holdout_b020` | `SEC-001` | `SEC-001` + `SEC-002`; risk 23 | No | Yes, `SEC-002` | Reminder/title context remains insufficient; noun “output” is interpreted as an action despite “never includes.” |
| `holdout_b023` | `SEC-001` | `SEC-001` on description `secret`; risk 10 | No | No | Educational/placeholder safety evidence across fields does not suppress the unsafe lexical occurrence. |

Scoped credential context resolved zero of the four known SEC-001 FPs. It added no new binary FP because all four were already false positives, but it increased benign risk materially on `b012` and `b020`.

## New-error audit

- Original TP to new FN: none.
- Original TN to new FP: none.
- Original correct sample with an unnecessary new P0 finding: none.
- Original FP with unnecessary new P0 evidence/risk: `b012` and `b020`.
- Original FP resolved: none.
- New FP introduced: none.
- Previously correct sample broken: none.
