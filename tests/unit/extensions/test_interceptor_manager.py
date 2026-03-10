"""Unit tests for Interceptor Manager API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.interceptor_manager import PolarionInterceptorManagerApi


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionInterceptorManagerApi(unittest.TestCase):
    """Test PolarionInterceptorManagerApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionInterceptorManagerApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "interceptor-manager")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Hooks Settings
    # =========================================================================

    def test_get_hook_settings_default(self) -> None:
        """Test get hook settings with default revision."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_hook_settings("hook1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/hook-settings/hook1/content"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params=None)

    def test_get_hook_settings_with_revision(self) -> None:
        """Test get hook settings with specific revision."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_hook_settings("hook1", revision="rev123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/hook-settings/hook1/content"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"revision": "rev123"})

    def test_save_hook_settings(self) -> None:
        """Test save hook settings."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_hook_settings("hook1", data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/hook-settings/hook1/content"
        self.mock_connection.api_request_put.assert_called_once_with(expected_url, data=data)

    def test_get_hook_settings_defaults(self) -> None:
        """Test get hook settings defaults."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_hook_settings_defaults("hook1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/hook-settings/hook1/default-content"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_hook_settings_revisions(self) -> None:
        """Test get hook settings revisions."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_hook_settings_revisions("hook1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/hook-settings/hook1/revisions"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    # =========================================================================
    # Hooks
    # =========================================================================

    def test_get_hooks_default(self) -> None:
        """Test get hooks with default reload parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_hooks()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/hooks", params={"reload": "false"})

    def test_get_hooks_with_reload(self) -> None:
        """Test get hooks with reload=True."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_hooks(reload=True)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/hooks", params={"reload": "true"})


if __name__ == "__main__":
    unittest.main()
