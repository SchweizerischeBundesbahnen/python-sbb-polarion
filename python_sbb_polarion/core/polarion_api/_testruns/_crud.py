"""Testruns CRUD operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class TestrunsCrudMixin(BaseMixin):
    """Testruns CRUD operations.

    Provides methods for creating, reading, updating, and deleting test runs,
    as well as import/export actions.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
            "templates": "templates",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_testruns(
        self,
        project_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
        templates: str | None = None,
    ) -> Response:
        """Get list of test runs.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query string
            sort: Sort specification
            revision: Specific revision
            templates: Filter by templates

        Returns:
            Response: List of test runs from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if query:
            params["query"] = query
        if sort:
            params["sort"] = sort
        if revision:
            params["revision"] = revision
        if templates:
            params["templates"] = templates
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def get_testrun(
        self,
        project_id: str,
        testrun_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test run.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test run data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def create_testruns(self, project_id: str, data: JsonDict) -> Response:
        """Create test runs.

        Args:
            project_id: Project identifier
            data: Test runs data in JSON:API format

        Returns:
            Response: Created test runs data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns/{testRunId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        helper_params=["workflow_action"],
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def update_testrun(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
        workflow_action: str | None = None,
    ) -> Response:
        """Update a test run.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Test run data in JSON:API format
            workflow_action: Workflow action to execute

        Returns:
            Response: Updated test run data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}"
        params: dict[str, str] = {}
        if workflow_action:
            params["workflowAction"] = workflow_action
        return self.polarion_connection.api_request_patch(url, data=data, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/testruns",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        helper_params=["workflow_action"],
        required_params=["projectId"],
        response_type="json",
    )
    def update_testruns(
        self,
        project_id: str,
        data: JsonDict,
        workflow_action: str | None = None,
    ) -> Response:
        """Update multiple test runs.

        Args:
            project_id: Project identifier
            data: Test runs data in JSON:API format
            workflow_action: Workflow action to execute

        Returns:
            Response: Updated test runs data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns"
        params: dict[str, str] = {}
        if workflow_action:
            params["workflowAction"] = workflow_action
        return self.polarion_connection.api_request_patch(url, data=data, params=params or None)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def delete_testruns(self, project_id: str, data: JsonDict) -> Response:
        """Delete test runs.

        Args:
            project_id: Project identifier
            data: Test runs to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def delete_testrun(self, project_id: str, testrun_id: str) -> Response:
        """Delete a specific test run.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/actions/getWorkflowActions",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def get_testrun_workflow_actions(
        self,
        project_id: str,
        testrun_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get available workflow actions for a test run.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            revision: Specific revision

        Returns:
            Response: List of available workflow actions
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/actions/getWorkflowActions"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/actions/exportTestsToExcel",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        query_params={
            "query": "query",
            "sortBy": "sort_by",
            "template": "template",
        },
        helper_params=["revision"],
        required_params=["projectId", "testRunId"],
        response_type="binary",
    )
    def export_tests_to_excel(
        self,
        project_id: str,
        testrun_id: str,
        query: str | None = None,
        sort_by: str | None = None,
        template: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Export tests to Excel.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            query: Query filter for tests
            sort_by: Sort specification
            template: Template to use for export
            revision: Specific revision

        Returns:
            Response: Excel file content
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/actions/exportTestsToExcel"
        params: dict[str, str] = {}
        if query:
            params["query"] = query
        if sort_by:
            params["sortBy"] = sort_by
        if template:
            params["template"] = template
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/actions/importExcelTestResults",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        multipart_fields={
            "file": "files",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def import_excel_test_results(
        self,
        project_id: str,
        testrun_id: str,
        files: FilesDict,
    ) -> Response:
        """Import test results from Excel.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            files: Files dict with Excel file content

        Returns:
            Response: Import result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/actions/importExcelTestResults"
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/actions/importXUnitTestResults",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        multipart_fields={
            "file": "files",
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def import_xunit_test_results(
        self,
        project_id: str,
        testrun_id: str,
        files: FilesDict,
    ) -> Response:
        """Import test results from xUnit XML.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            files: Files dict with xUnit XML file content

        Returns:
            Response: Import result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/actions/importXUnitTestResults"
        return self.polarion_connection.api_request_post(url, files=files)
