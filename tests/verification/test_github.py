"""
GitHub-based API verification tests.

Tests extension clients against OpenAPI specs from GitHub repositories.
"""

from typing import Any

from .base_test import BaseExtensionAPIVerificationTest
from .config import GITHUB_ORG, OPENAPI_PATH, REPO_PREFIX, SKIP_EXTENSIONS_GITHUB
from .openapi_utils import fetch_openapi_spec


class GitHubAPIVerificationTest(BaseExtensionAPIVerificationTest):
    """
    Verify extension clients against OpenAPI specs from GitHub repositories.

    Fetches OpenAPI specifications from GitHub source code repositories.
    This is the primary verification method for development.

    Usage:
        # Run all GitHub tests
        uv run python -m unittest tests.verification.test_github.GitHubAPIVerificationTest -v

        # Run single extension test
        uv run python -m unittest tests.verification.test_github.GitHubAPIVerificationTest.test_pdf_exporter_completeness -v
    """

    skip_extensions = SKIP_EXTENSIONS_GITHUB

    def _fetch_openapi_spec(self, extension_name: str, repo_name: str) -> dict[str, Any] | None:
        """Fetch OpenAPI spec from GitHub."""
        return fetch_openapi_spec(extension_name, repo_name)

    def _get_report_metadata(self, extension_name: str, repo_name: str) -> dict[str, str]:
        """Return GitHub-specific report metadata."""
        return {
            "source": "github",
            "repository": f"{REPO_PREFIX}.{repo_name}",
            "openapi_spec_url": f"https://github.com/{GITHUB_ORG}/{REPO_PREFIX}.{repo_name}/blob/main/{OPENAPI_PATH}",
        }

    # =========================================================================
    # Test Methods - One per Extension (alphabetically sorted)
    # =========================================================================

    def test_aad_synchronizer_completeness(self) -> None:
        """Verify aad_synchronizer.py matches upstream AAD Synchronizer API."""
        self._verify_extension("aad_synchronizer")

    def test_api_extender_completeness(self) -> None:
        """Verify api_extender.py matches upstream API Extender API."""
        self._verify_extension("api_extender")

    def test_cucumber_completeness(self) -> None:
        """Verify cucumber.py matches upstream Cucumber API."""
        self._verify_extension("cucumber")

    def test_diff_tool_completeness(self) -> None:
        """Verify diff_tool.py matches upstream Diff Tool API."""
        self._verify_extension("diff_tool")

    def test_docx_exporter_completeness(self) -> None:
        """Verify docx_exporter.py matches upstream DOCX Exporter API."""
        self._verify_extension("docx_exporter")

    def test_excel_importer_completeness(self) -> None:
        """Verify excel_importer.py matches upstream Excel Importer API."""
        self._verify_extension("excel_importer")

    def test_fake_services_completeness(self) -> None:
        """Verify fake_services.py matches upstream Excel Importer API."""
        self._verify_extension("fake_services")

    def test_interceptor_manager_completeness(self) -> None:
        """Verify interceptor_manager.py matches upstream Interceptor Manager API."""
        self._verify_extension("interceptor_manager")

    def test_json_editor_completeness(self) -> None:
        """Verify json_editor.py matches upstream JSON Editor API."""
        self._verify_extension("json_editor")

    def test_mailworkflow_completeness(self) -> None:
        """Verify mailworkflow.py matches upstream Mail Workflow API."""
        self._verify_extension("mailworkflow")

    def test_pdf_exporter_completeness(self) -> None:
        """Verify pdf_exporter.py matches upstream PDF Exporter API."""
        self._verify_extension("pdf_exporter")

    def test_requirements_inspector_completeness(self) -> None:
        """Verify requirements_inspector.py matches upstream Requirements Inspector API."""
        self._verify_extension("requirements_inspector")

    def test_strictdoc_exporter_completeness(self) -> None:
        """Verify strictdoc_exporter.py matches upstream StrictDoc Exporter API."""
        self._verify_extension("strictdoc_exporter")

    def test_test_data_completeness(self) -> None:
        """Verify test_data.py matches upstream Test Data API."""
        self._verify_extension("test_data")
