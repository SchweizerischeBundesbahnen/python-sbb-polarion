"""Path utilities for resolving paths relative to caller's location."""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import overload


def __resolve_from_caller(relative_path: str | Path, stack_depth: int) -> Path:
    """Resolve path relative to caller's file location.

    Args:
        relative_path: Path relative to the caller's file location
        stack_depth: How many stack frames to go up to find the caller

    Returns:
        Absolute resolved path
    """
    caller_frame: inspect.FrameInfo = inspect.stack()[stack_depth]
    caller_file: Path = Path(caller_frame.filename).resolve()
    return (caller_file.parent / relative_path).resolve()


@overload
def abs_path_str(relative_path: None) -> None: ...
@overload
def abs_path_str(relative_path: str | Path) -> str: ...
def abs_path_str(relative_path: str | Path | None) -> str | None:
    """Resolve path relative to the caller's file location and return as string.

    Same as abs_path() but returns str instead of Path.

    Args:
        relative_path: Path relative to the caller's file location, or None

    Returns:
        Absolute resolved path as string, or None if input is None

    Example:
        # In /project/tests/test_foo.py:
        data_file = abs_path_str("data/config.json")
        # Returns: "/project/tests/data/config.json"

        # With None:
        data_file = abs_path_str(None)
        # Returns: None

        # Works regardless of current working directory
    """
    if relative_path is None:
        return None
    return str(__resolve_from_caller(relative_path, stack_depth=2))


@overload
def abs_path(relative_path: None) -> None: ...
@overload
def abs_path(relative_path: str | Path) -> Path: ...
def abs_path(relative_path: str | Path | None) -> Path | None:
    """Resolve path relative to the caller's file location.

    Unlike Path.resolve() which resolves relative to current working directory,
    this function resolves paths relative to the file that calls this function.

    This is useful for tests and configurations where you want to reference
    files relative to the source file, not the directory from which the script
    is executed.

    Args:
        relative_path: Path relative to the caller's file location, or None

    Returns:
        Absolute resolved path, or None if input is None

    Example:
        # In /project/tests/test_foo.py:
        data_file = abs_path("data/config.json")
        # Returns: /project/tests/data/config.json

        # With None:
        data_file = abs_path(None)
        # Returns: None

        # Works regardless of current working directory
    """
    if relative_path is None:
        return None
    return __resolve_from_caller(relative_path, stack_depth=2)
