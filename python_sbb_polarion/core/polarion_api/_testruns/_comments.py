"""Testruns comments operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class TestrunsCommentsMixin(BaseMixin):
    """Testruns comments operations.

    Provides methods for managing test run comments.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/comments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def get_testrun_comments(
        self,
        project_id: str,
        testrun_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of test run comments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of comments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/comments"
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
        path="/projects/{projectId}/testruns/{testRunId}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "commentId": "comment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "commentId"],
        response_type="json",
    )
    def get_testrun_comment(
        self,
        project_id: str,
        testrun_id: str,
        comment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test run comment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            comment_id: Comment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/comments/{comment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/comments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def create_testrun_comments(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Create test run comments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Comments data in JSON:API format

        Returns:
            Response: Created comments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/comments"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "commentId": "comment_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "commentId"],
        response_type="json",
    )
    def update_testrun_comment(
        self,
        project_id: str,
        testrun_id: str,
        comment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update test run comment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            comment_id: Comment identifier
            data: Comment data in JSON:API format

        Returns:
            Response: Updated comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/comments/{comment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/comments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def update_testrun_comments(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Update test run comments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Comments data in JSON:API format

        Returns:
            Response: Updated comments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/comments"
        return self.polarion_connection.api_request_patch(url, data=data)
