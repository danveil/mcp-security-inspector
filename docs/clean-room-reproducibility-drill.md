# Clean-Room Reproducibility and Recovery Drill

> **Day 6K status:** completed on Windows from tracked Git state at
> `e812114e62d27f5b003ff746e9281d4954ae1ca0`.
>
> This drill tested engineering recovery and verification/recalculation of
> preserved evidence. It did **not** rerun the exposed holdout, execute a detector
> experiment, tune rules, or create new effectiveness evidence.

## 1. Scope and authority

The recovery question was: if the current project directory and environment were
lost, could a technically competent future student recover the tracked repository,
build a fresh supported environment, verify preserved evidence, and reconstruct
the research chronology?

Evidence authority is deliberately separated:

- Git commits/tags establish tracked history and selected historical states;
- exact file SHA-256 values detect byte-identity changes against expected values;
- corpus identity functions bind a normalized manifest to referenced file content;
- frozen artifacts own historical matrices, metrics, configuration and provenance;
- tests own protected engineering behavior;
- documentation explains status but does not replace artifacts or source.

Hashes are unkeyed identity/integrity checks. They do not independently establish
publisher authenticity, safety, benignness, maliciousness, or scientific validity.

## 2. Primary safety gate

| Check | Expected | Day 6K result |
|---|---|---|
| Git root | MCP Tool Security Inspector repository | PASS |
| HEAD | `e812114e62d27f5b003ff746e9281d4954ae1ca0` | exact match |
| `origin/main` | same as HEAD | exact match |
| Starting worktree | clean | clean |
| `v0.3.0a1^{}` | `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` | exact match |
| Tag object | annotated tag | `tag` |

The release tag was neither moved nor recreated. The primary repository was not
used as the clean environment.

## 3. Isolation and clone procedure

Two disposable local clones were created below the operating-system temporary
directory, outside the primary repository:

1. **Primary recovery clone:** `<TEMP>/mcpsec-day6k-<id>/mcp-security-inspector-recovery`
   using `git clone -c core.autocrlf=false --no-hardlinks ...`.
2. **Hazard-control clone:** `<TEMP>/mcpsec-day6k-<id>/default-autocrlf-clone`
   using the machine's default Git policy (`core.autocrlf=true`).

The recovery clone had local `core.autocrlf=false`, a clean checkout, the expected
HEAD and tag, and 214 tracked paths. Its virtual environments, caches, build
outputs and corruption-test copy never entered the primary repository.

The source was a local full Git clone because the mission tests tracked-state
survival without depending on remote availability. A future real recovery should
clone the official remote or an independently preserved Git bundle and verify the
same identities.

## 4. Newline hazard test

The host-wide Git configuration was:

```text
file:C:/Program Files/Git/etc/gitconfig  core.autocrlf=true
```

CRLF conversion matters because byte SHA-256 changes when LF bytes become CRLF.
The corpus identity function also hashes UTF-8 decoded/re-encoded sample text, so
line-ending changes inside referenced corpus files change the aggregate corpus
identity even though the manifest is normalized.

Current `.gitattributes` uses scoped `-text` rules for:

- authoritative H0, Day 3C and primary Day 4C artifacts;
- development, holdout and exploratory manifests/catalogs;
- the original reviewer source;
- Day 6G knowledge-package files and selected secondary evidence.

### Actual result

Both the explicit LF-safe clone and the default `core.autocrlf=true` clone produced:

| Identity | Expected and recovered |
|---|---|
| H0 artifact | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` |
| Day 3C report | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` |
| Day 4C primary | `d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b` |
| Reviewer source | `857b20b5e138e67e7f684cb3784bfb0cd97831ff4a4cefdae6b6d6128465489c` |
| Development corpus | `a22de0126d2cf0b00c99ded46687b70dc6f417382a0a11c5ae4a9cad8f6d6f47` |
| Holdout corpus | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| Exploratory corpus | `4209b93750ac4fd1a6445af13d891fa49954e0ba5e1b939d6c52b955060fbba4` |

**Assessment:** durable protection is sufficient for the known frozen identities
tested. LF-safe cloning remains the safest documented default. Remaining risk:
future byte-sensitive files outside the exact patterns, unrecorded byte hashes such
as the review ledger, and archives/checkouts produced by other tools must be
explicitly reviewed.

## 5. Tracked-state recovery inventory

The clean clone contained 214 tracked paths:

| Top-level area | Tracked paths | Recovery result |
|---|---:|---|
| `src/` | 44 | implementation recovered |
| `tests/` | 31 | full automated suite recovered |
| `rules/` | 2 | example/data-only rules recovered |
| `evaluation/` | 85 | corpora, review and preserved artifacts recovered |
| `docs/` | 30 | research/recovery/training continuity recovered |
| `.github/` | 1 | Linux CI workflow recovered |
| Remaining root/examples/scripts/sample server | 21 | project metadata, commands and examples recovered |

Verified present: README, SECURITY policy, `pyproject.toml`, CI, release notes,
authoritative H0, Day 3C, primary Day 4C, all three corpus manifests/catalogs,
reviewer source/ledger, secondary evidence inventory, and all Day 6 continuity,
training, proposal and code-walkthrough documents.

## 6. Primary local-only and ignored-state audit

This audit was performed in the primary repository without adding files.

| Local item | Classification | Reason / recovery consequence |
|---|---|---|
| `.venv/`, `.venv-broken-*` | DISPOSABLE | Environments must be rebuilt; not evidence of clean recovery. |
| `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `__pycache__/`, `.coverage` | REGENERABLE | Engineering caches/results; ordinary gates recreate them. |
| `.npm-cache/` | DISPOSABLE | Not needed by this Python package's tracked recovery path. |
| `dist/` v0.2/v0.3 files | REGENERABLE / useful local comparison only | Builds are intentionally ignored; no tracked release digest authenticates these copies. |
| `baseline.json` (v0.1.0, two tools) | REGENERABLE / operator-local | A local operational baseline, not historical research evidence; may encode environment-specific source context. |
| `work/day2b2-full.json` | USEFUL SECONDARY EVIDENCE | Development-corpus schema 3.0.0 artifact; not required because later selected evidence is tracked. |
| `work/day2b2-repeated-e2e.json` | USEFUL SECONDARY EVIDENCE | Historical development timing; machine-dependent and superseded for core preservation. |
| `work/day2b2-without-injection.json` | USEFUL SECONDARY EVIDENCE | Development ablation; not required to authenticate H0. |
| `work/day2b2-comparison.json` | USEFUL SECONDARY EVIDENCE | Derived comparison; regenerable from preserved inputs if compatible tooling remains. |

No untracked rule pack, suppression file, research corpus, label file or required
frozen artifact was found. The ignored `work/` material should remain clearly
secondary/local unless a future archival decision assigns it thesis citation value.

## 7. Machine-state and secret audit

Two tracked historical documents contain creation-time local Windows paths:

- `evaluation/runs/day3c-deep-failure-analysis.md`;
- `docs/final-adversarial-review.md`.

They are provenance/privacy debt, not runtime dependencies. They were not rewritten
because the files are historical/preserved evidence. No actual API credential,
private key, `.env` value or real secret was identified. Security-token wording in
examples and manuals is inert synthetic teaching content. No local database,
untracked rule/suppression file, required IDE setting or external MCP service is
needed for ordinary static recovery.

The wheel smoke helper sets `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` for its
subprocesses. That is a deliberate encoding assumption, not a secret.

## 8. Declared and verified Python environment

### Repository declarations

| Property | Declaration |
|---|---|
| Minimum Python | `>=3.12` |
| Ruff target | Python 3.12 |
| Mypy target | Python 3.12, strict |
| Build backend | `hatchling.build` |
| Build requirement | `hatchling>=1.27` |
| Console entry point | `mcpsec = mcpsec.cli:app` |
| Runtime dependencies | `mcp>=2.0,<3`, `httpx2>=2.5,<3`, `typer>=0.12,<1`, `rich>=13.7,<15`, `pydantic>=2.8,<3`, `PyYAML>=6.0,<7`, `jsonschema>=4.23,<5` |
| Development dependencies | `build>=1.2,<2`, pytest/coverage, Ruff, mypy, PyYAML/jsonschema stubs with lower bounds |

CI tests Ubuntu with Python 3.12. Day 6K locally verified Windows with the app's
installed Python 3.12.13 runtime; no system Python was on PATH. A new venv was
created inside the disposable clone, so no original project environment was used.

### Resolved Day 6K versions

| Tool/package | Version |
|---|---:|
| Python | 3.12.13 |
| pip | 25.0.1 |
| mcp | 2.1.1 |
| httpx2 | 2.12.0 |
| typer | 0.27.2 |
| rich | 14.3.4 |
| pydantic | 2.13.5 |
| PyYAML | 6.0.3 |
| jsonschema | 4.26.0 |
| build | 1.6.0 |
| pytest / pytest-cov | 9.1.1 / 7.1.0 |
| Ruff | 0.16.5 |
| mypy | 2.3.1 |

These are observed Day 6K resolutions, not a lock or a promise that future
resolvers will select them.

## 9. Clean installation

Command inside the recovery clone:

```powershell
python -m venv .venv-recovery
.\.venv-recovery\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv-recovery\Scripts\python.exe -m pip check
```

The sandboxed first attempt correctly demonstrated dependence on package-index
network access: isolated build dependency resolution could not fetch Hatchling.
After package-index access was allowed, editable installation succeeded and
`pip check` reported no broken requirements. No dependency constraint was changed,
pip was not upgraded, and no lockfile was created.

## 10. Static quality gates

| Gate | Exact command | Result |
|---|---|---|
| Ruff lint | `python -m ruff check . --no-cache` | PASS — all checks passed |
| Ruff format | `python -m ruff format --check . --no-cache` | PASS — 123 files already formatted |
| Strict mypy | `python -m mypy src --no-incremental` | PASS — 43 source files, no issues |

These commands ran only in the recovery clone.

## 11. Test-suite safety and result

Before pytest, test references to `holdout`, `evaluate_corpus` and frozen artifacts
were inspected. Findings:

- `tests/test_evaluation.py` analyzes `evaluation/corpus/manifest.json`, the
  80-sample **development** corpus;
- experiment-engine tests analyze temporary synthetic development fixtures;
- holdout-named loader/integrity tests use temporary fixtures;
- the real H0 and Day 4C files are loaded/compared as frozen JSON compatibility
  fixtures; their holdout samples are not rescanned.

No exclusion was necessary.

```powershell
.\.venv-recovery\Scripts\python.exe -m pytest --cov=mcpsec --cov-report=term-missing
```

Result: **472 passed in 18.15 seconds**, total coverage **92.95%**, exceeding the
85% gate. Coverage emitted one non-fatal “module previously imported but not
measured” warning near completion; coverage and all tests still passed.

## 12. Build reproduction

```powershell
.\.venv-recovery\Scripts\python.exe -m build
```

The isolated build resolved `hatchling==1.32.0` and produced:

| Distribution | Size | Day 6K SHA-256 |
|---|---:|---|
| `mcp_tool_security_inspector-0.3.0a1-py3-none-any.whl` | 82,717 bytes | `8bfd7927a58792f0b6176154ba37e6cedee9eabf09e56eb001518e57b17afa0d` |
| `mcp_tool_security_inspector-0.3.0a1.tar.gz` | 487,653 bytes | `16fd2341718d08fa3b7200ccfe1fcee3703bf6b3d3b3a513d3b8073195cd8c12` |

**Functional build reproducibility: PASS.** Wheel and sdist were produced from the
clean clone and the wheel functioned in a separate environment.

**Byte-for-byte reproducible build: NOT ESTABLISHED.** The ignored local primary
v0.3 distributions had different hashes. The repository declares distributions
regenerable and does not provide an authoritative release-distribution digest or
reproducible-build protocol. Build timestamps/tool resolution can affect bytes.

## 13. Clean-wheel and CLI smoke test

`scripts/smoke_wheel.py` created another temporary venv, installed the freshly
built wheel with its dependencies, ran `pip check`, and verified:

- `mcpsec --version` → `mcpsec 0.3.0a1`;
- `mcpsec --help` → available, exit 0;
- `mcpsec demo` → bundled static catalog scanned successfully.

The smoke test passed. It contacted only the package index for declared
dependencies; it did not contact an MCP server or run a holdout.

### Windows pipe observation

Running `mcpsec --help | Select-Object -First 12` caused Rich to receive an
early-closed Windows output pipe and emit `OSError: [Errno 22]`. Running
`mcpsec --help` normally returned exit 0, and captured help in the clean-wheel
script also passed. This is a command-pipeline/console interoperability observation,
not a failure of ordinary help discovery. Avoid using an early-closing consumer
when verifying Rich output on Windows.

## 14. Authoritative H0 verification

Path:
`evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json`

| Property | Recovered value |
|---|---|
| File SHA-256 | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` — exact |
| Artifact schema | 3.0.0 |
| Recorded Git commit/dirty | `a4abee4661522ac13edb37e1b075186a2ccd7a03`, clean |
| Corpus identity | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| Configuration identity | `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1` |
| Historical rule pack | 1.0.0 |
| Matrix | TP=5, TN=18, FP=6, FN=19, N=48 |

The artifact contains sample records, strata, uncertainty, environment and
analysis-core timing. Its 480 timing observations represent 48 samples × 10
measured repetitions; timing is historical machine-dependent evidence, not rerun.

### Independent arithmetic reproduction

Using only the preserved matrix:

```text
N         = TP + TN + FP + FN = 5 + 18 + 6 + 19 = 48
Accuracy  = (TP + TN) / N      = 23 / 48 = 0.4791667 = 47.92%
Precision = TP / (TP + FP)     = 5 / 11  = 0.4545455 = 45.45%
Recall    = TP / (TP + FN)     = 5 / 24  = 0.2083333 = 20.83%
F1        = 2TP/(2TP+FP+FN)    = 10 / 35 = 0.2857143 = 28.57%
FPR       = FP / (FP + TN)     = 6 / 24  = 0.25      = 25.00%
```

Every result matched the frozen artifact. This proves calculation reproducibility
from the matrix, not independent detector-effectiveness replication.

## 15. Day 3C failure-analysis verification

Path: `evaluation/runs/day3c-deep-failure-analysis.md`

Recovered SHA-256:
`deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f`.

This is preserved post-unblinding analysis of H0 errors and rule-family evidence.
It is historical secondary analysis, not a second primary experiment.

## 16. v0.3 exploratory verification

Path:
`evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json`

| Property | Recovered value |
|---|---|
| File SHA-256 | `d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b` — exact |
| Artifact schema | 3.0.0 |
| Recorded Git commit/dirty | `a4abee4661522ac13edb37e1b075186a2ccd7a03`, **dirty** |
| Corpus identity | same exposed holdout `c514ba03...a2d8` |
| Configuration identity | `3cee3f4d1bf73637498ea876d5c26c0b8bf8bab40b6be03284fc9ec5da839323` |
| Historical rule pack | 1.0.0 with recorded resolved v0.3 rules |
| Matrix | TP=11, TN=18, FP=6, FN=13, N=48 |
| Metrics | accuracy 60.42%, precision 64.71%, recall 45.83%, F1 53.66%, FPR 25.00% |

The artifact hash and internal values matched. It remains authentic preserved
post-unblinding diagnostic evidence on the already exposed holdout. Its higher
point estimates do not demonstrate generalization, and dirty-state provenance
limits exact reconstruction of the generation checkout from its commit alone.

## 17. Corpus identity verification and semantics

The existing detector-free `mcpsec.evaluation.integrity.corpus_sha256` function was
called on each clean-clone manifest. No detector was instantiated or executed.

| Corpus | Manifest | Samples | Recovered identity |
|---|---|---:|---|
| Development | `evaluation/corpus/manifest.json` | 80 (40/40) | `a22de0126d2cf0b00c99ded46687b70dc6f417382a0a11c5ae4a9cad8f6d6f47` |
| Independent reviewed holdout | `evaluation/holdout/manifest.json` | 48 (24/24) | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` |
| v0.3 exploratory development | `evaluation/exploratory/v0_3/manifest.json` | 36 (18/18) | `4209b93750ac4fd1a6445af13d891fa49954e0ba5e1b939d6c52b955060fbba4` |

These are **aggregate semantic corpus identities**, not raw manifest-file hashes.
The function:

1. validates/normalizes the typed manifest;
2. sorts sample entries and selected set-like lists deterministically;
3. hashes the UTF-8 decoded/re-encoded content of every referenced catalog file;
4. canonicalizes a payload containing normalized manifest plus sorted file/hash
   records; and
5. SHA-256 hashes that canonical payload.

Therefore object/list normalization defined by the function may ignore some
manifest formatting/order differences, while catalog text line-ending changes
still change referenced-file hashes. Raw file, Git blob and corpus hashes must not
be compared as though they share semantics.

## 18. Human-review evidence and arithmetic

Original source: `evaluation/holdout/reviewer-source.md`

Recovered SHA-256:
`857b20b5e138e67e7f684cb3784bfb0cd97831ff4a4cefdae6b6d6128465489c`.

The ledger preserves:

- 48 reviewed samples;
- 47 agreements, one R08 disagreement, zero abstentions;
- reviewer labels 25 benign / 23 suspicious;
- original labels 24 benign / 24 suspicious;
- exact difficulty agreement 16/48;
- one blinded independent reviewer, not a review panel.

From the binary table:

```text
Observed agreement Po = 47/48 = 0.9791666667
Expected agreement Pe = (24/48 × 25/48) + (24/48 × 23/48)
                      = 0.5
Kappa = (Po - Pe)/(1 - Pe)
      = (0.9791666667 - 0.5)/0.5
      = 0.9583333333
Difficulty agreement = 16/48 = 0.3333333333
```

The preserved reviewer-source summary says 24 benign / 24 suspicious, but its 48
individual judgments total 25/23. The ledger corrects only that arithmetic and
retains every judgment. Silently editing the original would destroy source
provenance. Agreement/kappa describe concordance with one reviewer; they do not
validate detector accuracy, label truth or external validity.

## 19. Configuration identities

| Historical configuration | Identity | Interpretation |
|---|---|---|
| v0.2 H0 primary | `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1` | Frozen MEDIUM threshold, historical full built-in set, no custom rules/suppressions, preregistered timing. |
| v0.3 exposed exploratory primary | `3cee3f4d1bf73637498ea876d5c26c0b8bf8bab40b6be03284fc9ec5da839323` | Post-unblinding resolved v0.3 rule/configuration identity. |

Current package code has built-in rule pack 2.0.0 and current artifact schema
3.1.0, while both historical artifacts self-describe schema 3.0.0 and historical
rule-pack context. A newly calculated current configuration may differ legitimately.
Historical evidence must be interpreted using its recorded configuration and
resolved rule set, not current defaults.

## 20. Research chronology reconstructed from Git and evidence

| Stage | Repository anchor | What survives |
|---|---|---|
| Initial/v0.2 implementation | early commits; tag `v0.2.0` | baseline package history |
| Reproducibility foundation | `7d9ab81` | research identity/corpus framework |
| Experiment engine | `997c5fc` | evaluation, timing, uncertainty and artifact machinery |
| Holdout design/review/freeze | `a4abee4` | reviewed holdout 1.0.1, reviewer source/ledger, preregistration |
| H0 primary run | H0 artifact SHA `3307c...71b80` recording clean `a4abee...` | authoritative pilot matrix/metrics/provenance |
| Failure analysis | Day 3C SHA `deb97c...332f` | post-unblinding failure taxonomy |
| Exploratory hypotheses/rules | `b1a5d4c` | v0.3 exploratory candidate and five additions |
| Exposed-holdout diagnostic | Day 4C SHA `d5d84d...806b`, dirty provenance recorded | exploratory matrix; not confirmation |
| Hardening | `0651313` | safety, compatibility and reproducibility fixes |
| v0.3.0a1 release checkpoint | annotated tag at `3744710` | immutable historical release identity |
| Day 6 preservation | `e577f9c` | handover, recovery guides and selected historical evidence |
| Ownership/viva training | `77754aa` | code-ownership training package |
| Proposal seed | `21ce619` | formal FYP proposal planning |
| Source walkthrough | `e812114` | current main at start of Day 6K |

No missing commit was invented. Artifacts/hashes are used where a stage is more
accurately anchored by preserved output than by a unique commit message.

## 21. Release and Git-history survival

| Identity | Current value |
|---|---|
| Package | `mcp-tool-security-inspector` 0.3.0a1 |
| CLI | `mcpsec` |
| Current built-in rule pack | 2.0.0 |
| Current artifact schema | 3.1.0; loader also supports 3.0.0 |
| Historical tag object | annotated `v0.3.0a1` |
| Historical tag target | `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` |
| Current main | `e812114e62d27f5b003ff746e9281d4954ae1ca0` |

Current main correctly differs from the release target because documentation and
preservation work followed the release. Moving the tag would rewrite the meaning
of that historical release.

The full clone recovered 15 commits, annotated tags, ancestry and later Day 6
commits. A current source ZIP would retain current file bytes but lose Git object
IDs, annotated tag object/message, branch relationships, commit timestamps,
ancestry and direct checkout of historical snapshots. It can support current
source/evidence inspection if files are present, but not the same chronology or
release-provenance proof.

## 22. External dependency audit

| External requirement | Classification | Needed for |
|---|---|---|
| Full Git clone/bundle and Git client | ESSENTIAL for history-grade recovery | commits, tag objects, tracked source/evidence |
| Python 3.12-compatible interpreter | ESSENTIAL | installation, tests, CLI, hashing helpers |
| Package index or preserved wheelhouse | ESSENTIAL under current procedure | build/runtime/development dependency resolution |
| Network access | CONDITIONALLY ESSENTIAL | dependency installation when no local cache/wheelhouse exists |
| C/runtime-compatible OS wheels/toolchain | ESSENTIAL in practice | dependencies such as pydantic/cryptography/platform packages |
| Ruff, mypy, pytest/build dependencies | DEVELOPMENT ONLY | engineering gates and packaging |
| GitHub Actions Ubuntu runner | OPTIONAL validation service | CI evidence, not offline use |
| Packaging credentials/PyPI | RELEASE ONLY | publishing; not used in Day 6K |
| Loopback MCP server | OPTIONAL RETRIEVAL ONLY | explicit `fetch`; never required for files, tests, artifacts or H0 arithmetic |
| Remote MCP server/cloud/database | NOT REQUIRED | ordinary static analysis and evidence verification |

The repository is not a complete offline archive because interpreters and
dependencies are not vendored.

## 23. Dependency reproducibility

Runtime dependencies use lower bounds plus upper major bounds. Several development
dependencies have lower bounds only. The build backend itself is `hatchling>=1.27`.
Consequences:

- compatible installation was demonstrated today;
- a future resolver may choose newer versions with changed behavior;
- package-index removal/yanking or platform wheel changes can break recovery;
- the historical artifacts record direct runtime versions, but that is not a
  transitive lock or source archive;
- exact environment reconstruction and byte-identical builds are not guaranteed.

Future recommendation: before a formal confirmatory freeze, adopt a
supervisor-approved constraints/lock and wheelhouse/archive policy for supported
platforms, record hashes and resolver/tool versions, and keep human-readable
`pyproject.toml` bounds as the package policy. Do not retroactively claim it for
the pilot.

## 24. Platform reproducibility

| Platform | Evidence/status |
|---|---|
| Windows x64 | **DAY 6K LOCALLY VERIFIED** — Windows 10.0.26200, Python 3.12.13 |
| Linux | **CI-EVIDENCED** — GitHub Actions Ubuntu, Python 3.12, quality/tests/wheel/development evaluation workflow |
| macOS | **UNVERIFIED** — no repository workflow or Day 6K run found |

Platform-sensitive areas: Git newline conversion, path separators and maximum
path behavior, terminal encoding/Rich pipes, availability of binary dependency
wheels, temporary-directory behavior, case sensitivity, locale/Unicode handling,
filesystem iteration (mitigated where security identity requires sorting), and
machine/background-load-dependent timing.

Linux recovery should use `.venv/bin/python`, forward slashes and the CI commands.
This report does not claim a local Linux clean-room run.

## 25. Optional retrieval boundary

Normal recovery, static scanning, tests, builds, corpus hashing and preserved
evidence arithmetic require no MCP endpoint. Optional `mcpsec fetch` requires an
explicit local HTTP(S) MCP service and applies loopback, address, redirect/proxy,
pagination, size and timeout controls. It performs `tools/list`, never tool
invocation. It is neither necessary nor appropriate for reproducing H0 arithmetic.

## 26. Reproducibility levels

| Level | Question | Current assessment |
|---|---|---|
| 1 — Source recovery | Can tracked source/docs/tests/evidence be reconstructed? | **PASS:** 214 paths, history/tag and Day 6 docs recovered. |
| 2 — Functional engineering reproduction | Can a clean environment install, lint, type-check, test, build and smoke? | **PASS on Day 6K Windows:** 472 tests, 92.95%, wheel/sdist/smoke. Linux is CI-evidenced. |
| 3 — Evidence verification | Can frozen files and identities be authenticated against recorded digests? | **PASS for recorded identities:** H0, Day 3C, Day 4C, reviewer and three corpora match. Authenticity remains externally qualified. |
| 4 — Analysis reproduction | Can reported calculations be recomputed from preserved evidence? | **PASS:** H0 metrics and reviewer agreement/kappa reproduced without scanning. |
| 5 — Experimental replication | Can an independent study repeat the method on fresh data? | **NOT YET TESTED:** requires supervisor-approved construct/protocol, remediation and genuinely untouched data. |

Level 4 is not Level 5. Recomputing `5/24` recall verifies arithmetic; rescanning
the already exposed holdout would repeat an exposed-data procedure; only a new
independent study can address replication/generalization.

### Viva-ready distinction

“I reproduced the reported calculations from immutable matrices and labels, and I
verified their file/corpus/configuration identities. I did not rerun the exposed
holdout. Even rerunning that same holdout would not independently replicate the
study, because v0.3 was designed after those examples were exposed. Replication
requires a frozen candidate and genuinely untouched, independently governed data.”

## 27. Conceptual failure-injection matrix

| Scenario | What breaks | Detection | Recovery source/current mitigation | Future improvement |
|---|---|---|---|---|
| GitHub disappears | Primary remote availability | clone/fetch fails | existing full clones or Git bundle; local history is complete | independently stored verified bundle plus checksum |
| Laptop disappears | unarchived ignored/local files and environments | asset unavailable | tracked remote preserves selected evidence/docs; environments rebuild | independent encrypted backup inventory; avoid important local-only evidence |
| Package index changes | dependency resolution/exact versions | pip/build failure or changed lock-free resolution | bounded declarations, artifact environment metadata | reviewed locks/constraints and wheelhouse/archive |
| Python 3.12 becomes unavailable | install/test/build runtime | interpreter creation fails | source and documented version remain | archive interpreter/container recipe where policy permits; test newer Python before future freeze |
| Global autocrlf changes | byte-sensitive working-tree identities | recorded hashes/corpus hashes mismatch | scoped `.gitattributes`; LF-safe clone command | include any new frozen file in reviewed attributes/hash manifest |
| One artifact is corrupted | exact historical result bytes | file SHA mismatch and loader self-consistency may fail | Git object/remote/bundle/independent copy | signed/external manifest and multiple checked copies |
| One corpus file is corrupted | aggregate corpus identity and future exact reconstruction | `corpus_sha256` mismatch | Git + expected aggregate identity | signed archive/manifest and explicit freeze procedure |
| Annotated tag object is lost | release annotation and tag-object provenance | `cat-file -t`/tag lookup fails | full clone/bundle containing refs/objects | mirror tags and verified bundle; never rely only on ZIP |
| Only source ZIP survives | history, tag objects, ancestry and snapshots | no `.git`; Git commands fail | current files may preserve evidence/docs | preserve full Git bundle plus source/evidence archive |
| README is lost but Git survives | primary orientation | missing tracked file in working tree | restore exact file from commit; other docs/history remain | independent documentation index/export |

Poor recovery must never be “solved” by rerunning the exposed holdout and calling
the new output the historical artifact.

## 28. Hash-corruption drill

A copy of the harmless tracked `evaluation/holdout/integrity-report.json` was
placed outside the repository. Before alteration, original and copy both hashed:

`38fa2373ce6c0fff8dc1e3ea3dcc3b128cc67b4baf6d58ec8c6d0fe95e68bca4`.

A clearly marked drill-only JSON field was added to the copy. Its SHA-256 became:

`787efafa95f9ebc73ac88a3af9c4690e7b34fb735ac03f94f7550faa74564d9a`.

The altered copy was then deleted; the tracked original was never edited. This
demonstrates detection of identity/integrity mismatch. It does not establish
which copy is authentic, whether either is safe, or whether alteration is
malicious—those conclusions require trusted provenance and context.

## 29. Research-evidence survival table

| Evidence | Tracked / hashed | Historical? | Regenerable / safe? | Requires original? | Recovery location | Loss impact |
|---|---|---|---|---|---|---|
| v0.2 H0 | yes / exact file SHA | primary confirmatory pilot | **not safely regenerable as original** | yes | authoritative JSON in `evaluation/runs` + Git | critical: primary result/provenance lost |
| Day 3C | yes / exact file SHA | post-unblinding analysis | text may be rederived, but not as original evidence | yes for provenance | tracked Markdown | high: failure taxonomy/provenance weakened |
| Reviewer source | yes / exact file SHA | pre-H0 blinded review | no | yes | `evaluation/holdout/reviewer-source.md` | critical: independent-review source lost |
| Review ledger | yes / source hash linked; ledger itself not in critical hash table | adjudication record | should not be reconstructed silently | yes | `evaluation/holdout/review-ledger.md` | high: R08/agreement trail weakened |
| Development corpus | yes / aggregate corpus identity | frozen v1.0.0 development | files technically recreatable only as new version, not original | yes for historical metrics | `evaluation/corpus` | high: regression history lost |
| Holdout 1.0.1 | yes / aggregate corpus identity | exposed historical holdout | never regenerate/overwrite as same corpus | yes | `evaluation/holdout` | critical: H0 sample/label identity lost |
| v0.3 exploratory corpus | yes / aggregate corpus identity | post-unblinding development | may create new version, not replace original | yes for historical v0.3 work | `evaluation/exploratory/v0_3` | high: mechanism-test provenance lost |
| v0.3 exposed result | yes / exact file SHA | exploratory | must not be regenerated as original | yes | Day 4C primary JSON | critical for honest status/comparison |
| Secondary H0 ablations/H1 | selected items tracked and inventoried | secondary | derived calculations may be repeated descriptively; original bytes preferred | original for citation/provenance | `evaluation/runs` | medium/high depending thesis citation |
| Day 3D/4A/4B/4C support | selected historical set tracked | secondary/exploratory | some derived items regenerable; dirty provenance cautions | originals preferred | tracked run subdirectories | medium/high |
| Release documentation | yes; Git/tag identity | release | can restore from Git commit | yes for exact history | `docs/releases`, tag | high for release interpretation |
| Day 6/proposal/training docs | yes; Git history | continuity/planning | prose could be rewritten but would lose reviewed state | tracked original preferred | `docs/` | high for student continuity, low for detector execution |

## 30. Windows recovery runbook

The sequence deliberately omits any holdout evaluation command.

```powershell
# 1. Recover exact tracked state without CRLF conversion.
git clone -c core.autocrlf=false https://github.com/danveil/mcp-security-inspector.git
Set-Location mcp-security-inspector
git rev-parse HEAD
git status --porcelain
git rev-parse "v0.3.0a1^{}"
git cat-file -t v0.3.0a1

# 2. Create a clean supported environment.
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pip check

# 3. Engineering verification.
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m mypy src
.\.venv\Scripts\python.exe -m pytest --cov=mcpsec --cov-report=term-missing
.\.venv\Scripts\python.exe -m build
$wheel = (Get-ChildItem dist\*.whl | Select-Object -First 1).FullName
.\.venv\Scripts\python.exe scripts\smoke_wheel.py $wheel

# 4. Verify preserved exact-byte evidence; compare output to the recovery manifest.
Get-FileHash -Algorithm SHA256 `
  evaluation\runs\exp-20260827T060056391880Z-c514ba03-a660fd6d.json, `
  evaluation\runs\day3c-deep-failure-analysis.md, `
  evaluation\runs\day4c\post-unblinding-exploratory-holdout-full-analysis-core.json, `
  evaluation\holdout\reviewer-source.md

# 5. Detector-free corpus identity verification.
.\.venv\Scripts\python.exe -c "from pathlib import Path; from mcpsec.evaluation.integrity import corpus_sha256; paths=['evaluation/corpus/manifest.json','evaluation/holdout/manifest.json','evaluation/exploratory/v0_3/manifest.json']; [print(p, corpus_sha256(Path(p))) for p in paths]"
```

Do not add `mcpsec evaluate evaluation/holdout/manifest.json` to this runbook.

## 31. Linux recovery notes

**CI-EVIDENCED:** Ubuntu + Python 3.12 installs `.[dev]`, runs Ruff, format, mypy,
pytest/coverage, builds/smokes a wheel, evaluates only the development corpus, and
scans an offline clean example. Substitute `.venv/bin/python` and
`.venv/bin/mcpsec`; quote wheel globs as appropriate for the shell.

**NOT DAY 6K LOCALLY VERIFIED:** Linux clean-room behavior, distribution hashes,
terminal rendering and timings. LF is normally native, but hashes must still be
verified. Do not convert CI evidence into a claim of exhaustive Linux support.

## 32. Five-years-later checklist

- [ ] Obtain a full clone or verified Git bundle, not only a source ZIP.
- [ ] Confirm expected current recovery commit before interpreting later changes.
- [ ] Confirm `v0.3.0a1` is still an annotated tag at `3744710...`.
- [ ] Use an available Python compatible with the recorded `>=3.12` policy.
- [ ] Inspect dependency bounds, index availability and archived wheels before install.
- [ ] Clone with `core.autocrlf=false` and verify every critical digest.
- [ ] Identify H0 as `exp-20260827T060056391880Z-c514ba03-a660fd6d.json`.
- [ ] State that H0 is the authoritative first confirmatory result within the pilot.
- [ ] Identify Day 4C as post-unblinding exploratory on the exposed holdout.
- [ ] Never overwrite H0, Day 3C, Day 4C, reviewer source/ledger or corpus versions.
- [ ] Recompute metrics only from preserved matrices/labels unless a new protocol exists.
- [ ] Keep H0 configuration `a660fd...` separate from current defaults.
- [ ] Keep v0.3 exploratory configuration `3cee3f...` separate from H0.
- [ ] Remember the exposed holdout cannot provide fresh v0.3 confirmation.
- [ ] Review the P0 finding-budget decision-coupling defect before a future freeze.
- [ ] Check whether newer code still loads historical schema 3.0.0 safely.
- [ ] Treat ignored/local baselines, caches and builds as non-authoritative.
- [ ] Obtain supervisor approval for construct, engineering gates and study protocol.
- [ ] Use genuinely untouched, independently governed data for future confirmation.
- [ ] Preserve raw future artifacts immediately and label all later work post-unblinding.

## 33. Supervisor/examiner verification script (3–5 minutes)

“The pilot result is preserved as a specific tracked JSON artifact. First, check
out the documented Git commit and confirm the annotated release/history rather
than trusting my current working directory. Second, compute the H0 artifact's
SHA-256 and compare it with the independently repeated value
`3307c28d...71b80`. The artifact self-describes the holdout identity
`c514ba03...a2d8`, configuration `a660fd...f9a1`, historical rules, Git state,
runtime, matrix and per-sample evidence. Third, use the detector-free corpus hash
function to verify that the manifest and referenced sample population still bind
to that corpus identity. Fourth, verify the blinded reviewer source hash and its
ledger: 47/48 agreement, one retained disagreement and the unchanged individual
judgments. Finally, independently calculate the reported metrics from 5 TP, 18 TN,
6 FP and 19 FN. The calculation matches the artifact.

This chain makes silent modification detectable when compared with trusted
digests and Git history. It does not make an unkeyed hash independent proof of
authorship, nor does it make the synthetic pilot externally valid. The later v0.3
artifact has a different configuration and explicitly dirty, post-unblinding
provenance. It is exploratory and cannot replace H0 or prove generalization.”

## 34. Reproducibility claims register

| Claim | Supported? | Evidence | Safe wording / overclaim to avoid |
|---|---|---|---|
| Current tracked state can be recovered from a full clone | yes | clean 214-path clone | “Recovered at this commit”; avoid “GitHub can never lose it.” |
| Day 6 documents survive a clone | yes | all named files present | Avoid saying local ignored state is also preserved. |
| Historical annotated tag survives | yes | object type/tag target | Avoid moving it to current main. |
| Repository installs from a clean clone | yes, today | isolated 3.12 installation | Qualify by Windows/date/index availability. |
| Dependencies are exactly reproducible | no | ranges/no lock | Say “compatible resolution succeeded”; avoid “same environment forever.” |
| Ruff and strict mypy pass | yes | clean-clone gates | Scope to this commit/resolved tools. |
| Normal tests pass | yes | 472/472, 92.95% | Avoid implying tests prove production security. |
| Tests reran the exposed holdout | no | pre-test path inspection | They read frozen artifacts and evaluate development/synthetic fixtures. |
| Wheel and sdist can be built | yes | clean build outputs | Functional packaging reproduction. |
| Build is byte-for-byte reproducible | unsupported | new/local hashes differ; no protocol | Explicitly say not established. |
| Built wheel works in a new environment | yes | repository smoke script | Version/help/demo only, not every deployment scenario. |
| CLI performs no network I/O ever | false | optional `fetch` exists; pip needed for install | Say static scan is offline/default; retrieval is explicit loopback-only. |
| H0 artifact is byte-identical | yes against expected digest | exact SHA match in both clones | Hash comparison needs trusted expected provenance. |
| H0 arithmetic is reproducible | yes | independent formulas match artifact | Does not equal experimental replication. |
| H0 proves effective detection | no | recall 20.83%, FPR 25% | Report result honestly; avoid production assurance. |
| v0.3 artifact is byte-identical | yes against expected digest | exact SHA match | Preserve its dirty/exploratory provenance. |
| v0.3 improved generalization | unsupported | same exposed holdout informed rules | Say point estimates increased on exposed data. |
| Corpus identities are reproducible | yes | detector-free function matches all three | Describe aggregate semantics; do not call raw file hashes. |
| Reviewer agreement arithmetic is reproducible | yes | source/ledger and kappa calculation | Does not prove label truth or detector validity. |
| `.gitattributes` mitigates known CRLF risk | yes for tested scoped files | default and LF-safe clones match | Avoid “all future files are protected automatically.” |
| Full Git history supports chronology | yes | 15 commits, tags and anchors | Some stages are artifact- rather than unique-commit anchored. |
| Source ZIP is equivalent to full clone | no | tag/history object analysis | ZIP retains current files, not history/tag provenance. |
| Windows is clean-room verified | yes | Day 6K | One host/runtime, not every Windows configuration. |
| Linux is supported by evidence | qualified | CI Ubuntu/Python 3.12 | CI-evidenced, not Day 6K locally verified. |
| macOS is verified | no | no workflow/run found | Call it unverified. |
| Study is independently replicated | no | no fresh untouched study | Future supervisor-approved work required. |

## 35. Hidden assumptions discovered

| Assumption | Evidence/impact |
|---|---|
| A Python 3.12 interpreter can be obtained | No system Python was on PATH; Day 6K used an installed bundled 3.12.13 runtime. |
| Package index/network remains available | initial isolated install/build failed without network; dependencies are not vendored. |
| Resolver choices remain compatible | lower/major bounds allow moving versions; no exact lock. |
| Git is available and full history is cloned | ZIP cannot reproduce tag/ancestry evidence. |
| Correct Git newline policy is used | global Windows autocrlf was true; scoped attributes and LF-safe clone mitigated known files. |
| UTF-8 input assumptions hold | bounded readers decode UTF-8; wheel smoke forces UTF-8 subprocess behavior. |
| Current working directory is repository root for relative commands | runbooks and several scripts use relative paths. |
| File ordering is deterministic where identity matters | code sorts manifest/file/key collections; unsorted additions could destabilize results. |
| Filesystem/path semantics are compatible | Windows vs Linux separators/case/path length differ. |
| Rich console output has a functioning consumer | early-closing PowerShell pipeline produced an OSError; normal/captured output passed. |
| Timing environment is comparable | machine identifier was blank in historical/Day 6K Python platform metadata; timing remains host/load dependent. |
| Git expected hashes come from a trustworthy source | hashes stored beside data can be replaced together. |
| Baselines and suppressions are operator-approved | local configuration can legitimize drift or hide findings; not needed for H0. |
| Optional local MCP response is hostile but reachable | relevant only to explicit retrieval, never offline evidence verification. |
| Historical dirty state is interpreted honestly | Day 4C commit alone cannot reconstruct its exact source tree. |
| External privacy/redistribution decisions remain valid | two historical files retain local creation paths; no secrets found. |

## 36. Future reproducibility backlog

### P0 — before formal confirmatory FYP work

1. Resolve finding-budget coupling so retention cannot change risk, fail-on,
   affected counts or evaluation predictions; add overflow invariance tests.
2. Freeze a supervisor-approved construct/threat model and experiment protocol.
3. Create a clean, versioned candidate and untouched-data access/freeze process;
   do not reuse the exposed holdout as fresh evidence.
4. Preserve future raw artifact, corpus/config/rule identities and environment
   metadata before analysis; prohibit silent reruns/overwrites.
5. Define label/reviewer, ethics, leakage and sample-size/statistics procedures.

### P1 — strongly desirable

1. Adopt reviewed constraints/lock files and a hashed wheelhouse/archive strategy
   for formal experimental platforms.
2. Add independently held or signed release/evidence manifests; preserve a full
   Git bundle and its digest outside the repository.
3. Extend `.gitattributes`/hash-manifest review to every future frozen byte-sensitive
   file, including review/adjudication records where exact bytes matter.
4. Capture architecture/toolchain/resolver information more reliably; the current
   Python `platform.machine()` record can be blank.
5. Add Windows/Linux clean-room automation and test Rich output piping behavior;
   add macOS only if support is claimed.
6. Decide whether remaining `work/day2b2-*` evidence deserves an independently
   checksummed supplementary archive or is safe to discard.

### P2 — useful improvements

1. Document offline installation from a wheelhouse and periodic recovery drills.
2. Add a machine-readable tracked evidence manifest without self-hash recursion.
3. Record reproducible-build requirements if byte-identical distributions become
   a project goal.
4. Provide normalized path provenance fields for future artifacts while preserving
   historical originals.
5. Test source-ZIP recovery as a clearly lower-assurance fallback.

No backlog item was implemented during Day 6K.

## 37. Final mutation and safety record

The only intended primary-worktree addition is this document. No tracked path
under `src/`, `tests/`, `rules/` or `evaluation/` was modified. The temporary
corruption copy was deleted. Recovery clones, virtual environments, caches and
build outputs were isolated outside the primary repository and are disposable.

No exposed holdout was rerun. No detector experiment, tuning, rule/threshold/risk
change, corpus/label mutation, artifact rewrite, commit, push, tag or release was
performed.
