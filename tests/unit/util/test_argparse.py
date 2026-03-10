"""Unit tests for argument parsing utilities."""

from __future__ import annotations

import sys
import unittest
from typing import TYPE_CHECKING
from unittest.mock import patch

from python_sbb_polarion.util.argparse import get_script_arguments


if TYPE_CHECKING:
    import argparse


class TestGetScriptArguments(unittest.TestCase):
    """Test get_script_arguments function."""

    def test_default_arguments(self) -> None:
        """Test parsing with no command line arguments."""
        with patch.object(sys, "argv", ["script.py"]):
            args: argparse.Namespace = get_script_arguments()

            self.assertIsNone(args.app_url)
            self.assertIsNone(args.app_token)
            self.assertIsNone(args.app_username)
            self.assertIsNone(args.app_password)
            self.assertIsNone(args.ssh_username)
            self.assertIsNone(args.ssh_private_key_path)
            self.assertIsNone(args.ssh_private_key_password)
            self.assertEqual(args.postgres_db_name, "postgres")
            self.assertIsNone(args.postgres_username)
            self.assertIsNone(args.postgres_password)
            self.assertIsNone(args.apim_client_id)
            self.assertIsNone(args.apim_client_secret)
            self.assertIsNone(args.apim_api_key)
            self.assertIsNone(args.apim_token_endpoint)
            self.assertIsNone(args.smtp_host)
            self.assertIsNone(args.smtp_port)
            self.assertIsNone(args.smtp_username)
            self.assertIsNone(args.smtp_password)
            self.assertIsNone(args.tc_polarion_image_name)
            self.assertIsNone(args.tc_weasyprint_service_image_name)
            self.assertIsNone(args.tc_extension_version)
            self.assertIsNone(args.tc_additional_bundles)
            self.assertIsNone(args.tc_admin_utility_version)

    def test_app_url_argument(self) -> None:
        """Test --app_url argument."""
        with patch.object(sys, "argv", ["script.py", "--app_url", "https://custom.com"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.app_url, "https://custom.com")

    def test_app_token_argument(self) -> None:
        """Test --app_token argument."""
        with patch.object(sys, "argv", ["script.py", "--app_token", "abc123"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.app_token, "abc123")

    def test_app_username_argument(self) -> None:
        """Test --app_username argument."""
        with patch.object(sys, "argv", ["script.py", "--app_username", "testuser"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.app_username, "testuser")

    def test_app_password_argument(self) -> None:
        """Test --app_password argument."""
        with patch.object(sys, "argv", ["script.py", "--app_password", "testpass"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.app_password, "testpass")

    def test_ssh_username_argument(self) -> None:
        """Test --ssh_username argument."""
        with patch.object(sys, "argv", ["script.py", "--ssh_username", "sshuser"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.ssh_username, "sshuser")

    def test_ssh_private_key_path_argument(self) -> None:
        """Test --ssh_private_key_path argument."""
        with patch.object(sys, "argv", ["script.py", "--ssh_private_key_path", "/path/to/key"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.ssh_private_key_path, "/path/to/key")

    def test_ssh_private_key_password_argument(self) -> None:
        """Test --ssh_private_key_password argument."""
        with patch.object(sys, "argv", ["script.py", "--ssh_private_key_password", "keypass"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.ssh_private_key_password, "keypass")

    def test_postgres_arguments(self) -> None:
        """Test postgres-related arguments."""
        with patch.object(sys, "argv", ["script.py", "--postgres_db_name", "mydb", "--postgres_username", "pguser", "--postgres_password", "pgpass"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.postgres_db_name, "mydb")
            self.assertEqual(args.postgres_username, "pguser")
            self.assertEqual(args.postgres_password, "pgpass")

    def test_postgres_db_name_default(self) -> None:
        """Test postgres_db_name default value."""
        with patch.object(sys, "argv", ["script.py"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.postgres_db_name, "postgres")

    def test_apim_client_id_argument(self) -> None:
        """Test --apim_client_id argument."""
        with patch.object(sys, "argv", ["script.py", "--apim_client_id", "client123"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.apim_client_id, "client123")

    def test_apim_client_secret_argument(self) -> None:
        """Test --apim_client_secret argument."""
        with patch.object(sys, "argv", ["script.py", "--apim_client_secret", "secret123"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.apim_client_secret, "secret123")

    def test_apim_api_key_argument(self) -> None:
        """Test --apim_api_key argument."""
        with patch.object(sys, "argv", ["script.py", "--apim_api_key", "apikey123"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.apim_api_key, "apikey123")

    def test_apim_token_endpoint_argument(self) -> None:
        """Test --apim_token_endpoint argument."""
        with patch.object(sys, "argv", ["script.py", "--apim_token_endpoint", "https://token.example.com"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.apim_token_endpoint, "https://token.example.com")

    def test_smtp_arguments(self) -> None:
        """Test SMTP-related arguments."""
        with patch.object(sys, "argv", ["script.py", "--smtp_host", "smtp.example.com", "--smtp_port", "587", "--smtp_username", "user", "--smtp_password", "pass"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.smtp_host, "smtp.example.com")
            self.assertEqual(args.smtp_port, "587")
            self.assertEqual(args.smtp_username, "user")
            self.assertEqual(args.smtp_password, "pass")

    def test_testcontainer_arguments(self) -> None:
        """Test testcontainer-related arguments."""
        with patch.object(sys, "argv", ["script.py", "--tc_polarion_image_name", "polarion:latest", "--tc_weasyprint_service_image_name", "weasyprint:latest"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.tc_polarion_image_name, "polarion:latest")
            self.assertEqual(args.tc_weasyprint_service_image_name, "weasyprint:latest")

    def test_tc_extension_version_argument(self) -> None:
        """Test --tc_extension_version argument."""
        with patch.object(sys, "argv", ["script.py", "--tc_extension_version", "1.2.3"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.tc_extension_version, "1.2.3")

    def test_tc_additional_bundles_argument(self) -> None:
        """Test --tc_additional_bundles argument."""
        with patch.object(sys, "argv", ["script.py", "--tc_additional_bundles", "group:artifact:1.0.0"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.tc_additional_bundles, "group:artifact:1.0.0")

    def test_tc_admin_utility_version_argument(self) -> None:
        """Test --tc_admin_utility_version argument."""
        with patch.object(sys, "argv", ["script.py", "--tc_admin_utility_version", "2.0.0"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.tc_admin_utility_version, "2.0.0")

    def test_multiple_arguments_combined(self) -> None:
        """Test multiple arguments combined."""
        with patch.object(sys, "argv", ["script.py", "--app_url", "https://test.com", "--app_token", "token", "--ssh_username", "sshuser", "--postgres_username", "pguser"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.app_url, "https://test.com")
            self.assertEqual(args.app_token, "token")
            self.assertEqual(args.ssh_username, "sshuser")
            self.assertEqual(args.postgres_username, "pguser")

    def test_unknown_arguments_ignored(self) -> None:
        """Test that unknown arguments are ignored gracefully."""
        with patch.object(sys, "argv", ["script.py", "--unknown_arg", "value", "--app_url", "https://test.com"]):
            args: argparse.Namespace = get_script_arguments()
            self.assertEqual(args.app_url, "https://test.com")
            # Unknown arguments should not raise an error


if __name__ == "__main__":
    unittest.main()
