"""Unit tests for OAuth2 authentication utilities."""

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from python_sbb_polarion.types import AuthScheme
from python_sbb_polarion.util.oauth import get_oauth2_client_credentials


class TestGetOAuth2ClientCredentials(unittest.TestCase):
    """Test get_oauth2_client_credentials function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.client_id = "test-client-id"
        self.client_secret = "test-client-secret"
        self.token_endpoint = "https://example.com/oauth/token"

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_success(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test successful OAuth2 token retrieval."""
        # Mock HTTPBasicAuth
        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth

        # Mock BackendApplicationClient
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client

        # Mock OAuth2Session
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.return_value = {"access_token": "test-access-token-123", "token_type": AuthScheme.BEARER, "expires_in": 3600}

        # Call the function
        token: str = get_oauth2_client_credentials(self.client_id, self.client_secret, self.token_endpoint)

        # Verify HTTPBasicAuth was created with correct credentials
        mock_http_basic_auth.assert_called_once_with(self.client_id, self.client_secret)

        # Verify BackendApplicationClient was created with client_id
        mock_backend_client_class.assert_called_once_with(client_id=self.client_id)

        # Verify OAuth2Session was created with the client
        mock_oauth_session_class.assert_called_once_with(client=mock_client)

        # Verify fetch_token was called with correct parameters
        mock_session.fetch_token.assert_called_once_with(token_url=self.token_endpoint, auth=mock_auth)

        # Verify the access token was returned
        self.assertEqual(token, "test-access-token-123")

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_different_token(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test with different access token."""
        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.return_value = {"access_token": "different-token-xyz", "token_type": AuthScheme.BEARER}

        token: str = get_oauth2_client_credentials(self.client_id, self.client_secret, self.token_endpoint)

        self.assertEqual(token, "different-token-xyz")

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_with_extra_fields(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test token response with extra fields."""
        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session

        # Token response with extra fields
        mock_session.fetch_token.return_value = {
            "access_token": "token-with-extras",
            "token_type": AuthScheme.BEARER,
            "expires_in": 7200,
            "refresh_token": "refresh-token",
            "scope": "read write",
        }

        token: str = get_oauth2_client_credentials(self.client_id, self.client_secret, self.token_endpoint)

        # Should only extract access_token
        self.assertEqual(token, "token-with-extras")

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_different_endpoint(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test with different token endpoint."""
        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.return_value = {"access_token": "token123"}

        different_endpoint: str = "https://different.com/token"
        token: str = get_oauth2_client_credentials(self.client_id, self.client_secret, different_endpoint)

        # Verify fetch_token was called with different endpoint
        mock_session.fetch_token.assert_called_once_with(token_url=different_endpoint, auth=mock_auth)
        self.assertEqual(token, "token123")

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_different_credentials(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test with different client credentials."""
        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.return_value = {"access_token": "token"}

        different_id: str = "another-client-id"
        different_secret: str = "another-client-secret"

        token: str = get_oauth2_client_credentials(different_id, different_secret, self.token_endpoint)

        # Verify HTTPBasicAuth was called with different credentials
        mock_http_basic_auth.assert_called_once_with(different_id, different_secret)
        # Verify BackendApplicationClient was created with different client_id
        mock_backend_client_class.assert_called_once_with(client_id=different_id)

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_fetch_token_error(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test handling of fetch_token errors."""
        from oauthlib.oauth2.rfc6749.errors import OAuth2Error

        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.side_effect = OAuth2Error("Invalid credentials")

        with self.assertRaises(OAuth2Error):
            get_oauth2_client_credentials(self.client_id, self.client_secret, self.token_endpoint)

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_request_exception(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test handling of request exceptions."""
        from requests.exceptions import RequestException

        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.side_effect = RequestException("Network error")

        with self.assertRaises(RequestException):
            get_oauth2_client_credentials(self.client_id, self.client_secret, self.token_endpoint)

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_get_oauth2_client_credentials_missing_access_token(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test handling of missing access_token in response."""
        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.return_value = {"token_type": AuthScheme.BEARER}  # Missing access_token

        with self.assertRaises(KeyError):
            get_oauth2_client_credentials(self.client_id, self.client_secret, self.token_endpoint)

    @patch("python_sbb_polarion.util.oauth.OAuth2Session")
    @patch("python_sbb_polarion.util.oauth.BackendApplicationClient")
    @patch("python_sbb_polarion.util.oauth.HTTPBasicAuth")
    def test_backend_application_client_flow(self, mock_http_basic_auth: Mock, mock_backend_client_class: Mock, mock_oauth_session_class: Mock) -> None:
        """Test that BackendApplicationClient is used (not other OAuth2 flows)."""
        mock_auth = Mock()
        mock_http_basic_auth.return_value = mock_auth
        mock_client = Mock()
        mock_backend_client_class.return_value = mock_client
        mock_session = Mock()
        mock_oauth_session_class.return_value = mock_session
        mock_session.fetch_token.return_value = {"access_token": "token"}

        get_oauth2_client_credentials(self.client_id, self.client_secret, self.token_endpoint)

        # Verify BackendApplicationClient was used (client credentials flow)
        mock_backend_client_class.assert_called_once_with(client_id=self.client_id)
        # Verify OAuth2Session was created with the backend client
        mock_oauth_session_class.assert_called_once_with(client=mock_client)


if __name__ == "__main__":
    unittest.main()
