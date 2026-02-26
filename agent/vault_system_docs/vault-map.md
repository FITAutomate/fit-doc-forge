# Vault Map

> Quick reference for the FIT-Vault folder structure.
> See the full blueprint in `fit-docs-forge/FIT-Automate-Master-Blueprint-v3.md`, Part 2.

## Folder Structure

| Folder | Purpose | Who Writes |
|---|---|---|
| `00-INBOX/` | Quick captures, brain dumps, voice notes | Human |
| `00-INBOX/_agent-drop/` | Agent first drafts land here for review | Agent |
| `01-PLANNING/ideas/` | Feature ideas, future content | Human |
| `01-PLANNING/requests/` | Structured doc requests (sop, kb, procedure, solution, service) | Human / Agent |
| `01-PLANNING/roadmap/` | Content roadmap and priorities | Human |
| `02-DRAFTS/` | Active drafts, mirrors fit-docs library structure | Agent / Human |
| `03-REVIEW/` | Drafts approaching gate-complete, awaiting final review | Human |
| `04-OPERATIONS/` | Ops dashboard, daily briefings, decisions log | Agent / Human |
| `05-KNOWLEDGE/` | AI tools, prompts, research, lessons learned | Human |
| `06-CLIENTS/` | Per-client folders (overview, notes, comms) | Human |
| `07-ARCHIVE/promoted/` | Successfully promoted drafts (moved here after publish) | Script |
| `07-ARCHIVE/abandoned/` | Drafts that won't be published | Human |
| `_SYSTEM/` | Templates, scripts, agent rules, vault metadata | Agent / Human |

## Draft Subfolders (02-DRAFTS/)

These mirror the `fit-docs/docs/` structure exactly:

| Subfolder | Maps to fit-docs |
|---|---|
| `Blog/` | `blog/posts/` |
| `Finance/` | `Finance/` |
| `Knowledge-Base/` | `Knowledge Base/` |
| `Operations/SOPs/` | `Operations/SOPs/` |
| `Operations/Procedures/` | `Operations/Procedures/` |
| `project/` | `project/` |
| `Services/` | `Services/` |
| `Solutions/` | `Solutions/` |
| `Test-Examples/` | `Test Examples/` |

## System Files (_SYSTEM/)

| File | Purpose |
|---|---|
| `agent-instructions.md` | Rules every AI tool must follow (Part 0 + general rules) |
| `vault-map.md` | This file |
| `naming-conventions.md` | File naming rules across all libraries |
| `tag-taxonomy.md` | Approved tags for Obsidian |
| `changelog.md` | Log of agent actions in the vault |
| `templates/` | Obsidian draft templates (hotkey starting points) |
| `scripts/` | fit-promote.py, fit-airtable-sync.py |

## Naming Conventions (Quick Reference)

| Type | Pattern | Example |
|---|---|---|
| SOP draft | `DRAFT-sop-NN-title.md` | `DRAFT-sop-21-onboarding.md` |
| Procedure draft | `DRAFT-procedure-system-title.md` | `DRAFT-procedure-teams-new-channel.md` |
| KB draft | `DRAFT-kb-title.md` | `DRAFT-kb-password-policy.md` |
| Published SOP | `SOP NN - Title.md` | `SOP 21 - Onboarding.md` |
| Published Procedure | `PROC - System - Title.md` | `PROC - Teams - New Channel.md` |
| Published KB | `KB - Title.md` | `KB - Password Policy.md` |
