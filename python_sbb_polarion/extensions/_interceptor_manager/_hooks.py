"""Interceptor Manager hooks mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class HooksMixin(BaseMixin):
    """Hooks operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/hooks",
        query_params={
            "reload": "reload",
        },
        required_params=[],
        response_type="json",
    )
    def get_hooks(self, reload: bool = False) -> Response:
        """GET hooks list

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/hooks"
        params: dict[str, str] = {
            "reload": str(reload).lower(),
        }
        return self.polarion_connection.api_request_get(url, params=params)
