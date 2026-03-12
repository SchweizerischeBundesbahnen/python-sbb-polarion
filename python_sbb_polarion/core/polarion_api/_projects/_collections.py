"""Projects collections operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class ProjectsCollectionsMixin(BaseMixin):
    """Projects collections operations.

    Provides methods for managing document collections and their relationships.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/collections",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_collections(
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
        """Get list of collections.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query string
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of collections from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
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
        path="/projects/{projectId}/collections/{collectionId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "collectionId"],
        response_type="json",
    )
    def get_collection(
        self,
        project_id: str,
        collection_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific collection.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Collection data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/collections",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def create_collections(self, project_id: str, data: JsonDict) -> Response:
        """Create collections.

        Args:
            project_id: Project identifier
            data: Collections data in JSON:API format

        Returns:
            Response: Created collections data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/collections/{collectionId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        body_param="data",
        required_params=["projectId", "collectionId"],
        response_type="json",
    )
    def update_collection(
        self,
        project_id: str,
        collection_id: str,
        data: JsonDict,
    ) -> Response:
        """Update a collection.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier
            data: Collection data in JSON:API format

        Returns:
            Response: Updated collection data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/collections",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def delete_collections(self, project_id: str, data: JsonDict) -> Response:
        """Delete collections.

        Args:
            project_id: Project identifier
            data: Collections to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/collections/{collectionId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        required_params=["projectId", "collectionId"],
        response_type="json",
    )
    def delete_collection(self, project_id: str, collection_id: str) -> Response:
        """Delete a specific collection.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/collections/{collectionId}/actions/close",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        required_params=["projectId", "collectionId"],
        response_type="json",
    )
    def close_collection(self, project_id: str, collection_id: str) -> Response:
        """Close a collection.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}/actions/close"
        return self.polarion_connection.api_request_post(url)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/collections/{collectionId}/actions/reopen",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        required_params=["projectId", "collectionId"],
        response_type="json",
    )
    def reopen_collection(self, project_id: str, collection_id: str) -> Response:
        """Reopen a collection.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}/actions/reopen"
        return self.polarion_connection.api_request_post(url)

    # Collection Relationships

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/collections/{collectionId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
            "relationshipId": "relationship_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "collectionId", "relationshipId"],
        response_type="json",
    )
    def get_collection_relationships(
        self,
        project_id: str,
        collection_id: str,
        relationship_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get collection relationships.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier
            relationship_id: Relationship identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/collections/{collectionId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "collectionId", "relationshipId"],
        response_type="json",
    )
    def create_collection_relationships(
        self,
        project_id: str,
        collection_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Create collection relationships.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier
            relationship_id: Relationship identifier
            data: Relationships data in JSON:API format

        Returns:
            Response: Created relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/collections/{collectionId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "collectionId", "relationshipId"],
        response_type="json",
    )
    def update_collection_relationships(
        self,
        project_id: str,
        collection_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Update collection relationships.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier
            relationship_id: Relationship identifier
            data: Relationships data in JSON:API format

        Returns:
            Response: Updated relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/collections/{collectionId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "collectionId", "relationshipId"],
        response_type="json",
    )
    def delete_collection_relationships(
        self,
        project_id: str,
        collection_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete collection relationships.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier
            relationship_id: Relationship identifier
            data: Relationships to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_delete(url, data=data)

    # New endpoints in Polarion 2512

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/collections/{collectionId}/actions/reuse",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        query_params={
            "revision": "revision",
        },
        body_param="data",
        required_params=["projectId", "collectionId"],
        response_type="json",
    )
    def reuse_collection(
        self,
        project_id: str,
        collection_id: str,
        data: JsonDict,
        revision: str | None = None,
    ) -> Response:
        """Reuse a collection.

        Args:
            project_id: Project identifier
            collection_id: Collection identifier
            data: Reuse operation data in JSON:API format
            revision: Specific revision

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/collections/{collection_id}/actions/reuse"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_post(url, data=data, params=params or None)
