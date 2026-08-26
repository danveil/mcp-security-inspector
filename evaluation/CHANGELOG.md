# Evaluation corpus changelog

## [Unreleased]

- Declared corpus 1.0.0 as the development/regression split without changing any sample content or ground-truth label.
- Added corpus methodology, single-reviewer status, and synthetic source/license-policy metadata.
- Added backward-compatible typed support for provenance, normalized difficulty, and expected field locations.
- Added deterministic corpus hashing and development/holdout exact-overlap validation.
- Baseline remains TP 37, TN 36, FP 4, and FN 3.

## [1.0.0] - 2026-08-25

- Added 40 benign and 40 suspicious harmless static MCP metadata samples.
- Added explicit binary/category ground truth, rationale, difficulty, and optional expected rule IDs.
