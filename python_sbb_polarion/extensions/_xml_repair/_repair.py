"""XML Repair repair operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class RepairMixin(BaseMixin):
    """Repair operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/repairers",
        query_params={
            "entityType": "entity_type",
        },
        required_params=["entityType"],
    )
    def get_repairers(self, entity_type: str) -> Response:
        """Gets list of repairers for specified entity type

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] = {}
        if entity_type:
            params["entityType"] = entity_type
        url: str = f"{self.rest_api_url}/repairers"
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/api/repair",
        body_param="repair_params",
        naming_ok=True,
    )
    def repair(self, repair_params: JsonDict) -> Response:
        """Checks or repairs XML issues based on provided parameters

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/repair"
        return self.polarion_connection.api_request_post(url, data=repair_params)
