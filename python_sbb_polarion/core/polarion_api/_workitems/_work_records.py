"""Workitems work records operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class WorkitemsWorkRecordsMixin(BaseMixin):
    """Workitems work records operations.

    Provides methods for managing work item work records (time tracking).
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/workrecords",
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
    def get_work_records(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of work records.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of work records from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/workrecords"
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
        path="/projects/{projectId}/workitems/{workItemId}/workrecords/{workRecordId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "workRecordId": "work_record_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "workRecordId"],
        response_type="json",
    )
    def get_work_record(
        self,
        project_id: str,
        workitem_id: str,
        work_record_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific work record.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            work_record_id: Work record identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Work record data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/workrecords/{work_record_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/workrecords",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def create_work_records(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Create work records.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Work records data in JSON:API format

        Returns:
            Response: Created work records data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/workrecords"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/workrecords",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def delete_work_records(
        self,
        project_id: str,
        workitem_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete work records.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            data: Work records to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/workrecords"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/workrecords/{workRecordId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "workRecordId": "work_record_id",
        },
        required_params=["projectId", "workItemId", "workRecordId"],
        response_type="json",
    )
    def delete_work_record(
        self,
        project_id: str,
        workitem_id: str,
        work_record_id: str,
    ) -> Response:
        """Delete a specific work record.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            work_record_id: Work record identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/workrecords/{work_record_id}"
        return self.polarion_connection.api_request_delete(url)
