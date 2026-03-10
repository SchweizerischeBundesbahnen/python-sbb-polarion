"""Collection Checker collections mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class CollectionsMixin(BaseMixin):
    """Collections operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/collections",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_collections(self, project_id: str) -> Response:
        """Get all collections within the project

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/collections"
        return self.polarion_connection.api_request_get(url)
