"""Unit tests for core base classes."""

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class MockExtensionApi(PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi):
    """Mock extension API with both base and settings functionality for testing."""


class TestPolarionRestApiConnection(unittest.TestCase):
    """Test PolarionRestApiConnection class."""

    @patch("python_sbb_polarion.util.http.Session")
    def test_init_inherits_from_http_connection(self, mock_session_class: Mock) -> None:
        """Test that PolarionRestApiConnection properly inherits from HttpConnection."""
        mock_session: Mock = Mock()
        mock_session_class.return_value = mock_session

        conn: PolarionRestApiConnection = PolarionRestApiConnection(url="https://polarion.example.com", token="test-token")

        self.assertEqual(conn.host, "https://polarion.example.com")
        self.assertIsNotNone(conn._HttpConnection__authorization_headers)  # type: ignore[attr-defined]
        mock_session_class.assert_called_once()


class TestPolarionGenericExtensionApi(unittest.TestCase):
    """Test PolarionGenericExtensionApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock(spec=PolarionRestApiConnection)
        self.extension_name = "test-extension"
        self.api = MockExtensionApi(self.extension_name, self.mock_connection)

    def test_init(self) -> None:
        """Test initialization sets correct attributes."""
        self.assertEqual(self.api.polarion_connection, self.mock_connection)
        self.assertEqual(self.api.extension_name, self.extension_name)
        self.assertEqual(self.api.rest_api_url, "/polarion/test-extension/rest/api")

    def test_get_context(self) -> None:
        """Test get_context method."""
        expected_response: JsonDict = {"context": "test"}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_context()

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/context")

    def test_get_version(self) -> None:
        """Test get_version method."""
        expected_response: JsonDict = {"version": "1.0.0"}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_version()

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/version")

    def test_get_settings_default_name(self) -> None:
        """Test get_setting_content with default name."""
        expected_response: JsonDict = {"setting1": "value1"}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_content("feature1")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Default/content", params=None)

    def test_get_settings_custom_name(self) -> None:
        """Test get_setting_content with custom name."""
        expected_response: JsonDict = {"setting1": "value1"}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_content("feature1", name="Custom")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom/content", params=None)

    def test_get_settings_with_scope(self) -> None:
        """Test get_setting_content with scope parameter."""
        expected_response: JsonDict = {"setting1": "value1"}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_content("feature1", scope="project/TEST/")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Default/content", params={"scope": "project/TEST/"})

    def test_get_settings_with_name_and_scope(self) -> None:
        """Test get_setting_content with both name and scope."""
        expected_response: JsonDict = {"setting1": "value1"}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_content("feature1", name="Custom", scope="project/TEST/")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom/content", params={"scope": "project/TEST/"})

    def test_save_settings_default_name(self) -> None:
        """Test save_setting with default name."""
        data: JsonDict = {
            "setting1": "new_value",
        }
        expected_response: JsonDict = {"status": "success"}
        self.mock_connection.api_request_put.return_value = expected_response

        result: Response = self.api.save_setting("feature1", data)

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_put.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Default/content", data=data, params=None)

    def test_save_settings_custom_name(self) -> None:
        """Test save_setting with custom name."""
        data: JsonDict = {
            "setting1": "new_value",
        }
        expected_response: JsonDict = {"status": "success"}
        self.mock_connection.api_request_put.return_value = expected_response

        result: Response = self.api.save_setting("feature1", data, name="Custom")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_put.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom/content", data=data, params=None)

    def test_save_settings_with_scope(self) -> None:
        """Test save_setting with scope parameter."""
        data: JsonDict = {
            "setting1": "new_value",
        }
        expected_response: JsonDict = {"status": "success"}
        self.mock_connection.api_request_put.return_value = expected_response

        result: Response = self.api.save_setting("feature1", data, scope="project/TEST/")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_put.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Default/content", data=data, params={"scope": "project/TEST/"})

    def test_save_settings_with_name_and_scope(self) -> None:
        """Test save_setting with both name and scope."""
        data: JsonDict = {
            "setting1": "new_value",
        }
        expected_response: JsonDict = {"status": "success"}
        self.mock_connection.api_request_put.return_value = expected_response

        result: Response = self.api.save_setting("feature1", data, name="Custom", scope="project/TEST/")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_put.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom/content", data=data, params={"scope": "project/TEST/"})

    def test_delete_settings_default_scope(self) -> None:
        """Test delete_setting without scope."""
        expected_response: JsonDict = {"status": "deleted"}
        self.mock_connection.api_request_delete.return_value = expected_response

        result: Response = self.api.delete_setting("feature1", "Custom")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom", params=None)

    def test_delete_settings_with_scope(self) -> None:
        """Test delete_setting with scope parameter."""
        expected_response: JsonDict = {"status": "deleted"}
        self.mock_connection.api_request_delete.return_value = expected_response

        result: Response = self.api.delete_setting("feature1", "Custom", scope="project/TEST/")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom", params={"scope": "project/TEST/"})

    def test_get_settings_defaults(self) -> None:
        """Test get_setting_default_content method."""
        expected_response: JsonDict = {"default_setting": "value"}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_default_content("feature1")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/default-content")

    def test_get_settings_revisions_default_name(self) -> None:
        """Test get_setting_revisions with default name."""
        expected_response: JsonDict = {"revisions": ["1", "2", "3"]}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_revisions("feature1")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Default/revisions", params=None)

    def test_get_settings_revisions_custom_name(self) -> None:
        """Test get_setting_revisions with custom name."""
        expected_response: JsonDict = {"revisions": ["1", "2", "3"]}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_revisions("feature1", name="Custom")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom/revisions", params=None)

    def test_get_settings_revisions_with_scope(self) -> None:
        """Test get_setting_revisions with scope parameter."""
        expected_response: JsonDict = {"revisions": ["1", "2", "3"]}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_revisions("feature1", scope="project/TEST/")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Default/revisions", params={"scope": "project/TEST/"})

    def test_get_settings_revisions_with_name_and_scope(self) -> None:
        """Test get_setting_revisions with both name and scope."""
        expected_response: JsonDict = {"revisions": ["1", "2", "3"]}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_setting_revisions("feature1", name="Custom", scope="project/TEST/")

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/settings/feature1/names/Custom/revisions", params={"scope": "project/TEST/"})

    def test_get_swagger(self) -> None:
        """Test get_swagger method."""
        expected_response: JsonDict = {"swagger": "2.0", "info": {"title": "API"}}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_swagger()

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/swagger")

    def test_get_openapi(self) -> None:
        """Test get_openapi method."""
        expected_response: JsonDict = {"openapi": "3.0.0", "info": {"title": "API"}}
        self.mock_connection.api_request_get.return_value = expected_response

        result: Response = self.api.get_openapi()

        self.assertEqual(result, expected_response)
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/test-extension/rest/api/openapi.json")


if __name__ == "__main__":
    unittest.main()
