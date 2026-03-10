"""Interceptor Manager hook settings mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class HookSettingsMixin(BaseMixin):
    """Hook settings operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/hook-settings/{hook}/content",
        path_params={
            "hook": "hook",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["hook"],
        response_type="json",
    )
    def get_hook_settings(self, hook: str, revision: str = "") -> Response:
        """GET settings for the specified hook and revision

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/hook-settings/{hook}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="PUT",
        path="/api/hook-settings/{hook}/content",
        path_params={
            "hook": "hook",
        },
        body_param="data",
        required_params=["hook"],
        response_type="json",
    )
    def save_hook_settings(self, hook: str, data: JsonDict) -> Response:
        """PUT settings for specified hook

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/hook-settings/{hook}/content"
        return self.polarion_connection.api_request_put(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/hook-settings/{hook}/default-content",
        path_params={
            "hook": "hook",
        },
        required_params=["hook"],
        response_type="json",
    )
    def get_hook_settings_defaults(self, hook: str) -> Response:
        """GET settings defaults for specified hook

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/hook-settings/{hook}/default-content"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/hook-settings/{hook}/revisions",
        path_params={
            "hook": "hook",
        },
        required_params=["hook"],
        response_type="json",
    )
    def get_hook_settings_revisions(self, hook: str) -> Response:
        """GET hook settings revisions for specified hook

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/hook-settings/{hook}/revisions"
        return self.polarion_connection.api_request_get(url)
