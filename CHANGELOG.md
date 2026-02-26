# Changelog

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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
