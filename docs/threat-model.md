# Threat model

## Assets

- AI client and human-review trust
- User data and credentials
- Tool catalog integrity
- Approved tool definitions and their baselines

## Threat actors

- Malicious MCP server publisher
- Compromised MCP server or dependency
- Malicious metadata contributor
- Operator making an accidental risky configuration

## Threats

The scanner focuses on tool-description poisoning, model instruction injection, concealment, sensitive-data collection indicators, schema drift, capability expansion, misleading tool naming, and metadata obfuscation. Reports are also a boundary: hostile strings could target terminals or spreadsheets, so evidence is bounded, escape bytes are neutralized, CSV formula prefixes are escaped, and `--redact` suppresses excerpts.

## Out of scope

- Detecting every prompt injection
- Runtime sandboxing or proving implementation behavior
- Malware analysis, OAuth implementation, or network intrusion detection
- Unauthorized MCP invocation or malicious server-registration prevention
- Automatically deciding whether a server is safe or malicious

Human review, server authentication, least privilege, confirmation UI, runtime isolation, and audit logging remain separate controls.

