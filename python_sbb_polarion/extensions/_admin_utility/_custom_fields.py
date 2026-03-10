"""Admin Utility custom fields management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class CustomFieldsMixin(BaseMixin):
    """Custom fields management operations."""

    @restapi_endpoint(
        method="PUT",
        path="/api/custom-fields",
        body_param="data",
        required_params=["__request_body__"],
    )
    def update_custom_fields_for_default_repo(self, data: JsonDict) -> Response:
        """Update custom fields for default repository

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/custom-fields"
        return self.polarion_connection.api_request_put(url, data=data)

    @restapi_endpoint(
        method="PUT",
        path="/api/projects/{projectId}/custom-fields",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId", "__request_body__"],
    )
    def update_custom_fields_for_project(self, project_id: str, data: JsonDict) -> Response:
        """Update custom fields for project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/custom-fields"
        return self.polarion_connection.api_request_put(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/custom-fields/{entityType}/{typeId}",
        path_params={
            "entityType": "entity_type",
            "typeId": "type_id",
        },
        query_params={
            "projectId": "project_id",
        },
        required_params=["entityType", "typeId"],
    )
    def get_custom_field_declarations(self, entity_type: str, type_id: str, project_id: str | None = None) -> Response:
        """Get field declarations

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/custom-fields/{entity_type}/{type_id}"
        params: dict[str, str] = {}
        if project_id:
            params["projectId"] = project_id
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/api/custom-fields/{entityType}/{typeId}",
        path_params={
            "entityType": "entity_type",
            "typeId": "type_id",
        },
        query_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["entityType", "typeId"],
    )
    def declare_custom_field(self, entity_type: str, type_id: str, data: JsonDict, project_id: str | None = None) -> Response:
        """Declare a custom field

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/custom-fields/{entity_type}/{type_id}"
        params: dict[str, str] = {}
        if project_id:
            params["projectId"] = project_id
        return self.polarion_connection.api_request_post(url, params=params or None, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/api/custom-fields/{entityType}/{typeId}/{fieldId}",
        path_params={
            "entityType": "entity_type",
            "typeId": "type_id",
            "fieldId": "field_id",
        },
        query_params={
            "projectId": "project_id",
        },
        required_params=["entityType", "typeId", "fieldId"],
    )
    def delete_custom_field_declaration(self, entity_type: str, type_id: str, field_id: str, project_id: str | None = None) -> Response:
        """Delete a field declaration

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/custom-fields/{entity_type}/{type_id}/{field_id}"
        params: dict[str, str] = {}
        if project_id:
            params["projectId"] = project_id
        return self.polarion_connection.api_request_delete(url, params=params or None)

    def set_custom_field_type(self, field_id: str, field_name: str, field_type: str, field_description: str | None = None, is_required: bool = False, project_id: str | None = None, work_item_type: str | None = None) -> Response:
        """Create or update custom field type (convenience method)

        Returns:
            Response: Response object from the API call
        """
        data: JsonDict = {
            "workItemType": work_item_type,
            "customFields": [
                {
                    "id": field_id,
                    "name": field_name,
                    "type": field_type,
                    "description": field_description,
                    "isRequired": is_required,
                },
            ],
        }
        if project_id:
            return self.update_custom_fields_for_project(project_id, data)
        return self.update_custom_fields_for_default_repo(data)
