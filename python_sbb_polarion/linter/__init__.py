"""Custom AST-based linter for python-sbb-polarion code style rules.

This module provides code style checking that enforces rules beyond what ruff/mypy can check.
It includes caching for performance and configuration via pyproject.toml.

Rules (PSP001-PSP017):
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
    PSP014: Don't use print() in library code, use logging instead (skipped in tests)
    PSP015: Don't use assert in production code (skipped in tests)
    PSP016: Don't use typing.cast() (skipped in tests)
    PSP017: Don't use Any in type annotations (skipped in tests)

CLI Usage:
    # Basic usage
    python-sbb-polarion-lint src/
    python -m python_sbb_polarion.linter src/

    # Rule filtering
    python-sbb-polarion-lint --disable PSP001 src/
    python-sbb-polarion-lint --only PSP005 src/

    # Path exclusions
    python-sbb-polarion-lint --exclude tests/ src/
    python-sbb-polarion-lint --exclude-pattern '*_test.py' src/

    # Caching
    python-sbb-polarion-lint --no-cache src/     # Disable caching
    python-sbb-polarion-lint --clear-cache src/  # Clear cache first

Configuration (pyproject.toml):
    [tool.python-sbb-polarion-lint]
    disable = ["PSP001"]                    # Disable rules
    only = []                               # Only check these rules
    exclude = ["migrations/"]               # Exclude paths
    exclude-patterns = ["*_generated.py"]   # Exclude glob patterns
    cache = true                            # Enable caching (default)

Programmatic Usage:
    from pathlib import Path
    from python_sbb_polarion.linter import (
        lint_file,
        find_python_files,
        LinterConfig,
        LinterCache,
    )

    # Simple usage
    violations = lint_file(Path("my_file.py"))
    for v in violations:
        print(v)  # file:line:col: PSP001 message

    # Load configuration from pyproject.toml
    config = LinterConfig.from_pyproject()

    # Find files with exclusions
    for py_file in find_python_files(
        Path("src/"),
        exclude_paths=config.exclude,
        exclude_patterns=config.exclude_patterns,
    ):
        violations = lint_file(py_file)

    # With caching
    cache = LinterCache(Path(".psp-lint-cache"))
    for py_file in find_python_files(Path("src/")):
        if cache.is_unchanged(py_file):
            continue
        violations = lint_file(py_file)
        if violations:
            cache.invalidate(py_file)
        else:
            cache.update(py_file)
    cache.save()

Suppressing Violations:
    # Use psp-ignore comment (different from ruff's noqa)
    params: dict[str, Any] = {}  # psp-ignore: PSP017 - reason
    data = {...}  # psp-ignore: PSP001, PSP005

Exit Codes:
    0 - No violations found
    1 - Violations found
    2 - Error (file not found, parse error, etc.)
"""

from python_sbb_polarion.linter.code_style_linter import (
    CodeStyleLinter,
    LinterCache,
    LinterConfig,
    Violation,
    find_python_files,
    lint_file,
    main,
)


__all__ = [
    "CodeStyleLinter",
    "LinterCache",
    "LinterConfig",
    "Violation",
    "find_python_files",
    "lint_file",
    "main",
]
