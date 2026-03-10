"""Testruns test records operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class TestrunsRecordsMixin(BaseMixin):
    """Testruns test records operations.

    Provides methods for managing test records and their attachments/parameters.
    """

    # Test Records

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "testResultId": "test_result_id",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def get_test_records(
        self,
        project_id: str,
        testrun_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
        test_case_project_id: str | None = None,
        test_case_id: str | None = None,
        test_result_id: str | None = None,
    ) -> Response:
        """Get list of test records.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision
            test_case_project_id: Filter by test case project ID
            test_case_id: Filter by test case ID
            test_result_id: Filter by test result ID

        Returns:
            Response: List of test records from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords"
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
        if test_case_project_id:
            params["testCaseProjectId"] = test_case_project_id
        if test_case_id:
            params["testCaseId"] = test_case_id
        if test_result_id:
            params["testResultId"] = test_result_id
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def get_test_record(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test record.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test record data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def create_test_records(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Create test records.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Test records data in JSON:API format

        Returns:
            Response: Created test records data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def update_test_records(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Update test records.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Test records data in JSON:API format

        Returns:
            Response: Updated test records data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}",
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
    def update_test_record(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        data: JsonDict,
    ) -> Response:
        """Update a specific test record.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            data: Test record data in JSON:API format

        Returns:
            Response: Updated test record data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def delete_test_record(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
    ) -> Response:
        """Delete a specific test record.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}"
        return self.polarion_connection.api_request_delete(url)

    # Test Record Attachments

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def get_test_record_attachments(
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
        """Get list of test record attachments.

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
            Response: List of attachments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/attachments"
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
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "attachmentId": "attachment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "attachmentId"],
        response_type="json",
    )
    def get_test_record_attachment(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        attachment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test record attachment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            attachment_id: Attachment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Attachment metadata from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/attachments/{attachment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "attachmentId"],
        response_type="binary",
    )
    def get_test_record_attachment_content(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        attachment_id: str,
        revision: str | None = None,
    ) -> Response:
        """Download test record attachment content.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            attachment_id: Attachment identifier
            revision: Specific revision

        Returns:
            Response: Binary attachment content
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/attachments/{attachment_id}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/attachments",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        multipart_fields={
            "resource": "files",
            "files": "files",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def create_test_record_attachments(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        files: FilesDict,
    ) -> Response:
        """Create test record attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            files: Files dict with 'resource' (JSON metadata) and 'files' (file content)

        Returns:
            Response: Created attachments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/attachments"
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "attachmentId": "attachment_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "attachmentId"],
        response_type="json",
    )
    def update_test_record_attachment(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        attachment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update test record attachment metadata.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            attachment_id: Attachment identifier
            data: Attachment metadata in JSON:API format

        Returns:
            Response: Updated attachment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "attachmentId": "attachment_id",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "attachmentId"],
        response_type="json",
    )
    def delete_test_record_attachment(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        attachment_id: str,
    ) -> Response:
        """Delete test record attachment.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            attachment_id: Attachment identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/attachments",
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
    def delete_test_record_attachments(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        data: JsonDict,
    ) -> Response:
        """Delete test record attachments.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            data: Attachments to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/attachments"
        return self.polarion_connection.api_request_delete(url, data=data)

    # Test Record Parameters

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/testparameters",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration"],
        response_type="json",
    )
    def get_test_record_test_parameters(
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
        """Get test record test parameters.

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
            Response: List of test parameters from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters"
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
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/testparameters/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testParamId": "test_param_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testParamId"],
        response_type="json",
    )
    def get_test_record_test_parameter(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_param_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test record test parameter.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_param_id: Test parameter identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test parameter data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters/{test_param_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/testparameters",
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
    def create_test_record_test_parameters(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        data: JsonDict,
    ) -> Response:
        """Create test record test parameters.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            data: Test parameters data in JSON:API format

        Returns:
            Response: Created test parameters data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testrecords/{testCaseProjectId}/{testCaseId}/{iteration}/testparameters/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testCaseProjectId": "test_case_project_id",
            "testCaseId": "test_case_id",
            "iteration": "iteration",
            "testParamId": "test_param_id",
        },
        required_params=["projectId", "testRunId", "testCaseProjectId", "testCaseId", "iteration", "testParamId"],
        response_type="json",
    )
    def delete_test_record_test_parameter(
        self,
        project_id: str,
        testrun_id: str,
        test_case_project_id: str,
        test_case_id: str,
        iteration: int,
        test_param_id: str,
    ) -> Response:
        """Delete a specific test record test parameter.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_case_project_id: Test case project identifier
            test_case_id: Test case identifier
            iteration: Iteration number
            test_param_id: Test parameter identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testrecords/{test_case_project_id}/{test_case_id}/{iteration}/testparameters/{test_param_id}"
        return self.polarion_connection.api_request_delete(url)
