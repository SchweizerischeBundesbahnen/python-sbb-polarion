"""Documents comments operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class DocumentsCommentsMixin(BaseMixin):
    """Documents comments operations.

    Provides methods for managing document comments.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/comments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def get_document_comments(
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
        """Get list of document comments.

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
            Response: List of comments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments"
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
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "commentId": "comment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName", "commentId"],
        response_type="json",
    )
    def get_document_comment(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        comment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific document comment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            comment_id: Comment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments/{comment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/comments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def create_document_comments(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        data: JsonDict,
    ) -> Response:
        """Create document comments.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            data: Comments data in JSON:API format

        Returns:
            Response: Created comments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "commentId": "comment_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName", "commentId"],
        response_type="json",
    )
    def update_document_comment(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        comment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update document comment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            comment_id: Comment identifier
            data: Comment data in JSON:API format

        Returns:
            Response: Updated comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/comments/{comment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)
