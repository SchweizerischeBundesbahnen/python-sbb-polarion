"""Diff Tool conversion mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.extensions._shared_exporter_types import Orientation, PaperSize
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response


class ConversionMixin(BaseMixin):
    """Conversion operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/conversion/html-to-pdf",
        query_params={
            "orientation": "orientation",
            "paperSize": "paper_size",
        },
        body_param="html",
    )
    def convert_html_to_pdf(
        self,
        html: str,
        orientation: Orientation = Orientation.LANDSCAPE,
        paper_size: PaperSize = PaperSize.A4,
    ) -> Response:
        """POST Returns requested HTML converted to PDF

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/conversion/html-to-pdf"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.ANY,
            Header.CONTENT_TYPE: MediaType.HTML,
        }
        params: dict[str, str] = {
            "orientation": orientation,
            "paperSize": paper_size,
        }
        return self.polarion_connection.api_request_post(url, data=html, headers=headers, params=params)
