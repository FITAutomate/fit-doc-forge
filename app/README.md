# Next.js Preview UI

This directory contains the Next.js App Router UI for documentation review.
Phase 4 PR2 adds a read-only draft browser and frontmatter gate panel.

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
- Approve-to-promote action remains a later PR

## Environment

Set `VAULT_ROOT` to your local vault path if different from the default:

```bash
VAULT_ROOT=D:\Vaults\FIT-Vault
```
