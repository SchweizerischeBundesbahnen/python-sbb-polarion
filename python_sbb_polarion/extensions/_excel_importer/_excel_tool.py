"""Excel Importer excel tool mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, JsonList


class AttachTableParams(NamedTuple):
    """Definition of parameters for attach_table API call."""

    object_type: str
    object_id: str
    html_table: str
    file_name: str
    file_title: str


class ExcelToolMixin(BaseMixin):
    """Excel tool operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/excel-tool/export-html-table",
        multipart_fields={
            "tableHtml": "html",
            "sheetName": "sheet_name",
        },
        required_params=[],
        response_type="json",
    )
    def export_html_table(self, html: str, sheet_name: str | None = None) -> Response:
        """Export html table as excel sheet

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/excel-tool/export-html-table"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.JSON,
        }
        files: FilesDict = {
            "tableHtml": html,
        }
        if sheet_name is not None:
            files = {
                **files,
                "sheetName": sheet_name,
            }
        return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    @restapi_endpoint(
        method="GET",
        path="/api/excel-tool/exports/{exportId}/wait",
        path_params={
            "exportId": "export_id",
        },
        query_params={
            "timeout": "timeout",
        },
        required_params=["exportId", "timeout"],
        response_type="binary",
    )
    def wait_for_export(self, export_id: str, timeout: int) -> Response:
        """Wait for export to complete and return result

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/excel-tool/exports/{export_id}/wait"
        params: dict[str, str] = {
            "timeout": str(timeout),
        }
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="POST",
        path="/api/excel-tool/html-table-from-list",
        body_param="source_list",
        required_params=["__request_body__"],
        response_type="html",
    )
    def create_html_table_from_list(self, source_list: JsonList) -> Response:
        """Create html table from list

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/excel-tool/html-table-from-list"
        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.HTML,
        }
        return self.polarion_connection.api_request_post(url, headers=headers, data=source_list)

    @restapi_endpoint(
        method="POST",
        path="/api/excel-tool/projects/{projectId}/attach-table",
        path_params={
            "projectId": "project_id",
        },
        body_param="params",
        required_params=["projectId", "__request_body__"],
        response_type="json",
    )
    def attach_table(self, project_id: str, attach_table_params: AttachTableParams) -> Response:
        """Attach table as an attachment

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/excel-tool/projects/{project_id}/attach-table"
        data: JsonDict = {
            "objectType": attach_table_params.object_type,
            "objectId": attach_table_params.object_id,
            "htmlTable": attach_table_params.html_table,
            "fileName": attach_table_params.file_name,
            "fileTitle": attach_table_params.file_title,
        }
        return self.polarion_connection.api_request_post(url, data=data)
