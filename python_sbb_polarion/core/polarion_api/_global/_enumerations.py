"""Global enumerations operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, SparseFields


class GlobalEnumerationsMixin(BaseMixin):
    """Global enumerations operations.

    Provides methods for managing global-level enumerations and icons.
    """

    @restapi_endpoint(
        method="GET",
        path="/enumerations/{enumContext}/{enumName}/{targetType}",
        path_params={
            "enumContext": "enum_context",
            "enumName": "enum_name",
            "targetType": "target_type",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["enumContext", "enumName", "targetType"],
        response_type="json",
    )
    def get_global_enumeration(
        self,
        enum_context: str,
        enum_name: str,
        target_type: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get a specific global enumeration.

        Args:
            enum_context: Enumeration context
            enum_name: Enumeration name
            target_type: Target type
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: Enumeration data from API
        """
        url: str = f"{self.base_url}/enumerations/{enum_context}/{enum_name}/{target_type}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/enumerations",
        body_param="data",
        required_params=[],
        response_type="json",
    )
    def create_global_enumeration(self, data: JsonDict) -> Response:
        """Create global enumerations.

        Args:
            data: Enumerations data in JSON:API format

        Returns:
            Response: Created enumerations data from API
        """
        url: str = f"{self.base_url}/enumerations"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/enumerations/{enumContext}/{enumName}/{targetType}",
        path_params={
            "enumContext": "enum_context",
            "enumName": "enum_name",
            "targetType": "target_type",
        },
        body_param="data",
        required_params=["enumContext", "enumName", "targetType"],
        response_type="json",
    )
    def update_global_enumeration(
        self,
        enum_context: str,
        enum_name: str,
        target_type: str,
        data: JsonDict,
    ) -> Response:
        """Update a global enumeration.

        Args:
            enum_context: Enumeration context
            enum_name: Enumeration name
            target_type: Target type
            data: Enumeration data in JSON:API format

        Returns:
            Response: Updated enumeration data from API
        """
        url: str = f"{self.base_url}/enumerations/{enum_context}/{enum_name}/{target_type}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/enumerations/{enumContext}/{enumName}/{targetType}",
        path_params={
            "enumContext": "enum_context",
            "enumName": "enum_name",
            "targetType": "target_type",
        },
        required_params=["enumContext", "enumName", "targetType"],
        response_type="json",
    )
    def delete_global_enumeration(
        self,
        enum_context: str,
        enum_name: str,
        target_type: str,
    ) -> Response:
        """Delete a global enumeration.

        Args:
            enum_context: Enumeration context
            enum_name: Enumeration name
            target_type: Target type

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/enumerations/{enum_context}/{enum_name}/{target_type}"
        return self.polarion_connection.api_request_delete(url)

    # Global Icons

    @restapi_endpoint(
        method="GET",
        path="/enumerations/icons",
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
        },
        required_params=[],
        response_type="json",
        naming_ok=True,
    )
    def get_global_icons(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get list of global icons.

        Args:
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: List of icons from API
        """
        url: str = f"{self.base_url}/enumerations/icons"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/enumerations/icons/{iconId}",
        path_params={
            "iconId": "icon_id",
        },
        query_params={
            "fields": "fields",
        },
        required_params=["iconId"],
        response_type="json",
    )
    def get_global_icon(
        self,
        icon_id: str,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get a specific global icon.

        Args:
            icon_id: Icon identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: Icon data from API
        """
        url: str = f"{self.base_url}/enumerations/icons/{icon_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/enumerations/icons",
        multipart_fields={
            "resource": "files['resource']",
            "files": "files['files']",
        },
        required_params=[],
        response_type="json",
    )
    def create_global_icons(self, files: FilesDict) -> Response:
        """Create global icons.

        Args:
            files: Files dict with icon data

        Returns:
            Response: Created icons data from API
        """
        url: str = f"{self.base_url}/enumerations/icons"
        return self.polarion_connection.api_request_post(url, files=files)

    # Default Icons

    @restapi_endpoint(
        method="GET",
        path="/enumerations/defaulticons",
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
        },
        required_params=[],
        response_type="json",
        naming_ok=True,
    )
    def get_default_icons(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get list of default icons.

        Args:
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: List of default icons from API
        """
        url: str = f"{self.base_url}/enumerations/defaulticons"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/enumerations/defaulticons/{iconId}",
        path_params={
            "iconId": "icon_id",
        },
        query_params={
            "fields": "fields",
        },
        required_params=["iconId"],
        response_type="json",
    )
    def get_default_icon(
        self,
        icon_id: str,
        fields: SparseFields | None = None,
    ) -> Response:
        """Get a specific default icon.

        Args:
            icon_id: Icon identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})

        Returns:
            Response: Default icon data from API
        """
        url: str = f"{self.base_url}/enumerations/defaulticons/{icon_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        return self.polarion_connection.api_request_get(url, params=params or None)
