"""Unit tests for Integrity Scanner API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.integrity_scanner import PolarionIntegrityScannerApi


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionIntegrityScannerApi(unittest.TestCase):
    """Test PolarionIntegrityScannerApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionIntegrityScannerApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "integrity-scanner")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Scanner Operations
    # =========================================================================

    def test_get_projects(self) -> None:
        """Test get list of projects accessible to the current user."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_projects()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/projects",
        )

    def test_get_documents(self) -> None:
        """Test get list of documents in the given project."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_documents(project_id="elibrary")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/projects/elibrary/documents",
        )

    def test_scan(self) -> None:
        """Test scan a document for the list of documents it refers."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        scan_params: JsonDict = {
            "projectId": "elibrary",
            "space": "specification",
            "documentName": "Project Specification",
        }
        response: Response = self.api.scan(scan_params=scan_params)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/scan",
            data=scan_params,
        )

    def test_get_revisions(self) -> None:
        """Test get list of revisions for a particular document."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_revisions(
            project_id="elibrary",
            space="specification",
            document_name="Project Specification",
        )

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "projectId": "elibrary",
            "space": "specification",
            "documentName": "Project Specification",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/revisions",
            params=expected_params,
        )
