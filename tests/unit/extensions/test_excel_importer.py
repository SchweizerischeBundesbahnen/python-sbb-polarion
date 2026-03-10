"""Unit tests for Excel Importer API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock, mock_open, patch

from python_sbb_polarion.extensions.excel_importer import (
    AttachTableParams,
    PolarionExcelImporterApi,
)
from python_sbb_polarion.types import Header, MediaType


# Feature name for mappings settings (matches internal constant)
MAPPINGS_FEATURE = "mappings"


if TYPE_CHECKING:
    from typing import Any

    from requests import Response

    from python_sbb_polarion.types import JsonDict, JsonList


class TestAttachTableParams(unittest.TestCase):
    """Test AttachTableParams NamedTuple."""

    def test_attach_table_params_creation(self) -> None:
        """Test creating AttachTableParams."""
        params = AttachTableParams(
            object_type="WorkItem",
            object_id="WI-123",
            html_table="<table></table>",
            file_name="test.xlsx",
            file_title="Test File",
        )

        self.assertEqual(params.object_type, "WorkItem")
        self.assertEqual(params.object_id, "WI-123")
        self.assertEqual(params.html_table, "<table></table>")
        self.assertEqual(params.file_name, "test.xlsx")
        self.assertEqual(params.file_title, "Test File")


class TestPolarionExcelImporterApi(unittest.TestCase):
    """Test PolarionExcelImporterApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionExcelImporterApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "excel-importer")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Excel Tool
    # =========================================================================

    def test_export_html_table_with_sheet_name(self) -> None:
        """Test export html table with sheet name."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.export_html_table("<table></table>", sheet_name="Sheet1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/excel-tool/export-html-table"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON}

        self.mock_connection.api_request_post.assert_called_once_with(expected_url, headers=expected_headers, files={"tableHtml": "<table></table>", "sheetName": "Sheet1"})

    def test_export_html_table_without_sheet_name(self) -> None:
        """Test export html table without sheet name."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.export_html_table("<table></table>")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/excel-tool/export-html-table"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON}

        self.mock_connection.api_request_post.assert_called_once_with(expected_url, headers=expected_headers, files={"tableHtml": "<table></table>"})

    def test_html_table_from_list(self) -> None:
        """Test html table from list."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        source_list: JsonList = [{"col1": "val1", "col2": "val2"}]

        response: Response = self.api.create_html_table_from_list(source_list)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/excel-tool/html-table-from-list"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.HTML}, data=source_list)

    def test_attach_table(self) -> None:
        """Test attach table."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        params = AttachTableParams(
            object_type="WorkItem",
            object_id="WI-123",
            html_table="<table></table>",
            file_name="test.xlsx",
            file_title="Test File",
        )

        response: Response = self.api.attach_table("PROJ", params)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/excel-tool/projects/PROJ/attach-table"
        expected_data: JsonDict = {
            "objectType": "WorkItem",
            "objectId": "WI-123",
            "htmlTable": "<table></table>",
            "fileName": "test.xlsx",
            "fileTitle": "Test File",
        }
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=expected_data)

    # =========================================================================
    # Import
    # =========================================================================

    @patch("pathlib.Path.open", new_callable=mock_open, read_data=b"excel content")
    def test_import_excel_sheet_default_mapping(self, mock_file: Mock) -> None:
        """Test import excel sheet with default mapping."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.import_excel_sheet("PROJ", "/path/to/file.xlsx")

        self.assertEqual(response, mock_response)
        expected_url: str = "/polarion/excel-importer/rest/api/projects/PROJ/import"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON}

        # Verify the call was made with correct arguments
        self.mock_connection.api_request_post.assert_called_once()
        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertEqual(call_args[0][0], expected_url)
        self.assertEqual(call_args[1]["headers"], expected_headers)
        self.assertIn("files", call_args[1])

    @patch("pathlib.Path.open", new_callable=mock_open, read_data=b"excel content")
    def test_import_excel_sheet_custom_mapping(self, mock_file: Mock) -> None:
        """Test import excel sheet with custom mapping."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.import_excel_sheet("PROJ", "/path/to/file.xlsx", mapping_name="CustomMapping")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once()

    # =========================================================================
    # Workitem Types and Fields
    # =========================================================================

    def test_get_workitem_types(self) -> None:
        """Test get workitem types."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_workitem_types("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = "/polarion/excel-importer/rest/api/projects/PROJ/workitem_types"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_workitem_fields(self) -> None:
        """Test get workitem fields."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_workitem_fields("PROJ", "requirement")

        self.assertEqual(response, mock_response)
        expected_url: str = "/polarion/excel-importer/rest/api/projects/PROJ/workitem_types/requirement/fields"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    # =========================================================================
    # Mapping Settings
    # =========================================================================

    def test_get_mapping_default(self) -> None:
        """Test get mapping with default parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_mapping()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Default/content"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params=None)

    def test_get_mapping_with_scope(self) -> None:
        """Test get mapping with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_mapping(name="Custom", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Custom/content"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"scope": "project/elibrary/"})

    def test_save_mapping_default(self) -> None:
        """Test save mapping with default parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_mapping(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Default/content"
        self.mock_connection.api_request_put.assert_called_once_with(expected_url, data=data, params=None)

    def test_save_mapping_with_scope(self) -> None:
        """Test save mapping with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_mapping(data, name="Custom", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Custom/content"
        self.mock_connection.api_request_put.assert_called_once_with(expected_url, data=data, params={"scope": "project/elibrary/"})

    def test_delete_mapping_default(self) -> None:
        """Test delete mapping with default parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_mapping()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Default"
        self.mock_connection.api_request_delete.assert_called_once_with(expected_url, params=None)

    def test_delete_mapping_with_scope(self) -> None:
        """Test delete mapping with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_mapping(name="Custom", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Custom"
        self.mock_connection.api_request_delete.assert_called_once_with(expected_url, params={"scope": "project/elibrary/"})

    def test_get_default_mapping(self) -> None:
        """Test get default mapping."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_default_mapping()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/default-content"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_mapping_revisions_default(self) -> None:
        """Test get mapping revisions with default parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_mapping_revisions()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Default/revisions"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params=None)

    def test_get_mapping_revisions_with_scope(self) -> None:
        """Test get mapping revisions with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_mapping_revisions(name="Custom", scope="project/elibrary/")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/Custom/revisions"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"scope": "project/elibrary/"})

    # =========================================================================
    # Settings Mixin Methods (from PolarionGenericExtensionSettingsApi)
    # =========================================================================

    def test_get_features(self) -> None:
        """Test get_features method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_features()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings")

    def test_get_setting_names(self) -> None:
        """Test get_setting_names method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_names("feature1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names", params=None)

    def test_get_setting_content(self) -> None:
        """Test get_setting_content method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_content("feature1", name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/content", params={"scope": "project/test"})

    def test_save_setting(self) -> None:
        """Test save_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_setting("feature1", data, name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_put.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/content", data=data, params={"scope": "project/test"})

    def test_rename_setting(self) -> None:
        """Test rename_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.rename_setting("feature1", "OldName", "NewName")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/OldName", payload="NewName", params=None)

    def test_delete_setting(self) -> None:
        """Test delete_setting method."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_setting("feature1", "Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom", params={"scope": "project/test"})

    def test_get_setting_default_content(self) -> None:
        """Test get_setting_default_content method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_default_content("feature1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/default-content")

    def test_get_setting_revisions(self) -> None:
        """Test get_setting_revisions method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_setting_revisions("feature1", name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/settings/feature1/names/Custom/revisions", params={"scope": "project/test"})

    # =========================================================================
    # Excel Export Operations
    # =========================================================================

    def test_wait_for_export(self) -> None:
        """Test wait for export method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.wait_for_export("export-123", timeout=30)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/excel-tool/exports/export-123/wait"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"timeout": "30"})

    # =========================================================================
    # Import Jobs
    # =========================================================================

    def test_get_all_import_jobs(self) -> None:
        """Test get all import jobs."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_all_import_jobs()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/import/jobs"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    @patch("pathlib.Path.open", new_callable=mock_open, read_data=b"excel content")
    def test_start_import_job(self, mock_file: Mock) -> None:
        """Test start import job."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.start_import_job("PROJ", "/path/to/file.xlsx", mapping_name="CustomMapping")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/import/jobs"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON}

        self.mock_connection.api_request_post.assert_called_once()
        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertEqual(call_args[0][0], expected_url)
        self.assertEqual(call_args[1]["headers"], expected_headers)
        self.assertIn("files", call_args[1])

    def test_get_import_job_status(self) -> None:
        """Test get import job status."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_import_job_status("job-123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/import/jobs/job-123"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_import_job_result(self) -> None:
        """Test get import job result."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_import_job_result("job-123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/import/jobs/job-123/result"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    # =========================================================================
    # Mapping Convenience Methods
    # =========================================================================

    def test_get_mapping_names(self) -> None:
        """Test get mapping names."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_mapping_names(scope="project/test")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"scope": "project/test"})

    def test_rename_mapping(self) -> None:
        """Test rename mapping."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.rename_mapping("OldName", "NewName", scope="project/test")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/settings/{MAPPINGS_FEATURE}/names/OldName"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, payload="NewName", params={"scope": "project/test"})


if __name__ == "__main__":
    unittest.main()
