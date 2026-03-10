"""Unit tests for LDAP connection utilities."""

import json
import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock, mock_open, patch

from python_sbb_polarion.util.ldap import LDAP_BASE_DN, LDAP_SERVER_NAME, LdapConnection


if TYPE_CHECKING:
    from python_sbb_polarion.types import JsonDict


class TestLdapConnection(unittest.TestCase):
    """Test LdapConnection class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.user_name = "test@example.com"
        self.user_password = "testpass"
        self.server_name = LDAP_SERVER_NAME

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_init_without_cache_file(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test initialization when cache file does not exist."""
        mock_exists.return_value = False
        mock_server_instance = Mock()
        mock_server.return_value = mock_server_instance
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        conn = LdapConnection(self.user_name, self.user_password)

        # Verify server was created
        mock_server.assert_called_once_with(LDAP_SERVER_NAME, use_ssl=True, get_info=unittest.mock.ANY)
        # Verify connection was created
        mock_connection.assert_called_once()
        # Verify empty user cache
        self.assertEqual(conn.ldap_users, {})
        self.assertEqual(conn.ldap_groups, {})

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    @patch("pathlib.Path.open", new_callable=mock_open, read_data='{"user1": {"name": "User One"}}')
    def test_init_with_cache_file(self, mock_file: Mock, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test initialization when cache file exists."""
        mock_exists.return_value = True
        mock_server_instance = Mock()
        mock_server.return_value = mock_server_instance
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        conn = LdapConnection(self.user_name, self.user_password)

        # Verify cache was loaded
        self.assertEqual(conn.ldap_users, {"user1": {"name": "User One"}})

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_init_with_custom_server_name(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test initialization with custom server name."""
        mock_exists.return_value = False
        mock_server_instance = Mock()
        mock_server.return_value = mock_server_instance
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance
        custom_server: str = "custom.example.com"

        conn = LdapConnection(self.user_name, self.user_password, server_name=custom_server)

        mock_server.assert_called_once_with(custom_server, use_ssl=True, get_info=unittest.mock.ANY)

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_get_info_about_user_not_cached(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test getting user info when not in cache."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        # Mock LDAP search result
        mock_entry = Mock()
        mock_entry.entry_to_json.return_value = '{"userPrincipalName": "user@example.com", "msDS-ExternalDirectoryObjectId": "User_123"}'
        mock_conn_instance.entries = [mock_entry]

        conn = LdapConnection(self.user_name, self.user_password)
        result: JsonDict = conn.get_info_about_user("testuser")

        # Verify LDAP search was performed
        mock_conn_instance.search.assert_called_once_with(search_base=LDAP_BASE_DN, search_filter="(sAMAccountName=testuser)", attributes=unittest.mock.ANY)
        # Verify result was cached and returned
        self.assertIn("testuser", conn.ldap_users)
        self.assertEqual(result["userPrincipalName"], "user@example.com")

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_get_info_about_user_cached(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test getting user info when already in cache."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        conn = LdapConnection(self.user_name, self.user_password)
        # Pre-populate cache
        cached_data: JsonDict = {"userPrincipalName": "cached@example.com"}
        conn.ldap_users["testuser"] = cached_data

        result: JsonDict = conn.get_info_about_user("testuser")

        # Verify LDAP search was NOT performed
        mock_conn_instance.search.assert_not_called()
        # Verify cached data was returned
        self.assertEqual(result, cached_data)

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_get_info_about_user_not_found(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test getting user info when user is not found."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance
        mock_conn_instance.entries = []  # Empty result

        conn = LdapConnection(self.user_name, self.user_password)
        result: JsonDict = conn.get_info_about_user("nonexistent")

        # Verify empty dict is returned and cached
        self.assertEqual(result, {})
        self.assertEqual(conn.ldap_users["nonexistent"], {})

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_get_user_object_id(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test get_user_object_id method."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        conn = LdapConnection(self.user_name, self.user_password)
        # Pre-populate cache with object ID
        conn.ldap_users["testuser"] = {"msDS-ExternalDirectoryObjectId": "User_abc-123-def"}

        object_id: str = conn.get_user_object_id("testuser")

        self.assertEqual(object_id, "abc-123-def")

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_get_user_object_id_not_found(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test get_user_object_id when user not found."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        conn = LdapConnection(self.user_name, self.user_password)
        conn.ldap_users["testuser"] = {}  # Empty user data

        object_id: str = conn.get_user_object_id("testuser")

        self.assertEqual(object_id, "")

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_get_user_email_address(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test get_user_email_address method."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        conn = LdapConnection(self.user_name, self.user_password)
        # Pre-populate cache with email
        conn.ldap_users["testuser"] = {"userPrincipalName": "test@example.com"}

        email: str = conn.get_user_email_address("testuser")

        self.assertEqual(email, "test@example.com")

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_get_user_email_address_not_found(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test get_user_email_address when user not found."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        conn = LdapConnection(self.user_name, self.user_password)
        conn.ldap_users["testuser"] = {}  # Empty user data

        email: str = conn.get_user_email_address("testuser")

        self.assertEqual(email, "")

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    @patch("pathlib.Path.open", new_callable=mock_open)
    def test_destructor_saves_cache(self, mock_file: Mock, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test that __del__ saves cache to file."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_connection.return_value = Mock()

        conn = LdapConnection(self.user_name, self.user_password)
        conn.ldap_users = {"user1": {"name": "User One"}, "user2": {"name": "User Two"}}

        conn.__del__()

        # Verify file was opened for writing
        mock_file.assert_called_once()
        # Verify json.dump was called (through the file write)
        handle: Mock = mock_file()
        self.assertTrue(handle.write.called)

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path.exists")
    def test_multiple_user_lookups(self, mock_exists: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test looking up multiple users."""
        mock_exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance

        # Mock different responses for different users
        def mock_search(search_base: str, search_filter: str, attributes: list[str]) -> None:
            if "user1" in search_filter:
                mock_entry = Mock()
                mock_entry.entry_to_json.return_value = '{"userPrincipalName": "user1@example.com"}'
                mock_conn_instance.entries = [mock_entry]
            elif "user2" in search_filter:
                mock_entry = Mock()
                mock_entry.entry_to_json.return_value = '{"userPrincipalName": "user2@example.com"}'
                mock_conn_instance.entries = [mock_entry]

        mock_conn_instance.search.side_effect = mock_search

        conn = LdapConnection(self.user_name, self.user_password)

        result1: JsonDict = conn.get_info_about_user("user1")
        result2: JsonDict = conn.get_info_about_user("user2")

        self.assertEqual(result1["userPrincipalName"], "user1@example.com")
        self.assertEqual(result2["userPrincipalName"], "user2@example.com")
        # Both should be cached
        self.assertIn("user1", conn.ldap_users)
        self.assertIn("user2", conn.ldap_users)

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path")
    @patch("python_sbb_polarion.util.ldap.json.load")
    def test_init_with_corrupted_cache_file(self, mock_json_load: Mock, mock_path: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test initialization with corrupted cache file."""
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.open.return_value.__enter__.return_value = Mock()
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        mock_server.return_value = Mock()
        mock_connection.return_value = Mock()

        # Should handle corrupted cache gracefully
        conn = LdapConnection(self.user_name, self.user_password)
        self.assertEqual(conn.ldap_users, {})

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path")
    def test_get_info_about_user_ldap_exception(self, mock_path: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test LDAP search exception handling."""
        import ldap3.core.exceptions

        mock_path.return_value.exists.return_value = False
        mock_server.return_value = Mock()
        mock_conn_instance = Mock()
        mock_connection.return_value = mock_conn_instance
        mock_conn_instance.search.side_effect = ldap3.core.exceptions.LDAPException("LDAP error")

        conn = LdapConnection(self.user_name, self.user_password)
        result: JsonDict = conn.get_info_about_user("testuser")

        # Should return empty dict on LDAP error
        self.assertEqual(result, {})

    @patch("python_sbb_polarion.util.ldap.ldap3.Connection")
    @patch("python_sbb_polarion.util.ldap.ldap3.Server")
    @patch("python_sbb_polarion.util.ldap.pathlib.Path")
    def test_destructor_with_write_error(self, mock_path: Mock, mock_server: Mock, mock_connection: Mock) -> None:
        """Test destructor handles cache write errors gracefully."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False
        mock_path_instance.open.side_effect = OSError("Cannot write file")

        mock_server.return_value = Mock()
        mock_connection.return_value = Mock()

        conn = LdapConnection(self.user_name, self.user_password)
        conn.ldap_users["test"] = {"data": "value"}

        # Should not raise exception
        conn.__del__()


if __name__ == "__main__":
    unittest.main()
