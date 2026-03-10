"""Common implementation for LDAP connections."""

import json
import logging
import pathlib

import ldap3
import ldap3.core.exceptions

from python_sbb_polarion.types import JsonDict


logger = logging.getLogger(__name__)


LDAP_SERVER_NAME = "ldap.example.com"
LDAP_BASE_DN = "OU=Users,DC=example,DC=com"

USER_NAME_FOR_LDAP_READ = "ldap-reader@example.com"  # INFO: must include domain suffix
USER_PASSWORD_FOR_LDAP_READ = ""  # WARNING: Do not hardcode passwords - use environment variables or config files

USER_CACHE_FILE = "./util_ldap_user.cache"
GROUP_CACHE_FILE = "./util_ldap_group.cache"


class LdapConnection:
    """LDAP connection manager with user and group caching.

    Provides methods to query LDAP for user information with automatic caching
    to local JSON files for improved performance.
    """

    def __init__(self, user_name: str, user_password: str, server_name: str = LDAP_SERVER_NAME) -> None:
        """Initialize LDAP connection.

        Args:
            user_name: LDAP username (must include domain suffix, e.g. @example.com)
            user_password: LDAP password
            server_name: LDAP server hostname (default: ldap.example.com)
        """
        self.server = ldap3.Server(server_name, use_ssl=True, get_info=ldap3.ALL)
        self.connection = ldap3.Connection(self.server, user_name, user_password, auto_bind=ldap3.AUTO_BIND_NO_TLS)
        self.ldap_users: dict[str, JsonDict] = {}
        self.ldap_groups: dict[str, JsonDict] = {}

        # load user cache from a file
        if pathlib.Path(USER_CACHE_FILE).exists():
            try:
                with pathlib.Path(USER_CACHE_FILE).open(encoding="utf-8") as f:
                    self.ldap_users = json.load(f)
                logger.debug("Loaded %d users from cache", len(self.ldap_users))
            except (OSError, json.JSONDecodeError):
                logger.exception("Failed to load user cache from %s", USER_CACHE_FILE)
                self.ldap_users = {}

    def get_info_about_user(self, user: str) -> JsonDict:
        """Get user information from LDAP or cache.

        Args:
            user: Username to query (sAMAccountName)

        Returns:
            JsonDict: User information as JSON dict, or empty dict if user not found
        """
        if user not in self.ldap_users:
            # store the user information to prevent from requesting users information from LDAP again
            try:
                self.connection.search(
                    search_base=LDAP_BASE_DN,
                    search_filter=f"(sAMAccountName={user})",
                    attributes=ldap3.ALL_ATTRIBUTES,
                )
                if self.connection.entries:
                    # Convert ldap3.Entry to JSON-serializable dict
                    entry: ldap3.Entry = self.connection.entries[0]
                    self.ldap_users[user] = json.loads(entry.entry_to_json())
                    logger.debug("User %s found in LDAP", user)
                else:
                    self.ldap_users[user] = {}
                    logger.warning("User %s not found in LDAP", user)
            except ldap3.core.exceptions.LDAPException:
                logger.exception("LDAP search failed for user %s", user)
                self.ldap_users[user] = {}
        return self.ldap_users[user]

    def get_user_object_id(self, user: str) -> str:
        """Get Azure AD object ID for user.

        Args:
            user: Username to query

        Returns:
            str: Azure AD object ID (with 'User_' prefix removed), or empty string if not found
        """
        user_data: JsonDict = self.get_info_about_user(user)
        if user_data and "msDS-ExternalDirectoryObjectId" in user_data:
            return str(user_data["msDS-ExternalDirectoryObjectId"]).replace("User_", "")
        return ""

    def get_user_email_address(self, user: str) -> str:
        """Get email address for user.

        Args:
            user: Username to query

        Returns:
            str: User's email address (userPrincipalName), or empty string if not found
        """
        user_data: JsonDict = self.get_info_about_user(user)
        if user_data and "userPrincipalName" in user_data:
            return str(user_data["userPrincipalName"])
        return ""

    def __del__(self) -> None:
        """Save cached user data to file on object destruction."""
        try:
            with pathlib.Path(USER_CACHE_FILE).open("w", encoding="utf-8") as f:
                json.dump(self.ldap_users, f, indent=2)
            logger.debug("Saved %d users to cache", len(self.ldap_users))
        except OSError:
            logger.exception("Failed to save user cache to %s", USER_CACHE_FILE)
