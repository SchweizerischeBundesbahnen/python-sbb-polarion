"""Testruns attachments operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class TestrunsAttachmentsMixin(BaseMixin):
    """Testruns attachments operations.

    Provides methods for managing test run attachments.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/attachments",
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
    def get_testrun_attachments(
        self,
        project_id: str,
        testrun_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of test run attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of attachments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/attachments"
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
        path="/projects/{projectId}/testruns/{testRunId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "attachmentId": "attachment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "attachmentId"],
        response_type="json",
    )
    def get_testrun_attachment(
        self,
        project_id: str,
        testrun_id: str,
        attachment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test run attachment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            attachment_id: Attachment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Attachment metadata from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/attachments/{attachment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "attachmentId"],
        response_type="binary",
    )
    def get_testrun_attachment_content(
        self,
        project_id: str,
        testrun_id: str,
        attachment_id: str,
        revision: str | None = None,
    ) -> Response:
        """Download test run attachment content.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            attachment_id: Attachment identifier
            revision: Specific revision

        Returns:
            Response: Binary attachment content
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/attachments/{attachment_id}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        multipart_fields={
            "resource": "files",
            "files": "files",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def create_testrun_attachments(
        self,
        project_id: str,
        testrun_id: str,
        files: FilesDict,
    ) -> Response:
        """Create test run attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            files: Files dict with 'resource' (JSON metadata) and 'files' (file content)

        Returns:
            Response: Created attachments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/attachments"
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "attachmentId": "attachment_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "attachmentId"],
        response_type="json",
    )
    def update_testrun_attachment(
        self,
        project_id: str,
        testrun_id: str,
        attachment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update test run attachment metadata.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            attachment_id: Attachment identifier
            data: Attachment metadata in JSON:API format

        Returns:
            Response: Updated attachment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "attachmentId": "attachment_id",
        },
        required_params=["projectId", "testRunId", "attachmentId"],
        response_type="json",
    )
    def delete_testrun_attachment(
        self,
        project_id: str,
        testrun_id: str,
        attachment_id: str,
    ) -> Response:
        """Delete test run attachment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            attachment_id: Attachment identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def delete_testrun_attachments(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete test run attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Attachments to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/attachments"
        return self.polarion_connection.api_request_delete(url, data=data)
