"""
Base class for extension API verification tests.
"""

import json
import logging
import unittest
from typing import Any, ClassVar

import requests

from .config import EXTENSION_MAPPING
from .method_naming import ExtensionNamingReport, validate_extension_naming
from .openapi_utils import (
    OpenAPIFetchError,
    extract_annotated_methods,
    extract_api_endpoints,
    extract_unannotated_api_methods,
    validate_annotation_against_openapi,
    validate_implementation_http_method,
)


# Configure logging for tests
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class BaseExtensionAPIVerificationTest(unittest.TestCase):
    """
    Base class for extension API verification tests.

    Provides common verification logic used by both GitHub-based and live Polarion tests.
    Subclasses must implement:
        - _fetch_openapi_spec(): Fetch OpenAPI spec for an extension
        - _get_report_metadata(): Return metadata for the JSON report

    Subclasses should override:
        - skip_extensions: List of extension names to skip for this test type
    """

    # Extensions to skip - override in subclasses
    skip_extensions: ClassVar[list[str]] = []

    def _fetch_openapi_spec(self, extension_name: str, repo_name: str) -> dict[str, Any] | None:
        """
        Fetch OpenAPI spec for an extension. Must be implemented by subclasses.

        Args:
            extension_name: Python module name (e.g., 'pdf_exporter')
            repo_name: Repository/extension name in kebab-case (e.g., 'pdf-exporter')

        Returns:
            OpenAPI specification as dictionary, or None if not available
        """
        raise NotImplementedError("Subclasses must implement _fetch_openapi_spec")

    def _get_report_metadata(self, extension_name: str, repo_name: str) -> dict[str, str]:
        """
        Get metadata for the JSON report. Must be implemented by subclasses.

        Args:
            extension_name: Python module name
            repo_name: Repository/extension name

        Returns:
            Dictionary with report metadata (source, url, etc.)
        """
        raise NotImplementedError("Subclasses must implement _get_report_metadata")

    def _get_report_title(self, extension_name: str) -> str:
        """Get title for the report output. Can be overridden by subclasses."""
        return f"OpenAPI Verification Report: {extension_name}"

    def _verify_extension(self, extension_name: str) -> None:
        """
        Core verification logic for an extension.

        Args:
            extension_name: Python module name (e.g., 'pdf_exporter')

        Raises:
            AssertionError: If extension is missing methods for API endpoints
        """
        # Skip if extension is in skip list
        if extension_name in self.skip_extensions:
            self.skipTest(f"Extension '{extension_name}' is in skip_extensions list")

        # Get repo name
        repo_name: str | None = EXTENSION_MAPPING.get(extension_name)
        if not repo_name:
            self.fail(f"No repository mapping found for extension '{extension_name}'")

        # Fetch OpenAPI spec (implementation depends on subclass)
        try:
            openapi_spec: dict[str, Any] | None = self._fetch_openapi_spec(extension_name, repo_name)
        except OpenAPIFetchError as e:
            self.skipTest(str(e))
        except requests.exceptions.RequestException as e:
            self.skipTest(f"Could not fetch OpenAPI spec: {e}")

        if not openapi_spec:
            self.skipTest(f"No OpenAPI spec found for extension '{extension_name}' (repo: {repo_name})")

        # Extract API endpoints from OpenAPI spec
        endpoints: list[dict[str, Any]] = extract_api_endpoints(openapi_spec)
        if not endpoints:
            self.skipTest(f"No endpoints found in OpenAPI spec for extension '{extension_name}'")

        # Extract annotated methods (with @restapi_endpoint decorator)
        annotated_methods: dict[str, Any] = extract_annotated_methods(extension_name)
        logger.info("Found %d annotated methods in %s", len(annotated_methods), extension_name)

        # Compare endpoints with annotated Python methods (exact match only)
        missing_methods: list[dict[str, Any]] = []
        implemented_methods: dict[str, dict[str, Any]] = {}
        annotation_issues: list[dict[str, Any]] = []

        # Track which endpoints are covered and by which methods (to detect duplicates)
        endpoint_to_methods: dict[str, list[str]] = {}  # "METHOD /path" -> [method_names]

        # Match annotated methods by exact method+path
        matched_endpoints: set[int] = set()
        for method_name, annotation_data in annotated_methods.items():
            endpoint_key: str = f"{annotation_data['method']} {annotation_data['path']}"

            # Track all methods that annotate this endpoint
            if endpoint_key not in endpoint_to_methods:
                endpoint_to_methods[endpoint_key] = []
            endpoint_to_methods[endpoint_key].append(method_name)

            matching_endpoint: dict[str, Any] | None = None
            for idx, endpoint in enumerate(endpoints):
                if endpoint["method"] == annotation_data["method"] and endpoint["path"] == annotation_data["path"]:
                    matching_endpoint = endpoint
                    matched_endpoints.add(idx)
                    break

            if matching_endpoint is not None:
                validation_errors: list[str] = validate_annotation_against_openapi(method_name, annotation_data, matching_endpoint)

                # Validate that api_request_* call matches annotated HTTP method
                impl_error: str | None = validate_implementation_http_method(annotation_data["func"], annotation_data["method"])
                if impl_error:
                    validation_errors.append(impl_error)

                if validation_errors:
                    annotation_issues.append({"method": method_name, "annotation": annotation_data, "endpoint": matching_endpoint, "errors": validation_errors})
                else:
                    implemented_methods[method_name] = matching_endpoint
            else:
                orphan_errors: list[str] = [f"ORPHAN ANNOTATION: Method '{method_name}' has @restapi_endpoint({annotation_data['method']} {annotation_data['path']}) but this endpoint does NOT exist in OpenAPI spec"]

                # Still validate implementation HTTP method for orphan annotations
                impl_error2: str | None = validate_implementation_http_method(annotation_data["func"], annotation_data["method"])
                if impl_error2:
                    orphan_errors.append(impl_error2)

                annotation_issues.append(
                    {
                        "method": method_name,
                        "annotation": annotation_data,
                        "endpoint": None,
                        "errors": orphan_errors,
                    }
                )

        # Check for duplicate annotations (multiple methods annotated for same endpoint)
        for endpoint_key, methods in endpoint_to_methods.items():
            if len(methods) > 1:
                for method_name in methods:
                    annotation_issues.append(
                        {
                            "method": method_name,
                            "annotation": annotated_methods[method_name],
                            "endpoint": None,
                            "errors": [f"DUPLICATE ANNOTATION: Endpoint '{endpoint_key}' is annotated by multiple methods: {methods}. Each endpoint should have exactly one @restapi_endpoint."],
                        }
                    )

        # Check for unmatched OpenAPI endpoints (missing @restapi_endpoint annotations)
        for idx, endpoint in enumerate(endpoints):
            if idx in matched_endpoints:
                continue

            path: str = endpoint["path"]
            method: str = endpoint["method"]
            operation_id: str = endpoint["operation_id"]
            params: dict[str, Any] = endpoint["parameters"]

            missing_info: dict[str, Any] = {
                "http_method": method,
                "path": path,
                "operation_id": operation_id,
                "parameters": {
                    "path_params": params["path_params"],
                    "query_params": params["query_params"],
                    "required_params": list(params["required_params"]),
                    "all_params": list(params["all_params"]),
                    "body_schema": params["body_schema"],
                },
            }
            missing_methods.append(missing_info)

        # Check for API-like methods in extension class that lack @restapi_endpoint
        unannotated_methods: list[str] = extract_unannotated_api_methods(extension_name)
        for method_name in unannotated_methods:
            annotation_issues.append(
                {
                    "method": method_name,
                    "annotation": {"method": "UNKNOWN", "path": "UNKNOWN"},
                    "endpoint": None,
                    "errors": [f"MISSING ANNOTATION: Method '{method_name}' looks like an API method but lacks @restapi_endpoint decorator"],
                }
            )

        # Build report
        total_issues: int = len(missing_methods) + len(annotation_issues)

        # Get report metadata from subclass
        report_metadata: dict[str, str] = self._get_report_metadata(extension_name, repo_name)

        report: dict[str, Any] = {
            "extension": extension_name,
            **report_metadata,
            "summary": {
                "total_issues": total_issues,
                "total_openapi_endpoints": len(endpoints),
                "missing_annotations": len(missing_methods),
                "annotation_issues": len(annotation_issues),
                "implemented_methods": len(implemented_methods),
                "annotated_methods": len(annotated_methods),
            },
            "missing_annotations": missing_methods,
            "annotation_issues": [
                {
                    "method": ann_issue["method"],
                    "annotation": {"method": ann_issue["annotation"]["method"], "path": ann_issue["annotation"]["path"]},
                    "openapi_endpoint": {"method": ann_issue["endpoint"]["method"], "path": ann_issue["endpoint"]["path"], "operation_id": ann_issue["endpoint"]["operation_id"]} if ann_issue["endpoint"] else None,
                    "errors": ann_issue["errors"],
                }
                for ann_issue in annotation_issues
            ],
            "implemented_methods": sorted(implemented_methods.keys()),
        }

        # Validate method naming conventions
        naming_report: ExtensionNamingReport = validate_extension_naming(extension_name)
        naming_errors: int = naming_report.error_count
        naming_warnings: int = naming_report.warning_count

        naming_suggestions: int = naming_report.suggestion_count

        if naming_errors > 0 or naming_warnings > 0 or naming_suggestions > 0:
            naming_issues_detail: list[dict[str, Any]] = []
            for result in naming_report.results:
                if not result.is_valid or result.has_warnings or result.has_suggestions:
                    issues_with_suggestions: list[str] = []
                    for issue in result.issues:
                        if issue.suggestion:
                            issues_with_suggestions.append(f"{issue.message} -> {issue.suggestion}")
                        else:
                            issues_with_suggestions.append(issue.message)
                    naming_issues_detail.append(
                        {
                            "method": result.method_name,
                            "endpoint": f"{result.http_method} {result.path}",
                            "issues": issues_with_suggestions,
                        }
                    )
            report["naming_issues"] = naming_issues_detail
            report["summary"]["naming_errors"] = naming_errors
            report["summary"]["naming_warnings"] = naming_warnings
            report["summary"]["naming_suggestions"] = naming_suggestions

        total_issues += naming_errors + naming_warnings + naming_suggestions

        if total_issues > 0:
            logger.warning(
                "OpenAPI verification found %d issues for %s (missing: %d, annotation: %d, naming errors: %d, warnings: %d, suggestions: %d)",
                total_issues,
                repo_name,
                len(missing_methods),
                len(annotation_issues),
                naming_errors,
                naming_warnings,
                naming_suggestions,
            )
            # Build JSON report with all issues
            json_output: str = json.dumps(report, indent=2, sort_keys=False)
            separator: str = "=" * 100
            self.fail(
                f"{extension_name}: Found {total_issues} issues "
                f"({len(missing_methods)} missing @restapi_endpoint annotations, "
                f"{len(annotation_issues)} annotation validation issues, "
                f"{naming_errors} naming errors, {naming_warnings} naming warnings, "
                f"{naming_suggestions} naming suggestions).\n\n"
                f"{separator}\n"
                f"{self._get_report_title(extension_name)}\n"
                f"{separator}\n\n"
                f"{json_output}\n\n"
                f"{separator}"
            )
        else:
            logger.info("OpenAPI verification passed for %s (%d endpoints verified via annotations)", repo_name, len(implemented_methods))
