"""Promote a vault draft into fit-docs with gate validation.

Validates frontmatter gate fields, builds a compliant filename with emoji
prefix, copies the body (stripping YAML frontmatter) into the correct
fit-docs folder, archives the original, and optionally commits to Git.

Based on blueprint Part 6.

Usage:
    python promote.py "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-onboarding.md"
    python promote.py --dry-run "02-DRAFTS/Knowledge-Base/DRAFT-kb-glossary.md"
"""

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
FIT_DOCS_ROOT = Path(os.getenv("FIT_DOCS_ROOT", r"D:\dev\github\fit-docs\docs"))

DRAFT_TO_DOCS: dict[str, str] = {
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

TYPE_TO_EMOJI: dict[str, str | None] = {
    "sop": "\U0001f4da",        # 📚
    "procedure": "\U0001f4cb",  # 📋
    "kb-article": "\U0001f4d8", # 📘
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

FAILURE_ACTION = "PROMOTE_FAILED"


def append_audit_entry(
    action: str,
    source_file: str,
    target_file: str,
    commit_hash: str,
    *,
    audit_log: Path,
) -> None:
    """Append one UTC audit entry to the vault audit log."""
    audit_log.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] [{action}] [{source_file}] [{target_file}] [{commit_hash}]\n"
    with audit_log.open("a", encoding="utf-8") as fh:
        fh.write(line)


def summarize_error(exc: Exception) -> str:
    """Return a compact one-line error summary suitable for audit logs."""
    text = str(exc).replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "error"
    return text[:160]


def append_failure_audit_entry(
    *,
    audit_log: Path,
    stage: str,
    draft_rel_path: str | None,
    target_path: Path | None,
    error: Exception,
) -> None:
    """Append a promote failure audit entry."""
    source_file = draft_rel_path or "-"
    target_file = str(target_path) if target_path is not None else "-"
    summary = summarize_error(error)
    detail = f"failed:{stage}:{summary}"
    append_audit_entry(FAILURE_ACTION, source_file, target_file, detail, audit_log=audit_log)


def load_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (metadata_dict, body_text)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]


def check_gate(fm: dict) -> list[str]:
    """Return list of gate fields that are not true."""
    failures = [f for f in GATE_FIELDS if not fm.get(f, False)]
    if fm.get("kb_target") in ("PUBLIC_WEB", "Dual"):
        failures += [f for f in PUBLIC_GATE_FIELDS if not fm.get(f, False)]
    return failures


def resolve_target_folder(draft_rel_path: str, fit_docs_root: Path = FIT_DOCS_ROOT) -> Path:
    """Map a vault-relative draft path to the correct fit-docs destination folder."""
    rel = draft_rel_path.replace("\\", "/")
    if rel.startswith("02-DRAFTS/"):
        rel = rel[len("02-DRAFTS/"):]

    for draft_prefix, docs_folder in sorted(DRAFT_TO_DOCS.items(), key=lambda x: -len(x[0])):
        if rel.startswith(draft_prefix + "/") or rel.startswith(draft_prefix + "\\"):
            return fit_docs_root / docs_folder

    raise ValueError(
        f"Cannot resolve target folder for '{draft_rel_path}'. "
        f"Expected path under 02-DRAFTS/ matching one of: {list(DRAFT_TO_DOCS.keys())}"
    )


def build_filename(fm: dict, original_name: str) -> str:
    """Build a compliant published filename with emoji prefix."""
    doc_type = fm.get("type", "")
    emoji = TYPE_TO_EMOJI.get(doc_type)
    if emoji is None:
        return original_name.replace("DRAFT-", "")

    title = fm.get("title", "untitled").strip()
    if doc_type == "sop":
        num = str(fm.get("sop_number", "XX")).zfill(2)
        return f"{emoji} SOP {num} \u2014 {title}.md"
    elif doc_type == "procedure":
        system = fm.get("system", "").strip()
        if system:
            return f"{emoji} PROC \u2014 {system} \u2014 {title}.md"
        return f"{emoji} PROC \u2014 {title}.md"
    elif doc_type == "kb-article":
        return f"{emoji} KB \u2014 {title}.md"
    return f"{emoji} {title}.md"


def update_last_updated(body: str) -> str:
    """Replace the Last Updated value in the markdown metadata table."""
    today = date.today().strftime("%Y-%m-%d")
    return re.sub(
        r"(\|\s*Last Updated\s*\|\s*)[^\|]+(\|)",
        rf"\g<1>{today} \2",
        body,
    )


def promote(
    draft_rel_path: str,
    *,
    vault_root: Path = VAULT_ROOT,
    fit_docs_root: Path = FIT_DOCS_ROOT,
    dry_run: bool = False,
    git_commit: bool = True,
) -> dict[str, str]:
    """Promote a draft. Returns dict with keys: target, archive, filename."""
    audit_log = vault_root / "_SYSTEM" / "logs" / "audit-log.md"
    stage = "validate_status"
    target_path: Path | None = None

    try:
        draft_path = vault_root / draft_rel_path
        if not draft_path.exists():
            raise FileNotFoundError(f"Draft not found: {draft_path}")

        fm, body = load_frontmatter(draft_path)

        if fm.get("status") != "promote-ready":
            raise ValueError(
                f"Status is '{fm.get('status')}' -- must be 'promote-ready'"
            )

        stage = "validate_gates"
        failures = check_gate(fm)
        if failures:
            raise ValueError(
                "Gate check failed:\n" + "\n".join(f"  - {f}: must be true" for f in failures)
            )

        stage = "resolve_target"
        target_folder = resolve_target_folder(draft_rel_path, fit_docs_root)
        if not dry_run:
            target_folder.mkdir(parents=True, exist_ok=True)

        filename = build_filename(fm, draft_path.name)
        target_path = target_folder / filename
        body = update_last_updated(body)

        if dry_run:
            return {"target": str(target_path), "archive": "", "filename": filename, "commit_result": "dry_run"}

        stage = "write_target"
        target_path.write_text(body.lstrip(), encoding="utf-8")
        git_root = fit_docs_root.parent
        stage = "mkdocs_strict"
        try:
            subprocess.run(["mkdocs", "build", "--strict"], cwd=git_root, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            target_path.unlink(missing_ok=True)
            raise RuntimeError("mkdocs build --strict failed; promotion aborted with no commit") from exc

        archive = vault_root / "07-ARCHIVE" / "promoted" / draft_path.name
        commit_hash = ""
        commit_result = "skipped"

        if git_commit:
            stage = "git_add"
            subprocess.run(["git", "add", str(target_path)], cwd=git_root, check=True)
            stage = "git_diff_cached"
            target_rel = target_path.relative_to(git_root).as_posix()
            diff_proc = subprocess.run(
                ["git", "diff", "--cached", "--quiet", "--", target_rel],
                cwd=git_root,
                check=False,
            )
            if diff_proc.returncode == 1:
                stage = "git_commit"
                subprocess.run(
                    ["git", "commit", "-m", f"docs: promote {filename}"],
                    cwd=git_root,
                    check=True,
                )
                commit_result = "committed"
            elif diff_proc.returncode == 0:
                commit_result = "no_changes"
            else:
                raise subprocess.CalledProcessError(diff_proc.returncode, diff_proc.args)

            commit_hash = (
                subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=git_root)
                .decode("utf-8")
                .strip()
            )

        stage = "post_publish_update"
        archive.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(draft_path, archive)

        draft_path.write_text(
            "---\n"
            + yaml.dump({**fm, "status": "promoted", "updated": str(date.today())}, allow_unicode=True)
            + f"---\n{body}",
            encoding="utf-8",
        )

        if git_commit:
            append_audit_entry(
                "PROMOTE_SUCCESS",
                draft_rel_path,
                str(target_path),
                commit_hash,
                audit_log=audit_log,
            )

        return {
            "target": str(target_path),
            "archive": str(archive),
            "filename": filename,
            "commit_result": commit_result,
        }

    except Exception as exc:
        # Dry-run without errors should never write audit. Failed runs are always auditable.
        try:
            append_failure_audit_entry(
                audit_log=audit_log,
                stage=stage,
                draft_rel_path=draft_rel_path,
                target_path=target_path,
                error=exc,
            )
        except Exception:
            pass
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote a vault draft into fit-docs")
    parser.add_argument("draft", help="Vault-relative path to the draft file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without writing")
    parser.add_argument("--no-commit", action="store_true", help="Skip the git add/commit step")
    parser.add_argument("--vault", type=Path, default=VAULT_ROOT)
    parser.add_argument("--fit-docs", type=Path, default=FIT_DOCS_ROOT)
    args = parser.parse_args()

    try:
        result = promote(
            args.draft,
            vault_root=args.vault,
            fit_docs_root=args.fit_docs,
            dry_run=args.dry_run,
            git_commit=not args.no_commit and not args.dry_run,
        )
    except (FileNotFoundError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"[dry-run] Would promote to: {result['target']}")
        print(f"[dry-run] Published filename: {result['filename']}")
    else:
        print(f"Promoted -> {result['target']}")
        print(f"Archived -> {result['archive']}")
        if not args.no_commit:
            if result.get("commit_result") == "no_changes":
                print("Git commit skipped: no publish diff (already up to date).")
            else:
                print(f"Git committed: docs: promote {result['filename']}")


if __name__ == "__main__":
    main()
