"""Projects enumerations operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class ProjectsEnumerationsMixin(BaseMixin):
    """Projects enumerations operations.

    Provides methods for managing project-level enumerations and icons.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/enumerations",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_project_enumerations(
        self,
        project_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get project enumerations.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: List of project enumerations from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/enumerations",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def create_project_enumeration(
        self,
        project_id: str,
        data: JsonDict,
    ) -> Response:
        """Create a project enumeration.

        Args:
            project_id: Project identifier
            data: Enumeration data in JSON:API format

        Returns:
            Response: Created enumeration data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/enumerations/{enumContext}/{enumName}/{targetType}",
        path_params={
            "projectId": "project_id",
            "enumContext": "enum_context",
            "enumName": "enum_name",
            "targetType": "target_type",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["projectId", "enumContext", "enumName", "targetType"],
        response_type="json",
    )
    def get_project_enumeration(
        self,
        project_id: str,
        enum_context: str,
        enum_name: str,
        target_type: str,
        fields: SparseFields | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific project enumeration.

        Args:
            project_id: Project identifier
            enum_context: Enumeration context
            enum_name: Enumeration name
            target_type: Target type
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            revision: Specific revision

        Returns:
            Response: Enumeration data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations/{enum_context}/{enum_name}/{target_type}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/enumerations/{enumContext}/{enumName}/{targetType}",
        path_params={
            "projectId": "project_id",
            "enumContext": "enum_context",
            "enumName": "enum_name",
            "targetType": "target_type",
        },
        body_param="data",
        required_params=["projectId", "enumContext", "enumName", "targetType"],
        response_type="json",
    )
    def update_project_enumeration(
        self,
        project_id: str,
        enum_context: str,
        enum_name: str,
        target_type: str,
        data: JsonDict,
    ) -> Response:
        """Update a project enumeration.

        Args:
            project_id: Project identifier
            enum_context: Enumeration context
            enum_name: Enumeration name
            target_type: Target type
            data: Enumeration data in JSON:API format

        Returns:
            Response: Updated enumeration data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations/{enum_context}/{enum_name}/{target_type}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/enumerations/{enumContext}/{enumName}/{targetType}",
        path_params={
            "projectId": "project_id",
            "enumContext": "enum_context",
            "enumName": "enum_name",
            "targetType": "target_type",
        },
        required_params=["projectId", "enumContext", "enumName", "targetType"],
        response_type="json",
    )
    def delete_project_enumeration(
        self,
        project_id: str,
        enum_context: str,
        enum_name: str,
        target_type: str,
    ) -> Response:
        """Delete a project enumeration.

        Args:
            project_id: Project identifier
            enum_context: Enumeration context
            enum_name: Enumeration name
            target_type: Target type

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations/{enum_context}/{enum_name}/{target_type}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/enumerations/icons",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_project_icons(
        self,
        project_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get list of project icons.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: List of icons from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations/icons"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/enumerations/icons/{iconId}",
        path_params={
            "projectId": "project_id",
            "iconId": "icon_id",
        },
        query_params={
            "fields": "fields",
        },
        required_params=["projectId", "iconId"],
        response_type="json",
    )
    def get_project_icon(
        self,
        project_id: str,
        icon_id: str,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get a specific project icon.

        Args:
            project_id: Project identifier
            icon_id: Icon identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: Icon data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations/icons/{icon_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/enumerations/icons",
        path_params={
            "projectId": "project_id",
        },
        multipart_fields={
            "files": "files",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def create_project_icons(
        self,
        project_id: str,
        files: FilesDict,
    ) -> Response:
        """Create project icons.

        Args:
            project_id: Project identifier
            files: Files dict with icon data

        Returns:
            Response: Created icons data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/enumerations/icons"
        return self.polarion_connection.api_request_post(url, files=files)
