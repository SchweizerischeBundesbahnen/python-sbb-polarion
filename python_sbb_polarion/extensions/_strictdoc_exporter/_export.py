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
        """Export Polarion live document to StrictDoc format.

        Args:
            export_params: Export parameters containing projectId, location, format, fileName

        Returns:
            Response: Response object with exported document content
        """
        url: str = f"{self.rest_api_url}/export/livedoc"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.OCTET_STREAM,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=export_params)
