"""Backward-compatible wrapper for fit_docs_sync.py.

Use fit_docs_sync.py for new integrations.
"""

from fit_docs_sync import main, sync

__all__ = ["main", "sync"]


if __name__ == "__main__":
    main()
