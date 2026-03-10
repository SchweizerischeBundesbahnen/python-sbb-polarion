"""Users operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class UsersMixin(BaseMixin):
    """Users operations.

    Provides methods for managing users, avatars, and licenses.
    """

    @restapi_endpoint(
        method="GET",
        path="/users",
        query_params={
            "page[size]": "page_size",
            "page[number]": "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
        },
        required_params=[],
        response_type="json",
    )
    def get_users(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get list of users.

        Args:
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query string
            sort: Sort specification
            revision: Specific revision

        Returns:
            Response: List of users from API
        """
        url: str = f"{self.base_url}/users"
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
        path="/users/{userId}",
        path_params={
            "userId": "user_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["userId"],
        response_type="json",
    )
    def get_user(
        self,
        user_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific user.

        Args:
            user_id: User identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: User data from API
        """
        url: str = f"{self.base_url}/users/{user_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/users",
        body_param="data",
        required_params=[],
        response_type="json",
    )
    def create_users(self, data: JsonDict) -> Response:
        """Create users.

        Args:
            data: Users data in JSON:API format

        Returns:
            Response: Created users data from API
        """
        url: str = f"{self.base_url}/users"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/users/{userId}",
        path_params={
            "userId": "user_id",
        },
        body_param="data",
        required_params=["userId"],
        response_type="json",
    )
    def update_user(self, user_id: str, data: JsonDict) -> Response:
        """Update a user.

        Args:
            user_id: User identifier
            data: User data in JSON:API format

        Returns:
            Response: Updated user data from API
        """
        url: str = f"{self.base_url}/users/{user_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/users/{userId}/actions/getAvatar",
        path_params={
            "userId": "user_id",
        },
        required_params=["userId"],
        response_type="binary",
    )
    def get_user_avatar(self, user_id: str) -> Response:
        """Get user avatar.

        Args:
            user_id: User identifier

        Returns:
            Response: Avatar image data
        """
        url: str = f"{self.base_url}/users/{user_id}/actions/getAvatar"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/users/{userId}/actions/updateAvatar",
        path_params={
            "userId": "user_id",
        },
        multipart_fields={
            "avatar": "files['avatar']",
        },
        required_params=["userId"],
        response_type="json",
    )
    def update_user_avatar(self, user_id: str, files: FilesDict) -> Response:
        """Update user avatar.

        Args:
            user_id: User identifier
            files: Files dict with avatar image

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/users/{user_id}/actions/updateAvatar"
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="POST",
        path="/users/{userId}/actions/setLicense",
        path_params={
            "userId": "user_id",
        },
        body_param="data",
        required_params=["userId"],
        response_type="json",
    )
    def set_user_license(self, user_id: str, data: JsonDict) -> Response:
        """Set user license.

        Args:
            user_id: User identifier
            data: License data

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/users/{user_id}/actions/setLicense"
        return self.polarion_connection.api_request_post(url, data=data)

    # New endpoints in Polarion 2512

    @restapi_endpoint(
        method="GET",
        path="/user",
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        response_type="json",
    )
    def get_current_user(
        self,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get the current authenticated user.

        Args:
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Current user data from API
        """
        url: str = f"{self.base_url}/user"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)
