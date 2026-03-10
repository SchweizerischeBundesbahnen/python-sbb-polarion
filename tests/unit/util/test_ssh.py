"""Unit tests for SSH connection utilities."""

import unittest
from unittest.mock import Mock, patch

from python_sbb_polarion.util.ssh import SshConnection


class TestSshConnection(unittest.TestCase):
    """Test SshConnection class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.host = "example.com"
        self.port = 22
        self.ssh_username = "testuser"
        self.ssh_private_key_password = "keypass"

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_init_success(self, mock_ssh_client_class: Mock) -> None:
        """Test successful SSH connection initialization."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        conn = SshConnection(self.host, self.port, ssh_username=self.ssh_username, ssh_private_key_password=self.ssh_private_key_password)

        # Verify SSHClient was created and configured
        mock_ssh_client_class.assert_called_once()
        mock_client.load_system_host_keys.assert_called_once()
        mock_client.set_missing_host_key_policy.assert_called_once()
        mock_client.connect.assert_called_once_with(self.host, port=self.port, username=self.ssh_username, passphrase=self.ssh_private_key_password)
        self.assertEqual(conn.client, mock_client)

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_init_with_default_port(self, mock_ssh_client_class: Mock) -> None:
        """Test initialization with default port."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        conn = SshConnection(self.host, ssh_username=self.ssh_username)

        # Should use port 22 by default
        mock_client.connect.assert_called_once_with(self.host, port=22, username=self.ssh_username, passphrase=None)

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_init_with_custom_port(self, mock_ssh_client_class: Mock) -> None:
        """Test initialization with custom port."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client
        custom_port: int = 2222

        conn = SshConnection(self.host, port=custom_port, ssh_username=self.ssh_username)

        mock_client.connect.assert_called_once_with(self.host, port=custom_port, username=self.ssh_username, passphrase=None)

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    @patch("python_sbb_polarion.util.ssh.logger")
    def test_init_with_print_info_true(self, mock_logger: Mock, mock_ssh_client_class: Mock) -> None:
        """Test initialization with print_info enabled."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        SshConnection(self.host, ssh_username=self.ssh_username, print_info=True)

        mock_logger.info.assert_called_once_with("SSH connection established to %s:%d", self.host, 22)

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    @patch("python_sbb_polarion.util.ssh.logger")
    def test_init_with_print_info_false(self, mock_logger: Mock, mock_ssh_client_class: Mock) -> None:
        """Test initialization with print_info disabled."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        SshConnection(self.host, ssh_username=self.ssh_username, print_info=False)

        mock_logger.info.assert_not_called()

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    @patch("python_sbb_polarion.util.ssh.logger")
    def test_init_connection_error(self, mock_logger: Mock, mock_ssh_client_class: Mock) -> None:
        """Test handling of connection errors during initialization."""
        import paramiko

        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client
        mock_client.connect.side_effect = paramiko.SSHException("Connection failed")

        # Now the code raises the exception instead of suppressing it
        with self.assertRaises(paramiko.SSHException):
            SshConnection(self.host, ssh_username=self.ssh_username)

        mock_logger.exception.assert_called_once_with("SSH connection failed to %s:%d", self.host, 22)

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_exec_command_success(self, mock_ssh_client_class: Mock) -> None:
        """Test successful command execution."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        # Mock command execution
        mock_stdout = Mock()
        mock_stdout.read.return_value = b"output data"
        mock_stderr = Mock()
        mock_stderr.read.return_value = b"error data"
        mock_client.exec_command.return_value = (Mock(), mock_stdout, mock_stderr)

        conn = SshConnection(self.host, ssh_username=self.ssh_username)
        stdout: str
        stderr: str
        stdout, stderr = conn.exec_command("ls -la")

        self.assertEqual(stdout, "output data")
        self.assertEqual(stderr, "error data")
        mock_client.exec_command.assert_called_once_with("ls -la")

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_exec_command_empty_output(self, mock_ssh_client_class: Mock) -> None:
        """Test command execution with empty output."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        mock_stdout = Mock()
        mock_stdout.read.return_value = b""
        mock_stderr = Mock()
        mock_stderr.read.return_value = b""
        mock_client.exec_command.return_value = (Mock(), mock_stdout, mock_stderr)

        conn = SshConnection(self.host, ssh_username=self.ssh_username)
        stdout: str
        stderr: str
        stdout, stderr = conn.exec_command("echo")

        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "")

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_exec_command_unicode(self, mock_ssh_client_class: Mock) -> None:
        """Test command execution with Unicode characters."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        # Unicode test data
        unicode_output: str = "Héllo Wörld 日本語"
        mock_stdout = Mock()
        mock_stdout.read.return_value = unicode_output.encode("utf-8")
        mock_stderr = Mock()
        mock_stderr.read.return_value = b""
        mock_client.exec_command.return_value = (Mock(), mock_stdout, mock_stderr)

        conn = SshConnection(self.host, ssh_username=self.ssh_username)
        stdout: str
        stderr: str
        stdout, stderr = conn.exec_command("echo test")

        self.assertEqual(stdout, unicode_output)
        self.assertEqual(stderr, "")

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_exec_command_multiple_calls(self, mock_ssh_client_class: Mock) -> None:
        """Test multiple command executions."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        # Setup different responses for each call
        responses: list[tuple[Mock, Mock, Mock]] = [
            (Mock(), Mock(read=Mock(return_value=b"output1")), Mock(read=Mock(return_value=b""))),
            (Mock(), Mock(read=Mock(return_value=b"output2")), Mock(read=Mock(return_value=b""))),
            (Mock(), Mock(read=Mock(return_value=b"output3")), Mock(read=Mock(return_value=b""))),
        ]
        mock_client.exec_command.side_effect = responses

        conn = SshConnection(self.host, ssh_username=self.ssh_username)

        stdout1: str
        stdout2: str
        stdout3: str
        stdout1, _ = conn.exec_command("command1")
        stdout2, _ = conn.exec_command("command2")
        stdout3, _ = conn.exec_command("command3")

        self.assertEqual(stdout1, "output1")
        self.assertEqual(stdout2, "output2")
        self.assertEqual(stdout3, "output3")
        self.assertEqual(mock_client.exec_command.call_count, 3)

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_destructor_closes_connection(self, mock_ssh_client_class: Mock) -> None:
        """Test that __del__ closes the SSH connection."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client

        conn = SshConnection(self.host, ssh_username=self.ssh_username)
        conn.__del__()

        mock_client.close.assert_called_once()

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    @patch("python_sbb_polarion.util.ssh.paramiko.RejectPolicy")
    def test_reject_policy_set(self, mock_reject_policy: Mock, mock_ssh_client_class: Mock) -> None:
        """Test that RejectPolicy is set for missing host keys."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client
        mock_policy = Mock()
        mock_reject_policy.return_value = mock_policy

        SshConnection(self.host, ssh_username=self.ssh_username)

        mock_client.set_missing_host_key_policy.assert_called_once()
        # Verify the policy instance was created
        mock_reject_policy.assert_called_once()

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_exec_command_exception(self, mock_ssh_client_class: Mock) -> None:
        """Test exec_command handles SSH exceptions."""
        import paramiko

        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client
        mock_client.exec_command.side_effect = paramiko.SSHException("Command execution failed")

        conn = SshConnection(self.host, ssh_username=self.ssh_username)

        with self.assertRaises(paramiko.SSHException):
            conn.exec_command("ls -la")

    @patch("python_sbb_polarion.util.ssh.paramiko.SSHClient")
    def test_destructor_close_exception(self, mock_ssh_client_class: Mock) -> None:
        """Test destructor handles close exceptions gracefully."""
        mock_client = Mock()
        mock_ssh_client_class.return_value = mock_client
        mock_client.close.side_effect = Exception("Close error")

        conn = SshConnection(self.host, ssh_username=self.ssh_username)
        # Should not raise exception
        conn.__del__()

    def test_destructor_without_client_attribute(self) -> None:
        """Test destructor when object has no client attribute."""
        # Create a minimal object without going through __init__
        conn: SshConnection = object.__new__(SshConnection)
        # Should not raise exception even without client attribute
        conn.__del__()


if __name__ == "__main__":
    unittest.main()
