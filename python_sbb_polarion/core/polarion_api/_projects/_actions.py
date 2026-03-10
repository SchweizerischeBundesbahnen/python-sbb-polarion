"""Projects actions operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class ProjectsActionsMixin(BaseMixin):
    """Projects actions operations.

    Provides methods for project actions like move, mark, and unmark.
    """

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/actions/moveProject",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def move_project(self, project_id: str, data: JsonDict) -> Response:
        """Move a project to a different location.

        Args:
            project_id: Project identifier
            data: Move configuration data

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/actions/moveProject"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/projects/actions/markProject",
        body_param="data",
        response_type="json",
    )
    def mark_project(self, data: JsonDict) -> Response:
        """Mark a project.

        Args:
            data: Mark configuration data

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/actions/markProject"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/actions/unmarkProject",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def unmark_project(self, project_id: str) -> Response:
        """Unmark a project.

        Args:
            project_id: Project identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/actions/unmarkProject"
        return self.polarion_connection.api_request_post(url)
