from pathlib import Path

from scaffold_vault import DIRECTORIES, PLACEHOLDER_FILES, scaffold


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
