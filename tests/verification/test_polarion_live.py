"""
Live Polarion API verification tests.

Tests extension clients against OpenAPI specs from deployed Polarion instances.
"""

import logging
import os
import unittest
from typing import Any

from .base_test import BaseExtensionAPIVerificationTest
from .config import DEFAULT_APP_URL, SKIP_EXTENSIONS_LIVE
from .openapi_utils import fetch_openapi_from_polarion_live


logger = logging.getLogger(__name__)


class PolarionLiveAPIVerificationTest(BaseExtensionAPIVerificationTest):
    """
    Verify extension clients against LIVE Polarion instance OpenAPI specs.

    This test class fetches OpenAPI specifications directly from a deployed
    Polarion instance, allowing verification against actual production APIs.

    Configuration (environment variables):
        APP_URL: Polarion instance URL (default: https://polarion.example.com)
        APP_TOKEN: Bearer token for API authentication (REQUIRED)

    Usage:
        # Set environment variables
        export APP_URL="https://polarion.example.com"
        export APP_TOKEN="your-token-here"

        # Run all live tests
        uv run python -m unittest tests.verification.polarion_live_test.PolarionLiveAPIVerificationTest -v

        # Run single extension test
        uv run python -m unittest tests.verification.polarion_live_test.PolarionLiveAPIVerificationTest.test_pdf_exporter_completeness_live -v

        # Or use the CLI helper
        uv run python -m tests.verification --live --extension pdf-exporter
    """

    skip_extensions = SKIP_EXTENSIONS_LIVE
    app_url: str = ""
    app_token: str = ""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test class - verify Polarion credentials are available."""
        cls.app_url = os.environ.get("APP_URL", DEFAULT_APP_URL)
        cls.app_token = os.environ.get("APP_TOKEN", "")

        if not cls.app_token:
            raise unittest.SkipTest("APP_TOKEN environment variable is required for live API tests. Set it to run these tests.")

        logger.info("Live API tests configured for: %s", cls.app_url)

    def _fetch_openapi_spec(self, extension_name: str, repo_name: str) -> dict[str, Any] | None:
        """Fetch OpenAPI spec from live Polarion instance."""
        return fetch_openapi_from_polarion_live(repo_name, self.app_url, self.app_token)

    def _get_report_metadata(self, extension_name: str, repo_name: str) -> dict[str, str]:
        """Return live Polarion-specific report metadata."""
        return {
            "source": "polarion_live",
            "app_url": self.app_url,
            "openapi_spec_url": f"{self.app_url}/polarion/{repo_name}/rest/api/openapi.json",
        }

    def _get_report_title(self, extension_name: str) -> str:
        """Get title for the live Polarion report."""
        return f"Live Polarion OpenAPI Verification Report: {extension_name}\nSource: {self.app_url}"

    # =========================================================================
    # Test Methods - One per Extension (alphabetically sorted)
    # =========================================================================

    def test_aad_synchronizer_completeness_live(self) -> None:
        """Verify aad_synchronizer.py against live Polarion API."""
        self._verify_extension("aad_synchronizer")

    def test_admin_utility_completeness_live(self) -> None:
        """Verify admin_utility.py against live Polarion API."""
        self._verify_extension("admin_utility")

    def test_api_extender_completeness_live(self) -> None:
        """Verify api_extender.py against live Polarion API."""
        self._verify_extension("api_extender")

    def test_collection_checker_completeness_live(self) -> None:
        """Verify collection_checker.py against live Polarion API."""
        self._verify_extension("collection_checker")

    def test_cucumber_completeness_live(self) -> None:
        """Verify cucumber.py against live Polarion API."""
        self._verify_extension("cucumber")

    def test_diff_tool_completeness_live(self) -> None:
        """Verify diff_tool.py against live Polarion API."""
        self._verify_extension("diff_tool")

    def test_dms_doc_connector_completeness_live(self) -> None:
        """Verify dms_doc_connector.py against live Polarion API."""
        self._verify_extension("dms_doc_connector")

    def test_dms_wi_connector_completeness_live(self) -> None:
        """Verify dms_wi_connector.py against live Polarion API."""
        self._verify_extension("dms_wi_connector")

    def test_docx_exporter_completeness_live(self) -> None:
        """Verify docx_exporter.py against live Polarion API."""
        self._verify_extension("docx_exporter")

    def test_excel_importer_completeness_live(self) -> None:
        """Verify excel_importer.py against live Polarion API."""
        self._verify_extension("excel_importer")

    def test_fake_services_completeness_live(self) -> None:
        """Verify fake_services.py against live Polarion API."""
        self._verify_extension("fake_services")

    def test_interceptor_manager_completeness_live(self) -> None:
        """Verify interceptor_manager.py against live Polarion API."""
        self._verify_extension("interceptor_manager")

    def test_json_editor_completeness_live(self) -> None:
        """Verify json_editor.py against live Polarion API."""
        self._verify_extension("json_editor")

    def test_mailworkflow_completeness_live(self) -> None:
        """Verify mailworkflow.py against live Polarion API."""
        self._verify_extension("mailworkflow")

    def test_pdf_exporter_completeness_live(self) -> None:
        """Verify pdf_exporter.py against live Polarion API."""
        self._verify_extension("pdf_exporter")

    def test_requirements_inspector_completeness_live(self) -> None:
        """Verify requirements_inspector.py against live Polarion API."""
        self._verify_extension("requirements_inspector")

    def test_strictdoc_exporter_completeness_live(self) -> None:
        """Verify strictdoc_exporter.py against live Polarion API."""
        self._verify_extension("strictdoc_exporter")

    def test_test_data_completeness_live(self) -> None:
        """Verify test_data.py against live Polarion API."""
        self._verify_extension("test_data")

    def test_xml_repair_completeness_live(self) -> None:
        """Verify xml_repair.py against live Polarion API."""
        self._verify_extension("xml_repair")
