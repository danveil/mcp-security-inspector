# Experiment plan template

Complete and freeze this plan before a scored holdout is unblinded. Leave unknown results blank; do not insert or infer holdout labels here.

## Study identity

- Study title:
- Researcher(s) and reviewer(s):
- Plan version and freeze timestamp (UTC):
- Research question:
- Primary hypothesis:
- Null hypothesis:
- Confirmatory analyses:
- Exploratory analyses, if any:

## Corpus and isolation

- Development manifest, version, split, and SHA-256:
- Holdout manifest, version, split, and SHA-256:
- Label-review status and reviewer independence:
- Provenance/license policy:
- Exact-overlap check artifact and result:
- Manual near-duplicate review method and result:
- Who can access holdout labels before unblinding:

## Frozen detector configuration

- Application version and Git commit:
- Working tree clean (`yes`/`no`; explain if no):
- Rule-pack name/version:
- Classification threshold:
- Enabled detector family and stable rule IDs:
- Ablation preset:
- Additional disabled family IDs:
- Additional disabled stable rule IDs:
- Custom rule-pack identity, configuration SHA-256, and file SHA-256:
- Suppression identities and file SHA-256:
- Full configuration SHA-256:

## Planned runs

List every confirmatory full or ablation run before unblinding.

| Run ID | Split | Purpose | Ablation/family/rule selection | Timing mode | Warm-ups | Measured repetitions |
|---|---|---|---|---|---:|---:|
|  |  |  |  |  |  |  |

## Outcomes and analysis

- Primary outcome and acceptance criterion:
- Stopping rule:
- Secondary outcomes:
- Required raw confusion counts:
- Planned category analysis:
- Planned strata (expected category, field location, difficulty, ground truth):
- Minimum-stratum interpretation rule (default: mark `n < 10` low evidence):
- Uncertainty method (default: Wilson score 95% for accuracy, recall, and FPR):
- Zero-denominator handling:
- Multiple-comparison or exploratory-label policy:
- Timing comparison eligibility rule:

## Execution environment

- Operating system/release:
- Machine architecture and processor description:
- Python version:
- Recorded dependency versions:
- Background-load/process-isolation controls:
- Reason this environment is suitable for any latency claims:

## Artifact handling

- Authoritative JSON destination:
- External immutable storage location:
- Artifact SHA-256 recording method:
- Retention period:
- Comparison direction (`B - A`) and planned pairs:
- Output schema version:

## Unblinding and deviations

- Authorized unblinding date/person:
- Post-unblinding tuning prohibition acknowledged:
- Procedure for versioning exploratory follow-up:
- Deviations from this frozen plan (complete only after execution):

## Results (complete after execution)

- Experiment IDs:
- Compatibility/warnings from artifact comparison:
- Primary and secondary results:
- Limitations and low-evidence strata:
- Confirmatory conclusion:
- Exploratory observations clearly labeled:
