"""JSON Editor attachments mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict


class WorkItemAttachmentsMixin(BaseMixin):
    """Work item attachments operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/workitems/{workItemId}/attachments",
        path_params={
            "projectId": "project_id",
            "workItemId": "work_item_id",
        },
        multipart_fields={
            "fileName": "file_name",
        },
        required_params=["projectId", "workItemId"],
        response_type="text",
    )
    def create_workitem_attachment(self, project_id: str, work_item_id: str, file_name: str) -> Response:
        """Create an attachment

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/workitems/{work_item_id}/attachments"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        files: FilesDict = {
            "fileName": file_name,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    @restapi_endpoint(
        method="PATCH",
        path="/api/projects/{projectId}/workitems/{workItemId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "work_item_id",
            "attachmentId": "attachment_id",
        },
        multipart_fields={
            "content": "content",
        },
        required_params=["projectId", "workItemId", "attachmentId"],
        response_type="text",
    )
    def update_workitem_attachment(self, project_id: str, work_item_id: str, attachment_id: str, content: str) -> Response:
        """Update attachment content

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/workitems/{work_item_id}/attachments/{attachment_id}"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        files: FilesDict = {
            "content": content,
        }
        return self.polarion_connection.api_request_patch(url, headers=headers, files=files)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/workitems/{workItemId}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "workItemId": "work_item_id",
            "attachmentId": "attachment_id",
        },
        required_params=["projectId", "workItemId", "attachmentId"],
        response_type="text",
    )
    def get_workitem_attachment(self, project_id: str, work_item_id: str, attachment_id: str) -> Response:
        """Get attachment content

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/workitems/{work_item_id}/attachments/{attachment_id}/content"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)
