# Commands reference for fit-doc-forge

## Windows prerequisite
If `python` or `py` fails with "The file cannot be accessed by the system":
1. Open **Settings → Apps → Advanced app settings → App execution aliases**
2. Toggle **off** `python.exe` and `python3.exe` (the "App Installer" entries)
3. Open a **new** terminal — verify with `python --version`

## Python gate (`agent/`)
```
cd agent
pip install -e ".[dev]"
ruff check .
pytest
```

## Next.js gate (`app/`)
```
cd app
npm ci
npm run lint
npm run build
```

## Full validation (run both before any PR)
```
# Terminal 1:
cd agent && pip install -e ".[dev]" && ruff check . && pytest
# Terminal 2:
cd app && npm ci && npm run lint && npm run build
```

## Vault scaffold (Phase 2)
```
python agent/scaffold_vault.py
```
Creates the full Obsidian vault folder tree at VAULT_ROOT (from `.env`, default `D:\Vaults\FIT-Vault`). Also copies templates into `_SYSTEM/templates/` and system docs into `_SYSTEM/`. Idempotent — safe to re-run.

## Promote a draft (Phase 3)
```
python agent/promote.py "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-onboarding.md"
```
Validates gate fields, builds compliant filename with emoji prefix, copies body into fit-docs, archives the original, and commits to Git.

Options:
```
python agent/promote.py --dry-run "02-DRAFTS/..."   # preview without writing
python agent/promote.py --no-commit "02-DRAFTS/..." # promote but skip git commit
```

## Sync fit-docs into vault (Phase 2)
```
python agent/sync_fit_docs.py
```
One-way mirror of `fit-docs/docs/` into `_REFERENCE/fit-docs/` inside the vault. Copies new/updated files, removes deleted files. Uses FIT_DOCS_ROOT and VAULT_ROOT from `.env`.

Override paths:
```
python agent/sync_fit_docs.py --source D:\Dev\fit-docs\docs --vault D:\Vaults\FIT-Vault
```
