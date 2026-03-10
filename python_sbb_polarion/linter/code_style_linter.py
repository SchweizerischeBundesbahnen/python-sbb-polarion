"""Custom AST-based linter for python-sbb-polarion code style rules.

This linter enforces code style rules that cannot be checked by ruff or mypy.
It includes file caching for performance and configuration via pyproject.toml.

Rules:
    PSP001: All local variables must have type annotations
    PSP002: api_request_* arguments must be variables (not inline dicts/f-strings)
    PSP003: URL must be assigned to a variable before passing to API methods
    PSP004: Query params must use params= dict, not URL concatenation
    PSP005: Dict with type annotation must have each key-value pair on separate line
           (includes nested dicts and dicts in lists for JsonDict typed variables)
    PSP006: Use HTTPStatus enum instead of numeric HTTP status codes
    PSP007: Use Header enum instead of string literals for HTTP headers
    PSP008: Use MediaType enum instead of string literals for MIME types
    PSP009: Use AuthScheme enum instead of string literals for auth schemes
    PSP010: Use `from __future__ import annotations` instead of quoted types
    PSP011: Params/headers/data/files dict must be initialized as `{}`, not `None`
    PSP012: For `list | None` or `dict | None` use `is not None`, not truthy check
    PSP013: When passing params/headers to API methods, use `or None` for empty dict
    PSP014: Don't use print() in library code (skipped in tests/)
    PSP015: Don't use assert in production code (skipped in tests/)
    PSP016: Don't use typing.cast() (skipped in tests/)
    PSP017: Don't use Any in type annotations (skipped in tests/)

Usage:
    python-sbb-polarion-lint src/
    python-sbb-polarion-lint --disable PSP001 src/
    python-sbb-polarion-lint --only PSP005 src/
    python-sbb-polarion-lint --exclude tests/ --exclude-pattern '*_test.py' src/
    python-sbb-polarion-lint --no-cache src/
    python-sbb-polarion-lint --clear-cache src/

Configuration (pyproject.toml):
    [tool.python-sbb-polarion-lint]
    disable = ["PSP001"]
    exclude = ["migrations/"]
    exclude-patterns = ["*_generated.py"]
    cache = true

Suppressing violations:
    # psp-ignore: PSP017 - reason
    # psp-ignore: PSP001, PSP005

Exit codes:
    0 - No violations found
    1 - Violations found
    2 - Error (file not found, parse error, etc.)
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path
from typing import TYPE_CHECKING

# Import from submodules
from ._cache import CACHE_FILE, LinterCache
from ._config import LinterConfig
from ._helpers import (
    contains_query_params as _contains_query_params,
)
from ._helpers import (
    find_python_files,
)
from ._helpers import (
    get_method_name as _get_method_name,
)
from ._helpers import (
    matches_pattern as _matches_pattern,
)
from ._helpers import (
    reconstruct_fstring as _reconstruct_fstring,
)
from ._violation import Violation
from ._visitor import CodeStyleLinter


if TYPE_CHECKING:
    from collections.abc import Sequence


# Cache file location (relative to pyproject.toml or current directory)
CACHE_DIR: str = ".psp-lint-cache"

# Re-export for backward compatibility
__all__ = [
    "CACHE_DIR",
    "CACHE_FILE",
    "CodeStyleLinter",
    "LinterCache",
    "LinterConfig",
    "Violation",
    "_contains_query_params",
    "_get_method_name",
    "_matches_pattern",
    "_reconstruct_fstring",
    "find_python_files",
    "lint_file",
    "main",
]


def lint_file(file_path: Path) -> list[Violation]:
    """Lint a single Python file.

    Returns:
        List of violations found in the file.
    """
    try:
        source: str = file_path.read_text(encoding="utf-8")
        source_lines: list[str] = source.splitlines()
        tree: ast.AST = ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        return [
            Violation(
                file=file_path,
                line=e.lineno or 1,
                col=e.offset or 0,
                code="E999",
                message=f"SyntaxError: {e.msg}",
            )
        ]
    except OSError as e:
        return [
            Violation(
                file=file_path,
                line=1,
                col=0,
                code="E902",
                message=f"IOError: {e}",
            )
        ]

    linter: CodeStyleLinter = CodeStyleLinter(file_path, source_lines)
    linter.visit(tree)
    return linter.violations


def _process_file(
    py_file: Path,
    cache: LinterCache | None,
    config: LinterConfig,
) -> tuple[list[Violation], bool]:
    """Process a single file and return violations.

    Returns:
        Tuple of (filtered violations list, was_skipped boolean).
    """
    if cache is not None and cache.is_unchanged(py_file):
        return [], True

    violations: list[Violation] = lint_file(py_file)
    file_violations: list[Violation] = _filter_violations(violations, config)

    if file_violations:
        if cache is not None:
            cache.invalidate(py_file)
    elif cache is not None:
        cache.update(py_file)

    return file_violations, False


def _filter_violations(violations: list[Violation], config: LinterConfig) -> list[Violation]:
    """Filter violations by config rules.

    Returns:
        List of violations after filtering by config.
    """
    filtered: list[Violation] = []
    for violation in violations:
        if config.only and violation.code not in config.only:
            continue
        if violation.code in config.disable:
            continue
        filtered.append(violation)
    return filtered


def _setup_cache(config: LinterConfig, clear_cache: bool) -> LinterCache | None:
    """Setup cache based on config.

    Returns:
        LinterCache instance if caching is enabled, None otherwise.
    """
    if not config.cache:
        return None
    cache_dir: Path = Path.cwd() / CACHE_DIR
    cache: LinterCache = LinterCache(cache_dir)
    if clear_cache and cache.cache_file.exists():
        cache.cache_file.unlink()
        cache = LinterCache(cache_dir)
    return cache


def _print_summary(violations: list[Violation], files_checked: int, files_skipped: int) -> None:
    """Print summary of linting results."""
    if violations:
        sys.stdout.write(f"\nFound {len(violations)} violation(s)")
        if files_skipped > 0:
            sys.stdout.write(f" (checked {files_checked} files, skipped {files_skipped} cached)")
        sys.stdout.write("\n")
    else:
        msg: str = "No violations found"
        if files_skipped > 0:
            msg += f" (checked {files_checked} files, skipped {files_skipped} cached)"
        sys.stdout.write(f"{msg}\n")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the linter on specified paths.

    Configuration is loaded from pyproject.toml [tool.python-sbb-polarion-lint] section.
    CLI arguments override configuration file settings.

    Args:
        argv: Command line arguments. If None, uses sys.argv.

    Returns:
        Exit code: 0 if no violations, 1 if violations found, 2 on error.
    """
    args: argparse.Namespace = _parse_args(argv)
    config: LinterConfig = _build_config(args)
    cache: LinterCache | None = _setup_cache(config, args.clear_cache)

    all_violations: list[Violation] = []
    files_checked: int = 0
    files_skipped: int = 0

    for path_str in args.paths:
        path: Path = Path(path_str)
        if not path.exists():
            sys.stderr.write(f"Error: Path does not exist: {path}\n")
            return 2

        for py_file in find_python_files(path, config.exclude, config.exclude_patterns):
            file_violations: list[Violation]
            was_skipped: bool
            file_violations, was_skipped = _process_file(py_file, cache, config)
            if was_skipped:
                files_skipped += 1
            else:
                files_checked += 1
                all_violations.extend(file_violations)

    if cache is not None:
        cache.save()

    all_violations.sort(key=lambda v: (str(v.file), v.line, v.col))

    for violation in all_violations:
        sys.stdout.write(f"{violation}\n")

    _print_summary(all_violations, files_checked, files_skipped)

    return 1 if all_violations else 0


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments namespace.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Custom code style linter for python-sbb-polarion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Paths to lint (default: current directory)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Show fix suggestions (does not modify files)",
    )
    parser.add_argument(
        "--disable",
        action="append",
        default=[],
        help="Disable specific rules (e.g., --disable PSP001)",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Only check specific rules (e.g., --only PSP001)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Exclude paths from linting (e.g., --exclude tests/)",
    )
    parser.add_argument(
        "--exclude-pattern",
        action="append",
        default=[],
        help="Exclude files matching glob pattern (e.g., --exclude-pattern '*_test.py')",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching (recheck all files)",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the cache before running",
    )
    return parser.parse_args(argv)


def _build_config(args: argparse.Namespace) -> LinterConfig:
    """Build configuration from pyproject.toml and CLI args.

    Returns:
        LinterConfig with merged settings.
    """
    base_config: LinterConfig = LinterConfig.from_pyproject()
    return base_config.merge_cli(
        disable=set(args.disable),
        only=set(args.only),
        exclude=args.exclude,
        exclude_patterns=args.exclude_pattern,
        cache=False if args.no_cache else None,
    )


if __name__ == "__main__":
    sys.exit(main())
