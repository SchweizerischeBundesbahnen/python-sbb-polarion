"""Diff Tool utility operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class UtilityMixin(BaseMixin):
    """Utility operations for spaces, documents, work items, and extension info."""

    # =========================================================================
    # Spaces and Documents
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/spaces",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_spaces(self, project_id: str) -> Response:
        """Gets list of spaces (folders) located in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
        },
        required_params=["projectId", "spaceId"],
    )
    def get_documents_in_space(self, project_id: str, space_id: str) -> Response:
        """Gets list of documents located in specified space of specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{docName}/revisions",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "docName": "document_name",
        },
        required_params=["projectId", "spaceId", "docName"],
    )
    def get_document_revisions(self, project_id: str, space_id: str, document_name: str) -> Response:
        """Gets list of revisions for the document located in specified space of specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/revisions"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/duplicate",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "revision": "revision",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName", "__request_body__"],
    )
    def create_document_duplicate(self, project_id: str, space_id: str, document_name: str, data: JsonDict, revision: str | None = None) -> Response:
        """Post request to create duplicate of given document

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/duplicate"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_post(url, params=params or None, data=data)

    # =========================================================================
    # Work Item Fields and Statuses
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/workitem-fields",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_all_workitem_fields(self, project_id: str) -> Response:
        """Gets full list of all general and custom fields configured for all kind of work items in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/workitem-fields"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/workitem-statuses",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_all_workitem_statuses(self, project_id: str) -> Response:
        """Gets list of all statuses configured for all kind of work items in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/workitem-statuses"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/hyperlink-roles",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_all_hyperlink_roles(self, project_id: str) -> Response:
        """Gets list of all hyperlink roles configured in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/hyperlink-roles"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/linked-workitem-roles",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_all_linked_workitem_roles(self, project_id: str) -> Response:
        """Gets list of all linked workitem roles configured in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/linked-workitem-roles"
        return self.polarion_connection.api_request_get(url)

    # =========================================================================
    # Queue Statistics
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/queueStatistics",
        body_param="data",
    )
    def receive_queue_statistics(self, data: JsonDict | None = None) -> Response:
        """Gets queue statistics

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/queueStatistics"
        if data is not None:
            return self.polarion_connection.api_request_post(url, data=data)
        return self.polarion_connection.api_request_post(url)

    @restapi_endpoint(
        method="DELETE",
        path="/api/queueStatistics",
    )
    def clear_queue_statistics(self) -> Response:
        """Clears queue statistics

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/queueStatistics"
        return self.polarion_connection.api_request_delete(url)

    # =========================================================================
    # Extension Info
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/communication/settings",
    )
    def get_communication_settings(self) -> Response:
        """Gets communication settings

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/communication/settings"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/extension/info",
    )
    def get_extension_info(self) -> Response:
        """Gets extension information

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/extension/info"
        return self.polarion_connection.api_request_get(url)
