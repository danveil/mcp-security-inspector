# v0.3 Exploratory Performance Comparison

## Methodology

The exposed holdout contains 48 static tools. The `analysis-core` run used 3 warm-ups and 10 measured repetitions per sample (480 observations). The `static-end-to-end` run used 1 warm-up and 5 measured repetitions (240 observations). Warm-ups were excluded. Repetitions returned identical findings and risk. No MCP tool, command, network endpoint, metadata URL, or model was invoked.

Environment recorded by the artifact:

- Python 3.12.13
- Windows 11
- `httpx2 2.12.0`
- `jsonschema 4.26.0`
- `mcp 2.1.1`
- `pydantic 2.13.4`
- `PyYAML 6.0.3`
- `rich 14.3.4`
- `typer 0.27.1`

The worktree was intentionally dirty with Day 4B source changes. The application still reports package version 0.2.0 because Day 4C does not authorize a version bump.

## Historical reference versus current observation

| Boundary/statistic | v0.2 H0 reference | v0.3 exploratory | Absolute difference | Day 4A guardrail | Result |
|---|---:|---:|---:|---:|---|
| Analysis-core mean ms/tool | 1.7159 | 1.5531 | -0.1628 | ≤3.4318 | PASS |
| Analysis-core p95 ms | 3.2229 | 2.1840 | -1.0389 | ≤6.4458 | PASS |
| Static-end-to-end mean ms/tool | 4.3020 | 3.4837 | -0.8183 | ≤8.6040 | PASS |
| Static-end-to-end p95 ms | 6.3104 | 4.0936 | -2.2168 | reference only | PASS/reference |

The v0.3 analysis-core median was `1.4924 ms`, minimum `1.0284`, maximum `3.4112`, and population standard deviation `0.3914`. Static median was `3.4439 ms`, minimum `2.9068`, maximum `4.8987`, and standard deviation `0.3761`.

The observed timing is lower than the historical reference, but the difference must not be attributed to detector efficiency: wall-clock results vary with machine state, caching, Python execution, and background load. The defensible conclusion is only that this campaign stayed within the frozen exploratory guardrails.

## Security-boundary confirmation

Focused representation and OBF tests reconfirmed:

- exactly one decode depth;
- 512-character input and output limits;
- four candidates per field and 32 per tool;
- 4,096 retained decoded characters per tool;
- strict UTF-8 byte decoding;
- 90% printable-text threshold;
- NUL/control, malformed, binary, and invalid-padding rejection;
- inert evidence/redaction behavior;
- no execution, network, filesystem retrieval, metadata replacement, recursion, decompression, or arbitrary codec guessing.

All 42 focused tests passed. The full 417-test suite passed with 93.17% coverage, along with Ruff, format check, strict mypy, and `git diff --check`. Day 4B build and clean-wheel smoke results remain applicable because Day 4C made no source correctness change.
