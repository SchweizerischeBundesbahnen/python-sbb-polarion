"""Pages (Wiki) CRUD operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class PagesMixin(BaseMixin):
    """Pages (Wiki) operations.

    Provides methods for managing wiki pages and their attachments.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "pageName"],
        response_type="json",
    )
    def get_page(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a wiki page.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Page data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "pageName"],
        response_type="json",
    )
    def update_page(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        data: JsonDict,
    ) -> Response:
        """Update a wiki page.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            data: Page data in JSON:API format

        Returns:
            Response: Updated page data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}"
        return self.polarion_connection.api_request_patch(url, data=data)

    # Page Attachments

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "attachmentId": "attachment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "pageName", "attachmentId"],
        response_type="json",
    )
    def get_page_attachment(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        attachment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific page attachment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            attachment_id: Attachment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Attachment metadata from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments/{attachment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/attachments/{attachmentId}/content",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "attachmentId": "attachment_id",
        },
        query_params={
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "pageName", "attachmentId"],
        response_type="binary",
    )
    def get_page_attachment_content(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        attachment_id: str,
        revision: str | None = None,
    ) -> Response:
        """Download page attachment content.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            attachment_id: Attachment identifier
            revision: Specific revision

        Returns:
            Response: Binary attachment content
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments/{attachment_id}/content"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/attachments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
        },
        multipart_fields={
            "resource": "files['resource']",
            "files": "files['files']",
        },
        required_params=["projectId", "spaceId", "pageName"],
        response_type="json",
    )
    def create_page_attachments(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        files: FilesDict,
    ) -> Response:
        """Create page attachments.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            files: Files dict with 'resource' (JSON metadata) and 'files' (file content)

        Returns:
            Response: Created attachments data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments"
        return self.polarion_connection.api_request_post(url, files=files)

    # New endpoints in Polarion 2512

    @restapi_endpoint(
        method="GET",
        path="/all/pages",
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        response_type="json",
    )
    def get_all_pages(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get all pages across all projects.

        Args:
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter pages
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of pages from API
        """
        url: str = f"{self.base_url}/all/pages"
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
        path="/pages",
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
        },
        response_type="json",
    )
    def get_global_pages(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
    ) -> Response:
        """Get global (repository-level) pages.

        Args:
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter pages
            sort: Sort specification

        Returns:
            Response: List of global pages from API
        """
        url: str = f"{self.base_url}/pages"
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
        path="/spaces/{spaceId}/pages",
        path_params={"spaceId": "space_id"},
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        required_params=["spaceId"],
        response_type="json",
    )
    def get_repository_space_pages(
        self,
        space_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get pages in a repository-level space.

        Args:
            space_id: Space identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter pages
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of pages from API
        """
        url: str = f"{self.base_url}/spaces/{space_id}/pages"
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
        path="/projects/{projectId}/pages",
        path_params={"projectId": "project_id"},
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
    def get_project_pages(
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
        """Get all pages in a project.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter pages
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of pages from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/pages"
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
        path="/projects/{projectId}/spaces/{spaceId}/pages",
        path_params={"projectId": "project_id", "spaceId": "space_id"},
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
        },
        required_params=["projectId", "spaceId"],
        response_type="json",
    )
    def get_space_pages(
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
        """Get pages in a project space.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query to filter pages
            sort: Sort specification

        Returns:
            Response: List of pages from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages"
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
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/pages",
        path_params={"projectId": "project_id", "spaceId": "space_id"},
        body_param="data",
        required_params=["projectId", "spaceId"],
        response_type="json",
    )
    def create_page(
        self,
        project_id: str,
        space_id: str,
        data: JsonDict,
    ) -> Response:
        """Create a new wiki page.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            data: Page data in JSON:API format

        Returns:
            Response: Created page data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
        },
        required_params=["projectId", "spaceId", "pageName"],
        response_type="json",
    )
    def delete_page(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
    ) -> Response:
        """Delete a wiki page.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name

        Returns:
            Response: Deletion result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}"
        return self.polarion_connection.api_request_delete(url)

    # Page Attachments - additional methods

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/attachments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "pageName"],
        response_type="json",
    )
    def get_page_attachments(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get all attachments for a page.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of attachments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments"
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
        method="PATCH",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "attachmentId": "attachment_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "pageName", "attachmentId"],
        response_type="json",
    )
    def update_page_attachment(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        attachment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update a page attachment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            attachment_id: Attachment identifier
            data: Attachment data in JSON:API format

        Returns:
            Response: Updated attachment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/attachments/{attachmentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "attachmentId": "attachment_id",
        },
        required_params=["projectId", "spaceId", "pageName", "attachmentId"],
        response_type="json",
    )
    def delete_page_attachment(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        attachment_id: str,
    ) -> Response:
        """Delete a page attachment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            attachment_id: Attachment identifier

        Returns:
            Response: Deletion result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_delete(url)

    # Page Comments

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/comments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "pageName"],
        response_type="json",
    )
    def get_page_comments(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get all comments for a page.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of comments from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/comments"
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
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "commentId": "comment_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "pageName", "commentId"],
        response_type="json",
    )
    def get_page_comment(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        comment_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific page comment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            comment_id: Comment identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/comments/{comment_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/comments",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "pageName"],
        response_type="json",
    )
    def create_page_comment(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        data: JsonDict,
    ) -> Response:
        """Create a comment on a page.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            data: Comment data in JSON:API format

        Returns:
            Response: Created comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/comments"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/comments/{commentId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "commentId": "comment_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "pageName", "commentId"],
        response_type="json",
    )
    def update_page_comment(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        comment_id: str,
        data: JsonDict,
    ) -> Response:
        """Update a page comment.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            comment_id: Comment identifier
            data: Comment data in JSON:API format

        Returns:
            Response: Updated comment data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/comments/{comment_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    # Page Relationships

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "relationshipId": "relationship_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "spaceId", "pageName", "relationshipId"],
        response_type="json",
    )
    def get_page_relationships(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        relationship_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get page relationships.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            relationship_id: Relationship type identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Relationship data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/relationships/{relationship_id}"
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
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "pageName", "relationshipId"],
        response_type="json",
    )
    def create_page_relationships(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Create page relationships.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            relationship_id: Relationship type identifier
            data: Relationship data in JSON:API format

        Returns:
            Response: Created relationship data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "pageName", "relationshipId"],
        response_type="json",
    )
    def update_page_relationships(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Update page relationships.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            relationship_id: Relationship type identifier
            data: Relationship data in JSON:API format

        Returns:
            Response: Updated relationship data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/spaces/{spaceId}/pages/{pageName}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "pageName": "page_name",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "pageName", "relationshipId", "__request_body__"],
        response_type="json",
    )
    def delete_page_relationships(
        self,
        project_id: str,
        space_id: str,
        page_name: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete page relationships.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            page_name: Page name
            relationship_id: Relationship type identifier
            data: Relationship data to delete in JSON:API format

        Returns:
            Response: Deletion result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/pages/{page_name}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_delete(url, data=data)
