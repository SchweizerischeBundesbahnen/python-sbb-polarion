"""Revisions operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import SparseFields


class RevisionsMixin(BaseMixin):
    """Revisions operations.

    Provides methods for accessing repository revisions.
    """

    @restapi_endpoint(
        method="GET",
        path="/revisions",
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
        },
        required_params=[],
        response_type="json",
    )
    def get_revisions(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
    ) -> Response:
        """Get list of revisions.

        Args:
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query string
            sort: Sort specification

        Returns:
            Response: List of revisions from API
        """
        url: str = f"{self.base_url}/revisions"
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
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/revisions/{repositoryName}/{revision}",
        path_params={
            "repositoryName": "repository_name",
            "revision": "revision",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["repositoryName", "revision"],
        response_type="json",
    )
    def get_revision(
        self,
        repository_name: str,
        revision: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get a specific revision.

        Args:
            repository_name: Repository name
            revision: Revision identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: Revision data from API
        """
        url: str = f"{self.base_url}/revisions/{repository_name}/{revision}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)
