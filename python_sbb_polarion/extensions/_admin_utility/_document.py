"""Admin Utility document (module) management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header


if TYPE_CHECKING:
    from requests import Response


class DocumentMixin(BaseMixin):
    """Document (module) management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{documentName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        body_param="payload",
        header_params={
            Header.CONTENT_TYPE: "content_type",
        },
        required_params=["projectId", "spaceId", "documentName"],
    )
    def create_document(self, project_id: str, space_id: str, document_name: str, content_type: str, payload: str | bytes) -> Response:
        """Create module

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}"
        headers: dict[str, str] = {
            Header.CONTENT_TYPE: content_type,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, payload=payload)

    @restapi_endpoint(
        method="DELETE",
        path="/api/projects/{projectId}/spaces/{spaceId}/documents/{documentName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        required_params=["projectId", "spaceId", "documentName"],
    )
    def delete_document(self, project_id: str, space_id: str, document_name: str) -> Response:
        """Delete module

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}"
        return self.polarion_connection.api_request_delete(url)
