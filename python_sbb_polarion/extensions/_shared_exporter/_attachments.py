"""Shared test run attachments mixin for PDF and DOCX exporters.

This module provides common attachment methods shared between exporters.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response


class SharedExporterAttachmentsMixin(BaseMixin):
    """Shared test run attachment operations.

    This mixin provides common methods for:
    - Getting test run attachment by ID
    - Getting test run attachment content
    """

    # =========================================================================
    # Test Run Attachments (Shared)
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/testruns/{testRunId}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "test_run_id",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "attachmentId"],
        response_type="json",
    )
    def get_test_run_attachment(self, project_id: str, test_run_id: str, attachment_id: str, revision: str | None = None) -> Response:
        """Get test run attachment by ID.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/testruns/{test_run_id}/attachments/{attachment_id}"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/testruns/{testRunId}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "testRunId": "test_run_id",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "attachmentId"],
        response_type="binary",
    )
    def get_test_run_attachment_content(self, project_id: str, test_run_id: str, attachment_id: str, revision: str | None = None) -> Response:
        """Get test run attachment content.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/testruns/{test_run_id}/attachments/{attachment_id}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.OCTET_STREAM,
        }
        return self.polarion_connection.api_request_get(url, headers=headers, params=params or None)
