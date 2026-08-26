# Local demonstration server

This server uses the official MCP Python SDK v2 and makes no network calls, reads no files or environment variables, and executes no commands. `suspicious_metadata_fixture` contains intentionally suspicious **description text only**, clearly marked for security testing. Running the server is optional; `mcpsec` never starts it automatically.

## Recommended Windows Inspector workflow

From the repository root:

```powershell
.\scripts\dev-inspector.ps1
```

Open the main URL printed by the command, normally `http://localhost:6274/`, then enable the `mcp.exe` connection switch. The connection should identify the server as `mcpsec-local-demo` and populate the Tools tab.

Do **not** open a URL ending in `/sandbox` directly. It is an internal iframe endpoint used to isolate MCP Apps and is intentionally blank when opened as a top-level page.

The helper deliberately launches Inspector with `.venv\Scripts\mcp.exe`. This avoids `mcp dev` generating a `uv run ...` connection when `uv` is not installed. It also uses a project-local npm cache and disables automatic browser opening so the wrong sandbox endpoint is not selected.

If port 6274 belongs to an older Inspector process, stop its terminal with Ctrl+C or choose another port:

```powershell
.\scripts\dev-inspector.ps1 -Port 6284
```

The first Inspector run needs Internet access so `npx` can obtain the pinned Inspector package. Later runs reuse `.npm-cache`.

To run only the server over stdio without the web Inspector:

```powershell
.\.venv\Scripts\mcp.exe run sample_mcp_server\server.py
```

To demonstrate v0.2's opt-in localhost-only catalog retrieval, run the harmless server in one terminal:

```powershell
.\.venv\Scripts\python.exe sample_mcp_server\server.py --http --port 8765
```

Then, in another terminal, retrieve only `tools/list` and scan the saved static catalog:

```powershell
mcpsec fetch http://127.0.0.1:8765/mcp --output local-tools.json
mcpsec scan local-tools.json
```

`fetch` does not start a process and never invokes a discovered tool. Its dedicated transport validates each request as loopback, disables redirects, ignores proxy environment variables, and enforces timeout, page-count, tool-count, cumulative response-size, normalized metadata-size, string, and duplicate-name limits. The local demo uses no authentication; do not expose it on a public interface.

Only connect with an MCP client you control. The application's primary workflow is static JSON inspection.
