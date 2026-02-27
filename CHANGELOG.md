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
- `pytest.ini` at repo root so `pytest` resolves `agent/` modules when run from repo root
- 4 sync tests covering copy, update, delete, and idempotency
- `app/` minimal real Next.js App Router scaffold (`app/app/layout.js`, `app/app/page.js`, `app/app/globals.css`, `.eslintrc.json`)
- `app/app/drafts/page.js` read-only draft browser with markdown preview, frontmatter table, and gate status panel
- `app/lib/vault.js` filesystem-backed vault reader for `02-DRAFTS/` and `03-REVIEW/` with safe path checks

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
