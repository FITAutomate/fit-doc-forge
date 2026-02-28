"""Sync Airtable tasks into the vault ops dashboard.

Phase 5 implementation target from the blueprint:
- Pull overdue + due-today tasks from Airtable.
- Overwrite 04-OPERATIONS/_ops-dashboard.md in the vault.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_BASE = "https://api.airtable.com/v0"
DEFAULT_COMPLETED_STATUSES = {"done", "complete", "completed", "closed", "canceled", "cancelled"}
FIELD_ID_PATTERN = re.compile(r"^fld[A-Za-z0-9]+$")


@dataclass(frozen=True)
class AirtableTask:
    record_id: str
    due: date
    title: str
    owner: str
    priority: str
    status: str


def _parse_date(value: Any) -> date | None:
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    # Airtable dates are commonly YYYY-MM-DD or ISO timestamps.
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        pass

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return None


def _field_to_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, dict):
        if "name" in value and isinstance(value["name"], str):
            return value["name"].strip()
        return json.dumps(value, ensure_ascii=False)

    if isinstance(value, list):
        parts = [_field_to_text(item) for item in value]
        return ", ".join(part for part in parts if part)

    return str(value)


def _escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _escape_link_text(value: str) -> str:
    return value.replace("[", "\\[").replace("]", "\\]")


def _looks_like_field_id(value: str) -> bool:
    return bool(FIELD_ID_PATTERN.match(value.strip()))


def build_airtable_url(
    base_id: str,
    table_id: str,
    *,
    view: str = "",
    offset: str = "",
    page_size: int = 100,
    return_fields_by_field_id: bool = False,
) -> str:
    encoded_base = quote(base_id, safe="")
    encoded_table = quote(table_id, safe="")
    params: dict[str, str | int] = {"pageSize": page_size}
    if view:
        params["view"] = view
    if offset:
        params["offset"] = offset
    if return_fields_by_field_id:
        params["returnFieldsByFieldId"] = "true"
    return f"{AIRTABLE_API_BASE}/{encoded_base}/{encoded_table}?{urlencode(params)}"


def build_airtable_record_url(
    *,
    base_id: str,
    table_id: str,
    view: str,
    record_id: str,
) -> str:
    parts = [quote(base_id, safe=""), quote(table_id, safe="")]
    if view:
        parts.append(quote(view, safe=""))
    parts.append(quote(record_id, safe=""))
    return f"https://airtable.com/{'/'.join(parts)}"


def _fetch_base_name(
    api_key: str,
    base_id: str,
    fetcher: Callable[[str, str], dict[str, Any]] | None = None,
) -> str:
    real_fetcher = fetcher or fetch_json
    data = real_fetcher(f"{AIRTABLE_API_BASE}/meta/bases", api_key)
    bases = data.get("bases", [])
    if not isinstance(bases, list):
        return ""
    for base in bases:
        if not isinstance(base, dict):
            continue
        if str(base.get("id", "")).strip() == base_id:
            return _field_to_text(base.get("name"))
    return ""


def _fetch_table_and_view_names(
    api_key: str,
    base_id: str,
    *,
    table_id: str,
    view_id: str,
    fetcher: Callable[[str, str], dict[str, Any]] | None = None,
) -> tuple[str, str]:
    real_fetcher = fetcher or fetch_json
    encoded_base = quote(base_id, safe="")
    data = real_fetcher(f"{AIRTABLE_API_BASE}/meta/bases/{encoded_base}/tables", api_key)
    tables = data.get("tables", [])
    if not isinstance(tables, list):
        return "", ""

    found_table_name = ""
    found_view_name = ""
    for table in tables:
        if not isinstance(table, dict):
            continue
        table_match = str(table.get("id", "")).strip() == table_id or _field_to_text(table.get("name")) == table_id
        if not table_match:
            continue
        found_table_name = _field_to_text(table.get("name"))
        views = table.get("views", [])
        if not isinstance(views, list):
            break
        for view in views:
            if not isinstance(view, dict):
                continue
            view_match = str(view.get("id", "")).strip() == view_id or _field_to_text(view.get("name")) == view_id
            if view_match:
                found_view_name = _field_to_text(view.get("name"))
                break
        break

    return found_table_name, found_view_name


def resolve_airtable_display_names(
    *,
    api_key: str,
    base_id: str,
    table_id: str,
    view: str,
    base_name: str = "",
    table_name: str = "",
    view_name: str = "",
    fetcher: Callable[[str, str], dict[str, Any]] | None = None,
) -> tuple[str, str, str]:
    resolved_base = base_name.strip() if base_name else ""
    resolved_table = table_name.strip() if table_name else ""
    resolved_view = view_name.strip() if view_name else ""

    if resolved_base and resolved_table and (resolved_view or not view):
        return resolved_base, resolved_table, resolved_view

    try:
        if not resolved_base:
            resolved_base = _fetch_base_name(api_key, base_id, fetcher=fetcher)
        if (not resolved_table) or (view and not resolved_view):
            table_display, view_display = _fetch_table_and_view_names(
                api_key,
                base_id,
                table_id=table_id,
                view_id=view,
                fetcher=fetcher,
            )
            if not resolved_table:
                resolved_table = table_display
            if view and not resolved_view:
                resolved_view = view_display
    except RuntimeError:
        # Metadata scopes may be unavailable; fall back to IDs.
        pass

    return (
        resolved_base or base_id,
        resolved_table or table_id,
        resolved_view or (view or "(none)"),
    )


def fetch_json(url: str, api_key: str) -> dict[str, Any]:
    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=30) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Airtable API error ({exc.code}): {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Airtable API unreachable: {exc.reason}") from exc


def fetch_airtable_records(
    *,
    api_key: str,
    base_id: str,
    table_id: str,
    view: str = "",
    page_size: int = 100,
    max_records: int = 500,
    return_fields_by_field_id: bool = False,
    fetcher: Callable[[str, str], dict[str, Any]] = fetch_json,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    offset = ""

    while True:
        url = build_airtable_url(
            base_id,
            table_id,
            view=view,
            offset=offset,
            page_size=page_size,
            return_fields_by_field_id=return_fields_by_field_id,
        )
        data = fetcher(url, api_key)
        page_records = data.get("records", [])
        if not isinstance(page_records, list):
            raise RuntimeError("Airtable response is missing a valid records list")

        records.extend(page_records)
        if len(records) >= max_records:
            return records[:max_records]

        next_offset = data.get("offset")
        if not isinstance(next_offset, str) or not next_offset:
            return records
        offset = next_offset


def record_to_task(
    record: dict[str, Any],
    *,
    due_field: str,
    title_field: str,
    status_field: str,
    owner_field: str,
    priority_field: str,
    completed_statuses: set[str],
) -> AirtableTask | None:
    fields = record.get("fields", {})
    if not isinstance(fields, dict):
        return None

    due_value = _parse_date(fields.get(due_field))
    if due_value is None:
        return None

    status = _field_to_text(fields.get(status_field))
    if status.lower() in completed_statuses:
        return None

    title = _field_to_text(fields.get(title_field))
    record_id = _field_to_text(record.get("id"))

    if not title:
        title = f"(untitled task {record_id or 'unknown'})"
    owner = _field_to_text(fields.get(owner_field)) if owner_field else ""
    priority = _field_to_text(fields.get(priority_field)) if priority_field else ""

    return AirtableTask(
        record_id=record_id or "unknown",
        due=due_value,
        title=title,
        owner=owner,
        priority=priority or "-",
        status=status or "unspecified",
    )


def split_tasks(tasks: list[AirtableTask], *, today: date) -> tuple[list[AirtableTask], list[AirtableTask]]:
    overdue = [task for task in tasks if task.due < today]
    due_today = [task for task in tasks if task.due == today]
    overdue.sort(key=lambda item: (item.due, item.title.lower()))
    due_today.sort(key=lambda item: item.title.lower())
    return overdue, due_today


def _render_section(
    tasks: list[AirtableTask],
    *,
    base_id: str,
    table_id: str,
    view: str,
) -> list[str]:
    if not tasks:
        return ["_None._"]

    lines = [
        "| Due | Task | Owner | Priority | Status |",
        "|---|---|---|---|---|",
    ]
    for task in tasks:
        task_label = _escape_table_cell(task.title)
        if base_id and table_id and task.record_id != "unknown":
            record_url = build_airtable_record_url(
                base_id=base_id,
                table_id=table_id,
                view=view,
                record_id=task.record_id,
            )
            task_label = f"[{_escape_link_text(task_label)}]({record_url})"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(task.due),
                    task_label,
                    _escape_table_cell(task.owner or "-"),
                    _escape_table_cell(task.priority or "-"),
                    _escape_table_cell(task.status),
                ]
            )
            + " |"
        )
    return lines


def render_dashboard(
    *,
    overdue: list[AirtableTask],
    due_today: list[AirtableTask],
    generated_at: datetime,
    base_name: str,
    table_name: str,
    view_name: str,
    base_id: str,
    table_id: str,
    view: str,
    dashboard_view_url: str = "",
    dashboard_view_label: str = "Open board view",
) -> str:
    timestamp = generated_at.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: list[str] = [
        "# Ops Dashboard",
        "",
        "Airtable task mirror (overdue + due today).",
        "",
        f"- Last sync: {timestamp}",
        f"- Airtable base: {base_name}",
        f"- Airtable table: {table_name}",
        f"- Airtable view: {view_name}",
    ]
    if dashboard_view_url:
        lines.extend(
            [
                "",
                f"[{dashboard_view_label}]({dashboard_view_url})",
            ]
        )
    lines.extend(
        [
        "",
        "## Overdue",
        ]
    )
    lines.extend(_render_section(overdue, base_id=base_id, table_id=table_id, view=view))
    lines.extend(["", "## Due Today"])
    lines.extend(_render_section(due_today, base_id=base_id, table_id=table_id, view=view))
    lines.extend(
        [
            "",
            "## Summary",
            f"- Overdue: {len(overdue)}",
            f"- Due today: {len(due_today)}",
            f"- Total surfaced: {len(overdue) + len(due_today)}",
            "",
        ]
    )
    return "\n".join(lines)


def sync(
    *,
    api_key: str,
    base_id: str,
    table_id: str,
    vault_root: Path,
    view: str = "",
    due_field: str = "Due Date",
    title_field: str = "Task Name",
    status_field: str = "Status",
    owner_field: str = "Assignee Name",
    priority_field: str = "Priority",
    base_name: str = "",
    table_name: str = "",
    view_name: str = "",
    dashboard_view_url: str = "",
    dashboard_view_label: str = "Open board view",
    max_records: int = 500,
    use_field_ids: bool = False,
    dry_run: bool = False,
    today: date | None = None,
    fetcher: Callable[[str, str], dict[str, Any]] = fetch_json,
) -> dict[str, Any]:
    records = fetch_airtable_records(
        api_key=api_key,
        base_id=base_id,
        table_id=table_id,
        view=view,
        max_records=max_records,
        return_fields_by_field_id=use_field_ids,
        fetcher=fetcher,
    )

    completed_statuses = {status.lower() for status in DEFAULT_COMPLETED_STATUSES}
    tasks: list[AirtableTask] = []
    for record in records:
        task = record_to_task(
            record,
            due_field=due_field,
            title_field=title_field,
            status_field=status_field,
            owner_field=owner_field,
            priority_field=priority_field,
            completed_statuses=completed_statuses,
        )
        if task:
            tasks.append(task)

    ref_day = today or date.today()
    overdue, due_today = split_tasks(tasks, today=ref_day)
    resolved_base_name, resolved_table_name, resolved_view_name = resolve_airtable_display_names(
        api_key=api_key,
        base_id=base_id,
        table_id=table_id,
        view=view,
        base_name=base_name,
        table_name=table_name,
        view_name=view_name,
        fetcher=fetcher,
    )

    rendered = render_dashboard(
        overdue=overdue,
        due_today=due_today,
        generated_at=datetime.now(timezone.utc),
        base_name=resolved_base_name,
        table_name=resolved_table_name,
        view_name=resolved_view_name,
        base_id=base_id,
        table_id=table_id,
        view=view,
        dashboard_view_url=dashboard_view_url,
        dashboard_view_label=dashboard_view_label,
    )

    target = vault_root / "04-OPERATIONS" / "_ops-dashboard.md"
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")

    return {
        "total_records": len(records),
        "overdue_count": len(overdue),
        "due_today_count": len(due_today),
        "written": not dry_run,
        "target": str(target),
        "dashboard": rendered,
        "base_name": resolved_base_name,
        "table_name": resolved_table_name,
        "view_name": resolved_view_name,
    }


def inspect_records(
    *,
    records: list[dict[str, Any]],
    due_field: str,
    status_field: str,
) -> dict[str, Any]:
    field_names: set[str] = set()
    status_counts: dict[str, int] = {}
    due_populated = 0

    for record in records:
        fields = record.get("fields", {})
        if not isinstance(fields, dict):
            continue
        field_names.update(str(name) for name in fields.keys())

        if fields.get(due_field):
            due_populated += 1

        status = _field_to_text(fields.get(status_field)) or "(blank)"
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "total_records": len(records),
        "due_populated": due_populated,
        "field_names": sorted(field_names),
        "status_counts": dict(sorted(status_counts.items())),
    }


def _env_int(name: str, fallback: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


def _env_bool(name: str, fallback: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return fallback
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _ensure_utf8_stdio() -> None:
    stdout = getattr(sys.stdout, "buffer", None)
    stderr = getattr(sys.stderr, "buffer", None)
    if stdout and sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(stdout, encoding="utf-8", errors="replace")
    if stderr and sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
        sys.stderr = io.TextIOWrapper(stderr, encoding="utf-8", errors="replace")


def main() -> None:
    _ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Sync Airtable tasks into the vault ops dashboard")
    parser.add_argument("--api-key", default=os.getenv("AIRTABLE_API_KEY", ""), help="Airtable API key")
    parser.add_argument("--base-id", default=os.getenv("AIRTABLE_BASE_ID", ""), help="Airtable base ID")
    parser.add_argument("--table-id", default=os.getenv("AIRTABLE_TABLE_ID", ""), help="Airtable table ID/name")
    parser.add_argument("--view", default=os.getenv("AIRTABLE_VIEW", ""), help="Optional Airtable view")
    parser.add_argument("--base-name", default=os.getenv("AIRTABLE_BASE_NAME", ""), help="Display name for Airtable base")
    parser.add_argument("--table-name", default=os.getenv("AIRTABLE_TABLE_NAME", ""), help="Display name for Airtable table")
    parser.add_argument("--view-name", default=os.getenv("AIRTABLE_VIEW_NAME", ""), help="Display name for Airtable view")
    parser.add_argument(
        "--dashboard-view-url",
        default=os.getenv("AIRTABLE_DASHBOARD_VIEW_URL", ""),
        help="Top-of-dashboard link to Airtable board view",
    )
    parser.add_argument(
        "--dashboard-view-label",
        default=os.getenv("AIRTABLE_DASHBOARD_VIEW_LABEL", "Open board view"),
        help="Label text for the top-of-dashboard view link",
    )
    parser.add_argument("--due-field", default=os.getenv("AIRTABLE_DUE_FIELD", "Due Date"), help="Due date field")
    parser.add_argument("--title-field", default=os.getenv("AIRTABLE_TITLE_FIELD", "Task Name"), help="Task title field")
    parser.add_argument("--status-field", default=os.getenv("AIRTABLE_STATUS_FIELD", "Status"), help="Task status field")
    parser.add_argument("--owner-field", default=os.getenv("AIRTABLE_OWNER_FIELD", "Assignee Name"), help="Task owner field")
    parser.add_argument("--priority-field", default=os.getenv("AIRTABLE_PRIORITY_FIELD", "Priority"), help="Task priority field")
    parser.add_argument(
        "--use-field-ids",
        action="store_true",
        default=_env_bool("AIRTABLE_USE_FIELD_IDS", False),
        help="Treat AIRTABLE_*_FIELD values as Airtable field IDs (fld...)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=_env_int("AIRTABLE_MAX_RECORDS", 500),
        help="Maximum records to process",
    )
    parser.add_argument(
        "--vault",
        type=Path,
        default=Path(os.getenv("VAULT_ROOT", r"D:\Vaults\FIT-Vault")),
        help="Vault root path",
    )
    parser.add_argument(
        "--today",
        type=lambda value: date.fromisoformat(value),
        default=None,
        help="Override current day (YYYY-MM-DD) for deterministic runs",
    )
    parser.add_argument(
        "--inspect-fields",
        action="store_true",
        help="Print field names/status counts from records and exit",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print preview only, do not write files")
    args = parser.parse_args()

    missing: list[str] = []
    if not args.api_key:
        missing.append("AIRTABLE_API_KEY / --api-key")
    if not args.base_id:
        missing.append("AIRTABLE_BASE_ID / --base-id")
    if not args.table_id:
        missing.append("AIRTABLE_TABLE_ID / --table-id")
    if missing:
        for item in missing:
            print(f"ERROR: missing required setting: {item}", file=sys.stderr)
        raise SystemExit(1)

    resolved_use_field_ids = args.use_field_ids or any(
        _looks_like_field_id(value)
        for value in [args.due_field, args.title_field, args.status_field, args.owner_field, args.priority_field]
    )

    try:
        if args.inspect_fields:
            records = fetch_airtable_records(
                api_key=args.api_key,
                base_id=args.base_id,
                table_id=args.table_id,
                view=args.view,
                max_records=args.max_records,
                return_fields_by_field_id=resolved_use_field_ids,
            )
            summary = inspect_records(records=records, due_field=args.due_field, status_field=args.status_field)
            print(f"Records scanned: {summary['total_records']}")
            print(f"Records with {args.due_field} populated: {summary['due_populated']}")
            print("Field names seen in records:")
            for field_name in summary["field_names"]:
                print(f"- {field_name}")
            print("Status counts:")
            for status_name, count in summary["status_counts"].items():
                print(f"- {status_name}: {count}")
            return

        result = sync(
            api_key=args.api_key,
            base_id=args.base_id,
            table_id=args.table_id,
            view=args.view,
            due_field=args.due_field,
            title_field=args.title_field,
            status_field=args.status_field,
            owner_field=args.owner_field,
            priority_field=args.priority_field,
            base_name=args.base_name,
            table_name=args.table_name,
            view_name=args.view_name,
            dashboard_view_url=args.dashboard_view_url,
            dashboard_view_label=args.dashboard_view_label,
            max_records=args.max_records,
            use_field_ids=resolved_use_field_ids,
            vault_root=args.vault,
            today=args.today,
            dry_run=args.dry_run,
        )
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    mode = "Dry run" if args.dry_run else "Sync complete"
    print(f"{mode}: {result['total_records']} records scanned")
    print(f"  Overdue: {result['overdue_count']}")
    print(f"  Due today: {result['due_today_count']}")
    print(f"  Dashboard: {result['target']}")
    if args.dry_run:
        print("\n--- dashboard preview ---\n")
        print(result["dashboard"])


if __name__ == "__main__":
    main()
