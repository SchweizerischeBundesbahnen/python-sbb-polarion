"""API Extender records mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class RecordsMixin(BaseMixin):
    """Global records operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/records/{key}",
        path_params={
            "key": "key",
        },
        required_params=["key"],
        response_type="json",
    )
    def get_record(self, key: str) -> Response:
        """Get global record

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/records/{key}"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/records/{key}",
        path_params={
            "key": "key",
        },
        body_param="field_data",
        required_params=["key"],
        response_type="json",
    )
    def save_record(self, key: str, value: str) -> Response:
        """Save global record

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/records/{key}"
        data: JsonDict = {
            "value": value,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/api/records/{key}",
        path_params={
            "key": "key",
        },
        required_params=["key"],
        response_type="json",
    )
    def delete_record(self, key: str) -> Response:
        """Delete global record

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/records/{key}"
        return self.polarion_connection.api_request_delete(url)
