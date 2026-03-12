"""Documents attachments operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class DocumentsAttachmentsMixin(BaseMixin):
    """Documents attachments operations.

    Provides methods for managing document attachments.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/attachments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def get_document_attachments(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of document attachments.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of attachments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "attachmentId": "attachment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName", "attachmentId"],
        response_type="json",
    )
    def get_document_attachment(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        attachment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific document attachment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            attachment_id: Attachment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Attachment metadata from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments/{attachment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName", "attachmentId"],
        response_type="binary",
    )
    def get_document_attachment_content(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        attachment_id: str,
        revision: str | None = None,
    ) -> Response:
        """Download document attachment content.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            attachment_id: Attachment identifier
            revision: Specific revision

        Returns:
            Response: Binary attachment content
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments/{attachment_id}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/attachments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        multipart_fields={
            "resource": "files",
            "files": "files",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def create_document_attachments(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        files: FilesDict,
    ) -> Response:
        """Create document attachments.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            files: Files dict with 'resource' (JSON metadata) and 'files' (file content)

        Returns:
            Response: Created attachments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments"
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "attachmentId": "attachment_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName", "attachmentId"],
        response_type="json",
    )
    def update_document_attachment(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        attachment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update document attachment metadata.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            attachment_id: Attachment identifier
            data: Attachment metadata in JSON:API format

        Returns:
            Response: Updated attachment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)
