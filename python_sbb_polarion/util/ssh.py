"""Common implementation for SSH connections."""

import logging
from typing import TypedDict, Unpack

import paramiko


logger = logging.getLogger(__name__)


class SshConnectionConfig(TypedDict, total=False):
    """Configuration parameters for SSH connection."""

    ssh_username: str
    ssh_private_key_password: str
    print_info: bool


class SshConnection:
    """SSH connection manager using Paramiko."""

    def __init__(self, host: str, port: int = 22, **kwargs: Unpack[SshConnectionConfig]) -> None:
        """Initialize SSH connection.

        Args:
            host: SSH server hostname or IP address
            port: SSH server port (default: 22)
            **kwargs: SSH connection parameters
                ssh_username: SSH username for authentication
                ssh_private_key_password: Passphrase for SSH private key
                print_info: Enable info logging (default: True)

        Raises:
            paramiko.SSHException: If SSH connection fails
            paramiko.AuthenticationException: If authentication fails
        """
        ssh_username: str | None = kwargs.get("ssh_username")
        ssh_private_key_password: str | None = kwargs.get("ssh_private_key_password")
        print_info: bool = kwargs.get("print_info", True)

        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
            self.client.connect(host, port=port, username=ssh_username, passphrase=ssh_private_key_password)
            # enable SSH agent forwarding for a session
            # https://stackoverflow.com/questions/23666600/ssh-key-forwarding-using-python-paramiko
            # self.session = self.client.get_transport().open_session()
            # paramiko.agent.AgentRequestHandler(self.session)
            if print_info:
                logger.info("SSH connection established to %s:%d", host, port)
        except (paramiko.SSHException, paramiko.AuthenticationException):
            logger.exception("SSH connection failed to %s:%d", host, port)
            raise

    def exec_command(self, command: str) -> tuple[str, str]:
        """Execute command over SSH connection.

        Args:
            command: Shell command to execute on remote server

        Returns:
            tuple[str, str]: A tuple containing (stdout output, stderr output) as decoded UTF-8 strings

        Raises:
            paramiko.SSHException: If command execution fails
        """
        try:
            stdout: paramiko.channel.ChannelFile
            stderr: paramiko.channel.ChannelStderrFile
            (_stdin, stdout, stderr) = self.client.exec_command(command)
            stdout_str: str = stdout.read().decode("utf-8")
            stderr_str: str = stderr.read().decode("utf-8")
            logger.debug("Command executed: %s", command)
            return stdout_str, stderr_str  # noqa: TRY300
        except paramiko.SSHException:
            logger.exception("Failed to execute command: %s", command)
            raise

    def __del__(self) -> None:
        """Close SSH connection on object destruction."""
        if hasattr(self, "client"):
            try:
                self.client.close()
                logger.debug("SSH connection closed")
            except Exception:  # noqa: S110
                # Suppress all exceptions in destructor to avoid issues during interpreter shutdown
                pass
