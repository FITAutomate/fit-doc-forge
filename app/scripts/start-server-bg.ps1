$ErrorActionPreference = "Stop"

$appDir = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $appDir ".next-dev.pid"
$logFile = Join-Path $appDir ".next-dev.log"

if (Test-Path $pidFile) {
    $trackedPid = (Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
    if ($trackedPid -and (Get-Process -Id $trackedPid -ErrorAction SilentlyContinue)) {
        Write-Host "Next.js dev server is already running (PID $trackedPid)."
        Write-Host "Log: $logFile"
        exit 0
    }
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
}

$command = "cd /d `"$appDir`" && npm run dev >> `"$logFile`" 2>&1"
$process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $command -WindowStyle Hidden -PassThru

Set-Content -Path $pidFile -Value $process.Id -Encoding ascii

Write-Host "Started Next.js dev server on port 3200 (PID $($process.Id))."
Write-Host "Log: $logFile"
