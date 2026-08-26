[CmdletBinding()]
param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 6274
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonExecutable = Join-Path $projectRoot ".venv\Scripts\python.exe"
$mcpExecutable = Join-Path $projectRoot ".venv\Scripts\mcp.exe"
$serverFile = Join-Path $projectRoot "sample_mcp_server\server.py"
$npmCache = Join-Path $projectRoot ".npm-cache"

if (-not (Test-Path -LiteralPath $pythonExecutable -PathType Leaf) -or -not (Test-Path -LiteralPath $mcpExecutable -PathType Leaf)) {
    throw "Project environment not found. Run: python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -e `".[dev]`""
}

try {
    & $pythonExecutable --version 2>$null | Out-Null
}
catch {
    throw "Project environment is stale or broken. Remove .venv, recreate it with Python 3.12+, then install: .\.venv\Scripts\python.exe -m pip install -e `".[dev]`""
}
if ($LASTEXITCODE -ne 0) {
    throw "Project environment is stale or broken. Remove .venv, recreate it with Python 3.12+, then install: .\.venv\Scripts\python.exe -m pip install -e `".[dev]`""
}

if (-not (Get-Command npx.cmd -ErrorAction SilentlyContinue)) {
    throw "Node.js with npx is required for the web Inspector. Install Node.js, then retry."
}

$existingListener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($existingListener) {
    throw "Port $Port is already in use. Stop the previous Inspector with Ctrl+C, or run: .\scripts\dev-inspector.ps1 -Port 6284"
}

New-Item -ItemType Directory -Force -Path $npmCache | Out-Null
$env:NPM_CONFIG_CACHE = $npmCache
$env:CLIENT_PORT = [string]$Port
$env:MCP_AUTO_OPEN_ENABLED = "false"

Write-Host "Starting MCP Inspector with the project virtual environment."
Write-Host "Open the Inspector UI shown below (for example http://localhost:$Port/)."
Write-Host "Do not open the /sandbox URL directly; it is an internal iframe endpoint."
Write-Host "Press Ctrl+C here to stop the Inspector."

Push-Location $projectRoot
try {
    & npx.cmd -y "@modelcontextprotocol/inspector@2.2.0" $mcpExecutable run $serverFile
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
