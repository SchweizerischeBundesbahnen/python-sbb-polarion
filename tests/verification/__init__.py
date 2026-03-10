"""
Extension API Verification Tests.

This package provides tools for verifying Python extension clients against OpenAPI specs.

Usage:
    # Run GitHub-based tests (default)
    uv run python -m tests.verification

    # Run live Polarion tests
    uv run python -m tests.verification --live --extension pdf-exporter

    # List available extensions
    uv run python -m tests.verification --list
"""

from .base_test import BaseExtensionAPIVerificationTest
from .config import (
    DEFAULT_APP_URL,
    EXTENSION_MAPPING,
    GITHUB_ORG,
    GITHUB_TOKEN,
    OPENAPI_PATH,
    REPO_PREFIX,
    SKIP_EXTENSIONS_GITHUB,
    SKIP_EXTENSIONS_LIVE,
)
from .openapi_utils import (
    extract_annotated_methods,
    extract_api_endpoints,
    fetch_openapi_from_polarion_live,
    fetch_openapi_spec,
    validate_annotation_against_openapi,
)
from .test_github import GitHubAPIVerificationTest
from .test_polarion_live import PolarionLiveAPIVerificationTest


__all__ = [
    "DEFAULT_APP_URL",
    "EXTENSION_MAPPING",
    "GITHUB_ORG",
    "GITHUB_TOKEN",
    "OPENAPI_PATH",
    "REPO_PREFIX",
    "SKIP_EXTENSIONS_GITHUB",
    "SKIP_EXTENSIONS_LIVE",
    "BaseExtensionAPIVerificationTest",
    "GitHubAPIVerificationTest",
    "PolarionLiveAPIVerificationTest",
    "extract_annotated_methods",
    "extract_api_endpoints",
    "fetch_openapi_from_polarion_live",
    "fetch_openapi_spec",
    "validate_annotation_against_openapi",
]
