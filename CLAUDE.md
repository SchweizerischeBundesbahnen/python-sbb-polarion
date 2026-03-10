# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`python-sbb-polarion` is a Python library for Polarion requirements management system. It provides utilities, core API access, extension clients, and testing helpers:

- **util** - Shared utilities (HTTP, LDAP, SSH, SQL, OAuth, mailer, argparse, environment, sshtunnel)
- **core** - Base classes and core Polarion API (PolarionApiV1, PolarionGenericExtensionApi, ExtensionApiFactory)
- **extensions** - Extension clients for SBB Polarion extensions
- **linter** - Custom AST-based code style linter (PSP001-PSP017) - can be used by projects that depend on this library
- **testing** - Test helpers and utilities for system tests
- **types** - Type definitions (`JsonDict`, `JsonValue`, `FileUpload`, etc.)

### Polarion REST API

| Class | Description | Status |
|-------|-------------|--------|
| `PolarionApiV1` | Full Polarion REST API v1 (based on Polarion 2512) | **CURRENT** - use this |

**Notes:**
- `PolarionApiV1` provides complete coverage of Polarion REST API v1 endpoints
- OpenAPI spec source: Polarion 2512

**Error Handling Philosophy:**
- Response-based approach - API methods ALWAYS return `Response` (never `None`)
- HTTP status codes (4xx, 5xx) are returned as valid Response objects - check `response.status_code`
- `requests.exceptions.RequestException` is raised ONLY for network/connection errors (timeout, SSL, connection refused)
- Use try/except for network errors, use status code checks for HTTP errors

**JSON:API Sparse Fieldsets:**
- Polarion REST API follows JSON:API spec for sparse fieldsets
- Use `SparseFields` type alias (`dict[str, str]`) for the `fields` parameter
- Format: `{"resource_type": "field1,field2"}` produces `?fields[resource_type]=field1,field2`
- Use `"@all"` to request all fields: `{"workitems": "@all"}`
- Multiple resource types can be specified: `{"workitems": "id,title", "categories": "id,name"}`

```python
from python_sbb_polarion.types import SparseFields

# Get workitem with all fields
fields: SparseFields = {"workitems": "@all"}
response = api.get_workitem("project1", "WI-123", fields=fields)

# Get workitem with specific fields + related resource fields
fields = {
    "workitems": "id,title,description",
    "categories": "id,name",
}
response = api.get_workitem("project1", "WI-123", fields=fields, include="categories")
```

**Simplified Update API:**
- `update_workitem()` accepts `attributes` dict directly (not full JSON:API envelope)
- Method automatically wraps attributes in JSON:API format

```python
# Update workitem - just pass attributes, method wraps in JSON:API format
response = api.update_workitem(
    project_id="project1",
    workitem_id="WI-123",
    attributes={"title": "New Title", "status": {"id": "open"}},
)
# Method sends: {"data": {"type": "workitems", "id": "project1/WI-123", "attributes": {...}}}

# For batch updates, use update_workitems() with full JSON:API format
data: JsonDict = {
    "data": [
        {"type": "workitems", "id": "project1/WI-123", "attributes": {"title": "Title 1"}},
        {"type": "workitems", "id": "project1/WI-456", "attributes": {"title": "Title 2"}},
    ]
}
response = api.update_workitems("project1", data)
```

## Package Manager

This project uses **uv** for dependency management. All dependency operations must use uv commands.

## Development Commands

### Setup and Dependencies
```bash
uv sync                          # Install all dependencies
uv sync --all-extras             # Install with all optional dependencies (including dev)
uv lock                          # Update uv.lock file
uv tree                          # Show dependency tree
```

### Testing
```bash
uv run tox                       # Run all tests and checks (ruff, mypy, py311, py313)
uv run tox -e ruff               # Run only ruff (linting and formatting)
uv run tox -e mypy               # Run only mypy (type checking)
uv run tox -e py311              # Run tests on Python 3.11
uv run tox -e py313              # Run tests on Python 3.13

uv run pytest .                  # Run tests directly
uv run pytest . --junitxml="junittest.xml"  # Run with JUnit XML output
uv run pytest path/to/test_file.py           # Run single test file
uv run pytest path/to/test_file.py::test_function  # Run single test

uv run coverage run --source=python_sbb_polarion --branch -m pytest .  # Run with coverage
uv run coverage report -m        # Display coverage report
uv run coverage xml              # Generate coverage XML
```

### Extension API Verification Tests
```bash
# RECOMMENDED: Use dedicated tox environment (manual/local only)
# Currently uses GitHub as primary source (Polarion endpoint needs investigation)

# Option A: Use .env file (recommended for local development)
cp .env.example .env  # Edit .env and add GitHub token
uv run tox -e verify-openapi-mapping

# Option B: Use GitHub CLI authentication (recommended)
gh auth login  # One-time setup, token auto-detected
uv run tox -e verify-openapi-mapping

# Option C: Export GITHUB_TOKEN manually
export GITHUB_TOKEN="your-github-personal-access-token"
uv run tox -e verify-openapi-mapping

# Direct execution
uv run python -m tests.verification

# Disable parameter validation (method names only)
VALIDATE_PARAMETERS=false uv run tox -e verify-openapi-mapping

# Test single extension
uv run python -m tests.verification --extension pdf-exporter
```

**Important:**
- Located in `tests/verification/` (separate from unit tests in `tests/unit/`)
- Included in standard `uv run tox` test suite
- Can also run separately via `uv run tox -e verify-openapi-mapping`
- Tests FAIL when issues are found (shows detailed JSON report)
- **Current status:**
  - **Primary source:** GitHub repositories (source code - WORKING)
  - **Experimental:** Polarion endpoints (needs investigation - currently returns SSO login pages)

**What it validates:**
- ✅ Python methods exist for each OpenAPI endpoint
- ✅ Method parameters match OpenAPI specifications (names, required/optional)
- ✅ Smart name matching (camelCase → snake_case)
- ✅ Path, query, and body parameters
- ✅ Method naming conventions (verbs, HTTP method correspondence, plural consistency)
- ✅ Orphan annotations (methods annotated but not in OpenAPI)
- ✅ Duplicate annotations (multiple methods for same endpoint)
- ✅ Naming suggestions with `naming_ok=True` to suppress false positives

**See:** `tests/README.md` for comprehensive documentation

## Logging

This library uses Python's standard `logging` module. All print statements have been migrated to logging.

### For Users of the Library

**Basic setup:**
```python
import logging

# Enable INFO level for all python-sbb-polarion modules
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from python_sbb_polarion.core import PolarionApiV1
api = PolarionApiV1(url="...", auth_token="...")
```

**Advanced configuration:**
```python
import logging

# Configure root logger
logging.basicConfig(level=logging.WARNING)

# Enable DEBUG for specific module
logging.getLogger('python_sbb_polarion.extensions.pdf_exporter').setLevel(logging.DEBUG)

# Disable all logging
logging.getLogger('python_sbb_polarion').setLevel(logging.CRITICAL + 1)
```

**Log levels:**
- `DEBUG`: Detailed diagnostic info (execution flow, variable values)
- `INFO`: Successful operations, milestones
- `WARNING`: Unexpected but handled conditions
- `ERROR`: Operation failures

### For Developers

The library includes a `NullHandler` by default, so no output is generated unless users configure logging.

**Best practices:**
- Use lazy formatting: `logger.info("Message %s", var)` not f-strings
- Use appropriate log levels
- Use `logger.exception()` for exception logging (includes stack trace)

### Linting and Formatting
```bash
uv run ruff check python_sbb_polarion      # Check code quality
uv run ruff check --fix python_sbb_polarion  # Auto-fix issues
uv run ruff format python_sbb_polarion     # Format code
uv run ruff format --check python_sbb_polarion  # Check formatting without changes
```

### Custom Code Style Linter (PSP001-PSP017)

This library includes a custom AST-based linter that enforces code style rules beyond ruff/mypy. The linter is included in the published package and can be used by projects that depend on this library.

**Rules:**

| Rule | Description | Test files |
|------|-------------|------------|
| PSP001 | All local variables must have type annotations | ✓ |
| PSP002 | `api_request_*` arguments must be variables (not inline dicts/f-strings) | ✓ |
| PSP003 | URL must be assigned to a variable before passing to API methods | ✓ |
| PSP004 | Query params must use `params=` dict, not URL concatenation | ✓ |
| PSP005 | Dict with type annotation must have each key-value pair on separate line (including nested dicts and dicts in lists for JsonDict) | ✗ (nested check) |
| PSP006 | Use `HTTPStatus` enum instead of numeric codes (`HTTPStatus.OK` not `200`) | ✓ |
| PSP007 | Use `Header` enum instead of string literals (`Header.CONTENT_TYPE`) | ✓ |
| PSP008 | Use `MediaType` enum instead of string literals (`MediaType.JSON`) | ✓ |
| PSP009 | Use `AuthScheme` enum instead of string literals (`AuthScheme.BEARER`) | ✓ |
| PSP010 | Use `from __future__ import annotations` instead of quoted types | ✓ |
| PSP011 | Params/headers/data/files dict must be initialized as `{}`, not `None` | ✓ |
| PSP012 | For `list | None` or `dict | None` use `is not None`, not truthy check | ✓ |
| PSP013 | When passing params/headers to API methods, use `or None` for empty dict | ✓ |
| PSP014 | Don't use `print()` in library code, use `logging` module | ✗ |
| PSP015 | Don't use `assert` in production code | ✗ |
| PSP016 | Don't use `typing.cast()`, use proper type design | ✗ |
| PSP017 | Don't use `Any` in type annotations (use `JsonDict` for `dict[str, Any]`) | ✗ |

**Note:** Rules marked with ✗ in "Test files" column are automatically skipped for files in `tests/` and `testing/` directories.

**CLI Usage:**
```bash
# Basic usage
python-sbb-polarion-lint src/
python -m python_sbb_polarion.linter src/

# Rule filtering
python-sbb-polarion-lint --disable PSP001 src/           # Disable specific rule
python-sbb-polarion-lint --disable PSP001 --disable PSP002 src/  # Disable multiple
python-sbb-polarion-lint --only PSP005 src/              # Check only specific rule

# Path exclusions
python-sbb-polarion-lint --exclude tests/ src/           # Exclude directory
python-sbb-polarion-lint --exclude-pattern '*_test.py' src/  # Exclude by pattern
python-sbb-polarion-lint --exclude-pattern '*_generated.py' --exclude-pattern '*_pb2.py' src/

# Caching (enabled by default)
python-sbb-polarion-lint --no-cache src/    # Disable caching, recheck all files
python-sbb-polarion-lint --clear-cache src/ # Clear cache before running

# Run via tox (for this project)
uv run tox -e python-sbb-polarion-linter
```

**Configuration (pyproject.toml):**
```toml
[tool.python-sbb-polarion-lint]
# Disable specific rules (merged with CLI --disable)
disable = ["PSP001"]

# Only check these rules (CLI --only overrides this completely)
only = []

# Exclude paths from linting (merged with CLI --exclude)
exclude = ["migrations/", "generated/"]

# Exclude files matching glob patterns (merged with CLI --exclude-pattern)
exclude-patterns = ["*_test.py", "*_generated.py", "*_pb2.py"]

# Enable file caching to skip unchanged files (default: true)
cache = true
```

**Configuration Priority:** CLI arguments > pyproject.toml > defaults

**Caching:**
- Cache is stored in `.psp-lint-cache/cache.json` (add to `.gitignore`)
- Uses MD5 hash of file content to detect changes
- Files with violations are not cached (rechecked on next run)
- Cache is automatically invalidated when file content changes

**Programmatic Usage:**
```python
from pathlib import Path
from python_sbb_polarion.linter import (
    lint_file,
    find_python_files,
    LinterConfig,
    LinterCache,
    Violation,
)

# Simple usage
violations = lint_file(Path("my_code.py"))
for v in violations:
    print(v)  # file:line:col: PSP001 message

# With configuration from pyproject.toml
config = LinterConfig.from_pyproject()
print(f"Disabled rules: {config.disable}")
print(f"Excluded paths: {config.exclude}")

# Find files with exclusions
for py_file in find_python_files(
    Path("src/"),
    exclude_paths=["src/generated/"],
    exclude_patterns=["*_test.py"],
):
    violations = lint_file(py_file)
    # process violations...

# With caching
cache = LinterCache(Path(".psp-lint-cache"))
for py_file in find_python_files(Path("src/")):
    if cache.is_unchanged(py_file):
        continue  # Skip unchanged files
    violations = lint_file(py_file)
    if violations:
        cache.invalidate(py_file)
    else:
        cache.update(py_file)
cache.save()
```

**Suppressing Violations:**
```python
# Use psp-ignore comment (different from ruff's noqa to avoid conflicts)
params: dict[str, Any] = {}  # psp-ignore: PSP017 - psycopg2 requires dict[str, Any]

# Multiple codes
data = {...}  # psp-ignore: PSP001, PSP005

# With explanation (text after code is ignored)
value = get_value()  # psp-ignore: PSP001 - type inferred from function
```

**Exit Codes:**
- `0` - No violations found
- `1` - Violations found
- `2` - Error (file not found, parse error, etc.)

### Type Checking
```bash
uv run mypy python_sbb_polarion  # Run type checking
uv run ruff check --select ANN   # Check type annotations
```

**Type checking is MANDATORY for all code:**
- **ALL variables MUST have explicit type annotations** - even when types are obvious
  - `url: str = f"{base}/items"` NOT `url = f"{base}/items"`
  - `headers: dict[str, str] = {...}` NOT `headers = {...}`
  - `params: dict[str, str] = {...}` NOT `params = {...}`
  - `data: JsonDict = {...}` NOT `data = {...}`
- All functions and methods MUST have complete type annotations (parameters and return types)
- Type checking is enforced by pre-commit hooks and CI/CD
- Use `typing` module for complex types: `list`, `dict`, `Mapping`, etc.
- **NO `Any` or `object` types allowed** - use specific types from `python_sbb_polarion.types` module
- **NO `assert` for type narrowing in production code** - use explicit checks with `raise` or proper type design
  - `assert` is OK in test code (tests/unit, tests/verification)
  - In production code, use proper type initialization or explicit runtime checks
- **Response-based error handling** - API methods return `Response` (NOT `| None`)
  - `requests.exceptions.RequestException` raised ONLY for network errors (timeout, SSL, connection refused)
  - HTTP status errors (4xx, 5xx) are returned as Response - check `response.status_code`
  - No need to check for `None` - response is always valid
- **NO quoted types** - use `from __future__ import annotations` instead of string quotes for forward references
  - `var: JsonDict = {}` NOT `var: "JsonDict" = {}`
  - `def func() -> Response:` NOT `def func() -> "Response":`
  - Exception: recursive type definitions in `types.py` (e.g., `list["JsonValue"]`)
- **NO `cast()`** - avoid using `typing.cast()`, instead use proper type design or build typed data structures explicitly
  - Build `JsonDict` explicitly instead of casting `TypedDict` to `JsonDict`
  - Use `@overload` decorators for type-safe factory methods

**Type-Safe Extension API Factory:**

The project uses `@overload` decorators for type-safe factory methods. This provides full IDE autocomplete and mypy type inference without needing `cast()`:

```python
from python_sbb_polarion.testing import GenericTestCase

# ✅ Type-safe - mypy infers PolarionAdminUtilityApi
admin_api = GenericTestCase.create_extension_api("admin-utility")
admin_api.create_project(...)  # Full autocomplete!

# ✅ Type-safe - mypy infers PolarionTestDataApi
test_data = GenericTestCase.create_extension_api("test-data")
test_data.save_project_template(...)  # Full autocomplete!

# ❌ OLD way - don't use cast anymore
from typing import cast
admin_api = cast(PolarionAdminUtilityApi, GenericTestCase.create_extension_api("admin-utility"))
```

**Available extensions** (all with full type support):
- `aad-synchronizer`, `admin-utility`, `api-extender`, `collection-checker`
- `cucumber`, `diff-tool`, `dms-doc-connector`, `dms-wi-connector`
- `docx-exporter`, `excel-importer`, `interceptor-manager`, `json-editor`
- `mailworkflow`, `pdf-exporter`, `requirements-inspector`, `strictdoc-exporter`
- `test-data`

**Type Checking Examples:**
```python
from http import HTTPStatus

from requests import exceptions

# ✅ Correct - complete type annotations, response handling
def fetch_data(project_id: str) -> dict | None:
    """Fetch data from API.

    Returns:
        dict | None: Workitem data if found, None if not found or error

    Raises:
        requests.exceptions.RequestException: Only for network/connection errors
    """
    try:
        response = api.get_workitem(project_id, "WI-123")
        # Check HTTP status code using HTTPStatus enum
        if response.status_code == HTTPStatus.OK:
            return response.json()
        elif response.status_code == HTTPStatus.NOT_FOUND:
            logger.warning("Workitem not found")
            return None
        else:
            logger.error("HTTP error: %s", response.status_code)
            return None
    except exceptions.RequestException as e:
        # Only for network errors (timeout, connection refused, etc.)
        logger.error("Network error: %s", e)
        return None

# ✅ Correct - ALL variables must have explicit type annotations
url: str = f"{base_url}/projects/{project_id}/items"
headers: dict[str, str] = {
    Header.ACCEPT: MediaType.JSON,
}
params: dict[str, str] = {
    "limit": str(100),
}
data: JsonDict = {
    "name": "value",
}

# ✅ Correct - proper type initialization (no Optional needed)
class MyClass:
    def __init__(self, name: str, value: int) -> None:
        self.name: str = name  # Always str, never None
        self.value: int = value  # Always int, never None
        self.optional_field: str | None = None  # Explicitly Optional

# ❌ Wrong - missing type annotations on variables
url = f"{base_url}/items"  # Missing `: str`
headers = {"Accept": "application/json"}  # Missing `: dict[str, str]`
params = {"limit": "100"}  # Missing `: dict[str, str]`

# ❌ Wrong - missing type annotations on functions
def process_data(items, limit):
    return {"count": min(len(items), limit)}

# ❌ Wrong - using assert for type narrowing in production code
def process_item(item: str | None) -> None:
    assert item is not None  # Don't use assert in production!
    print(item.upper())

# ✅ Correct - explicit check with raise
def process_item(item: str | None) -> None:
    if item is None:
        raise ValueError("item cannot be None")
    print(item.upper())

# ❌ Wrong - checking for None (API methods never return None)
response = api.get_workitem(project_id, "WI-123")
if response is None:  # This is dead code - response is always Response
    return
```

### Type System Notes

**Custom Types (`python_sbb_polarion/types.py`):**
- `JsonDict`, `JsonValue`, `JsonPrimitive`, `JsonList` - Required because Python stdlib has no JSON types
- Enables strict "no Any" policy (82 uses across codebase)
- Not reinventing wheel - fills stdlib gap
- `SupportsRead[T]` Protocol - More flexible than `typing.BinaryIO` (requires only `read()` method)
- File upload types (`FileContent`, `FileTuple`, `FilesDict`, `FileUpload`) - Match requests library expectations
- **`FilesDict`** - Use for all `files` parameters in API methods (multipart form data)
- **`SparseFields`** - JSON:API sparse fieldsets (`dict[str, str]`), use for all `fields` parameters
- See `TYPES_ANALYSIS.md` for detailed rationale

**HTTP Constants (StrEnum classes in `python_sbb_polarion/types.py`):**
- `MediaType` - MIME types: `JSON`, `HTML`, `XML`, `PDF`, `PLAIN`, `OCTET_STREAM`, `DOCX`, `ANY`
- `Header` - HTTP headers: `ACCEPT`, `AUTHORIZATION`, `CONTENT_TYPE`, `X_API_KEY`
- `AuthScheme` - Auth schemes: `BEARER`, `BASIC`

```python
from http import HTTPStatus
from python_sbb_polarion.types import Header, MediaType, AuthScheme

# ✅ Use enums instead of string literals
headers = {
    Header.ACCEPT: MediaType.JSON,
    Header.CONTENT_TYPE: MediaType.XML,
}
auth_header = {Header.AUTHORIZATION: f"{AuthScheme.BEARER} {token}"}

# ✅ Use MediaType.ANY for Accept: */*
headers = {
    Header.ACCEPT: MediaType.ANY,
    Header.CONTENT_TYPE: MediaType.HTML,
}

# ✅ Use HTTPStatus instead of numeric codes
if response.status_code == HTTPStatus.OK:
    return response.json()
elif response.status_code == HTTPStatus.NOT_FOUND:
    logger.warning("Resource not found")
    return None

# ❌ Don't use string literals or numeric codes
headers = {"Accept": "application/json"}  # Wrong
headers = {"Accept": "*/*"}  # Wrong - use MediaType.ANY
if response.status_code == 200:  # Wrong
```

**TYPE_CHECKING Pattern:**
- Python 3.13+ supports deferred annotation evaluation (PEP 649)
- Use `if TYPE_CHECKING:` to avoid circular imports (e.g., importing `JsonDict` from `types.py`)
- Don't use for same-file Protocols (unnecessary, adds complexity)
- Example: `admin_utility.py` imports `JsonDict` under `TYPE_CHECKING` to avoid circular dependency

### Pre-commit Hooks
```bash
pre-commit run --all-files       # Run all pre-commit hooks manually
pre-commit install               # Install pre-commit hooks
```

Pre-commit checks include:
- **mypy** - Type checking (enforces type annotations)
- **ruff check** - Code quality, import sorting, type annotations
- **ruff format** - Code formatting
- Standard checks (merge conflicts, trailing whitespace, file format validation)
- uv-lock (keep lock file in sync with pyproject.toml)
- ggshield (secret scanning)

### Building and Publishing
```bash
uv build                         # Build distribution packages (wheel and sdist)
# Publishing is handled automatically by Jenkins CI/CD on git tags
```

**Note:** Version management is synchronized with Git tags in CI/CD. The version in `pyproject.toml` should remain `0.0.0` - versions are set during release by Jenkins.

### Adding Dependencies
```bash
uv add package-name              # Add production dependency
uv add --dev package-name        # Add development dependency
uv remove package-name           # Remove dependency
```

## Code Style Configuration

- **Line Length**: 240 characters (ruff)
- **Linter**: Ruff (replaces black, isort, flake8, pylint, pyupgrade)
- **Rule Selection**: `ALL` with intentional ignores (see `pyproject.toml`)
- **Max Complexity**: 10 (McCabe C901)
- **Type Checking**: ENFORCED - All code must have complete type annotations
  - Checked by: `ruff` (ALL ANN rules) + `mypy` (strict mode)
  - **NO `Any` types allowed** - all types must be specific
  - Pre-commit hooks block commits without proper type hints
- **API Request Style**:
  - All arguments to `api_request_*` methods MUST be variables (no inline dicts or f-strings)
  - URL MUST be assigned to a variable before passing to API methods
  - Query parameters MUST be passed via `params=` dict, NOT concatenated to URL
  - All dicts MUST be defined as variables with type annotations and each key-value pair on its own line (even for single-element dicts)
  - **Standard types for API request arguments:**
    - `headers`: always `dict[str, str]`
    - `params`: always `dict[str, str]`
    - `data`: always `JsonDict` (for JSON request bodies)
    - `files`: always `FilesDict` (for multipart form data)
  ```python
  # ✅ Correct - all arguments are variables with types
  url = f"{self.rest_api_url}/projects/{project_id}/documents"
  headers: dict[str, str] = {
      Header.ACCEPT: MediaType.JSON,
      Header.CONTENT_TYPE: MediaType.JSON,
  }
  params: dict[str, str] = {
      "scope": scope,
      "revision": revision,
  }
  data: JsonDict = {
      "projectId": project_id,
      "documentName": document_name,
  }
  files: FilesDict = {
      "file": (file_name, file_content),
      "mappingName": mapping_name,
  }
  return connection.api_request_post(url, headers=headers, params=params, data=data, files=files)

  # ❌ Wrong - inline dicts in method call
  return connection.api_request_get(url, headers={Header.ACCEPT: MediaType.JSON}, params={"scope": scope})

  # ❌ Wrong - inline URL in method call
  return connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/documents", params=params)

  # ❌ Wrong - URL concatenation for query params
  url += f"?scope={scope}&revision={revision}"
  ```
- **Control Flow**: Explicit `if-else` blocks preferred over ternary operators (SIM108 ignored)
  ```python
  # ✅ Preferred - params with `or None` pattern (converts empty dict to None)
  params: dict[str, str] = {}
  if scope:
      params["scope"] = scope
  if revision:
      params["revision"] = revision
  return self.polarion_connection.api_request_get(url, params=params or None)

  # ✅ Preferred - explicit if-else for type conversions
  ignore_link_roles_list: JsonList | None = None
  if ignore_link_roles is not None:
      ignore_link_roles_list = list(ignore_link_roles)

  # ✅ Dict initialization - multiline format (even for single-element dicts)
  params: dict[str, str] = {
      "scope": scope,
  }

  # ❌ Avoid - ternary operators
  params = {"revision": revision} if revision else None
  ignore_link_roles_list = list(ignore_link_roles) if ignore_link_roles is not None else None
  ```
- **None checks**: Use appropriate check style based on type
  - For `str | None` - use `if var:` (empty string is also falsy, treated as "no value")
  - For `list | None`, `dict | None` - use `if var is not None:` (empty collection is valid value)
  - For `int | None`, `bool | None` - use `if var is not None:` (0 and False are valid values)
  ```python
  # ✅ Correct - str | None with truthy check
  if revision:
      params = {"revision": revision}

  # ✅ Correct - list | None with explicit None check
  if ignore_link_roles is not None:
      ignore_link_roles_list = list(ignore_link_roles)

  # ❌ Wrong - list with truthy check (empty list is valid!)
  if ignore_link_roles:  # Won't process empty list []
      ignore_link_roles_list = list(ignore_link_roles)
  ```
- **Key Ignored Rules**:
  - Documentation rules (D100-D415) - Too verbose for internal tools
  - Complexity metrics (PLR*) - Handle case-by-case with inline `# noqa`
  - SIM108 (if-else-instead-of-ternary) - Explicit if-else preferred for readability
- **Formatter**: Ruff format (Black-compatible)
- **Import Sorting**: Ruff (isort-compatible, Google-style docstrings)
- **NamedTuple/TypedDict naming conventions**:
  - **NamedTuple fields** - always use snake_case (Python PEP 8 convention)
  - **TypedDict fields** - camelCase is allowed when fields match JSON API schema (for `**kwargs: Unpack[...]` pattern)
  - When building `JsonDict` from NamedTuple, map snake_case to camelCase explicitly
  ```python
  # ✅ Correct - NamedTuple with snake_case fields
  class AttachTableParams(NamedTuple):
      object_type: str
      object_id: str
      html_table: str

  # ✅ Correct - explicit mapping to JSON camelCase keys
  data: JsonDict = {
      "objectType": params.object_type,
      "objectId": params.object_id,
      "htmlTable": params.html_table,
  }

  # ✅ Acceptable - TypedDict with camelCase for API kwargs
  class CollectionCheckOptions(TypedDict, total=False):
      ignoreLinkRoles: list[str] | None  # Matches JSON API schema
      ignoreWorkItemIsContainedInMultipleRevisionsErrors: bool

  # ❌ Wrong - NamedTuple with camelCase
  class AttachTableParams(NamedTuple):
      objectType: str  # Should be object_type
  ```

## Extension API Coverage

**API Implementation Status:** 252 annotated methods across all extensions
- All methods have `@restapi_endpoint` annotations for OpenAPI validation
- All methods pass naming convention validation (0 errors, 0 warnings)

Extensions with settings functionality inherit from `PolarionGenericExtensionSettingsApi` mixin which provides generic settings methods:

### Settings Mixin Methods

**Available to extensions that inherit from `PolarionGenericExtensionSettingsApi`:**

Extensions using this mixin: `api-extender`, `diff-tool`, `dms-doc-connector`, `dms-wi-connector`, `docx-exporter`, `excel-importer`, `pdf-exporter`

```python
from python_sbb_polarion.extensions import PolarionPdfExporterApi

# Extensions with settings have these public methods:
api = PolarionPdfExporterApi(connection)

# Get list of available features
response = api.get_features()

# Get setting names for a feature
response = api.get_setting_names(feature="pdf-settings", scope="project/test")

# Get settings content
response = api.get_setting_content(feature="pdf-settings", name="Default")

# Save settings
data = {"key": "value"}
response = api.save_setting(feature="pdf-settings", data=data, name="MyConfig")

# Rename settings
response = api.rename_setting(feature="pdf-settings", name="OldName", new_name="NewName")

# Delete settings
response = api.delete_setting(feature="pdf-settings", name="MyConfig")

# Get defaults
response = api.get_setting_default_content(feature="pdf-settings")

# Get revisions
response = api.get_setting_revisions(feature="pdf-settings", name="Default")
```

**Parameters:**
- `feature` (str): Feature name (e.g., "pdf-settings", "docx-exporter")
- `name` (str): Config name, defaults to "Default"
- `scope` (str | None): Optional scope filter (e.g., "project/test")
- `revision` (str | None): Optional revision for get_setting_content
- `data` (JsonDict): Settings data for save operations
- `new_name` (str): New name for rename operations

**Return:** All methods return `Response` object (never `None`)

### Convenience Wrapper Methods

Extensions provide convenience wrapper methods that delegate to base class settings methods with pre-filled feature names:

```python
# Convenience wrappers (feature is pre-filled)
api.get_style_packages_names(scope="project/test")  # pdf_exporter, docx_exporter
api.get_mapping_names(scope="project/test")          # excel_importer
api.get_diff_settings(name="Default")                # diff_tool

# Equivalent base class calls
api.get_setting_names("style-package", scope="project/test")
api.get_setting_names("mappings", scope="project/test")
api.get_setting_content("diff", name="Default")
```

Wrapper methods have "(convenience wrapper for X)" in their docstrings and are excluded from annotation validation.

## Architecture

The codebase is organized into four main modules:

### Util Module (`python_sbb_polarion/util/`)
Reusable utilities shared across all modules:
- `http.py` - HTTP connection management with auth (Bearer tokens, API keys, basic auth)
- `ssh.py` - SSH connection utilities
- `sshtunnel.py` - SSH tunnel management
- `ldap.py` - LDAP operations
- `sql.py` - SQL database utilities
- `oauth.py` - OAuth authentication
- `mailer.py` - Email utilities
- `argparse.py` - Command-line argument parsing
- `environment.py` - Environment variable management

### Core Module (`python_sbb_polarion/core/`)
Core Polarion API components:
- `base.py` - Base classes: `PolarionGenericExtensionApi`, `PolarionGenericExtensionSettingsApi` (mixin), and `PolarionRestApiConnection`
- `polarion_api/` - `PolarionApiV1` - Full Polarion REST API v1 (based on Polarion 2512 OpenAPI spec)
- `factory.py` - `ExtensionApiFactory` - Factory for creating extension API instances
- `annotations.py` - `@restapi_endpoint` decorator for explicit OpenAPI endpoint mapping

**PolarionApiV1 Structure:**
```
python_sbb_polarion/core/polarion_api/
├── polarion_api_v1.py      # Main class combining all mixins
├── _base.py                # BaseMixin with connection handling
├── _documents/             # Document operations (CRUD, parts, attachments, branching, etc.)
├── _global/                # Global operations (users, enumerations, icons, misc)
├── _plans/                 # Plan operations (CRUD, relationships)
├── _projects/              # Project operations (CRUD, collections, enumerations, icons)
├── _testruns/              # Test run operations (CRUD, records, parameters, step results)
└── _workitems/             # Work item operations (CRUD, attachments, comments, links, etc.)
```

All extension APIs inherit from `PolarionGenericExtensionApi` which provides base HTTP methods and connection management. Extensions with settings endpoints also inherit from `PolarionGenericExtensionSettingsApi` mixin.

### REST API Endpoint Annotations

The `@restapi_endpoint` decorator provides explicit mapping between Python methods and REST API endpoints for OpenAPI validation:

```python
from python_sbb_polarion.core.annotations import restapi_endpoint

@restapi_endpoint(
    method="POST",
    path="/api/projects/{projectId}/documents/{documentName}",
    path_params={"projectId": "project_id", "documentName": "document_name"},
    query_params={"quantity": "quantity"},
    body_param="export_params",
    helper_params=["file_path"],  # Python-only params not in OpenAPI
    required_params=["projectId", "documentName"],
    response_type="binary",
)
def export_document(self, project_id: str, document_name: str, export_params: JsonDict,
                    quantity: int | None = None, file_path: str | None = None) -> Response:
    ...
```

**Decorator parameters:**
- `method`: HTTP method (GET, POST, PUT, PATCH, DELETE)
- `path`: API endpoint path with `{placeholders}` for path parameters
- `path_params`: Mapping of OpenAPI path parameter names to Python parameter names
- `query_params`: Mapping of OpenAPI query parameter names to Python parameter names
- `body_param`: Name of Python parameter containing request body
- `multipart_fields`: Mapping for file uploads
- `header_params`: Mapping of header names to Python parameter names
- `helper_params`: Python-only parameters not in OpenAPI spec (e.g., file paths)
- `required_params`: List of required OpenAPI parameter names
- `response_type`: Expected response type ("json" | "text" | "binary")
- `deprecated`: Whether endpoint is deprecated in OpenAPI spec
- `naming_ok`: Suppress naming validation suggestions for this method (use when method name is intentionally non-standard)

**Suppressing naming suggestions:**

When a method name intentionally doesn't follow naming conventions (e.g., matching external API terminology), use `naming_ok=True` to suppress validation suggestions:

```python
@restapi_endpoint(
    method="GET",
    path="/api/opentext/api/v1/nodes/{nodeId}/output",
    path_params={"nodeId": "nodeId"},
    naming_ok=True,  # Method name is intentionally non-standard
)
def run_web_report(self, node_id: str) -> Response:
    """Run a WebReport - name matches OpenText API terminology."""
    ...
```

### Extensions Module (`python_sbb_polarion/extensions/`)
Client interfaces for SBB Polarion extensions. Each module corresponds to a specific extension from:
`https://github.com/SchweizerischeBundesbahnen/ch.sbb.polarion.extension.*`

**Available extension clients (19 total):**
- **Document Export**: `pdf_exporter.py`, `docx_exporter.py`, `strictdoc_exporter.py`
- **Document Import**: `excel_importer.py`
- **DMS Connectors**: `dms_doc_connector.py`, `dms_wi_connector.py`
- **Administration**: `admin_utility.py`, `aad_synchronizer.py`
- **Tools**: `diff_tool.py`, `api_extender.py`, `json_editor.py`, `xml_repair.py`
- **Testing/Workflows**: `cucumber.py`, `test_data.py`, `fake_services.py`
- **Integration**: `interceptor_manager.py`, `mailworkflow.py`
- **Validation**: `collection_checker.py`, `requirements_inspector.py`

**Shared Mixins (`_shared_exporter/`):**
Common functionality shared between `pdf_exporter` and `docx_exporter`:
- `SharedExporterAttachmentsMixin` - Test run attachment by ID, attachment content
- `SharedExporterConfigurationMixin` - CORS, default settings, DLE toolbar, document properties pane
- `SharedExporterSettingsMixin` - Localization upload/download, style package operations
- `SharedExporterUtilityMixin` - Document collection, link roles, language, webhooks, project name

**Extension Enums (`StrEnum` classes):**

Type-safe enums replace string literals in API methods. All enums are exported from `python_sbb_polarion.extensions`.

*Shared exporter types (`_shared_exporter_types.py`)* - used by pdf-exporter and docx-exporter:
- `DocumentType` - LIVE_DOC, LIVE_REPORT, TEST_RUN, WIKI_PAGE
- `Orientation` - PORTRAIT, LANDSCAPE
- `PaperSize` - A5, A4, A3, B5, B4, JIS_B5, JIS_B4, LETTER, LEGAL, LEDGER
- `Language` - EN, DE, FR, IT
- `ConverterJobStatus` - IN_PROGRESS, SUCCESSFULLY_FINISHED, FAILED, CANCELLED
- `CommentsRenderType` - OPEN, ALL
- `WebhookAuthType` - BEARER_TOKEN, BASIC_AUTH

*PDF-exporter specific (`_pdf_exporter/_types.py`)*:
- `PdfVariant` - PDF_A_1A, PDF_A_1B, PDF_A_2A, PDF_A_2B, PDF_A_2U, PDF_A_3A, PDF_A_3B, PDF_A_3U, PDF_A_4E, PDF_A_4F, PDF_A_4U, PDF_UA_1, PDF_UA_2
- `ImageDensity` - DPI_96, DPI_192, DPI_300, DPI_600

*Collection-checker specific (`_collection_checker/_types.py`)*:
- `ReportFormat` - JSON, TXT

```python
from python_sbb_polarion.extensions import (
    PolarionPdfExporterApi,
    Orientation,
    PaperSize,
    PdfVariant,
)

api = PolarionPdfExporterApi(connection)
response = api.convert_html(
    html="<h1>Hello</h1>",
    orientation=Orientation.LANDSCAPE,
    paper_size=PaperSize.A4,
    pdf_variant=PdfVariant.PDF_A_2B,
)
```

### Testing Module (`python_sbb_polarion/testing/`)
Test helpers for system tests:

- **`generic_test_case.py`** - Base test case class with common test utilities
  - Provides `create_extension_api()` factory method with full type safety via `@overload`
  - All extension APIs have type-safe overloads - no `cast()` needed
  - Example: `admin_api = GenericTestCase.create_extension_api("admin-utility")`

- **`testcontainers_helper.py`** - Docker testcontainers setup for Polarion
  - Manages Docker containers for integration testing

- **`temp_project.py`** - Temporary project management for tests
  - Type-safe design - all required fields are non-Optional
  - Initialized in `__init__`, never `None` after construction
  - No `assert` statements - uses proper type initialization
  - Example:
    ```python
    # All fields are properly typed, no Optional
    temp = TempProject("project_id", "Project Name", "template_id")
    project_id = temp.get_temp_project_id()  # Returns str, not str | None
    ```

## CI/CD (Jenkins)

Pipeline stages:
1. **Setup**: Install uv package manager
2. **Testing**: Run `uv run tox` for all Python versions and linting
3. **SonarQube**: Code quality analysis
4. **Build & Release**:
   - Triggered only on Git tags
   - Automatically sets version from tag name
   - Builds using `uv build`
   - Publishes to private Artifactory PyPI repository using twine

Artifacts archived: `dist/*`, `.coverage`, `coverage.xml`, `junittest.xml`

## Important Notes

- **Pytest ignores**: `python_sbb_polarion/extensions/test_data.py` is excluded from test discovery
- **Python versions**: Support Python >=3.11, <3.14
- **Private PyPI**: Uses a private Artifactory PyPI repository as supplemental package source
- **Private repository config**: Configured in `uv.toml` - authentication via environment variables if needed
- **Paramiko requirement**: When running scripts requiring paramiko, use: `uv run --with paramiko python script.py`
- **Migration**: Project migrated from Poetry to uv - see `UV_MIGRATION.md` for details
- **Test Coverage**: 98% (1254 tests, 154 files with 100% coverage)

## Version Compatibility

| Library Version | Polarion Version | OpenAPI Spec |
|-----------------|------------------|--------------|
| Current | 2512 | `PolarionApiV1` based on 2512 |
