"""Documents fields operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class DocumentsFieldsMixin(BaseMixin):
    """Documents fields operations.

    Provides methods for getting document field options.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/fields/{fieldId}/actions/getAvailableOptions",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "fieldId": "field_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
        },
        required_params=["projectId", "spaceId", "documentName", "fieldId"],
        response_type="json",
    )
    def get_document_available_enum_options(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        field_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
    ) -> Response:
        """Get available enum options for a document field.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            field_id: Field identifier
            page_size: Number of items per page
            page_number: Page number (0-based)

        Returns:
            Response: List of available enum options from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/fields/{field_id}/actions/getAvailableOptions"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/fields/{fieldId}/actions/getCurrentOptions",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "fieldId": "field_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName", "fieldId"],
        response_type="json",
    )
    def get_document_current_enum_options(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        field_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get current enum options for a document field.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            field_id: Field identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            revision: Specific revision

        Returns:
            Response: List of current enum options from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/fields/{field_id}/actions/getCurrentOptions"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/documents/fields/{fieldId}/actions/getAvailableOptions",
        path_params={
            "projectId": "project_id",
            "fieldId": "field_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "type": "document_type",
        },
        required_params=["projectId", "fieldId"],
        response_type="json",
    )
    def get_documents_available_enum_options(
        self,
        project_id: str,
        field_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        document_type: str | None = None,
    ) -> Response:
        """Get available enum options for document type field.

        Args:
            project_id: Project identifier
            field_id: Field identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            document_type: Document type filter

        Returns:
            Response: List of available enum options from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/documents/fields/{field_id}/actions/getAvailableOptions"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        if document_type:
            params["type"] = document_type
        return self.polarion_connection.api_request_get(url, params=params or None)
