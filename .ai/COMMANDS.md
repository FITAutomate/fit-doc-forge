# Commands Reference

All commands run from repo root: `D:\dev\github\fit-docs-forge`.

## Everyday Commands

### Promote a draft

```bash
python agent/promote.py "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-onboarding.md"
```

Behavior summary:
- validates gate fields and `status: promote-ready`
- writes published target and runs `mkdocs build --strict`
- commit behavior:
  - changed publish content: commit + `PROMOTE_SUCCESS`
  - no publish diff: skip commit gracefully + `PROMOTE_SUCCESS`
  - failure: append `PROMOTE_FAILED` with stage details

Flags:
- `--dry-run`: preview only, no writes, no audit append
- `--no-commit`: write/archive/status update but skip git commit/audit success entry
- `--vault PATH`: override vault root
- `--fit-docs PATH`: override fit-docs docs root

Obsidian Shell Command (recommended wrapper):

Dry run:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\run-promote.ps1" -DryRun -DraftPath "{{file_path:relative}}"
```

Real promote:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\run-promote.ps1" -DraftPath "{{file_path:relative}}"
```

Persistent output log:
`D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log`

### Rollback a promoted doc

```bash
python agent/rollback.py "🌐 Solution - fit-docs.md"
python agent/rollback.py "🌐 Solution - fit-docs.md" --dry-run
```

Behavior summary:
- finds latest matching `PROMOTE_SUCCESS` from `_SYSTEM/logs/audit-log.md`
- dry-run prints plan and appends `ROLLBACK_DRY_RUN`
- real rollback deletes target -> strict build -> git rm/commit -> restores draft -> appends `ROLLBACK_SUCCESS`

Flags:
- `--dry-run`
- `--vault PATH`
- `--fit-docs PATH`

Obsidian Shell Command examples:

Dry run rollback:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$log='D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log'; Add-Content $log \"`n--- $(Get-Date -Format o) ROLLBACK-DRY-RUN <published-filename>.md ---\"; $env:PATH='D:\dev\github\fit-docs\venv\Scripts;' + $env:PATH; & 'D:\dev\github\fit-docs\venv\Scripts\python.exe' 'D:\dev\github\fit-docs-forge\agent\rollback.py' '<published-filename>.md' --dry-run 2>&1 | Tee-Object -FilePath $log -Append"
```

Real rollback:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$log='D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log'; Add-Content $log \"`n--- $(Get-Date -Format o) ROLLBACK <published-filename>.md ---\"; $env:PATH='D:\dev\github\fit-docs\venv\Scripts;' + $env:PATH; & 'D:\dev\github\fit-docs\venv\Scripts\python.exe' 'D:\dev\github\fit-docs-forge\agent\rollback.py' '<published-filename>.md' 2>&1 | Tee-Object -FilePath $log -Append"
```

### Sync fit-docs into vault

```bash
python agent/fit-docs_sync.py
```

### Sync Airtable tasks

```bash
python agent/airtable_sync.py --dry-run
python agent/airtable_sync.py
```

## Validation Gates

Python gate:
```bash
cd agent
python -m pip install -e ".[dev]"
ruff check .
pytest -q
```

Next.js gate:
```bash
cd app
npm ci
npm run lint
npm run build
```

## Environment Setup (`agent/.env`)

```dotenv
VAULT_ROOT=D:\Vaults\FIT-Vault
FIT_DOCS_ROOT=D:\dev\github\fit-docs\docs
ANTHROPIC_API_KEY=

AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_TABLE_ID=tblXXXXXXXXXXXXXX
AIRTABLE_VIEW=viwXXXXXXXXXXXXXX
AIRTABLE_BASE_NAME=
AIRTABLE_TABLE_NAME=
AIRTABLE_VIEW_NAME=
AIRTABLE_DASHBOARD_VIEW_URL=
AIRTABLE_DASHBOARD_VIEW_LABEL=Open board view

# IDs-first mapping (preferred)
AIRTABLE_DUE_FIELD=fldXXXXXXXXXXXXDUE
AIRTABLE_TITLE_FIELD=fldXXXXXXXXXXXXTTL
AIRTABLE_STATUS_FIELD=fldXXXXXXXXXXXXSTS
AIRTABLE_OWNER_FIELD=fldXXXXXXXXXXXXOWN
AIRTABLE_PRIORITY_FIELD=fldXXXXXXXXXXXXPRI
AIRTABLE_USE_FIELD_IDS=true
AIRTABLE_MAX_RECORDS=500
```

## Audit Actions

`_SYSTEM/logs/audit-log.md` actions:
- `PROMOTE_SUCCESS`
- `PROMOTE_FAILED`
- `ROLLBACK_SUCCESS`
- `ROLLBACK_DRY_RUN`

## Status Flow Reference

```text
captured > draft > review > promote-ready > [promote.py] > promoted
```
