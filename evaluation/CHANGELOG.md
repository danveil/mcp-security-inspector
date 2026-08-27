# Evaluation corpus changelog

## [Unreleased]

- Added a separate post-unblinding 36-sample v0.3 exploratory development set with 18 benign hard negatives and 18 suspicious construct cases for `PI-002`, `HID-002`, `SEC-002`, `MIS-002`, and `OBF-005`; it is not a confirmatory holdout.
- Confirmed no duplicate IDs or exact canonical content overlap between the bundled development corpus and the v0.3 exploratory fixture set.
- Preserved the bundled development baseline at TP 37, TN 36, FP 4, and FN 3 after the exploratory P0 detector changes.
- Declared corpus 1.0.0 as the development/regression split without changing any sample content or ground-truth label.
- Added corpus methodology, single-reviewer status, and synthetic source/license-policy metadata.
- Added backward-compatible typed support for provenance, normalized difficulty, and expected field locations.
- Added deterministic corpus hashing and development/holdout exact-overlap validation.
- Constructed a separate 48-sample candidate holdout corpus 1.0.0 with balanced labels and difficulties, explicit provenance, expected categories, and poisoning-bearing field paths.
- Recorded detector-free cross-split integrity, preliminary near-duplicate review, coverage, and confounding checks. At construction time the holdout remained unreviewed and unevaluated.
- Baseline remains TP 37, TN 36, FP 4, and FN 3.

## [Holdout 1.0.1] - 2026-08-27

- Preserved all 48 decisions from one blinded independent reviewer and corrected only the source report's summary arithmetic from 24/24 to the actual 25 benign / 23 suspicious judgments.
- Recorded 47 binary agreements, one disagreement, no abstentions, 97.9167% raw agreement, and Cohen's kappa 0.9583 without running the detector.
- Retained `holdout_s011` as suspicious under the pre-existing malformed-schema security-review rubric while preserving the reviewer's benign judgment and ambiguity.
- Preserved original difficulty labels separately from reviewer difficulty; exact difficulty agreement was 16/48.
- Set corpus review status to `independently_reviewed`, incremented the corpus version, and updated the final corpus hash without changing any tool fixture or detector behavior.

## [1.0.0] - 2026-08-25

- Added 40 benign and 40 suspicious harmless static MCP metadata samples.
- Added explicit binary/category ground truth, rationale, difficulty, and optional expected rule IDs.
