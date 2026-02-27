from pathlib import Path

import pytest
import yaml

from promote import (
    build_filename,
    check_gate,
    load_frontmatter,
    promote,
    resolve_target_folder,
    update_last_updated,
)


def _write_draft(vault: Path, rel_path: str, fm: dict, body: str = "\n# Test\n") -> Path:
    """Helper to write a draft file with YAML frontmatter."""
    p = vault / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    content = "---\n" + yaml.dump(fm, allow_unicode=True) + f"---\n{body}"
    p.write_text(content, encoding="utf-8")
    return p


VALID_FM = {
    "title": "Test Doc",
    "type": "sop",
    "sop_number": 21,
    "status": "promote-ready",
    "kb_target": "INTERNAL",
    "gate_has_owner": True,
    "gate_metadata_complete": True,
    "gate_heading_structure_valid": True,
    "gate_reviewed_by_human": True,
}


# --- load_frontmatter ---

def test_load_frontmatter(tmp_path: Path):
    p = tmp_path / "test.md"
    p.write_text("---\ntitle: Hello\ntype: sop\n---\n# Body\n", encoding="utf-8")
    fm, body = load_frontmatter(p)
    assert fm["title"] == "Hello"
    assert "# Body" in body


def test_load_frontmatter_no_yaml(tmp_path: Path):
    p = tmp_path / "test.md"
    p.write_text("# No frontmatter\n", encoding="utf-8")
    fm, body = load_frontmatter(p)
    assert fm == {}
    assert "# No frontmatter" in body


# --- check_gate ---

def test_check_gate_all_pass():
    assert check_gate(VALID_FM) == []


def test_check_gate_missing_fields():
    fm = {**VALID_FM, "gate_has_owner": False, "gate_reviewed_by_human": False}
    failures = check_gate(fm)
    assert "gate_has_owner" in failures
    assert "gate_reviewed_by_human" in failures


def test_check_gate_public_extra_fields():
    fm = {**VALID_FM, "kb_target": "PUBLIC_WEB"}
    failures = check_gate(fm)
    assert "gate_no_internal_refs" in failures
    assert "gate_no_invented_slas" in failures


def test_check_gate_public_all_pass():
    fm = {
        **VALID_FM,
        "kb_target": "PUBLIC_WEB",
        "gate_no_internal_refs": True,
        "gate_no_invented_slas": True,
    }
    assert check_gate(fm) == []


# --- build_filename ---

def test_build_filename_sop():
    fm = {"type": "sop", "sop_number": 5, "title": "Onboarding"}
    assert build_filename(fm, "DRAFT-sop-05.md") == "\U0001f4da SOP 05 \u2014 Onboarding.md"


def test_build_filename_procedure_with_system():
    fm = {"type": "procedure", "title": "Clone Workflow", "system": "GitHub"}
    result = build_filename(fm, "DRAFT-proc.md")
    assert result == "\U0001f4cb PROC \u2014 GitHub \u2014 Clone Workflow.md"


def test_build_filename_procedure_no_system():
    fm = {"type": "procedure", "title": "General Steps"}
    result = build_filename(fm, "DRAFT-proc.md")
    assert result == "\U0001f4cb PROC \u2014 General Steps.md"


def test_build_filename_kb():
    fm = {"type": "kb-article", "title": "Glossary"}
    assert build_filename(fm, "DRAFT-kb.md") == "\U0001f4d8 KB \u2014 Glossary.md"


def test_build_filename_no_emoji_type():
    fm = {"type": "blog", "title": "Update"}
    assert build_filename(fm, "DRAFT-blog-update.md") == "blog-update.md"


# --- resolve_target_folder ---

def test_resolve_sop():
    result = resolve_target_folder("02-DRAFTS/Operations/SOPs/DRAFT-sop-01.md")
    assert result.as_posix().endswith("Operations/SOPs")


def test_resolve_kb():
    result = resolve_target_folder("02-DRAFTS/Knowledge-Base/DRAFT-kb-glossary.md")
    assert result.as_posix().endswith("Knowledge Base")


def test_resolve_unknown_raises():
    with pytest.raises(ValueError, match="Cannot resolve"):
        resolve_target_folder("02-DRAFTS/Unknown/file.md")


# --- update_last_updated ---

def test_update_last_updated():
    body = "| Last Updated | 2025-01-01 |"
    result = update_last_updated(body)
    assert "2025-01-01" not in result
    assert "Last Updated" in result


# --- promote (integration) ---

def test_promote_full_flow(tmp_path: Path):
    vault = tmp_path / "vault"
    fit_docs = tmp_path / "fit-docs" / "docs"
    fit_docs.mkdir(parents=True)

    draft_rel = "02-DRAFTS/Operations/SOPs/DRAFT-sop-21-onboarding.md"
    body = "\n| Last Updated | 2025-01-01 |\n\n# Onboarding\n\n## Purpose\n"
    _write_draft(vault, draft_rel, VALID_FM, body)

    result = promote(
        draft_rel,
        vault_root=vault,
        fit_docs_root=fit_docs,
        git_commit=False,
    )

    target = Path(result["target"])
    assert target.exists()
    assert "\U0001f4da SOP 21" in target.name
    assert "Onboarding" in target.read_text(encoding="utf-8")

    archive = Path(result["archive"])
    assert archive.exists()
    assert "07-ARCHIVE" in str(archive)

    draft_after = (vault / draft_rel).read_text(encoding="utf-8")
    assert "status: promoted" in draft_after


def test_promote_rejects_non_ready(tmp_path: Path):
    vault = tmp_path / "vault"
    fit_docs = tmp_path / "fit-docs" / "docs"
    fit_docs.mkdir(parents=True)

    fm = {**VALID_FM, "status": "draft"}
    _write_draft(vault, "02-DRAFTS/Operations/SOPs/test.md", fm)

    with pytest.raises(ValueError, match="must be 'promote-ready'"):
        promote("02-DRAFTS/Operations/SOPs/test.md", vault_root=vault, fit_docs_root=fit_docs, git_commit=False)


def test_promote_rejects_failed_gate(tmp_path: Path):
    vault = tmp_path / "vault"
    fit_docs = tmp_path / "fit-docs" / "docs"
    fit_docs.mkdir(parents=True)

    fm = {**VALID_FM, "gate_has_owner": False}
    _write_draft(vault, "02-DRAFTS/Operations/SOPs/test.md", fm)

    with pytest.raises(ValueError, match="gate_has_owner"):
        promote("02-DRAFTS/Operations/SOPs/test.md", vault_root=vault, fit_docs_root=fit_docs, git_commit=False)


def test_promote_dry_run(tmp_path: Path):
    vault = tmp_path / "vault"
    fit_docs = tmp_path / "fit-docs" / "docs"
    fit_docs.mkdir(parents=True)

    _write_draft(vault, "02-DRAFTS/Operations/SOPs/test.md", VALID_FM)

    result = promote(
        "02-DRAFTS/Operations/SOPs/test.md",
        vault_root=vault,
        fit_docs_root=fit_docs,
        dry_run=True,
    )

    assert "Operations" in result["target"]
    assert result["archive"] == ""
    assert not (fit_docs / "Operations" / "SOPs").exists()
