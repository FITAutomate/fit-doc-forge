"""Airtable -> vault operations sync entrypoint.

Phase 5 implementation target from the blueprint.
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Airtable tasks into the vault ops dashboard")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions only")
    args = parser.parse_args()

    mode = "dry-run" if args.dry_run else "run"
    print(f"airtable_sync.py is not implemented yet ({mode}).")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
