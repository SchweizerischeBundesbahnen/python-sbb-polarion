"""Documents CRUD operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class DocumentsCrudMixin(BaseMixin):
    """Documents CRUD operations.

    Provides methods for creating, reading, and updating documents.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def get_document(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a document.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Document data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId"],
        response_type="json",
    )
    def create_documents(
        self,
        project_id: str,
        space_id: str,
        data: JsonDict,
    ) -> Response:
        """Create documents.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            data: Documents data in JSON:API format

        Returns:
            Response: Created documents data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "workflowAction": "workflow_action",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def update_document(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        data: JsonDict,
        workflow_action: str | None = None,
    ) -> Response:
        """Update a document.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            data: Document data in JSON:API format
            workflow_action: Workflow action to execute

        Returns:
            Response: Updated document data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}"
        params: dict[str, str] = {}
        if workflow_action:
            params["workflowAction"] = workflow_action
        return self.polarion_connection.api_request_patch(url, data=data, params=params or None)

    # New endpoints in Polarion 2512

    @restapi_endpoint(
        method="GET",
        path="/all/documents",
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        response_type="json",
    )
    def get_all_documents(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get all documents across all projects.

        Args:
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter documents
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of documents from API
        """
        url: str = f"{self.base_url}/all/documents"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if query:
            params["query"] = query
        if sort:
            params["sort"] = sort
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/documents",
        path_params={"projectId": "project_id"},
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_project_documents(
        self,
        project_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get all documents in a project.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter documents
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of documents from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/documents"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if query:
            params["query"] = query
        if sort:
            params["sort"] = sort
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/documents",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
        },
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
        },
        required_params=["projectId", "spaceId"],
        response_type="json",
    )
    def get_space_documents(
        self,
        project_id: str,
        space_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
    ) -> Response:
        """Get all documents in a project space.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter documents
            sort: Sort specification

        Returns:
            Response: List of documents from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents"
        params: dict[str, str] = {}
        if page_size is not None:
            params["page[size]"] = str(page_size)
        if page_number is not None:
            params["page[number]"] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if query:
            params["query"] = query
        if sort:
            params["sort"] = sort
        return self.polarion_connection.api_request_get(url, params=params or None)
