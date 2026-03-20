[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=bugs)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=coverage)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=SchweizerischeBundesbahnen_python-sbb-polarion&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=SchweizerischeBundesbahnen_python-sbb-polarion)

A Python library for interacting with Polarion requirements management system.
Provides utilities, core API access, extension clients, and testing helpers for SBB Polarion extensions.

## Installation

```bash
# For development
git clone <repository-url>
cd python-sbb-polarion
uv sync --all-extras  # Install all dependencies including dev tools
```

## Quick Start

```python
from python_sbb_polarion.core import PolarionApiV1, ExtensionApiFactory
from python_sbb_polarion.core.base import PolarionRestApiConnection

# Create connection
connection = PolarionRestApiConnection(
    url="https://polarion.example.com",
    token="your-api-token"
)

# Use Polarion REST API v1 (based on Polarion 2512 OpenAPI spec)
api = PolarionApiV1(connection)
workitem = api.get_workitem("PROJECT", "ITEM-123")

# Use extension APIs via factory
pdf_api = ExtensionApiFactory.get_extension_api_by_name(
    "pdf-exporter",
    connection
)
result = pdf_api.convert({"projectId": "PROJECT", "documentName": "doc"})
```

## Polarion REST API

| Class | Description | Status |
|-------|-------------|--------|
| `PolarionApiV1` | Full Polarion REST API v1 (based on Polarion 2512) | **Current** - use this |

**Current version:** Polarion 2512

## Documentation

* Internal documentation: See project wiki

## Project Structure

```
python_sbb_polarion/
├── util/           # Shared utilities (HTTP, SSH, LDAP, SQL, OAuth, mailer, etc.)
├── core/           # Core Polarion API (base classes, main API, factory)
│   └── polarion_api/       # PolarionApiV1 (current, based on Polarion 2512)
│       ├── _documents/     # Document operations
│       ├── _global/        # Global operations (users, enumerations)
│       ├── _plans/         # Plan operations
│       ├── _projects/      # Project operations
│       ├── _testruns/      # Test run operations
│       └── _workitems/     # Work item operations
├── extensions/     # Extension clients for SBB Polarion extensions
│   └── _shared_exporter/  # Shared mixins for PDF and DOCX exporters
├── linter/         # Custom code style linter (PSP001-PSP017)
├── polarion_project_manager/   # Polarion project manager
├── testing/        # Test helpers and utilities for system tests
└── types.py        # Type definitions (JsonDict, MediaType, Header, etc.)

tests/
├── unit/           # Unit tests
└── verification/   # OpenAPI verification tests
```

## Key Modules

- **util** - Reusable utilities: http, ssh, sshtunnel, ldap, sql, oauth, mailer, argparse, environment
- **core** - Core API: `PolarionApiV1`, `PolarionGenericExtensionApi`, `ExtensionApiFactory`
- **extensions** - Client interfaces for SBB Polarion extensions (pdf-exporter, docx-exporter, admin-utility, etc.)
- **linter** - Custom AST-based code style linter (PSP001-PSP017)
- **testing** - Test helpers: `GenericTestCase`, `TestContainersHelper`, `TempProject`
- **types** - Type definitions: `JsonDict`, `MediaType`, `Header`, `AuthScheme`, file upload types

## Development Commands

```bash
# Run tests
uv run tox                    # Run all tests and checks (ruff, mypy, py311, py313, py314)
uv run tox -e py314           # Run unit tests only (Python 3.14)

# Linting and formatting (using Ruff)
uv run ruff check python_sbb_polarion       # Check code quality
uv run ruff format python_sbb_polarion      # Format code
uv run ruff check --fix python_sbb_polarion # Auto-fix issues

# OpenAPI verification
gh auth login                              # One-time GitHub authentication
uv run tox -e verify-openapi-mapping       # Verify extension APIs match upstream

# Build package
uv build
```

## Code Style Linter

This library includes a custom AST-based linter that enforces code style rules beyond ruff/mypy:

- **PSP001**: All local variables must have type annotations
- **PSP002**: `api_request_*` arguments must be variables (not inline dicts/f-strings)
- **PSP003**: URL must be assigned to a variable before passing to API methods
- **PSP004**: Query params must use `params=` dict, not URL concatenation
- **PSP005**: Dict with type annotation must have each key-value pair on separate line
- **PSP006**: Use `HTTPStatus` enum instead of numeric HTTP status codes
- **PSP007**: Use `Header` enum instead of string literals for HTTP headers
- **PSP008**: Use `MediaType` enum instead of string literals for MIME types
- **PSP009**: Use `AuthScheme` enum instead of string literals for auth schemes
- **PSP010**: Don't use quoted type annotations, use `from __future__ import annotations`

```bash
# CLI command (after pip install)
python-sbb-polarion-lint src/
python-sbb-polarion-lint --disable PSP001 src/
python-sbb-polarion-lint --only PSP005 src/

# Or as module
python -m python_sbb_polarion.linter src/
```

Programmatic usage:

```python
from pathlib import Path
from python_sbb_polarion.linter import lint_file

violations = lint_file(Path("my_code.py"))
for v in violations:
    print(v)
```

## Polarion Project Manager

This module provides a command-line interface for downloading, uploading, and creating Polarion project templates through PolarionProjectManager.

The CLI wraps around the core project manager class and exposes three commands:

* download — Retrieve a project template ZIP from Polarion
* create — Create a temporary Polarion project from a template
* upload_template — Upload a local ZIP file as a new template

```bash
# Run as a module
python -m python_sbb_polarion.polarion_project_manager.cli <command> [options]
```

### Download a project template by its project ID

```bash
python -m python_sbb_polarion.polarion_project_manager.cli download --project_id elibrary --project_group "Demo Projects" --output elibrary_st
```

### Parameters
| Parameter       | Default value        | Mandatory   | Description                                        |
|-----------------|----------------------|-------------|----------------------------------------------------|
| --project_id    | -                    | yes         | The ID of the project to download                  |
| --project_group | -                    | no          | The project group identifier                       |
| --output        | {project_id}_remote  | no          | Custom output filename without the .zip extension  |


### Create a temporary project from a template

```bash
python -m python_sbb_polarion.polarion_project_manager.cli create --project_id elibrary_system_test --project_name "Elibrary System Test" --template_id custom_project_template_for_st
```

### Parameters
| Parameter       | Default value                                                | Mandatory | Description                            |
|-----------------|--------------------------------------------------------------|-----------|----------------------------------------|
| --project_id    | -                                                            | yes       | ID for the temporary project           |
| --project_name  | E-Library                                                    | no        | Display name for the temporary project |
| --template_id   | custom_project_template_for_st                               | no        | Template identifier                    |
| --template_path | auto-detected (first .zip in template-dir if not specified)  | no        | Path to the project template zip file  |

### Upload a local ZIP file as a new template

```bash
python -m python_sbb_polarion.polarion_project_manager.cli upload_template --template_id custom_project_template_for_st
```

### Parameters
| Parameter       | Default value                                                | Mandatory | Description                            |
|-----------------|--------------------------------------------------------------|-----------|----------------------------------------|
| --template_id   | custom_project_template_for_st                               | no        | Template identifier                    |
| --template_path | auto-detected (first .zip in template-dir if not specified)  | no        | Path to the project template zip file  |

## Requirements

- Python >=3.11, <3.15
- uv package manager

## License

This project is licensed under the [Apache License 2.0](LICENSE).
