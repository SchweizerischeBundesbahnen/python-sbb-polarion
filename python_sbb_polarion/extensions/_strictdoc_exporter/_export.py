"""StrictDoc Exporter export mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class ExportMixin(BaseMixin):
    """Export operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/export/livedoc",
        body_param="export_params",
        response_type="binary",
    )
    def export_live_doc(self, export_params: JsonDict) -> Response:
        """Export Polarion live documents to StrictDoc format.

        Args:
            export_params: Export parameters containing projectId, locations
                (list of {spaceId, moduleName, revision?, baselineRevision?}), format, fileName, renderComments

        Returns:
            Response: Response object with a zip archive holding the exported documents
        """
        url: str = f"{self.rest_api_url}/export/livedoc"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.OCTET_STREAM,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=export_params)

    @restapi_endpoint(
        method="POST",
        path="/api/export-github/livedoc",
        body_param="export_params",
        response_type="binary",
    )
    def export_github_livedoc(self, export_params: JsonDict) -> Response:
        """Export Polarion live documents to StrictDoc format and upload them to GitHub.

        Args:
            export_params: Export parameters containing projectId, locations
                (list of {spaceId, moduleName, revision?, baselineRevision?}), folderName, owner, repo, commitMessage

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/export-github/livedoc"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.OCTET_STREAM,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=export_params)

    @restapi_endpoint(
        method="POST",
        path="/api/widgets/bulk-export/items",
        body_param="request_params",
        required_params=["__request_body__"],
        response_type="json",
    )
    def find_widgets_bulk_export_items(self, request_params: JsonDict) -> Response:
        """Get the rows of a bulk export widget.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/widgets/bulk-export/items"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.JSON,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, data=request_params, headers=headers)
