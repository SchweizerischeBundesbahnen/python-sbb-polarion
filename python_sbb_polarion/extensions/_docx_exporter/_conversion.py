"""DOCX Exporter conversion operations mixin.

This module provides conversion methods for HTML, documents, and async jobs.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict


class ConversionMixin(BaseMixin):
    """DOCX conversion operations.

    This mixin provides methods for:
    - HTML to DOCX conversion
    - Asynchronous conversion jobs
    - Document conversion
    - Template retrieval
    """

    # =========================================================================
    # DOCX Conversion - HTML
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/convert/html",
        query_params={
            "fileName": "file_name",
        },
        multipart_fields={
            "html": "html",
            "template": "template",
        },
        helper_params=["options", "params"],
        required_params=[],
        response_type="binary",
    )
    def convert_html(self, html: str, template: bytes | None = None, options: JsonDict | None = None, params: JsonDict | None = None, file_name: str = "html-to-docx.docx") -> Response:
        """POST Returns requested HTML converted to DOCX

        Returns:
            Response: Response object from the API call
        """
        files: FilesDict = {
            "html": ("file.html", html),
        }
        if template:
            files = {
                **files,
                "template": ("template.docx", template),
            }
        if options:
            files = {
                **files,
                "options": ("options.json", json.dumps(options)),
            }
        if params:
            files = {
                **files,
                "params": ("params.json", json.dumps(params)),
            }

        url: str = f"{self.rest_api_url}/convert/html"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.ANY,
        }
        query_params: dict[str, str] = {
            "fileName": file_name,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, params=query_params, files=files)

    # =========================================================================
    # DOCX Conversion - Jobs
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/convert/jobs",
        response_type="json",
    )
    def get_all_docx_converter_jobs(self) -> Response:
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
    def start_docx_converter_job(self, export_params: JsonDict) -> Response:
        """POST Starts asynchronous conversion job of Polarion's document to DOCX

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/jobs"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.JSON,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=export_params)

    @restapi_endpoint(
        method="GET",
        path="/api/convert/jobs/{id}/result",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        response_type="binary",
    )
    def get_docx_converter_job_result(self, job_id: str) -> Response:
        """Get conversion result

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/jobs/{job_id}/result"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.DOCX,
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
    def get_docx_converter_job_status(self, job_id: str) -> Response:
        """Get conversion job status

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert/jobs/{job_id}"
        return self.polarion_connection.api_request_get(url, allow_redirects=False)

    # =========================================================================
    # DOCX Conversion - Document
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/prepared-html-content",
        body_param="export_params",
        required_params=["__request_body__"],
        response_type="text",
    )
    def receive_prepared_html_content(self, export_params: JsonDict) -> Response:
        """POST Returns requested Polarion's document as HTML which can be used later for DOCX generation

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/prepared-html-content"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.HTML,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=export_params)

    @restapi_endpoint(
        method="POST",
        path="/api/convert",
        body_param="export_params",
        required_params=["__request_body__"],
        response_type="binary",
    )
    def convert(self, export_params: JsonDict) -> Response:
        """POST Returns requested Polarion's document converted to DOCX

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/convert"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.DOCX,
            Header.CONTENT_TYPE: MediaType.JSON,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=export_params)

    # =========================================================================
    # Template
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/template",
        required_params=[],
        response_type="binary",
    )
    def get_template(self) -> Response:
        """GET Returns default DOCX template

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/template"
        return self.polarion_connection.api_request_get(url)
