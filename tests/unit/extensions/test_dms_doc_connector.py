"""Unit tests for DMS Doc Connector API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.dms_doc_connector import PolarionDmsDocConnectorApi


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionDmsDocConnectorApi(unittest.TestCase):
    """Test PolarionDmsDocConnectorApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionDmsDocConnectorApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "dms-doc-connector")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

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

    def test_get_setting_names_with_scope(self) -> None:
        """Test get_setting_names with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_names("feature1", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names", params={"scope": "project/elibrary/"})

    def test_get_setting_content(self) -> None:
        """Test get_setting_content method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_content("feature1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Default/content", params=None)

    def test_get_setting_content_with_all_params(self) -> None:
        """Test get_setting_content with all parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_content("feature1", name="Custom", scope="project/elibrary/", revision="12345")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/content", params={"scope": "project/elibrary/", "revision": "12345"})

    def test_save_setting(self) -> None:
        """Test save_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_setting("feature1", data)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_put.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Default/content", data=data, params=None)

    def test_save_setting_with_all_params(self) -> None:
        """Test save_setting with all parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_setting("feature1", data, name="Custom", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_put.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/content", data=data, params={"scope": "project/elibrary/"})

    def test_rename_setting(self) -> None:
        """Test rename_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.rename_setting("feature1", "OldName", "NewName")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/OldName", payload="NewName", params=None)

    def test_rename_setting_with_scope(self) -> None:
        """Test rename_setting with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.rename_setting("feature1", "OldName", "NewName", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/OldName", payload="NewName", params={"scope": "project/elibrary/"})

    def test_delete_setting(self) -> None:
        """Test delete_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_setting("feature1", "Custom")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom", params=None)

    def test_delete_setting_with_scope(self) -> None:
        """Test delete_setting with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_setting("feature1", "Custom", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom", params={"scope": "project/elibrary/"})

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

        response: Response = self.api.get_setting_revisions("feature1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Default/revisions", params=None)

    def test_get_setting_revisions_with_all_params(self) -> None:
        """Test get_setting_revisions with all parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_revisions("feature1", name="Custom", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/revisions", params={"scope": "project/elibrary/"})


if __name__ == "__main__":
    unittest.main()
