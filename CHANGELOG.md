# Changelog

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added

- `.ai/COMMANDS.md` rewritten as full command manual with flags, Obsidian shell command syntax, gate reference, and first-time setup
- `agent/promote.py` promote script from blueprint Part 6: validates gates, builds compliant filenames, routes to fit-docs, archives originals
- 19 promote tests covering gate validation, filename building, folder routing, dry-run, and full integration flow
- Scaffold now copies `promote.py`, `fit-docs_sync.py`, and `airtable_sync.py` into vault `_SYSTEM/scripts/`
- `.ai/skills/changelog.md` format rules for CHANGELOG entries
- `agent/scaffold_vault.py` idempotent script to create the full vault folder tree (blueprint Part 2)
- `agent/tests/test_scaffold_vault.py` tests covering folder creation, placeholders, idempotency
- `agent/vault_templates/` 5 Obsidian draft templates from blueprint Part 5 (sop, kb-article, procedure, solution-description, doc-request)
- Scaffold script now copies templates into `_SYSTEM/templates/` without overwriting user edits
- `agent/vault_system_docs/agent-instructions.md` embeds Part 0 README-as-schema rule plus general agent rules
- `agent/vault_system_docs/vault-map.md` folder structure quick reference with naming conventions
- Scaffold script now copies system docs into `_SYSTEM/` without overwriting user edits
- `_REFERENCE/fit-docs/` vault folder read-only mirror of published docs for Obsidian indexing
- `agent/fit_docs_sync.py` canonical one-way sync from `fit-docs/docs/` into vault `_REFERENCE/` plus CLI alias `fit-docs_sync.py`
- `agent/airtable_sync.py` Phase 5 entrypoint placeholder with CLI flags
- `agent/airtable_sync.py` Phase 5 implementation: Airtable pagination, due-date filtering, markdown dashboard rendering, and `--dry-run` preview support
- `agent/airtable_sync.py --inspect-fields` mode to print discovered column names and status counts before syncing
- Airtable record links in ops dashboard now use full app/table/view/record URLs and display friendly labels (`Open`) instead of raw `rec...` IDs
- `agent/airtable_sync.py` now supports field-ID mode (`AIRTABLE_USE_FIELD_IDS` / `--use-field-ids`) so schema renames won't break mapping
- Ops dashboard header now displays Airtable base/table/view names (with metadata lookup + env overrides), includes one top configurable board-view link, and removes the redundant Airtable link column
- Ops dashboard task table now includes a `Priority` column sourced from configurable field mapping (`AIRTABLE_PRIORITY_FIELD`)
- `agent/scripts/register-airtable-sync-task.ps1` and `agent/scripts/run-airtable-sync.ps1` to schedule hourly Airtable sync runs (08:00-22:00 by default)
- `agent/scripts/unregister-airtable-sync-task.ps1` helper to remove the scheduled task cleanly
- `agent/tests/test_airtable_sync.py` coverage for Airtable URL building, pagination, filtering, and dashboard file writes
- `pytest.ini` at repo root so `pytest` resolves `agent/` modules when run from repo root
- 4 sync tests covering copy, update, delete, and idempotency
- `app/` minimal real Next.js App Router scaffold (`app/app/layout.js`, `app/app/page.js`, `app/app/globals.css`, `.eslintrc.json`)
- `app/app/drafts/page.js` read-only draft browser with markdown preview, frontmatter table, and gate status panel
- `app/lib/vault.js` filesystem-backed vault reader for `02-DRAFTS/` and `03-REVIEW/` with safe path checks
- `app/app/api/promote/route.js` Node.js API endpoint to run `agent/promote.py --no-commit` with path and gate validation
- `app/app/drafts/approve-button.js` client-side approve action with status and error feedback in the draft browser
- `app/scripts/start-server-bg.ps1` Windows helper to run Next.js dev server in the background
- `app/scripts/stop-server-bg.ps1` Windows helper to stop the tracked background server process

### Changed

- Blueprint Part 0 library README table updated to match actual file paths (`README.md`, not emoji names)
- `agent-instructions.md` now points agents to `_REFERENCE/fit-docs/` for library rules
- `vault-map.md` includes `_REFERENCE/` section
- Phase 3 complete: all promote script checklist items checked in blueprint
- Checked Phase 2 scaffold/templates/system-docs boxes in blueprint Part 10
- Checked all Phase 1 boxes in blueprint Part 10 (Phase 1 complete)
- Updated `.ai/skills/repo.md` with CHANGELOG.md, `.github`, and fit-docs key directories
- Issue template dropdown now shows real phase descriptions from the blueprint
- Removed nonexistent `piv` label from issue template
- Cleaned up stale merged branches
- `agent/promote.py` now resolves output paths from the provided `fit_docs_root` override
- Script naming standardized across docs and vault system files (`promote.py`, `fit-docs_sync.py`, `airtable_sync.py`)
- Repo naming standardized to `fit-docs-forge` in top-level metadata files
- `agent/scaffold_vault.py` now creates `_SYSTEM/naming-conventions.md` and `_SYSTEM/tag-taxonomy.md` placeholder files for Phase 2 consistency
- `app/package.json` scripts now run real `next lint` and `next build` commands instead of placeholders
- `README.md` app status updated from `Placeholder` to `Scaffolded`
- `.ai/skills/repo.md` app structure note updated to reflect the new Next.js scaffold baseline
- `README.md` app status updated to `Active (Phase 4 PR2)` and `app/README.md` now documents vault browser behavior
- Checked the remaining Phase 4 approve box and milestone in the blueprint
- `README.md` app status updated to `Active (Phase 4 PR3)` and `app/README.md` now documents approve endpoint env vars
- `app/package.json` Next.js default `dev` and `start` ports set to `3200`
- Root and app READMEs now document background start/stop commands plus one-line Windows boot autostart task
- Added explicit phase status note indicating Phase 3 is closed
- `.ai/COMMANDS.md` now documents `airtable_sync.py` usage and Airtable env variables
- `agent/airtable_sync.py` default Airtable field mapping updated to `Task Name` / `Due Date` / `Status` / `Assignee Name` and console UTF-8 output handling hardened for Windows
- `.ai/COMMANDS.md` and `agent/.env.example` now document `AIRTABLE_USE_FIELD_IDS` for robust Airtable field mapping
- `.ai/COMMANDS.md` and `agent/.env.example` now include base/table/view display name and top-link settings for dashboard output
- `FIT-Automate-Master-Blueprint-v3.md` upgraded to v3.5 with new Phase 5.5 Safety & Observability section, Part 2/Part 4 additions, corrected Part 6 promote sequence, and Part 10 rollout updates
- Pytest temp/cache config now uses repo-local `.pytest_scratch/` to avoid Windows temp-folder permission issues that caused slow/hanging test runs
- Checked Phase 5 scheduler and milestone boxes in the blueprint
- `agent/.env.example` now includes Airtable base/table/view/field configuration variables
- Checked the Phase 5 `Build airtable_sync.py` box in the blueprint

## 2026-02-26

### Added

- Full v3 master blueprint (864 lines) replacing the placeholder v1 (`d90225a`)
- `.ai/` scaffolding: AGENT.md, COMMANDS.md, piv.config.yaml, templates, skills (`0a9e571`)
- `.github/` plumbing: forge-ci.yml (Python + Next.js gates), dependabot.yml, PR template, issue template (`0a9e571`)
- Agent skeleton: `agent/pyproject.toml`, `.env.example`, placeholder test (`0a9e571`)
- App skeleton: `app/package.json` with placeholder lint/build scripts (`7bc695e`)
- CHANGELOG.md and documentation gate rules (this PR)

### Fixed

- `setup-node` cache path pointed at repo root instead of `app/package-lock.json` (`5075f44`)

### Removed

- Placeholder v1 blueprint (replaced by real v3) (`d90225a`)
