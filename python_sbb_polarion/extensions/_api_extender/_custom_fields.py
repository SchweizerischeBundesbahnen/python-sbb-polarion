"""API Extender custom fields mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class CustomFieldsMixin(BaseMixin):
    """Project custom fields operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/keys/{key}",
        path_params={
            "projectId": "project_id",
            "key": "key",
        },
        required_params=["projectId", "key"],
        response_type="json",
    )
    def get_custom_field(self, project_id: str, key: str) -> Response:
        """Get project custom field

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/keys/{key}"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/keys/{key}",
        path_params={
            "projectId": "project_id",
            "key": "key",
        },
        body_param="field_data",
        required_params=["projectId", "key"],
        response_type="json",
    )
    def save_custom_field(self, project_id: str, key: str, value: str) -> Response:
        """Save project custom field

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/keys/{key}"
        data: JsonDict = {
            "value": value,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/api/projects/{projectId}/keys/{key}",
        path_params={
            "projectId": "project_id",
            "key": "key",
        },
        required_params=["projectId", "key"],
        response_type="json",
    )
    def delete_custom_field(self, project_id: str, key: str) -> Response:
        """Delete project custom field

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/keys/{key}"
        return self.polarion_connection.api_request_delete(url)
