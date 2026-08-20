# Detection rules

| Rule ID | Name | Category | Default severity | Purpose | Possible false positives |
|---|---|---|---|---|---|
| PI-001 | Possible instruction override | instruction override | High | Find model-directed priority changes | Defensive documentation quoting or negating attack phrases |
| HID-001 | Concealment wording | concealment | High | Find instructions discouraging user disclosure | Privacy-preserving background operations |
| SEC-001 | Sensitive credential terminology | sensitive data | Medium | Highlight potentially sensitive inputs/outputs | Password managers, authentication, and secret rotation tools |
| SCH-001 | Malformed JSON Schema | schema | Medium | Detect invalid declared schema dialects | Unsupported drafts or vendor extensions |
| SCH-002 | Privileged input parameters | schema | Medium/High | Surface privileged parameter combinations | Terminal and administrative tools |
| MIS-001 | Name/description/schema mismatch | mismatch | High | Compare stated purpose with high-impact schema categories | Broad utility tools or ambiguous vocabulary |
| OBF-001 | Invisible Unicode formatting | obfuscation | Medium/High | Expose zero-width and bidi controls | Legitimate international text formatting |
| OBF-002 | Unusually long description | obfuscation | Low | Find metadata difficult to review | Generated API documentation |
| OBF-003 | Extreme whitespace | obfuscation | Low | Find presentation-based concealment | Formatting/export artifacts |
| OBF-004 | Encoded-looking block | obfuscation | Medium | Highlight opaque Base64-like content | Binary examples and test fixtures |
| CAP-001 | High-impact capability indicators | capability | Informational | Summarize powerful advertised operations | Legitimate administration tools |

Use `mcpsec explain RULE_ID` for rationale, benign context, and review guidance. Fixed built-in regular expressions are short, bounded, and avoid nested quantifiers over unbounded alternatives. Custom YAML patterns are deliberately literal strings, not regular expressions, preventing catastrophic backtracking and executable configuration.

Custom files have exactly one top-level `rules` list and are capped at 200 entries. Rule objects reject unknown keys; patterns are capped at 256 characters; severities, confidence, score, identifiers, and allowed fields are strictly validated. `yaml.safe_load` prevents Python-object construction. Disabled rules validate but do not run.

