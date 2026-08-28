# Final Preservation Manifest

> **Archive role:** compact human-readable and machine-readable index for the
> preserved MCP Tool Security Inspector pre-FYP prototype/pilot checkpoint.
> **Audited:** 2026-08-29 (Asia/Kuala_Lumpur). This document creates no new
> scientific evidence and does not supersede a frozen artifact.

If this manifest conflicts with a frozen artifact, **the frozen artifact wins
for historical result content**. If it conflicts with implementation behavior,
**current source and tests win**. Git and SHA-256 establish identity relative to
trusted reference values; they do not establish safety, truth or authorship.

## 1. Archive identity

| Field | Audited value |
|---|---|
| Project | MCP Tool Security Inspector |
| Scientific stage | PRE-FYP RESEARCH PROTOTYPE / PILOT STUDY |
| Branch | `main` |
| Audited HEAD | `82499f6313638e2ec2dfa62cb7e8ff05452968f9` |
| Local `origin/main` tracking ref | `82499f6313638e2ec2dfa62cb7e8ff05452968f9` |
| Starting worktree | clean |
| Historical tag | annotated `v0.3.0a1` |
| Tag object | `732f76c381c893942e8ca159b590444c9a6724c8` |
| Tag commit target | `374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad` |
| Package / built-in rule pack | `0.3.0a1` / `builtin` `2.0.0` |
| Current artifact schema | `3.1.0` |
| Supported artifact schemas | `3.0.0`, `3.1.0` |
| Current repository inventory | 216 tracked paths |

`origin/main` above is the locally stored tracking ref, not a claim that the
live hosting service was independently queried during this audit. The
historical release tag predates later documentation commits and must not move.

### Machine-readable preservation record

```json
{
  "format": "mcpsec-final-preservation-manifest-1",
  "audited_date": "2026-08-29",
  "scientific_stage": "pre-fyp-prototype-pilot",
  "head": "82499f6313638e2ec2dfa62cb7e8ff05452968f9",
  "origin_main_tracking_ref": "82499f6313638e2ec2dfa62cb7e8ff05452968f9",
  "historical_tag": {
    "name": "v0.3.0a1",
    "object": "732f76c381c893942e8ca159b590444c9a6724c8",
    "target": "374471094fd83f4f8b2d4816a7fcb2cdeccbf3ad"
  },
  "versions": {
    "package": "0.3.0a1",
    "builtin_rule_pack": "2.0.0",
    "artifact_schema_current": "3.1.0",
    "artifact_schemas_supported": ["3.0.0", "3.1.0"]
  },
  "research_status": {
    "v0_2_h0": "authoritative-confirmatory-within-pre-fyp-pilot",
    "v0_3": "post-unblinding-exploratory-only",
    "formal_fyp_evidence": "not-created",
    "exposed_holdout_reusable_for_confirmation": false
  },
  "p0_finding_budget_decision_coupling": "unresolved"
}
```

## 2. Scientific evidence identities

The first four identities below are raw-file SHA-256 values. The corpus values
are semantic corpus hashes calculated with
`mcpsec.evaluation.integrity.corpus_sha256`; they are not manifest-file hashes.

| Evidence | Repository path | Identity | Status |
|---|---|---|---|
| Authoritative H0 | `evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json` | `3307c28daca91132507abad116b771cbc4b505ab8c6e961e6ff33ed436871b80` | Preregistered/confirmatory within the pre-FYP pilot; immutable |
| Day 3C analysis | `evaluation/runs/day3c-deep-failure-analysis.md` | `deb97ce25609a1d267d8fd00212994c8493f929b6ee31141efcb0b4ff2f9332f` | Post-unblinding failure analysis; immutable |
| v0.3 diagnostic | `evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-analysis-core.json` | `d5d84dc33f3ca9091ed02b60d61aca4333206e92d4cecba0488c0f432643806b` | Post-unblinding exploratory only; immutable |
| Reviewer source | `evaluation/holdout/reviewer-source.md` | `857b20b5e138e67e7f684cb3784bfb0cd97831ff4a4cefdae6b6d6128465489c` | Original blinded response; immutable |
| Development corpus | `evaluation/corpus/manifest.json` | `a22de0126d2cf0b00c99ded46687b70dc6f417382a0a11c5ae4a9cad8f6d6f47` | 80-sample visible development/regression data |
| Reviewed holdout | `evaluation/holdout/manifest.json` | `c514ba03ac2ca6a6f67ec1e6cc7bb24f0347ccf51a98b0083bdaa53234f5a2d8` | 48-sample reviewed pilot holdout; now permanently exposed |
| Exploratory corpus | `evaluation/exploratory/v0_3/manifest.json` | `4209b93750ac4fd1a6445af13d891fa49954e0ba5e1b939d6c52b955060fbba4` | 36-sample post-unblinding development material |

Frozen configuration identities:

- H0: `a660fd6dcccf01d691dbfca3683f97aa5f2224cff0f895da602e0c9b2a94f9a1`.
- v0.3 exploratory primary:
  `3cee3f4d1bf73637498ea876d5c26c0b8bf8bab40b6be03284fc9ec5da839323`.

Historical artifacts retain their own package, rule-pack, schema, threshold and
Git provenance. Current defaults must not be substituted when interpreting them.

## 3. Verified historical results and review

| Evidence | TP | TN | FP | FN | N | Scientific interpretation |
|---|---:|---:|---:|---:|---:|---|
| v0.2 H0 | 5 | 18 | 6 | 19 | 48 | Authoritative first pilot result; not deployment performance |
| v0.3 exposed rerun | 11 | 18 | 6 | 13 | 48 | Diagnostic post-unblinding result; not fresh confirmation |

The review record contains all 48 decisions: 47 binary agreements, one
disagreement (`R08` / `holdout_s011` / `bounded_result_sampler`), zero
abstentions, reviewer totals 25 benign/23 suspicious, and original totals 24
benign/24 suspicious. Cohen's kappa is approximately 0.9583 and exact difficulty
agreement is 16/48. The reviewer source's summary line incorrectly says 24/24;
that historical typo remains preserved. The adjudication ledger corrects the
arithmetic without changing any individual judgment and retains the R08
ambiguity. Agreement does not validate detector effectiveness or objective label
truth.

## 4. Research status and claims boundary

### Supported today

- A deterministic, bounded, defensive static MCP metadata prototype exists.
- It has seven implemented detector families and 16 stable current rule IDs.
- Static scanning does not invoke discovered tools; optional retrieval is
  explicit, bounded and loopback-only.
- A frozen v0.2 pilot H0 artifact and independently reviewed label record exist.
- A transparent post-unblinding v0.3 diagnostic artifact exists.
- Engineering recovery succeeded on the recorded Windows/Python environment,
  and CI supplies Ubuntu/Python 3.12 evidence.
- Corpus, configuration, source, artifact and historical-schema identities are
  recorded for reproducibility and interpretation.

### Not established today

- v0.3 generalization or superiority on untouched data;
- production, operational or real-world effectiveness;
- performance under real deployment prevalence;
- state-of-the-art status or novelty;
- formal-FYP effectiveness;
- comprehensive MCP or runtime attack coverage;
- experimental replication on fresh independent data; or
- safety, authenticity or malicious intent from a hash, finding or clean scan.

The current work is engineering plus a controlled pilot and exploratory
follow-up. It is not a completed formal FYP and must not be presented as one.

## 5. Known P0 and bounded backlog

### P0 before a future detector freeze

Finding-output retention remains coupled to semantic decisions. In
`scanner.py`, risk is calculated from retained findings after per-tool/report
limits. In `evaluator.py`, additional report-cap truncation can recalculate risk
from a reduced list, and classification/categories use retained findings. The
same retained state feeds CLI `--fail-on` and affected-tool presentation.
Therefore later tools can appear risk-zero/benign solely because presentation
capacity was exhausted.

Required future architecture: separate **detection state**, **decision state**
and bounded **presentation/retention state**, then prove budget/order invariance
with regression, property and CLI/evaluation tests. Formal freeze must wait
because current predictions can be input-order/cap dependent at extreme finding
volumes.

The historical H0 and v0.3 artifacts were not affected: they retained 16 and 24
findings respectively, at most two per sample, with no sample marked truncated;
these are far below the 64-per-tool and 2,048-per-report limits. This does not
make the defect harmless for future/adversarial input.

Supervisor-controlled P0 methodology gates also remain: freeze the target
construct/threat model; approve statistics, data and review plans; and freeze a
clean candidate/protocol before untouched data is created or exposed.

### P1—important, not scope expansion

- adopt a reviewed constraints/lock/environment snapshot strategy;
- test worst-case intermediate resource use and finding pressure;
- define privacy-minimized reports, baseline provenance and suppression
  governance before operational or real-data use;
- preserve historical schema/risk interpretation and scoped newline policy; and
- add independent, realistic development/review perspectives if approved.

### P2—optional and research-question dependent

- controlled cross-machine benchmarks;
- signed attestations/SBOM or stronger provenance; and
- multilingual or broader ecosystem work only if the formal scope requires it.

## 6. Reproducibility and dependency status

The project requires Python `>=3.12`, uses `hatchling>=1.27` as build backend,
and specifies bounded runtime dependency ranges in `pyproject.toml`. Development
tools are optional dependency ranges. There is no exact lockfile or constraints
set. CI runs Ubuntu with Python 3.12; the preserved Day 6K clean-room drill used
Windows with Python 3.12.13.

| Level | Status | Boundary |
|---|---|---|
| Source reproduction | Supported | Git commit/tag, tracked files, hashes and LF-safe recovery guidance exist |
| Functional engineering reproduction | Supported on recorded environments | Day 6K install/lint/type/test/build/smoke passed; current audit reconfirmed normal gates |
| Evidence/analysis verification | Supported | Immutable artifacts, corpus/config identities and compatibility-aware readers exist |
| Exact dependency reproduction | Not supported | Version ranges exist but no exact reviewed lock/archive |
| Experimental replication | Not established | No new independent corpus/run replicates the scientific result |

Current audit quality snapshot: Ruff lint passed; Ruff format check reported 125
files formatted; strict mypy passed for 43 source files; 472 tests passed with
92.95% coverage. Tests touching H0/v0.3 load preserved artifacts rather than
rerunning the exposed corpus. These are engineering checks, not effectiveness
evidence. A non-fatal coverage warning noted that `mcpsec` had previously been
imported; the final measured coverage matched the preserved 92.95% baseline.

## 7. Preservation, local state, privacy and paths

All known raw-hash critical artifacts, corpus files and reviewer source are
scoped `-text` in `.gitattributes`, protecting their checkout bytes from
`core.autocrlf`. Selected Day 6G documents and secondary evidence are similarly
protected. Later Day 6H–6L documents are tracked but not byte-frozen; this is
acceptable because they are continuity/training plans, not frozen scientific
results. **Future risk:** new byte-sensitive artifacts/reviewer records outside
existing patterns require an explicit scoped attribute and recorded hash before
freeze. Never broadly renormalize historical files.

Ignored state contains no critical scientific evidence:

| Class | Local items | Preservation decision |
|---|---|---|
| Disposable | `.coverage`, tool caches, `__pycache__`, broken venv | Safe to delete/recreate; not evidence |
| Regenerable | `.venv/`, `dist/` | Rebuild from verified source; local packages are not authenticated releases |
| Operator-local / potentially sensitive | `baseline.json` | Two-tool operational baseline; review before sharing; not research evidence |
| Secondary evidence | four `work/day2b2-*.json` files | Documented development/timing/ablation material; useful but superseded for core preservation |
| Critical scientific evidence | none ignored | Core artifacts/corpora/reviewer evidence are tracked |

A conservative tracked-file pattern scan found no obvious private-key header,
GitHub/OpenAI/AWS token, generic quoted credential assignment, credential file,
or `.env` secret. This is a pattern audit, not a proof that no sensitive text
exists.

Three tracked documents contain the same creation-time local Windows repository
path: `docs/final-adversarial-review.md`, the immutable Day 3C analysis, and the
tracked Day 4A exploratory design. Classification: historical provenance with
low privacy debt; no runtime dependency and no rewrite required. Relative venv
paths in documentation/scripts are portable command conventions. A `/tmp/`
reference in a retrieval test is synthetic test input.

## 8. Final evidence survival table

| Critical asset | Tracked | Identity verified | Byte-sensitive | Scientific status | Do not overwrite | Recovery source |
|---|---|---|---|---|---|---|
| H0 JSON | yes | raw SHA exact | yes, protected | pilot H0 | yes | recovery manifest / Git |
| Day 3C analysis | yes | raw SHA exact | yes, protected | post-unblinding analysis | yes | recovery manifest / Git |
| v0.3 primary JSON | yes | raw SHA exact | yes, protected | exploratory | yes | recovery manifest / Git |
| Reviewer source | yes | raw SHA exact | yes, protected | original blinded review | yes | recovery manifest / Git |
| Review ledger | yes | content audited | scientific record; not separately hash-frozen | adjudication | yes | Git / holdout docs |
| Development corpus | yes | semantic SHA exact | yes, protected | development | yes; new version for changes | recovery manifest / Git |
| Reviewed holdout | yes | semantic SHA exact | yes, protected | exposed historical pilot | yes | recovery manifest / Git |
| v0.3 construct corpus | yes | semantic SHA exact | yes, protected | exploratory development | yes; new version for changes | recovery manifest / Git |
| H0/v0.3 config identities | yes, in artifacts | exact | artifact-bound | historical configurations | yes | immutable artifacts |
| `v0.3.0a1` tag | yes | object and target exact | Git object | historical alpha release | never move/recreate | Git/tag verification |
| Secondary evidence inventory | yes | tracked inventory | protected | supporting historical evidence | preserve status labels | Git / Day 6G inventory |

## 9. Critical document index

All 14 high-value Day 6 continuity/training/FYP documents are tracked:

| Path | Purpose |
|---|---|
| `docs/captain-technical-map.md` | Repository architecture and evidence map |
| `docs/captains-manual.md` | Technical learning, research teaching and viva reference |
| `docs/fyp-handover.md` | Research continuity and formal-FYP resumption |
| `docs/disaster-recovery.md` | Reconstruction, backup and LF-safe recovery |
| `docs/recovery-manifest.md` | Prior critical identities and recovery procedure |
| `docs/final-adversarial-review.md` | Adversarial risk/validity review and P0/P1/P2 register |
| `docs/formal-fyp-blueprint.md` | Supervisor-dependent future methodology blueprint |
| `docs/code-ownership-training.md` | Student code-ownership and viva training |
| `docs/code-ownership-flashcards.md` | Compact ownership/research recall aid |
| `docs/fyp-proposal-seed-pack.md` | Proposal drafting inputs, not an approved proposal |
| `docs/fyp-literature-workbook.md` | Literature search/claim-verification plan, not evidence of novelty |
| `docs/research-code-walkthrough.md` | Guided source trace and controlled debugging exercises |
| `docs/clean-room-reproducibility-drill.md` | Day 6K recovery results and reproduction boundaries |
| `docs/thesis-evidence-blueprint.md` | Claim/table/figure provenance and thesis safeguards |

This manifest is the compact entry point; it does not replace those documents.

## 10. Repository health snapshot

At audit time the repository contains 216 tracked paths: 44 under `src/`, 31
under `tests/`, two under `rules/`, 85 under `evaluation/`, 32 under `docs/`, and
one CI workflow. Source, detector registry, test suite, rules, package metadata,
CI, corpora, reviewer records, frozen artifacts and continuity documentation are
present. The starting worktree was clean. Creation of this manifest is the only
authorized Day 6M change.

This is an archival completeness snapshot, not a security or performance metric.

## 11. Do-not-touch assets and forbidden next steps

Do not overwrite frozen artifacts, reviewed holdout bytes/labels, reviewer
judgments, historical configuration identities or the `v0.3.0a1` tag. Do not:

- use the exposed holdout as fresh confirmation;
- call the v0.3 exposed result confirmatory or validated generalization;
- tune rules, severities, threshold, risk or suppressions against exposed data;
- relabel historical samples or repair the reviewer-source typo in place;
- opportunistically rerun a poor future primary result;
- claim development performance as external effectiveness;
- claim production readiness, operational prevalence performance, novelty or
  state-of-the-art status without the required evidence; or
- publish/release from this preservation checkpoint without a separate approved
  release process.

Safe present work is limited to literature review, ownership training,
supervisor preparation, ethics/data questions, formal methodology design and
non-mutating preservation verification.

## 12. Formal-FYP restart and Captain return protocol

If returning months later:

1. Read this manifest.
2. Verify HEAD, clean status, tag object/target and critical hashes using
   `docs/recovery-manifest.md` and `docs/disaster-recovery.md`.
3. Read `docs/fyp-handover.md` and `docs/final-adversarial-review.md`.
4. Read `docs/formal-fyp-blueprint.md` and
   `docs/thesis-evidence-blueprint.md`.
5. Refresh code ownership with the walkthrough, training pack and flashcards.
6. Discuss framing, construct, RQs, objectives, literature, ethics, statistics
   and methodology with the supervisor; record approval.
7. Remediate the finding-budget P0 in a versioned development-only phase and
   pass regression/security/resource gates.
8. Freeze the approved candidate, threshold, rule/config identities and clean
   commit before holdout creation.
9. Create genuinely untouched data under approved authorship/leakage controls;
   conduct blinded review/adjudication; freeze labels and corpus hash.
10. Preregister metrics, uncertainty, exclusions, timing, comparisons, command,
    artifact path and stop/retry rules.
11. Run one primary evaluation, preserve/hash the raw artifact immediately, and
    separate preregistered analysis from every later exploratory action.

Do **not** begin by rerunning the exposed pilot holdout. Recovery and ownership
come before implementation; supervisor-approved methodology comes before a new
formal experiment.

## 13. Recovery pointers and campaign closure

Primary recovery instructions are in `docs/disaster-recovery.md`; exact prior
identities and LF-safe commands are in `docs/recovery-manifest.md`; verified
clean-room behavior and limitations are in
`docs/clean-room-reproducibility-drill.md`. Preserve an independent off-device
Git bundle or checksummed archive according to those guides; a Git working copy
and one remote are not independent trust anchors.

The current Codex development campaign is frozen and closed. No exposed holdout
was rerun, no detector experiment or scientific result was created, and no
detector, rule, corpus, label, threshold, risk model, review record or frozen
artifact was modified during this final audit. Future work begins only through
the restart protocol above.
