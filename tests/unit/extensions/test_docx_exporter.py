"""Unit tests for DOCX Exporter extension"""

from __future__ import annotations

import unittest
from http import HTTPStatus
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock, mock_open, patch

from python_sbb_polarion.extensions.docx_exporter import PolarionDocxExporterApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, JsonList


class TestPolarionDocxExporterApi(unittest.TestCase):
    """Test PolarionDocxExporterApi class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.mock_connection = Mock()
        self.api = PolarionDocxExporterApi(self.mock_connection)

    def test_initialization(self) -> None:
        """Test API initialization"""
        self.assertEqual(self.api.extension_name, "docx-exporter")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)
        self.assertEqual(self.api.rest_api_url, "/polarion/docx-exporter/rest/api")

    # =========================================================================
    # Collections
    # =========================================================================

    def test_documents_from_collection_without_revision(self) -> None:
        """Test documents_from_collection without revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_documents_from_collection("test_project", "collection_123")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/projects/test_project/collections/collection_123/documents", params=None)
        self.assertEqual(result, mock_response)

    def test_documents_from_collection_with_revision(self) -> None:
        """Test documents_from_collection with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_documents_from_collection("test_project", "collection_123", revision="12345")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/projects/test_project/collections/collection_123/documents", params={"revision": "12345"})
        self.assertEqual(result, mock_response)

    # =========================================================================
    # DOCX Conversion
    # =========================================================================

    def test_convert_html_default_params(self) -> None:
        """Test convert_html method with default parameters"""
        html_content: str = "<html><body>Test</body></html>"
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert_html(html_content)

        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertEqual(call_args[0][0], "/polarion/docx-exporter/rest/api/convert/html")
        self.assertEqual(call_args[1]["headers"][Header.ACCEPT], MediaType.ANY)
        self.assertEqual(call_args[1]["params"]["fileName"], "html-to-docx.docx")
        self.assertIn("files", call_args[1])
        self.assertEqual(result, mock_response)

    def test_convert_html_with_template(self) -> None:
        """Test convert_html method with template"""
        html_content: str = "<html><body>Test</body></html>"
        template: bytes = b"custom template content in binary format"
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert_html(html_content, template=template, file_name="custom.docx")

        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertEqual(call_args[0][0], "/polarion/docx-exporter/rest/api/convert/html")
        self.assertEqual(call_args[1]["params"]["fileName"], "custom.docx")
        self.assertEqual(call_args[1]["files"]["html"], ("file.html", "<html><body>Test</body></html>"))
        self.assertEqual(call_args[1]["files"]["template"], ("template.docx", b"custom template content in binary format"))
        self.assertEqual(result, mock_response)

    def test_convert_html_with_options(self) -> None:
        """Test convert_html method with options parameter"""
        html_content: str = "<html><body>Test</body></html>"
        options: JsonDict = {"option1": "value1"}
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert_html(html_content, options=options)

        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertIn("options", call_args[1]["files"])
        self.assertEqual(result, mock_response)

    def test_convert_html_with_params(self) -> None:
        """Test convert_html method with params parameter"""
        html_content: str = "<html><body>Test</body></html>"
        params: JsonDict = {
            "param1": "value1",
        }
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert_html(html_content, params=params)

        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertIn("params", call_args[1]["files"])
        self.assertEqual(result, mock_response)

    def test_get_all_docx_converter_jobs(self) -> None:
        """Test get_all_docx_converter_jobs method"""
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_all_docx_converter_jobs()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/convert/jobs")
        self.assertEqual(result, mock_response)

    def test_start_docx_converter_job(self) -> None:
        """Test start_docx_converter_job method"""
        export_params: JsonDict = {"projectId": "test_project", "documentName": "test_doc"}
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.CREATED
        mock_response.json.return_value = {"jobId": "job-123"}
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.start_docx_converter_job(export_params)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/convert/jobs",
            data=export_params,
            headers={Header.ACCEPT: MediaType.JSON, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    def test_get_docx_converter_job_result(self) -> None:
        """Test get_docx_converter_job_result method"""
        job_id: str = "job-456"
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_docx_converter_job_result(job_id)

        self.mock_connection.api_request_get.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/convert/jobs/job-456/result",
            headers={Header.ACCEPT: MediaType.DOCX, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    def test_get_docx_converter_job_status(self) -> None:
        """Test get_docx_converter_job_status method"""
        job_id: str = "job-123"
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_docx_converter_job_status(job_id)

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/convert/jobs/job-123", allow_redirects=False)
        self.assertEqual(result, mock_response)

    def test_prepared_html_content(self) -> None:
        """Test prepared_html_content method"""
        export_params: JsonDict = {"projectId": "test_project", "documentName": "test_doc"}
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.receive_prepared_html_content(export_params)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/prepared-html-content",
            data=export_params,
            headers={Header.ACCEPT: MediaType.HTML, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    def test_convert(self) -> None:
        """Test convert method"""
        export_params: JsonDict = {"projectId": "test_project", "documentName": "test_doc"}
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert(export_params)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/convert",
            data=export_params,
            headers={Header.ACCEPT: MediaType.DOCX, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Template
    # =========================================================================

    def test_get_template(self) -> None:
        """Test get_template method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_template()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/template")
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Localization Settings
    # =========================================================================

    @patch("pathlib.Path.open", new_callable=mock_open, read_data="<xliff>test</xliff>")
    def test_settings_localization_upload(self, mock_file: Mock) -> None:
        """Test settings_localization_upload method"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.upload_localization_settings("/path/to/test.xliff", "en", "project/test")

        self.mock_connection.api_request_post.assert_called_once()
        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertEqual(call_args[0][0], "/polarion/docx-exporter/rest/api/settings/localization/upload")
        self.assertIn("files", call_args[1])
        self.assertEqual(call_args[1]["params"], {"language": "en", "scope": "project/test"})
        self.assertEqual(result, mock_response)

    @patch("pathlib.Path.open", create=True)
    def test_settings_localization_upload_with_scope(self, mock_open: Mock) -> None:
        """Test settings_localization_upload with scope parameter"""
        mock_file_content: str = "xliff content"
        mock_open.return_value.__enter__.return_value.read.return_value = mock_file_content
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.upload_localization_settings("en", "/path/to/file.xliff", scope="project")

        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertIn("scope", call_args[1]["params"])
        self.assertEqual(call_args[1]["params"]["scope"], "project")
        self.assertEqual(result, mock_response)

    @patch("pathlib.Path.open", create=True)
    def test_settings_localization_upload_with_empty_scope(self, mock_open: Mock) -> None:
        """Test settings_localization_upload with empty scope (falsy value)"""
        mock_file_content: str = "xliff content"
        mock_open.return_value.__enter__.return_value.read.return_value = mock_file_content
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.upload_localization_settings("en", "/path/to/file.xliff", scope="")

        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        # Empty string is falsy, so scope should not be added to params
        self.assertNotIn("scope", call_args[1]["params"])
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Suitable Style Package Names
    # =========================================================================

    def test_find_suitable_style_package_names(self) -> None:
        """Test find_suitable_style_package_names method"""
        data: JsonList = [
            {
                "projectId": "PROJECT",
                "spaceId": "Space1",
                "documentName": "doc1",
            }
        ]
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.find_suitable_style_package_names(data)

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/suitable-names", data=data)
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Style Package Weights
    # =========================================================================

    def test_get_style_package_weights(self) -> None:
        """Test get_style_package_weights method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_package_weights("project/test")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/weights", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_save_style_package_weights(self) -> None:
        """Test save_style_package_weights method"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonList = [{"name": "Package1", "weight": 10}]

        result: Response = self.api.save_style_package_weights(data)

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/weights", data=data)
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Localization Download
    # =========================================================================

    def test_settings_localization_download_minimal(self) -> None:
        """Test settings_localization_download with minimal parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.download_localization_settings("en")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/localization/names/Default/download", headers={Header.ACCEPT: MediaType.XML}, params={"language": "en"})
        self.assertEqual(result, mock_response)

    def test_settings_localization_download_with_all_params(self) -> None:
        """Test settings_localization_download with all parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.download_localization_settings("de", name="Custom", scope="project/test", revision="12345")

        self.mock_connection.api_request_get.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/settings/localization/names/Custom/download", headers={Header.ACCEPT: MediaType.XML}, params={"language": "de", "scope": "project/test", "revision": "12345"}
        )
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Test Run Attachments
    # =========================================================================

    def test_get_test_run_attachment_without_revision(self) -> None:
        """Test get_test_run_attachment without revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment("test_project", "testrun_123", "attach_456")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/projects/test_project/testruns/testrun_123/attachments/attach_456", params=None)
        self.assertEqual(result, mock_response)

    def test_get_test_run_attachment_with_revision(self) -> None:
        """Test get_test_run_attachment with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment("test_project", "testrun_123", "attach_456", revision="12345")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/projects/test_project/testruns/testrun_123/attachments/attach_456", params={"revision": "12345"})
        self.assertEqual(result, mock_response)

    def test_test_run_attachment_content_without_revision(self) -> None:
        """Test test_run_attachment_content without revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment_content("test_project", "testrun_123", "attach_456")

        self.mock_connection.api_request_get.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/projects/test_project/testruns/testrun_123/attachments/attach_456/content",
            headers={Header.ACCEPT: MediaType.OCTET_STREAM},
            params=None,
        )
        self.assertEqual(result, mock_response)

    def test_test_run_attachment_content_with_revision(self) -> None:
        """Test test_run_attachment_content with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment_content("test_project", "testrun_123", "attach_456", revision="12345")

        self.mock_connection.api_request_get.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/projects/test_project/testruns/testrun_123/attachments/attach_456/content",
            headers={Header.ACCEPT: MediaType.OCTET_STREAM},
            params={"revision": "12345"},
        )
        self.assertEqual(result, mock_response)

    def test_test_run_attachments_minimal(self) -> None:
        """Test test_run_attachments with minimal parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachments("test_project", "testrun_123")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/projects/test_project/testruns/testrun_123/attachments", params=None)
        self.assertEqual(result, mock_response)

    def test_test_run_attachments_with_all_params(self) -> None:
        """Test test_run_attachments with all parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachments("test_project", "testrun_123", revision="12345", filter_query="*.png")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/projects/test_project/testruns/testrun_123/attachments", params={"revision": "12345", "filter": "*.png"})
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Document Utilities
    # =========================================================================

    def test_generate_document_export_filename(self) -> None:
        """Test generate_document_export_filename method"""
        data: JsonDict = {
            "projectId": "test_project",
            "documentName": "test_doc",
        }
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.generate_document_export_filename(data)

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/docx-exporter/rest/api/export-filename", headers={Header.ACCEPT: MediaType.PLAIN}, data=data)
        self.assertEqual(result, mock_response)

    def test_get_link_role_names(self) -> None:
        """Test get_link_role_names method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_link_role_names("project/test")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/link-role-names", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_get_document_language_without_revision(self) -> None:
        """Test get_document_language without revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_document_language("test_project", "test_space", "test_doc")

        self.mock_connection.api_request_get.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/document-language", headers={Header.ACCEPT: MediaType.PLAIN}, params={"projectId": "test_project", "spaceId": "test_space", "documentName": "test_doc"}
        )
        self.assertEqual(result, mock_response)

    def test_get_document_language_with_revision(self) -> None:
        """Test get_document_language with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_document_language("test_project", "test_space", "test_doc", revision="12345")

        self.mock_connection.api_request_get.assert_called_once_with(
            "/polarion/docx-exporter/rest/api/document-language", headers={Header.ACCEPT: MediaType.PLAIN}, params={"projectId": "test_project", "spaceId": "test_space", "documentName": "test_doc", "revision": "12345"}
        )
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Webhooks and Project Info
    # =========================================================================

    def test_get_webhooks_status(self) -> None:
        """Test get_webhooks_status method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_webhooks_status()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/webhooks/status")
        self.assertEqual(result, mock_response)

    def test_get_project_name(self) -> None:
        """Test get_project_name method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_project_name("test_project")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/projects/test_project/name", headers={Header.ACCEPT: MediaType.PLAIN})
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Style Packages
    # =========================================================================

    def test_get_style_packages_names_default(self) -> None:
        """Test get_style_packages_names with default scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_packages_names()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names", params=None)
        self.assertEqual(result, mock_response)

    def test_get_style_packages_names_with_scope(self) -> None:
        """Test get_style_packages_names with specific scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_packages_names(scope="project/test")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_get_style_package_minimal(self) -> None:
        """Test get_style_package with minimal parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_package("PackageName")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names/PackageName/content", params=None)
        self.assertEqual(result, mock_response)

    def test_get_style_package_with_all_params(self) -> None:
        """Test get_style_package with all parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_package("PackageName", scope="project/test", revision="12345")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names/PackageName/content", params={"scope": "project/test", "revision": "12345"})
        self.assertEqual(result, mock_response)

    def test_save_style_package_default(self) -> None:
        """Test save_style_package with default scope"""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "styleContent": "test",
        }

        result: Response = self.api.save_style_package("PackageName", data)

        self.mock_connection.api_request_put.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names/PackageName/content", params=None, data=data)
        self.assertEqual(result, mock_response)

    def test_save_style_package_with_scope(self) -> None:
        """Test save_style_package with specific scope"""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "styleContent": "test",
        }

        result: Response = self.api.save_style_package("PackageName", data, scope="project/test")

        self.mock_connection.api_request_put.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names/PackageName/content", params={"scope": "project/test"}, data=data)
        self.assertEqual(result, mock_response)

    def test_delete_style_package_default(self) -> None:
        """Test delete_style_package with default scope"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_style_package("PackageName")

        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names/PackageName", params=None)
        self.assertEqual(result, mock_response)

    def test_delete_style_package_with_scope(self) -> None:
        """Test delete_style_package with specific scope"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_style_package("PackageName", scope="project/test")

        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/style-package/names/PackageName", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Configuration Checks
    # =========================================================================

    def test_get_cors_config(self) -> None:
        """Test get_cors_config method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_cors_config()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/configuration/cors-config")
        self.assertEqual(result, mock_response)

    def test_default_settings_without_scope(self) -> None:
        """Test default_settings method without scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_default_settings()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/configuration/default-settings", params=None)
        self.assertEqual(result, mock_response)

    def test_default_settings_with_scope(self) -> None:
        """Test default_settings method with scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_default_settings(scope="project/test")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/configuration/default-settings", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_get_dle_toolbar_config(self) -> None:
        """Test get_dle_toolbar_config method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_dle_toolbar_config()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/configuration/dle-toolbar-config")
        self.assertEqual(result, mock_response)

    def test_validate_document_properties_pane_config_without_scope(self) -> None:
        """Test validate_document_properties_pane_config without scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_document_properties_pane_config()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/configuration/document-properties-pane-config", params=None)
        self.assertEqual(result, mock_response)

    def test_validate_document_properties_pane_config_with_scope(self) -> None:
        """Test validate_document_properties_pane_config with scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_document_properties_pane_config(scope="project/test")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/configuration/document-properties-pane-config", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_validate_pandoc(self) -> None:
        """Test validate_pandoc method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_pandoc()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/configuration/pandoc")
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Base Class Settings Methods
    # =========================================================================

    def test_get_features(self) -> None:
        """Test get_features method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_features()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings")
        self.assertEqual(result, mock_response)

    def test_get_setting_content(self) -> None:
        """Test get_setting_content method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_setting_content("cover-page", "MySettings", scope="project")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/cover-page/names/MySettings/content", params={"scope": "project"})
        self.assertEqual(result, mock_response)

    def test_get_setting_names(self) -> None:
        """Test get_setting_names method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_setting_names("cover-page")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/cover-page/names", params=None)
        self.assertEqual(result, mock_response)

    def test_rename_setting(self) -> None:
        """Test rename_setting method"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.rename_setting("cover-page", "OldName", "NewName")

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/cover-page/names/OldName", payload="NewName", params=None)
        self.assertEqual(result, mock_response)

    def test_rename_setting_with_scope(self) -> None:
        """Test rename_setting method with scope parameter"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.rename_setting("cover-page", "OldName", "NewName", scope="project/TEST/")

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/docx-exporter/rest/api/settings/cover-page/names/OldName", payload="NewName", params={"scope": "project/TEST/"})
        self.assertEqual(result, mock_response)

    def test_save_setting(self) -> None:
        """Test save_setting method"""
        data: JsonDict = {
            "key": "value",
        }
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response

        result: Response = self.api.save_setting("feature1", data, name="Custom", scope="project/elibrary/")

        self.assertEqual(result, mock_response)

    def test_delete_setting(self) -> None:
        """Test delete_setting method"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_setting("feature1", "Custom", scope="project/elibrary/")

        self.assertEqual(result, mock_response)

    def test_get_setting_default_content(self) -> None:
        """Test get_setting_default_content method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_setting_default_content("feature1")

        self.assertEqual(result, mock_response)

    def test_get_setting_revisions(self) -> None:
        """Test get_setting_revisions method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_setting_revisions("feature1", name="Custom", scope="project/elibrary/")

        self.assertEqual(result, mock_response)


if __name__ == "__main__":
    unittest.main()
