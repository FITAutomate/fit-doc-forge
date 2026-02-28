# Commands Reference

All commands run from the repo root: `D:\dev\github\fit-docs-forge`

---

## Windows Prerequisite

If `python` or `py` fails with "The file cannot be accessed by the system":

1. Open **Settings > Apps > Advanced app settings > App execution aliases**
2. Toggle **off** `python.exe` and `python3.exe` (the "App Installer" entries)
3. Open a **new** terminal and verify with `python --version`

---

## Everyday Commands

### Promote a draft

```
python agent/promote.py "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-onboarding.md"
```

Validates gate fields, builds compliant filename, copies body into fit-docs, runs `mkdocs build --strict`, then archives + updates draft status.  
When committing:
- changed publish content -> commits and audits `PROMOTE_SUCCESS`
- unchanged publish content -> skips commit gracefully and still audits `PROMOTE_SUCCESS`
- failures -> audits `PROMOTE_FAILED` with stage details

| Flag | Effect |
|---|---|
| `--dry-run` | Preview what would happen without writing anything |
| `--no-commit` | Promote the file but skip the git add/commit step |
| `--vault PATH` | Override vault root (default: from `.env` or `D:\Vaults\FIT-Vault`) |
| `--fit-docs PATH` | Override fit-docs root (default: from `.env` or `D:\dev\github\fit-docs\docs`) |

**Obsidian Shell Command (recommended wrapper):**

Dry run:
```
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\run-promote.ps1" -DryRun -DraftPath "{{file_path:relative}}"
```

Real promote:
```
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\run-promote.ps1" -DraftPath "{{file_path:relative}}"
```

The wrapper writes persistent command output to:
`D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log`

Obsidian shell command examples:

Dry run rollback:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$log='D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log'; Add-Content $log \"`n--- $(Get-Date -Format o) ROLLBACK-DRY-RUN <published-filename>.md ---\"; $env:PATH='D:\dev\github\fit-docs\venv\Scripts;' + $env:PATH; & 'D:\dev\github\fit-docs\venv\Scripts\python.exe' 'D:\dev\github\fit-docs-forge\agent\rollback.py' '<published-filename>.md' --dry-run 2>&1 | Tee-Object -FilePath $log -Append"
```

Real rollback:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$log='D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log'; Add-Content $log \"`n--- $(Get-Date -Format o) ROLLBACK <published-filename>.md ---\"; $env:PATH='D:\dev\github\fit-docs\venv\Scripts;' + $env:PATH; & 'D:\dev\github\fit-docs\venv\Scripts\python.exe' 'D:\dev\github\fit-docs-forge\agent\rollback.py' '<published-filename>.md' 2>&1 | Tee-Object -FilePath $log -Append"
```

Note: rollback operates on the published filename in `fit-docs/docs/...`, so replace `<published-filename>.md` before running.

### Sync fit-docs into vault

```
python agent/fit-docs_sync.py
```

One-way mirror of `fit-docs/docs/` into `_REFERENCE/fit-docs/` inside the vault. Copies new/updated files, removes deleted files. Run this after any changes to fit-docs.

| Flag | Effect |
|---|---|
| `--source PATH` | Override fit-docs/docs/ path |
| `--vault PATH` | Override vault root |

Legacy alias still works:
```
python agent/fit_docs_sync.py
python agent/sync_fit_docs.py
```

### Sync Airtable tasks into ops dashboard

```
python agent/airtable_sync.py
```

Pulls Airtable tasks, filters overdue and due-today items, and writes `04-OPERATIONS/_ops-dashboard.md` in the vault.

| Flag | Effect |
|---|---|
| `--dry-run` | Print dashboard preview without writing files |
| `--vault PATH` | Override vault root |
| `--base-id ID` | Override Airtable base ID |
| `--table-id ID_OR_NAME` | Override Airtable table |
| `--view NAME` | Optional Airtable view |
| `--base-name NAME` | Force dashboard display name for base |
| `--table-name NAME` | Force dashboard display name for table |
| `--view-name NAME` | Force dashboard display name for view |
| `--dashboard-view-url URL` | Add single top-of-dashboard link to this Airtable view |
| `--dashboard-view-label TEXT` | Label for the top view link |
| `--due-field FIELD` | Due date field name (default `Due Date`) |
| `--title-field FIELD` | Task title field name (default `Task Name`) |
| `--status-field FIELD` | Task status field name (default `Status`) |
| `--owner-field FIELD` | Task owner field name (default `Assignee Name`) |
| `--priority-field FIELD` | Task priority field name (default `Priority`) |
| `--use-field-ids` | Treat `AIRTABLE_*_FIELD` values as Airtable field IDs (`fld...`) |
| `--max-records N` | Max records to process (default `500`) |
| `--today YYYY-MM-DD` | Override current date for deterministic runs |
| `--inspect-fields` | Print discovered field names + status counts and exit |

### Schedule Airtable sync (Windows Task Scheduler)

Register hourly task (08:00-22:00):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "agent\scripts\register-airtable-sync-task.ps1"
```

Remove the task:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "agent\scripts\unregister-airtable-sync-task.ps1"
```

### Scaffold the vault

```
python agent/scaffold_vault.py
```

Creates the full Obsidian vault folder tree, copies templates into `_SYSTEM/templates/`, system docs into `_SYSTEM/`, and scripts into `_SYSTEM/scripts/`. Idempotent -- safe to re-run anytime.

---

## CI Validation Gates

Run both before opening any PR.

### Python gate

```
cd agent
pip install -e ".[dev]"
ruff check .
pytest
```

### Next.js gate

```
cd app
npm ci
npm run lint
npm run build
```

### Both gates (PowerShell)

```powershell
# Terminal 1:
cd agent; pip install -e ".[dev]"; ruff check .; pytest

# Terminal 2:
cd app; npm ci; npm run lint; npm run build
```

---

## Environment Setup

### `.env` file (in `agent/`)

Copy `agent/.env.example` to `agent/.env` and fill in:

```
VAULT_ROOT=D:\Vaults\FIT-Vault
FIT_DOCS_ROOT=D:\dev\github\fit-docs\docs
ANTHROPIC_API_KEY=
AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=
AIRTABLE_TABLE_ID=
AIRTABLE_VIEW=
AIRTABLE_BASE_NAME=
AIRTABLE_TABLE_NAME=
AIRTABLE_VIEW_NAME=
AIRTABLE_DASHBOARD_VIEW_URL=
AIRTABLE_DASHBOARD_VIEW_LABEL=Open board view
AIRTABLE_DUE_FIELD=fldXXXXXXXXXXXXDUE
AIRTABLE_TITLE_FIELD=fldXXXXXXXXXXXXTTL
AIRTABLE_STATUS_FIELD=fldXXXXXXXXXXXXSTS
AIRTABLE_OWNER_FIELD=fldXXXXXXXXXXXXOWN
AIRTABLE_PRIORITY_FIELD=fldXXXXXXXXXXXXPRI
AIRTABLE_USE_FIELD_IDS=true
AIRTABLE_MAX_RECORDS=500
```

### First-time setup

```powershell
cd agent; pip install -e ".[dev]"
cd ..\app; npm ci
python agent/scaffold_vault.py
python agent/fit-docs_sync.py
```

---

## Status Flow Reference

```
captured > draft > review > promote-ready > [promote.py] > promoted
```

| Gate Field | Must be `true` before promote |
|---|---|
| `gate_has_owner` | Document has an assigned owner |
| `gate_metadata_complete` | All required metadata fields filled |
| `gate_heading_structure_valid` | H2/H3 structure matches library README |
| `gate_reviewed_by_human` | Human has reviewed and approved |
| `gate_no_internal_refs` | No internal refs in public docs (PUBLIC_WEB only) |
| `gate_no_invented_slas` | No made-up SLAs/prices (PUBLIC_WEB only) |

## Audit Actions

`_SYSTEM/logs/audit-log.md` now includes:
- `PROMOTE_SUCCESS`
- `PROMOTE_FAILED`
- `ROLLBACK_SUCCESS`
- `ROLLBACK_DRY_RUN`
