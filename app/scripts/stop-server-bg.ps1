$ErrorActionPreference = "Stop"

$appDir = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $appDir ".next-dev.pid"

if (!(Test-Path $pidFile)) {
    Write-Host "No PID file found. Server is already stopped."
    exit 0
}

$trackedPid = (Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
if (!$trackedPid) {
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    Write-Host "PID file was empty. Cleared stale file."
    exit 0
}

cmd /c "taskkill /PID $trackedPid /T /F" > $null 2>&1
Remove-Item $pidFile -Force -ErrorAction SilentlyContinue

Write-Host "Stopped Next.js dev server (PID $trackedPid)."
