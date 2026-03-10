"""Projects CRUD operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class ProjectsCrudMixin(BaseMixin):
    """Projects CRUD operations.

    Provides methods for managing projects.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects",
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        response_type="json",
    )
    def get_projects(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of projects.

        Args:
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query string
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of projects from API
        """
        url: str = f"{self.base_url}/projects"
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
        method="GET",
        path="/projects/{projectId}",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_project(
        self,
        project_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific project.

        Args:
            project_id: Project identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Project data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/actions/createProject",
        body_param="data",
        response_type="json",
    )
    def create_project(self, data: JsonDict) -> Response:
        """Create a project.

        Args:
            data: Project data in JSON:API format

        Returns:
            Response: Created project data from API
        """
        url: str = f"{self.base_url}/projects/actions/createProject"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def update_project(self, project_id: str, data: JsonDict) -> Response:
        """Update a project.

        Args:
            project_id: Project identifier
            data: Project data in JSON:API format

        Returns:
            Response: Updated project data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def delete_project(self, project_id: str) -> Response:
        """Delete a project.

        Args:
            project_id: Project identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="GET",
        path="/projecttemplates",
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
        },
        response_type="json",
    )
    def get_project_templates(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get list of project templates.

        Args:
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: List of project templates from API
        """
        url: str = f"{self.base_url}/projecttemplates"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    # New endpoints in Polarion 2512

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/actions/getFieldsMetadata",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            "resourceType": "resource_type",
            "targetType": "target_type",
        },
        required_params=["projectId", "resourceType"],
        response_type="json",
    )
    def get_project_fields_metadata(
        self,
        project_id: str,
        resource_type: str,
        target_type: str | None = None,
    ) -> Response:
        """Get project fields metadata.

        Args:
            project_id: Project identifier
            resource_type: Resource type (e.g., 'workitems', 'documents')
            target_type: Target type (e.g., work item type)

        Returns:
            Response: Project fields metadata from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/actions/getFieldsMetadata"
        params: dict[str, str] = {
            "resourceType": resource_type,
        }
        if target_type:
            params["targetType"] = target_type
        return self.polarion_connection.api_request_get(url, params=params)
