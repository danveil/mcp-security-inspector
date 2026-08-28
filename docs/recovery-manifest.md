# MCP Tool Security Inspector Recovery Manifest

> Human-readable integrity manifest for the Day 6G preservation checkpoint.
> This manifest is **not cryptographically signed**. Trust requires an
> independently obtained copy of this manifest or its containing verified Git
> commit/archive.

## Project identity

| Field | Exact value |
|---|---|
| Project | MCP Tool Security Inspector |
| Scientific stage | PRE-FYP RESEARCH PROTOTYPE / PILOT STUDY |
| Repository | `https://github.com/danveil/mcp-security-inspector` |
| Audited branch | `main` |
| Preserved engineering/release checkpoint | `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` |
| Day 6G preservation checkpoint | The Git commit containing this manifest; its parent is `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` |
| Day 6G commit message | `docs: preserve fyp research handover and recovery guides` |
| Release tag | `v0.3.0a1` |
| Package | `mcp-tool-security-inspector` `0.3.0a1` |
| Built-in rule pack | `builtin` `2.0.0` |
| Current artifact schema | `3.1.0` |
| Historical artifact schema supported | `3.0.0` |
| Default evaluation threshold | `MEDIUM` |
| Built-in detectors | 7 families, 16 stable rule identities |

Before Day 6G editing, local `main`, the locally stored `origin/main` tracking
ref, and the annotated `v0.3.0a1` tag resolved to the engineering/release
checkpoint above. The Day 6G documentation commit intentionally comes after
that tag; the tag must continue to resolve to
`374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`. A future recovery must verify the
live remote separately.

## Scientific-state invariants

1. The v0.2 H0 artifact is the authoritative first confirmatory result of this
   pilot: TP 5, TN 18, FP 6, FN 19; accuracy 47.92%, precision 45.45%, recall
   20.83%, F1 28.57%, FPR 25.00%.
2. The v0.3 result on the same 48 samples is **POST-UNBLINDING EXPLORATORY ONLY**:
   TP 11, TN 18, FP 6, FN 13; accuracy 60.42%, precision 64.71%, recall 45.83%,
   F1 53.66%, FPR 25.00%.
3. The holdout is permanently exposed for this detector-development lineage. It
   must not be used as fresh confirmatory evidence.
4. No fresh v0.3 confirmatory result exists.
5. The development and v0.3 construct corpora are development/regression
   evidence, not independent estimates of deployment performance.
6. R08/`holdout_s011` retains the original suspicious label under the frozen
   schema-security-review construct while preserving the independent reviewer's
   benign judgment. Malformed schema alone does not prove malicious intent.

## Immutable research files

These are SHA-256 file identities. Preserve exact bytes and derive new analysis
in a different file.

| SHA-256 | Repository-relative path | Status |
|---|---|---|
| `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` | `evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json` | Authoritative v0.2 H0 |
| `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` | `evaluation/runs/day3c-deep-failure-analysis.md` | Post-unblinding H0 failure analysis |
| `d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b` | `evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json` | v0.3 exposed-holdout exploratory artifact |
| `857b20b5e138e67e7f684cb3784bfb0cd97831ff4a4cefdae6b6d6128465489c` | `evaluation/holdout/reviewer-source.md` | Original blinded reviewer source |

Machine-friendly pairs:

```text
3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80  evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json
deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f  evaluation/runs/day3c-deep-failure-analysis.md
d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b  evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json
857b20b5e138e67e7f684cb3784bfb0cd97831ff4a4cefdae6b6d6128465489c  evaluation/holdout/reviewer-source.md
```

## Corpus identities

These are semantic corpus hashes produced by
`mcpsec.evaluation.integrity.corpus_sha256`, not hashes of the manifest file
alone.

| Corpus SHA-256 | Manifest | Identity | Samples | Exposure/use |
|---|---|---|---:|---|
| `a22de0126d2cf0b00c99ded46687b70dc6f417382a0a11c5ae4a9cad8f6d6f47` | `evaluation/corpus/manifest.json` | `mcpsec-synthetic-metadata` v1.0.0, development | 80 (40/40) | Visible development/regression |
| `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` | `evaluation/holdout/manifest.json` | `mcpsec-independent-holdout-metadata` v1.0.1, holdout | 48 (24/24) | Independently reviewed before H0; now exposed/historical |
| `4209b93750ac4fd1a6445af13d891fa49954e0ba5e1b939d6c52b955060fbba4` | `evaluation/exploratory/v0_3/manifest.json` | `mcpsec-v0.3-construct-exploratory-development` v1.0.0, development | 36 (18/18) | Post-unblinding mechanism regression |

Machine-friendly pairs:

```text
a22de0126d2cf0b00c99ded46687b70dc6f417382a0a11c5ae4a9cad8f6d6f47  evaluation/corpus/manifest.json
c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8  evaluation/holdout/manifest.json
4209b93750ac4fd1a6445af13d891fa49954e0ba5e1b939d6c52b955060fbba4  evaluation/exploratory/v0_3/manifest.json
```

## Experiment identities

| Identity | Exact value |
|---|---|
| H0 corpus hash | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| H0 configuration hash | `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1` |
| H0 Git commit | `a4abee4661522ac13edb37e1b075186a2ccd7a03` |
| H0 Git state | clean (`dirty=false`) |
| H0 package / rule pack | `0.2.0` / `builtin` `1.0.0` |
| H0 artifact schema | `3.0.0` |
| H0 threshold/custom/suppressions | `MEDIUM`; none; none |
| v0.3 exploratory configuration hash | `3cee3f4d1bf73637498ea876d5c26c0b8bf8bab40b6be03284fc9ec5da839323` |
| v0.3 exploratory recorded Git state | `a4abee4661522ac13edb37e1b075186a2ccd7a03`; `dirty=true` |
| v0.3 exploratory artifact schema | `3.0.0` |

Historical package/rule-pack/schema values are authentic artifact provenance;
do not rewrite them to current `0.3.0a1`/`2.0.0`/`3.1.0` values.

## Day 6 knowledge/recovery documents

These are the final Day 6G document identities after the approved technical-map
corrections, recovery/newline consolidation, and index creation. Documents not
listed as corrected retained their pre-6G bytes.

| SHA-256 | Path | Role |
|---|---|---|
| `c3a6749a7bce93ea35f3e60d3c2cd34d37b890dc1aee178e839d0834ea877f0e` | `docs/captain-technical-map.md` | Architecture and evidence map; Day 6G release-state/baseline example corrected |
| `c93fabe9c020ef6826244e058f5650bcce43fde209280c53da39beaa1c470a1e` | `docs/captains-manual.md` | Technical learning and viva manual |
| `4c6960f33287503375e9e273a8d4c0213aea9f23528b9cc83018a8ea1e991bcc` | `docs/fyp-handover.md` | Research continuity and formal-FYP resumption |
| `7a5a9558d0587fdaba6732fff42501a928df97bcbfc7dbd73596deacbd6a769e` | `docs/disaster-recovery.md` | Reconstruction, backup, LF-safe recovery, and Day 6G preservation status |
| `8c4388b3f46a6954edf3a515246c28cf12137aac2884c9b85d29869d71f40b72` | `docs/final-adversarial-review.md` | Final adversarial examination and risk register |
| `36d78b765fae7b2b8b60200b21e9586a5c39906eb3d286dd3e530dd891706dc6` | `docs/formal-fyp-blueprint.md` | Supervisor-dependent formal-FYP design |
| `e733e9acd84b3dac602d753031eb403d90ba8ffb2607bc3e1fe3f565ba63774a` | `docs/day6-index.md` | Concise Day 6 entry point and reading order |

The selected secondary research inventory is:

| SHA-256 | Path | Status |
|---|---|---|
| `8d801c54dcc6e294e169471d21a1496f7caa9fd69de2fdfeb689f6c7a3be8403` | `evaluation/runs/day6g-secondary-evidence-inventory.md` | Classification and exact hashes for 45 historical supporting files |

This manifest does not list its own hash because embedding a self-hash would be
circular. Hash `docs/recovery-manifest.md` separately when archiving the complete
Day 6 set.

## Required tracked recovery paths

```text
pyproject.toml
.gitignore
.gitattributes
.github/workflows/ci.yml
README.md
SECURITY.md
CHANGELOG.md
docs/research-status.md
docs/reproducibility.md
docs/releases/v0.3.0a1.md
docs/day6-index.md
docs/captain-technical-map.md
docs/captains-manual.md
docs/fyp-handover.md
docs/disaster-recovery.md
docs/recovery-manifest.md
docs/final-adversarial-review.md
docs/formal-fyp-blueprint.md
docs/research-protocol.md
docs/holdout-experiment-plan.md
evaluation/corpus/manifest.json
evaluation/holdout/manifest.json
evaluation/holdout/reviewer-source.md
evaluation/holdout/review-ledger.md
evaluation/holdout/integrity-report.json
evaluation/exploratory/v0_3/manifest.json
evaluation/runs/README.md
evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json
evaluation/runs/day3c-deep-failure-analysis.md
evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json
evaluation/runs/day6g-secondary-evidence-inventory.md
```

## Recovery verification procedure

### 1. Use an LF-safe clone

```powershell
git clone -c core.autocrlf=false https://github.com/danveil/mcp-security-inspector.git
Set-Location mcp-security-inspector
git fetch --tags
git log --all --format="%H %s" -- docs/day6-index.md
git checkout <day6g-preservation-commit>
git rev-parse HEAD
git rev-list -n 1 v0.3.0a1
git status --porcelain
```

An ordinary Windows checkout with `core.autocrlf=true` was observed to change
reviewer/corpus identities. If the expected hashes do not match, inspect newline
policy before declaring corruption. Do not rewrite the expected hashes.
The `v0.3.0a1` tag must still resolve to
`374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`; it does not contain the later Day
6G documentation package.

### 2. Rebuild the environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

### 3. Verify file hashes

```powershell
$critical = @(
  'evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json',
  'evaluation/runs/day3c-deep-failure-analysis.md',
  'evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json',
  'evaluation/holdout/reviewer-source.md'
)
Get-FileHash -Algorithm SHA256 $critical | Select-Object Path, Hash
```

### 4. Verify corpus hashes without detection

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; from mcpsec.evaluation.integrity import corpus_sha256; paths=['evaluation/corpus/manifest.json','evaluation/holdout/manifest.json','evaluation/exploratory/v0_3/manifest.json']; [print(p, corpus_sha256(Path(p))) for p in paths]"
.\.venv\Scripts\mcpsec.exe corpus-check evaluation\corpus\manifest.json evaluation\holdout\manifest.json
```

### 5. Run safe engineering gates

```powershell
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\ruff.exe format --check .
.\.venv\Scripts\mypy.exe src
.\.venv\Scripts\python.exe -m pytest --cov=mcpsec --cov-report=term-missing
.\.venv\Scripts\python.exe -m build
.\.venv\Scripts\mcpsec.exe --version
.\.venv\Scripts\mcpsec.exe --help
.\.venv\Scripts\mcpsec.exe demo
```

Do not run the exposed holdout evaluation during recovery.

## Day 6G preservation status

Day 6D found five local/untracked knowledge documents and ignored Day 3/Day 4
supporting evidence. Day 6E and Day 6F added the adversarial review and formal
blueprint. Day 6G reviews and checkpoints all seven source documents, a concise
index, scoped LF/byte-preservation metadata, and the 45-file secondary evidence
selection described by `day6g-secondary-evidence-inventory.md`.

The Git checkpoint is one preservation channel, not an independently trusted
backup. After pushing, create and verify an off-device Git bundle or another
approved checksummed archive. Do not place a large redundant bundle inside the
repository.

The exposed holdout was not rerun to create this manifest, and this manifest does
not constitute fresh confirmatory evidence.
