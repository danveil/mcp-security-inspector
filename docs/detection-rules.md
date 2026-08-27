# Detection rules

Package version and built-in rule-pack version are independent identities. Package `0.3.0a1` uses built-in pack `builtin` `2.0.0`; the pack's major increment records the materially expanded v0.3 semantics. Preserved v0.2/Day 4 artifacts retain their authentic recorded `1.0.0` metadata and internally recorded rule sets.

| Rule ID | Name | Category | Default severity | Purpose | Possible false positives |
|---|---|---|---|---|---|
| PI-001 | Possible instruction override | instruction override | High | Find model-directed priority changes in field-addressable metadata text | Defensive documentation quoting or negating attack phrases |
| PI-002 | Instruction-priority claim | instruction override | High | Require authority, instruction-object, and agent/user-guidance concepts in one local window | Policy prose and ordinary data-ranking terminology |
| HID-001 | Concealment wording | concealment | High | Find instructions discouraging disclosure in field-addressable metadata text | Privacy-preserving background operations |
| HID-002 | Withheld material activity | concealment | High | Require omission, material-operation, and observer/disclosure concepts in one local window | UI collapsing, privacy redaction, and irrelevant-field removal |
| SEC-001 | Sensitive credential terminology | sensitive data | Medium | Highlight potentially sensitive inputs/outputs | Password managers, authentication, and secret rotation tools |
| SEC-002 | Sensitive value handling action | sensitive data | Medium | Link an active handling operation to a credential or secret value in local context | Reviewed credential-management workflows |
| SCH-001 | Malformed JSON Schema | schema | Medium | Detect invalid declared schema dialects | Unsupported drafts or vendor extensions |
| SCH-002 | Privileged input parameters | schema | Medium/High | Surface privileged parameter combinations | Terminal and administrative tools |
| MIS-001 | Name/description/schema mismatch | mismatch | High | Compare stated purpose with high-impact schema categories | Broad utility tools or ambiguous vocabulary |
| MIS-002 | Corroborated purpose/capability contradiction | mismatch | Medium/High | Require a path-preserving high-impact capability, missing purpose alignment, and an independent contradiction cue | Legitimate administration, simulation, and plan-only tools |
| OBF-001 | Invisible Unicode formatting | obfuscation | Medium/High | Expose zero-width and bidi controls | Legitimate international text formatting |
| OBF-002 | Unusually long description | obfuscation | Low | Find metadata difficult to review | Generated API documentation |
| OBF-003 | Extreme whitespace | obfuscation | Low | Find presentation-based concealment | Formatting/export artifacts |
| OBF-004 | Encoded-looking block | obfuscation | Medium | Highlight opaque Base64-like content | Binary examples and test fixtures |
| OBF-005 | Decoded high-risk metadata | obfuscation | Informational/Medium | Decode four explicit representations once and report only high-risk decoded constructs or safety-budget events | Safe printable examples and documentation |
| CAP-001 | High-impact capability indicators | capability | Informational | Summarize powerful advertised operations | Legitimate administration tools |

Use `mcpsec explain RULE_ID` for rationale, benign context, and review guidance. Fixed built-in regular expressions are short, bounded, and avoid nested quantifiers over unbounded alternatives. Custom YAML patterns are deliberately literal strings, not regular expressions, preventing catastrophic backtracking and executable configuration.

`OBF-005` recognizes only numeric HTML entities, explicitly separated/prefixed hex bytes, separated decimal character codes, and strict Base64. It uses strict UTF-8 for byte decoders, a 90% printable-text requirement, depth exactly one, and fixed limits of 512 encoded characters, 512 decoded characters, four candidates per field, 32 per tool, and 4,096 retained decoded characters per tool. It never executes decoded text. A limit event is informational; a `MEDIUM` result also requires a decoded instruction-priority, concealment, sensitive-value-action, or structured high-impact-capability signal.

Custom files contain a top-level `rules` list and may include reproducibility metadata such as `rule_pack: {name: research, version: "1.0.0"}`. Legacy files without metadata remain valid and are reported as `legacy-custom` version `0.0.0`. YAML uses `SafeLoader`; files with a `.json` suffix use the same strict duplicate-key/non-finite-number rejection as scan inputs. Files are capped at 1 MiB and 200 entries; each rule may contain at most 9 fields and 32 literal patterns, and each pattern is capped at 256 characters. Rule objects reject unknown keys; severities, confidence, score, identifiers, and allowed fields are strictly validated. Custom IDs must be unique and cannot collide with any built-in rule ID. YAML pre-parse alias, node-expansion, depth, and scalar limits remain enforced. Disabled rules validate but do not run.

Suppressions are separate safe-loaded YAML data capped at 1 MiB and 500 entries, with the same YAML structural limits. Each entry requires a known rule ID, optional exact tool-name scope, and a 10–1,000 character justification. Duplicate rule/tool scopes and unknown IDs are rejected. Research evaluation does not apply suppressions unless explicitly requested.
