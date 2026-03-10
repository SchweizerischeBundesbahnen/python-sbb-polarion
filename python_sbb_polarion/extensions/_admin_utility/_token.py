"""Admin Utility token management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TokenMixin(BaseMixin):
    """Token management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/tokens",
        body_param="data",
        helper_params=["name", "expires_on"],
        required_params=["__request_body__"],
    )
    def create_token(self, name: str, expires_on: str) -> Response:
        """Create access token

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/tokens"
        data: JsonDict = {
            "name": name,
            "expiresOn": expires_on,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/api/tokens",
    )
    def delete_all_tokens(self) -> Response:
        """Delete all tokens

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/tokens"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="DELETE",
        path="/api/tokens/{tokenId}",
        path_params={
            "tokenId": "token_id",
        },
        required_params=["tokenId"],
    )
    def delete_token(self, token_id: str) -> Response:
        """Delete token

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/tokens/{token_id}"
        return self.polarion_connection.api_request_delete(url)
