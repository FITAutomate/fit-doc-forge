# Next.js Preview UI

This directory contains the Next.js App Router UI for documentation review.
Phase 4 PR3 adds browser-based approve-to-promote execution.

## Commands

```bash
npm ci
npm run lint
npm run build
npm run dev
```

## Scope

- `/drafts` reads markdown files from `02-DRAFTS/` and `03-REVIEW/`
- Renders markdown content and parsed frontmatter
- Shows gate field pass/fail panel in read-only mode
- Approve button posts to `POST /api/promote`
- API route validates draft path, status, and gate checks before invoking `agent/promote.py --no-commit`

## Environment

Set environment variables if your local paths differ from defaults:

```bash
VAULT_ROOT=D:\Vaults\FIT-Vault
FIT_DOCS_ROOT=D:\dev\github\fit-docs\docs
# Optional
PYTHON_BIN=python
FIT_FORGE_ROOT=D:\dev\github\fit-docs-forge
```
