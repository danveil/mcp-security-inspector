# Preparation

## Environment audit (2026-08-13)

- Required: Python 3.12 or newer. The inspected host's global `python` command was unavailable; the Codex project runtime provides Python 3.12.13.
- Git: required for the recommended workflow. Git 2.53.0 was available through the project runtime.
- Official MCP Python SDK: not installed before project setup. This project installs the stable v2 SDK as the `mcp>=2,<3` dependency.
- Initial project directory: empty except for Codex-managed `work/` and `outputs/` folders.
- No system-wide applications were installed.

## Recommended workstation

Install Python 3.12+, Git, and Visual Studio Code. Recommended VS Code extensions are Python, Pylance, Ruff, and Even Better TOML. Do not store credentials in the repository.

## Virtual environment

```bash
python -m venv .venv
```

Windows PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS activation:

```bash
source .venv/bin/activate
```

Upgrade packaging tools and install the project:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Required runtime dependencies are the official `mcp` Python SDK, Typer, Rich, Pydantic, PyYAML, and jsonschema. Optional development dependencies are pytest, pytest-cov, Ruff, mypy, and types-PyYAML.

## Verification commands

```bash
python -m pytest
python -m pytest --cov=mcpsec --cov-report=term-missing --cov-report=html
ruff check .
ruff format --check .
mypy src
mcpsec --help
mcpsec scan examples/clean_tools.json
mcpsec scan examples/suspicious_tools.json --format json
mcpsec baseline examples/clean_tools.json --output baseline.json
mcpsec compare examples/changed_tools.json --baseline baseline.json
```

On Windows, the repository helpers work without activating the environment:

```powershell
.\scripts\test.ps1 -q
.\scripts\dev-inspector.ps1
```

The Inspector UI is normally `http://localhost:6274/`. A generated URL ending in `/sandbox` is an internal iframe document and should not be opened directly. The Inspector helper requires Node.js/`npx` and may use the Internet on its first run; ordinary `mcpsec` scans remain offline.

Ordinary scans need no Internet access. `mcpsec` has no telemetry, external API, or cloud dependency.
