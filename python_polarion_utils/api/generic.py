"""Generic Polarion Extension API"""

import string

from ...common.util_http import HttpConnection


class PolarionRestApiConnection(HttpConnection):
    """Generic Polarion Extension REST API Connection"""


class PolarionGenericExtensionApi:
    """Generic Polarion Extension REST API"""

    def __init__(self, extension_name: string, polarion_connection: PolarionRestApiConnection):
        self.polarion_connection = polarion_connection
        self.extension_name = extension_name
        self.rest_api_url = f"/polarion/{extension_name}/rest/api"

    def get_context(self):
        """GET context"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/context")

    def get_version(self):
        """GET version"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/version")

    def _get_settings(self, feature, name="Default", scope=None):
        """GET settings for the specified :feature and specified :name (or Default)"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}/content"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_get(url)

    def _save_settings(self, feature, data, name="Default", scope=None):
        """PUT settings for specified :feature and specified :name (or Default)"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}/content"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_put(url, data=data)

    def _delete_settings(self, feature, name, scope=None):
        """DELETE settings by specified :feature and specified :name"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_delete(url)

    def _get_settings_defaults(self, feature):
        """GET settings defaults for specified :feature"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/settings/{feature}/default-content")

    def _get_settings_revisions(self, feature, name="Default", scope=None):
        """GET settings revisions for specified :feature and specified :name (or Default)"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}/revisions"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_get(url)

    def get_swagger(self):
        """GET swagger page"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/swagger")
