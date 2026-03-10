"""Documents parts operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class DocumentsPartsMixin(BaseMixin):
    """Documents parts operations.

    Provides methods for managing document parts.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/parts",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def get_document_parts(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of document parts.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of document parts from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/parts"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/parts/{partId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "partId": "part_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName", "partId"],
        response_type="json",
    )
    def get_document_part(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        part_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific document part.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            part_id: Part identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Document part data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/parts/{part_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/parts",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def create_document_parts(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        data: JsonDict,
    ) -> Response:
        """Create document parts.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            data: Document parts data in JSON:API format

        Returns:
            Response: Created document parts data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/parts"
        return self.polarion_connection.api_request_post(url, data=data)

    # New endpoints in Polarion 2512

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/parts/{partId}/actions/move",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
            "partId": "part_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName", "partId"],
        response_type="json",
    )
    def move_document_parts(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        part_id: str,
        data: JsonDict,
    ) -> Response:
        """Move document parts.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            part_id: Part identifier
            data: Move operation data in JSON:API format

        Returns:
            Response: Move operation result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/parts/{part_id}/actions/move"
        return self.polarion_connection.api_request_post(url, data=data)
