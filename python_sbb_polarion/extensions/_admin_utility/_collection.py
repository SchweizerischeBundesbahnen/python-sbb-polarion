"""Admin Utility collection management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import deprecated_method, restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class CollectionMixin(BaseMixin):
    """Collection management operations."""

    @restapi_endpoint(
        method="DELETE",
        path="/api/projects/{projectId}/collections/{collectionId}",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        required_params=["projectId", "collectionId"],
    )
    @deprecated_method("PolarionApiV1.delete_collection")
    def delete_collection(self, project_id: str, collection_id: str) -> Response:
        """Delete collection

        .. deprecated::
            Use ``PolarionApiV1.delete_collection`` instead. The standard Polarion REST API v1
            covers collection deletion since Polarion 2606.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/collections/{collection_id}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/collections/{collectionId}/modules",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        body_param="data",
        helper_params=["module_id"],
        required_params=["projectId", "collectionId", "__request_body__"],
    )
    @deprecated_method("PolarionApiV1.create_collection_relationships")
    def add_to_collection(self, project_id: str, collection_id: str, module_id: str) -> Response:
        """Add an element to the collection

        .. deprecated::
            Use ``PolarionApiV1.create_collection_relationships`` (relationship ``documents``)
            instead. Express the module as a JSON:API id (``projectId/spaceId/documentName``).

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/collections/{collection_id}/modules"
        data: JsonDict = {
            "moduleId": module_id,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/collections",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        helper_params=["collection_name"],
        required_params=["projectId", "__request_body__"],
    )
    @deprecated_method("PolarionApiV1.create_collections")
    def create_collection(self, project_id: str, collection_name: str) -> Response:
        """Create collection

        .. deprecated::
            Use ``PolarionApiV1.create_collections`` instead. The standard Polarion REST API v1
            covers collection creation since Polarion 2606.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/collections"
        data: JsonDict = {
            "collectionName": collection_name,
        }
        return self.polarion_connection.api_request_post(url, data=data)
