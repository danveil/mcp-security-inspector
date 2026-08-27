# Evaluation run artifacts

Use this directory for authoritative local JSON artifacts created by:

```bash
mcpsec evaluate evaluation/corpus/manifest.json --format json --runs-dir evaluation/runs
```

Generated artifacts are ignored by default because they can be numerous and environment-specific. Three specifically allowlisted files are the immutable evidence archive for the completed Day 3/Day 4 study and must never be regenerated, normalized, or overwritten:

| Evidence | Scientific status | SHA-256 |
|---|---|---|
| `exp-20260827T060056391880Z-c514ba03-a660fd6d.json` | Original v0.2 H0; first confirmatory evaluation of holdout 1.0.1 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` |
| `day3c-deep-failure-analysis.md` | Post-unblinding failure-analysis report for H0 | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` |
| `day4c/post-unblinding-exploratory-holdout-full-analysis-core.json` | v0.3 post-unblinding exploratory comparison on the already exposed holdout | `d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b` |

The repository's `.gitattributes` marks all three evidence files as non-text so Git never changes their original line endings. The Day 4C artifact's metadata is authentic and intentionally unchanged: it reports application version `0.2.0`, commit `a4abee4661522ac13edb37e1b075186a2ccd7a03`, and `dirty=true`. It was produced from the uncommitted v0.3 exploratory implementation before the package-version and built-in-rule-pack-version corrections. Those provenance limitations mean it is exploratory evidence, not a cleanly reproducible confirmatory result. The current loader validates the artifact from its recorded schema/configuration and recorded rule sets rather than falsely treating it as a current-registry artifact.

The holdout corpus remains under `evaluation/holdout/`; these files are results and analysis, not a new corpus. Future generated runs remain ignored unless a later research protocol explicitly selects and hashes them for preservation.
