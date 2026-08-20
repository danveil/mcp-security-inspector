# Contributing

1. Open an issue describing the detector, compatibility fix, or documentation change.
2. Create a focused branch and keep generated reports, baselines, credentials, and `.env` files out of commits.
3. Add false-positive and true-positive tests for detector changes.
4. Run `ruff check .`, `ruff format --check .`, `mypy src`, and `pytest`.
5. Document the rule's rationale, benign triggers, and review guidance.

Detectors must be deterministic, offline, non-executing, and bounded. Do not add `eval`, `exec`, dynamic imports from input, arbitrary subprocesses, metadata URL fetching, telemetry, or unbounded regex patterns. Test fixtures must be artificial and inert.

