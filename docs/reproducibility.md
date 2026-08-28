# Reproducibility guide

## Frozen identities

- Public alpha package: `0.3.0a1`
- Built-in rule pack: `2.0.0`
- Alpha engineering checkpoint: `0651313cb9fe650f3004e849de7d14000343cacf`
- v0.3 exploratory detector checkpoint: `b1a5d4c92797f630a5aed8b19dec3da21085fa76`
- Independently reviewed holdout checkpoint: `a4abee4661522ac13edb37e1b075186a2ccd7a03`
- Holdout corpus SHA-256: `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8`

Authoritative preserved evidence:

| Artifact | Status | SHA-256 |
|---|---|---|
| `evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json` | Original v0.2 H0 confirmatory artifact | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` |
| `evaluation/runs/day3c-deep-failure-analysis.md` | Post-unblinding H0 failure analysis | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` |
| `evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json` | v0.3 exposed-holdout exploratory artifact | `d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b` |

These files are historical evidence. Do not regenerate, normalize, or overwrite them.

## LF-safe clone and byte preservation

On Windows, a global `core.autocrlf=true` setting was observed to convert
unprotected research files to CRLF during an ordinary clone. The content looked
equivalent, but the byte-sensitive reviewer identity and semantic corpus hashes
changed. Use an LF-preserving clone for recovery and research verification:

```powershell
git clone -c core.autocrlf=false https://github.com/danveil/mcp-security-inspector.git
Set-Location mcp-security-inspector
git config --get core.autocrlf
```

The expected repository-local value in that recovery clone is `false`. The
scoped `.gitattributes` rules also protect the known frozen corpus, reviewer,
and selected historical-evidence paths from checkout conversion. They do not
normalize or rewrite the preserved Git blobs. Do not run broad renormalization
commands over historical research files. If a hash differs, first verify HEAD,
Git status, attributes, and line-ending policy; do not update the expected hash
to match a transformed checkout.

## Development evaluation

Install the development environment, then evaluate only the development manifest:

```bash
python -m pip install -e ".[dev]"
mcpsec evaluate evaluation/corpus/manifest.json
mcpsec evaluate evaluation/corpus/manifest.json --format json --output development-result.json
```

The expected development regression confusion matrix is TP 37, TN 36, FP 4, FN 3. Development results are not independent accuracy estimates.

## Detector-free corpus integrity

The existing holdout may be checked for identity and cross-split integrity without running detector logic:

```bash
mcpsec corpus-check evaluation/corpus/manifest.json evaluation/holdout/manifest.json
```

Do not evaluate the exposed holdout as if it were fresh validation evidence.

## Inspecting and comparing preserved artifacts

Artifact inspection and comparison load existing evidence without rescanning the corpus:

```bash
mcpsec compare-experiments \
  evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json \
  evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json
```

The expected compatibility status is `comparable_with_warning` because the artifacts record different detector configurations and the authentic Day 4C artifact records a dirty worktree. That warning is provenance evidence, not corruption.

For scientific interpretation and limitations, read the [public research status](research-status.md), [v0.3 exploratory checkpoint](v0.3-exploratory-checkpoint.md), and [evaluation methodology](evaluation-methodology.md).
