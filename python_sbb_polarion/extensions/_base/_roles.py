"""Roles mixin for extensions that expose /api/roles.

Not every extension has this endpoint, so it is a separate mixin rather than
part of PolarionGenericExtensionApi. Mixing it into an extension whose
OpenAPI spec has no /api/roles would leave an orphan annotation behind.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base._mixin import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class RolesMixin(BaseMixin):
    """Read the roles an extension knows about."""

    @restapi_endpoint(
        method="GET",
        path="/api/roles",
        query_params={
            "scope": "scope",
        },
        response_type="json",
    )
    def get_roles(self, scope: str | None = None) -> Response:
        """Get roles, optionally for a single scope.

        Returns:
            Response: Roles from API
        """
        url: str = f"{self.rest_api_url}/roles"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_get(url, params=params or None)
