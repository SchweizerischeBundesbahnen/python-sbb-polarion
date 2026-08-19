"""Export permission mixin for the exporter extensions.

Only the exporters expose /api/permissions/export, so this is a separate mixin
for the same reason RolesMixin is one.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base._mixin import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class ExportPermissionMixin(BaseMixin):
    """Ask whether the current user may export."""

    @restapi_endpoint(
        method="GET",
        path="/api/permissions/export",
        query_params={
            "projectId": "project_id",
        },
        response_type="json",
    )
    def get_export_permission(self, project_id: str | None = None) -> Response:
        """Get the export permission, optionally for a single project.

        Returns:
            Response: Export permission from API
        """
        url: str = f"{self.rest_api_url}/permissions/export"
        params: dict[str, str] = {}
        if project_id:
            params["projectId"] = project_id
        return self.polarion_connection.api_request_get(url, params=params or None)
