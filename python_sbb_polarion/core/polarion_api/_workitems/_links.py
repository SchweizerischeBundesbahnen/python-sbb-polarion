"""Workitems links operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class WorkitemsLinksMixin(BaseMixin):
    """Workitems links operations.

    Provides methods for managing work item links including internal links,
    external links, and OSLC resources.
    """

    # Internal Linked Work Items

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/linkedworkitems",
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
    def get_linked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get linked work items.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of linked work items from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedworkitems"
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
        path="/projects/{projectId}/workitems/{workItemId}/linkedworkitems/{roleId}/{targetProjectId}/{linkedWorkItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "roleId": "role_id",
            "targetProjectId": "target_project_id",
            "linkedWorkItemId": "linked_workitem_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "roleId", "targetProjectId", "linkedWorkItemId"],
        response_type="json",
    )
    def get_linked_workitem(
        self,
        project_id: str,
        workitem_id: str,
        role_id: str,
        target_project_id: str,
        linked_workitem_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific linked work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            role_id: Link role identifier
            target_project_id: Target project identifier
            linked_workitem_id: Linked work item identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Linked work item data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_workitem_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/linkedworkitems",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_linked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create linked work items.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Linked work items data in JSON:API format

        Returns:
            Response: Created linked work items data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedworkitems"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/linkedworkitems/{roleId}/{targetProjectId}/{linkedWorkItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "roleId": "role_id",
            "targetProjectId": "target_project_id",
            "linkedWorkItemId": "linked_workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "roleId", "targetProjectId", "linkedWorkItemId"],
        response_type="json",
    )
    def update_linked_workitem(
        self,
        project_id: str,
        workitem_id: str,
        role_id: str,
        target_project_id: str,
        linked_workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Update a linked work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            role_id: Link role identifier
            target_project_id: Target project identifier
            linked_workitem_id: Linked work item identifier
            data: Link data in JSON:API format

        Returns:
            Response: Updated link data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_workitem_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/linkedworkitems",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def delete_linked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete linked work items.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Links to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedworkitems"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/linkedworkitems/{roleId}/{targetProjectId}/{linkedWorkItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "roleId": "role_id",
            "targetProjectId": "target_project_id",
            "linkedWorkItemId": "linked_workitem_id",
        },
        required_params=["projectId", "workItemId", "roleId", "targetProjectId", "linkedWorkItemId"],
        response_type="json",
    )
    def delete_linked_workitem(
        self,
        project_id: str,
        workitem_id: str,
        role_id: str,
        target_project_id: str,
        linked_workitem_id: str,
    ) -> Response:
        """Delete a specific linked work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            role_id: Link role identifier
            target_project_id: Target project identifier
            linked_workitem_id: Linked work item identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedworkitems/{role_id}/{target_project_id}/{linked_workitem_id}"
        return self.polarion_connection.api_request_delete(url)

    # Externally Linked Work Items

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/externallylinkedworkitems",
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
    def get_externally_linked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get externally linked work items.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of externally linked work items from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/externallylinkedworkitems"
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
        path="/projects/{projectId}/workitems/{workItemId}/externallylinkedworkitems/{roleId}/{hostname}/{targetProjectId}/{linkedWorkItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "roleId": "role_id",
            "hostname": "hostname",
            "targetProjectId": "target_project_id",
            "linkedWorkItemId": "linked_workitem_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "roleId", "hostname", "targetProjectId", "linkedWorkItemId"],
        response_type="json",
    )
    def get_externally_linked_workitem(
        self,
        project_id: str,
        workitem_id: str,
        role_id: str,
        hostname: str,
        target_project_id: str,
        linked_workitem_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific externally linked work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            role_id: Link role identifier
            hostname: External server hostname
            target_project_id: Target project identifier
            linked_workitem_id: Linked work item identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Externally linked work item data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/externallylinkedworkitems/{role_id}/{hostname}/{target_project_id}/{linked_workitem_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/externallylinkedworkitems",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_externally_linked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create externally linked work items.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: External links data in JSON:API format

        Returns:
            Response: Created external links data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/externallylinkedworkitems"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/externallylinkedworkitems",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def delete_externally_linked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete externally linked work items.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: External links to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/externallylinkedworkitems"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/externallylinkedworkitems/{roleId}/{hostname}/{targetProjectId}/{linkedWorkItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "roleId": "role_id",
            "hostname": "hostname",
            "targetProjectId": "target_project_id",
            "linkedWorkItemId": "linked_workitem_id",
        },
        required_params=["projectId", "workItemId", "roleId", "hostname", "targetProjectId", "linkedWorkItemId"],
        response_type="json",
    )
    def delete_externally_linked_workitem(
        self,
        project_id: str,
        workitem_id: str,
        role_id: str,
        hostname: str,
        target_project_id: str,
        linked_workitem_id: str,
    ) -> Response:
        """Delete a specific externally linked work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            role_id: Link role identifier
            hostname: External server hostname
            target_project_id: Target project identifier
            linked_workitem_id: Linked work item identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/externallylinkedworkitems/{role_id}/{hostname}/{target_project_id}/{linked_workitem_id}"
        return self.polarion_connection.api_request_delete(url)

    # OSLC Resources

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/linkedoslcresources",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_oslc_resources(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get linked OSLC resources.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Query specification
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of OSLC resources from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedoslcresources"
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
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/linkedoslcresources",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_oslc_resources(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create linked OSLC resources.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: OSLC resources data in JSON:API format

        Returns:
            Response: Created OSLC resources data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedoslcresources"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/linkedoslcresources",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def delete_oslc_resources(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete linked OSLC resources.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: OSLC resources to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/linkedoslcresources"
        return self.polarion_connection.api_request_delete(url, data=data)

    # Backlinked Work Items - New in Polarion 2512

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/backlinkedworkitems",
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
    def get_backlinked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get backlinked work items (incoming links from other work items).

        Returns the incoming links from other Work Items (also known as backlinks).
        Does not pertain to External links.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of backlinked work items from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/backlinkedworkitems"
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
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/backlinkedworkitems",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_backlinked_workitems(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create backlinked work items.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Backlink data in JSON:API format

        Returns:
            Response: Created backlinks data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/backlinkedworkitems"
        return self.polarion_connection.api_request_post(url, data=data)
