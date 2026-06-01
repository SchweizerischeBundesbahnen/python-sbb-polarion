"""Test Data documents mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class DocumentsMixin(BaseMixin):
    """Document operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{documentName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "quantity": "quantity",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="text",
    )
    def create_document_with_generated_workitems(self, project_id: str, space_id: str, document_name: str, quantity: int | None = None) -> Response:
        """Create test live document with generated workitems

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}"
        params: dict[str, str] = {}
        if quantity:
            params["quantity"] = str(quantity)
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/append",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "quantity": "quantity",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="text",
    )
    def extend_document_with_generated_workitems(self, project_id: str, space_id: str, document_name: str, quantity: int | None = None) -> Response:
        """Extend test live document with generated workitems

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/append"
        params: dict[str, str] = {}
        if quantity:
            params["quantity"] = str(quantity)
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_patch(url, headers=headers, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/change-wi-descriptions",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "interval": "interval",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="text",
    )
    def change_document_work_item_descriptions(self, project_id: str, space_id: str, document_name: str, interval: int | None = None) -> Response:
        """Update workitem descriptions in specified document

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/change-wi-descriptions"
        params: dict[str, str] = {}
        if interval:
            params["interval"] = str(interval)
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PLAIN,
        }
        return self.polarion_connection.api_request_patch(url, headers=headers, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/baselines/{baselineName}",
        path_params={
            "projectId": "project_id",
            "baselineName": "baseline_name",
        },
        query_params={
            "description": "description",
            "revision": "revision",
        },
        required_params=["projectId", "baselineName"],
    )
    def create_baseline(self, project_id: str, baseline_name: str, description: str | None = None, revision: str | None = None) -> Response:
        """Create a baseline in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/baselines/{baseline_name}"
        params: dict[str, str] = {}
        if description:
            params["description"] = description
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_post(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/collections/{collectionName}",
        path_params={
            "projectId": "project_id",
            "collectionName": "collection_name",
        },
        body_param="data",
        required_params=["projectId", "collectionName", "__request_body__"],
    )
    def create_collection(self, project_id: str, collection_name: str, data: JsonDict) -> Response:
        """Create a collection in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/collections/{collection_name}"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/cross-document-links",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId", "__request_body__"],
    )
    def create_cross_document_links(self, project_id: str, data: JsonDict) -> Response:
        """Create cross-document links in specified project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/cross-document-links"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/linked-revisions",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName", "__request_body__"],
    )
    def add_linked_revisions(self, project_id: str, space_id: str, document_name: str, data: JsonDict) -> Response:
        """Add linked revisions to specified document

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/linked-revisions"
        return self.polarion_connection.api_request_post(url, data=data)
