"""Unit tests for HTTP connection utilities."""

import base64
import unittest
from http import HTTPStatus
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import requests
from requests import Response

from python_sbb_polarion.types import AuthScheme, Header, MediaType
from python_sbb_polarion.util.http import HttpConnection


if TYPE_CHECKING:
    from python_sbb_polarion.types import JsonDict


class TestHttpConnection(unittest.TestCase):
    """Test HttpConnection class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_url = "https://example.com"

    @patch("python_sbb_polarion.util.http.Session")
    def test_init_with_bearer_token(self, mock_session_class: Mock) -> None:
        """Test initialization with Bearer token authentication."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        conn = HttpConnection(url=self.base_url, token="test-token-123")

        self.assertEqual(conn.host, self.base_url)
        self.assertEqual(conn._HttpConnection__authorization_headers, {Header.AUTHORIZATION: f"{AuthScheme.BEARER} test-token-123"})  # type: ignore[attr-defined]
        self.assertFalse(mock_session.trust_env)
        mock_session_class.assert_called_once()

    @patch("python_sbb_polarion.util.http.Session")
    def test_init_with_api_key(self, mock_session_class: Mock) -> None:
        """Test initialization with API key authentication."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        conn = HttpConnection(url=self.base_url, api_key="test-api-key")

        self.assertEqual(conn._HttpConnection__authorization_headers, {Header.X_API_KEY: "test-api-key"})  # type: ignore[attr-defined]

    @patch("python_sbb_polarion.util.http.Session")
    def test_init_with_basic_auth(self, mock_session_class: Mock) -> None:
        """Test initialization with Basic authentication."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        conn = HttpConnection(url=self.base_url, username="user", password="pass")

        expected_auth: str = base64.b64encode(b"user:pass").decode("utf-8")
        self.assertEqual(conn._HttpConnection__authorization_headers, {Header.AUTHORIZATION: f"{AuthScheme.BASIC} {expected_auth}"})  # type: ignore[attr-defined]

    @patch("python_sbb_polarion.util.http.Session")
    def test_init_with_custom_content_type(self, mock_session_class: Mock) -> None:
        """Test initialization with custom content type."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        conn = HttpConnection(url=self.base_url, token="token", content_type=MediaType.XML, accept=MediaType.HTML)

        expected_headers: dict[str, str] = {Header.CONTENT_TYPE: MediaType.XML, Header.ACCEPT: MediaType.HTML, Header.AUTHORIZATION: f"{AuthScheme.BEARER} token"}
        self.assertEqual(conn._HttpConnection__default_connection_headers, expected_headers)  # type: ignore[attr-defined]

    @patch("python_sbb_polarion.util.http.Session")
    def test_init_with_trust_env(self, mock_session_class: Mock) -> None:
        """Test initialization with trust_env enabled."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        HttpConnection(url=self.base_url, token="token", trust_env=True)

        self.assertTrue(mock_session.trust_env)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_get_success(self, mock_session_class: Mock) -> None:
        """Test successful GET request."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        url: str = "/api/test"
        response: Response = conn.api_request_get(url)

        self.assertEqual(response, mock_response)
        mock_session.request.assert_called_once()
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertEqual(call_args[1]["url"], f"{self.base_url}/api/test")
        self.assertEqual(call_args[1]["verify"], True)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_post_with_data(self, mock_session_class: Mock) -> None:
        """Test POST request with JSON data."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.CREATED
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        test_data: dict[str, str] = {"key": "value"}
        url: str = "/api/test"
        response: Response = conn.api_request_post(url, data=test_data)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertEqual(call_args[1]["json"], test_data)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_post_with_payload(self, mock_session_class: Mock) -> None:
        """Test POST request with raw payload."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        payload: str = "raw data"
        url: str = "/api/test"
        response: Response = conn.api_request_post(url, payload=payload)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[1]["data"], payload)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_patch(self, mock_session_class: Mock) -> None:
        """Test PATCH request."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        url: str = "/api/test"
        data: dict[str, str] = {
            "update": "value",
        }
        response: Response = conn.api_request_patch(url, data=data)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[0][0], "PATCH")

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_put(self, mock_session_class: Mock) -> None:
        """Test PUT request."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        url: str = "/api/test"
        data: dict[str, str] = {
            "replace": "value",
        }
        response: Response = conn.api_request_put(url, data=data)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[0][0], "PUT")

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_delete(self, mock_session_class: Mock) -> None:
        """Test DELETE request."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.NO_CONTENT
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        url: str = "/api/test/123"
        response: Response = conn.api_request_delete(url)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[0][0], "DELETE")

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_params(self, mock_session_class: Mock) -> None:
        """Test request with query parameters."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        params: JsonDict = {
            "filter": "active",
            "limit": 10,
        }
        url: str = "/api/test"
        response: Response = conn.api_request_get(url, params=params)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        # Params are converted to strings in http.py
        self.assertEqual(call_args[1]["params"], {"filter": "active", "limit": "10"})

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_complex_params(self, mock_session_class: Mock) -> None:
        """Test request with dict/list/None params - should be converted properly."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        params: JsonDict = {
            "dict_param": {"key": "value"},
            "list_param": [1, 2, 3],
            "none_param": None,
            "str_param": "test",
        }
        url: str = "/api/test"
        response: Response = conn.api_request_get(url, params=params)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        # Complex params are converted: dict/list to JSON, None to "", others to str
        expected_params: dict[str, str] = {
            "dict_param": '{"key": "value"}',
            "list_param": "[1, 2, 3]",
            "none_param": "",
            "str_param": "test",
        }
        self.assertEqual(call_args[1]["params"], expected_params)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_list_data(self, mock_session_class: Mock) -> None:
        """Test request with list data."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        list_data: JsonDict = {"x": 1, "y": "2", "z": None}
        url: str = "/api/test"
        response: Response = conn.api_request_post(url, data=list_data)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[1]["json"], list_data)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_string_data(self, mock_session_class: Mock) -> None:
        """Test request with string data."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        str_data: str = "test string"
        url: str = "/api/test"
        response: Response = conn.api_request_post(url, data=str_data)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[1]["json"], str_data)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_bool_data(self, mock_session_class: Mock) -> None:
        """Test request with boolean data."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        bool_data: bool = True
        url: str = "/api/test"
        response: Response = conn.api_request_post(url, data=bool_data)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[1]["json"], True)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_custom_headers(self, mock_session_class: Mock) -> None:
        """Test request with custom headers."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        custom_headers: dict[str, str] = {"X-Custom": "value"}
        url: str = "/api/test"
        response: Response = conn.api_request_get(url, headers=custom_headers)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        # Custom headers should include authorization
        self.assertIn(Header.AUTHORIZATION, call_args[1]["headers"])
        self.assertIn("X-Custom", call_args[1]["headers"])

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_files(self, mock_session_class: Mock) -> None:
        """Test request with file upload."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        files: dict[str, tuple[str, str]] = {
            "file": ("test.txt", "content"),
        }
        url: str = "/api/upload"
        response: Response = conn.api_request_post(url, files=files)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[1]["files"], files)
        # Content-Type should be removed when files are present
        self.assertNotIn(Header.CONTENT_TYPE, call_args[1]["headers"])

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_error_response(self, mock_session_class: Mock) -> None:
        """Test handling of error response (non-2xx status)."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.NOT_FOUND
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        url: str = "/api/notfound"
        response: Response = conn.api_request_get(url)

        self.assertEqual(response, mock_response)
        self.assertTrue(conn.get_requests_error_occurred())
        # Second call should return False and reset
        self.assertFalse(conn.get_requests_error_occurred())

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_exception(self, mock_session_class: Mock) -> None:
        """Test handling of request exception."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_session.request.side_effect = requests.exceptions.ConnectionError("Connection failed")

        conn = HttpConnection(url=self.base_url, token="token")

        with self.assertRaises(requests.exceptions.ConnectionError):
            url: str = "/api/test"
            conn.api_request_get(url)

    @patch("python_sbb_polarion.util.http.Session")
    def test_api_request_with_allow_redirects(self, mock_session_class: Mock) -> None:
        """Test request with allow_redirects parameter."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        url: str = "/api/test"
        response: Response = conn.api_request_get(url, allow_redirects=False)

        self.assertEqual(response, mock_response)
        call_args: Mock = mock_session.request.call_args
        self.assertEqual(call_args[1]["allow_redirects"], False)

    @patch("python_sbb_polarion.util.http.Session")
    def test_set_print_error(self, mock_session_class: Mock) -> None:
        """Test set_print_error method."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        conn = HttpConnection(url=self.base_url, token="token")
        conn.set_print_error(False)

        # Error logging should be disabled
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_session.request.return_value = mock_response

        with patch("python_sbb_polarion.util.http.logger") as mock_logger:
            url: str = "/api/test"
            conn.api_request_get(url)
            # Logger should not be called when print_error is False
            mock_logger.error.assert_not_called()

    @patch("python_sbb_polarion.util.http.Session")
    def test_init_with_print_error_false(self, mock_session_class: Mock) -> None:
        """Test initialization with print_error disabled."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        conn = HttpConnection(url=self.base_url, token="token", print_error=False)

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_session.request.return_value = mock_response

        with patch("python_sbb_polarion.util.http.logger") as mock_logger:
            url: str = "/api/test"
            conn.api_request_get(url)
            mock_logger.error.assert_not_called()

    @patch("python_sbb_polarion.util.http.Session")
    def test_request_error_state_reset(self, mock_session_class: Mock) -> None:
        """Test that request error state is properly reset."""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_session.request.return_value = mock_response

        conn = HttpConnection(url=self.base_url, token="token")
        url: str = "/api/test"
        conn.api_request_get(url)

        # First call should return True
        self.assertTrue(conn.get_requests_error_occurred())
        # Second call should return False (reset)
        self.assertFalse(conn.get_requests_error_occurred())
        # Third call should still return False
        self.assertFalse(conn.get_requests_error_occurred())


if __name__ == "__main__":
    unittest.main()
