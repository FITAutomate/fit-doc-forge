# Commands Reference

All commands run from repo root: `D:\dev\github\fit-docs-forge`

## Everyday Commands

### Promote a draft

```bash
python agent/promote.py "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-onboarding.md"
```

Behavior summary:
- validates gate fields and `status: promote-ready`
- routes + writes target file in `fit-docs/docs/...`
- runs `mkdocs build --strict` before commit
- on successful commit, archives draft and appends audit entry

Flags:
- `--dry-run`: preview only, no writes, no audit append
- `--no-commit`: write/archive/update draft but skip git commit and skip audit append
- `--vault PATH`: override vault root
- `--fit-docs PATH`: override fit-docs docs root

Obsidian shell command example:

```bash
python D:\dev\github\fit-docs-forge\agent\promote.py --dry-run "{{file_path:relative}}"
```

### Rollback a promoted doc (Phase 5.5.2)

```bash
python agent/rollback.py "📚 SOP 21 — Onboarding.md"
```

Behavior summary:
- finds last matching `PROMOTE_SUCCESS` entry in `_SYSTEM/logs/audit-log.md`
- deletes target doc from `fit-docs/docs/...`
- runs `mkdocs build --strict`
- runs `git rm` + `git commit`
- restores archived draft to original draft path and resets `status: promote-ready`
- appends `ROLLBACK_SUCCESS` audit entry

Flags:
- `--dry-run`: print rollback plan and append `ROLLBACK_DRY_RUN`
- `--vault PATH`: override vault root
- `--fit-docs PATH`: override fit-docs docs root

### Sync fit-docs into vault

```bash
python agent/fit-docs_sync.py
```

### Sync Airtable tasks into ops dashboard

```bash
python agent/airtable_sync.py --dry-run
python agent/airtable_sync.py
```

Airtable field mapping policy:
- default team mode is field IDs (`fld...`) in env values
- set `AIRTABLE_USE_FIELD_IDS=true`
- use `--inspect-fields` to discover available field names/status counts before mapping

Useful flags:
- `--inspect-fields`
- `--use-field-ids`
- `--title-field`, `--due-field`, `--status-field`, `--owner-field`, `--priority-field`
- `--base-id`, `--table-id`, `--view`

## Windows Scheduler

Register hourly Airtable sync task:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "agent\scripts\register-airtable-sync-task.ps1"
```

Remove task:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "agent\scripts\unregister-airtable-sync-task.ps1"
```

## Validation Gates

Python gate:

```bash
cd agent
pip install -e ".[dev]"
ruff check .
pytest
```

Next.js gate:

```bash
cd app
npm ci
npm run lint
npm run build
```

## Environment Setup (`agent/.env`)

Start from `agent/.env.example`.

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

If you intentionally map by field names instead of IDs, set `AIRTABLE_USE_FIELD_IDS=false`.

## Audit Log Reference

File: `_SYSTEM/logs/audit-log.md`

Format:

```text
[TIMESTAMP_UTC] [ACTION] [SOURCE_FILE] [TARGET_FILE] [GIT_COMMIT_HASH]
```

Actions in use:
- `PROMOTE_SUCCESS`
- `ROLLBACK_SUCCESS`
- `ROLLBACK_DRY_RUN`
