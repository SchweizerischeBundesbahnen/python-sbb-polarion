"""Unit tests for SSH tunnel utilities."""

import unittest
from typing import Any
from unittest.mock import Mock, patch

from python_sbb_polarion.util.sshtunnel import SshTunnelConnection


class TestSshTunnelConnection(unittest.TestCase):
    """Test SshTunnelConnection class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.host = "example.com"
        self.port = 5432  # PostgreSQL default port
        self.ssh_username = "testuser"
        self.ssh_private_key_password = "keypass"

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_init_success(self, mock_open_tunnel: Mock) -> None:
        """Test successful SSH tunnel initialization."""
        mock_tunnel = Mock()
        mock_tunnel.local_bind_port = 12345
        mock_open_tunnel.return_value = mock_tunnel

        conn = SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username, ssh_private_key_password=self.ssh_private_key_password)

        # Verify tunnel was created with correct parameters
        mock_open_tunnel.assert_called_once_with(
            (self.host, 22),  # Default SSH port
            ssh_username=self.ssh_username,
            ssh_pkey=None,
            ssh_private_key_password=self.ssh_private_key_password,
            allow_agent=True,
            remote_bind_address=("localhost", self.port),
        )
        mock_tunnel.start.assert_called_once()
        self.assertEqual(conn.ssh_tunnel_forward, mock_tunnel)

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_init_with_custom_ssh_port(self, mock_open_tunnel: Mock) -> None:
        """Test initialization with custom SSH port."""
        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel
        custom_ssh_port: int = 2222

        SshTunnelConnection(self.host, self.port, ssh_port=custom_ssh_port, ssh_username=self.ssh_username)

        # Verify custom SSH port was used
        call_args: Any = mock_open_tunnel.call_args
        self.assertEqual(call_args[0][0], (self.host, custom_ssh_port))

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_init_with_private_key_file(self, mock_open_tunnel: Mock) -> None:
        """Test initialization with private key file."""
        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel
        key_path: str = "/path/to/key"

        SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username, ssh_private_key_path=key_path)

        call_args: Any = mock_open_tunnel.call_args
        self.assertEqual(call_args[1]["ssh_pkey"], key_path)

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_init_with_allow_agent_false(self, mock_open_tunnel: Mock) -> None:
        """Test initialization with allow_agent disabled."""
        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel

        SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username, allow_agent=False)

        call_args: Any = mock_open_tunnel.call_args
        self.assertEqual(call_args[1]["allow_agent"], False)

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    @patch("python_sbb_polarion.util.sshtunnel.logger")
    def test_init_with_print_info_true(self, mock_logger: Mock, mock_open_tunnel: Mock) -> None:
        """Test initialization with print_info enabled."""
        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel

        SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username, print_info=True)

        mock_logger.info.assert_called_once_with("SSH tunnel established to %s:%d -> localhost:%d", self.host, 22, self.port)

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    @patch("python_sbb_polarion.util.sshtunnel.logger")
    def test_init_with_print_info_false(self, mock_logger: Mock, mock_open_tunnel: Mock) -> None:
        """Test initialization with print_info disabled."""
        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel

        SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username, print_info=False)

        # Info should not be logged
        mock_logger.info.assert_not_called()

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    @patch("python_sbb_polarion.util.sshtunnel.logger")
    def test_init_tunnel_error(self, mock_logger: Mock, mock_open_tunnel: Mock) -> None:
        """Test handling of tunnel creation errors."""
        import sshtunnel

        mock_open_tunnel.side_effect = sshtunnel.BaseSSHTunnelForwarderError("Tunnel creation failed")

        # Now the code raises the exception instead of suppressing it
        with self.assertRaises(sshtunnel.BaseSSHTunnelForwarderError):
            SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username)

        mock_logger.exception.assert_called_once_with("SSH tunnel failed to %s:%d", self.host, 22)

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_get_local_bind_port(self, mock_open_tunnel: Mock) -> None:
        """Test get_local_bind_port method."""
        mock_tunnel = Mock()
        mock_tunnel.local_bind_port = 54321
        mock_open_tunnel.return_value = mock_tunnel

        conn = SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username)
        local_port: int = conn.get_local_bind_port()

        self.assertEqual(local_port, 54321)

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_get_local_bind_port_different_values(self, mock_open_tunnel: Mock) -> None:
        """Test get_local_bind_port with different port values."""
        test_ports: list[int] = [12345, 23456, 34567, 45678]

        for port in test_ports:
            mock_tunnel = Mock()
            mock_tunnel.local_bind_port = port
            mock_open_tunnel.return_value = mock_tunnel

            conn = SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username)
            local_port: int = conn.get_local_bind_port()

            self.assertEqual(local_port, port)

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    @patch("python_sbb_polarion.util.sshtunnel.logger")
    def test_close_ssh_tunnel(self, mock_logger: Mock, mock_open_tunnel: Mock) -> None:
        """Test close_ssh_tunnel method."""
        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel

        conn = SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username)
        conn.close_ssh_tunnel()

        mock_tunnel.close.assert_called_once()
        mock_logger.info.assert_called_with("SSH tunnel closed")

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_tunnel_with_multiple_parameters(self, mock_open_tunnel: Mock) -> None:
        """Test tunnel creation with all parameters."""
        mock_tunnel = Mock()
        mock_tunnel.local_bind_port = 12345
        mock_open_tunnel.return_value = mock_tunnel

        conn = SshTunnelConnection(
            self.host,
            self.port,
            ssh_port=2222,
            ssh_username=self.ssh_username,
            ssh_private_key_password=self.ssh_private_key_password,
            ssh_private_key_path="/path/to/key",
            allow_agent=False,
            print_info=True,
        )

        # Verify all parameters were passed correctly
        call_args: Any = mock_open_tunnel.call_args
        self.assertEqual(call_args[0][0], (self.host, 2222))
        self.assertEqual(call_args[1]["ssh_username"], self.ssh_username)
        self.assertEqual(call_args[1]["ssh_pkey"], "/path/to/key")
        self.assertEqual(call_args[1]["ssh_private_key_password"], self.ssh_private_key_password)
        self.assertEqual(call_args[1]["allow_agent"], False)
        self.assertEqual(call_args[1]["remote_bind_address"], ("localhost", self.port))

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_remote_bind_address_format(self, mock_open_tunnel: Mock) -> None:
        """Test that remote_bind_address is always (localhost, port)."""
        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel

        test_ports: list[int] = [5432, 3306, 6379, 27017]

        for port in test_ports:
            mock_open_tunnel.reset_mock()
            SshTunnelConnection(self.host, port, ssh_username=self.ssh_username)

            call_args: Any = mock_open_tunnel.call_args
            self.assertEqual(call_args[1]["remote_bind_address"], ("localhost", port))

    @patch("python_sbb_polarion.util.sshtunnel.sshtunnel.open_tunnel")
    def test_close_ssh_tunnel_exception(self, mock_open_tunnel: Mock) -> None:
        """Test close_ssh_tunnel handles exceptions."""
        import sshtunnel

        mock_tunnel = Mock()
        mock_open_tunnel.return_value = mock_tunnel
        mock_tunnel.close.side_effect = sshtunnel.BaseSSHTunnelForwarderError("Close error")

        conn = SshTunnelConnection(self.host, self.port, ssh_username=self.ssh_username)

        with self.assertRaises(sshtunnel.BaseSSHTunnelForwarderError):
            conn.close_ssh_tunnel()


if __name__ == "__main__":
    unittest.main()
