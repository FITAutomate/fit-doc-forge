param(
    [string]$TaskName = "fit-docs-forge-airtable-sync"
)

Write-Output "Removing task '$TaskName'..."
schtasks /Delete /TN $TaskName /F

if ($LASTEXITCODE -eq 0) {
    Write-Output "Task removed."
}
else {
    Write-Error "Failed to remove task (exit $LASTEXITCODE)."
    exit $LASTEXITCODE
}
