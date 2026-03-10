"""Unit tests for JSON Editor API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.json_editor import PolarionJsonEditorApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response


class TestPolarionJsonEditorApi(unittest.TestCase):
    """Test PolarionJsonEditorApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionJsonEditorApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "json-editor")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Attachments
    # =========================================================================

    def test_create_workitem_attachment(self) -> None:
        """Test create workitem attachment."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_workitem_attachment("PROJ", "WI-123", "test.json")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/workitems/WI-123/attachments"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, files={"fileName": "test.json"})

    def test_update_workitem_attachment(self) -> None:
        """Test update workitem attachment content."""
        mock_response = Mock()
        self.mock_connection.api_request_patch.return_value = mock_response

        response: Response = self.api.update_workitem_attachment("PROJ", "WI-123", "attach-1", '{"key": "value"}')

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/workitems/WI-123/attachments/attach-1"
        self.mock_connection.api_request_patch.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, files={"content": '{"key": "value"}'})

    def test_get_workitem_attachment(self) -> None:
        """Test get workitem attachment content."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_workitem_attachment("PROJ", "WI-123", "attach-1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/workitems/WI-123/attachments/attach-1/content"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN})


if __name__ == "__main__":
    unittest.main()
