# fit-docs-forge

AI-powered documentation pipeline for FIT Automate. Agents read library READMEs as schemas, draft and validate documents through gate fields, and promote them into the published `fit-docs` repo via a promote script.

The full plan lives in [`FIT-Automate-Master-Blueprint-v3.md`](FIT-Automate-Master-Blueprint-v3.md).

## Structure
| Path | What | Status |
|---|---|---|
| `.ai/` | Agent rules, commands, config, templates, skills | Active |
| `.github/` | CI workflows, Dependabot, PR/issue templates | Active |
| `agent/` | Python package - AI logic, promote/rollback scripts, folder rewrites | Active (Phase 5.5) |
| `app/` | Next.js - preview UI, gate status, approve-to-promote | Active (Phase 4 PR3) |
| `FIT-Automate-Master-Blueprint-v3.md` | The master plan (7 phases) | Active |
| `CHANGELOG.md` | Running history of every merged change | Active |

## Validation gates
Every PR must pass both gates before merge.

### Python gate (`agent/`)
```bash
cd agent
pip install -e ".[dev]"
ruff check .
pytest
```

### Next.js gate (`app/`)
```bash
cd app
npm ci
npm run lint
npm run build
```

## Local UI Ops (Windows)
- App runs on `http://localhost:3200` by default.
- Start in background: `cd app && npm run server:bg:start`
- Stop background server: `cd app && npm run server:bg:stop`
- Boot autostart (one-line PowerShell):
```powershell
schtasks /Create /TN "fit-docs-forge-ui" /SC ONSTART /RL LIMITED /TR "powershell -NoProfile -ExecutionPolicy Bypass -File \"D:\dev\github\fit-docs-forge\app\scripts\start-server-bg.ps1\"" /F
```

## Obsidian Promote Commands (Windows)
- Dry run:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\run-promote.ps1" -DryRun -DraftPath "{{file_path:relative}}"
```
- Real promote:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\run-promote.ps1" -DraftPath "{{file_path:relative}}"
```
- Persistent shell-command log:
  `D:\Vaults\FIT-Vault\_SYSTEM\logs\shell-command.log`

## Ops Sync (Airtable)
```bash
cd agent
python airtable_sync.py --dry-run
python airtable_sync.py
```

Field mapping note:
- Team default is field IDs (`fld...`) with `AIRTABLE_USE_FIELD_IDS=true`.
- Use `python airtable_sync.py --inspect-fields` before mapping or remapping fields.

### Airtable Schedule (Windows)
Run hourly from `08:00` to `22:00`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\register-airtable-sync-task.ps1"
```

Remove task:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\dev\github\fit-docs-forge\agent\scripts\unregister-airtable-sync-task.ps1"
```

## Phase Status
- Phase 2 (Vault Foundation): closed.
- Phase 3 (Promote Script): closed.
- Phase 5 (Airtable Bridge): closed.
- Phase 5.5.1 (Audit Trail Log): closed.
- Phase 5.5.2 (Rollback Script): in progress.

## Safety & Observability
- Promote now validates strict build before commit and writes audit entries to `_SYSTEM/logs/audit-log.md` on successful commit.
- Rollback flow is implemented in `agent/rollback.py` and can run in dry-run mode before changing files.
- See `.ai/COMMANDS.md` for current promote/rollback operational commands.

## Promote Troubleshooting
- If a repeated promote has no publish diff, `promote.py` now completes successfully and skips git commit.
- Promote failures append `PROMOTE_FAILED` entries to `_SYSTEM/logs/audit-log.md` with failure stage details.

## Contributing
1. Read `.ai/AGENT.md` before every session.
2. One concern per PR, always draft first.
3. Reference the relevant blueprint phase in the PR description.
4. Update `CHANGELOG.md` and this README when your PR changes repo structure or adds features.
5. Both CI gates must pass before requesting review.
