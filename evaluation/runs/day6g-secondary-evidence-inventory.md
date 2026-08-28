# Day 6G Secondary Research Evidence Inventory

## Status and selection rule

This inventory records the previously ignored Day 3/Day 4 material selected
for the Day 6G preservation checkpoint. Selection was based on scientific,
thesis, provenance, and reproducibility value—not on favorable results. These
files do not replace the three primary immutable evidence files and do not make
the exposed holdout fresh.

The selected package contains 45 files (4,578,736 bytes before this inventory):

| Group | Classification | Reason |
|---|---|---|
| Day 3B inventory, H1 timing, and seven H0 ablations | **A — MUST PRESERVE IN GIT** | Exact preregistered secondary-run identities and timings cited by Day 3D/Day 6 |
| Day 3D results/discussion/table/figure/viva bundle | **A — MUST PRESERVE IN GIT** | Thesis-ready synthesis with explicit confirmatory/descriptive claim boundaries |
| Day 4A exploratory design | **A — MUST PRESERVE IN GIT** | Records post-unblinding hypotheses, rejected ideas, and the design lineage of v0.3 |
| Day 4C JSON, analyses, and helper | **A — MUST PRESERVE IN GIT** | Exact exploratory provenance cannot be recreated from the recorded clean commit because the source was dirty; files support the published interpretation |
| Day 4B development/exploratory artifacts | **B — SHOULD PRESERVE IN GIT** | Partly duplicated by Day 4C, but small and useful for the chronology and dirty-state implementation checkpoint |
| Virtual environments, caches, coverage, build outputs | **D — REGENERABLE / SAFE TO LOSE** | Environment/transient output, not research evidence |
| Secrets, credentials, private keys | **E — SHOULD NOT PRESERVE** | None were selected |

No category-C file remains in this selected 45-file set. An independent Git
bundle is still recommended as a second preservation channel.

## Scientific and privacy boundary

- H0 remains the authoritative first confirmatory pilot result.
- Day 3C/Day 3D interpretations are post-unblinding descriptive where stated.
- Day 4A/Day 4B/Day 4C detector-improvement material remains post-unblinding
  exploratory.
- The selected artifacts contain synthetic research metadata and sample-level
  predictions for an already exposed holdout; they are not fresh evidence.
- No API credential, private key, `.env` content, or real secret was identified.
- The Day 4A historical design record and the Day 6E final adversarial review
  contain their creation-time local repository root. They are retained
  unchanged as historical provenance and must not be copied into new public
  artifacts as required paths.
- `analysis_snapshot.py` is a historical analysis helper. It reads preserved
  JSON and prints a derived summary; it is not production code and was not
  executed during Day 6G. An explicit Day 6G Ruff audit found two E501
  line-length findings and a formatting delta. Its original bytes are
  intentionally preserved instead of rewriting historical provenance; the
  normal repository quality gate continues to exclude ignored run material.

## Exact selected-file identities

```text
A  daadd90f9d57c39edf7535fdb0197bbd1be3148e324ae41d88d9efa46aad426c  evaluation/runs/day3b-artifact-inventory.json
A  34ca72d23d45f815bff284cc7745b39e258849176c78d0119367861b60c4421d  evaluation/runs/day3d/claims-register.md
A  6eb1f43d9c7b35b12feb6d7453bcb3b01b93bb86cb0822ed843849665afef838  evaluation/runs/day3d/day3d-summary.md
A  d00b49acda0368cf3c164c60051861e62dd67f385ca50375fa9a0ef6d7ca7e3e  evaluation/runs/day3d/discussion-evidence.md
A  c62a924ea033122a7890241e720b6be0a58b1d04909e8d0cdbda74675191dca9  evaluation/runs/day3d/figure-specifications.md
A  986e50ddcbbe36011277d1565379736cf2048f289779a259a117694c311ccd7e  evaluation/runs/day3d/results-evidence.md
A  5250513f59dbff1e194ec684c551c8981d0611e70ce69824834be82cdef54275  evaluation/runs/day3d/tables.md
A  c3319052f4e6ef3081b065a80c5c894b3914b5326a5b3b788e740b99b51d140f  evaluation/runs/day3d/viva-evidence.md
A  884142b2e17ef1c6ef9d5b3a2fc2092a31612067c0a3ef60ac61b93d382d8601  evaluation/runs/day4a/day4a-exploratory-improvement-design.md
B  56482ac679f5779f4ad0ad32d6f19145c8244ad61fc4eb66cabdc3d46d2b400d  evaluation/runs/day4b/development-analysis-core.json
B  1a6a29d1a2bac16d50e629cc709d1c95d9246565c9763c063e06c63bf9cc5373  evaluation/runs/day4b/development-static-end-to-end.json
B  d2a251a14e14cf03141b3bb4ceb54400c1ecf0969811dd81b0e35902afaedeb1  evaluation/runs/day4b/exploratory-analysis-core.json
B  301d5e2f8eed3c9fd4eefa759ea0e8fbddda6ea018a6f9fae294cb3a3b627692  evaluation/runs/day4b/exploratory-static-end-to-end.json
A  a4325eae6b9f702fdd78786ad1562454c14471a44b955eb782acb76018e028f2  evaluation/runs/day4c/analysis_snapshot.py
A  4862a580a7b73ef3395300118ae207e1de78177ed4dedb86ecea94c8ebc6a132  evaluation/runs/day4c/development-full.json
A  8a50fb21b77bb695776fbf4a389cbb1c6047056d8f753c457c62fa6e8c956cf8  evaluation/runs/day4c/development-without-hid-002.json
A  973c86a30bfc81147d8a3fc63dc6957f9c70a782a979801f1b056aca94c0fed9  evaluation/runs/day4c/development-without-mis-002.json
A  ee042b4ff51f28fa5d5978e1e0e15fd7bac92334ef4c8b292ed62613aa1d78a5  evaluation/runs/day4c/development-without-obf-005.json
A  7acbf94ca36e26708396684027533c8abcd5a86d174512c04b706e488a179b3e  evaluation/runs/day4c/development-without-pi-002.json
A  01b0c521fd57500c707b6458157c3a78c137509498544828aaabd5397e11aabf  evaluation/runs/day4c/development-without-sec-002.json
A  c1b4dbcb898a6ffe174afac301d39e0ddfeb4d4c81ca27569c02f4c881990c08  evaluation/runs/day4c/exploratory-fixtures-full.json
A  ce68a4cdd1f325762be1f680eed67b4e9ec43e30822ffd3a0b1eff620724d351  evaluation/runs/day4c/exploratory-fixtures-without-hid-002.json
A  0af8e298c0c5929d5eeb08b49f4ba0cca5ebf4a8789cd88e4124e188c5b643f5  evaluation/runs/day4c/exploratory-fixtures-without-mis-002.json
A  46a0b184471b2a6b91f16b3eb299ab4cc797ad0443141cabd76cadc7f5f99cb3  evaluation/runs/day4c/exploratory-fixtures-without-obf-005.json
A  681fa361be60ebdfeeebfb67362e3f9b071153e4e05f58eb2e4626a68a72c204  evaluation/runs/day4c/exploratory-fixtures-without-pi-002.json
A  d6191f5f9b8706700db9e68e0a80bfe4d3f730b6b3a6550e3a6e1bc9026a666e  evaluation/runs/day4c/exploratory-fixtures-without-sec-002.json
A  1dda3f9c431edd257fb7de2a1e3dd65108df0205f65e7c0896db5246450567e2  evaluation/runs/day4c/failure-recovery-map.md
A  1ade12bdf0fb2a49dac78b426a71ea083705962343b80da5205b63e914784f81  evaluation/runs/day4c/performance-comparison.md
A  046c4ea0aaafe9f4b561d1d3544b7735e1d81a72af26007cece984d4187b5c2f  evaluation/runs/day4c/post-unblinding-exploratory-holdout-full-static-end-to-end.json
A  6dfd64ebd50ed914f4bb8279f38692593b7afcafa59c58c3b5b3f644e2f8eddf  evaluation/runs/day4c/post-unblinding-exploratory-holdout-without-hid-002.json
A  ffe3af47864266637b2af3fbe80a8d324e7d37f8ffbedc62b9d7134c8a750890  evaluation/runs/day4c/post-unblinding-exploratory-holdout-without-mis-002.json
A  221c982c58325004b3e7b7c30942b8e9cdc6a80058725c4e8244e217a69d9728  evaluation/runs/day4c/post-unblinding-exploratory-holdout-without-obf-005.json
A  e781ffbd6d387a8769f45134ea2e51b30538cbbf47a804e6fe2098376706b6bd  evaluation/runs/day4c/post-unblinding-exploratory-holdout-without-pi-002.json
A  75d2c3236cbac327a86c4e3b57a7c59812c1ddc77dcbd1edd1b48df80265ae28  evaluation/runs/day4c/post-unblinding-exploratory-holdout-without-sec-002.json
A  a3cace8c6df9c781c2cb019be477838591ce525f339681d970a4f44cfcbe80bd  evaluation/runs/day4c/rule-contribution.md
A  fdb9a68b131635aeefbdb9ab39c692fab0b51745eddae43aa78af25b9ccc1219  evaluation/runs/day4c/v02-v03-comparison.md
A  3c9112fbb90b8af2e55df66c7edc2fb84ed73efb2b299dbc660f4cffde223608  evaluation/runs/day4c/v03-exploratory-summary.md
A  969b3fecea24f93e2fd5a578152f0e3620ba237a1088552443125c2916bff7af  evaluation/runs/exp-20260827T060157485815Z-c514ba03-cde99024.json
A  b9829eb9f129894ad50fca458988f2a64b893885b233e3f29535d6dbe3184937  evaluation/runs/exp-20260827T060254063218Z-c514ba03-2fdd6d66.json
A  7fe662dd5b208eae8685be1322c9a58a3f9e85042e3f8794dfc219b9d6a9353e  evaluation/runs/exp-20260827T060257853936Z-c514ba03-f02a443b.json
A  9953343f189ee66e8ff826c6d3b2303b047277b0ba0e23cccbe9f38edd6255c7  evaluation/runs/exp-20260827T060259610698Z-c514ba03-8f81f058.json
A  7b5502777777cb0ad20bc0d0d011b58cab5e75a7bf7a4ad14f2e5c65228187ce  evaluation/runs/exp-20260827T060302489565Z-c514ba03-1a982507.json
A  99fdd5b8fd33ddae5ec0717f8eb174bbe8228a472e2b09bc00ed384734afd77e  evaluation/runs/exp-20260827T060305429500Z-c514ba03-7e77de9a.json
A  0e3234ec56d031e3d7eac95d25d9ae0549f4e9f0e904c905b437808fe5814875  evaluation/runs/exp-20260827T060308496807Z-c514ba03-fe437481.json
A  e192b7e386b579336fb16886a01a7c6c5e3ac2db755e5f8f986d36e92efec091  evaluation/runs/exp-20260827T060311632569Z-c514ba03-416700af.json
```

The hashes above identify the original selected files before staging. Git
attributes preserve their bytes; no corpus or detector was executed to create
this inventory.
