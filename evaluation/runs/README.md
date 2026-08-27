# Evaluation run artifacts

Use this directory for authoritative local JSON artifacts created by:

```bash
mcpsec evaluate evaluation/corpus/manifest.json --format json --runs-dir evaluation/runs
```

Generated `*.json` files are ignored by Git because they can be numerous and environment-specific. Preserve selected immutable artifacts in controlled research storage, record their SHA-256 when required by the study plan, and never overwrite an artifact after unblinding a holdout. This directory does not contain or create a holdout corpus.
