"""Excel Importer import operations mixin."""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict


class ImportMixin(BaseMixin):
    """Import operations."""

    if TYPE_CHECKING:
        extension_name: str

    @restapi_endpoint(
        method="GET",
        path="/api/import/jobs",
        required_params=[],
        response_type="json",
    )
    def get_all_import_jobs(self) -> Response:
        """Get all importer jobs

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/import/jobs"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/import/jobs",
        multipart_fields={
            "file": "excel_file_path",
            "mappingName": "mapping_name",
            "projectId": "project_id",
        },
        helper_params=["excel_file_path"],
        required_params=[],
        response_type="json",
    )
    def start_import_job(self, project_id: str, excel_file_path: str, mapping_name: str = "Default") -> Response:
        """Start asynchronous import job

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/import/jobs"

        with pathlib.Path(excel_file_path).open("rb") as excel_content:
            files: FilesDict = {
                "file": (pathlib.Path(excel_file_path).name, excel_content),
                "mappingName": mapping_name,
                "projectId": project_id,
            }

            headers: dict[str, str] = {
                Header.ACCEPT: MediaType.JSON,
            }
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    @restapi_endpoint(
        method="GET",
        path="/api/import/jobs/{id}",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        response_type="json",
    )
    def get_import_job_status(self, job_id: str) -> Response:
        """Get import job status

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/import/jobs/{job_id}"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/import/jobs/{id}/result",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        response_type="json",
    )
    def get_import_job_result(self, job_id: str) -> Response:
        """Get import job result

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/import/jobs/{job_id}/result"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/import",
        path_params={
            "projectId": "project_id",
        },
        multipart_fields={
            "file": "excel_file_path",
            "mappingName": "mapping_name",
        },
        helper_params=["excel_file_path"],
        required_params=["projectId"],
        response_type="json",
    )
    def import_excel_sheet(self, project_id: str, excel_file_path: str, mapping_name: str = "Default") -> Response:
        """Import Excel sheet

        Returns:
            Response: Response object from the API call
        """
        url: str = f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/import"

        with pathlib.Path(excel_file_path).open("rb") as excel_content:
            files: FilesDict = {
                "file": (pathlib.Path(excel_file_path).name, excel_content),
                "mappingName": mapping_name,
            }

            headers: dict[str, str] = {
                Header.ACCEPT: MediaType.JSON,
            }
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)
