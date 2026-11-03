"""Unit tests for StrictDoc Exporter API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.strictdoc_exporter import PolarionStrictDocExporterApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionStrictDocExporterApi(unittest.TestCase):
    """Test PolarionStrictDocExporterApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionStrictDocExporterApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "strictdoc-exporter")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    def test_export_live_doc(self) -> None:
        """Test export live doc."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        export_params: JsonDict = {
            "projectId": "PROJ",
            "locations": [{"spaceId": "Specification", "moduleName": "Test"}],
            "format": "SDOC",
            "fileName": "export",
        }
        response: Response = self.api.export_live_doc(export_params)

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.OCTET_STREAM, Header.CONTENT_TYPE: MediaType.JSON}
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/export/livedoc",
            data=export_params,
            headers=expected_headers,
        )

    def test_export_github_livedoc(self) -> None:
        """Test export of a live document to StrictDoc format on GitHub."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        export_params: JsonDict = {
            "projectId": "PROJ",
            "locations": [{"spaceId": "Specification", "moduleName": "Test"}],
            "format": "SDOC",
            "fileName": "export",
        }
        response: Response = self.api.export_github_livedoc(export_params)

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.OCTET_STREAM, Header.CONTENT_TYPE: MediaType.JSON}
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/export-github/livedoc",
            data=export_params,
            headers=expected_headers,
        )

    def test_find_widgets_bulk_export_items(self) -> None:
        """Test getting the rows of a bulk export widget."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        request_params: JsonDict = {
            "projectId": "elibrary",
            "query": "type:testrun",
        }
        response: Response = self.api.find_widgets_bulk_export_items(request_params)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/widgets/bulk-export/items",
            data=request_params,
            headers={Header.ACCEPT: MediaType.JSON, Header.CONTENT_TYPE: MediaType.JSON},
        )


if __name__ == "__main__":
    unittest.main()
