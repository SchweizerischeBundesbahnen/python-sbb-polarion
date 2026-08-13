"""Disclaimer mixin for extensions that expose /api/disclaimer.

Six extensions have this endpoint and the rest do not, so it is a separate
mixin for the same reason RolesMixin is one.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base._mixin import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class DisclaimerMixin(BaseMixin):
    """Read the disclaimer an extension shows in its UI."""

    @restapi_endpoint(
        method="GET",
        path="/api/disclaimer",
        response_type="json",
    )
    def get_disclaimer(self) -> Response:
        """Get the disclaimer.

        Returns:
            Response: Disclaimer from API
        """
        url: str = f"{self.rest_api_url}/disclaimer"
        return self.polarion_connection.api_request_get(url)
