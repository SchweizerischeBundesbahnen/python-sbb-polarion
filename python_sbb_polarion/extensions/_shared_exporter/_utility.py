"""Shared utility operations mixin for PDF and DOCX exporters.

This module provides utility methods for collections, documents, webhooks, and project info.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class SharedExporterUtilityMixin(BaseMixin):
    """Shared utility operations for exporters.

    This mixin provides methods for:
    - Collection documents
    - Document export filename generation
    - Link role names
    - Document language
    - Webhooks status
    - Project name
    """

    # =========================================================================
    # Collections
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/collections/{collectionId}/documents",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "collectionId"],
        response_type="json",
    )
    def get_documents_from_collection(self, project_id: str, collection_id: str, revision: str | None = None) -> Response:
        """Get documents from collection.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/collections/{collection_id}/documents"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    # =========================================================================
    # Document Info
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/export-filename",
        body_param="data",
        required_params=["__request_body__"],
        response_type="text",
    )
    def generate_document_export_filename(self, data: JsonDict) -> Response:
        """Get filename for converted document.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/export-filename"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/link-role-names",
        query_params={
            "scope": "scope",
        },
        required_params=["scope"],
        response_type="json",
    )
    def get_link_role_names(self, scope: str) -> Response:
        """Get names of link-roles from requested scope.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/link-role-names"
        params: dict[str, str] = {
            "scope": scope,
        }
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/document-language",
        query_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "revision": "revision",
        },
        required_params=[],
        response_type="text",
    )
    def get_document_language(self, project_id: str, space_id: str, document_name: str, revision: str | None = None) -> Response:
        """Get language of requested document.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/document-language"
        params: dict[str, str] = {
            "projectId": project_id,
            "spaceId": space_id,
            "documentName": document_name,
        }
        if revision:
            params["revision"] = revision

        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_get(url, headers=headers, params=params)

    # =========================================================================
    # Webhooks and Project
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/webhooks/status",
        required_params=[],
        response_type="json",
    )
    def get_webhooks_status(self) -> Response:
        """Get status of webhooks.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/webhooks/status"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/name",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
        response_type="text",
    )
    def get_project_name(self, project_id: str) -> Response:
        """Get name of requested project.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/name"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)
