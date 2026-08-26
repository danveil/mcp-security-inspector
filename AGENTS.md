# AGENTS.md

## Purpose

MCP Tool Security Inspector performs deterministic defensive static analysis of MCP tool metadata. It must never invoke scanned tools, execute metadata, download metadata-linked resources, or send catalog content to a model.

## Architecture

- `src/mcpsec/loader.py` and `resource_policy.py`: bounded hostile-input handling
- `src/mcpsec/normalizer.py`: NFC normalization, alias validation, and typed tool definitions
- `src/mcpsec/detectors/` and `rules/`: built-in detectors and data-only custom rules
- `src/mcpsec/risk.py`: deterministic, capped risk calculation
- `fingerprint.py`, `baseline.py`, and `compare.py`: canonical hashes and drift
- `src/mcpsec/retrieval.py`: explicit loopback-only MCP `tools/list` transport
- `src/mcpsec/evaluation/`: corpus validation and metrics
- `src/mcpsec/reporter.py` and `cli.py`: inert output and CLI coordination

## Commands

```powershell
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
python -m pytest --cov=mcpsec --cov-report=term-missing
python -m build
python scripts/smoke_wheel.py dist/<wheel-file>.whl
```

If `.venv\Scripts\python.exe --version` fails, recreate the virtual environment before using the helper scripts.

## Security invariants

- Treat names, descriptions, schemas, annotations, metadata, rules, suppressions, baselines, and server responses as hostile data.
- Static analysis remains the default; never invoke tools or start supplied commands.
- Retrieval remains opt-in and loopback-only at the HTTP transport layer; do not enable redirects or environment proxies.
- Reject inputs over resource limits and conflicting aliases; never silently truncate or discard security-significant content.
- Preserve deterministic finding order, canonical hashes, risk caps, and stable rule IDs.
- Render hostile terminal text literally and neutralize spreadsheet formulas.
- Keep custom configuration data-only; do not introduce executable expressions or user-controlled regular expressions.

## Testing expectations

- Add a regression test for every correctness or security fix.
- Detector changes require suspicious cases and benign counterexamples, followed by corpus evaluation.
- Record intentional corpus/rule metric changes in documentation and the changelog.
- Do not delete meaningful tests or weaken resource limits to make checks pass.

## Definition of done

Ruff lint/format, strict mypy, the full coverage-gated suite, corpus evaluation, wheel build, and clean installed-wheel smoke test all pass. Documentation and security claims must match enforced behavior, and generated environments/build artifacts must remain untracked.
