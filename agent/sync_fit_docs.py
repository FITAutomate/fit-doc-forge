"""Sync fit-docs/docs/ into the vault's _REFERENCE/fit-docs/ folder.

One-way mirror: published docs are copied into the vault so Obsidian
can index them for search, Dataview queries, and side-by-side reference
while drafting.  Files in _REFERENCE/ should never be edited directly.

Behaviour:
- New and updated files are copied (compared by mtime + size).
- Files deleted from fit-docs are removed from _REFERENCE/.
- A .gitkeep-style marker is written so the folder is never empty.

Usage:
    python sync_fit_docs.py                          # uses .env paths
    python sync_fit_docs.py --source D:\\Dev\\fit-docs\\docs --vault D:\\Vaults\\FIT-Vault
"""

from __future__ import annotations

import argparse
import io
import os
import shutil
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from dotenv import load_dotenv

load_dotenv()

IGNORE_PATTERNS = {".git", "__pycache__", ".obsidian", "node_modules", ".cache"}


def _should_ignore(path: Path) -> bool:
    return any(part in IGNORE_PATTERNS for part in path.parts)


def sync(source: Path, vault_root: Path) -> dict[str, list[str]]:
    """Mirror *source* into vault_root/_REFERENCE/fit-docs/. Return action log."""
    dest_root = vault_root / "_REFERENCE" / "fit-docs"
    dest_root.mkdir(parents=True, exist_ok=True)

    actions: dict[str, list[str]] = {"copied": [], "updated": [], "removed": []}

    source_rel_paths: set[Path] = set()
    for src_file in sorted(source.rglob("*")):
        if src_file.is_dir() or _should_ignore(src_file.relative_to(source)):
            continue
        rel = src_file.relative_to(source)
        source_rel_paths.add(rel)
        dest_file = dest_root / rel

        if not dest_file.exists():
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest_file)
            actions["copied"].append(str(rel))
        elif (
            src_file.stat().st_size != dest_file.stat().st_size
            or src_file.stat().st_mtime > dest_file.stat().st_mtime
        ):
            shutil.copy2(src_file, dest_file)
            actions["updated"].append(str(rel))

    for dest_file in sorted(dest_root.rglob("*")):
        if dest_file.is_dir():
            continue
        rel = dest_file.relative_to(dest_root)
        if rel not in source_rel_paths:
            dest_file.unlink()
            actions["removed"].append(str(rel))

    for dest_dir in sorted(dest_root.rglob("*"), reverse=True):
        if dest_dir.is_dir() and not any(dest_dir.iterdir()):
            dest_dir.rmdir()

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync fit-docs into vault _REFERENCE")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(os.getenv("FIT_DOCS_ROOT", r"D:\Dev\fit-docs\docs")),
        help="Path to fit-docs/docs/ (default: FIT_DOCS_ROOT from .env)",
    )
    parser.add_argument(
        "--vault",
        type=Path,
        default=Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault")),
        help="Path to vault root (default: VAULT_ROOT from .env)",
    )
    args = parser.parse_args()

    if not args.source.is_dir():
        print(f"ERROR: source not found: {args.source}", file=sys.stderr)
        sys.exit(1)

    print(f"Syncing: {args.source}")
    print(f"   Into: {args.vault / '_REFERENCE' / 'fit-docs'}")

    results = sync(args.source, args.vault)

    total = sum(len(v) for v in results.values())
    for action, files in results.items():
        for f in files:
            print(f"  {action}: {f}")

    if total:
        print(f"\nDone. {total} files processed.")
    else:
        print("Nothing to do -- _REFERENCE is up to date.")


if __name__ == "__main__":
    main()
