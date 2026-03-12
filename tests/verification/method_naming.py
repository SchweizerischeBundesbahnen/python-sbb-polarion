"""
Method naming validation for REST API endpoints.

Validates that Python method names follow best practices and match their
corresponding OpenAPI endpoints.

Validation rules:
1. Methods must start with a verb (get, create, save, delete, etc.)
2. HTTP method correspondence (GET → get_, POST → create_/save_, etc.)
3. Plural/singular consistency (endpoint returns list → plural method name)
4. Path keywords should appear in method name
5. No redundant prefixes (class already implies context)
6. Consistent naming patterns across similar endpoints

Usage:
    uv run python -m tests.verification --naming
    uv run python -m tests.verification --naming --extension pdf-exporter
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from python_sbb_polarion.core.annotations import RestApiEndpoint


# =============================================================================
# Constants
# =============================================================================


class ValidationStatus(StrEnum):
    """Validation result status."""

    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUGGESTION = "SUGGESTION"


# Valid starting verbs for method names (grouped by category)
CRUD_VERBS = frozenset({"get", "create", "update", "delete", "save", "remove", "add", "set", "clear", "attach"})
ACTION_VERBS = frozenset({"start", "stop", "cancel", "run", "execute", "trigger", "enable", "disable", "activate", "wait", "promote"})
DATA_VERBS = frozenset({"fetch", "list", "find", "search", "query", "load", "read", "write", "inspect"})
TRANSFER_VERBS = frozenset({"import", "export", "upload", "download", "send", "sync", "push", "pull", "receive"})
TRANSFORM_VERBS = frozenset({"convert", "transform", "parse", "render", "prepare", "generate", "build", "format", "diff", "merge"})
CHECK_VERBS = frozenset({"check", "validate", "verify", "is", "has", "can", "exists", "authenticate"})  # Note: 'test' removed - often noun
SETTINGS_VERBS = frozenset({"persist", "rename", "apply", "reset", "configure", "extend", "change", "modify", "append", "declare"})

ALL_VALID_VERBS = CRUD_VERBS | ACTION_VERBS | DATA_VERBS | TRANSFER_VERBS | TRANSFORM_VERBS | CHECK_VERBS | SETTINGS_VERBS

# HTTP method to expected verb prefix mapping
# Core verbs per HTTP method (based on REST conventions):
#   GET:    get_*, find_*, list_*, search_*, check_*, validate_*
#   POST:   create_*, save_*, start_*, import_*, upload_*, convert_*
#   PUT:    update_*, save_*, replace_*
#   DELETE: delete_*, remove_*, clear_*
HTTP_METHOD_VERBS: dict[str, frozenset[str]] = {
    "GET": frozenset(
        {
            # Core
            "get",
            "find",
            "list",
            "search",
            "fetch",
            "load",
            "read",
            "query",
            # Checks
            "check",
            "validate",
            "is",
            "has",
            "can",
            "exists",
            # Transfer
            "download",
            "export",
            # Domain-specific
            "wait",
            "inspect",
            "prepared",
        }
    ),
    "POST": frozenset(
        {
            # Core
            "create",
            "save",
            "start",
            # Transfer
            "import",
            "upload",
            "export",
            "send",
            "sync",
            "push",
            "receive",
            # Transform
            "convert",
            "generate",
            "prepare",
            "build",
            "diff",
            "merge",
            # Actions
            "run",
            "execute",
            "trigger",
            "apply",
            "activate",
            # CRUD-like
            "add",
            "write",
            "attach",
            "declare",
            "persist",
            "rename",
            "set",
            "cancel",
            # Checks/Search (POST for complex validation/search with body)
            "validate",
            "check",
            "inspect",
            "authenticate",
            "promote",
            "find",
        }
    ),
    "PUT": frozenset({"update", "save", "replace", "set", "write"}),
    "PATCH": frozenset({"update", "patch", "modify", "change", "extend", "append"}),
    "DELETE": frozenset({"delete", "remove", "cancel", "clear", "disable"}),
}

# Words that indicate plural (list) response
PLURAL_INDICATORS = frozenset(
    {
        "names",
        "items",
        "documents",
        "projects",
        "settings",
        "features",
        "jobs",
        "results",
        "attachments",
        "templates",
        "packages",
        "checks",
        "fields",
        "roles",
        "weights",
        "revisions",
        "collections",
        "testruns",
        "webhooks",
        "endpoints",
        "configurations",
        "images",
        "files",
    }
)

# Singular equivalents for plurals
PLURAL_TO_SINGULAR: dict[str, str] = {
    "names": "name",
    "items": "item",
    "documents": "document",
    "projects": "project",
    "settings": "setting",
    "features": "feature",
    "jobs": "job",
    "results": "result",
    "attachments": "attachment",
    "templates": "template",
    "packages": "package",
    "checks": "check",
    "fields": "field",
    "roles": "role",
    "weights": "weight",
    "revisions": "revision",
    "collections": "collection",
    "testruns": "testrun",
    "webhooks": "webhook",
    "images": "image",
    "files": "file",
    "tokens": "token",
    "modules": "module",
    "spaces": "space",
    "licenses": "license",
    "records": "record",
    "exports": "export",
}

# Common abbreviations that should be kept
ABBREVIATIONS = frozenset({"pdf", "html", "xml", "json", "csv", "xlsx", "docx", "api", "dms", "wi", "aad", "cors", "dle", "xliff"})

# Words that are commonly nouns in API context (even though they can be verbs)
# These should not be flagged as "double verbs" when following another verb
NOUN_IN_CONTEXT = frozenset(
    {
        "test",
        "export",
        "import",
        "download",
        "upload",
        "run",
        "check",
        "sync",
        "search",
        "query",
        "report",
        "log",
        "result",
    }
)


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class NamingIssue:
    """Single naming validation issue."""

    status: ValidationStatus
    rule: str
    message: str
    suggestion: str | None = None


@dataclass
class MethodNamingResult:
    """Result of method naming validation."""

    method_name: str
    http_method: str
    path: str
    issues: list[NamingIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if method name is valid (no errors)."""
        return not any(i.status == ValidationStatus.ERROR for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        """Check if there are warnings."""
        return any(i.status == ValidationStatus.WARNING for i in self.issues)

    @property
    def has_suggestions(self) -> bool:
        """Check if there are suggestions."""
        return any(i.status == ValidationStatus.SUGGESTION for i in self.issues)


@dataclass
class ExtensionNamingReport:
    """Complete naming validation report for an extension."""

    extension_name: str
    results: list[MethodNamingResult] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        """Count methods with errors."""
        return sum(1 for r in self.results if not r.is_valid)

    @property
    def warning_count(self) -> int:
        """Count methods with warnings."""
        return sum(1 for r in self.results if r.has_warnings)

    @property
    def suggestion_count(self) -> int:
        """Count methods with suggestions."""
        return sum(1 for r in self.results if r.has_suggestions)

    @property
    def valid_count(self) -> int:
        """Count fully valid methods."""
        return sum(1 for r in self.results if r.is_valid and not r.has_warnings and not r.has_suggestions)


# =============================================================================
# Utility Functions
# =============================================================================


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    # Handle acronyms (e.g., HTMLParser -> html_parser)
    step1: str = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    step2: str = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", step1)
    return step2.lower()


def extract_path_keywords(path: str) -> list[str]:
    """Extract meaningful keywords from endpoint path."""
    # Remove path parameters
    path_clean: str = re.sub(r"\{[^}]+\}", "", path)
    # Remove api prefix
    path_clean = re.sub(r"^/?(api/)?", "", path_clean)
    # Split by / and process each part
    keywords: list[str] = []
    for part in path_clean.split("/"):
        if not part:
            continue
        # Convert camelCase to snake_case (e.g., queueStatistics -> queue_statistics)
        snake_part: str = camel_to_snake(part)
        # Replace kebab-case with underscore (keep as single term, e.g., default-content -> default_content)
        snake_part = snake_part.replace("-", "_")
        # Add as single keyword (don't split further)
        if len(snake_part) > 1 and not snake_part.isdigit():
            keywords.append(snake_part)
    return keywords


def path_returns_list(path: str, http_method: str) -> bool:
    """Determine if endpoint likely returns a list based on path."""
    if http_method != "GET":
        return False

    # If path ends with path parameter like {id}, it returns single item
    if re.search(r"/\{[^}]+\}$", path):
        return False

    # Remove path parameters and check last segment
    path_clean: str = re.sub(r"\{[^}]+\}", "", path).rstrip("/")
    if not path_clean:
        return False

    last_segment: str = path_clean.rsplit("/", maxsplit=1)[-1].replace("-", "_").lower()
    return last_segment in PLURAL_INDICATORS


def get_verb_from_method_name(method_name: str) -> str | None:
    """Extract the verb (first word) from method name."""
    parts: list[str] = method_name.split("_")
    if parts:
        return parts[0].lower()
    return None


def suggest_better_name(method_name: str, http_method: str, path: str, _operation_id: str = "") -> str | None:
    """Suggest a better method name based on endpoint."""
    path_keywords: list[str] = extract_path_keywords(path)

    # Determine appropriate verb based on HTTP method
    verb_map: dict[str, str] = {
        "GET": "get",
        "POST": "create",
        "PUT": "update",
        "PATCH": "update",
        "DELETE": "delete",
    }

    # Special cases for POST
    verb: str
    if http_method == "POST":
        path_lower: str = path.lower()
        if "convert" in path_lower:
            verb = "convert"
        elif "import" in path_lower:
            verb = "import"
        elif "export" in path_lower:
            verb = "export"
        elif "upload" in path_lower:
            verb = "upload"
        elif "start" in path_lower or "jobs" in path_lower:
            verb = "start"
        elif "validate" in path_lower:
            verb = "validate"
        elif "persist" in path_lower:
            verb = "persist"
        else:
            verb = verb_map.get(http_method, "do")
    else:
        verb = verb_map.get(http_method, "do")

    # Check if path returns list
    if path_returns_list(path, http_method) and verb == "get":
        verb = "get"  # Could also suggest "list" but "get" with plural is more common

    # Build suggested name from path keywords
    if path_keywords:
        # Use last 1-3 meaningful keywords
        meaningful_keywords: list[str] = [k for k in path_keywords if k not in {"api", "rest", "v1", "v2"}]
        if meaningful_keywords:
            # Take last 2-3 keywords
            name_parts: list[str] = meaningful_keywords[-3:] if len(meaningful_keywords) > 2 else meaningful_keywords
            suggested: str = f"{verb}_{'_'.join(name_parts)}"
            if suggested != method_name:
                return suggested

    return None


# =============================================================================
# Validation Rules
# =============================================================================


def validate_starts_with_verb(method_name: str) -> NamingIssue | None:
    """Rule 1: Method name must start with a verb."""
    verb: str | None = get_verb_from_method_name(method_name)
    if not verb:
        return NamingIssue(
            status=ValidationStatus.ERROR,
            rule="starts_with_verb",
            message="Method name is empty or invalid",
        )

    if verb not in ALL_VALID_VERBS:
        # Check if it could be a domain noun used as first word
        similar_verbs: list[str] = [v for v in ALL_VALID_VERBS if v.startswith(verb[:2])]
        suggestion: str | None = f"Consider using: {', '.join(sorted(similar_verbs)[:3])}" if similar_verbs else None
        return NamingIssue(
            status=ValidationStatus.WARNING,
            rule="starts_with_verb",
            message=f"Method does not start with a standard verb (got: '{verb}')",
            suggestion=suggestion,
        )
    return None


def validate_http_method_correspondence(method_name: str, http_method: str) -> NamingIssue | None:
    """Rule 2: Method verb should correspond to HTTP method."""
    verb: str | None = get_verb_from_method_name(method_name)
    if not verb:
        return None  # Already caught by starts_with_verb

    expected_verbs: frozenset[str] = HTTP_METHOD_VERBS.get(http_method, frozenset())
    if verb not in expected_verbs:
        # Suggest a better verb based on HTTP method
        suggested_verb: str = _suggest_verb_for_http_method(http_method)
        rest_of_name: str = method_name[len(verb) :]
        suggested_name: str = f"{suggested_verb}{rest_of_name}"
        return NamingIssue(
            status=ValidationStatus.SUGGESTION,
            rule="http_method_correspondence",
            message=f"Verb '{verb}' is unusual for {http_method}",
            suggestion=f"Consider renaming to: {suggested_name}",
        )
    return None


def _suggest_verb_for_http_method(http_method: str) -> str:
    """Suggest the most common verb for a given HTTP method."""
    verb_map: dict[str, str] = {
        "GET": "get",
        "POST": "create",
        "PUT": "update",
        "PATCH": "update",
        "DELETE": "delete",
    }
    return verb_map.get(http_method, "get")


def validate_plural_consistency(method_name: str, path: str, http_method: str) -> NamingIssue | None:
    """Rule 3: Plural consistency - list endpoints should have plural method names."""
    returns_list: bool = path_returns_list(path, http_method)
    path_keywords: list[str] = extract_path_keywords(path)

    if not path_keywords:
        return None

    last_keyword: str = path_keywords[-1]

    # Check if endpoint is plural but method is singular
    if returns_list and last_keyword in PLURAL_INDICATORS and last_keyword not in method_name:
        # Check if method name contains singular form instead of plural
        singular: str = PLURAL_TO_SINGULAR.get(last_keyword, last_keyword.rstrip("s"))
        if singular in method_name:
            # Don't flag if method name already has another plural indicator
            # e.g., get_cover_page_template_names - "names" is already plural
            method_has_plural: bool = any(plural in method_name for plural in PLURAL_INDICATORS)
            if method_has_plural:
                return None
            return NamingIssue(
                status=ValidationStatus.SUGGESTION,
                rule="plural_consistency",
                message=f"Endpoint returns list ({last_keyword}) but method uses singular",
                suggestion=f"Consider using '{last_keyword}' instead of '{singular}'",
            )

    # Check if method is plural but endpoint returns single item
    if not returns_list and http_method == "GET":
        for plural, singular in PLURAL_TO_SINGULAR.items():
            # Check if path also has the singular (e.g., /items/{itemId})
            path_has_singular: bool = f"{{{singular}" in path.lower() or f"/{singular}" in path.lower()
            if plural in method_name and singular not in method_name and not path_has_singular:
                return NamingIssue(
                    status=ValidationStatus.SUGGESTION,
                    rule="plural_consistency",
                    message=f"Method uses plural '{plural}' but endpoint returns single item",
                    suggestion=f"Consider using '{singular}' for single item endpoints",
                )

    return None


def _extract_words_between_api(path: str) -> set[str]:
    """Extract words between /api/.../api/ patterns (e.g., 'opentext' in /api/opentext/api/).

    These are typically service/vendor prefixes, not semantic keywords.
    """
    # Match pattern: /api/{word}/api/ - word between two api segments
    matches: list[str] = re.findall(r"/api/([^/]+)/api/", path)
    return {m.lower() for m in matches}


def validate_path_keywords_present(method_name: str, path: str) -> NamingIssue | None:
    """Rule 4: Key path segments should appear in method name."""
    path_keywords: list[str] = extract_path_keywords(path)

    if not path_keywords:
        return None

    # Get words between /api/.../api/ patterns (vendor prefixes like 'opentext')
    vendor_prefixes: set[str] = _extract_words_between_api(path)

    # Get meaningful keywords (exclude common/generic ones)
    # 'api', 'rest' - just URL prefixes, not semantic
    # 'settings', 'projects', 'testruns' etc. - often contextual and implied by class
    common_generic: set[str] = {
        "api",
        "rest",
        "v1",
        "v2",
        "v3",  # URL prefixes
        "id",
        "content",
        "names",
        "status",
        "result",  # Generic suffixes
        "settings",
        "projects",
        "testruns",
        "attachments",
        "configuration",  # Contextual
    }
    # Also exclude vendor prefixes found between /api/.../api/
    common_generic |= vendor_prefixes
    meaningful: list[str] = [k for k in path_keywords if k not in common_generic]

    if not meaningful:
        return None

    # Check if at least one meaningful keyword appears in method name
    method_lower: str = method_name.lower()

    def keyword_matches(keyword: str) -> bool:
        """Check if keyword or its singular form is in method name."""
        if keyword in method_lower or keyword.replace("_", "") in method_lower:
            return True
        # Check singular form (tokens -> token, documents -> document)
        singular: str = PLURAL_TO_SINGULAR.get(keyword, keyword.rstrip("s"))
        return singular in method_lower

    found_keywords: list[str] = [k for k in meaningful if keyword_matches(k)]

    if not found_keywords:
        # Only report if there are important keywords missing (longer than 5 chars)
        important_missing: list[str] = [k for k in meaningful if len(k) > 5]
        if important_missing:
            # Generate suggested method name by replacing last part with missing keyword
            parts: list[str] = method_name.split("_")
            verb: str = parts[0] if parts else "get"
            missing_kw: str = important_missing[0]
            # Keep verb and middle parts, replace last with missing keyword
            suggested_name: str
            if len(parts) > 2:
                suggested_name = f"{verb}_{'_'.join(parts[1:-1])}_{missing_kw}"
            else:
                suggested_name = f"{verb}_{missing_kw}"
            return NamingIssue(
                status=ValidationStatus.SUGGESTION,
                rule="path_keywords",
                message=f"Method name missing path keywords: {important_missing[:3]}",
                suggestion=f"Consider renaming to: {suggested_name}",
            )

    return None


def validate_consistent_verbs(_method_name: str, _similar_methods: list[str]) -> NamingIssue | None:
    """Rule 6: Consistent verb usage across similar endpoints."""
    # This is a more complex check that requires context from other methods
    # For now, we skip this as it needs aggregate analysis
    return None


def validate_naming_length(method_name: str) -> NamingIssue | None:
    """Rule 7: Method name should not be too short or too long."""
    if len(method_name) < 4:
        return NamingIssue(
            status=ValidationStatus.WARNING,
            rule="naming_length",
            message=f"Method name is too short ({len(method_name)} chars)",
            suggestion="Consider a more descriptive name",
        )

    if len(method_name) > 50:
        return NamingIssue(
            status=ValidationStatus.WARNING,
            rule="naming_length",
            message=f"Method name is very long ({len(method_name)} chars)",
            suggestion="Consider a shorter, more concise name",
        )

    return None


def validate_no_double_verbs(method_name: str) -> NamingIssue | None:
    """Rule 8: Method name should not have consecutive verbs."""
    parts: list[str] = method_name.split("_")
    if len(parts) >= 2:
        verb1: str = parts[0]
        verb2: str = parts[1]
        # Only flag if second word is a verb AND not commonly used as noun in API context
        if verb1 in ALL_VALID_VERBS and verb2 in ALL_VALID_VERBS and verb2 not in NOUN_IN_CONTEXT:
            return NamingIssue(
                status=ValidationStatus.SUGGESTION,
                rule="no_double_verbs",
                message=f"Method has consecutive verbs: '{verb1}_{verb2}'",
                suggestion=f"Consider using just '{verb1}' or '{verb2}'",
            )
    return None


def validate_underscore_consistency(method_name: str) -> NamingIssue | None:
    """Rule 9: Check for inconsistent underscore usage."""
    # Check for double underscores
    if "__" in method_name:
        return NamingIssue(
            status=ValidationStatus.WARNING,
            rule="underscore_consistency",
            message="Method name contains double underscores",
            suggestion="Use single underscores to separate words",
        )

    # Check for mixed camelCase and snake_case
    if re.search(r"[a-z][A-Z]", method_name):
        return NamingIssue(
            status=ValidationStatus.ERROR,
            rule="underscore_consistency",
            message="Method name mixes camelCase with snake_case",
            suggestion=f"Use pure snake_case: {camel_to_snake(method_name)}",
        )

    return None


# =============================================================================
# Main Validation Function
# =============================================================================


def validate_method_naming(
    method_name: str,
    endpoint_metadata: RestApiEndpoint,
) -> MethodNamingResult:
    """
    Validate method naming against best practices.

    Args:
        method_name: Python method name
        endpoint_metadata: RestApiEndpoint metadata from @restapi_endpoint decorator

    Returns:
        MethodNamingResult with all validation issues
    """
    result = MethodNamingResult(
        method_name=method_name,
        http_method=endpoint_metadata.method,
        path=endpoint_metadata.path,
    )

    # Skip naming validation if naming_ok=True is set in decorator
    if endpoint_metadata.naming_ok:
        result.issues.append(
            NamingIssue(
                status=ValidationStatus.OK,
                rule="all",
                message="Method naming explicitly marked as OK (naming_ok=True)",
            )
        )
        return result

    # Run all validation rules
    validators: list[Any] = [
        lambda: validate_starts_with_verb(method_name),
        lambda: validate_http_method_correspondence(method_name, endpoint_metadata.method),
        lambda: validate_plural_consistency(method_name, endpoint_metadata.path, endpoint_metadata.method),
        lambda: validate_path_keywords_present(method_name, endpoint_metadata.path),
        lambda: validate_naming_length(method_name),
        lambda: validate_no_double_verbs(method_name),
        lambda: validate_underscore_consistency(method_name),
    ]

    for validator in validators:
        issue: NamingIssue | None = validator()
        if issue:
            result.issues.append(issue)

    # If no issues, mark as OK
    if not result.issues:
        result.issues.append(
            NamingIssue(
                status=ValidationStatus.OK,
                rule="all",
                message="Method naming follows best practices",
            )
        )

    return result


def validate_extension_naming(extension_name: str) -> ExtensionNamingReport:
    """
    Validate all method names in an extension.

    Args:
        extension_name: Python module name (e.g., 'pdf_exporter')

    Returns:
        ExtensionNamingReport with results for all methods
    """
    from .openapi_utils import extract_annotated_methods

    report: ExtensionNamingReport = ExtensionNamingReport(extension_name=extension_name)

    # Get annotated methods
    annotated_methods: dict[str, Any] = extract_annotated_methods(extension_name)

    if not annotated_methods:
        return report

    for method_name, method_data in annotated_methods.items():
        metadata: RestApiEndpoint = method_data["metadata"]
        result: MethodNamingResult = validate_method_naming(
            method_name=method_name,
            endpoint_metadata=metadata,
        )
        report.results.append(result)

    return report


# =============================================================================
# Report Formatting
# =============================================================================


def format_naming_report(report: ExtensionNamingReport, verbose: bool = False) -> str:
    """
    Format naming validation report as human-readable string.

    Args:
        report: ExtensionNamingReport to format
        verbose: Include OK methods in output

    Returns:
        Formatted report string
    """
    lines: list[str] = []
    lines.append(f"\n{'=' * 80}")
    lines.append(f"Method Naming Report: {report.extension_name}")
    lines.append(f"{'=' * 80}")

    # Summary
    total: int = len(report.results)
    lines.append(f"\nSummary: {total} methods analyzed")
    lines.append(f"  ✅ Valid:       {report.valid_count}")
    lines.append(f"  ⚠️  Warnings:    {report.warning_count}")
    lines.append(f"  💡 Suggestions: {report.suggestion_count}")
    lines.append(f"  ❌ Errors:      {report.error_count}")

    # Details
    if report.results:
        lines.append(f"\n{'-' * 80}")
        lines.append("Details:")
        lines.append(f"{'-' * 80}")

        for result in sorted(report.results, key=lambda r: (r.is_valid, not r.has_warnings, r.method_name)):
            # Skip OK methods unless verbose
            if result.is_valid and not result.has_warnings and not result.has_suggestions and not verbose:
                continue

            lines.append(f"\n📌 {result.method_name}")
            lines.append(f"   Endpoint: {result.http_method} {result.path}")

            for issue in result.issues:
                if issue.status == ValidationStatus.OK:
                    if verbose:
                        lines.append(f"   ✅ {issue.message}")
                elif issue.status == ValidationStatus.ERROR:
                    lines.append(f"   ❌ [{issue.rule}] {issue.message}")
                elif issue.status == ValidationStatus.WARNING:
                    lines.append(f"   ⚠️  [{issue.rule}] {issue.message}")
                else:
                    lines.append(f"   💡 [{issue.rule}] {issue.message}")

                if issue.suggestion:
                    lines.append(f"      → {issue.suggestion}")

    return "\n".join(lines)


def format_naming_report_json(report: ExtensionNamingReport) -> dict[str, object]:
    """
    Format naming validation report as JSON-serializable dict.

    Args:
        report: ExtensionNamingReport to format

    Returns:
        Dictionary representation of the report
    """
    return {
        "extension": report.extension_name,
        "summary": {
            "total": len(report.results),
            "valid": report.valid_count,
            "warnings": report.warning_count,
            "suggestions": report.suggestion_count,
            "errors": report.error_count,
        },
        "methods": [
            {
                "name": r.method_name,
                "http_method": r.http_method,
                "path": r.path,
                "is_valid": r.is_valid,
                "issues": [
                    {
                        "status": i.status.value,
                        "rule": i.rule,
                        "message": i.message,
                        "suggestion": i.suggestion,
                    }
                    for i in r.issues
                ],
            }
            for r in report.results
        ],
    }
