"""Excel Importer workitems mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class WorkItemsMixin(BaseMixin):
    """WorkItems operations."""

    if TYPE_CHECKING:
        extension_name: str

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/workitem_types",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_workitem_types(self, project_id: str) -> Response:
        """Get workitem types for selected project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/workitem_types"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/workitem_types/{workItemType}/fields",
        path_params={
            "projectId": "project_id",
            "workItemType": "workitem_type",
        },
        required_params=["projectId", "workItemType"],
        response_type="json",
    )
    def get_workitem_fields(self, project_id: str, workitem_type: str) -> Response:
        """Get workitem fields for selected project and workitem type

        Returns:
            Response: Response object from the API call
        """
        url: str = f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/workitem_types/{workitem_type}/fields"
        return self.polarion_connection.api_request_get(url)
