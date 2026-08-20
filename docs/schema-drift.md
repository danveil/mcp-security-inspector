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

