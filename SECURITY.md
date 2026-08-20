# Security policy

## Supported version

Security fixes are provided for the latest 0.1.x release until a later supported line is announced.

## Reporting a vulnerability

Please use GitHub's private security-advisory feature. Include the affected version, minimal reproduction, impact, and suggested mitigation. Do not include real credentials, malicious server access, or private customer data. Maintainers should acknowledge reports within seven days and coordinate disclosure after a fix is available.

## Security invariants

`mcpsec` statically analyzes local metadata. It must not call tools, start supplied server commands, fetch metadata URLs or icons, discover credentials, evaluate templates, or execute configuration. It uses no telemetry. Scanned values and rule files are hostile inputs; reports must preserve those boundaries.

Do not use this project to probe systems without authorization. A finding is not proof of compromise, and a clean result is not a trust decision.

