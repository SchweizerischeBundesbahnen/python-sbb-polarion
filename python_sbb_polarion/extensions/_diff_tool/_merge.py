"""Diff Tool merge operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class MergeMixin(BaseMixin):
    """Merge operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/merge/documents",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_document_workitems(self, data: JsonDict) -> Response:
        """Merge workItems from different documents

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/documents"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/merge/documents-fields",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_documents_fields(self, data: JsonDict) -> Response:
        """Merge fields values from one live document into another

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/documents-fields"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/merge/documents-content",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_documents_content(self, data: JsonDict) -> Response:
        """Merge content from one live document into another

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/documents-content"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/merge/workitems",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_detached_workitems(self, data: JsonDict) -> Response:
        """Merge workItems out of documents scope

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/workitems"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/merge/chapter",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_chapter(self, data: JsonDict) -> Response:
        """Copies or moves a chapter of one live document into another one

        The merge runs in the background. This method answers 202 as soon as the merge
        is started, and the job which delivers its result is named in the Location header.
        Poll get_chapter_merge_job() and read get_chapter_merge_job_result().

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/chapter"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/merge/chapter/jobs",
    )
    def get_chapter_merge_jobs(self) -> Response:
        """Gets the chapter merge jobs of the current user, keyed by job id

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/chapter/jobs"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/merge/chapter/jobs/{jobId}",
        path_params={
            "jobId": "job_id",
        },
        required_params=["jobId"],
    )
    def get_chapter_merge_job(self, job_id: str) -> Response:
        """Gets the state of a certain chapter merge job

        Answers 202 while the merge runs, 303 to its result once it is over, and 409 if
        it failed. The redirect is not followed here, so the caller sees which of the
        three it is; get_chapter_merge_job_result() reads the result itself.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/chapter/jobs/{job_id}"
        return self.polarion_connection.api_request_get(url, allow_redirects=False)

    @restapi_endpoint(
        method="GET",
        path="/api/merge/chapter/jobs/{jobId}/result",
        path_params={
            "jobId": "job_id",
        },
        required_params=["jobId"],
        response_type="json",
    )
    def get_chapter_merge_job_result(self, job_id: str) -> Response:
        """Gets the merge result of a chapter merge job which is over

        A merge which did not do what was asked of it reports that in its result too, so
        an unsuccessful merge result is answered with 200 like any other.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/chapter/jobs/{job_id}/result"
        return self.polarion_connection.api_request_get(url)
