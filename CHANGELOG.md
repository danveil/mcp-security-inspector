# Changelog

All notable changes follow Keep a Changelog conventions and semantic versioning.

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

- Normalization rejects metadata deeper than 64 levels and key collisions introduced by Unicode normalization or key-length bounds
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
