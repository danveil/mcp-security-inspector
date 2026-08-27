# Changelog

All notable changes follow Keep a Changelog conventions and semantic versioning.

## [Unreleased]

### Added

- Post-unblinding exploratory `PI-002`, `HID-002`, `SEC-002`, `MIS-002`, and bounded depth-one `OBF-005` detector rules
- Structured, path-preserving high-impact capability signals and a 36-sample v0.3 exploratory development fixture set
- Central resource policy for JSON/YAML/baseline sizes, structure nodes, text, tool counts, pagination, rule fields/patterns, and YAML aliases/nodes
- Real loopback transport regression coverage for IPv4, IPv6, redirects, proxy variables, request destinations, and response bytes
- Packaged demonstration catalog and clean-wheel CLI smoke-test script
- Field-aware instruction-override and concealment inspection across nested MCP metadata
- Typed development/holdout corpus metadata, provenance, difficulty migration, expected field locations, and label-review status
- Semantic corpus/configuration SHA-256 identities, Git/runtime experiment metadata, and exact cross-split overlap checks
- Structured evaluation failure classes and a documented holdout isolation and post-unblinding research protocol
- Repeatable analysis-core and static-end-to-end evaluation timing with explicit warm-up boundaries and dispersion statistics
- Evaluation-only detector-family and stable rule-ID ablation presets with exact configuration identities
- Wilson uncertainty intervals, transparent stratified metrics, authoritative run preservation, and paired experiment comparison
- A pre-registration-style experiment-plan template and short-lived CI evaluation artifact retention

### Changed

- Package identity is now `0.3.0a1`, marking the accepted post-unblinding exploratory detector candidate rather than a final release
- Sensitive-data, instruction-priority, and concealment matching now use scoped local context and negation while retaining the bundled development confusion matrix
- Oversized security-significant strings and keys are rejected instead of silently truncated
- Identical alias pairs remain compatible while conflicting or null/non-null alias pairs are rejected
- Rename inference now requires a unique one-to-one component signature and calculates current fingerprints once
- Educational instruction-injection quotations are excluded unless they continue with a direct action
- Corpus 1.0.0 regression result is now TP 37, TN 36, FP 4, FN 3 (F1 91.36%, FPR 10.00%)

### Fixed

- `mcpsec demo` now works from an installed wheel without relying on the source checkout
- `scan --output` writes terminal-format reports instead of silently ignoring the destination
- CLI error and comparison output consistently escape hostile Rich markup
- Windows helper scripts report stale virtual environments explicitly

### Security

- Representation decoding is limited to four explicit formats, strict UTF-8, depth one, fixed candidate/output/count/retained-text budgets, and inert evidence rendering
- MCP retrieval now uses a dedicated transport that validates every destination as loopback, disables redirects, ignores proxy environment variables, and caps cumulative wire bytes and pages
- Policy, suppression, baseline, and static catalog inputs now have explicit resource-exhaustion boundaries

## [0.2.0] - 2026-08-25

### Added

- Versioned 80-sample synthetic metadata corpus and validated ground-truth manifest
- Shared evaluation engine with binary/category metrics, confusion matrices, FP/FN evidence, reproducibility metadata, and timing statistics
- `mcpsec evaluate` terminal, JSON, and CSV experiments
- Lightweight rule-pack name/version metadata with legacy rule-file compatibility
- Safe-loaded, justified, optional tool-scoped suppressions
- Opt-in localhost/loopback MCP SDK `tools/list` retrieval with timeout, tool-count, byte-size, and normalization limits
- Evaluation methodology, false-positive analysis, risk-scoring documentation, and v0.2 audit

### Changed

- Extracted scanning from CLI presentation into a shared engine used by static scan and evaluation
- Expanded the harmless sample server with an explicit localhost Streamable HTTP mode
- Added a backward-compatible baseline format version as a future integrity-envelope migration point
- CI now validates the bundled corpus with an offline evaluation run

### Fixed

- Equivalent duplicate findings no longer inflate category risk; the strongest confidence-adjusted rule/category contribution wins deterministically

### Security

- Normalization rejects metadata deeper than 64 levels and key collisions introduced by Unicode normalization
- Retrieval rejects non-loopback endpoints, URL credentials/fragments, invalid tool metadata, duplicate names, oversized responses, excessive tool counts, pagination cursor loops, and timeouts
- Evaluation applies no suppressions unless explicitly requested and records suppression state

## [0.1.0] - 2026-08-13

### Added

- Static MCP tool loading, normalization, canonicalization, and SHA-256 fingerprints
- Privacy-conscious baselines and field-level drift comparison
- Seven modular detector families and strict data-only custom rules
- Explainable capped risk scoring
- Rich terminal, JSON, CSV, and SARIF reporting with redaction
- CLI severity thresholds, examples, local safe server, documentation, tests, and CI
