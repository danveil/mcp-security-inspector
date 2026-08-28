# MCP Tool Security Inspector Disaster-Recovery Guide

> **Purpose:** reconstruct the `v0.3.0a1` pre-FYP prototype and its scientific
> record after loss of a laptop, environment, IDE state, local clone, or working
> memory.
> **Engineering/release checkpoint audited:** `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`
> **Day 6 preservation:** use the Git commit containing this guide and
> [`day6-index.md`](day6-index.md)
> **Recovery manifest:** [`recovery-manifest.md`](recovery-manifest.md)

This guide is a preservation procedure, not a detector-improvement or research-
evaluation plan. Recovery must restore historical identities; it must never
recreate favorable results from memory or use the exposed holdout as new
confirmatory evidence.

## 1. Recovery outcome

A successful recovery has all of the following:

- complete Git history and release tags, or a documented limitation if only a
  source archive survives;
- exact source, tests, rules, corpora, review evidence and three immutable
  research evidence files at the audited checkpoint;
- a Python 3.12+ environment rebuilt from `pyproject.toml`;
- passing safe engineering gates without evaluating the exposed holdout;
- exact critical file and corpus identities from the recovery manifest;
- the seven Day 6 knowledge/recovery documents plus `docs/day6-index.md`;
- an explicit scientific state: v0.2 H0 is authoritative, v0.3 is
  post-unblinding exploratory, and fresh confirmation has not occurred; and
- a record of any missing local-only analyses rather than an attempt to invent
  them.

## 2. Immediate rules after suspected loss or corruption

1. Stop editing the surviving copy.
2. Preserve the current device/archive read-only where practical.
3. Record what failed, the time discovered, available copies, Git HEAD, Git
   status and observed hashes. Do not print secrets.
4. Choose the most trustworthy source: verified Git remote, independent Git
   bundle, another full clone, or checksummed archive.
5. Reconstruct into a **new directory**. Do not repair over the only surviving
   copy.
6. Verify identities before interpreting or changing research material.
7. Do not run `mcpsec evaluate` against `evaluation/holdout/manifest.json`.
8. If exact H0 bytes cannot be recovered, report evidence loss. A rerun on the
   exposed holdout is not a replacement H0.

## 3. Critical asset inventory

### 3.1 Recovery classification

| Asset | Recovery class | Required treatment |
|---|---|---|
| `src/` production package | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Recover from checkpoint/tag; never reconstruct detector logic from memory |
| `tests/` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Required to verify behavior and security boundaries |
| top-level `rules/` examples | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Data-only examples; do not replace with unreviewed local rules |
| `src/mcpsec/evaluation/` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Corpus validation, metrics, hashing, artifacts and comparison |
| `evaluation/corpus/` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Development/regression corpus v1.0.0 |
| `evaluation/holdout/` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Exposed historical holdout v1.0.1, reviewer and integrity records |
| `evaluation/exploratory/v0_3/` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Post-unblinding development fixtures, not a holdout |
| three allowlisted files under `evaluation/runs/` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Immutable H0, Day 3C and primary Day 4C evidence |
| Day 6G-selected secondary files under `evaluation/runs/` | **TRACKED IN GIT** / **HISTORICAL SECONDARY EVIDENCE** | Exact selection, classifications, hashes, and status are in `day6g-secondary-evidence-inventory.md`; never upgrade them to confirmatory evidence |
| other/new `evaluation/runs/` files | **IGNORED**, normally **REGENERABLE** or transient | Preserve separately only when a protocol explicitly selects and hashes them |
| `README.md`, `SECURITY.md`, `CHANGELOG.md`, tracked `docs/` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Public scope, claims, release and reproducibility record |
| seven Day 6 documents plus `docs/day6-index.md` | **TRACKED IN THE DAY 6G DOCUMENTATION CHECKPOINT** | Preserve together; verify final hashes through the recovery manifest |
| `pyproject.toml` | **TRACKED IN GIT** / **REMOTE-DEPENDENT** install | Package metadata and bounded dependency declarations |
| `.github/workflows/ci.yml` | **TRACKED IN GIT** / **REMOTE-DEPENDENT** execution | Ubuntu quality-gate recipe; GitHub Actions availability required |
| `.gitignore`, `.gitattributes` | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Ignore and immutable-evidence checkout policy |
| `.git/` history, branches and tags | **SHOULD BE PRESERVED**; remote or bundle dependent | A source ZIP is not a substitute for Git history/tag provenance |
| `v0.3.0a1` tag and release notes | **TRACKED IN GIT** / **SHOULD BE PRESERVED** | Tag identifies current alpha commit; release page must be checked separately |
| `.venv/`, `.venv-*` | **REGENERABLE** / **SHOULD NOT BE PRESERVED** | Recreate; do not commit or use as the authoritative dependency record |
| `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `__pycache__/`, coverage files | **REGENERABLE** / **SHOULD NOT BE PRESERVED** | Safe to lose |
| `dist/`, `build/`, `*.egg-info/` | **REGENERABLE** / **SHOULD NOT BE PRESERVED** | Rebuild from a verified commit; verify a separately released artifact if one exists |
| reports, baselines and temporary output | Usually **REGENERABLE** / **SHOULD NOT BE PRESERVED** | Preserve only if a protocol names it as evidence |
| IDE state `.idea/`, `.vscode/` | **LOCAL-ONLY** / normally **SAFE TO LOSE** | Recreate personal preferences; do not make research depend on them |
| `.env*`, private keys, credentials files, real tokens | **SECRET / MUST NOT BE COMMITTED** | Store in a password manager or approved secret store, never the project archive |

### 3.2 What a normal fresh clone contains

At the Day 6D audit, Git tracked 155 paths: 44 under `src/`, 31 tests, two
top-level rule examples, 39 evaluation paths, 17 tracked documentation paths and
one CI workflow. A clean clone contained the production package, tests, corpora,
holdout review material, release documentation, H0, Day 3C and primary Day 4C.

It did **not** contain:

- `docs/captain-technical-map.md`;
- `docs/captains-manual.md`;
- `docs/fyp-handover.md`;
- this disaster-recovery guide or the recovery manifest until they are reviewed
  and preserved later;
- Day 3D synthesis files;
- Day 4A design report;
- most Day 4B/Day 4C generated runs and secondary analyses; or
- the ignored Day 4C analysis helper.

That list records the Day 6D starting gap. Day 6G selected the complete Day 6
documentation package and the reviewed secondary-evidence set for one versioned
checkpoint. A live remote and independent bundle still need separate
verification; Git cannot protect material until its commit is pushed or
otherwise archived.

## 4. Safe reconstruction procedure

### 4.1 Clone with research-safe line endings

The audit discovered a Windows-specific identity risk. System Git had
`core.autocrlf=true`; an ordinary clone converted unprotected Markdown/JSON
research inputs to CRLF. File content looked the same, but the reviewer and all
three corpus hashes changed. The three primary evidence artifacts remained exact
because `.gitattributes` marks them `-text`.

Use an LF-preserving clone on **every platform** when restoring this checkpoint:

```powershell
git clone -c core.autocrlf=false https://github.com/danveil/mcp-security-inspector.git
Set-Location mcp-security-inspector
git config --get core.autocrlf
git fetch --tags
git rev-parse HEAD
git status --porcelain
git tag --list
git show --no-patch v0.3.0a1
```

Expected `core.autocrlf` is `false`. Expected alpha commit is
`374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`.

If an existing recovery clone used CRLF conversion, do not reset a dirty or sole
copy. Make a second clean clone with the command above and verify it. A future
reviewed maintenance change may extend `.gitattributes` or make research hashing
newline-independent, but Day 6D does not alter that infrastructure.

### 4.2 If GitHub is unavailable

Use, in preference order:

1. a verified `git bundle` containing all refs;
2. another complete clone with `.git/` intact;
3. a checksummed source archive plus separately preserved Git metadata; or
4. a source archive alone, explicitly recording that branch/tag history cannot
   be independently reconstructed.

To restore a bundle:

```powershell
git bundle verify X:\approved-backup\mcpsec.bundle
git clone -c core.autocrlf=false X:\approved-backup\mcpsec.bundle mcp-security-inspector
Set-Location mcp-security-inspector
git rev-parse HEAD
git tag --list
```

Never treat an unverified directory copied from an unknown machine as the
authoritative research source.

### 4.3 Select the checkpoint

For historical reconstruction:

```powershell
git checkout v0.3.0a1
git rev-parse HEAD
git status --porcelain
```

This creates a detached checkout suitable for inspection. For new formal FYP
work, return to the supervisor-approved base branch and create a new development
branch; do not develop on the tag or rewrite it.

The `v0.3.0a1` tag intentionally predates the Day 6G documentation commit. To
recover the knowledge package, locate and check out the later commit that added
`docs/day6-index.md`:

```powershell
git log --all --format="%H %s" -- docs/day6-index.md
git checkout <day6g-preservation-commit>
git rev-list -n 1 v0.3.0a1
```

The last command must still resolve to
`374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`.

## 5. Detector-free integrity verification

### 5.1 Verify preserved file bytes

From the LF-safe clone:

```powershell
$critical = @(
  'evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json',
  'evaluation/runs/day3c-deep-failure-analysis.md',
  'evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json',
  'evaluation/holdout/reviewer-source.md'
)
Get-FileHash -Algorithm SHA256 $critical |
  Select-Object Path, Hash
```

Compare against [`recovery-manifest.md`](recovery-manifest.md). Do not update the
manifest merely because an observed hash differs.

### 5.2 Verify semantic corpus identities

After installing the package, use the existing detector-free hashing
infrastructure:

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; from mcpsec.evaluation.integrity import corpus_sha256; paths=['evaluation/corpus/manifest.json','evaluation/holdout/manifest.json','evaluation/exploratory/v0_3/manifest.json']; [print(p, corpus_sha256(Path(p))) for p in paths]"

.\.venv\Scripts\mcpsec.exe corpus-check `
  evaluation\corpus\manifest.json `
  evaluation\holdout\manifest.json
```

`corpus_sha256` hashes the strict manifest identity and referenced corpus files.
`corpus-check` verifies split declarations, duplicate IDs and exact canonical
cross-split content. Neither command executes detector rules or invokes tools.

Do **not** substitute:

```text
mcpsec evaluate evaluation/holdout/manifest.json
```

The holdout is already exposed, and another run cannot create new confirmatory
evidence.

### 5.3 Damage response

```text
Hash matches
  -> mark asset verified and continue.

Hash differs
  -> stop;
  -> record expected/observed hash, HEAD, status and checkout line-ending policy;
  -> compare with the tag, verified bundle and independent archive;
  -> determine line-ending conversion, corruption or intentional versioning;
  -> restore exact trusted bytes into a new copy;
  -> never rewrite the expected hash to make the check pass.
```

## 6. Environment rebuild

### 6.1 Supported evidence

- Package declaration: Python `>=3.12`.
- CI: Ubuntu with Python 3.12.
- Day 6D clean rebuild: Windows with Python 3.12.13.
- macOS: not exercised by repository CI; no support claim is made.

### 6.2 Windows procedure

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"

.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\ruff.exe format --check .
.\.venv\Scripts\mypy.exe src
.\.venv\Scripts\python.exe -m pytest --cov=mcpsec --cov-report=term-missing
.\.venv\Scripts\python.exe -m build

$wheel = (Get-ChildItem dist\*.whl | Select-Object -First 1).FullName
.\.venv\Scripts\python.exe scripts\smoke_wheel.py $wheel
.\.venv\Scripts\mcpsec.exe --version
.\.venv\Scripts\mcpsec.exe --help
.\.venv\Scripts\mcpsec.exe demo
```

### 6.3 Linux procedure

```bash
python3.12 -m venv .venv
.venv/bin/python --version
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"

.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy src
.venv/bin/python -m pytest --cov=mcpsec --cov-report=term-missing
.venv/bin/python -m build
.venv/bin/python scripts/smoke_wheel.py dist/*.whl
.venv/bin/mcpsec --version
.venv/bin/mcpsec --help
.venv/bin/mcpsec demo
```

The Linux procedure mirrors CI, but the Day 6D local reconstruction ran on
Windows. Re-run it in CI for the exact recovered commit.

### 6.4 What Day 6D actually verified

The temporary Git-only reconstruction installed successfully from source with
Python 3.12.13. Ruff lint and format check passed; strict mypy passed; 472 tests
passed with 92.95% coverage; source distribution and wheel built; the clean
installed-wheel smoke passed; and `mcpsec --version`, `--help` and the inert
bundled `demo` passed. No holdout evaluation was run.

## 7. Dependency preservation and drift

There is no lock file, requirements lock or constraints file. The project can
rebuild a compatible environment, but it cannot reproduce the exact resolver
result months later from Git alone.

### 7.1 Declared policy

| Dependency group | Constraint quality | Recovery implication |
|---|---|---|
| Runtime: `mcp`, `httpx2`, `typer`, `rich`, `pydantic`, `PyYAML`, `jsonschema` | Lower and upper major bounds | Prevents the next major release but allows minor/patch drift |
| `build` dev dependency | `>=1.2,<2` | Major bounded |
| `pytest`, `pytest-cov`, `ruff`, `mypy`, type stubs | Lower bound only | Future major versions may be selected and break tests/configuration |
| Build backend `hatchling` | `>=1.27`, no upper bound | Fresh isolated build depends on future compatible behavior |
| Python | `>=3.12` | Future Python versions are accepted by metadata even though CI currently tests 3.12 only |
| GitHub Actions | Major tags (`@v4`, `@v5`) | Convenient maintenance but not immutable action commits |

### 7.2 Day 6D resolved snapshot

The successful clean build resolved, among direct tools, `mcp 2.1.1`, `httpx2
2.12.0`, `typer 0.27.1`, `rich 14.3.4`, `pydantic 2.13.4`, `PyYAML 6.0.3`,
`jsonschema 4.26.0`, `pytest 9.1.1`, `pytest-cov 7.1.0`, `ruff 0.16.5`, `mypy
2.3.1`, `build 1.6.0`, and isolated `hatchling 1.32.0`. This is an observed
recovery snapshot, not a new dependency lock or support promise.

### 7.3 Risk classification

- **P0 recovery blocker:** none while package indexes and compatible versions are
  available; the clean install succeeded.
- **P1 reproducibility risk:** no exact dependency lock/constraints snapshot;
  lower-only dev/build ranges; Python metadata broader than tested versions.
- **P2 maintenance risk:** GitHub Actions major tags and normal dependency/API
  deprecation over time.

Future formal research should record the resolved environment in each artifact
and consider an approved constraints/lock strategy. Do not overhaul dependencies
just before a confirmatory run without a new freeze and regression verification.

## 8. Platform recovery risks

| Platform/topic | Repository evidence | Recovery advice |
|---|---|---|
| Windows | Day 6D clean build/tests; PowerShell helper scripts; README activation command | Use Python 3.12 and explicit interpreter paths; clone with `core.autocrlf=false`; expect `Scripts\*.exe` |
| Linux | GitHub Actions Ubuntu/Python 3.12; portable smoke script | Treat CI as the principal Linux evidence; use `.venv/bin/*` and LF checkout |
| macOS | README gives POSIX activation, but SECURITY explicitly makes no tested support claim | Treat as unverified until a full clean build/test/smoke run passes on macOS |
| Paths | Production code uses `pathlib`; Windows helper scripts use backslashes/PowerShell | Do not copy PowerShell-only commands verbatim to POSIX shells |
| Console | Rich rendering and hostile terminal escaping are tested; glyph support varies | Prefer JSON for machine comparison; terminal replacement glyphs do not imply evidence corruption |
| Encoding | Explicit UTF-8/UTF-8-SIG handling; strict JSON; evidence byte hashes | Preserve LF research checkout; beware editor/BOM/newline transformations |
| Line endings | Only three primary artifacts are currently `-text` in `.gitattributes` | Use recovery-safe clone command; raw Windows CRLF checkout changes reviewer/corpus hashes |
| Filesystem | Case and rename semantics differ; paths are stored portably in artifacts | Avoid case-only renames and absolute private paths; verify on target OS |
| Timing | Machine, power mode, clock and background load affect results | Never compare recovered latency without matching recorded environment/boundary |

## 9. Release recovery

Local evidence at Day 6D:

- package `0.3.0a1` in `pyproject.toml` and `src/mcpsec/__init__.py`;
- built-in pack `builtin` `2.0.0` in `src/mcpsec/constants.py`;
- annotated local tag `v0.3.0a1` at
  `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad`;
- local `main` and stored `origin/main` at the same commit; and
- tracked `docs/releases/v0.3.0a1.md`.

A future user must manually verify on GitHub:

1. repository ownership and remote URL;
2. default branch and its commit;
3. annotated `v0.3.0a1` tag and commit;
4. prerelease/release-page status and attached assets;
5. source archive identity/provenance; and
6. whether branch protections or releases changed after this audit.

Day 6D did not perform a live GitHub fetch/release-page audit. PyPI is not
required. A verified clone installs with:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\mcpsec.exe --version
```

Dependencies still require an accessible package index/cache unless independently
archived. Do not publish to PyPI merely as a recovery workaround.

## 10. Documentation recovery set

| Question | Recovery source | Day 6D result |
|---|---|---|
| What is the project? | `README.md`, `docs/architecture.md` | Answered in tracked Git |
| What version is it? | `pyproject.toml`, `__init__.py`, release notes, tag | Answered |
| What is authoritative? | `docs/research-status.md`, `docs/reproducibility.md`, `evaluation/runs/README.md` | H0 and hashes answered |
| What is exploratory? | research status and v0.3 checkpoint | Answered |
| What is the exposed holdout? | README, holdout README, research protocol | Answered |
| How is the environment rebuilt? | README, `PREPARATION.md`, CI, this guide | Basic tracked instructions existed; clean procedure verified here |
| How is evidence verified? | reproducibility guide and recovery manifest | Previous guide covered three artifacts; Day 6D adds reviewer/corpus/knowledge identities and LF warning |
| How is the FYP resumed? | `fyp-handover.md` and `formal-fyp-blueprint.md` | Preserved by the Day 6G documentation checkpoint |
| How is the architecture relearned? | technical map/manual | Preserved by the Day 6G documentation checkpoint |

Day 6G closes the documentation, LF-guidance, compact-manifest, and selected
secondary-evidence preservation gaps. Remaining gaps are:

- no lock file recreates exact dependency versions;
- an independent Git bundle/remote still requires operational verification;
- future run artifacts remain intentionally ignored until a protocol selects
  them; and
- the v0.3 dirty-state source cannot be reconstructed from its recorded clean
  commit and must remain exploratory.

Earlier creation-day statements are retained as historical audit context rather
than rewritten as if the gap never existed.

## 11. Local-only data classification

| Local material | Loss class | Action |
|---|---|---|
| Day 6 documentation package | **TRACKED / MUST BACK UP** | Preserve the seven source documents, index, and recovery manifest together |
| `evaluation/runs/day3d/*.md` | **TRACKED / HISTORICAL SYNTHESIS** | Thesis-ready but retain confirmatory/descriptive boundaries |
| Day 4A design report | **TRACKED / POST-UNBLINDING DESIGN** | Explains why v0.3 exists and records rejected unsafe/post-hoc ideas |
| Day 4B development/exploratory JSON | **TRACKED / SECONDARY PROVENANCE** | Chronology and exact dirty-state timings; not independent evidence |
| Day 4C secondary JSON/Markdown and ablations | **TRACKED / POST-UNBLINDING EXPLORATORY** | Preserve raw files; never call them confirmation |
| Day 4C `analysis_snapshot.py` | **TRACKED HISTORICAL HELPER** | Review before execution; it is not production code |
| Extra Day 3B timing/ablation artifacts | **TRACKED / PREREGISTERED SECONDARY** | Exact values and hashes are preserved; H0 remains primary |
| `.venv`, caches, coverage, build products | **SAFE TO LOSE** | Recreate; exclude from backup |
| `.env`, keys, credential files | **MUST NOT COMMIT** | Store separately in an approved secret manager; do not include in project archive |
| IDE/editor state | **SAFE TO LOSE** | Recreate personal configuration |

## 12. Secret and privacy handling

The Day 6D filename/content scan found no secret-like tracked filenames, private
key headers, common live-token prefixes, private absolute paths or email-like
content in working-tree files. Credential terms in tests/corpora are synthetic
security fixtures, not evidence of live credentials.

| Location | Category | Severity | Action |
|---|---|---:|---|
| `.git` commit/tag metadata | Contributor attribution may contain personal name/email | INFO / expected public Git metadata | Confirm contributor consent before mirroring; do not strip history casually |
| `evaluation/holdout/reviewer-source.md` and `review-ledger.md` | Human-authored review wording and role descriptor | LOW | Preserve immutable evidence; do not add unnecessary identity; confirm redistribution expectations |
| Corpora/tests | Synthetic password/token/key terminology | INFO | Retain as inert fixtures; never replace placeholders with real secrets |
| `.gitignore` secret patterns | Preventive exclusions for `.env`, keys and credential files | Protective | Keep; remember ignored does not mean encrypted/backed up |

If a genuine secret is later found in Git history, stop public redistribution and
escalate credential revocation/history-remediation decisions. Do not print the
secret into an issue, report or recovery log. Historical evidence preservation
does not override an urgent credential or personal-safety response.

## 13. Failure-mode matrix

| Scenario | What survives / what is lost | Detect damage | Recover | Never recreate from memory |
|---|---|---|---|---|
| **A. Laptop SSD dies** | Git remote retains tracked assets; untracked Day 6 and ignored analyses disappear unless independently backed up | Compare fresh clone inventory and manifest | LF-safe clone; restore separate Day 6/analysis archive; verify hashes | H0 bytes, labels, review judgments, ignored analysis values |
| **B. GitHub inaccessible** | Local clone/history and offline bundle may survive; remote release/CI unavailable | `git fsck`, bundle verification, local refs | Work from verified clone/bundle; create temporary redundant backup, not a replacement public history | Tag meaning, release status or remote branch state |
| **C. Local repository deleted** | Remote/bundle survives; local ignored files/venv do not | Missing directory; compare backup inventory | Clone with LF policy; restore independent local-only archive | Untracked documents or exact ignored timings |
| **D. Virtual environment destroyed** | All tracked evidence/source survives | Interpreter/scripts missing | Recreate Python 3.12 venv, install `.[dev]`, run gates | Dependency behavior from memory; do not copy unknown site-packages |
| **E. Python ecosystem changes** | Git declarations survive; exact old resolver may be unavailable | Installation/test/build differences | Use recorded Python/dependency snapshot, compatible constraints/cache, or approved maintenance branch; test on development data | Claim that a new dependency environment is identical |
| **F. Research artifact corrupted** | Git/bundle/independent copy may retain exact bytes | SHA-256 mismatch | Restore exact file into a new copy; verify tag and all hashes | Rerun exposed holdout and call it the original artifact |
| **G. Corpus edited accidentally** | Git blob and other copies retain frozen version | Git status/diff and semantic corpus hash | Preserve accidental diff; restore verified version or create a new versioned corpus protocol | Original labels/rationales/hash |
| **H. Tag removed accidentally** | Commit may survive in branch/reflog/remote/bundle | `git tag --list`, remote/manual audit | Restore annotated tag only from verified tag object/bundle or documented release evidence; coordinate before pushing | Tag message, target or release date |
| **I. Return after six months** | Tracked docs survive; Day 6 set only if preserved | Student cannot explain H0/v0.3 chronology | Read handover, map, manual, recovery guide and manifest before code changes | Scientific chronology or favorable interpretation |
| **J. Supervisor requests new method** | Historical pilot remains valid as history; future plan changes | Written supervisor decision versus old protocol | Create a new versioned protocol, candidate and fresh data plan; keep old evidence separate | Pretend the new method was preregistered for H0 |

## 14. Unified recovery decision tree

```text
Loss or mismatch discovered
  |
  +-- Is a full verified Git clone/bundle available?
  |     |
  |     +-- yes -> copy it read-only -> LF-safe reconstruction -> verify refs
  |     |          -> verify critical hashes -> rebuild environment -> run safe gates
  |     |
  |     +-- no -> is a verified source archive available?
  |                |
  |                +-- yes -> recover source/evidence -> record missing Git provenance
  |                |
  |                +-- no -> declare recovery incomplete; do not invent evidence
  |
  +-- Do all critical file and corpus hashes match?
  |     |
  |     +-- yes -> mark scientific checkpoint intact
  |     |
  |     +-- no -> check newline policy/status -> compare independent copies
  |                -> restore exact trusted bytes or declare corruption
  |
  +-- Are Day 6 and selected local analyses present?
  |     |
  |     +-- yes -> verify their archive/document hashes
  |     |
  |     +-- no -> recover separate backup; do not reconstruct prose/results from memory
  |
  +-- Is formal FYP work resuming?
        |
        +-- yes -> read fyp-handover -> meet supervisor -> approve new protocol
        |          -> freeze candidate -> only then prepare genuinely untouched data
        |
        +-- no -> preserve recovered checkpoint without research changes
```

## 15. Things never to reconstruct from memory

- H0 JSON, confusion matrix metadata, file hash or configuration hash;
- Day 3C and Day 4C exact bytes or derived numerical tables;
- holdout sample content, labels, categories, difficulty or provenance;
- reviewer classifications, confidence, rationale, agreement or R08 adjudication;
- corpus hashes or experiment configuration identities;
- rule IDs, severities, thresholds or risk semantics for a historical artifact;
- Git commit/tag targets, messages or chronology;
- dependency versions claimed for a past experiment;
- timing values or environment metadata;
- a missing ignored analysis that was never independently archived; or
- the claim that v0.3 was independently confirmed.

If the exact record is lost, say it is lost. Honest missing evidence is safer
than fabricated reproducibility.

## 16. Practical three-copy backup policy

### Copy 1 — local working copy

Keep the active Git repository, clean milestone commits, and current Day 6/local
research working files. Use normal OS disk encryption and backups. Do not rely on
the working copy as the only copy.

### Copy 2 — GitHub remote

Push reviewed commits and annotated tags. Verify the remote branch/tag after
milestones. GitHub protects tracked content and history, not ignored/untracked
files. Do not assume an uncommitted document is online.

### Copy 3 — independent archive

At each milestone create:

```powershell
git bundle create mcpsec-all-YYYYMMDD.bundle --all
git bundle verify mcpsec-all-YYYYMMDD.bundle
Get-FileHash -Algorithm SHA256 mcpsec-all-YYYYMMDD.bundle
```

Store the bundle plus:

- the recovery manifest and its independently recorded hash;
- any supervisor-controlled material that cannot be committed;
- a file list and SHA-256 inventory for any future local-only evidence; and
- supervisor-approved protocols or review packages not yet committed.

Keep the independent archive in a separate approved cloud drive or offline
storage. Encrypt it if it contains private unpublished research. Store the
encryption recovery material separately.

Do **not** include:

- virtual environments;
- Python/editor/test caches;
- `dist/`, `build/`, coverage HTML or ordinary temporary reports;
- `.env`, keys, credentials or live tokens; or
- private data that the protocol does not authorize for archival.

During formal FYP, refresh the independent archive weekly while actively
working, and immediately before/after supervisor-approved freezes, corpus
freezes, reviewer handoffs, the single primary evaluation, thesis submission and
release milestones. Periodically test restoration rather than only copying.

## 17. Future FYP resumption pointers

1. Read [`research-status.md`](research-status.md) and
   [`reproducibility.md`](reproducibility.md).
2. Verify [`recovery-manifest.md`](recovery-manifest.md).
3. Use [`captain-technical-map.md`](captain-technical-map.md) to locate the system.
4. Use [`captains-manual.md`](captains-manual.md) to relearn the implementation,
   security and research method.
5. Follow [`fyp-handover.md`](fyp-handover.md) for the supervisor discussion and
   first-week freeze protocol.
6. Keep the old holdout historical/exposed. A future confirmation needs genuinely
   untouched samples under a new approved protocol.

## 18. Current recovery blockers and risks

### P0 — before leaving the project unattended

The Day 6G checkpoint resolves the earlier local-untracked documentation and
secondary-evidence P0 once the commit is preserved on a verified remote or
independent Git bundle. Do not assume that merely creating a local commit
completes that off-device verification.

### P1 — formal-FYP reproducibility

- Decide on a reviewed lock/constraints strategy for the formal frozen
  environment.
- Keep the scoped `.gitattributes` byte-preservation rules and LF-safe clone
  procedure tested as research files evolve.
- Maintain the Day 6G secondary-evidence inventory when a future protocol
  intentionally selects another generated artifact.
- Add/test macOS only if the FYP intends to claim support.

### P2 — maintenance

- Periodically review dependency ranges and GitHub Action versions.
- Test a complete restore from the independent Git bundle/archive.
- Record future release-page/source-archive checks separately from local Git
  verification.

## 19. Day 6D preservation statement

The Day 6D recovery audit created documentation only. The exposed holdout was
not evaluated, no fresh corpus was created, and no detector/research evidence
was changed.
