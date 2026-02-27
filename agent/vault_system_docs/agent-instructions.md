# Agent Instructions

> These rules apply to every AI tool, agent, or automation that operates inside this vault.
> Read this file completely before creating, editing, or moving any file.

---

## Part 0: README-as-Schema Rule (Agent Law)

**This is the most important rule in the system.**

Every library folder in the published `fit-docs` repo contains a `README.md`.
That README is the **complete specification** for every document in that folder.

A read-only mirror of fit-docs lives inside this vault at `_REFERENCE/fit-docs/`.
This is where you (and agents) find the rules and published docs without leaving Obsidian.

Before an agent creates, edits, or rewrites any file in a library folder, it **must**:

1. Read that library's `README.md` from `_REFERENCE/fit-docs/`
2. Extract from it:
   - File naming convention
   - Metadata table fields (the markdown table, not YAML)
   - Required H2/H3 sections in order
   - Content rules and restrictions
3. Apply only what the README defines — nothing invented, nothing from memory

### The Override Rule

If the library README and the master YAML conflict on any field name, format, or structure —
**the README wins.**

### Current Library READMEs

| Library | Vault path (inside `_REFERENCE/fit-docs/`) | Controls |
|---|---|---|
| SOPs | `Operations/SOPs/README.md` | Naming, metadata table, required sections |
| Procedures | `Operations/Procedures/README.md` | Naming, metadata table, steps format |
| Knowledge Base | `Knowledge Base/README.md` | Naming, metadata table, KB_TARGET |

### Keeping _REFERENCE/ Current

Run the sync script whenever fit-docs changes:

```
python _SYSTEM/scripts/fit-docs_sync.py
```

This is a one-way mirror. **Never edit files in `_REFERENCE/`** — they will be overwritten on next sync.

---

## General Agent Rules

1. **Never invent** SLAs, prices, numbers, or facts not present in existing docs or the blueprint.
2. **Never publish directly** — all drafts go through the promote script after human review.
3. **Always draft in `02-DRAFTS/`** — never write directly to `03-REVIEW/` or the fit-docs repo.
4. **Prefix draft filenames** with `DRAFT-` (e.g. `DRAFT-sop-21-onboarding.md`).
5. **Fill all gate fields as `false`** on initial draft — only a human sets them to `true`.
6. **One document per file** — no multi-doc bundles.
7. **Use templates** from `_SYSTEM/templates/` as starting points, but the library README is the authority.

---

## Drafting Workflow

```
1. CAPTURE   → 00-INBOX/_quick-capture.md or 01-PLANNING/requests/
2. DRAFT     → Agent reads library README → drafts into 02-DRAFTS/<library>/
3. ELABORATE → Human edits in Obsidian
4. REVIEW    → Move to 03-REVIEW/ when gate fields are approaching ready
5. PROMOTE   → Run promote.py → file lands in fit-docs with compliant name
6. ARCHIVE   → Original moves to 07-ARCHIVE/promoted/
```

---

## Gate Fields

Every draft must include these frontmatter booleans. All must be `true` before promotion.

| Gate Field | Meaning |
|---|---|
| `gate_has_owner` | Document has an assigned owner |
| `gate_metadata_complete` | All required metadata fields are filled |
| `gate_heading_structure_valid` | H2/H3 structure matches the library README |
| `gate_reviewed_by_human` | A human has reviewed and approved |
| `gate_no_internal_refs` | No internal-only references in public docs |
| `gate_no_invented_slas` | No made-up SLAs, prices, or metrics |

---

## File Paths

| What | Path |
|---|---|
| Vault root | `D:\Vaults\FIT-Vault\` |
| Published docs (external) | `D:\Dev\fit-docs\docs\` |
| Published docs (vault mirror) | `_REFERENCE\fit-docs\` |
| Agent system repo | `D:\dev\github\fit-docs-forge\` |
| Templates | `_SYSTEM\templates\` |
| Promote script | `_SYSTEM\scripts\promote.py` |
| fit-docs sync script | `_SYSTEM\scripts\fit-docs_sync.py` |
| Airtable sync script | `_SYSTEM\scripts\airtable_sync.py` |
