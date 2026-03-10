"""
OpenAPI verification tests for PolarionApiV1.

Validates that PolarionApiV1 methods have @restapi_endpoint annotations
that match the endpoints in polarion-openapi.json.
"""

from __future__ import annotations

import json
import logging
import unittest
from pathlib import Path
from typing import Any, ClassVar

from .openapi_utils import (
    extract_api_endpoints,
    extract_polarion_api_v1_annotated_methods,
    extract_polarion_api_v1_unannotated_methods,
    validate_annotation_against_openapi,
    validate_implementation_http_method,
)


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Path to OpenAPI spec file in project root
OPENAPI_FILE: Path = Path(__file__).parent.parent.parent / "polarion-openapi.json"


class TestPolarionApiV1AnnotationValidation(unittest.TestCase):
    """Validate PolarionApiV1 @restapi_endpoint annotations against polarion-openapi.json."""

    openapi_spec: ClassVar[dict[str, Any]]
    openapi_endpoints: ClassVar[list[dict[str, Any]]]
    annotated_methods: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        """Load OpenAPI spec and extract PolarionApiV1 annotated methods."""
        # Load OpenAPI spec
        if not OPENAPI_FILE.exists():
            raise FileNotFoundError(f"OpenAPI spec not found: {OPENAPI_FILE}")

        with OPENAPI_FILE.open(encoding="utf-8") as f:
            cls.openapi_spec = json.load(f)

        # Extract all endpoints from OpenAPI spec
        cls.openapi_endpoints = extract_api_endpoints(cls.openapi_spec)

        # Extract annotated methods from PolarionApiV1
        cls.annotated_methods = extract_polarion_api_v1_annotated_methods()

    def test_openapi_file_exists(self) -> None:
        """Test that polarion-openapi.json file exists."""
        self.assertTrue(OPENAPI_FILE.exists(), f"OpenAPI spec file not found: {OPENAPI_FILE}")

    def test_openapi_has_paths(self) -> None:
        """Test that OpenAPI spec contains paths."""
        self.assertIn("paths", self.openapi_spec)
        self.assertGreater(len(self.openapi_spec["paths"]), 0)

    def test_all_endpoints_have_annotations(self) -> None:
        """Test that all OpenAPI endpoints have corresponding @restapi_endpoint annotations.

        This is the main validation test that ensures:
        1. Every OpenAPI endpoint has a Python method with @restapi_endpoint
        2. The annotation parameters match the OpenAPI spec
        3. No orphan annotations exist (annotations without matching OpenAPI endpoint)
        4. No duplicate annotations (multiple methods for same endpoint)
        """
        # Track results
        missing_annotations: list[dict[str, Any]] = []
        annotation_issues: list[dict[str, Any]] = []
        implemented_methods: dict[str, dict[str, Any]] = {}
        endpoint_to_methods: dict[str, list[str]] = {}

        # Match annotated methods by exact method+path
        matched_endpoints: set[int] = set()

        for method_name, annotation_data in self.annotated_methods.items():
            endpoint_key: str = f"{annotation_data['method']} {annotation_data['path']}"

            # Track all methods that annotate this endpoint
            if endpoint_key not in endpoint_to_methods:
                endpoint_to_methods[endpoint_key] = []
            endpoint_to_methods[endpoint_key].append(method_name)

            # Find matching OpenAPI endpoint
            matching_endpoint: dict[str, Any] | None = None
            for idx, endpoint in enumerate(self.openapi_endpoints):
                if endpoint["method"] == annotation_data["method"] and endpoint["path"] == annotation_data["path"]:
                    matching_endpoint = endpoint
                    matched_endpoints.add(idx)
                    break

            if matching_endpoint is not None:
                # Validate annotation against OpenAPI
                validation_errors: list[str] = validate_annotation_against_openapi(method_name, annotation_data, matching_endpoint)

                # Validate implementation HTTP method
                impl_error: str | None = validate_implementation_http_method(annotation_data["func"], annotation_data["method"])
                if impl_error:
                    validation_errors.append(impl_error)

                if validation_errors:
                    annotation_issues.append(
                        {
                            "method": method_name,
                            "annotation": annotation_data,
                            "endpoint": matching_endpoint,
                            "errors": validation_errors,
                        }
                    )
                else:
                    implemented_methods[method_name] = matching_endpoint
            else:
                # Orphan annotation - no matching OpenAPI endpoint
                orphan_errors: list[str] = [f"ORPHAN ANNOTATION: Method '{method_name}' has @restapi_endpoint({annotation_data['method']} {annotation_data['path']}) but this endpoint does NOT exist in polarion-openapi.json"]
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

        # Check for duplicate annotations
        for endpoint_key, methods in endpoint_to_methods.items():
            if len(methods) > 1:
                for method_name in methods:
                    annotation_issues.append(
                        {
                            "method": method_name,
                            "annotation": self.annotated_methods[method_name],
                            "endpoint": None,
                            "errors": [f"DUPLICATE ANNOTATION: Endpoint '{endpoint_key}' is annotated by multiple methods: {methods}"],
                        }
                    )

        # Check for unmatched OpenAPI endpoints (missing annotations)
        for idx, endpoint in enumerate(self.openapi_endpoints):
            if idx in matched_endpoints:
                continue

            # Convert sets to lists for JSON serialization
            params: dict[str, Any] = endpoint["parameters"]
            serializable_params: dict[str, Any] = {
                "path_params": params.get("path_params", []),
                "query_params": params.get("query_params", []),
                "required_params": sorted(params.get("required_params", set())),
                "all_params": sorted(params.get("all_params", set())),
            }

            missing_info: dict[str, Any] = {
                "http_method": endpoint["method"],
                "path": endpoint["path"],
                "operation_id": endpoint["operation_id"],
                "parameters": serializable_params,
            }
            missing_annotations.append(missing_info)

        # Check for unannotated API methods
        unannotated_methods: list[str] = extract_polarion_api_v1_unannotated_methods()
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
        total_issues: int = len(missing_annotations) + len(annotation_issues)

        report: dict[str, Any] = {
            "api": "PolarionApiV1",
            "openapi_file": str(OPENAPI_FILE),
            "summary": {
                "total_issues": total_issues,
                "total_openapi_endpoints": len(self.openapi_endpoints),
                "missing_annotations": len(missing_annotations),
                "annotation_issues": len(annotation_issues),
                "implemented_methods": len(implemented_methods),
                "annotated_methods": len(self.annotated_methods),
            },
            "missing_annotations": missing_annotations[:20],  # Limit output
            "annotation_issues": [
                {
                    "method": issue["method"],
                    "annotation": {
                        "method": issue["annotation"]["method"],
                        "path": issue["annotation"]["path"],
                    },
                    "errors": issue["errors"],
                }
                for issue in annotation_issues[:20]  # Limit output
            ],
            "implemented_methods": sorted(implemented_methods.keys())[:20],
        }

        if total_issues > 0:
            json_output: str = json.dumps(report, indent=2, sort_keys=False)
            separator: str = "=" * 100
            self.fail(
                f"PolarionApiV1: Found {total_issues} issues "
                f"({len(missing_annotations)} missing annotations, "
                f"{len(annotation_issues)} annotation issues).\n\n"
                f"{separator}\n"
                f"OpenAPI Verification Report: PolarionApiV1\n"
                f"{separator}\n\n"
                f"{json_output}\n\n"
                f"{separator}\n\n"
                f"To fix: Add @restapi_endpoint annotations to all methods in polarion_api/ mixins."
            )

    def test_annotation_count_reasonable(self) -> None:
        """Test that we have annotations for most endpoints."""
        # We should have at least 80% coverage
        min_expected: int = int(len(self.openapi_endpoints) * 0.8)
        self.assertGreaterEqual(
            len(self.annotated_methods),
            min_expected,
            f"Expected at least {min_expected} annotated methods for {len(self.openapi_endpoints)} endpoints, got {len(self.annotated_methods)}. Add @restapi_endpoint annotations to methods.",
        )


class TestPolarionApiV1MethodSignatures(unittest.TestCase):
    """Validate that PolarionApiV1 method signatures follow conventions."""

    api_class: ClassVar[type[Any]]

    @classmethod
    def setUpClass(cls) -> None:
        """Load PolarionApiV1 class."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        cls.api_class = PolarionApiV1

    def test_all_methods_return_response(self) -> None:
        """Test that all public methods have return type annotation."""
        for name in dir(self.api_class):
            if name.startswith("_"):
                continue
            attr: Any = getattr(self.api_class, name, None)
            if callable(attr) and not isinstance(attr, type):
                hints: dict[str, Any] = getattr(attr, "__annotations__", {})
                if "return" in hints:
                    return_type: str = str(hints["return"])
                    self.assertIn(
                        "Response",
                        return_type,
                        f"Method {name} should return Response, got {return_type}",
                    )

    def test_method_naming_conventions(self) -> None:
        """Test that methods follow naming conventions."""
        method_prefixes: list[str] = [
            "get_",
            "create_",
            "update_",
            "delete_",
            "branch_",
            "copy_",
            "merge_",
            "close_",
            "reopen_",
            "move_",
            "mark_",
            "unmark_",
            "import_",
            "export_",
            "download_",
            "set_",
            "execute_",
            "reuse_",
        ]

        for name in dir(self.api_class):
            if name.startswith("_"):
                continue
            attr: Any = getattr(self.api_class, name, None)
            if callable(attr) and not isinstance(attr, type):
                has_valid_prefix: bool = any(name.startswith(prefix) for prefix in method_prefixes)
                self.assertTrue(
                    has_valid_prefix,
                    f"Method '{name}' should start with one of: {method_prefixes}",
                )


if __name__ == "__main__":
    unittest.main()
