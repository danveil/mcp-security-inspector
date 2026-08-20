# Architecture

`mcpsec` is a deterministic offline pipeline. `loader` enforces a 10 MiB limit and accepts a raw tool, arrays, `{tools: [...]}`, and JSON-RPC `{result: {tools: [...]}}`. `normalizer` maps camelCase and legacy snake_case keys into `ToolDefinition`, NFC-normalizes text, limits individual strings to 100,000 characters, and preserves unknown fields. Duplicate names are rejected because baseline identity would be ambiguous.

`canonicalizer` recursively orders object keys, preserves array order, removes irrelevant whitespace, rejects non-finite numbers, encodes UTF-8 with visible Unicode, and excludes source-path provenance from a tool's full fingerprint. `fingerprint` hashes canonical bytes with SHA-256.

Detectors consume normalized values only. They never mutate a definition. Built-ins use bounded regular expressions with fixed patterns; custom rules use case-insensitive literal containment. Findings feed the capped risk engine, then inert reporters. Baselines retain full/component hashes plus field-name summaries, avoiding raw descriptions and schema values.

Trust boundaries are the local input file, optional rule file, terminal, and report consumers. The application does not invoke MCP tools, start servers, fetch URLs/icons, discover credentials, or spawn subprocesses.

