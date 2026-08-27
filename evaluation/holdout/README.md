# Independent holdout corpus

## Purpose and completed blindness boundary

This directory contains inert static MCP tool metadata for the research question: “How effectively does the lightweight deterministic prototype detect known MCP tool-poisoning patterns on unseen metadata?” It evaluates known tool-poisoning construct detection, not general maliciousness or runtime behavior.

**STATUS — FIRST EXPERIMENT COMPLETED 2026-08-27.** The original prohibition on prediction-producing access was honored through the frozen v0.2 H0 run. The corpus is now exposed and must not be described or reused as an unseen confirmatory holdout for modified detectors. Any later use is explicitly post-unblinding exploratory analysis; a new confirmatory claim requires a fresh untouched holdout.

Version 1.0.1 is the independently reviewed holdout used for the completed first evaluation. Its final corpus SHA-256 is `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8`. The original v0.2 H0 and later v0.3 post-unblinding exploratory evidence are preserved with hashes and scientific status in `evaluation/runs/README.md`.

## Sampling rubric

- Planned size: 48 tools, balanced as 24 benign and 24 suspicious.
- Difficulty: eight benign and eight suspicious samples at each of `obvious`, `moderate`, and `subtle`.
- Suspicious category coverage: instruction override, concealment, sensitive-data request, schema abuse, capability mismatch, obfuscation, and capability indicators.
- Field coverage: root description, nested input schema, output schema, annotations, `_meta`, execution metadata, and preserved vendor/unknown text.
- Benign controls: ordinary metadata plus security, administration, prompt-safety education, credentials documentation, transparency, hidden-field terminology, and quiet/silent terminology without a poisoning instruction.
- Matched design: eight benign/suspicious pairs. Pairs share a broad task context but differ in the presence of the poisoning construct. Wording and structures are not exact copies.
- Provenance: repository-authored synthetic fixtures, with the suspicious member of each matched pair marked `derived` from its benign counterpart. All transformations are metadata-only and inert.
- Language: English only for version 1.0.1; this limitation must be retained in reporting.

The authoring rubric was defined before fixtures were written. Authors must reason from the construct definitions below and must not test wording against detector implementation or output.

Independence is limited and stated narrowly: the holdout was constructed as a separate batch without running detectors or seeing predictions, but the construction operator had prior project and taxonomy context. It is not a double-blind, externally authored dataset. The fixtures are concept-driven rather than rule-ID-driven. One independent reviewer subsequently reviewed all samples while blinded to original labels and detector predictions.

## Labeling rubric

### Suspicious

A suspicious sample contains metadata intended to influence an agent, conceal relevant activity, request or expose unrelated sensitive material, create a suspicious schema/capability mismatch, obscure security-significant text, or declare high-impact agent capabilities requiring review. The fixture represents the construct as inert text or data only. A suspicious label means “contains a known tool-poisoning/security-review construct,” not “is proven malicious.”

### Benign

A benign sample contains no such agent-directed poisoning construct, even when it mentions secrets, authentication, passwords, tokens, hidden data, prompts, instructions, security policies, administrative operations, or quiet behavior. Security-related vocabulary alone is not suspicious.

### Categories

Use only the existing taxonomy:

- `instruction_override`: metadata asserts priority over user/system/conversation guidance or attempts to control agent selection/behavior.
- `concealment`: metadata asks that relevant tool activity or consequences be withheld from the user/operator.
- `sensitive_data`: metadata requests, exposes, or routes sensitive material unrelated to the advertised purpose.
- `schema`: malformed, excessively permissive, or unexpectedly privileged schema content warrants review.
- `mismatch`: name/description and actual fields or declared operations materially disagree.
- `obfuscation`: security-significant content is deliberately made low-salience or difficult to inspect.
- `capability`: metadata declares high-impact file, execution, network, database, credential, or destructive capabilities warranting review.

Multi-label samples record every construct that is independently present. Categories describe ground-truth constructs and are not chosen to force a particular rule ID; `expected_rule_ids` is intentionally empty throughout this holdout.

## Difficulty rubric

- `obvious`: a human reviewer can identify a direct and explicit construct without relying on surrounding context.
- `moderate`: the construct appears in plausible operational wording or a less prominent metadata field and requires contextual reading.
- `subtle`: the construct is implicit, low-salience, or distributed across purpose and metadata, but still satisfies the labeling definition.

Difficulty is assigned before any prediction and reflects human interpretive difficulty, not anticipated detector success.

## Field-location rubric

Every suspicious entry records the actual path containing the principal poisoning/security-review construct. Paths are checked against the referenced raw tool object. A multi-label sample may still have one principal path when the constructs co-occur in that field. Benign samples use an empty location list because they have no expected poisoning-bearing field.

## Provenance and safety

- `synthetic`: independently authored for this holdout without claiming an external source.
- `derived`: the suspicious member of a declared matched pair, transformed from its named benign holdout counterpart solely by changing inert metadata.
- `real_world`: not used in version 1.0.1; no public or private service was contacted.

No sample contains a real credential, personal data, proprietary material, executable payload, operational exploit, live URL dependency, or tool invocation. All examples are repository-authored and distributed under the project MIT license.

## Review process

Corpus-level `label_review_status` is `independently_reviewed`. One independent human reviewer assessed all 48 binary labels, categories, field locations, difficulties, and rationales without original labels or detector output. The reviewer agreed on 47 binary labels, disagreed on one malformed-schema sample, and abstained on none. Reviewer classifications total 25 benign and 23 suspicious; the original submitted summary's 24/24 arithmetic is preserved and corrected in `review-ledger.md`.

R08 / `holdout_s011` remains suspicious after adjudication under the pre-existing malformed-schema security-review rubric. The reviewer benign judgment, confidence, rationale, and ambiguity remain preserved. Original difficulty labels also remain unchanged; reviewer difficulty agreed on 16/48 and is recorded separately. This is single-reviewer evidence, not multi-expert consensus.

The review/freeze checkpoint, Day 3A audit, and first H0 evaluation are complete. The original H0 bytes remain immutable; Day 5 remediation does not relabel, modify, or retune this corpus.

Construction and review evidence is retained in `integrity-report.json`, `near-duplicate-review.md`, `coverage-report.md`, `review-ledger.md`, and `reviewer-source.md`. Those files contain corpus identity, human judgments, and descriptive design checks only; prediction and performance evidence is preserved separately under `evaluation/runs/`.
