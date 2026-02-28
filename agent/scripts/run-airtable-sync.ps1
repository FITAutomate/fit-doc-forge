param(
    [string]$RepoRoot = "",
    [string]$PythonBin = "python",
    [switch]$DryRun
)

if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

$agentDir = Join-Path $RepoRoot "agent"

if (-not (Test-Path $agentDir)) {
    Write-Error "Agent directory not found: $agentDir"
    exit 1
}

Push-Location $agentDir
try {
    if ($DryRun) {
        & $PythonBin "airtable_sync.py" "--dry-run"
    }
    else {
        & $PythonBin "airtable_sync.py"
    }
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
