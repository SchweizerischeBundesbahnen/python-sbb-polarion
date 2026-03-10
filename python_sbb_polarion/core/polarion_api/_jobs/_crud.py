"""Jobs management operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class JobsManagementMixin(BaseMixin):
    """Jobs management operations.

    Provides methods for managing and executing Polarion jobs.
    New in Polarion 2512.
    """

    @restapi_endpoint(
        method="GET",
        path="/jobs",
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "projectId": "project_id",
        },
        response_type="json",
    )
    def get_jobs(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        project_id: str | None = None,
    ) -> Response:
        """Get list of jobs.

        Args:
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            project_id: Filter by project ID

        Returns:
            Response: List of jobs from API
        """
        url: str = f"{self.base_url}/jobs"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if project_id:
            params["projectId"] = project_id
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/jobs/actions/execute",
        body_param="data",
        response_type="json",
    )
    def execute_job(
        self,
        data: JsonDict,
    ) -> Response:
        """Execute a job.

        Args:
            data: Job execution data in JSON:API format

        Returns:
            Response: Job execution result from API
        """
        url: str = f"{self.base_url}/jobs/actions/execute"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/jobs/{jobId}/log/content",
        path_params={"jobId": "job_id"},
        required_params=["jobId"],
        response_type="text",
    )
    def get_job_log_content(
        self,
        job_id: str,
    ) -> Response:
        """Get job log content.

        Args:
            job_id: Job identifier

        Returns:
            Response: Job log content from API
        """
        url: str = f"{self.base_url}/jobs/{job_id}/log/content"
        return self.polarion_connection.api_request_get(url)
