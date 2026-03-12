"""Workitems comments operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class WorkitemsCommentsMixin(BaseMixin):
    """Workitems comments operations.

    Provides methods for managing work item comments.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/comments",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_workitem_comments(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of work item comments.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of comments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/comments"
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
        path="/projects/{projectId}/workitems/{workItemId}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "commentId": "comment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "commentId"],
        response_type="json",
    )
    def get_workitem_comment(
        self,
        project_id: str,
        workitem_id: str,
        comment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific work item comment.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            comment_id: Comment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/comments/{comment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/comments",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_workitem_comments(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create work item comments.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Comments data in JSON:API format

        Returns:
            Response: Created comments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/comments"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "commentId": "comment_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "commentId"],
        response_type="json",
    )
    def update_workitem_comment(
        self,
        project_id: str,
        workitem_id: str,
        comment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update work item comment.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            comment_id: Comment identifier
            data: Comment data in JSON:API format

        Returns:
            Response: Updated comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/comments/{comment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)
