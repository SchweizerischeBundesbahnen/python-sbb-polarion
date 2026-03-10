"""Admin Utility live report management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header


if TYPE_CHECKING:
    from requests import Response


class LiveReportMixin(BaseMixin):
    """Live report management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/spaces/{spaceId}/report/{name}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "name": "name",
        },
        body_param="content",
        header_params={
            Header.CONTENT_TYPE: "content_type",
        },
        required_params=["projectId", "spaceId", "name"],
    )
    def create_live_report(self, project_id: str, space_id: str, name: str, content_type: str, content: str) -> Response:
        """Create new live report in project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/report/{name}"
        headers: dict[str, str] = {
            Header.CONTENT_TYPE: content_type,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, payload=content)

    @restapi_endpoint(
        method="DELETE",
        path="/api/projects/{projectId}/spaces/{spaceId}/report/{name}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "name": "name",
        },
        required_params=["projectId", "spaceId", "name"],
    )
    def delete_live_report(self, project_id: str, space_id: str, name: str) -> Response:
        """Delete live report in project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/report/{name}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="POST",
        path="/api/spaces/{spaceId}/report/{name}",
        path_params={
            "spaceId": "space_id",
            "name": "name",
        },
        body_param="content",
        header_params={
            Header.CONTENT_TYPE: "content_type",
        },
        required_params=["spaceId", "name"],
    )
    def create_live_report_in_default_space(self, space_id: str, name: str, content_type: str, content: str) -> Response:
        """Create new live report in default space (no project)

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/spaces/{space_id}/report/{name}"
        headers: dict[str, str] = {
            Header.CONTENT_TYPE: content_type,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, payload=content)

    @restapi_endpoint(
        method="DELETE",
        path="/api/spaces/{spaceId}/report/{name}",
        path_params={
            "spaceId": "space_id",
            "name": "name",
        },
        required_params=["spaceId", "name"],
    )
    def delete_live_report_in_default_space(self, space_id: str, name: str) -> Response:
        """Delete live report in default space (no project)

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/spaces/{space_id}/report/{name}"
        return self.polarion_connection.api_request_delete(url)
