# Changelog

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- `.ai/skills/changelog.md` — format rules for CHANGELOG entries

### Changed
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
