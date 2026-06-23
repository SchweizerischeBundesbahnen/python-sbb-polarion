"""Generic Polarion Extension API"""

from requests import Response

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.types import JsonDict
from python_sbb_polarion.util.http import HttpConnection


class PolarionRestApiConnection(HttpConnection):
    """Generic Polarion Extension REST API Connection"""

    # Standard Polarion activation servlet (built into every Polarion installation,
    # no extension required -- so not annotated as a REST API v1 / OpenAPI endpoint).

    def activate_trial(self) -> Response:
        """Activate Polarion's built-in 30-day evaluation (trial) license.

        Calls Polarion's standard activation servlet (``POST /polarion/activate/entry``),
        which is available on any vanilla Polarion installation -- the admin-utility
        extension is *not* required. This is the programmatic equivalent of clicking
        "Start Trial" on the Polarion activation page.

        The servlet answers with a ``text/plain`` body ``{"activated": true}`` on success,
        or ``{"activated": false, "message": ...}`` when a trial cannot be (re)activated on
        this instance (e.g. a trial was already used or SALT licensing is enforced).

        Returns:
            Response: Response object from the activation servlet
        """
        url: str = "/polarion/activate/entry"
        return self.api_request_post(url)


class PolarionGenericExtensionApi:
    """Generic Polarion Extension REST API (Base class without settings)"""

    def __init__(self, extension_name: str, polarion_connection: PolarionRestApiConnection) -> None:
        self.polarion_connection = polarion_connection
        self.extension_name = extension_name
        self.rest_api_url = f"/polarion/{extension_name}/rest/api"

    # Info endpoints

    @restapi_endpoint(
        method="GET",
        path="/api/context",
        response_type="json",
    )
    def get_context(self) -> Response:
        """Get context.

        Returns:
            Response: Context information from API
        """
        url: str = f"{self.rest_api_url}/context"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/version",
        response_type="json",
    )
    def get_version(self) -> Response:
        """Get version.

        Returns:
            Response: Version information from API
        """
        url: str = f"{self.rest_api_url}/version"
        return self.polarion_connection.api_request_get(url)

    # Swagger endpoints (not included in OpenAPI spec -- so not annotated)

    def get_swagger(self) -> Response:
        """Get Swagger page.

        Returns:
            Response: Swagger UI from API
        """
        url: str = f"{self.rest_api_url}/swagger"
        return self.polarion_connection.api_request_get(url)

    def get_openapi(self) -> Response:
        """Get OpenAPI specification.

        Returns:
            Response: OpenAPI specification from API
        """
        url: str = f"{self.rest_api_url}/openapi.json"
        return self.polarion_connection.api_request_get(url)


class PolarionGenericExtensionSettingsApi:
    """Generic Polarion Extension REST API Settings Mixin

    Mixin class providing settings endpoints for Polarion extensions.
    Use with multiple inheritance: class MyApi(PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi)
    """

    # Type hints for attributes provided by PolarionGenericExtensionApi
    rest_api_url: str
    polarion_connection: PolarionRestApiConnection

    # Settings endpoints

    @restapi_endpoint(
        method="GET",
        path="/api/settings",
        required_params=[],
        response_type="json",
    )
    def get_features(self) -> Response:
        """Get list of available features.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/settings/{feature}/names",
        path_params={
            "feature": "feature",
        },
        query_params={
            "scope": "scope",
        },
        required_params=["feature"],
        response_type="json",
    )
    def get_setting_names(self, feature: str, scope: str | None = None) -> Response:
        """Get list of setting names for specified feature.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/{feature}/names"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/api/settings/{feature}/names/{name}",
        path_params={
            "feature": "feature",
            "name": "name",
        },
        query_params={
            "scope": "scope",
        },
        body_param="new_name",
        required_params=["feature", "name"],
        response_type="text",
    )
    def rename_setting(self, feature: str, name: str, new_name: str, scope: str | None = None) -> Response:
        """Rename specified setting.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/{feature}/names/{name}"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_post(url, payload=new_name, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/api/settings/{feature}/names/{name}/revisions",
        path_params={
            "feature": "feature",
            "name": "name",
        },
        query_params={
            "scope": "scope",
        },
        required_params=["feature", "name"],
        response_type="json",
    )
    def get_setting_revisions(self, feature: str, name: str = "Default", scope: str | None = None) -> Response:
        """Get setting revisions for specified feature and name.

        Returns:
            Response: Settings revisions from API
        """
        url: str = f"{self.rest_api_url}/settings/{feature}/names/{name}/revisions"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="DELETE",
        path="/api/settings/{feature}/names/{name}",
        path_params={
            "feature": "feature",
            "name": "name",
        },
        query_params={
            "scope": "scope",
        },
        required_params=["feature", "name"],
        response_type="json",
    )
    def delete_setting(self, feature: str, name: str, scope: str | None = None) -> Response:
        """Delete setting by specified feature and name.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/{feature}/names/{name}"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_delete(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/api/settings/{feature}/names/{name}/content",
        path_params={
            "feature": "feature",
            "name": "name",
        },
        query_params={
            "scope": "scope",
            "revision": "revision",
        },
        required_params=["feature", "name"],
        response_type="json",
    )
    def get_setting_content(self, feature: str, name: str = "Default", scope: str | None = None, revision: str | None = None) -> Response:
        """Get setting content for specified feature and name.

        Returns:
            Response: Settings data from API
        """
        url: str = f"{self.rest_api_url}/settings/{feature}/names/{name}/content"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="PUT",
        path="/api/settings/{feature}/names/{name}/content",
        path_params={
            "feature": "feature",
            "name": "name",
        },
        query_params={
            "scope": "scope",
        },
        body_param="data",
        required_params=["feature", "name"],
        response_type="json",
    )
    def save_setting(self, feature: str, data: JsonDict, name: str = "Default", scope: str | None = None) -> Response:
        """Save setting for specified feature and name.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/{feature}/names/{name}/content"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_put(url, data=data, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/api/settings/{feature}/default-content",
        path_params={
            "feature": "feature",
        },
        required_params=["feature"],
        response_type="json",
    )
    def get_setting_default_content(self, feature: str) -> Response:
        """Get default setting content for specified feature.

        Returns:
            Response: Default settings from API
        """
        url: str = f"{self.rest_api_url}/settings/{feature}/default-content"
        return self.polarion_connection.api_request_get(url)
