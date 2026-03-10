"""Testruns parameters operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class TestrunsParametersMixin(BaseMixin):
    """Testruns parameters operations.

    Provides methods for managing test run parameters and parameter definitions.
    """

    # Test Parameters

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testparameters",
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
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def get_testrun_test_parameters(
        self,
        project_id: str,
        testrun_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get test run test parameters.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of test parameters from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameters"
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
        path="/projects/{projectId}/testruns/{testRunId}/testparameters/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testParamId": "test_param_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testParamId"],
        response_type="json",
    )
    def get_testrun_test_parameter(
        self,
        project_id: str,
        testrun_id: str,
        test_param_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test run test parameter.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_param_id: Test parameter identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test parameter data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameters/{test_param_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/testparameters",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def create_testrun_test_parameters(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Create test run test parameters.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Test parameters data in JSON:API format

        Returns:
            Response: Created test parameters data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameters"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testparameters",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def delete_testrun_test_parameters(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete test run test parameters.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Test parameters to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameters"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testparameters/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testParamId": "test_param_id",
        },
        required_params=["projectId", "testRunId", "testParamId"],
        response_type="json",
    )
    def delete_testrun_test_parameter(
        self,
        project_id: str,
        testrun_id: str,
        test_param_id: str,
    ) -> Response:
        """Delete a specific test run test parameter.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_param_id: Test parameter identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameters/{test_param_id}"
        return self.polarion_connection.api_request_delete(url)

    # Test Parameter Definitions

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testruns/{testRunId}/testparameterdefinitions",
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
        },
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def get_testrun_test_parameter_definitions(
        self,
        project_id: str,
        testrun_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get test run test parameter definitions.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of test parameter definitions from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameterdefinitions"
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
        path="/projects/{projectId}/testruns/{testRunId}/testparameterdefinitions/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testParamId": "test_param_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "testRunId", "testParamId"],
        response_type="json",
    )
    def get_testrun_test_parameter_definition(
        self,
        project_id: str,
        testrun_id: str,
        test_param_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test run test parameter definition.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_param_id: Test parameter definition identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test parameter definition data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameterdefinitions/{test_param_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testruns/{testRunId}/testparameterdefinitions",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
        },
        body_param="data",
        required_params=["projectId", "testRunId"],
        response_type="json",
    )
    def create_testrun_test_parameter_definitions(
        self,
        project_id: str,
        testrun_id: str,
        data: JsonDict,
    ) -> Response:
        """Create test run test parameter definitions.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            data: Test parameter definitions data in JSON:API format

        Returns:
            Response: Created test parameter definitions data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameterdefinitions"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testruns/{testRunId}/testparameterdefinitions/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testRunId": "testrun_id",
            "testParamId": "test_param_id",
        },
        required_params=["projectId", "testRunId", "testParamId"],
        response_type="json",
    )
    def delete_testrun_test_parameter_definition(
        self,
        project_id: str,
        testrun_id: str,
        test_param_id: str,
    ) -> Response:
        """Delete a specific test run test parameter definition.

        Args:
            project_id: Project identifier
            testrun_id: Test run identifier
            test_param_id: Test parameter definition identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testruns/{testrun_id}/testparameterdefinitions/{test_param_id}"
        return self.polarion_connection.api_request_delete(url)
