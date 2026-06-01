"""Integrity Scanner scan operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class IntegrityScannerMixin(BaseMixin):
    """Integrity scanner endpoints."""

    @restapi_endpoint(
        method="GET",
        path="/api/projects",
    )
    def get_projects(self) -> Response:
        """Gets list of projects accessible to the current user

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/documents",
        path_params={"projectId": "project_id"},
        required_params=["projectId"],
    )
    def get_documents(self, project_id: str) -> Response:
        """Gets list of documents in the given project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/documents"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/scan",
        body_param="scan_params",
        naming_ok=True,
    )
    def scan(self, scan_params: JsonDict) -> Response:
        """Scans a document for the list of documents it refers

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/scan"
        return self.polarion_connection.api_request_post(url, data=scan_params)

    @restapi_endpoint(
        method="GET",
        path="/api/revisions",
        query_params={
            "projectId": "project_id",
            "space": "space",
            "documentName": "document_name",
        },
        required_params=["projectId", "space", "documentName"],
    )
    def get_revisions(self, project_id: str, space: str, document_name: str) -> Response:
        """Gets list of revisions for a particular document

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] = {
            "projectId": project_id,
            "space": space,
            "documentName": document_name,
        }
        url: str = f"{self.rest_api_url}/revisions"
        return self.polarion_connection.api_request_get(url, params=params)
