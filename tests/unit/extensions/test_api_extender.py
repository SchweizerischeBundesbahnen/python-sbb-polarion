"""Unit tests for API Extender API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.api_extender import PolarionApiExtenderApi


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionApiExtenderApi(unittest.TestCase):
    """Test PolarionApiExtenderApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionApiExtenderApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "api-extender")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Project Custom Fields
    # =========================================================================

    def test_get_custom_field(self) -> None:
        """Test get project custom field."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_custom_field("PROJ", "customKey")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/keys/customKey"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_save_custom_field(self) -> None:
        """Test save project custom field."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.save_custom_field("PROJ", "customKey", "customValue")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/keys/customKey"
        expected_data: JsonDict = {"value": "customValue"}
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=expected_data)

    def test_delete_custom_field(self) -> None:
        """Test delete project custom field."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_custom_field("PROJ", "customKey")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/keys/customKey"
        self.mock_connection.api_request_delete.assert_called_once_with(expected_url)

    # =========================================================================
    # Global Records
    # =========================================================================

    def test_get_record(self) -> None:
        """Test get global record."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_record("recordKey")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/records/recordKey"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_save_record(self) -> None:
        """Test save global record."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.save_record("recordKey", "recordValue")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/records/recordKey"
        expected_data: JsonDict = {"value": "recordValue"}
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=expected_data)

    def test_delete_record(self) -> None:
        """Test delete global record."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_record("recordKey")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/records/recordKey"
        self.mock_connection.api_request_delete.assert_called_once_with(expected_url)

    # =========================================================================
    # Regex Tool
    # =========================================================================

    def test_find_matches(self) -> None:
        """Test find regex matches."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.find_matches("test text 123", r"\d+")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/regex-tool/find-matches"
        expected_files: dict[str, str] = {"text": "test text 123", "regex": r"\d+"}
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, files=expected_files)

    # =========================================================================
    # Settings Mixin Methods (from PolarionGenericExtensionSettingsApi)
    # =========================================================================

    def test_get_features(self) -> None:
        """Test get_features method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_features()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings")

    def test_get_setting_names(self) -> None:
        """Test get_setting_names method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_names("feature1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names", params=None)

    def test_get_setting_content(self) -> None:
        """Test get_setting_content method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_content("feature1", name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/content", params={"scope": "project/test"})

    def test_save_setting(self) -> None:
        """Test save_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_setting("feature1", data, name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_put.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/content", data=data, params={"scope": "project/test"})

    def test_rename_setting(self) -> None:
        """Test rename_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.rename_setting("feature1", "OldName", "NewName")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/OldName", payload="NewName", params=None)

    def test_delete_setting(self) -> None:
        """Test delete_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_setting("feature1", "Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom", params={"scope": "project/test"})

    def test_get_setting_default_content(self) -> None:
        """Test get_setting_default_content method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_default_content("feature1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/default-content")

    def test_get_setting_revisions(self) -> None:
        """Test get_setting_revisions method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_revisions("feature1", name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/revisions", params={"scope": "project/test"})


if __name__ == "__main__":
    unittest.main()
