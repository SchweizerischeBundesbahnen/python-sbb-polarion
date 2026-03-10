"""Admin Utility vault management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class VaultMixin(BaseMixin):
    """Vault management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/vault",
        body_param="data",
        helper_params=["key", "user", "password"],
        required_params=["__request_body__"],
    )
    def create_vault_record(self, key: str, user: str, password: str) -> Response:
        """Create Vault record

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/vault"
        data: JsonDict = {
            "key": key,
            "user": user,
            "password": password,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/vault/{key}",
        path_params={
            "key": "vault_key",
        },
        required_params=["key"],
        response_type="json",
    )
    def get_vault_record(self, key: str) -> Response:
        """Get Vault record

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/vault/{key}"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="DELETE",
        path="/api/vault/{key}",
        path_params={
            "key": "vault_key",
        },
        required_params=["key"],
    )
    def delete_vault_record(self, key: str) -> Response:
        """Delete Vault record

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/vault/{key}"
        return self.polarion_connection.api_request_delete(url)
