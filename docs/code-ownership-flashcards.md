# MCP Tool Security Inspector Flashcards

These cards support recall after active exercises. They do not replace code
tracing or viva practice. All examples are **TRAINING ONLY — NOT RESEARCH DATA**.

| QUESTION | ANSWER | CATEGORY | DIFFICULTY |
|---|---|---|---|
| 1. What is MCP? | A protocol through which AI hosts/clients discover and use capabilities exposed by MCP servers. | MCP | Deckhand |
| 2. What is an MCP tool definition? | Metadata describing a named operation, including description, schemas and optional metadata. | MCP | Deckhand |
| 3. Why can tool metadata be security-significant? | An agent may read and reason over it before deciding whether or how to use a tool. | Security | Deckhand |
| 4. What is this project’s default boundary? | Deterministic static analysis; it does not invoke scanned tools or execute metadata. | Security | Deckhand |
| 5. Does a finding prove malicious intent? | No. It identifies a construct requiring review. | Claims | Deckhand |
| 6. What is tool poisoning? | Manipulative tool metadata intended to influence agent behavior beyond the honest tool purpose. | Security | Navigator |
| 7. Prompt injection versus tool poisoning? | Prompt injection is the broader instruction-manipulation class; tool poisoning places manipulation in tool metadata. | Security | Navigator |
| 8. What input shapes can `loader.extract_tools` accept? | One tool, an array, a `tools` object, or a JSON-RPC-like `result.tools` response. | Pipeline | Navigator |
| 9. Why strict JSON? | To reject duplicate keys and NaN/Infinity rather than accept ambiguous/non-interoperable input. | Input safety | Navigator |
| 10. What encoding does static JSON accept? | UTF-8 with optional BOM via `utf-8-sig`. | Input safety | Engineer |
| 11. What is the static input byte limit? | 10 MiB. | Limits | Engineer |
| 12. What is the static tool-count limit? | 1,000 tools. | Limits | Engineer |
| 13. What are the JSON structure bounds? | Depth 64 and 100,000 nodes. | Limits | Engineer |
| 14. What is the metadata string limit? | 100,000 characters. | Limits | Engineer |
| 15. Why normalize Unicode with NFC? | To make canonically equivalent Unicode representations consistent while preserving compatibility distinctions. | Normalization | Engineer |
| 16. Does NFC solve confusables? | No. It is not NFKC or a visual-confusable defense. | Normalization | Engineer |
| 17. What happens to conflicting `inputSchema` and `input_schema` aliases? | They are rejected rather than silently choosing one. | Normalization | Navigator |
| 18. Is `inputSchema` required? | Yes, and it must be a JSON object; an empty object is valid. | Normalization | Navigator |
| 19. Why preserve unknown fields? | Security-significant vendor metadata should not disappear merely because the core model does not name it. | Pipeline | Navigator |
| 20. How many detector families exist? | Seven. | Rules | Deckhand |
| 21. How many built-in rule IDs exist? | Sixteen. | Rules | Deckhand |
| 22. What are the seven family IDs? | injection, concealment, sensitive-data, schema, mismatch, obfuscation, capability. | Rules | Gunner |
| 23. What does PI-001 detect? | Explicit model-directed instruction-override wording. | Rules | Gunner |
| 24. What does PI-002 detect? | A contextual claim that metadata instructions outrank conflicting agent/user guidance. | Rules | Gunner |
| 25. What does HID-001 detect? | Explicit concealment or non-disclosure wording. | Rules | Gunner |
| 26. What does HID-002 detect? | A contextual relation withholding material activity from user/operator visibility. | Rules | Gunner |
| 27. What does SEC-001 detect? | Credential or secret terminology, with lower severity in legitimate/benign context. | Rules | Gunner |
| 28. What does SEC-002 detect? | Active handling of a sensitive value, such as collection, storage, transmission or output. | Rules | Gunner |
| 29. What does SCH-001 detect? | Invalid input or output JSON Schema. | Rules | Gunner |
| 30. What does SCH-002 detect? | Privileged-looking input parameters. | Rules | Gunner |
| 31. What does MIS-001 detect? | High-impact schema capability not reflected in the declared purpose. | Rules | Gunner |
| 32. What does MIS-002 detect? | Corroborated contradiction between narrow/offline purpose and concrete high-impact capability. | Rules | Gunner |
| 33. What does OBF-001 detect? | Invisible zero-width or bidi formatting controls. | Rules | Gunner |
| 34. What does OBF-002 detect? | A description longer than 12,000 characters. | Rules | Gunner |
| 35. What does OBF-003 detect? | Extreme whitespace in a description. | Rules | Gunner |
| 36. What does OBF-004 detect? | A long valid Base64-looking block in the description. | Rules | Gunner |
| 37. What does OBF-005 detect? | A bounded depth-one decode exposing a recognized high-risk static construct, or an INFO budget event. | Rules | Gunner |
| 38. What does CAP-001 detect? | Advertised high-impact capability indicators for triage. | Rules | Gunner |
| 39. Why is CAP-001 INFORMATIONAL? | Powerful capability is often legitimate and is context, not sufficient suspicion at MEDIUM. | Rules | Gunner |
| 40. Name the five v0.3 additions. | PI-002, HID-002, SEC-002, MIS-002 and OBF-005. | Rules | Gunner |
| 41. What rule-pack version identifies the current built-ins? | `builtin` version `2.0.0`. | Versioning | Engineer |
| 42. What is the package version? | `0.3.0a1`. | Versioning | Engineer |
| 43. What severity does PI-001 emit? | HIGH. | Rules | Gunner |
| 44. What severity can SEC-001 emit? | LOW in legitimate/benign context, otherwise MEDIUM. | Rules | Gunner |
| 45. What severity does SCH-001 emit? | MEDIUM. | Rules | Gunner |
| 46. What severity can OBF-001 emit? | MEDIUM for zero-width controls and HIGH for bidi controls. | Rules | Gunner |
| 47. What severity does OBF-002 emit? | LOW. | Rules | Gunner |
| 48. What severity does OBF-004 emit? | MEDIUM. | Rules | Gunner |
| 49. Why not memorize detector regexes? | Ownership requires semantic purpose, context, benign collisions and bypasses; regex text is implementation detail. | Learning | Deckhand |
| 50. When are suppressions applied? | After detection and before retention and risk calculation. | Pipeline | Engineer |
| 51. What does a global suppression risk? | Hiding a genuine finding for every tool with that rule ID. | Security | Engineer |
| 52. Why are custom rules data-only? | To avoid executable expressions and user-controlled regex behavior. | Configuration | Engineer |
| 53. What happens if a custom ID collides with a built-in ID? | Validation rejects it before scanning. | Configuration | Engineer |
| 54. What is the per-tool finding retention limit? | 64. | Limits | Engineer |
| 55. What is the per-report finding retention limit? | 2,048. | Limits | Engineer |
| 56. What is the retained evidence limit per tool? | 8,192 characters. | Limits | Engineer |
| 57. How are retained findings ordered? | Deterministically by descending severity, then rule ID, field, evidence and explanation. | Pipeline | Engineer |
| 58. What is the Day 6E P0 defect? | Presentation/finding retention limits currently alter risk, exit, affected counts and evaluation predictions. | Architecture | Captain |
| 59. What three states should a future fix separate? | Detection state, decision state and presentation/retention state. | Architecture | Captain |
| 60. Were H0 and v0.3 affected by the budget defect? | The preserved audits found their artifacts did not reach the relevant truncation bounds. | Research | Research Officer |
| 61. How is risk deduplicated? | The strongest confidence-adjusted contribution for each category/rule pair is used once. | Risk | Engineer |
| 62. What is the per-category risk cap? | 35 points. | Risk | Engineer |
| 63. What are aggregate risk bands? | 0–19 INFO, 20–39 LOW, 40–59 MEDIUM, 60–79 HIGH, 80–100 CRITICAL. | Risk | Engineer |
| 64. Is a HIGH finding guaranteed to produce HIGH aggregate risk? | No. Finding severity and aggregate score/band are separate. | Risk | Engineer |
| 65. What does MEDIUM evaluation threshold mean? | Any retained finding with severity MEDIUM or higher predicts suspicious. | Evaluation | Research Officer |
| 66. Does evaluation compare risk score to 40? | No. It compares finding severity ranks. | Evaluation | Research Officer |
| 67. What does CLI `--fail-on` inspect currently? | Retained finding severities. | CLI | Engineer |
| 68. Why neutralize CSV values beginning with `=`, `+`, `-`, or `@`? | To reduce spreadsheet formula injection when a CSV is opened. | Reporting | Engineer |
| 69. Why escape Rich markup and terminal controls? | Hostile metadata must render literally rather than alter terminal output. | Reporting | Engineer |
| 70. Does `--redact` make a report safe to share? | No. It reduces evidence exposure but other metadata/provenance may remain sensitive. | Reporting | Captain |
| 71. What does canonical JSON do to object keys? | Sorts them deterministically. | Hashing | Engineer |
| 72. What does canonical JSON do to array order? | Preserves it. | Hashing | Engineer |
| 73. What does a tool fingerprint establish? | Equality/change of the selected canonical tool content. | Hashing | Engineer |
| 74. What is excluded from canonical tool identity? | Internal provenance; raw user-supplied source remains significant if present. | Hashing | Engineer |
| 75. What component fingerprints exist? | Description, input schema, optional output schema, annotations, execution and other metadata, plus full. | Hashing | Engineer |
| 76. What does baseline drift prove? | A selected identity changed; not why it changed or whether it is malicious. | Baseline | Engineer |
| 77. When is rename inference accepted? | Exactly one removed and one added tool share the same six-component signature. | Baseline | Engineer |
| 78. Why can CRLF versus LF matter? | Byte hashes change even when parsed JSON semantics may not. | Reproducibility | Engineer |
| 79. What LF-safe clone option was documented? | `git clone -c core.autocrlf=false ...`. | Reproducibility | Engineer |
| 80. What does a corpus hash bind? | Canonicalized manifest identity plus selected sample content under the repository algorithm. | Reproducibility | Research Officer |
| 81. What does a configuration hash bind? | Semantic experiment settings such as threshold, resolved detectors, custom rules, suppressions and timing. | Reproducibility | Research Officer |
| 82. What is the authoritative H0 matrix? | TP 5, TN 18, FP 6, FN 19. | Research | Research Officer |
| 83. What is H0 accuracy? | 23/48 = 47.92%. | Metrics | Research Officer |
| 84. What is H0 precision? | 5/11 = 45.45%. | Metrics | Research Officer |
| 85. What is H0 recall? | 5/24 = 20.83%. | Metrics | Research Officer |
| 86. What is H0 F1? | 10/35 = 28.57%. | Metrics | Research Officer |
| 87. What is H0 FPR? | 6/24 = 25.00%. | Metrics | Research Officer |
| 88. Why is H0 valuable despite poor performance? | It is frozen independent pilot evidence exposing weak transfer and constraining honest claims. | Research | Captain |
| 89. What is the v0.3 exploratory matrix? | TP 11, TN 18, FP 6, FN 13. | Research | Research Officer |
| 90. What are v0.3 exploratory recall/F1/FPR? | 45.83%, 53.66%, and 25.00%. | Metrics | Research Officer |
| 91. Why is v0.3 not confirmatory? | Its rules were designed after H0 predictions and failures were exposed. | Research | Research Officer |
| 92. What is required for a future confirmatory claim? | Approved construct/protocol, frozen candidate, and a fresh untouched reviewed/preregistered evaluation. | Research | Captain |
| 93. What was reviewer binary agreement? | 47/48 = 97.9167%. | Human review | Research Officer |
| 94. What does κ≈0.9583 mean? | Very high binary agreement beyond chance for these marginals; not label truth or detector validity. | Human review | Research Officer |
| 95. What was R08? | `holdout_s011` / `bounded_result_sampler`, the retained malformed-schema label disagreement. | Human review | Research Officer |
| 96. What was exact difficulty agreement? | 16/48, showing that the difficulty dimension was much less stable. | Human review | Research Officer |
| 97. What are supported artifact schemas? | Historical 3.0.0 and current 3.1.0. | Compatibility | Engineer |
| 98. Why not reinterpret old artifacts with current detectors? | Their recorded application/rule/config identities define historical semantics. | Compatibility | Captain |
| 99. What is the H0 artifact path? | `evaluation/runs/exp-20260827T060056391880Z-c514ba03-a660fd6d.json`. | Evidence | Research Officer |
| 100. What is the safest final viva claim? | The prototype provides bounded deterministic metadata review and reproducible pilot evidence; H0 showed weak effectiveness and v0.3 remains exploratory. | Claims | Captain |
