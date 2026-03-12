"""Testruns test step results operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class TestrunsStepResultsMixin(BaseMixin):
    """Testruns test step results operations.

    Provides methods for managing test step results and their attachments.
    """

    # Test Step Results

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def get_test_step_results(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of test step results.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of test step results from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults"
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
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex"],
        response_type="json",
    )
    def get_test_step_result(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test step result.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test step result data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def create_test_step_results(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        data: JsonDict,
    ) -> Response:
        """Create test step results.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            data: Test step results data in JSON:API format

        Returns:
            Response: Created test step results data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def update_test_step_results(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        data: JsonDict,
    ) -> Response:
        """Update test step results.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            data: Test step results data in JSON:API format

        Returns:
            Response: Updated test step results data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex"],
        response_type="json",
    )
    def update_test_step_result(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        data: JsonDict,
    ) -> Response:
        """Update a specific test step result.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            data: Test step result data in JSON:API format

        Returns:
            Response: Updated test step result data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}"
        return self.polarion_connection.api_request_patch(url, data=data)

    # Test Step Result Attachments

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex"],
        response_type="json",
    )
    def get_test_step_result_attachments(  # noqa: PLR0917
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of test step result attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of attachments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments"
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
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
            "attachmentId": "attachment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex", "attachmentId"],
        response_type="json",
    )
    def get_test_step_result_attachment(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        attachment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test step result attachment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            attachment_id: Attachment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Attachment metadata from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex", "attachmentId"],
        response_type="binary",
    )
    def get_test_step_result_attachment_content(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        attachment_id: str,
        revision: str | None = None,
    ) -> Response:
        """Download test step result attachment content.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            attachment_id: Attachment identifier
            revision: Specific revision

        Returns:
            Response: Binary attachment content
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
        },
        multipart_fields={
            "resource": "files",
            "files": "files",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex"],
        response_type="json",
    )
    def create_test_step_result_attachments(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        files: FilesDict,
    ) -> Response:
        """Create test step result attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            files: Files dict with 'resource' (JSON metadata) and 'files' (file content)

        Returns:
            Response: Created attachments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments"
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
            "attachmentId": "attachment_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex", "attachmentId"],
        response_type="json",
    )
    def update_test_step_result_attachment(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        attachment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update test step result attachment metadata.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            attachment_id: Attachment identifier
            data: Attachment metadata in JSON:API format

        Returns:
            Response: Updated attachment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
            "attachmentId": "attachment_id",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex", "attachmentId"],
        response_type="json",
    )
    def delete_test_step_result_attachment(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        attachment_id: str,
    ) -> Response:
        """Delete test step result attachment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            attachment_id: Attachment identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/teststepresults/{testStepIndex}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testStepIndex": "test_step_index",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testStepIndex"],
        response_type="json",
    )
    def delete_test_step_result_attachments(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_step_index: int,
        data: JsonDict,
    ) -> Response:
        """Delete test step result attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_step_index: Test step index (0-based)
            data: Attachments to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/teststepresults/{test_step_index}/attachments"
        return self.polarion_connection.api_request_delete(url, data=data)
