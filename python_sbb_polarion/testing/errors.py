"""Exceptions raised by the testing helpers."""

from __future__ import annotations


class TempProjectError(RuntimeError):
    """Raised when setting up or tearing down a temporary test project fails.

    Replaces the previous ``sys.exit`` calls so a failure aborts only the current
    test (or surfaces through the CLI's exception handler) instead of killing the
    whole process.
    """
