"""Workitems test steps operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class WorkitemsTestStepsMixin(BaseMixin):
    """Workitems test steps operations.

    Provides methods for managing work item test steps and test parameter definitions.
    """

    # Test Steps

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/teststeps",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_test_steps(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of test steps.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of test steps from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/teststeps"
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
        path="/projects/{projectId}/workitems/{workItemId}/teststeps/{testStepIndex}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "testStepIndex": "test_step_index",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "testStepIndex"],
        response_type="json",
    )
    def get_test_step(
        self,
        project_id: str,
        workitem_id: str,
        test_step_index: int,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test step.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            test_step_index: Test step index (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test step data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/teststeps/{test_step_index}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/teststeps",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_test_steps(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create test steps.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Test steps data in JSON:API format

        Returns:
            Response: Created test steps data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/teststeps"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/teststeps",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def update_test_steps(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Update test steps.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Test steps data in JSON:API format

        Returns:
            Response: Updated test steps data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/teststeps"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/teststeps/{testStepIndex}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "testStepIndex": "test_step_index",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "testStepIndex"],
        response_type="json",
    )
    def update_test_step(
        self,
        project_id: str,
        workitem_id: str,
        test_step_index: int,
        data: JsonDict,
    ) -> Response:
        """Update a specific test step.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            test_step_index: Test step index (0-based)
            data: Test step data in JSON:API format

        Returns:
            Response: Updated test step data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/teststeps/{test_step_index}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/teststeps",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def delete_test_steps(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete test steps.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Test steps to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/teststeps"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/teststeps/{testStepIndex}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "testStepIndex": "test_step_index",
        },
        required_params=["projectId", "workItemId", "testStepIndex"],
        response_type="json",
    )
    def delete_test_step(
        self,
        project_id: str,
        workitem_id: str,
        test_step_index: int,
    ) -> Response:
        """Delete a specific test step.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            test_step_index: Test step index (0-based)

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/teststeps/{test_step_index}"
        return self.polarion_connection.api_request_delete(url)

    # Test Parameter Definitions

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/testparameterdefinitions",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_workitem_test_parameter_definitions(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get test parameter definitions for a work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of test parameter definitions from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/testparameterdefinitions"
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
        path="/projects/{projectId}/workitems/{workItemId}/testparameterdefinitions/{testParamId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "testParamId": "test_param_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "testParamId"],
        response_type="json",
    )
    def get_workitem_test_parameter_definition(
        self,
        project_id: str,
        workitem_id: str,
        test_param_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific test parameter definition for a work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            test_param_id: Test parameter definition identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test parameter definition data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/testparameterdefinitions/{test_param_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)
