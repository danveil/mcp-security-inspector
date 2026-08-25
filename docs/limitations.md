# Limitations

- Rule-based detection cannot guarantee that a tool is safe.
- A clean scan does not mean a tool or server is trusted.
- A suspicious scan does not necessarily mean malicious intent.
- Runtime behavior can differ from advertised metadata.
- The project analyzes metadata, not implementation code.
- Heuristics are English-oriented and category mappings are deliberately simple.
- Referenced remote JSON Schemas are not fetched; validation is structural and offline.
- Rename inference is intentionally conservative and can miss renamed-and-edited tools.
- Encoded blocks are detected but not semantically interpreted or executed.
- Baselines protect integrity only when their own storage and review process are trusted.
- Human review remains necessary.
- Bundled evaluation results apply only to the small synthetic corpus and are not real-world accuracy claims.
- English-oriented phrase context remains difficult: quotation, negation, privacy language, and generic schema words cause known false positives.
- Informational capability findings and low-severity presentation anomalies remain below the default binary evaluation threshold.
- MCP retrieval is deliberately limited to explicit localhost/loopback Streamable HTTP endpoints; it does not support arbitrary remote URLs or spawning stdio commands.
