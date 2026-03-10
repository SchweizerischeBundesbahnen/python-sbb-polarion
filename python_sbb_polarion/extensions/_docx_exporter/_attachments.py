"""DOCX Exporter test run attachments mixin.

This module provides DOCX-specific attachment methods.
Common methods are inherited from SharedExporterAttachmentsMixin.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._shared_exporter import SharedExporterAttachmentsMixin


if TYPE_CHECKING:
    from requests import Response


class TestRunAttachmentsMixin(SharedExporterAttachmentsMixin):
    """DOCX Exporter test run attachment operations.

    Common methods inherited from SharedExporterAttachmentsMixin:
    - get_test_run_attachment() - Get attachment by ID
    - get_test_run_attachment_content() - Get attachment content

    DOCX-specific methods:
    - get_test_run_attachments() - List attachments
    """

    # =========================================================================
    # Test Run Attachments (DOCX-specific)
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/testruns/{testRunId}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "test_run_id",
        },
        query_params={
            "revision": "revision",
            "filter": "filter_query",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def get_test_run_attachments(self, project_id: str, test_run_id: str, revision: str | None = None, filter_query: str | None = None) -> Response:
        """Get list of test run attachments.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/testruns/{test_run_id}/attachments"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        if filter_query:
            params["filter"] = filter_query
        return self.polarion_connection.api_request_get(url, params=params or None)
