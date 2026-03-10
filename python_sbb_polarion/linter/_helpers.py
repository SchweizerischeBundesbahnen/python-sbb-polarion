"""Helper functions for the linter."""

from __future__ import annotations

import ast
import fnmatch
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Iterator


def get_method_name(node: ast.Call) -> str | None:
    """Extract method name from call node.

    Returns:
        Method name string or None if not found.
    """
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    if isinstance(node.func, ast.Name):
        return node.func.id
    return None


def reconstruct_fstring(node: ast.JoinedStr) -> str:
    """Reconstruct f-string to check for query params.

    Returns:
        Reconstructed string with placeholders for expressions.
    """
    parts: list[str] = []
    for value in node.values:
        if isinstance(value, ast.Constant):
            parts.append(str(value.value))
        else:
            parts.append("{...}")
    return "".join(parts)


def contains_query_params(node: ast.BinOp) -> bool:
    """Check if binary operation contains query parameters.

    Returns:
        True if query params found, False otherwise.
    """
    if _is_query_param_string(node.left):
        return True
    if _is_query_param_string(node.right):
        return True
    if isinstance(node.left, ast.BinOp) and contains_query_params(node.left):
        return True
    return isinstance(node.right, ast.BinOp) and contains_query_params(node.right)


def _is_query_param_string(node: ast.expr) -> bool:
    """Check if node is a string containing query param characters.

    Args:
        node: AST expression node.

    Returns:
        True if node is a string with ? or &.
    """
    if not isinstance(node, ast.Constant):
        return False
    if not isinstance(node.value, str):
        return False
    return "?" in node.value or "&" in node.value


def matches_pattern(file_path: Path, patterns: list[str]) -> bool:
    """Check if file path matches any of the glob patterns.

    Args:
        file_path: Path to check.
        patterns: List of glob patterns (e.g., "tests/*", "**/__pycache__/*").

    Returns:
        True if file matches any pattern.
    """
    path_str: str = str(file_path)
    for pattern in patterns:
        if fnmatch.fnmatch(path_str, pattern):
            return True
        # Also check just the filename for simple patterns
        if fnmatch.fnmatch(file_path.name, pattern):
            return True
    return False


def find_python_files(
    path: Path,
    exclude_paths: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    skip_dirs: frozenset[str] | None = None,
) -> Iterator[Path]:
    """Find all Python files in path, respecting exclusions.

    Args:
        path: Root path to search.
        exclude_paths: List of paths to exclude (exact match or prefix).
        exclude_patterns: List of glob patterns to exclude.
        skip_dirs: Set of directory names to skip.

    Yields:
        Path objects for each Python file found.
    """
    exclude_paths = exclude_paths or []
    exclude_patterns = exclude_patterns or []
    skip_dirs = skip_dirs or frozenset()

    exclude_resolved: set[Path] = _resolve_exclude_paths(exclude_paths)

    if path.is_file():
        if path.suffix == ".py" and not _is_excluded(path, exclude_resolved, exclude_patterns):
            yield path
    elif path.is_dir():
        yield from _find_in_directory(path, exclude_resolved, exclude_patterns, skip_dirs)


def _resolve_exclude_paths(exclude_paths: list[str]) -> set[Path]:
    """Convert exclude paths to resolved absolute paths.

    Args:
        exclude_paths: List of paths to exclude.

    Returns:
        Set of resolved Path objects.
    """
    exclude_resolved: set[Path] = set()
    for exc_path in exclude_paths:
        exc: Path = Path(exc_path)
        if exc.is_absolute():
            exclude_resolved.add(exc)
        else:
            exclude_resolved.add(Path.cwd() / exc)
    return exclude_resolved


def _is_excluded(file_path: Path, exclude_resolved: set[Path], exclude_patterns: list[str]) -> bool:
    """Check if file should be excluded.

    Args:
        file_path: Path to check.
        exclude_resolved: Set of resolved exclude paths.
        exclude_patterns: List of glob patterns.

    Returns:
        True if file matches exclusion path or pattern.
    """
    resolved: Path = file_path.resolve()
    for excluded_path in exclude_resolved:
        if resolved == excluded_path or resolved.is_relative_to(excluded_path):
            return True
    return matches_pattern(file_path, exclude_patterns)


def _find_in_directory(
    path: Path,
    exclude_resolved: set[Path],
    exclude_patterns: list[str],
    skip_dirs: frozenset[str],
) -> Iterator[Path]:
    """Find Python files in a directory.

    Args:
        path: Directory to search.
        exclude_resolved: Set of resolved exclude paths.
        exclude_patterns: List of glob patterns.
        skip_dirs: Set of directory names to skip.

    Yields:
        Path objects for each Python file found.
    """
    for py_file in path.rglob("*.py"):
        parts: tuple[str, ...] = py_file.parts
        if any(part.startswith(".") or part in skip_dirs for part in parts):
            continue
        if _is_excluded(py_file, exclude_resolved, exclude_patterns):
            continue
        yield py_file
