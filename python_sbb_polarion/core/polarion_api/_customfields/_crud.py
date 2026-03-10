"""Custom fields management operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class CustomFieldsMixin(BaseMixin):
    """Custom fields management operations.

    Provides methods for managing global and project-level custom fields.
    New in Polarion 2512.
    """

    # Global Custom Fields

    @restapi_endpoint(
        method="GET",
        path="/customfields/{resourceType}/{targetType}",
        path_params={
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["resourceType", "targetType"],
        response_type="json",
    )
    def get_global_custom_fields(
        self,
        resource_type: str,
        target_type: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get global custom fields.

        Args:
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: List of custom fields from API
        """
        url: str = f"{self.base_url}/customfields/{resource_type}/{target_type}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/customfields",
        body_param="data",
        response_type="json",
    )
    def create_global_custom_fields(
        self,
        data: JsonDict,
    ) -> Response:
        """Create global custom fields.

        Args:
            data: Custom fields data in JSON:API format

        Returns:
            Response: Created custom fields data from API
        """
        url: str = f"{self.base_url}/customfields"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/customfields/{resourceType}/{targetType}",
        path_params={
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        body_param="data",
        required_params=["resourceType", "targetType"],
        response_type="json",
    )
    def update_global_custom_fields(
        self,
        resource_type: str,
        target_type: str,
        data: JsonDict,
    ) -> Response:
        """Update global custom fields.

        Args:
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)
            data: Custom fields data in JSON:API format

        Returns:
            Response: Updated custom fields data from API
        """
        url: str = f"{self.base_url}/customfields/{resource_type}/{target_type}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/customfields/{resourceType}/{targetType}",
        path_params={
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        required_params=["resourceType", "targetType"],
        response_type="json",
    )
    def delete_global_custom_fields(
        self,
        resource_type: str,
        target_type: str,
    ) -> Response:
        """Delete global custom fields.

        Args:
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)

        Returns:
            Response: Deletion result from API
        """
        url: str = f"{self.base_url}/customfields/{resource_type}/{target_type}"
        return self.polarion_connection.api_request_delete(url)

    # Project Custom Fields

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/customfields/{resourceType}/{targetType}",
        path_params={
            "projectId": "project_id",
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["projectId", "resourceType", "targetType"],
        response_type="json",
    )
    def get_project_custom_fields(
        self,
        project_id: str,
        resource_type: str,
        target_type: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get project-level custom fields.

        Args:
            project_id: Project identifier
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: List of custom fields from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/customfields/{resource_type}/{target_type}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/customfields",
        path_params={"projectId": "project_id"},
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def create_project_custom_fields(
        self,
        project_id: str,
        data: JsonDict,
    ) -> Response:
        """Create project-level custom fields.

        Args:
            project_id: Project identifier
            data: Custom fields data in JSON:API format

        Returns:
            Response: Created custom fields data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/customfields"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/customfields/{resourceType}/{targetType}",
        path_params={
            "projectId": "project_id",
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        body_param="data",
        required_params=["projectId", "resourceType", "targetType"],
        response_type="json",
    )
    def update_project_custom_field(
        self,
        project_id: str,
        resource_type: str,
        target_type: str,
        data: JsonDict,
    ) -> Response:
        """Update project-level custom fields.

        Args:
            project_id: Project identifier
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)
            data: Custom fields data in JSON:API format

        Returns:
            Response: Updated custom fields data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/customfields/{resource_type}/{target_type}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/customfields/{resourceType}/{targetType}",
        path_params={
            "projectId": "project_id",
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        required_params=["projectId", "resourceType", "targetType"],
        response_type="json",
    )
    def delete_project_custom_fields(
        self,
        project_id: str,
        resource_type: str,
        target_type: str,
    ) -> Response:
        """Delete project-level custom fields.

        Args:
            project_id: Project identifier
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)

        Returns:
            Response: Deletion result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/customfields/{resource_type}/{target_type}"
        return self.polarion_connection.api_request_delete(url)
