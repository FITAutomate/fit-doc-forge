"""Create the FIT-Vault Obsidian folder tree defined in blueprint Part 2.

Idempotent: directories are created with exist_ok=True and placeholder
files are only written when they don't already exist.  Templates are
copied from agent/vault_templates/ into _SYSTEM/templates/ only when
they don't already exist (so user edits are never overwritten).

Usage:
    python scaffold_vault.py                     # uses VAULT_ROOT from .env
    python scaffold_vault.py D:\\Vaults\\FIT-Vault  # explicit path
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DIRECTORIES = [
    "00-INBOX/_agent-drop",
    "01-PLANNING/ideas",
    "01-PLANNING/requests/sop-requests",
    "01-PLANNING/requests/kb-requests",
    "01-PLANNING/requests/procedure-requests",
    "01-PLANNING/requests/solution-requests",
    "01-PLANNING/requests/service-requests",
    "01-PLANNING/roadmap",
    "02-DRAFTS/Blog",
    "02-DRAFTS/Finance",
    "02-DRAFTS/Knowledge-Base",
    "02-DRAFTS/Operations/SOPs",
    "02-DRAFTS/Operations/Procedures",
    "02-DRAFTS/project",
    "02-DRAFTS/Services",
    "02-DRAFTS/Solutions/fit-docs",
    "02-DRAFTS/Solutions/fit-web",
    "02-DRAFTS/Solutions/fit-rag",
    "02-DRAFTS/Solutions/_new-solution-template",
    "02-DRAFTS/Test-Examples",
    "03-REVIEW/Operations/SOPs",
    "03-REVIEW/Operations/Procedures",
    "03-REVIEW/Knowledge-Base",
    "03-REVIEW/Solutions",
    "03-REVIEW/Services",
    "03-REVIEW/Blog",
    "04-OPERATIONS/decisions",
    "05-KNOWLEDGE/ai-tools",
    "05-KNOWLEDGE/prompts",
    "05-KNOWLEDGE/research",
    "05-KNOWLEDGE/lessons-learned",
    "06-CLIENTS",
    "07-ARCHIVE/promoted",
    "07-ARCHIVE/abandoned",
    "_REFERENCE/fit-docs",
    "_SYSTEM/templates",
    "_SYSTEM/scripts",
]

PLACEHOLDER_FILES: dict[str, str] = {
    "00-INBOX/_quick-capture.md": (
        "# Quick Capture\n\nDaily brain dump. Ideas, requests, voice notes.\n"
    ),
    "04-OPERATIONS/_ops-dashboard.md": (
        "# Ops Dashboard\n\nAirtable task mirror (populated by fit-airtable-sync).\n"
    ),
    "04-OPERATIONS/_daily-briefing.md": (
        "# Daily Briefing\n\nMorning priorities.\n"
    ),
    "_SYSTEM/changelog.md": (
        "# Vault Changelog\n\nWhat the agents did.\n"
    ),
}

TEMPLATES_DIR = Path(__file__).resolve().parent / "vault_templates"
SYSTEM_DOCS_DIR = Path(__file__).resolve().parent / "vault_system_docs"
SCRIPTS_DIR = Path(__file__).resolve().parent


def scaffold(vault_root: Path) -> list[str]:
    """Create the vault tree under *vault_root*. Return list of actions taken."""
    actions: list[str] = []

    for d in DIRECTORIES:
        target = vault_root / d
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            actions.append(f"mkdir {d}")

    for rel_path, content in PLACEHOLDER_FILES.items():
        target = vault_root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(content, encoding="utf-8")
            actions.append(f"write {rel_path}")

    if TEMPLATES_DIR.is_dir():
        dest_dir = vault_root / "_SYSTEM" / "templates"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted(TEMPLATES_DIR.glob("*.md")):
            dest = dest_dir / src.name
            if not dest.exists():
                shutil.copy2(src, dest)
                actions.append(f"template {src.name}")

    if SYSTEM_DOCS_DIR.is_dir():
        dest_dir = vault_root / "_SYSTEM"
        dest_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted(SYSTEM_DOCS_DIR.glob("*.md")):
            dest = dest_dir / src.name
            if not dest.exists():
                shutil.copy2(src, dest)
                actions.append(f"system-doc {src.name}")

    vault_scripts = ["promote.py", "sync_fit_docs.py"]
    scripts_dest = vault_root / "_SYSTEM" / "scripts"
    scripts_dest.mkdir(parents=True, exist_ok=True)
    for script_name in vault_scripts:
        src = SCRIPTS_DIR / script_name
        if src.exists():
            dest = scripts_dest / script_name
            if not dest.exists():
                shutil.copy2(src, dest)
                actions.append(f"script {script_name}")

    return actions


def main() -> None:
    if len(sys.argv) > 1:
        vault_root = Path(sys.argv[1])
    else:
        vault_root = Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault"))

    print(f"Scaffolding vault at: {vault_root}")
    actions = scaffold(vault_root)

    if actions:
        for a in actions:
            print(f"  + {a}")
        print(f"\nDone. {len(actions)} actions taken.")
    else:
        print("Nothing to do — vault already scaffolded.")


if __name__ == "__main__":
    main()
