"""Utility modules for Polarion integration.

Provides common utilities for HTTP connections, SSH tunneling, database access,
LDAP integration, OAuth authentication, email sending, and environment diagnostics.
"""

from python_sbb_polarion.util.argparse import get_script_arguments
from python_sbb_polarion.util.environment import (
    print_encoding,
    print_pip_information,
    print_python_information,
)
from python_sbb_polarion.util.http import HttpConnection
from python_sbb_polarion.util.ldap import LdapConnection
from python_sbb_polarion.util.mailer import Mailer, MailerError
from python_sbb_polarion.util.oauth import get_oauth2_client_credentials
from python_sbb_polarion.util.path import abs_path, abs_path_str
from python_sbb_polarion.util.sql import SqlDatabaseConnection
from python_sbb_polarion.util.ssh import SshConnection
from python_sbb_polarion.util.sshtunnel import SshTunnelConnection


__all__ = [
    "HttpConnection",
    "LdapConnection",
    "Mailer",
    "MailerError",
    "SqlDatabaseConnection",
    "SshConnection",
    "SshTunnelConnection",
    "abs_path",
    "abs_path_str",
    "get_oauth2_client_credentials",
    "get_script_arguments",
    "print_encoding",
    "print_pip_information",
    "print_python_information",
]
