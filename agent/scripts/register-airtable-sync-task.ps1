param(
    [string]$TaskName = "fit-docs-forge-airtable-sync",
    [string]$StartTime = "08:00",
    [string]$EndTime = "22:00",
    [string]$PythonBin = "python"
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$runScript = (Resolve-Path (Join-Path $PSScriptRoot "run-airtable-sync.ps1")).Path

$taskCommand = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$runScript`" -RepoRoot `"$repoRoot`" -PythonBin `"$PythonBin`""

try {
    $startTs = [TimeSpan]::Parse($StartTime)
    $endTs = [TimeSpan]::Parse($EndTime)
}
catch {
    Write-Error "Invalid time format. Use HH:mm (example: 08:00)."
    exit 1
}

$durationMinutes = [int]($endTs - $startTs).TotalMinutes
if ($durationMinutes -le 0) {
    $durationMinutes += 24 * 60
}

$hours = [int][math]::Floor($durationMinutes / 60)
$minutes = [int]($durationMinutes % 60)
$duration = "{0:D2}:{1:D2}" -f $hours, $minutes

Write-Output "Registering task '$TaskName' (daily, every 60 min from $StartTime to $EndTime)..."
Write-Output "Command: $taskCommand"

schtasks /Create /TN $TaskName /SC DAILY /MO 1 /ST $StartTime /RI 60 /DU $duration /RL LIMITED /TR $taskCommand /F

if ($LASTEXITCODE -eq 0) {
    Write-Output "Task registered."
}
else {
    Write-Error "Failed to register task (exit $LASTEXITCODE)."
    exit $LASTEXITCODE
}
