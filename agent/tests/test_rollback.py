from pathlib import Path
import subprocess

import pytest
import yaml

from rollback import (
    append_audit,
    find_last_promote_entry,
    parse_log_line,
    restore_draft_from_archive,
    rollback,
)


def _write_archive(vault: Path, archive_name: str, fm: dict, body: str = "# Body\n") -> Path:
    path = vault / "07-ARCHIVE" / "promoted" / archive_name
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "---\n" + yaml.dump(fm, allow_unicode=True) + f"---\n{body}"
    path.write_text(content, encoding="utf-8")
    return path


def _append_audit_line(vault: Path, line: str) -> Path:
    audit = vault / "_SYSTEM" / "logs" / "audit-log.md"
    audit.parent.mkdir(parents=True, exist_ok=True)
    with audit.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return audit


def test_parse_log_line_valid():
    line = (
        "[2026-02-28T00:00:00Z] [PROMOTE_SUCCESS] "
        "[02-DRAFTS/Operations/SOPs/DRAFT-sop-21.md] "
        "[D:/dev/github/fit-docs/docs/Operations/SOPs/SOP-21-Test.md] [abc123]"
    )
    parsed = parse_log_line(line)
    assert parsed is not None
    assert parsed["action"] == "PROMOTE_SUCCESS"
    assert parsed["commit"] == "abc123"


def test_parse_log_line_invalid():
    assert parse_log_line("not an audit line") is None


def test_find_last_promote_entry_uses_latest(tmp_path: Path):
    vault = tmp_path / "vault"
    audit = vault / "_SYSTEM" / "logs" / "audit-log.md"
    _append_audit_line(
        vault,
        "[2026-02-28T01:00:00Z] [PROMOTE_SUCCESS] [02-DRAFTS/a.md] [D:/docs/target.md] [oldhash]",
    )
    _append_audit_line(
        vault,
        "[2026-02-28T02:00:00Z] [PROMOTE_SUCCESS] [02-DRAFTS/b.md] [D:/docs/target.md] [newhash]",
    )

    entry = find_last_promote_entry("target.md", audit_log=audit)
    assert entry["source"] == "02-DRAFTS/b.md"
    assert entry["commit"] == "newhash"


def test_restore_draft_from_archive_resets_status(tmp_path: Path):
    vault = tmp_path / "vault"
    _write_archive(
        vault,
        "DRAFT-sop-21.md",
        {"title": "Test", "status": "promoted", "updated": "2025-01-01"},
        "## Body\n",
    )

    restored = restore_draft_from_archive(
        "DRAFT-sop-21.md",
        "02-DRAFTS/Operations/SOPs/DRAFT-sop-21.md",
        vault_root=vault,
    )
    text = restored.read_text(encoding="utf-8")
    assert "status: promote-ready" in text
    assert "## Body" in text


def test_rollback_dry_run_appends_dry_run_audit(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    vault = tmp_path / "vault"
    fit_docs = tmp_path / "fit-docs" / "docs"
    fit_docs.mkdir(parents=True, exist_ok=True)
    _append_audit_line(
        vault,
        "[2026-02-28T01:00:00Z] [PROMOTE_SUCCESS] "
        "[02-DRAFTS/Operations/SOPs/DRAFT-sop-21.md] "
        f"[{(fit_docs / 'Operations' / 'SOPs' / 'SOP-21-Test.md').as_posix()}] [abc123]",
    )

    rollback("SOP-21-Test.md", vault_root=vault, fit_docs_root=fit_docs, dry_run=True)
    out = capsys.readouterr().out
    assert "[dry-run] rollback plan" in out

    audit = vault / "_SYSTEM" / "logs" / "audit-log.md"
    lines = audit.read_text(encoding="utf-8").splitlines()
    assert any("[ROLLBACK_DRY_RUN]" in line and "[dry-run]" in line for line in lines)


def test_rollback_full_flow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    vault = tmp_path / "vault"
    fit_docs = tmp_path / "fit-docs" / "docs"
    target = fit_docs / "Operations" / "SOPs" / "SOP-21-Test.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# published\n", encoding="utf-8")

    _append_audit_line(
        vault,
        "[2026-02-28T01:00:00Z] [PROMOTE_SUCCESS] "
        "[02-DRAFTS/Operations/SOPs/DRAFT-sop-21.md] "
        f"[{target.as_posix()}] [abc123]",
    )
    _write_archive(
        vault,
        "DRAFT-sop-21.md",
        {"title": "Test", "status": "promoted", "updated": "2025-01-01"},
        "## Body\n",
    )

    calls: list[list[str]] = []

    def fake_run(cmd, cwd=None, check=False):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr("rollback.subprocess.run", fake_run)
    monkeypatch.setattr("rollback.subprocess.check_output", lambda *args, **kwargs: b"rollback123\n")

    rollback("SOP-21-Test.md", vault_root=vault, fit_docs_root=fit_docs, dry_run=False)

    assert calls[0] == ["mkdocs", "build", "--strict"]
    assert calls[1][0:2] == ["git", "rm"]
    assert calls[2][0:2] == ["git", "commit"]
    assert not target.exists()

    restored = vault / "02-DRAFTS" / "Operations" / "SOPs" / "DRAFT-sop-21.md"
    assert restored.exists()
    restored_text = restored.read_text(encoding="utf-8")
    assert "status: promote-ready" in restored_text

    audit = vault / "_SYSTEM" / "logs" / "audit-log.md"
    lines = audit.read_text(encoding="utf-8").splitlines()
    assert any("[ROLLBACK_SUCCESS]" in line and "[rollback123]" in line for line in lines)


def test_append_audit_writes_line(tmp_path: Path):
    audit = tmp_path / "vault" / "_SYSTEM" / "logs" / "audit-log.md"
    append_audit("ROLLBACK_DRY_RUN", "src.md", "target.md", "dry-run", audit_log=audit)
    text = audit.read_text(encoding="utf-8")
    assert "[ROLLBACK_DRY_RUN]" in text
    assert "[src.md]" in text
