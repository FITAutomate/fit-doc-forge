from pathlib import Path

from scaffold_vault import DIRECTORIES, PLACEHOLDER_FILES, TEMPLATES_DIR, SYSTEM_DOCS_DIR, scaffold

EXPECTED_TEMPLATES = [
    "doc-request.md",
    "kb-article-draft.md",
    "procedure-draft.md",
    "solution-description.md",
    "sop-draft.md",
]

EXPECTED_SYSTEM_DOCS = [
    "agent-instructions.md",
    "vault-map.md",
]

EXPECTED_SCRIPTS = [
    "promote.py",
    "rollback.py",
    "fit_docs_sync.py",
    "fit-docs_sync.py",
    "airtable_sync.py",
]


def test_scaffold_creates_all_directories(tmp_path: Path):
    scaffold(tmp_path)
    for d in DIRECTORIES:
        assert (tmp_path / d).is_dir(), f"Missing directory: {d}"


def test_scaffold_creates_placeholder_files(tmp_path: Path):
    scaffold(tmp_path)
    for rel_path, expected_content in PLACEHOLDER_FILES.items():
        target = tmp_path / rel_path
        assert target.exists(), f"Missing placeholder: {rel_path}"
        assert target.read_text(encoding="utf-8") == expected_content


def test_scaffold_copies_templates(tmp_path: Path):
    scaffold(tmp_path)
    tpl_dir = tmp_path / "_SYSTEM" / "templates"
    for name in EXPECTED_TEMPLATES:
        dest = tpl_dir / name
        assert dest.exists(), f"Missing template: {name}"
        src = TEMPLATES_DIR / name
        assert dest.read_text(encoding="utf-8") == src.read_text(encoding="utf-8")


def test_scaffold_copies_system_docs(tmp_path: Path):
    scaffold(tmp_path)
    sys_dir = tmp_path / "_SYSTEM"
    for name in EXPECTED_SYSTEM_DOCS:
        dest = sys_dir / name
        assert dest.exists(), f"Missing system doc: {name}"
        src = SYSTEM_DOCS_DIR / name
        assert dest.read_text(encoding="utf-8") == src.read_text(encoding="utf-8")


def test_scaffold_copies_scripts(tmp_path: Path):
    scaffold(tmp_path)
    scripts_dir = tmp_path / "_SYSTEM" / "scripts"
    for name in EXPECTED_SCRIPTS:
        assert (scripts_dir / name).exists(), f"Missing script: {name}"


def test_scaffold_does_not_overwrite_user_templates(tmp_path: Path):
    scaffold(tmp_path)
    custom = tmp_path / "_SYSTEM" / "templates" / "sop-draft.md"
    custom.write_text("my custom version", encoding="utf-8")

    actions = scaffold(tmp_path)
    assert not any("template sop-draft.md" in a for a in actions)
    assert custom.read_text(encoding="utf-8") == "my custom version"


def test_scaffold_does_not_overwrite_user_system_docs(tmp_path: Path):
    scaffold(tmp_path)
    custom = tmp_path / "_SYSTEM" / "agent-instructions.md"
    custom.write_text("my custom instructions", encoding="utf-8")

    actions = scaffold(tmp_path)
    assert not any("system-doc agent-instructions.md" in a for a in actions)
    assert custom.read_text(encoding="utf-8") == "my custom instructions"


def test_scaffold_is_idempotent(tmp_path: Path):
    scaffold(tmp_path)
    marker = tmp_path / "00-INBOX" / "_quick-capture.md"
    marker.write_text("user content", encoding="utf-8")

    actions = scaffold(tmp_path)
    assert actions == [], "Second run should take no actions"
    assert marker.read_text(encoding="utf-8") == "user content", "Existing file overwritten"


def test_scaffold_returns_actions(tmp_path: Path):
    actions = scaffold(tmp_path)
    assert len(actions) > 0, "First run should report actions"
    assert any("mkdir" in a for a in actions)
    assert any("write" in a for a in actions)
    assert any("template" in a for a in actions)
    assert any("system-doc" in a for a in actions)
