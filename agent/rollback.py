"""Rollback a promoted fit-docs document using audit-log metadata.

Usage:
    python rollback.py "<published filename>"
    python rollback.py "<published filename>" --dry-run
"""

from __future__ import annotations

import argparse
import io
import os
import re
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
FIT_DOCS_ROOT = Path(os.getenv("FIT_DOCS_ROOT", r"D:\dev\github\fit-docs\docs"))
AUDIT_LOG = VAULT_ROOT / "_SYSTEM" / "logs" / "audit-log.md"

AUDIT_PATTERN = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\] "
    r"\[(?P<action>[^\]]+)\] "
    r"\[(?P<source>[^\]]+)\] "
    r"\[(?P<target>[^\]]+)\] "
    r"\[(?P<commit>[^\]]+)\]$"
)


def parse_log_line(line: str) -> dict[str, str] | None:
    """Parse one audit-log line into a dict, or return None if invalid."""
    match = AUDIT_PATTERN.match(line.strip())
    if not match:
        return None
    return match.groupdict()


def append_audit(action: str, source: str, target: str, commit_hash: str, *, audit_log: Path = AUDIT_LOG) -> None:
    """Append one UTC audit event."""
    audit_log.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] [{action}] [{source}] [{target}] [{commit_hash}]\n"
    with audit_log.open("a", encoding="utf-8") as fh:
        fh.write(line)


def find_last_promote_entry(published_filename: str, *, audit_log: Path = AUDIT_LOG) -> dict[str, str]:
    """Find the latest PROMOTE_SUCCESS entry for the published filename."""
    if not audit_log.exists():
        raise ValueError(f"Audit log not found: {audit_log}")

    entries: list[dict[str, str]] = []
    for line in audit_log.read_text(encoding="utf-8").splitlines():
        parsed = parse_log_line(line)
        if parsed and parsed["action"] == "PROMOTE_SUCCESS":
            entries.append(parsed)

    for entry in reversed(entries):
        if Path(entry["target"]).name == published_filename:
            return entry

    raise ValueError(f"No promote audit entry found for '{published_filename}'")


def restore_draft_from_archive(
    archive_name: str,
    draft_rel: str,
    *,
    vault_root: Path = VAULT_ROOT,
    dry_run: bool = False,
) -> Path:
    """Restore archived draft and reset frontmatter to promote-ready."""
    archive_path = vault_root / "07-ARCHIVE" / "promoted" / archive_name
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    draft_path = vault_root / draft_rel
    if dry_run:
        return draft_path

    draft_path.parent.mkdir(parents=True, exist_ok=True)
    text = archive_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            fm["status"] = "promote-ready"
            fm["updated"] = str(date.today())
            text = "---\n" + yaml.dump(fm, allow_unicode=True) + "---\n" + parts[2].lstrip("\n")

    draft_path.write_text(text, encoding="utf-8")
    return draft_path


def rollback(
    published_filename: str,
    *,
    vault_root: Path = VAULT_ROOT,
    fit_docs_root: Path = FIT_DOCS_ROOT,
    dry_run: bool = False,
) -> None:
    """Rollback one promoted published file and restore the archived draft."""
    audit_log = vault_root / "_SYSTEM" / "logs" / "audit-log.md"
    entry = find_last_promote_entry(published_filename, audit_log=audit_log)
    source_rel = entry["source"]
    target_path = Path(entry["target"])
    archive_name = Path(source_rel).name

    if dry_run:
        print("[dry-run] rollback plan")
        print(f"  source from audit: {entry['source']}")
        print(f"  target file: {target_path}")
        print("  steps: delete target -> mkdocs build --strict -> git rm/commit -> restore archive -> append audit")
        append_audit("ROLLBACK_DRY_RUN", entry["source"], str(target_path), "dry-run", audit_log=audit_log)
        return

    # Remove target first so strict build validates the post-rollback tree.
    target_path.unlink(missing_ok=True)

    git_root = fit_docs_root.parent
    build_ok = True
    try:
        subprocess.run(["mkdocs", "build", "--strict"], cwd=git_root, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        build_ok = False
        print("WARNING: mkdocs build --strict failed after deletion. Continuing rollback.", file=sys.stderr)

    subprocess.run(["git", "rm", str(target_path)], cwd=git_root, check=False)
    subprocess.run(["git", "commit", "-m", f"docs: rollback {published_filename}"], cwd=git_root, check=True)
    commit_hash = (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=git_root)
        .decode("utf-8")
        .strip()
    )

    restored = restore_draft_from_archive(
        archive_name=archive_name,
        draft_rel=source_rel,
        vault_root=vault_root,
        dry_run=False,
    )
    append_audit("ROLLBACK_SUCCESS", str(restored), str(target_path), commit_hash, audit_log=audit_log)

    if build_ok:
        print("[done] Rollback complete.")
    else:
        print("[done] Rollback complete (with mkdocs warning).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rollback a promoted fit-docs file")
    parser.add_argument("published_filename", help="Published filename in fit-docs")
    parser.add_argument("--dry-run", action="store_true", help="Preview rollback actions only")
    parser.add_argument("--vault", type=Path, default=VAULT_ROOT)
    parser.add_argument("--fit-docs", type=Path, default=FIT_DOCS_ROOT)
    args = parser.parse_args()

    try:
        rollback(
            args.published_filename,
            vault_root=args.vault,
            fit_docs_root=args.fit_docs,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
