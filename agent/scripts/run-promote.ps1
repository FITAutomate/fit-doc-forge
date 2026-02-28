param(
    [Parameter(Mandatory = $true)]
    [string]$DraftPath,
    [switch]$DryRun,
    [string]$PythonPath = "D:\dev\github\fit-docs\venv\Scripts\python.exe",
    [string]$LogFile = "D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log"
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "..\promote.py"
$scriptPath = [System.IO.Path]::GetFullPath($scriptPath)

$logDir = Split-Path -Parent $LogFile
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$runType = if ($DryRun) { "PROMOTE-DRY-RUN" } else { "PROMOTE" }
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
$header = "`n--- $timestamp $runType $DraftPath ---"
Add-Content -Path $LogFile -Value $header

$args = @($scriptPath)
if ($DryRun) {
    $args += "--dry-run"
}
$args += $DraftPath

$output = & $PythonPath @args 2>&1
$exitCode = $LASTEXITCODE

$output | Tee-Object -FilePath $LogFile -Append
exit $exitCode
