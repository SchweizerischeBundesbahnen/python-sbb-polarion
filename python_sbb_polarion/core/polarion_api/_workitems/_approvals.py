"""Workitems approvals operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class WorkitemsApprovalsMixin(BaseMixin):
    """Workitems approvals operations.

    Provides methods for managing work item approvals.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/approvals",
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
    def get_workitem_approvals(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of work item approvals.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of approvals from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/approvals"
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
        path="/projects/{projectId}/workitems/{workItemId}/approvals/{userId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "userId": "user_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "userId"],
        response_type="json",
    )
    def get_workitem_approval(
        self,
        project_id: str,
        workitem_id: str,
        user_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific work item approval.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            user_id: User identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Approval data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/approvals/{user_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/approvals",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_workitem_approvals(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create work item approvals.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Approvals data in JSON:API format

        Returns:
            Response: Created approvals data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/approvals"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/approvals",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def update_workitem_approvals(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Update work item approvals.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Approvals data in JSON:API format

        Returns:
            Response: Updated approvals data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/approvals"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/approvals/{userId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "userId": "user_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "userId"],
        response_type="json",
    )
    def update_workitem_approval(
        self,
        project_id: str,
        workitem_id: str,
        user_id: str,
        data: JsonDict,
    ) -> Response:
        """Update a specific work item approval.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            user_id: User identifier
            data: Approval data in JSON:API format

        Returns:
            Response: Updated approval data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/approvals/{user_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/approvals",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def delete_workitem_approvals(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete work item approvals.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Approvals to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/approvals"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/approvals/{userId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "userId": "user_id",
        },
        required_params=["projectId", "workItemId", "userId"],
        response_type="json",
    )
    def delete_workitem_approval(
        self,
        project_id: str,
        workitem_id: str,
        user_id: str,
    ) -> Response:
        """Delete a specific work item approval.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            user_id: User identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/approvals/{user_id}"
        return self.polarion_connection.api_request_delete(url)
