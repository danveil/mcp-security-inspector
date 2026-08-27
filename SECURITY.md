# Security policy

## Supported versions and platforms

Security fixes are provided for the latest published 0.2.x release and the `0.3.0a1` public alpha until a later supported line is announced. The alpha is an evaluation release, not a production-readiness claim. The project requires Python 3.12 or newer; automated CI covers Ubuntu and development validation covers Windows. No macOS support claim is made until that platform is exercised in CI.

## Reporting a vulnerability

Please use GitHub's private security-advisory feature. Include the affected version, minimal reproduction, impact, and suggested mitigation. Do not include real credentials, malicious server access, or private customer data. Maintainers should acknowledge reports within seven days and coordinate disclosure after a fix is available.

## Security invariants

`mcpsec` statically analyzes local metadata by default. Its opt-in `fetch` command may contact only an explicit localhost/loopback MCP Streamable HTTP endpoint and sends only the protocol requests needed to initialize and list tools. The retrieval transport validates each request as loopback, pins `localhost` to a verified loopback IP before connecting, rejects redirects, ignores proxy environment variables, and applies cumulative response, pagination, timeout, and tool-count limits. It must not call tools, start supplied server commands, follow metadata URLs, fetch icons, discover credentials, evaluate templates, or execute configuration. Icon text may be inspected as inert metadata, but referenced icon resources are never retrieved. It uses no telemetry.

Scanned values, corpus manifests, rule files, suppressions, baselines, and server responses are hostile inputs. Duplicate JSON keys and non-finite numbers are rejected. Representation decoding is restricted to explicitly supported encodings, strict UTF-8, depth one, and bounded candidate/output/count budgets; decoded content remains inert evidence. Reports retain at most 64 findings per tool, 2,048 findings per scan or evaluation, and 8,192 evidence characters per tool, with explicit truncation status. Oversized security-significant inputs are rejected rather than silently discarded.

Do not use this project to probe systems without authorization. A finding is not proof of compromise, and a clean result is not a trust decision.
