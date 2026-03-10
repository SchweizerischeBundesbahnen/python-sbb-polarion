"""Cucumber features mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class FeaturesMixin(BaseMixin):
    """Features operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/2/field",
        required_params=["projectId"],
        response_type="json",
    )
    def get_jira_fields(self, project_id: str) -> Response:
        """Get jira fields

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/2/field"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.JSON,
            "projectId": project_id,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)

    @restapi_endpoint(
        method="POST",
        path="/api/feature",
        body_param="feature_data",
        required_params=["__request_body__"],
        response_type="json",
    )
    def save_feature(self, project_id: str, workitem_id: str, title: str, content: str) -> Response:
        """Save feature

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/feature"
        filename: str = f"{workitem_id}.feature"
        data: JsonDict = {
            "projectId": project_id,
            "workItemId": workitem_id,
            "title": title,
            "filename": filename,
            "content": content,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/feature/{projectId}/{workItemId}",
        path_params={
            "projectId": "project_id",
            "workItemId": "work_item_id",
        },
        required_params=["projectId", "workItemId"],
        response_type="json",
    )
    def get_feature(self, project_id: str, work_item_id: str) -> Response:
        """Get feature

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/feature/{project_id}/{work_item_id}"
        return self.polarion_connection.api_request_get(url)
