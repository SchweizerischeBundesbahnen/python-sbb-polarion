"""Admin Utility wiki page management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class WikiMixin(BaseMixin):
    """Wiki page management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/spaces/{spaceId}/wiki/{name}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "name": "name",
        },
        required_params=["projectId", "spaceId", "name"],
    )
    def create_wiki_page(self, project_id: str, space_id: str, name: str) -> Response:
        """Create new wiki page in project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/wiki/{name}"
        return self.polarion_connection.api_request_post(url)

    @restapi_endpoint(
        method="DELETE",
        path="/api/projects/{projectId}/spaces/{spaceId}/wiki/{name}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "name": "name",
        },
        required_params=["projectId", "spaceId", "name"],
    )
    def delete_wiki_page(self, project_id: str, space_id: str, name: str) -> Response:
        """Delete wiki page in project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/wiki/{name}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="POST",
        path="/api/spaces/{spaceId}/wiki/{name}",
        path_params={
            "spaceId": "space_id",
            "name": "name",
        },
        required_params=["spaceId", "name"],
    )
    def create_wiki_page_in_global_repo(self, space_id: str, name: str) -> Response:
        """Create new wiki page in global repo (no project)

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/spaces/{space_id}/wiki/{name}"
        return self.polarion_connection.api_request_post(url)

    @restapi_endpoint(
        method="DELETE",
        path="/api/spaces/{spaceId}/wiki/{name}",
        path_params={
            "spaceId": "space_id",
            "name": "name",
        },
        required_params=["spaceId", "name"],
    )
    def delete_wiki_page_in_global_repo(self, space_id: str, name: str) -> Response:
        """Delete wiki page in global repo (no project)

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/spaces/{space_id}/wiki/{name}"
        return self.polarion_connection.api_request_delete(url)
