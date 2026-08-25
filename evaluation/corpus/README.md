# Synthetic evaluation corpus

This corpus contains 80 harmless static MCP tool definitions: 40 benign and 40 suspicious. It is designed for deterministic development experiments, including deliberately ambiguous security, administration, privacy, quotation, and encoded-fixture language. It contains no real secrets, operational exploit payloads, destructive commands, network dependency, or executable content.

`manifest.json` is the ground truth. Every entry selects one tool from a small catalog and records a unique ID, source type, binary label, expected detector categories, rationale, difficulty, and optional expected stable rule IDs. The evaluator validates paths, labels, category consistency, duplicate IDs, and selected tool names before scanning.

The corpus is synthetic. Results measure behavior on these examples only and are not evidence of real-world attack-detection accuracy. Changes to examples or labels require a corpus version change and an entry in `evaluation/CHANGELOG.md`.
