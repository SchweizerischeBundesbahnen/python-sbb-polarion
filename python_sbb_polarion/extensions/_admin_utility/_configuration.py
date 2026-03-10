"""Admin Utility configuration management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response


class ConfigurationMixin(BaseMixin):
    """Configuration management operations for documents and work items."""

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/document-types-config",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_document_types_configuration(self, project_id: str) -> Response:
        """Get currently configured document types

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/document-types-config"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.XML,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/document-custom-fields-config/{documentType}",
        path_params={
            "projectId": "project_id",
            "documentType": "document_type",
        },
        required_params=["projectId", "documentType"],
    )
    def get_document_custom_fields_configuration(self, project_id: str, document_type: str) -> Response:
        """Get currently configured document custom fields

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/document-custom-fields-config/{document_type}"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.XML,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/document-custom-fields-config/{documentType}",
        path_params={
            "projectId": "project_id",
            "documentType": "document_type",
        },
        body_param="configuration_xml",
        required_params=["projectId", "documentType", "__request_body__"],
    )
    def set_document_custom_fields_configuration(self, project_id: str, document_type: str, configuration_xml: str | bytes) -> Response:
        """Update document custom fields xml configuration

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/document-custom-fields-config/{document_type}"
        headers: dict[str, str] = {
            Header.CONTENT_TYPE: MediaType.XML,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, payload=configuration_xml)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/workitem-custom-fields-config/{workitemType}",
        path_params={
            "projectId": "project_id",
            "workitemType": "workitem_type",
        },
        required_params=["projectId", "workitemType"],
    )
    def get_workitem_custom_fields_configuration(self, project_id: str, workitem_type: str) -> Response:
        """Get currently configured workitem custom fields

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/workitem-custom-fields-config/{workitem_type}"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.XML,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/workitem-custom-fields-config/{workitemType}",
        path_params={
            "projectId": "project_id",
            "workitemType": "workitem_type",
        },
        body_param="configuration_xml",
        required_params=["projectId", "workitemType", "__request_body__"],
    )
    def set_workitem_custom_fields_configuration(self, project_id: str, workitem_type: str, configuration_xml: str | bytes) -> Response:
        """Update workitem custom fields xml configuration

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/workitem-custom-fields-config/{workitem_type}"
        headers: dict[str, str] = {
            Header.CONTENT_TYPE: MediaType.XML,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, payload=configuration_xml)
