"""Admin Utility custom fields management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import deprecated_method, restapi_endpoint
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
    @deprecated_method("PolarionApiV1.update_global_custom_fields")
    def update_custom_fields_for_default_repo(self, data: JsonDict) -> Response:
        """Update custom fields for default repository

        .. deprecated::
            Use ``PolarionApiV1.update_global_custom_fields`` instead. The standard Polarion REST
            API v1 covers global custom field updates since Polarion 2606.

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
    @deprecated_method("PolarionApiV1.update_project_custom_field")
    def update_custom_fields_for_project(self, project_id: str, data: JsonDict) -> Response:
        """Update custom fields for project

        .. deprecated::
            Use ``PolarionApiV1.update_project_custom_field`` instead. The standard Polarion REST
            API v1 covers project custom field updates since Polarion 2606.

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
    @deprecated_method("PolarionApiV1.get_global_custom_fields / PolarionApiV1.get_project_custom_fields")
    def get_custom_field_declarations(self, entity_type: str, type_id: str, project_id: str | None = None) -> Response:
        """Get field declarations

        .. deprecated::
            Use ``PolarionApiV1.get_global_custom_fields`` (or ``get_project_custom_fields`` when a
            project is given) instead. Covered by the standard Polarion REST API v1 since Polarion 2606.

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
    @deprecated_method("PolarionApiV1.create_global_custom_fields / PolarionApiV1.create_project_custom_fields")
    def declare_custom_field(self, entity_type: str, type_id: str, data: JsonDict, project_id: str | None = None) -> Response:
        """Declare a custom field

        .. deprecated::
            Use ``PolarionApiV1.create_global_custom_fields`` (or ``create_project_custom_fields`` when a
            project is given) instead. Covered by the standard Polarion REST API v1 since Polarion 2606.

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
    @deprecated_method("PolarionApiV1 custom fields API (emulate get + update of the remaining fields)")
    def delete_custom_field_declaration(self, entity_type: str, type_id: str, field_id: str, project_id: str | None = None) -> Response:
        """Delete a field declaration

        .. deprecated::
            Use the standard Polarion REST API v1 custom fields API instead. There is no direct
            per-field delete: the standard ``DELETE`` drops the whole target config, so emulate a
            single-field delete by reading the declarations and updating with the remaining fields.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/custom-fields/{entity_type}/{type_id}/{field_id}"
        params: dict[str, str] = {}
        if project_id:
            params["projectId"] = project_id
        return self.polarion_connection.api_request_delete(url, params=params or None)

    @deprecated_method("PolarionApiV1.update_project_custom_field / PolarionApiV1.update_global_custom_fields")
    def set_custom_field_type(self, field_id: str, field_name: str, field_type: str, field_description: str | None = None, is_required: bool = False, project_id: str | None = None, work_item_type: str | None = None) -> Response:
        """Create or update custom field type (convenience method)

        .. deprecated::
            Use ``PolarionApiV1.update_project_custom_field`` (or ``update_global_custom_fields`` for the
            default repository) instead. Covered by the standard Polarion REST API v1 since Polarion 2606.

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
        # Issue the request directly rather than delegating to the (also deprecated) update methods:
        # that keeps this to a single DeprecationWarning without the thread-unsafe warnings.catch_warnings()
        # (warnings filter state is global before Python 3.12).
        if project_id:
            url: str = f"{self.rest_api_url}/projects/{project_id}/custom-fields"
        else:
            url = f"{self.rest_api_url}/custom-fields"
        return self.polarion_connection.api_request_put(url, data=data)
