"""License management operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class LicenseMixin(BaseMixin):
    """License management operations.

    Provides methods for managing Polarion licenses, slots, and assignments.
    New in Polarion 2512.
    """

    @restapi_endpoint(
        method="GET",
        path="/license",
        query_params={
            "fields": "fields",
            "include": "include",
        },
        response_type="json",
    )
    def get_license(
        self,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get license information.

        Args:
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: License data from API
        """
        url: str = f"{self.base_url}/license"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/license",
        body_param="data",
        response_type="json",
    )
    def update_license(
        self,
        data: JsonDict,
    ) -> Response:
        """Update license information.

        Args:
            data: License data in JSON:API format

        Returns:
            Response: Updated license data from API
        """
        url: str = f"{self.base_url}/license"
        return self.polarion_connection.api_request_patch(url, data=data)

    # License Slots

    @restapi_endpoint(
        method="GET",
        path="/license/types/{typeId}/slots",
        path_params={"typeId": "type_id"},
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["typeId"],
        response_type="json",
    )
    def get_license_slots(
        self,
        type_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get license slots for a license type.

        Args:
            type_id: License type identifier
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: List of license slots from API
        """
        url: str = f"{self.base_url}/license/types/{type_id}/slots"
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
        path="/license/types/{typeId}/slots/{model}/{group}",
        path_params={
            "typeId": "type_id",
            "model": "model",
            "group": "group",
        },
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["typeId", "model", "group"],
        response_type="json",
    )
    def get_license_slot(
        self,
        type_id: str,
        model: str,
        group: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get a specific license slot.

        Args:
            type_id: License type identifier
            model: License model
            group: License group
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: License slot data from API
        """
        url: str = f"{self.base_url}/license/types/{type_id}/slots/{model}/{group}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/license/types/{typeId}/slots",
        path_params={"typeId": "type_id"},
        body_param="data",
        required_params=["typeId"],
        response_type="json",
    )
    def create_license_slots(
        self,
        type_id: str,
        data: JsonDict,
    ) -> Response:
        """Create license slots.

        Args:
            type_id: License type identifier
            data: License slots data in JSON:API format

        Returns:
            Response: Created license slots data from API
        """
        url: str = f"{self.base_url}/license/types/{type_id}/slots"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/license/types/{typeId}/slots",
        path_params={"typeId": "type_id"},
        body_param="data",
        required_params=["typeId", "__request_body__"],
        response_type="json",
    )
    def delete_license_slots(
        self,
        type_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete license slots.

        Args:
            type_id: License type identifier
            data: License slots data to delete in JSON:API format

        Returns:
            Response: Deletion result from API
        """
        url: str = f"{self.base_url}/license/types/{type_id}/slots"
        return self.polarion_connection.api_request_delete(url, data=data)

    # License Assignments

    @restapi_endpoint(
        method="GET",
        path="/license/assignments",
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "activeOnly": "active_only",
        },
        response_type="json",
    )
    def get_license_assignments(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        active_only: bool | None = None,
    ) -> Response:
        """Get all license assignments.

        Args:
            page_size: Number of items per page
            page_number: Page number (1-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            active_only: Filter to active assignments only

        Returns:
            Response: List of license assignments from API
        """
        url: str = f"{self.base_url}/license/assignments"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if active_only is not None:
            params["activeOnly"] = str(active_only).lower()
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/license/assignments/{userId}",
        path_params={"userId": "user_id"},
        query_params={
            "fields": "fields",
            "include": "include",
        },
        required_params=["userId"],
        response_type="json",
    )
    def get_license_assignments_for_user(
        self,
        user_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
    ) -> Response:
        """Get license assignments for a specific user.

        Args:
            user_id: User identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources

        Returns:
            Response: User's license assignments from API
        """
        url: str = f"{self.base_url}/license/assignments/{user_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="PATCH",
        path="/license/assignments",
        body_param="data",
        response_type="json",
    )
    def update_license_assignments(
        self,
        data: JsonDict,
    ) -> Response:
        """Update license assignments.

        Args:
            data: License assignments data in JSON:API format

        Returns:
            Response: Updated assignments data from API
        """
        url: str = f"{self.base_url}/license/assignments"
        return self.polarion_connection.api_request_patch(url, data=data)
