"""Test Data templates mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from pathlib import Path

    from requests import Response

    from python_sbb_polarion.types import FilesDict


class TemplatesMixin(BaseMixin):
    """Template operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/templates/{templateId}/hash",
        path_params={
            "templateId": "template_id",
        },
        required_params=["templateId"],
        response_type="text",
    )
    def get_template_hash(self, template_id: str) -> Response:
        """Get the hash of a project template

        Returns:
            Response: Response object from the API call

        Raises:
            ValueError: If template_id is null or empty.
        """
        if not template_id or not template_id.strip():
            raise ValueError("Template ID cannot be null or empty")

        url: str = f"{self.rest_api_url}/templates/{template_id}/hash"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)

    @restapi_endpoint(
        method="POST",
        path="/api/templates/{templateId}/{templateHash}",
        path_params={
            "templateId": "template_id",
            "templateHash": "template_hash",
        },
        multipart_fields={
            "file": "file_content",
        },
        helper_params=["file_path"],
        required_params=["templateId", "templateHash"],
        response_type="json",
    )
    def save_project_template(self, template_id: str, file_path: Path, template_hash: str) -> Response:
        """Upload template with hash

        Returns:
            Response: Response object from the API call

        Raises:
            FileNotFoundError: If temp_project_template_location file cannot be opened or read.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with file_path.open("rb") as f:
            files: FilesDict = {
                "file": (file_path.name, f.read(), MediaType.ZIP),
            }
            url: str = f"{self.rest_api_url}/templates/{template_id}/{template_hash}"
            headers: dict[str, str] = {
                Header.ACCEPT: MediaType.JSON,
            }
            return self.polarion_connection.api_request_post(url, files=files, headers=headers)

    @restapi_endpoint(
        method="GET",
        path="/api/templates/{projectId}/download",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            "projectGroup": "project_group",
        },
        required_params=["projectId"],
        response_type="binary",
    )
    def download_project_template(self, project_id: str, project_group: str | None = None) -> Response:
        """Download a zipped project template

        Args:
            project_id: The unique identifier of the template to download
            project_group: The group to which the project belongs

        Returns:
            Response: Response object containing the ZIP file bytes

        Raises:
            ValueError: If project_id is null or empty
        """
        if not project_id or not project_id.strip():
            raise ValueError("Project ID cannot be null or empty")

        url: str = f"/{self.rest_api_url}/templates/{project_id}/download"

        params: dict[str, str] = {}
        if project_group:
            params["projectGroup"] = str(project_group)

        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.OCTET_STREAM,
        }
        return self.polarion_connection.api_request_get(url, headers=headers, params=params or None)
