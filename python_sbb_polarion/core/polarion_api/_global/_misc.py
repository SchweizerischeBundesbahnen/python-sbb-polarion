"""Miscellaneous global operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class MiscMixin(BaseMixin):
    """Miscellaneous global operations.

    Provides methods for roles, user groups, global workitems, and test parameter definitions.
    """

    @restapi_endpoint(
        method="GET",
        path="/roles/{roleId}",
        path_params={
            "roleId": "role_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["roleId"],
        response_type="json",
    )
    def get_role(
        self,
        role_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get a specific role.

        Args:
            role_id: Role identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: Role data from API
        """
        url: str = f"{self.base_url}/roles/{role_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/usergroups/{groupId}",
        path_params={
            "groupId": "group_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["groupId"],
        response_type="json",
    )
    def get_user_group(
        self,
        group_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific user group.

        Args:
            group_id: Group identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: User group data from API
        """
        url: str = f"{self.base_url}/usergroups/{group_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    # Global Workitems

    @restapi_endpoint(
        method="GET",
        path="/all/workitems",
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        required_params=[],
        response_type="json",
        naming_ok=True,
    )
    def get_all_workitems(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get all workitems from global context.

        Args:
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query string
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of workitems from API
        """
        url: str = f"{self.base_url}/all/workitems"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if query:
            params["query"] = query
        if sort:
            params["sort"] = sort
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/all/workitems",
        query_params={
            "workflowAction": "workflow_action",
        },
        body_param="data",
        required_params=[],
        response_type="json",
        naming_ok=True,
    )
    def update_all_workitems(
        self,
        data: JsonDict,
        workflow_action: str | None = None,
    ) -> Response:
        """Update workitems in global context.

        Args:
            data: Workitems data in JSON:API format
            workflow_action: Workflow action to execute

        Returns:
            Response: Updated workitems data from API
        """
        url: str = f"{self.base_url}/all/workitems"
        params: dict[str, str] = {}
        if workflow_action:
            params["workflowAction"] = workflow_action
        return self.polarion_connection.api_request_patch(url, data=data, params=params or None)

    @restapi_endpoint(
        method="DELETE",
        path="/all/workitems",
        body_param="data",
        required_params=[],
        response_type="json",
        naming_ok=True,
    )
    def delete_all_workitems(self, data: JsonDict) -> Response:
        """Delete workitems from global context.

        Args:
            data: Workitems to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/all/workitems"
        return self.polarion_connection.api_request_delete(url, data=data)

    # Project Test Parameter Definitions

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/testparameterdefinitions",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
        },
        required_params=["projectId"],
        response_type="json",
        naming_ok=True,
    )
    def get_project_test_parameter_definitions(
        self,
        project_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get project test parameter definitions.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of test parameter definitions from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testparameterdefinitions"
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
        path="/projects/{projectId}/testparameterdefinitions/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testParamId": "test_param_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["projectId", "testParamId"],
        response_type="json",
    )
    def get_project_test_parameter_definition(
        self,
        project_id: str,
        test_param_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific project test parameter definition.

        Args:
            project_id: Project identifier
            test_param_id: Test parameter definition identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Test parameter definition data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testparameterdefinitions/{test_param_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/testparameterdefinitions",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def create_project_test_parameter_definitions(
        self,
        project_id: str,
        data: JsonDict,
    ) -> Response:
        """Create project test parameter definitions.

        Args:
            project_id: Project identifier
            data: Test parameter definitions data in JSON:API format

        Returns:
            Response: Created test parameter definitions data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testparameterdefinitions"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testparameterdefinitions",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def delete_project_test_parameter_definitions(
        self,
        project_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete project test parameter definitions.

        Args:
            project_id: Project identifier
            data: Test parameter definitions to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testparameterdefinitions"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/testparameterdefinitions/{testParamId}",
        path_params={
            "projectId": "project_id",
            "testParamId": "test_param_id",
        },
        required_params=["projectId", "testParamId"],
        response_type="json",
    )
    def delete_project_test_parameter_definition(
        self,
        project_id: str,
        test_param_id: str,
    ) -> Response:
        """Delete a specific project test parameter definition.

        Args:
            project_id: Project identifier
            test_param_id: Test parameter definition identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/testparameterdefinitions/{test_param_id}"
        return self.polarion_connection.api_request_delete(url)

    # New endpoints in Polarion 2512

    @restapi_endpoint(
        method="GET",
        path="/enumerations",
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
        },
        response_type="json",
    )
    def get_global_enumerations(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get global enumerations.

        Args:
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: List of global enumerations from API
        """
        url: str = f"{self.base_url}/enumerations"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/actions/getFieldsMetadata",
        query_params={
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        required_params=["resourceType"],
        response_type="json",
    )
    def get_global_fields_metadata(
        self,
        resource_type: str,
        target_type: str | None = None,
    ) -> Response:
        """Get global fields metadata.

        Args:
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)

        Returns:
            Response: Global fields metadata from API
        """
        url: str = f"{self.base_url}/actions/getFieldsMetadata"
        params: dict[str, str] = {
            "resourceType": resource_type,
        }
        if target_type:
            params["targetType"] = target_type
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/metadata",
        query_params={
            "fields": "fields",
            "include": "include",
        },
        response_type="json",
    )
    def get_metadata(
        self,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get Polarion metadata.

        Args:
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: Polarion metadata from API
        """
        url: str = f"{self.base_url}/metadata"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)
