"""Common implementation for SSH tunneling."""

import logging
from typing import TypedDict, Unpack

import sshtunnel


logger = logging.getLogger(__name__)


class SshTunnelConfig(TypedDict, total=False):
    """Configuration parameters for SSH tunnel connection."""

    ssh_port: int
    ssh_username: str
    ssh_private_key_password: str
    ssh_private_key_path: str
    allow_agent: bool
    print_info: bool


class SshTunnelConnection:
    """SSH tunnel connection manager.

    Equivalent to: ssh -L local_bind_port:127.0.0.1:remote_bind_address host

    Note:
        Paramiko cannot talk to OpenSSH ssh-agent on Windows. It can talk to PuTTY Pageant only.
        In this case, please use ssh_private_key_path instead.
    """

    def __init__(self, host: str, port: int, **kwargs: Unpack[SshTunnelConfig]) -> None:
        """Initialize SSH tunnel connection.

        Args:
            host: SSH server hostname or IP address
            port: Remote port to forward
            **kwargs: SSH tunnel parameters
                ssh_port: SSH server port (default: 22)
                ssh_username: SSH username for authentication
                ssh_private_key_password: Passphrase for SSH private key
                ssh_private_key_path: Path to SSH private key file
                allow_agent: Allow SSH agent forwarding (default: True)
                print_info: Enable info logging (default: True)

        Raises:
            sshtunnel.BaseSSHTunnelForwarderError: If SSH tunnel creation fails
        """
        ssh_port: int = kwargs.get("ssh_port", 22)
        ssh_username: str | None = kwargs.get("ssh_username")
        ssh_private_key_password: str | None = kwargs.get("ssh_private_key_password")
        ssh_private_key_file: str | None = kwargs.get("ssh_private_key_path")
        allow_agent: bool = kwargs.get("allow_agent", True)
        print_info: bool = kwargs.get("print_info", True)

        try:
            self.ssh_tunnel_forward = sshtunnel.open_tunnel(
                (host, ssh_port),
                ssh_username=ssh_username,
                ssh_pkey=ssh_private_key_file,
                ssh_private_key_password=ssh_private_key_password,
                allow_agent=allow_agent,
                remote_bind_address=("localhost", port),
            )
            self.ssh_tunnel_forward.start()
            if print_info:
                logger.info("SSH tunnel established to %s:%d -> localhost:%d", host, ssh_port, port)
        except sshtunnel.BaseSSHTunnelForwarderError:
            logger.exception("SSH tunnel failed to %s:%d", host, ssh_port)
            raise

    def get_local_bind_port(self) -> int:
        """Get the local port number bound to the SSH tunnel.

        Returns:
            int: The local port number bound to the SSH tunnel
        """
        return int(self.ssh_tunnel_forward.local_bind_port)

    def close_ssh_tunnel(self) -> None:
        """Close the SSH tunnel.

        Raises:
            sshtunnel.BaseSSHTunnelForwarderError: If tunnel closure fails
        """
        try:
            self.ssh_tunnel_forward.close()
            logger.info("SSH tunnel closed")
        except sshtunnel.BaseSSHTunnelForwarderError:
            logger.exception("Failed to close SSH tunnel")
            raise
