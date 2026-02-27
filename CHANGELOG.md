# Changelog

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- `agent/promote.py` — promote script from blueprint Part 6: validates gates, builds compliant filenames, routes to fit-docs, archives originals
- 19 promote tests covering gate validation, filename building, folder routing, dry-run, and full integration flow
- Scaffold now copies promote.py and sync_fit_docs.py into vault `_SYSTEM/scripts/`
- `.ai/skills/changelog.md` — format rules for CHANGELOG entries
- `agent/scaffold_vault.py` — idempotent script to create the full vault folder tree (blueprint Part 2)
- `agent/tests/test_scaffold_vault.py` — 4 tests covering folder creation, placeholders, idempotency
- `agent/vault_templates/` — 5 Obsidian draft templates verbatim from blueprint Part 5 (sop, kb-article, procedure, solution-description, doc-request)
- Scaffold script now copies templates into `_SYSTEM/templates/` without overwriting user edits
- `agent/vault_system_docs/agent-instructions.md` — embeds Part 0 README-as-schema rule + general agent rules
- `agent/vault_system_docs/vault-map.md` — folder structure quick reference with naming conventions
- Scaffold script now copies system docs into `_SYSTEM/` without overwriting user edits
- `_REFERENCE/fit-docs/` vault folder — read-only mirror of published docs for Obsidian indexing
- `agent/sync_fit_docs.py` — one-way sync from fit-docs/docs/ into vault `_REFERENCE/`
- 4 sync tests covering copy, update, delete, and idempotency

### Changed
- Blueprint Part 0 library README table updated to match actual file paths (README.md, not emoji names)
- `agent-instructions.md` now points agents to `_REFERENCE/fit-docs/` for library rules
- `vault-map.md` includes `_REFERENCE/` section

### Changed
- Checked Phase 2 scaffold/templates/system-docs boxes in blueprint Part 10
- Checked all Phase 1 boxes in blueprint Part 10 — Phase 1 is complete
- Updated `.ai/skills/repo.md` with CHANGELOG.md, .github, fit-docs key directories
- Issue template dropdown now shows real phase descriptions from the blueprint
- Removed nonexistent `piv` label from issue template
- Cleaned up stale merged branches

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
