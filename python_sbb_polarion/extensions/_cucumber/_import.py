"""Cucumber import mixin."""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict


class ImportMixin(BaseMixin):
    """Import operations."""

    if TYPE_CHECKING:
        extension_name: str

    @restapi_endpoint(
        method="POST",
        path="/raven/1.0/import/execution/cucumber/multipart",
        multipart_fields={
            "info": "info_file_path",
            "result": "result_file_path",
        },
        response_type="json",
    )
    def import_cucumber_test_results_multipart(self, info_file_path: str, result_file_path: str) -> Response:
        """Import cucumber test results

        Returns:
            Response: Response object from the API call
        """
        url: str = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/cucumber/multipart"

        with pathlib.Path(info_file_path).open(encoding="utf-8") as info_content, pathlib.Path(result_file_path).open(encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files: FilesDict = {
                "info": ("cucumber-info.json", info_content, MediaType.JSON),
                "result": ("cucumber-result.json", result_content, MediaType.JSON),
            }

            headers: dict[str, str] = {
                Header.ACCEPT: MediaType.JSON,
            }
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    @restapi_endpoint(
        method="POST",
        path="/raven/1.0/import/execution/junit",
        query_params={
            "projectKey": "project_key",
            "testExecKey": "test_exec_key",
            "testPlanKey": "test_plan_key",
            "testEnvironments": "test_environments",
            "revision": "revision",
            "fixVersion": "fix_version",
        },
        multipart_fields={
            "file": "result_file_path",
        },
        response_type="json",
    )
    def import_junit_test_results(self, parameters: JsonDict, result_file_path: str) -> Response:
        """Import JUnit test results

        Returns:
            Response: Response object from the API call
        """
        url: str = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/junit"
        # Convert JsonDict to params - all values should be strings for query params
        params: dict[str, str] = {key: str(value) for key, value in parameters.items()}

        with pathlib.Path(result_file_path).open(encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files: FilesDict = {
                "file": ("result.json", result_content, MediaType.JSON),
            }

            headers: dict[str, str] = {
                Header.ACCEPT: MediaType.JSON,
            }
            return self.polarion_connection.api_request_post(url, headers=headers, files=files, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/raven/1.0/import/execution/junit/multipart",
        multipart_fields={
            "info": "info_file_path",
            "file": "result_file_path",
        },
        response_type="json",
    )
    def import_junit_test_results_multipart(self, info_file_path: str, result_file_path: str) -> Response:
        """Import JUnit test results

        Returns:
            Response: Response object from the API call
        """
        url: str = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/junit/multipart"

        with pathlib.Path(info_file_path).open(encoding="utf-8") as info_content, pathlib.Path(result_file_path).open(encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files: FilesDict = {
                "info": ("info.json", info_content, MediaType.JSON),
                "file": ("result.json", result_content, MediaType.JSON),
            }

            headers: dict[str, str] = {
                Header.ACCEPT: MediaType.JSON,
            }
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)
