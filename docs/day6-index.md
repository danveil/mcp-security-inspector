# Research continuity and technical documentation

This page is the entry point to the project's Day 6 knowledge-preservation
package. The documents capture the pre-FYP prototype, its evidence boundaries,
recovery procedure, and a supervisor-dependent path toward a formal FYP. They
do not create new detector evidence or upgrade the exposed v0.3 result to
confirmation.

## Recommended reading order

1. [Technical map](captain-technical-map.md)
2. [Captain's Manual](captains-manual.md)
3. [Final adversarial review](final-adversarial-review.md)
4. [FYP handover](fyp-handover.md)
5. [Formal FYP blueprint](formal-fyp-blueprint.md)
6. [Disaster-recovery guide](disaster-recovery.md)
7. [Recovery manifest](recovery-manifest.md)

## Document guide

| Document | What it is | When to read it | Intended reader |
|---|---|---|---|
| [Technical map](captain-technical-map.md) | Repository-grounded architecture, module, detector, evidence, and dependency map | First, when learning or locating the system | Student, maintainer, technical reviewer |
| [Captain's Manual](captains-manual.md) | Teaching manual covering MCP, security mechanisms, research methods, debugging, exercises, and viva preparation | After the map and before modifying or defending the project | Student and FYP candidate |
| [Final adversarial review](final-adversarial-review.md) | Independent-style challenge of security, construct validity, statistics, reproducibility, claims, and remaining risks | Before proposing formal conclusions or new research | Student, supervisor, examiner, security reviewer |
| [FYP handover](fyp-handover.md) | Continuity guide for resuming work without rewriting history or contaminating future evidence | At project resumption and before formal planning | Student, supervisor, future maintainer |
| [Formal FYP blueprint](formal-fyp-blueprint.md) | Design-only candidate framing, threat model, research questions, engineering gates, future holdout protocol, and backlog | During supervisor and methodology discussions | Student and supervisor |
| [Disaster-recovery guide](disaster-recovery.md) | Practical reconstruction, verification, backup, failure, and LF-safe recovery procedure | Before backup and after loss, corruption, or a long absence | Student, maintainer, recovery operator |
| [Recovery manifest](recovery-manifest.md) | Compact identities, hashes, scientific invariants, and verification commands | During checkpoint, archive, clone, or evidence verification | Reproducibility reviewer and recovery operator |

The v0.2 H0 remains the authoritative first confirmatory pilot result. The
v0.3.0a1 result remains post-unblinding exploratory, and a future confirmatory
claim requires a new untouched protocol and corpus approved by the supervisor.
