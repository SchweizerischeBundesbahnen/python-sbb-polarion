"""Admin Utility project management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class ProjectMixin(BaseMixin):
    """Project management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/projects",
        body_param="data",
        helper_params=["project_id", "project_name", "template_id"],
        required_params=["__request_body__"],
    )
    def create_project(self, project_id: str, project_name: str, template_id: str) -> Response:
        """Create project from specified project template

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects"
        data: JsonDict = {
            "projectId": project_id,
            "projectName": project_name,
            "templateId": template_id,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/test-run-templates",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        helper_params=["template_id"],
        required_params=["projectId"],
    )
    def create_test_run_template(self, project_id: str, template_id: str) -> Response:
        """Create test run template

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/test-run-templates"
        data: JsonDict = {
            "templateId": template_id,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{id}",
        path_params={
            "id": "project_id",
        },
        required_params=["id"],
    )
    def get_project(self, project_id: str) -> Response:
        """Get project info

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="DELETE",
        path="/api/projects/{id}",
        path_params={
            "id": "project_id",
        },
        required_params=["id"],
    )
    def delete_project(self, project_id: str) -> Response:
        """Delete project info

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}"
        return self.polarion_connection.api_request_delete(url)
