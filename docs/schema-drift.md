# Schema drift

```text
Approved definition
        ↓
SHA-256 fingerprint + structural summary
        ↓
Future definition
        ↓
Component comparison
        ↓
Field-level drift finding
```

Changes are classified as new, removed, conservatively inferred rename, description, input schema, output schema, annotations, execution metadata, or other metadata. Compact mode reports changed fields and added/removed structural keys without printing giant schemas. `--verbose` expands both structural summaries. Hashes detect any canonical content change even when a compact summary looks unchanged.

Normalization uses NFC text, sorted object keys, preserved array order, no insignificant whitespace, and UTF-8 SHA-256 input. The source path is not part of a tool fingerprint.

New baselines include `format_version: "1.0"`; older files without it load with the same default. This provides a stable migration point for a future experimental integrity envelope without adding keys, signatures, or PKI to the core v0.2 workflow. Baseline trust still depends on protecting and reviewing the baseline file itself.
