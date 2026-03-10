"""Jobs operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import SparseFields


class JobsMixin(BaseMixin):
    """Jobs operations.

    Provides methods for managing async jobs.
    """

    @restapi_endpoint(
        method="GET",
        path="/jobs/{jobId}",
        path_params={
            "jobId": "job_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["jobId"],
        response_type="json",
    )
    def get_job(
        self,
        job_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get job status.

        Args:
            job_id: Job identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: Job status data from API
        """
        url: str = f"{self.base_url}/jobs/{job_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/jobs/{jobId}/actions/download/{filename}",
        path_params={
            "jobId": "job_id",
            "filename": "filename",
        },
        required_params=["jobId", "filename"],
        response_type="binary",
    )
    def get_job_result_file(
        self,
        job_id: str,
        filename: str,
    ) -> Response:
        """Download job result file.

        Args:
            job_id: Job identifier
            filename: Result file name

        Returns:
            Response: Binary file content
        """
        url: str = f"{self.base_url}/jobs/{job_id}/actions/download/{filename}"
        return self.polarion_connection.api_request_get(url)
