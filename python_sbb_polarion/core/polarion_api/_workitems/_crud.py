"""Workitems CRUD operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class WorkitemsCrudMixin(BaseMixin):
    """Workitems CRUD operations.

    Provides methods for creating, reading, updating, and deleting work items,
    as well as moving them between documents.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_workitem(
        self,
        project_id: str,
        workitem_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get work item by ID.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            fields: JSON:API sparse fieldsets dict mapping resource type to field spec.
                    Example: {"workitems": "@all"} produces ?fields[workitems]=@all
            include: Include related resources (e.g., "author,assignee")
            revision: Specific revision to retrieve

        Returns:
            Response: Work item data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems",
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
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_workitems(
        self,
        project_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of work items.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict mapping resource type to field spec.
                    Example: {"workitems": "@all"} produces ?fields[workitems]=@all
            include: Include related resources
            query: Lucene query string
            sort: Sort specification (e.g., "id,-created")
            revision: Specific revision to retrieve

        Returns:
            Response: List of work items from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems"
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
        path="/projects/{projectId}/workitems",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def create_workitems(self, project_id: str, data: JsonDict) -> Response:
        """Create work items.

        Args:
            project_id: Project identifier
            data: Work items data in JSON:API format

        Returns:
            Response: Created work items data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            "workflowAction": "workflow_action",
            "changeTypeTo": "change_type_to",
        },
        body_param="attributes",
        helper_params=["attributes"],
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def update_workitem(
        self,
        project_id: str,
        workitem_id: str,
        attributes: JsonDict,
        workflow_action: str | None = None,
        change_type_to: str | None = None,
    ) -> Response:
        """Update a single work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            attributes: Work item attributes to update (will be wrapped in JSON:API format)
            workflow_action: Workflow action to execute
            change_type_to: Change work item type

        Returns:
            Response: Updated work item data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}"
        params: dict[str, str] = {}
        if workflow_action:
            params["workflowAction"] = workflow_action
        if change_type_to:
            params["changeTypeTo"] = change_type_to
        data: JsonDict = {
            "data": {
                "type": "workitems",
                "id": f"{project_id}/{workitem_id}",
                "attributes": attributes,
            }
        }
        return self.polarion_connection.api_request_patch(url, data=data, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            "workflowAction": "workflow_action",
            "changeTypeTo": "change_type_to",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def update_workitems(
        self,
        project_id: str,
        data: JsonDict,
        workflow_action: str | None = None,
        change_type_to: str | None = None,
    ) -> Response:
        """Update multiple work items.

        Args:
            project_id: Project identifier
            data: Work items data in JSON:API format
            workflow_action: Workflow action to execute
            change_type_to: Change work item type

        Returns:
            Response: Updated work items data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems"
        params: dict[str, str] = {}
        if workflow_action:
            params["workflowAction"] = workflow_action
        if change_type_to:
            params["changeTypeTo"] = change_type_to
        return self.polarion_connection.api_request_patch(url, data=data, params=params or None)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def delete_workitems(self, project_id: str, data: JsonDict) -> Response:
        """Delete work items.

        Args:
            project_id: Project identifier
            data: Work items to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/actions/getWorkflowActions",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_workflow_actions(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get available workflow actions for a work item.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            revision: Specific revision

        Returns:
            Response: List of available workflow actions
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/actions/getWorkflowActions"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/actions/moveToDocument",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def move_workitem_to_document(self, project_id: str, workitem_id: str, data: JsonDict) -> Response:
        """Move work item into a document.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Target document specification

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/actions/moveToDocument"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/actions/moveFromDocument",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def move_workitem_from_document(self, project_id: str, workitem_id: str, data: JsonDict) -> Response:
        """Move work item out of a document.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Move specification

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/actions/moveFromDocument"
        return self.polarion_connection.api_request_post(url, data=data)
