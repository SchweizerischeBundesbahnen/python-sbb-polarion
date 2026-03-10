"""Workitems fields operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class WorkitemsFieldsMixin(BaseMixin):
    """Workitems fields operations.

    Provides methods for getting field options and managing relationships.
    """

    # Field Options

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/fields/{fieldId}/actions/getAvailableOptions",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "fieldId": "field_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
        },
        required_params=["projectId", "workItemId", "fieldId"],
        response_type="json",
    )
    def get_workitem_available_enum_options(
        self,
        project_id: str,
        workitem_id: str,
        field_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get available enum options for a work item field.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            field_id: Field identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            revision: Specific revision

        Returns:
            Response: List of available enum options from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/fields/{field_id}/actions/getAvailableOptions"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/fields/{fieldId}/actions/getCurrentOptions",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "fieldId": "field_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "fieldId"],
        response_type="json",
    )
    def get_workitem_current_enum_options(
        self,
        project_id: str,
        workitem_id: str,
        field_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get current enum options for a work item field.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            field_id: Field identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            revision: Specific revision

        Returns:
            Response: List of current enum options from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/fields/{field_id}/actions/getCurrentOptions"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/fields/{fieldId}/actions/getAvailableOptions",
        path_params={
            "projectId": "project_id",
            "fieldId": "field_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "type": "type_filter",
        },
        required_params=["projectId", "fieldId"],
        response_type="json",
    )
    def get_workitems_available_enum_options(
        self,
        project_id: str,
        field_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        type_filter: str | None = None,
    ) -> Response:
        """Get available enum options for work items field type.

        Args:
            project_id: Project identifier
            field_id: Field identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            type_filter: Workitem type filter

        Returns:
            Response: List of available enum options from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/fields/{field_id}/actions/getAvailableOptions"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        if type_filter:
            params["type"] = type_filter
        return self.polarion_connection.api_request_get(url, params=params or None)

    # Relationships

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "relationshipId": "relationship_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "relationshipId"],
        response_type="json",
    )
    def get_workitem_relationships(
        self,
        project_id: str,
        workitem_id: str,
        relationship_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get work item relationships.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            relationship_id: Relationship identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/relationships/{relationship_id}"
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
        method="POST",
        path="/projects/{projectId}/workitems/{workItemId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "relationshipId"],
        response_type="json",
    )
    def create_workitem_relationships(
        self,
        project_id: str,
        workitem_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Create work item relationships.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            relationship_id: Relationship identifier
            data: Relationships data in JSON:API format

        Returns:
            Response: Created relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/workitems/{workItemId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "relationshipId"],
        response_type="json",
    )
    def update_workitem_relationships(
        self,
        project_id: str,
        workitem_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Update work item relationships.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            relationship_id: Relationship identifier
            data: Relationships data in JSON:API format

        Returns:
            Response: Updated relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/workitems/{workItemId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "workItemId", "relationshipId"],
        response_type="json",
    )
    def delete_workitem_relationships(
        self,
        project_id: str,
        workitem_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete work item relationships.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            relationship_id: Relationship identifier
            data: Relationships to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_delete(url, data=data)

    # Feature Selections

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/workitems/{workItemId}/featureselections",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_workitem_feature_selections(
        self,
        project_id: str,
        workitem_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get work item feature selections.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of feature selections from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/featureselections"
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
        path="/projects/{projectId}/workitems/{workItemId}/featureselections/{selectionTypeId}/{targetProjectId}/{targetWorkItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "workitem_id",
            "selectionTypeId": "selection_type_id",
            "targetProjectId": "target_project_id",
            "targetWorkItemId": "target_workitem_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "workItemId", "selectionTypeId", "targetProjectId", "targetWorkItemId"],
        response_type="json",
    )
    def get_workitem_feature_selection(
        self,
        project_id: str,
        workitem_id: str,
        selection_type_id: str,
        target_project_id: str,
        target_workitem_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific work item feature selection.

        Args:
            project_id: Project identifier
            workitem_id: Work item identifier
            selection_type_id: Selection type identifier
            target_project_id: Target project identifier
            target_workitem_id: Target work item identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Feature selection data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/featureselections/{selection_type_id}/{target_project_id}/{target_workitem_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)
