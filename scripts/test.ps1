[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PytestArguments
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonExecutable = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $pythonExecutable -PathType Leaf)) {
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

Push-Location $projectRoot
try {
    & $pythonExecutable -m pytest @PytestArguments
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
