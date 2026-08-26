# Security policy

## Supported version

Security fixes are provided for the latest 0.2.x release until a later supported line is announced.

## Reporting a vulnerability

Please use GitHub's private security-advisory feature. Include the affected version, minimal reproduction, impact, and suggested mitigation. Do not include real credentials, malicious server access, or private customer data. Maintainers should acknowledge reports within seven days and coordinate disclosure after a fix is available.

## Security invariants

`mcpsec` statically analyzes local metadata by default. Its opt-in `fetch` command may contact only an explicit localhost/loopback MCP Streamable HTTP endpoint and sends only the protocol requests needed to initialize and list tools. The retrieval transport validates each request as loopback, pins `localhost` to a verified loopback IP before connecting, rejects redirects, ignores proxy environment variables, and applies cumulative response, pagination, timeout, and tool-count limits. It must not call tools, start supplied server commands, follow metadata URLs, fetch icons, discover credentials, evaluate templates, or execute configuration. It uses no telemetry. Scanned values, corpus manifests, rule files, suppressions, baselines, and server responses are hostile inputs; resource budgets and rejection—not silent truncation—must preserve those boundaries.

Do not use this project to probe systems without authorization. A finding is not proof of compromise, and a clean result is not a trust decision.
