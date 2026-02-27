from pathlib import Path

from fit_docs_sync import sync


def _make_source(tmp_path: Path) -> Path:
    src = tmp_path / "source"
    (src / "Operations" / "SOPs").mkdir(parents=True)
    (src / "Operations" / "SOPs" / "README.md").write_text("SOP rules", encoding="utf-8")
    (src / "Operations" / "SOPs" / "SOP 01.md").write_text("content", encoding="utf-8")
    (src / "Knowledge Base").mkdir(parents=True)
    (src / "Knowledge Base" / "README.md").write_text("KB rules", encoding="utf-8")
    return src


def test_sync_copies_new_files(tmp_path: Path):
    src = _make_source(tmp_path)
    vault = tmp_path / "vault"
    vault.mkdir()

    result = sync(src, vault)

    assert len(result["copied"]) == 3
    ref = vault / "_REFERENCE" / "fit-docs"
    assert (ref / "Operations" / "SOPs" / "README.md").read_text(encoding="utf-8") == "SOP rules"
    assert (ref / "Knowledge Base" / "README.md").read_text(encoding="utf-8") == "KB rules"


def test_sync_updates_changed_files(tmp_path: Path):
    src = _make_source(tmp_path)
    vault = tmp_path / "vault"
    vault.mkdir()
    sync(src, vault)

    (src / "Operations" / "SOPs" / "README.md").write_text("updated rules", encoding="utf-8")
    result = sync(src, vault)

    assert "Operations\\SOPs\\README.md" in result["updated"] or "Operations/SOPs/README.md" in result["updated"]
    ref = vault / "_REFERENCE" / "fit-docs"
    assert (ref / "Operations" / "SOPs" / "README.md").read_text(encoding="utf-8") == "updated rules"


def test_sync_removes_deleted_files(tmp_path: Path):
    src = _make_source(tmp_path)
    vault = tmp_path / "vault"
    vault.mkdir()
    sync(src, vault)

    (src / "Operations" / "SOPs" / "SOP 01.md").unlink()
    result = sync(src, vault)

    assert len(result["removed"]) == 1
    ref = vault / "_REFERENCE" / "fit-docs"
    assert not (ref / "Operations" / "SOPs" / "SOP 01.md").exists()


def test_sync_is_idempotent(tmp_path: Path):
    src = _make_source(tmp_path)
    vault = tmp_path / "vault"
    vault.mkdir()
    sync(src, vault)

    result = sync(src, vault)
    total = sum(len(v) for v in result.values())
    assert total == 0
