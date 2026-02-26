# FIT Automate — Obsidian + MkDocs PIV Pipeline
## Master Blueprint v3.0
**Windows Local | AI-Agnostic | Single Source of Truth**
*Supersedes v2.0*

---

## THE SYSTEM IN ONE SENTENCE

Obsidian is your pre-commit authoring workspace (Plan + Implement).
fit-docs is your published source of truth (Validate + Publish).
A promote script is the only bridge between them.

```
Brain → Obsidian (capture → draft → gate) → promote script → fit-docs commit → CI → Live
```

---

## ⚡ WHAT'S NEW IN v3.0

- **README-as-Schema rule** added as Part 0 — the foundational rule all agents must follow
- **fit-docs-forge** introduced as the agent system repo that powers this pipeline
- Part 4 YAML clarified: universal base only — library READMEs override
- Part 10 phased rollout updated to reflect forge-first build order

---

## PART 0: README-AS-SCHEMA RULE (Agent Law — Read First)

> **This is the most important rule in the system. Every agent must follow it before touching any file.**

### The Rule

Every library folder inside `fit-docs/docs/` contains a `README.md`.
That README is the **complete specification** for every document in that folder.

Before an agent creates, edits, or rewrites any file in a library folder, it **must**:

1. Read that folder's `README.md`
2. Extract from it:
   - File naming convention
   - Metadata table fields (the markdown table, not YAML)
   - Required H2/H3 sections in order
   - Content rules and restrictions
3. Apply only what the README defines — nothing invented, nothing from memory

### Why This Exists

The master YAML in Part 4 is a universal base — it captures fields shared across all doc types.
But each library has its own shape. The SOP README defines RACI tables. The KB README defines
`KB_TARGET`. The Procedure README defines numbered H3 steps. These rules live in the README,
not in the agent prompt.

This means:
- You update one README → re-run the agent → every file in that folder conforms
- No hardcoded templates to maintain in code
- No divergence between what the README says and what the agent does

### The Override Rule

If the library README and Part 4 master YAML conflict on any field name, format, or structure —
**the README wins.**

### Current Library READMEs

| Library | README Location | Controls |
|---|---|---|
| SOPs | `docs/Operations/👮 SOP Library Rules.md` | Naming, metadata table, required sections |
| Procedures | `docs/Operations/👮 Procedures Library Rules.md` | Naming, metadata table, steps format |
| Knowledge Base | `docs/Knowledge Base/👮 Knowledge Base Library Rules.md` | Naming, metadata table, KB_TARGET |

### Folder-Level Rewrite Command

When you want to rewrite an entire library to a new spec:

1. Update the library's README with the new rules
2. Run: `fit-forge rewrite --folder Operations/SOPs`
3. Agent reads the updated README, diffs every file, rewrites non-conforming files
4. You review diffs in the Next.js preview UI
5. You approve → promote script runs for each file

---

## PART 1: FIT-DOCS STRUCTURE (Actual, as-built)

This is what exists in your repo. Never duplicated in Obsidian — only fed by it.

```
fit-docs/docs/
├── blog/
│   └── posts/                        ← Agent daily briefings land here
├── Finance/                          ← Scaffolded / Coming Soon
│   ├── receipts/
│   ├── invoices/
│   └── subscriptions/
├── home/
│   ├── index.md                      ← mkdocs_hooks.py Daily Snapshot target
│   ├── about.md
│   └── status.md
├── Knowledge Base/                   ← Client-facing KB articles
│   └── 👮 Knowledge Base Library Rules.md   ← README-as-schema source
├── Operations/                       ← Internal governance
│   ├── 👮 SOP Library Rules.md               ← README-as-schema source
│   ├── 👮 Procedures Library Rules.md        ← README-as-schema source
│   ├── SOPs/                         ← 📚 SOP NN — Title.md
│   └── Procedures/                   ← 📋 PROC — System — Title.md
├── project/                          ← PIV bootstrap + active project docs
├── Services/
│   ├── ai-readiness-audit.md
│   ├── intelligent-automation.md
│   └── ai-enablement.md
├── Solutions/
│   ├── fit-docs/
│   │   ├── description.md
│   │   └── README.md
│   ├── fit-web/
│   │   ├── description.md
│   │   └── README.md
│   └── fit-rag/
│       ├── description.md
│       └── README.md
├── stylesheets/                      ← Platform only, never authored
├── Test Examples/                    ← Sandbox, scaffold only
└── index.md
```

---

## PART 2: OBSIDIAN VAULT STRUCTURE

Location: `D:\Vaults\FIT-Vault\`

`02-DRAFTS/` mirrors `fit-docs/docs/` exactly. Every other folder serves authoring and operations.

```
D:\Vaults\FIT-Vault\
│
├── 00-INBOX/
│   ├── _quick-capture.md             ← Daily brain dump. Ideas, requests, voice notes.
│   └── _agent-drop/                  ← Agents write first drafts here for your review
│
├── 01-PLANNING/
│   ├── ideas/
│   ├── requests/
│   │   ├── sop-requests/
│   │   ├── kb-requests/
│   │   ├── procedure-requests/
│   │   ├── solution-requests/
│   │   └── service-requests/
│   └── roadmap/
│
├── 02-DRAFTS/                        ← MIRRORS fit-docs/docs/ exactly
│   ├── Blog/
│   ├── Finance/
│   ├── Knowledge-Base/
│   ├── Operations/
│   │   ├── SOPs/                     ← DRAFT-sop-NN-title.md
│   │   └── Procedures/               ← DRAFT-procedure-title.md
│   ├── project/
│   ├── Services/
│   ├── Solutions/
│   │   ├── fit-docs/
│   │   ├── fit-web/
│   │   ├── fit-rag/
│   │   └── _new-solution-template/
│   └── Test-Examples/
│
├── 03-REVIEW/
│   ├── Operations/
│   │   ├── SOPs/
│   │   └── Procedures/
│   ├── Knowledge-Base/
│   ├── Solutions/
│   ├── Services/
│   └── Blog/
│
├── 04-OPERATIONS/
│   ├── _ops-dashboard.md
│   ├── _daily-briefing.md
│   └── decisions/
│
├── 05-KNOWLEDGE/
│   ├── ai-tools/
│   ├── prompts/
│   ├── research/
│   └── lessons-learned/
│
├── 06-CLIENTS/
│   └── [client-name]/
│       ├── overview.md
│       ├── notes.md
│       └── comms/
│
├── 07-ARCHIVE/
│   ├── promoted/
│   └── abandoned/
│
└── _SYSTEM/
    ├── agent-instructions.md         ← Rules every AI tool must follow (includes Part 0)
    ├── vault-map.md
    ├── naming-conventions.md
    ├── tag-taxonomy.md
    ├── changelog.md
    ├── templates/
    │   ├── sop-draft.md
    │   ├── procedure-draft.md
    │   ├── kb-article-draft.md
    │   ├── solution-description.md
    │   ├── solution-readme.md
    │   ├── service-page.md
    │   └── doc-request.md
    └── scripts/
        ├── fit-promote.py
        └── fit-airtable-sync.py
```

---

## PART 3: NAMING CONVENTIONS

### Obsidian Draft Files
```
DRAFT-sop-21-aws-s3-backup.md
DRAFT-procedure-deploy-mkdocs.md
DRAFT-kb-what-is-fit-rag.md
DRAFT-blog-2025-03-01-march-update.md
```

### fit-docs Published Files (built by promote script — never manual)
```
📚 SOP 21 — AWS S3 Backup Configuration.md
📋 PROC — Deploy — MkDocs to Production.md
📘 KB — What Is FIT RAG.md
```

### Never Use
- Spaces in filenames
- `temp`, `misc`, `notes`, `untitled`
- Dates buried in the middle: `sop-2025-aws.md` ← wrong

---

## PART 4: FRONTMATTER SCHEMA

> **Universal Base Only.** These fields apply to all doc types.
> Library-specific fields are defined in each library's README.
> If a README defines a field differently than this table — the README wins.

### All Docs (Universal Base)
```yaml
---
title: ""
type: sop           # sop | procedure | kb-article | solution | service | blog | request
status: draft       # captured | draft | review | promote-ready | promoted
visibility: Internal  # Internal | Public | Dual
kb_target: INTERNAL   # INTERNAL | PUBLIC_WEB
publish_ready: false
redaction_needed: none  # none | light | heavy
version: "0.1"
owner: ""
created: 2025-02-25
updated: 2025-02-25
source_basis: ""
airtable_id: ""
# Publish gate — all relevant fields must be true before promote script runs
gate_has_owner: false
gate_metadata_complete: false
gate_heading_structure_valid: false
gate_reviewed_by_human: false
gate_no_internal_refs: false    # PUBLIC_WEB / Dual only
gate_no_invented_slas: false    # PUBLIC_WEB / Dual only
---
```

### Extended: SOP (defined by SOP README — these extend the base)
```yaml
sop_number: 21
applies_to: ""
review_cycle: Quarterly
raci_responsible: ""
raci_accountable: ""
```

### Extended: Solution
```yaml
solution_slug: fit-rag
solution_status: active     # planned | active | beta | deprecated
repo_url: ""
deploy_url: ""
```

---

## PART 5: TEMPLATES

> Templates in `_SYSTEM/templates/` are Obsidian authoring aids only.
> The agent derives structure from the library README, not from these templates.
> These templates exist so you can hit a hotkey and get a pre-filled draft in Obsidian.

### SOP Draft (`_SYSTEM/templates/sop-draft.md`)
```markdown
---
title: ""
type: sop
sop_number:
status: draft
visibility: Internal
kb_target: INTERNAL
publish_ready: false
redaction_needed: none
version: "0.1"
owner: ""
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}
source_basis: ""
airtable_id: ""
applies_to: ""
review_cycle: Quarterly
gate_has_owner: false
gate_metadata_complete: false
gate_heading_structure_valid: false
gate_reviewed_by_human: false
gate_no_internal_refs: false
gate_no_invented_slas: false
---

| Field | Value |
|---|---|
| Title | |
| Type | SOP Plan / Standard / Policy |
| SOP_TARGET | INTERNAL / PUBLIC_WEB |
| Visibility | Internal / Public |
| Publish Ready | No |
| Redaction Needed | None / Light / Heavy |
| Version | 0.1 |
| Owner | |
| Last Updated | {{date:YYYY-MM-DD}} |
| Applies To | |

# <Clean Title>

## Purpose

## Scope

## Standards

## Procedure

### Step 1:
**What:**
**Why:**
**How:**
**Expected result:**

## Roles and Responsibilities (RACI)
| Role | R | A | C | I |
|---|---|---|---|---|
| | | | | |

## Exceptions

## Review Cadence

## Changelog
| Date | Version | Change | Author |
|---|---|---|---|
| {{date:YYYY-MM-DD}} | 0.1 | Initial draft | |
```

### KB Article Draft (`_SYSTEM/templates/kb-article-draft.md`)
```markdown
---
title: ""
type: kb-article
status: draft
visibility: Public
kb_target: PUBLIC_WEB
publish_ready: false
redaction_needed: none
version: "0.1"
owner: ""
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}
gate_has_owner: false
gate_metadata_complete: false
gate_heading_structure_valid: false
gate_reviewed_by_human: false
gate_no_internal_refs: false
gate_no_invented_slas: false
---

| Field | Value |
|---|---|
| Title | |
| Type | Overview / Service / FAQ / Policy / Glossary |
| KB_TARGET | PUBLIC_WEB / INTERNAL |
| Visibility | Public / Internal |
| Publish Ready | No |
| Redaction Needed | None / Light / Heavy |
| Version | 0.1 |
| Owner | |
| Last Updated | {{date:YYYY-MM-DD}} |
| Categories | |
| Tags | |

# <Clean Title>

## Overview

## Who It Is For

## What It Includes

## What It Is Not

## Next Step / Related Links
```

### Procedure Draft (`_SYSTEM/templates/procedure-draft.md`)
```markdown
---
title: ""
type: procedure
status: draft
visibility: Internal
kb_target: INTERNAL
publish_ready: false
redaction_needed: none
version: "0.1"
owner: ""
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}
system: ""
app: ""
estimated_time: ""
gate_has_owner: false
gate_metadata_complete: false
gate_heading_structure_valid: false
gate_reviewed_by_human: false
---

| Field | Value |
|---|---|
| Title | |
| Library | PROC |
| Type | Procedure |
| Visibility | Internal / Public |
| Publish Ready | No |
| Redaction Needed | None / Light / Heavy |
| Version | 0.1 |
| Owner | |
| Last Updated | {{date:YYYY-MM-DD}} |
| System | |
| App | |
| Estimated Time | |
| Prereqs | |
| Tags | |

# <Clean Title>

## Goal

## When to Use This

## Prerequisites
- [ ]

## Procedure

### 1. Step Name

### 2. Step Name

## Troubleshooting

## Related Links
```

### Solution description.md (`_SYSTEM/templates/solution-description.md`)
```markdown
---
title: ""
type: solution
solution_slug: ""
status: draft
visibility: Public
kb_target: PUBLIC_WEB
publish_ready: false
redaction_needed: none
version: "0.1"
owner: ""
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}
gate_has_owner: false
gate_metadata_complete: false
gate_no_internal_refs: false
gate_no_invented_slas: false
gate_heading_structure_valid: false
gate_reviewed_by_human: false
---

| Field | Value |
|---|---|
| Title | |
| Type | FIT Solution |
| Visibility | Public |
| Publish Ready | No |
| Version | 0.1 |
| Owner | |
| Last Updated | {{date:YYYY-MM-DD}} |

# <Solution Name>

<One to two sentences. What it is and what problem it solves. Used verbatim in web and content.>
```

### Doc Request / Capture (`_SYSTEM/templates/doc-request.md`)
```markdown
---
title: ""
type: request
request_type: sop   # sop | procedure | kb-article | solution | service | blog
status: captured
created: {{date:YYYY-MM-DD}}
airtable_id: ""
---

## What I Need

## Why / Context

## Key Points to Cover
-
-

## Related Existing Docs

## Agent Prompt Seed
```

---

## PART 6: THE PROMOTE SCRIPT

> Full source: `_SYSTEM/scripts/fit-promote.py`
> This script is also maintained in the `fit-docs-forge` repo as the canonical version.

```python
# _SYSTEM/scripts/fit-promote.py
# Validates gate, routes file to correct fit-docs folder,
# builds compliant filename, strips Obsidian frontmatter, commits to Git.

import sys, re, shutil, subprocess, yaml
from pathlib import Path
from datetime import date

VAULT_ROOT    = Path(r"D:\Vaults\FIT-Vault")
FIT_DOCS_ROOT = Path(r"D:\Dev\fit-docs\docs")  # ← update to your actual path

DRAFT_TO_DOCS = {
    "Blog":                   "blog/posts",
    "Finance":                "Finance",
    "Knowledge-Base":         "Knowledge Base",
    "Operations/SOPs":        "Operations/SOPs",
    "Operations/Procedures":  "Operations/Procedures",
    "project":                "project",
    "Services":               "Services",
    "Solutions":              "Solutions",
    "Test-Examples":          "Test Examples",
}

TYPE_TO_EMOJI = {
    "sop":        "📚",
    "procedure":  "📋",
    "kb-article": "📘",
    "solution":   None,
    "service":    None,
    "blog":       None,
}

GATE_FIELDS = [
    "gate_has_owner",
    "gate_metadata_complete",
    "gate_heading_structure_valid",
    "gate_reviewed_by_human",
]

PUBLIC_GATE_FIELDS = [
    "gate_no_internal_refs",
    "gate_no_invented_slas",
]

def load_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]

def check_gate(fm):
    failures = [f for f in GATE_FIELDS if not fm.get(f, False)]
    if fm.get("kb_target") in ("PUBLIC_WEB", "Dual"):
        failures += [f for f in PUBLIC_GATE_FIELDS if not fm.get(f, False)]
    return failures

def build_filename(fm, original_name):
    doc_type = fm.get("type", "")
    emoji    = TYPE_TO_EMOJI.get(doc_type)
    if emoji is None:
        return original_name
    title = fm.get("title", "untitled").strip()
    if doc_type == "sop":
        num = str(fm.get("sop_number", "XX")).zfill(2)
        return f"{emoji} SOP {num} — {title}.md"
    elif doc_type == "procedure":
        return f"{emoji} PROC — {title}.md"
    elif doc_type == "kb-article":
        return f"{emoji} KB — {title}.md"
    return f"{emoji} {title}.md"

def promote(draft_rel_path):
    draft_path = VAULT_ROOT / draft_rel_path
    if not draft_path.exists():
        print(f"❌ File not found: {draft_path}"); sys.exit(1)

    fm, body = load_frontmatter(draft_path)

    if fm.get("status") != "promote-ready":
        print(f"❌ Status is '{fm.get('status')}' — must be 'promote-ready'")
        sys.exit(1)

    failures = check_gate(fm)
    if failures:
        print("❌ Publish gate failed:")
        for f in failures: print(f"   - {f}: must be true")
        sys.exit(1)

    target_folder = resolve_target_folder(draft_rel_path)
    target_folder.mkdir(parents=True, exist_ok=True)

    filename    = build_filename(fm, draft_path.name)
    target_path = target_folder / filename
    body        = update_last_updated(body)

    target_path.write_text(body.lstrip(), encoding="utf-8")
    print(f"✅ Promoted → {target_path}")

    archive = VAULT_ROOT / "07-ARCHIVE" / "promoted" / draft_path.name
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(draft_path, archive)

    draft_path.write_text(
        "---\n" + yaml.dump({**fm, "status": "promoted", "updated": str(date.today())})
        + f"---\n{body}", encoding="utf-8"
    )

    git_root = FIT_DOCS_ROOT.parent
    subprocess.run(["git", "add", str(target_path)], cwd=git_root, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"docs: promote {filename}"],
        cwd=git_root, check=True
    )
    print(f"✅ Git committed: docs: promote {filename}")
    print("\n🚀 Done. Run: .\\venv\\Scripts\\mkdocs.exe build --strict")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fit-promote.py <vault-relative-draft-path>")
        sys.exit(1)
    promote(sys.argv[1])
```

---

## PART 7: THE AUTHORING WORKFLOW

### Status Flow (Every Draft)
```
captured → draft → review → promote-ready → [script] → promoted
    ↑ Plan       ↑ Implement             ↑ Validate    ↑ Publish
```

### For a New SOP
```
1. CAPTURE   → 00-INBOX/_quick-capture.md

2. DRAFT     → Agent reads SOP README → drafts using sop-draft.md template
               Save to: 02-DRAFTS/Operations/SOPs/DRAFT-sop-21-title.md

3. ELABORATE → You edit in Obsidian

4. GATE      → Flip frontmatter: status: promote-ready, gate_*: true

5. PROMOTE   → python fit-promote.py "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-..."
               → Lands in fit-docs/docs/Operations/SOPs/📚 SOP 21 — Title.md
               → Git committed → mkdocs build --strict validates
```

### For a New Solution
```
1. CAPTURE   → 01-PLANNING/requests/solution-requests/
2. DRAFT x2  → description.md + README.md in 02-DRAFTS/Solutions/fit-newproduct/
3. GATE      → Both files need gate fields true
4. PROMOTE   → Run script twice — one call per file
```

### Agent System Prompt (Universal)
```
You are a documentation agent for FIT Automate.

CRITICAL — Before touching any file in a library folder:
1. Read that folder's README.md (the 👮 file at the folder root)
2. Extract naming convention, metadata table fields, required sections, content rules
3. Apply only what the README defines — nothing invented, nothing from memory
4. If README and master YAML conflict — README wins

Context: [paste _SYSTEM/vault-map.md]
Rules:
- Do NOT invent SLAs, prices, or numbers unless explicitly provided
- Set all gate_ fields to false, status to draft
- For PUBLIC_WEB docs: no internal tool names, no internal process references
- Output the complete markdown file only — no commentary, no preamble

Request: [paste capture note]
```

---

## PART 8: DAILY BRIEFING PIPELINE

```
07:00 daily (Windows Task Scheduler)
  ↓  fit-airtable-sync.py
     → Pulls overdue + due-today from Airtable
     → Overwrites 04-OPERATIONS/_ops-dashboard.md

  ↓  fit-briefing-agent.py  (Phase 4 — build after promote script proven)
     → Reads _ops-dashboard.md
     → Reads 02-DRAFTS/ file count per folder
     → Reads _SYSTEM/changelog.md (last 7 days)
     → Writes fit-docs/docs/blog/posts/YYYY-MM-DD-daily-snapshot.md

  ↓  mkdocs_hooks.py (already built)
     → Extracts Next Steps + Highlights
     → Injects Daily Snapshot into docs/home/index.md
```

---

## PART 9: PLUGIN STACK

**Tier 1 — Day 1 (Core)**
| Plugin | Why |
|---|---|
| Dataview | Query vault like a database |
| Templater | Template engine with date logic |
| Tasks | Task tracking with due dates |

**Tier 2 — Week 1 (Workflow)**
| Plugin | Why |
|---|---|
| QuickAdd | Rapid capture to correct location |
| Shell Commands | Run promote script from inside Obsidian |
| Commander | Toolbar buttons for promote, sync, capture |

**Tier 3 — Month 2 (Automation)**
| Plugin | Why |
|---|---|
| Local REST API | Vault at localhost:27123 — agent gateway |
| Obsidian-Git | Auto-commit vault on schedule |
| Kanban | Visual board for draft pipeline status |

---

## PART 10: PHASED ROLLOUT

### Phase 1 — fit-docs-forge Repo (Week 1)
> Build the agent system first. Everything else runs on top of it.
- [ ] Create `fit-docs-forge` repo from PIV bootstrap
- [ ] Run PIV loop: `.ai/` scaffolding + CI passes
- [ ] Seed `FIT-Automate-Master-Blueprint-v3.md` as the plan
- [ ] Agent reads blueprint → proposes Phase 2 PRs
- [ ] **Milestone:** PIV loop is live. Agent can read the plan and propose work.

### Phase 2 — Vault Foundation (Days 3-5)
- [ ] Create `D:\Vaults\FIT-Vault\` with full folder structure (Part 2)
- [ ] Create all 7 templates in `_SYSTEM/templates/`
- [ ] Create `_SYSTEM/agent-instructions.md` (embed Part 0 README-as-schema rule)
- [ ] Create `_SYSTEM/vault-map.md`
- [ ] Install Obsidian → open FIT-Vault
- [ ] Install Tier 1 plugins
- [ ] **Milestone:** You can draft and organize content in Obsidian

### Phase 3 — Promote Script (Days 5-7)
- [ ] `pip install pyyaml`
- [ ] Save `fit-promote.py` to `_SYSTEM/scripts/`
- [ ] Update `FIT_DOCS_ROOT` to your actual fit-docs path
- [ ] Test on a throwaway draft — confirm file lands correctly
- [ ] Confirm `mkdocs build --strict` passes after promote
- [ ] Install Shell Commands plugin → wire promote as a hotkey
- [ ] **Milestone:** One command ships a doc from Obsidian to fit-docs

### Phase 4 — Next.js Preview UI (Week 2)
> The fit-docs-forge `/app` directory. Preview rendered MD without opening Typora.
- [ ] Scaffold Next.js app in `fit-docs-forge/app/`
- [ ] Wire to vault path — reads `02-DRAFTS/` and `03-REVIEW/` folders
- [ ] Render MD files with frontmatter panel (shows gate status)
- [ ] Approve button → triggers promote script via Python API
- [ ] **Milestone:** Review and approve docs from browser. No Typora needed.

### Phase 5 — Airtable Bridge (Week 2-3)
- [ ] Get Airtable API key + Base/Table IDs
- [ ] Build `fit-airtable-sync.py`
- [ ] Windows Task Scheduler: every 60 minutes
- [ ] **Milestone:** Airtable tasks visible in Obsidian automatically

### Phase 6 — Agent Automation (Month 2)
- [ ] Install Local REST API plugin
- [ ] Build `fit-briefing-agent.py`
- [ ] Agent scans `01-PLANNING/requests/` → auto-drafts to `02-DRAFTS/`
- [ ] **Milestone:** Wake up to a daily briefing. Vault updates itself.

### Phase 7 — Folder Rewrite Command (Month 2-3)
- [ ] `fit-forge rewrite --folder <library>` command
- [ ] Agent reads README → diffs all files → rewrites non-conforming
- [ ] Diffs surfaced in Next.js UI for review
- [ ] **Milestone:** Update one README, re-run, entire folder conforms.

---

## QUICK REFERENCE

### 5 Files You'll Touch Daily
| File | Purpose |
|---|---|
| `00-INBOX/_quick-capture.md` | Brain dump |
| `04-OPERATIONS/_ops-dashboard.md` | Airtable task mirror |
| `04-OPERATIONS/_daily-briefing.md` | Morning priorities |
| `02-DRAFTS/` | Active drafts |
| `_SYSTEM/changelog.md` | What the agents did |

### The Command That Ships a Doc
```powershell
python D:\Vaults\FIT-Vault\_SYSTEM\scripts\fit-promote.py "02-DRAFTS/<path-to-draft>"
```

### What Belongs Where
| Content | Lives In | Never In |
|---|---|---|
| Published SOPs | fit-docs only | Obsidian |
| Draft SOPs | Obsidian `02-DRAFTS/` until promoted | fit-docs |
| Solution description.md | Obsidian draft → promoted → consumed by fit-web | Nowhere else |
| Prompt library | Obsidian `05-KNOWLEDGE/prompts/` | fit-docs |
| Agent rules | Obsidian `_SYSTEM/` + fit-docs-forge `.ai/` | Nowhere else |

---

*FIT Automate Internal | v3.0 | February 2025*
*Single source of truth. All previous drafts superseded.*
