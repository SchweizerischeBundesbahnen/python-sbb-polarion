"""Workitems attachments operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class WorkitemsAttachmentsMixin(BaseMixin):
    """Workitems attachments operations.

    Provides methods for managing work item attachments.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/attachments",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_workitem_attachments(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of work item attachments.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of attachments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "attachmentId": "attachment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "attachmentId"],
        response_type="json",
    )
    def get_workitem_attachment(
        self,
        project_id: str,
        workitem_id: str,
        attachment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific work item attachment.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            attachment_id: Attachment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Attachment metadata from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "attachmentId"],
        response_type="binary",
    )
    def get_workitem_attachment_content(
        self,
        project_id: str,
        workitem_id: str,
        attachment_id: str,
        revision: str | None = None,
    ) -> Response:
        """Download work item attachment content.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            attachment_id: Attachment identifier
            revision: Specific revision

        Returns:
            Response: Binary attachment content
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/attachments",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        multipart_fields={
            "resource": "files",
            "files": "files",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_workitem_attachments(
        self,
        project_id: str,
        workitem_id: str,
        files: FilesDict,
    ) -> Response:
        """Create work item attachments.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            files: Files dict with 'resource' (JSON metadata) and 'files' (file content)

        Returns:
            Response: Created attachments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments"
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "attachmentId": "attachment_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "attachmentId"],
        response_type="json",
    )
    def update_workitem_attachment(
        self,
        project_id: str,
        workitem_id: str,
        attachment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update work item attachment metadata.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            attachment_id: Attachment identifier
            data: Attachment metadata in JSON:API format

        Returns:
            Response: Updated attachment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "attachmentId": "attachment_id",
        },
        required_params=["projectId", "workItemId", "attachmentId"],
        response_type="json",
    )
    def delete_workitem_attachment(
        self,
        project_id: str,
        workitem_id: str,
        attachment_id: str,
    ) -> Response:
        """Delete work item attachment.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            attachment_id: Attachment identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_delete(url)
