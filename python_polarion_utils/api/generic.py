"""Generic Polarion Extension API"""

from typing import Any, Literal, TypeAlias

from requests import Response  # type: ignore

from python_polarion_utils.common.util_http import HttpConnection

PolarionApiExtensionName: TypeAlias = Literal[
    "aad-synchronizer",
    "admin-utility",
    "api-extender",
    "collection-checker",
    "cucumber",
    "diff-tool",
    "dms-doc-connector",
    "dms-wi-connector",
    "excel-importer",
    "hooks",
    "jobs",
    "json-editor",
    "mailworkflow",
    "pdf-exporter",
    "requirements-inspector",
    "sbbtool",
    "test-data",
    "generic",
]


class PolarionRestApiConnection(HttpConnection):
    """Generic Polarion Extension REST API Connection"""


class PolarionGenericExtensionApi:
    """Generic Polarion Extension REST API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection, extension_name: PolarionApiExtensionName = "generic"):
        self.polarion_connection = polarion_connection
        self.extension_name = extension_name
        self.rest_api_url = f"/polarion/{self.extension_name}/rest/api"

    def get_context(self) -> Response | None:
        """GET context"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/context")

    def get_version(self) -> Response | None:
        """GET version"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/version")

    def _get_settings(self, feature: str, name: str = "Default", scope: str | None = None) -> Response | None:
        """GET settings for the specified :feature and specified :name (or Default)"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}/content"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_get(url)

    def _save_settings(self, feature: str, data: dict[str, Any], name: str = "Default", scope: str | None = None) -> Response | None:
        """PUT settings for specified :feature and specified :name (or Default)"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}/content"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_put(url, data=data)

    def _delete_settings(self, feature: str, name: str, scope: str | None = None) -> Response | None:
        """DELETE settings by specified :feature and specified :name"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_delete(url)

    def _get_settings_defaults(self, feature: str) -> Response | None:
        """GET settings defaults for specified :feature"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/settings/{feature}/default-content")

    def _get_settings_revisions(self, feature: str, name: str = "Default", scope: str | None = None) -> Response | None:
        """GET settings revisions for specified :feature and specified :name (or Default)"""
        url = f"/{self.rest_api_url}/settings/{feature}/names/{name}/revisions"
        if scope is not None:
            url += f"?scope={scope}"
        return self.polarion_connection.api_request_get(url)

    def get_swagger(self) -> Response | None:
        """GET swagger page"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/swagger")
