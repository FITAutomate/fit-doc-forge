# FIT Automate — Obsidian + MkDocs PIV Pipeline | Master Blueprint v3.5
**Windows Local | AI-Agnostic | Single Source of Truth**
*Supersedes v2.0*

---

## THE SYSTEM IN ONE SENTENCE

Obsidian is your pre-commit authoring workspace (Plan + Implement).
fit-docs is your published source of truth (Validate + Publish).
A promote script is the only bridge between them.

```
Brain â†’ Obsidian (capture â†’ draft â†’ gate) â†’ promote script â†’ fit-docs commit â†’ CI â†’ Live
```

---

## ⚡ WHAT'S NEW IN v3.5

- **README-as-Schema rule** added as Part 0 â€” the foundational rule all agents must follow
- **fit-docs-forge** introduced as the agent system repo that powers this pipeline
- Part 4 YAML clarified: universal base only â€” library READMEs override
- Part 10 phased rollout updated to reflect forge-first build order
- Phase 5.5 Safety & Observability layer added — Audit Trail, Rollback, Health Dashboard, Dependency Graph, Template Diff Alerter
---

## PART 0: README-AS-SCHEMA RULE (Agent Law â€” Read First)

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
3. Apply only what the README defines â€” nothing invented, nothing from memory

### Why This Exists

The master YAML in Part 4 is a universal base â€” it captures fields shared across all doc types.
But each library has its own shape. The SOP README defines RACI tables. The KB README defines
`KB_TARGET`. The Procedure README defines numbered H3 steps. These rules live in the README,
not in the agent prompt.

This means:
- You update one README â†’ re-run the agent â†’ every file in that folder conforms
- No hardcoded templates to maintain in code
- No divergence between what the README says and what the agent does

### The Override Rule

If the library README and Part 4 master YAML conflict on any field name, format, or structure â€”
**the README wins.**

### Current Library READMEs

| Library | Location in fit-docs | Vault mirror path | Controls |
|---|---|---|---|
| SOPs | `docs/Operations/SOPs/README.md` | `_REFERENCE/fit-docs/Operations/SOPs/README.md` | Naming, metadata table, required sections |
| Procedures | `docs/Operations/Procedures/README.md` | `_REFERENCE/fit-docs/Operations/Procedures/README.md` | Naming, metadata table, steps format |
| Knowledge Base | `docs/Knowledge Base/README.md` | `_REFERENCE/fit-docs/Knowledge Base/README.md` | Naming, metadata table, KB_TARGET |

### Folder-Level Rewrite Command

When you want to rewrite an entire library to a new spec:

1. Update the library's README with the new rules
2. Run: `fit-forge rewrite --folder Operations/SOPs`
3. Agent reads the updated README, diffs every file, rewrites non-conforming files
4. You review diffs in the Next.js preview UI
5. You approve â†’ promote script runs for each file

---

## PART 1: FIT-DOCS STRUCTURE (Actual, as-built)

This is what exists in your repo. Never duplicated in Obsidian â€” only fed by it.

```
fit-docs/docs/
â”œâ”€â”€ blog/
â”‚   â””â”€â”€ posts/                        â† Agent daily briefings land here
â”œâ”€â”€ Finance/                          â† Scaffolded / Coming Soon
â”‚   â”œâ”€â”€ receipts/
â”‚   â”œâ”€â”€ invoices/
â”‚   â””â”€â”€ subscriptions/
â”œâ”€â”€ home/
â”‚   â”œâ”€â”€ index.md                      â† mkdocs_hooks.py Daily Snapshot target
â”‚   â”œâ”€â”€ about.md
â”‚   â””â”€â”€ status.md
â”œâ”€â”€ Knowledge Base/                   â† Client-facing KB articles
â”‚   â””â”€â”€ ðŸ‘® Knowledge Base Library Rules.md   â† README-as-schema source
â”œâ”€â”€ Operations/                       â† Internal governance
â”‚   â”œâ”€â”€ ðŸ‘® SOP Library Rules.md               â† README-as-schema source
â”‚   â”œâ”€â”€ ðŸ‘® Procedures Library Rules.md        â† README-as-schema source
â”‚   â”œâ”€â”€ SOPs/                         â† ðŸ“š SOP NN â€” Title.md
â”‚   â””â”€â”€ Procedures/                   â† ðŸ“‹ PROC â€” System â€” Title.md
â”œâ”€â”€ project/                          â† PIV bootstrap + active project docs
â”œâ”€â”€ Services/
â”‚   â”œâ”€â”€ ai-readiness-audit.md
â”‚   â”œâ”€â”€ intelligent-automation.md
â”‚   â””â”€â”€ ai-enablement.md
â”œâ”€â”€ Solutions/
â”‚   â”œâ”€â”€ fit-docs/
â”‚   â”‚   â”œâ”€â”€ description.md
â”‚   â”‚   â””â”€â”€ README.md
â”‚   â”œâ”€â”€ fit-web/
â”‚   â”‚   â”œâ”€â”€ description.md
â”‚   â”‚   â””â”€â”€ README.md
â”‚   â””â”€â”€ fit-rag/
â”‚       â”œâ”€â”€ description.md
â”‚       â””â”€â”€ README.md
â”œâ”€â”€ stylesheets/                      â† Platform only, never authored
â”œâ”€â”€ Test Examples/                    â† Sandbox, scaffold only
â””â”€â”€ index.md
```

---

## PART 2: OBSIDIAN VAULT STRUCTURE

Location: `D:\Vaults\FIT-Vault\`

`02-DRAFTS/` mirrors `fit-docs/docs/` exactly. Every other folder serves authoring and operations.

```
D:\Vaults\FIT-Vault\
â”‚
â”œâ”€â”€ 00-INBOX/
â”‚   â”œâ”€â”€ _quick-capture.md             â† Daily brain dump. Ideas, requests, voice notes.
â”‚   â””â”€â”€ _agent-drop/                  â† Agents write first drafts here for your review
â”‚
â”œâ”€â”€ 01-PLANNING/
â”‚   â”œâ”€â”€ ideas/
â”‚   â”œâ”€â”€ requests/
â”‚   â”‚   â”œâ”€â”€ sop-requests/
â”‚   â”‚   â”œâ”€â”€ kb-requests/
â”‚   â”‚   â”œâ”€â”€ procedure-requests/
â”‚   â”‚   â”œâ”€â”€ solution-requests/
â”‚   â”‚   â””â”€â”€ service-requests/
â”‚   â”œâ”€â”€ roadmap/
â”‚   â””â”€â”€ template-changes/
â”‚       â””â”€â”€ YYYY-MM-DD-changes.md
â”‚
â”œâ”€â”€ 02-DRAFTS/                        â† MIRRORS fit-docs/docs/ exactly
â”‚   â”œâ”€â”€ Blog/
â”‚   â”œâ”€â”€ Finance/
â”‚   â”œâ”€â”€ Knowledge-Base/
â”‚   â”œâ”€â”€ Operations/
â”‚   â”‚   â”œâ”€â”€ SOPs/                     â† DRAFT-sop-NN-title.md
â”‚   â”‚   â””â”€â”€ Procedures/               â† DRAFT-procedure-title.md
â”‚   â”œâ”€â”€ project/
â”‚   â”œâ”€â”€ Services/
â”‚   â”œâ”€â”€ Solutions/
â”‚   â”‚   â”œâ”€â”€ fit-docs/
â”‚   â”‚   â”œâ”€â”€ fit-web/
â”‚   â”‚   â”œâ”€â”€ fit-rag/
â”‚   â”‚   â””â”€â”€ _new-solution-template/
â”‚   â””â”€â”€ Test-Examples/
â”‚
â”œâ”€â”€ 03-REVIEW/
â”‚   â”œâ”€â”€ Operations/
â”‚   â”‚   â”œâ”€â”€ SOPs/
â”‚   â”‚   â””â”€â”€ Procedures/
â”‚   â”œâ”€â”€ Knowledge-Base/
â”‚   â”œâ”€â”€ Solutions/
â”‚   â”œâ”€â”€ Services/
â”‚   â””â”€â”€ Blog/
â”‚
â”œâ”€â”€ 04-OPERATIONS/
â”‚   â”œâ”€â”€ _ops-dashboard.md
â”‚   â”œâ”€â”€ _daily-briefing.md
â”‚   â”œâ”€â”€ _doc-health.md
â”‚   â”œâ”€â”€ _dependency-graph.md
â”‚   â””â”€â”€ decisions/
â”‚
â”œâ”€â”€ 05-KNOWLEDGE/
â”‚   â”œâ”€â”€ ai-tools/
â”‚   â”œâ”€â”€ prompts/
â”‚   â”œâ”€â”€ research/
â”‚   â””â”€â”€ lessons-learned/
â”‚
â”œâ”€â”€ 06-CLIENTS/
â”‚   â””â”€â”€ [client-name]/
â”‚       â”œâ”€â”€ overview.md
â”‚       â”œâ”€â”€ notes.md
â”‚       â””â”€â”€ comms/
â”‚
â”œâ”€â”€ 07-ARCHIVE/
â”‚   â”œâ”€â”€ promoted/
â”‚   â””â”€â”€ abandoned/
â”‚
â””â”€â”€ _SYSTEM/
    â”œâ”€â”€ agent-instructions.md         â† Rules every AI tool must follow (includes Part 0)
    â”œâ”€â”€ vault-map.md
    â”œâ”€â”€ naming-conventions.md
    â”œâ”€â”€ tag-taxonomy.md
    â”œâ”€â”€ changelog.md
    â”œâ”€â”€ logs/
    â”‚   â””â”€â”€ audit-log.md              â† Append-only promote/rollback log
    â”œâ”€â”€ templates/
    â”‚   â”œâ”€â”€ sop-draft.md
    â”‚   â”œâ”€â”€ procedure-draft.md
    â”‚   â”œâ”€â”€ kb-article-draft.md
    â”‚   â”œâ”€â”€ solution-description.md
    â”‚   â”œâ”€â”€ solution-readme.md
    â”‚   â”œâ”€â”€ service-page.md
    â”‚   â””â”€â”€ doc-request.md
    â””â”€â”€ scripts/
        â”œâ”€â”€ promote.py
        â”œâ”€â”€ airtable_sync.py
        â”œâ”€â”€ rollback.py
        â”œâ”€â”€ health.py
        â”œâ”€â”€ dep-graph.py
        â””â”€â”€ template-diff.py
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

### fit-docs Published Files (built by promote script â€” never manual)
```
ðŸ“š SOP 21 â€” AWS S3 Backup Configuration.md
ðŸ“‹ PROC â€” Deploy â€” MkDocs to Production.md
ðŸ“˜ KB â€” What Is FIT RAG.md
```

### Never Use
- Spaces in filenames
- `temp`, `misc`, `notes`, `untitled`
- Dates buried in the middle: `sop-2025-aws.md` â† wrong

---

## PART 4: FRONTMATTER SCHEMA

> **Universal Base Only.** These fields apply to all doc types.
> Library-specific fields are defined in each library's README.
> If a README defines a field differently than this table â€” the README wins.

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
references: []
# Publish gate â€” all relevant fields must be true before promote script runs
gate_has_owner: false
gate_metadata_complete: false
gate_heading_structure_valid: false
gate_reviewed_by_human: false
gate_no_internal_refs: false    # PUBLIC_WEB / Dual only
gate_no_invented_slas: false    # PUBLIC_WEB / Dual only
---
```

### Extended: SOP (defined by SOP README â€” these extend the base)
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

## PART 5.5: SYSTEM SAFETY & OBSERVABILITY

> This phase adds operational safety controls and observability on top of the existing pipeline.
> It does not change folder taxonomy or core publish gates.

### Feature 1: Audit Trail Log

- Append-only file: `_SYSTEM/logs/audit-log.md`
- Entry format: `[TIMESTAMP] [ACTION] [SOURCE_FILE] [TARGET_FILE] [GIT_COMMIT_HASH]`
- Timestamp standard: UTC ISO-8601 (`YYYY-MM-DDTHH:MM:SSZ`)
- Allowed actions:
  - `PROMOTE_SUCCESS`
  - `ROLLBACK_SUCCESS`
  - `ROLLBACK_DRY_RUN`

#### Promote extension snippet (append on successful commit only)

```python
from datetime import datetime, timezone
from pathlib import Path

AUDIT_LOG = VAULT_ROOT / "_SYSTEM" / "logs" / "audit-log.md"


def append_audit_entry(action: str, source_file: str, target_file: str, commit_hash: str) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] [{action}] [{source_file}] [{target_file}] [{commit_hash}]\n"
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(line)
```

---

### Feature 2: Rollback Script

- Script path: `_SYSTEM/scripts/rollback.py`
- CLI:
  - `python rollback.py <published_filename>`
  - `python rollback.py <published_filename> --dry-run`

```python
# _SYSTEM/scripts/rollback.py

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

VAULT_ROOT = Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault"))
FIT_DOCS_ROOT = Path(os.getenv("FIT_DOCS_ROOT", r"D:\Dev\fit-docs\docs"))
AUDIT_LOG = VAULT_ROOT / "_SYSTEM" / "logs" / "audit-log.md"


def parse_log_line(line: str) -> dict[str, str] | None:
    m = re.match(r"^\[(.+?)\] \[(.+?)\] \[(.+?)\] \[(.+?)\] \[(.+?)\]$", line.strip())
    if not m:
        return None
    return {
        "timestamp": m.group(1),
        "action": m.group(2),
        "source": m.group(3),
        "target": m.group(4),
        "commit": m.group(5),
    }


def append_audit(action: str, source: str, target: str, commit_hash: str) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{ts}] [{action}] [{source}] [{target}] [{commit_hash}]\n")


def find_last_promote_entry(published_filename: str) -> dict[str, str]:
    if not AUDIT_LOG.exists():
        raise ValueError(f"Audit log not found: {AUDIT_LOG}")

    entries: list[dict[str, str]] = []
    for line in AUDIT_LOG.read_text(encoding="utf-8").splitlines():
        parsed = parse_log_line(line)
        if parsed and parsed["action"] == "PROMOTE_SUCCESS":
            entries.append(parsed)

    for entry in reversed(entries):
        if Path(entry["target"]).name == published_filename:
            return entry

    raise ValueError(f"No promote audit entry found for '{published_filename}'")


def restore_draft_from_archive(archive_name: str, draft_rel: str, dry_run: bool) -> Path:
    archive_path = VAULT_ROOT / "07-ARCHIVE" / "promoted" / archive_name
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    draft_path = VAULT_ROOT / draft_rel
    if dry_run:
        return draft_path

    draft_path.parent.mkdir(parents=True, exist_ok=True)
    text = archive_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            body = parts[2]
            fm["status"] = "promote-ready"
            fm["rollback_date"] = str(date.today())
            updated = "---\n" + yaml.dump(fm, allow_unicode=True) + "---\n" + body.lstrip()
            draft_path.write_text(updated, encoding="utf-8")
            return draft_path

    draft_path.write_text(text, encoding="utf-8")
    return draft_path


def rollback(published_filename: str, dry_run: bool = False) -> None:
    entry = find_last_promote_entry(published_filename)
    target_path = Path(entry["target"])

    if not target_path.exists() and not dry_run:
        raise FileNotFoundError(f"Target file not found: {target_path}")

    source_rel = entry["source"].replace("\\", "/")
    archive_name = Path(source_rel).name
    git_root = FIT_DOCS_ROOT.parent

    if dry_run:
        print("[dry-run] rollback plan")
        print(f"  source from audit: {entry['source']}")
        print(f"  target file: {target_path}")
        print("  steps: delete target -> mkdocs build --strict -> git rm/commit -> restore archive -> append audit")
        append_audit("ROLLBACK_DRY_RUN", entry["source"], str(target_path), "dry-run")
        return

    # 1-2. Validate target and delete
    if not target_path.exists():
        raise FileNotFoundError(f"Target file not found: {target_path}")
    target_path.unlink()

    # 3. Validate docs build after deletion
    build_ok = True
    try:
        subprocess.run(["mkdocs", "build", "--strict"], cwd=git_root, check=True)
    except subprocess.CalledProcessError:
        build_ok = False
        print("WARNING: mkdocs build --strict failed after deletion. Continuing rollback.", file=sys.stderr)

    # 4. git rm + commit
    subprocess.run(["git", "rm", str(target_path)], cwd=git_root, check=False)
    subprocess.run(["git", "commit", "-m", f"docs: rollback {published_filename}"], cwd=git_root, check=True)
    commit_hash = (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=git_root)
        .decode("utf-8")
        .strip()
    )

    # 5-6. Restore archive and reset frontmatter
    restored = restore_draft_from_archive(archive_name=archive_name, draft_rel=source_rel, dry_run=False)

    # 7. Audit log entry
    append_audit("ROLLBACK_SUCCESS", str(restored), str(target_path), commit_hash)

    if build_ok:
        print("✅ Rollback complete.")
    else:
        print("✅ Rollback complete (with mkdocs warning).")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Rollback a promoted fit-docs file")
    p.add_argument("published_filename", help="Published filename in fit-docs")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    try:
        rollback(args.published_filename, dry_run=args.dry_run)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
```

---

### Feature 3: Doc Health Dashboard

- Script path: `_SYSTEM/scripts/health.py`
- CLI:
  - `python health.py`
  - `python health.py --dry-run`
- Output report: `04-OPERATIONS/_doc-health.md`

```python
# _SYSTEM/scripts/health.py

from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

VAULT_ROOT = Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault"))
REPORT_PATH = VAULT_ROOT / "04-OPERATIONS" / "_doc-health.md"
REQUIRED_FIELDS = ["title", "status", "owner", "updated"]
REVIEW_OK = {"review", "promote-ready"}


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]


def stale_days(updated_value: str) -> int | None:
    try:
        updated = date.fromisoformat(str(updated_value)[:10])
    except Exception:
        return None
    return (date.today() - updated).days


def scan() -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    for rel_root in ["02-DRAFTS", "03-REVIEW"]:
        root = VAULT_ROOT / rel_root
        if not root.exists():
            continue

        for path in sorted(root.rglob("*.md")):
            rel = path.relative_to(VAULT_ROOT).as_posix()
            fm, _ = load_frontmatter(path)
            status = str(fm.get("status", "")).strip()

            missing = [f for f in REQUIRED_FIELDS if not str(fm.get(f, "")).strip()]
            if missing:
                findings.append({
                    "file": rel,
                    "issue": "missing_required_fields",
                    "detail": ", ".join(missing),
                })

            if rel_root == "02-DRAFTS" and status == "promoted":
                findings.append({
                    "file": rel,
                    "issue": "invalid_status_for_folder",
                    "detail": "02-DRAFTS contains status=promoted",
                })

            if rel_root == "03-REVIEW" and (status == "promoted" or status not in REVIEW_OK):
                findings.append({
                    "file": rel,
                    "issue": "invalid_status_for_folder",
                    "detail": "03-REVIEW must be review/promote-ready and never promoted",
                })

            days = stale_days(fm.get("updated", ""))
            if days is not None and days > 180:
                findings.append({
                    "file": rel,
                    "issue": "stale_doc",
                    "detail": f"updated {days} days ago",
                })

    return findings


def render(findings: list[dict[str, str]]) -> str:
    lines = [
        "# Doc Health Dashboard",
        "",
        f"Generated: {date.today()}",
        "",
        "## Summary",
    ]

    by_type: dict[str, int] = {}
    for row in findings:
        by_type[row["issue"]] = by_type.get(row["issue"], 0) + 1

    if by_type:
        for key in sorted(by_type):
            lines.append(f"- {key}: {by_type[key]}")
    else:
        lines.append("- no issues found")

    lines.extend([
        "",
        "## Findings",
        "| File | Issue | Detail |",
        "|---|---|---|",
    ])

    if findings:
        for row in findings:
            lines.append(f"| {row['file']} | {row['issue']} | {row['detail']} |")
    else:
        lines.append("| - | - | Clean |")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build document health dashboard")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    findings = scan()
    output = render(findings)

    if args.dry_run:
        print(output)
        return

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(output, encoding="utf-8")
    print(f"Wrote: {REPORT_PATH}")


if __name__ == "__main__":
    main()
```

---

### Feature 4: Doc Dependency Graph

- Script path: `_SYSTEM/scripts/dep-graph.py`
- CLI: `python dep-graph.py`
- Output path (fixed): `04-OPERATIONS/_dependency-graph.md`

```python
# _SYSTEM/scripts/dep-graph.py

from __future__ import annotations

import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

VAULT_ROOT = Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault"))
DRAFT_ROOT = VAULT_ROOT / "02-DRAFTS"
OUT_PATH = VAULT_ROOT / "04-OPERATIONS" / "_dependency-graph.md"
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def slug(node: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", node).strip("_") or "node"


def build_edges() -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []

    for path in sorted(DRAFT_ROOT.rglob("*.md")):
        rel = path.relative_to(VAULT_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")

        for m in WIKILINK_RE.finditer(text):
            target = m.group(1).strip()
            if target:
                edges.append((rel, target, "wikilink"))

        fm = load_frontmatter(path)
        refs = fm.get("references", [])
        if isinstance(refs, list):
            for item in refs:
                target = str(item).strip()
                if target:
                    edges.append((rel, target, "frontmatter.references"))

    return edges


def render(edges: list[tuple[str, str, str]]) -> str:
    lines = [
        "# Draft Dependency Graph",
        "",
        "```mermaid",
        "graph TD",
    ]

    seen: set[tuple[str, str, str]] = set()
    for src, dst, label in edges:
        key = (src, dst, label)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"  {slug(src)}[\"{src}\"] -->|{label}| {slug(dst)}[\"{dst}\"]")

    lines.extend([
        "```",
        "",
        "## Edge Table",
        "| Source | Target | Type |",
        "|---|---|---|",
    ])

    if seen:
        for src, dst, label in sorted(seen):
            lines.append(f"| {src} | {dst} | {label} |")
    else:
        lines.append("| - | - | no edges found |")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    edges = build_edges()
    output = render(edges)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(output, encoding="utf-8")
    print(f"Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
```

---

### Feature 5: Template Auto-Update Alerter

- Script path: `_SYSTEM/scripts/template-diff.py`
- CLI:
  - `python template-diff.py`
  - `python template-diff.py --date 2026-02-28`
- Output path: `01-PLANNING/template-changes/YYYY-MM-DD-changes.md`

```python
# _SYSTEM/scripts/template-diff.py

from __future__ import annotations

import argparse
import os
import re
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

VAULT_ROOT = Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault"))
TEMPLATES_ROOT = VAULT_ROOT / "_SYSTEM" / "templates"
DRAFTS_ROOT = VAULT_ROOT / "02-DRAFTS"
OUT_ROOT = VAULT_ROOT / "01-PLANNING" / "template-changes"
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

MATCH_RULES = {
    "sop-draft.md": "DRAFT-sop-*.md",
    "procedure-draft.md": "DRAFT-procedure-*.md",
    "kb-article-draft.md": "DRAFT-kb-*.md",
}


def h2_sections(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [m.group(1).strip() for m in H2_RE.finditer(text)]


def compare_sections(template_sections: list[str], doc_sections: list[str]) -> tuple[list[str], list[str]]:
    missing = [s for s in template_sections if s not in doc_sections]
    extra = [s for s in doc_sections if s not in template_sections]
    return missing, extra


def run_diff() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for tpl_name, glob_pat in MATCH_RULES.items():
        tpl_path = TEMPLATES_ROOT / tpl_name
        if not tpl_path.exists():
            continue

        tpl_sections = h2_sections(tpl_path)
        for draft in sorted(DRAFTS_ROOT.rglob(glob_pat)):
            doc_sections = h2_sections(draft)
            missing, extra = compare_sections(tpl_sections, doc_sections)
            if missing or extra:
                rows.append(
                    {
                        "template": tpl_name,
                        "draft": draft.relative_to(VAULT_ROOT).as_posix(),
                        "missing_h2": "; ".join(missing) if missing else "-",
                        "extra_h2": "; ".join(extra) if extra else "-",
                    }
                )

    return rows


def render(rows: list[dict[str, str]], run_date: str) -> str:
    lines = [
        f"# Template Change Report - {run_date}",
        "",
        "Structural differences between templates and matching drafts (H2 headings only).",
        "",
        "| Template | Draft | Missing H2 | Extra H2 |",
        "|---|---|---|---|",
    ]

    if rows:
        for r in rows:
            lines.append(f"| {r['template']} | {r['draft']} | {r['missing_h2']} | {r['extra_h2']} |")
    else:
        lines.append("| - | - | no differences found | - |")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="Template structural diff alerter")
    p.add_argument("--date", dest="run_date", default=str(date.today()))
    args = p.parse_args()

    rows = run_diff()
    output = render(rows, args.run_date)

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    out_path = OUT_ROOT / f"{args.run_date}-changes.md"
    out_path.write_text(output, encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
```

---

### Validation / Test Scenarios (Phase 5.5)

1. Audit log
   - Promote success appends one correctly formatted line.
   - Promote dry-run does not append.
2. Rollback
   - Finds last matching target entry from audit log.
   - Dry-run prints resolved commit/archive/target actions only.
   - Non-dry run performs delete + strict build + git commit + draft restore + log append.
3. Health
   - Flags promoted docs still in `02-DRAFTS`.
   - Flags stale docs over 180 days.
   - Flags missing required fields.
   - Generates markdown report with deterministic columns.
4. Dependency graph
   - Parses wikilinks correctly.
   - Produces valid Mermaid block and writes fixed path in `04-OPERATIONS`.
5. Template diff
   - Detects H2 section drift.
   - Writes dated report file in `01-PLANNING/template-changes/`.
   - Never modifies drafts/templates.

### Implementation Notes

- Keep these additions as a safety layer only; do not change existing core workflow semantics beyond the promote sequence correction below.
- Keep timestamps UTC in audit entries for deterministic parsing.

---

## PART 6: THE PROMOTE SCRIPT

> Full source: `_SYSTEM/scripts/promote.py`
> This script is also maintained in the `fit-docs-forge` repo as the canonical version.

### Canonical Promote Sequence (v3.5 Corrected)

1. Validate gate/frontmatter status and required checks.
2. Copy draft body to the target file in `fit-docs/docs/...`.
3. Run `mkdocs build --strict`.
   - If build fails: remove copied file, print error, exit non-zero, do not commit.
4. Run `git add` + `git commit` only after strict build passes.
5. Archive draft into `07-ARCHIVE/promoted/`.
6. Update draft frontmatter status to `promoted`.
7. Append audit entry to `_SYSTEM/logs/audit-log.md`.

```python
# _SYSTEM/scripts/promote.py
# Validates gate, routes file to correct fit-docs folder,
# builds compliant filename, strips Obsidian frontmatter,
# runs strict build validation, commits to Git, archives, updates draft, appends audit log.

from __future__ import annotations

import argparse
import io
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

VAULT_ROOT = Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault"))
FIT_DOCS_ROOT = Path(os.getenv("FIT_DOCS_ROOT", r"D:\Dev\fit-docs\docs"))
AUDIT_LOG = VAULT_ROOT / "_SYSTEM" / "logs" / "audit-log.md"

DRAFT_TO_DOCS = {
    "Blog": "blog/posts",
    "Finance": "Finance",
    "Knowledge-Base": "Knowledge Base",
    "Operations/SOPs": "Operations/SOPs",
    "Operations/Procedures": "Operations/Procedures",
    "project": "project",
    "Services": "Services",
    "Solutions": "Solutions",
    "Test-Examples": "Test Examples",
}

TYPE_TO_EMOJI = {
    "sop": "📚",
    "procedure": "📋",
    "kb-article": "📘",
    "solution": None,
    "service": None,
    "blog": None,
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


def append_audit_entry(action: str, source_file: str, target_file: str, commit_hash: str) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{ts}] [{action}] [{source_file}] [{target_file}] [{commit_hash}]\\n")


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]


def check_gate(fm: dict) -> list[str]:
    failures = [f for f in GATE_FIELDS if not fm.get(f, False)]
    if fm.get("kb_target") in ("PUBLIC_WEB", "Dual"):
        failures += [f for f in PUBLIC_GATE_FIELDS if not fm.get(f, False)]
    return failures


def resolve_target_folder(draft_rel_path: str, fit_docs_root: Path = FIT_DOCS_ROOT) -> Path:
    rel = draft_rel_path.replace("\\", "/")
    if rel.startswith("02-DRAFTS/"):
        rel = rel[len("02-DRAFTS/"):]

    for draft_prefix, docs_folder in sorted(DRAFT_TO_DOCS.items(), key=lambda x: -len(x[0])):
        if rel.startswith(draft_prefix + "/"):
            return fit_docs_root / docs_folder

    raise ValueError(f"Cannot resolve target folder for '{draft_rel_path}'")


def build_filename(fm: dict, original_name: str) -> str:
    doc_type = fm.get("type", "")
    emoji = TYPE_TO_EMOJI.get(doc_type)
    if emoji is None:
        return original_name.replace("DRAFT-", "")

    title = fm.get("title", "untitled").strip()
    if doc_type == "sop":
        num = str(fm.get("sop_number", "XX")).zfill(2)
        return f"{emoji} SOP {num} — {title}.md"
    if doc_type == "procedure":
        system = fm.get("system", "").strip()
        if system:
            return f"{emoji} PROC — {system} — {title}.md"
        return f"{emoji} PROC — {title}.md"
    if doc_type == "kb-article":
        return f"{emoji} KB — {title}.md"
    return f"{emoji} {title}.md"


def update_last_updated(body: str) -> str:
    today = date.today().strftime("%Y-%m-%d")
    return re.sub(r"(\\|\\s*Last Updated\\s*\\|\\s*)[^\\|]+(\\|)", rf"\\g<1>{today} \\2", body)


def promote(draft_rel_path: str, dry_run: bool = False) -> dict[str, str]:
    draft_path = VAULT_ROOT / draft_rel_path
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft not found: {draft_path}")

    fm, body = load_frontmatter(draft_path)

    if fm.get("status") != "promote-ready":
        raise ValueError(f"Status is '{fm.get('status')}' -- must be 'promote-ready'")

    failures = check_gate(fm)
    if failures:
        raise ValueError("Gate check failed:\\n" + "\\n".join(f"  - {f}: must be true" for f in failures))

    target_folder = resolve_target_folder(draft_rel_path)
    target_folder.mkdir(parents=True, exist_ok=True)

    filename = build_filename(fm, draft_path.name)
    target_path = target_folder / filename
    body = update_last_updated(body)

    if dry_run:
        return {"target": str(target_path), "archive": "", "filename": filename}

    # 1-2. Copy content to fit-docs target
    target_path.write_text(body.lstrip(), encoding="utf-8")

    # 3. Strict build validation before commit
    git_root = FIT_DOCS_ROOT.parent
    try:
        subprocess.run(["mkdocs", "build", "--strict"], cwd=git_root, check=True)
    except subprocess.CalledProcessError as exc:
        if target_path.exists():
            target_path.unlink()
        raise RuntimeError("mkdocs build --strict failed; promotion aborted with no commit") from exc

    # 4. Git commit only after strict build pass
    subprocess.run(["git", "add", str(target_path)], cwd=git_root, check=True)
    subprocess.run(["git", "commit", "-m", f"docs: promote {filename}"], cwd=git_root, check=True)
    commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=git_root).decode("utf-8").strip()

    # 5. Archive draft
    archive = VAULT_ROOT / "07-ARCHIVE" / "promoted" / draft_path.name
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(draft_path, archive)

    # 6. Update draft status
    draft_path.write_text(
        "---\\n" + yaml.dump({**fm, "status": "promoted", "updated": str(date.today())}, allow_unicode=True) + "---\\n" + body,
        encoding="utf-8",
    )

    # 7. Append audit entry
    append_audit_entry("PROMOTE_SUCCESS", draft_rel_path, str(target_path), commit_hash)

    return {"target": str(target_path), "archive": str(archive), "filename": filename}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Promote a vault draft into fit-docs")
    parser.add_argument("draft", help="Vault-relative path to draft file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        result = promote(args.draft, dry_run=args.dry_run)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"[dry-run] Would promote to: {result['target']}")
        print(f"[dry-run] Published filename: {result['filename']}")
    else:
        print(f"Promoted -> {result['target']}")
        print(f"Archived -> {result['archive']}")
```

---

## PART 7: THE AUTHORING WORKFLOW

### Status Flow (Every Draft)
```
captured â†’ draft â†’ review â†’ promote-ready â†’ [script] â†’ promoted
    â†‘ Plan       â†‘ Implement             â†‘ Validate    â†‘ Publish
```

### For a New SOP
```
1. CAPTURE   â†’ 00-INBOX/_quick-capture.md

2. DRAFT     â†’ Agent reads SOP README â†’ drafts using sop-draft.md template
               Save to: 02-DRAFTS/Operations/SOPs/DRAFT-sop-21-title.md

3. ELABORATE â†’ You edit in Obsidian

4. GATE      â†’ Flip frontmatter: status: promote-ready, gate_*: true

5. PROMOTE   â†’ python promote.py "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-..."
               â†’ Lands in fit-docs/docs/Operations/SOPs/ðŸ“š SOP 21 â€” Title.md
               â†’ mkdocs build --strict validates â†’ Git committed
```

### For a New Solution
```
1. CAPTURE   â†’ 01-PLANNING/requests/solution-requests/
2. DRAFT x2  â†’ description.md + README.md in 02-DRAFTS/Solutions/fit-newproduct/
3. GATE      â†’ Both files need gate fields true
4. PROMOTE   â†’ Run script twice â€” one call per file
```

### Agent System Prompt (Universal)
```
You are a documentation agent for FIT Automate.

CRITICAL â€” Before touching any file in a library folder:
1. Read that folder's README.md (the ðŸ‘® file at the folder root)
2. Extract naming convention, metadata table fields, required sections, content rules
3. Apply only what the README defines â€” nothing invented, nothing from memory
4. If README and master YAML conflict â€” README wins

Context: [paste _SYSTEM/vault-map.md]
Rules:
- Do NOT invent SLAs, prices, or numbers unless explicitly provided
- Set all gate_ fields to false, status to draft
- For PUBLIC_WEB docs: no internal tool names, no internal process references
- Output the complete markdown file only â€” no commentary, no preamble

Request: [paste capture note]
```

---

## PART 8: DAILY BRIEFING PIPELINE

```
07:00 daily (Windows Task Scheduler)
  â†“  airtable_sync.py
     â†’ Pulls overdue + due-today from Airtable
     â†’ Overwrites 04-OPERATIONS/_ops-dashboard.md

  â†“  fit-briefing-agent.py  (Phase 4 â€” build after promote script proven)
     â†’ Reads _ops-dashboard.md
     â†’ Reads 02-DRAFTS/ file count per folder
     â†’ Reads _SYSTEM/changelog.md (last 7 days)
     â†’ Writes fit-docs/docs/blog/posts/YYYY-MM-DD-daily-snapshot.md

  â†“  mkdocs_hooks.py (already built)
     â†’ Extracts Next Steps + Highlights
     â†’ Injects Daily Snapshot into docs/home/index.md
```

---

## PART 9: PLUGIN STACK

**Tier 1 â€” Day 1 (Core)**
| Plugin | Why |
|---|---|
| Dataview | Query vault like a database |
| Templater | Template engine with date logic |
| Tasks | Task tracking with due dates |

**Tier 2 â€” Week 1 (Workflow)**
| Plugin | Why |
|---|---|
| QuickAdd | Rapid capture to correct location |
| Shell Commands | Run promote script from inside Obsidian |
| Commander | Toolbar buttons for promote, sync, capture |

**Tier 3 â€” Month 2 (Automation)**
| Plugin | Why |
|---|---|
| Local REST API | Vault at localhost:27123 â€” agent gateway |
| Obsidian-Git | Auto-commit vault on schedule |
| Kanban | Visual board for draft pipeline status |

---

## PART 10: PHASED ROLLOUT

### Phase 1 â€” fit-docs-forge Repo (Week 1) âœ…
> Build the agent system first. Everything else runs on top of it.
- [x] Create `fit-docs-forge` repo from PIV bootstrap
- [x] Run PIV loop: `.ai/` scaffolding + CI passes
- [x] Seed `FIT-Automate-Master-Blueprint-v3.md` as the plan
- [x] Agent reads blueprint â†’ proposes Phase 2 PRs
- [x] **Milestone:** PIV loop is live. Agent can read the plan and propose work.

### Phase 2 â€” Vault Foundation (Days 3-5)
- [x] Create `D:\Vaults\FIT-Vault\` with full folder structure (Part 2)
- [x] Create all 5 templates in `_SYSTEM/templates/` (Part 5 defines 5; 2 more TBD)
- [x] Create `_SYSTEM/agent-instructions.md` (embed Part 0 README-as-schema rule)
- [x] Create `_SYSTEM/vault-map.md`
- [ ] Install Obsidian â†’ open FIT-Vault
- [ ] Install Tier 1 plugins
- [ ] **Milestone:** You can draft and organize content in Obsidian

### Phase 3 â€” Promote Script (Days 5-7) âœ…
- [x] `pip install pyyaml`
- [x] Save `promote.py` to `_SYSTEM/scripts/` (scaffold copies automatically)
- [x] Update `FIT_DOCS_ROOT` to your actual fit-docs path (via .env)
- [x] Test on a throwaway draft â€” confirm file lands correctly
- [x] Confirm `mkdocs build --strict` passes after promote
- [x] Install Shell Commands plugin â†’ wire promote as a hotkey
- [x] **Milestone:** One command ships a doc from Obsidian to fit-docs

### Phase 4 â€” Next.js Preview UI (Week 2)
> The fit-docs-forge `/app` directory. Preview rendered MD without opening Typora.
- [x] Scaffold Next.js app in `fit-docs-forge/app/`
- [x] Wire to vault path â€” reads `02-DRAFTS/` and `03-REVIEW/` folders
- [x] Render MD files with frontmatter panel (shows gate status)
- [x] Approve button -> triggers promote script via Python API
- [x] **Milestone:** Review and approve docs from browser. No Typora needed.

### Phase 5 â€” Airtable Bridge (Week 2-3)
- [ ] Get Airtable API key + Base/Table IDs
- [x] Build `airtable_sync.py`
- [x] Windows Task Scheduler: every 60 minutes
- [x] **Milestone:** Airtable tasks visible in Obsidian automatically

### Phase 5.5 â€” System Safety & Observability
| Phase | Feature | Est. Time | Dependencies |
|---|---|---:|---|
| Phase 5.5.1 | Audit Trail Log | 1 day | promote.py working (done) |
| Phase 5.5.2 | Rollback Script | 1 day | Audit Trail |
| Phase 5.5.3 | Doc Health Dashboard | 2 days | None |
| Phase 5.5.4 | Doc Dependency Graph | 2 days | Dataview plugin installed |
| Phase 5.5.5 | Template Auto-Update Alerter | 2 days | None |

### Phase 6 â€” Agent Automation (Month 2)
- [ ] Install Local REST API plugin
- [ ] Build `fit-briefing-agent.py`
- [ ] Agent scans `01-PLANNING/requests/` â†’ auto-drafts to `02-DRAFTS/`
- [ ] **Milestone:** Wake up to a daily briefing. Vault updates itself.

### Phase 7 â€” Folder Rewrite Command (Month 2-3)
- [ ] `fit-forge rewrite --folder <library>` command
- [ ] Agent reads README â†’ diffs all files â†’ rewrites non-conforming
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
python D:\Vaults\FIT-Vault\_SYSTEM\scripts\promote.py "02-DRAFTS/<path-to-draft>"
```

### What Belongs Where
| Content | Lives In | Never In |
|---|---|---|
| Published SOPs | fit-docs only | Obsidian |
| Draft SOPs | Obsidian `02-DRAFTS/` until promoted | fit-docs |
| Solution description.md | Obsidian draft â†’ promoted â†’ consumed by fit-web | Nowhere else |
| Prompt library | Obsidian `05-KNOWLEDGE/prompts/` | fit-docs |
| Agent rules | Obsidian `_SYSTEM/` + fit-docs-forge `.ai/` | Nowhere else |

---

*FIT Automate Internal | v3.5 | February 2025*
*Single source of truth. All previous drafts superseded.*




