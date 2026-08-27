# Architecture

`mcpsec` is a deterministic, offline-first pipeline. `loader` enforces a 10 MiB, 100,000-node, 1,000-tool boundary and accepts a raw tool, arrays, `{tools: [...]}`, and JSON-RPC `{result: {tools: [...]}}`. An opt-in retrieval adapter can obtain only `tools/list` from an explicitly supplied localhost Streamable HTTP endpoint and save it as static JSON. `normalizer` maps camelCase and legacy snake_case keys into `ToolDefinition`, NFC-normalizes text, rejects strings or keys longer than 100,000 characters, and preserves unknown fields. If both forms of an alias are present they must normalize to equal values; conflicting or null/non-null pairs are rejected. Duplicate names are rejected because baseline identity would be ambiguous.

`canonicalizer` recursively orders object keys, preserves array order, removes irrelevant whitespace, rejects non-finite numbers, encodes UTF-8 with visible Unicode, and excludes source-path provenance from a tool's full fingerprint. `fingerprint` hashes canonical bytes with SHA-256.

Detectors consume normalized values only. They never mutate a definition. Instruction-override, concealment, and sensitive-data checks use sentence-bounded local context and scoped negation across individual, field-addressable text values; values are never concatenated. Structured capability signals retain category, original evidence, and exact paths so the mismatch detector can require purpose contradiction plus corroboration; capability alone remains informational under `CAP-001`.

The representation helper is a pure, depth-one decoder for four explicit text forms. Candidate input/output, per-field/per-tool counts, retained decoded text, strict UTF-8, printable ratio, and control characters are bounded before semantic matching. Decoded text is treated as hostile inert data: it is never executed, fetched, imported, recursively decoded, or submitted to a model. Built-ins otherwise use fixed regular expressions, while custom rules use case-insensitive literal containment. Findings feed the unchanged duplicate-resistant capped risk engine and inert reporters. Baselines retain full/component hashes plus field-name summaries, avoiding raw descriptions and schema values. Evaluation uses the same scan engine and does not maintain a separate detector path.

```mermaid
flowchart TD
  A[Static MCP JSON] --> L[Bounded loader]
  B[Opt-in localhost tools/list] --> L
  L --> N[Normalizer]
  N --> C[Canonicalizer + SHA-256]
  N --> D[Detectors + versioned rules]
  C --> BC[Baseline comparator]
  D --> R[Capped risk score]
  BC --> O[Reporting]
  R --> O
  O --> E[Versioned corpus evaluation + metrics]
```

Trust boundaries are the local input file, optional rule/suppression files, baseline files, explicit localhost endpoint, terminal, and report consumers. A centralized resource policy bounds bytes, strings, nesting, structure nodes, tools, rule fields/patterns, YAML aliases/nodes, response bytes, and pagination. The application does not invoke MCP tools, start supplied commands, follow metadata URLs, download icons, discover credentials, or spawn subprocesses. Retrieval uses a dedicated no-proxy, no-redirect HTTP transport that validates every request destination as loopback, pins `localhost` to a verified literal loopback address while retaining its HTTPS SNI, and enforces an overall timeout plus tool-count, page, wire-byte, and serialized-metadata limits. Static scanning remains the default and initializes no MCP client or network transport.
