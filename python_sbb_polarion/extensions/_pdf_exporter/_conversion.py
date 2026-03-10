"""PDF Conversion operations mixin.

This module provides methods for converting HTML and documents to PDF,
managing conversion jobs, and validating PDF output.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.extensions._pdf_exporter._types import PdfVariant
from python_sbb_polarion.extensions._shared_exporter_types import Orientation, PaperSize
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class ConversionMixin(BaseMixin):
    """PDF conversion operations (HTML, Jobs, Documents).

    This mixin provides methods for:
    - Converting HTML to PDF
    - Managing asynchronous PDF conversion jobs
    - Converting Polarion documents to PDF
    - Validating PDF output
    """

    # =========================================================================
    # PDF Conversion - HTML
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/convert/html",
        query_params={
            "orientation": "orientation",
            "paperSize": "paper_size",
            "pdfVariant": "pdf_variant",
            "fitToPage": "fit_to_page",
            "fileName": "filename",
        },
        body_param="html",
        required_params=[],
        response_type="binary",
    )
    def convert_html(
        self,
        html: str,
        orientation: Orientation = Orientation.PORTRAIT,
        paper_size: PaperSize = PaperSize.A4,
        pdf_variant: PdfVariant = PdfVariant.PDF_A_2B,
        filename: str = "html-to-pdf.pdf",
        fit_to_page: bool = False,
    ) -> Response:
        """POST Returns requested HTML converted to PDF

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/html"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.ANY,
            Header.CONTENT_TYPE: MediaType.HTML,
        }
        params: dict[str, str] = {
            "orientation": orientation,
            "paperSize": paper_size,
            "pdfVariant": pdf_variant,
            "fitToPage": str(fit_to_page).lower(),
            "fileName": filename,
        }
        return self.polarion_connection.api_request_post(url, payload=html, headers=headers, params=params)

    # =========================================================================
    # PDF Conversion - Jobs
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/convert/jobs",
        required_params=[],
        response_type="json",
    )
    def get_all_pdf_converter_jobs(self) -> Response:
        """Get all jobs

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/jobs"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/convert/jobs",
        body_param="export_params",
        required_params=["__request_body__"],
        response_type="json",
    )
    def start_pdf_conversion_job(self, export_params: JsonDict) -> Response:
        """POST Starts asynchronous conversion job of Polarion's document to PDF

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/jobs"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.JSON,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, data=export_params, headers=headers)

    @restapi_endpoint(
        method="GET",
        path="/api/convert/jobs/{id}/result",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        response_type="binary",
    )
    def get_pdf_converter_job_result(self, job_id: str) -> Response:
        """Get conversion result

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/jobs/{job_id}/result"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PDF,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_get(url, headers=headers)

    @restapi_endpoint(
        method="GET",
        path="/api/convert/jobs/{id}",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        response_type="json",
    )
    def get_pdf_converter_job_status(self, job_id: str) -> Response:
        """Get conversion job status

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/jobs/{job_id}"
        return self.polarion_connection.api_request_get(url, allow_redirects=False)

    # =========================================================================
    # PDF Conversion - Document
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/prepared-html-content",
        body_param="export_params",
        required_params=["__request_body__"],
        response_type="text",
    )
    def receive_prepared_html_content(self, export_params: JsonDict) -> Response:
        """POST Returns requested Polarion's document as HTML which can be used later for PDF generation

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/prepared-html-content"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.HTML,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, data=export_params, headers=headers)

    @restapi_endpoint(
        method="POST",
        path="/api/validate",
        query_params={
            "max-results": "max_results",
        },
        body_param="export_params",
        required_params=["max-results"],
        response_type="json",
    )
    def validate(self, export_params: JsonDict, max_results: int = 6) -> Response:
        """POST Validates if requested Polarion's document been converted to PDF doesn't contain pages which content exceeds page's width

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/validate"
        params: dict[str, str] = {
            "max-results": str(max_results),
        }
        return self.polarion_connection.api_request_post(url, data=export_params, params=params)

    @restapi_endpoint(
        method="POST",
        path="/api/convert",
        body_param="export_params",
        required_params=["__request_body__"],
        response_type="binary",
    )
    def convert(self, export_params: JsonDict) -> Response:
        """POST Returns requested Polarion's document converted to PDF

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.PDF,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, data=export_params, headers=headers)
