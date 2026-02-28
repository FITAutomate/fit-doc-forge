from datetime import date
from pathlib import Path

from airtable_sync import (
    build_airtable_url,
    fetch_airtable_records,
    sync,
)


def test_build_airtable_url_encodes_table_and_view():
    url = build_airtable_url("appBase123", "Ops Tasks", view="Daily Queue", page_size=50)
    assert url.startswith("https://api.airtable.com/v0/appBase123/Ops%20Tasks?")
    assert "view=Daily+Queue" in url
    assert "pageSize=50" in url


def test_fetch_airtable_records_handles_pagination():
    calls: list[str] = []
    pages = [
        {"records": [{"id": "recA", "fields": {}}], "offset": "next-page"},
        {"records": [{"id": "recB", "fields": {}}]},
    ]

    def fake_fetcher(url: str, api_key: str):  # noqa: ARG001
        calls.append(url)
        return pages[len(calls) - 1]

    records = fetch_airtable_records(
        api_key="key123",
        base_id="appBase",
        table_id="Tasks",
        fetcher=fake_fetcher,
        page_size=1,
    )

    assert [record["id"] for record in records] == ["recA", "recB"]
    assert len(calls) == 2
    assert "offset=next-page" in calls[1]


def test_sync_filters_overdue_and_due_today_and_renders_preview(tmp_path: Path):
    today = date(2026, 2, 28)
    payload = {
        "records": [
            {
                "id": "recOverdue",
                "fields": {"Due": "2026-02-27", "Task": "Fix alerts", "Owner": "Ops", "Status": "In Progress"},
            },
            {
                "id": "recToday",
                "fields": {"Due": "2026-02-28", "Task": "Publish update", "Owner": "Docs", "Status": "Open"},
            },
            {
                "id": "recDone",
                "fields": {"Due": "2026-02-28", "Task": "Closed item", "Owner": "Ops", "Status": "Done"},
            },
            {
                "id": "recFuture",
                "fields": {"Due": "2026-03-01", "Task": "Future item", "Owner": "Ops", "Status": "Open"},
            },
            {
                "id": "recNoDue",
                "fields": {"Task": "No date", "Owner": "Ops", "Status": "Open"},
            },
        ]
    }

    def fake_fetcher(url: str, api_key: str):  # noqa: ARG001
        return payload

    result = sync(
        api_key="key123",
        base_id="appBase",
        table_id="Tasks",
        vault_root=tmp_path / "vault",
        dry_run=True,
        today=today,
        fetcher=fake_fetcher,
    )

    assert result["total_records"] == 5
    assert result["overdue_count"] == 1
    assert result["due_today_count"] == 1
    assert result["written"] is False
    assert "Fix alerts" in result["dashboard"]
    assert "Publish update" in result["dashboard"]
    assert "Closed item" not in result["dashboard"]
    assert "Future item" not in result["dashboard"]

    dashboard_path = Path(result["target"])
    assert not dashboard_path.exists()


def test_sync_writes_ops_dashboard_file(tmp_path: Path):
    payload = {
        "records": [
            {
                "id": "recWrite",
                "fields": {"Due": "2026-02-28", "Task": "Ship release", "Owner": "Ops", "Status": "Open"},
            }
        ]
    }

    def fake_fetcher(url: str, api_key: str):  # noqa: ARG001
        return payload

    vault = tmp_path / "vault"
    result = sync(
        api_key="key123",
        base_id="appBase",
        table_id="Tasks",
        vault_root=vault,
        dry_run=False,
        today=date(2026, 2, 28),
        fetcher=fake_fetcher,
    )

    target = Path(result["target"])
    assert target.exists()
    content = target.read_text(encoding="utf-8")
    assert content.startswith("# Ops Dashboard")
    assert "Ship release" in content
    assert result["written"] is True
