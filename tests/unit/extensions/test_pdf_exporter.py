"""Unit tests for PDF Exporter extension"""

from __future__ import annotations

import unittest
from http import HTTPStatus
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock, mock_open, patch

from python_sbb_polarion.extensions.pdf_exporter import DocumentType, Orientation, PaperSize, PdfVariant, PolarionPdfExporterApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, JsonList


class TestDocumentType(unittest.TestCase):
    """Test DocumentType enum"""

    def test_document_type_values(self) -> None:
        """Test that DocumentType enum has correct values"""
        self.assertEqual(DocumentType.LIVE_DOC.value, "LIVE_DOC")
        self.assertEqual(DocumentType.LIVE_REPORT.value, "LIVE_REPORT")
        self.assertEqual(DocumentType.TEST_RUN.value, "TEST_RUN")
        self.assertEqual(DocumentType.WIKI_PAGE.value, "WIKI_PAGE")

    def test_document_type_is_string(self) -> None:
        """Test that DocumentType enum values are strings"""
        self.assertIsInstance(DocumentType.LIVE_DOC, str)
        self.assertEqual(DocumentType.LIVE_DOC, "LIVE_DOC")


class TestPdfVariant(unittest.TestCase):
    """Test PdfVariant enum"""

    def test_pdf_variant_values(self) -> None:
        """Test that PdfVariant enum has correct values"""
        self.assertEqual(PdfVariant.PDF_A_1A.value, "PDF_A_1A")
        self.assertEqual(PdfVariant.PDF_A_1B.value, "PDF_A_1B")
        self.assertEqual(PdfVariant.PDF_A_2A.value, "PDF_A_2A")
        self.assertEqual(PdfVariant.PDF_A_2B.value, "PDF_A_2B")
        self.assertEqual(PdfVariant.PDF_A_2U.value, "PDF_A_2U")
        self.assertEqual(PdfVariant.PDF_A_3A.value, "PDF_A_3A")
        self.assertEqual(PdfVariant.PDF_A_3B.value, "PDF_A_3B")
        self.assertEqual(PdfVariant.PDF_A_3U.value, "PDF_A_3U")
        self.assertEqual(PdfVariant.PDF_A_4E.value, "PDF_A_4E")
        self.assertEqual(PdfVariant.PDF_A_4F.value, "PDF_A_4F")
        self.assertEqual(PdfVariant.PDF_A_4U.value, "PDF_A_4U")
        self.assertEqual(PdfVariant.PDF_UA_1.value, "PDF_UA_1")
        self.assertEqual(PdfVariant.PDF_UA_2.value, "PDF_UA_2")

    def test_pdf_variant_is_string(self) -> None:
        """Test that PdfVariant enum values are strings"""
        self.assertIsInstance(PdfVariant.PDF_A_2B, str)
        self.assertEqual(PdfVariant.PDF_A_2B, "PDF_A_2B")


class TestOrientation(unittest.TestCase):
    """Test Orientation enum"""

    def test_orientation_values(self) -> None:
        """Test that Orientation enum has correct values"""
        self.assertEqual(Orientation.PORTRAIT.value, "PORTRAIT")
        self.assertEqual(Orientation.LANDSCAPE.value, "LANDSCAPE")

    def test_orientation_is_string(self) -> None:
        """Test that Orientation enum values are strings"""
        self.assertIsInstance(Orientation.PORTRAIT, str)
        self.assertEqual(Orientation.PORTRAIT, "PORTRAIT")


class TestPaperSize(unittest.TestCase):
    """Test PaperSize enum"""

    def test_paper_size_values(self) -> None:
        """Test that PaperSize enum has correct values"""
        self.assertEqual(PaperSize.A5.value, "A5")
        self.assertEqual(PaperSize.A4.value, "A4")
        self.assertEqual(PaperSize.A3.value, "A3")
        self.assertEqual(PaperSize.B5.value, "B5")
        self.assertEqual(PaperSize.B4.value, "B4")
        self.assertEqual(PaperSize.JIS_B5.value, "JIS_B5")
        self.assertEqual(PaperSize.JIS_B4.value, "JIS_B4")
        self.assertEqual(PaperSize.LETTER.value, "LETTER")
        self.assertEqual(PaperSize.LEGAL.value, "LEGAL")
        self.assertEqual(PaperSize.LEDGER.value, "LEDGER")

    def test_paper_size_is_string(self) -> None:
        """Test that PaperSize enum values are strings"""
        self.assertIsInstance(PaperSize.A4, str)
        self.assertEqual(PaperSize.A4, "A4")


class TestPolarionPdfExporterApi(unittest.TestCase):
    """Test PolarionPdfExporterApi class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.mock_connection = Mock()
        self.api = PolarionPdfExporterApi(self.mock_connection)

    def test_initialization(self) -> None:
        """Test API initialization"""
        self.assertEqual(self.api.extension_name, "pdf-exporter")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)
        self.assertEqual(self.api.rest_api_url, "/polarion/pdf-exporter/rest/api")

    # =========================================================================
    # Style Packages
    # =========================================================================

    def test_delete_style_package(self) -> None:
        """Test delete_style_package method"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_style_package("package1", scope="project/elibrary/")

        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names/package1", params={"scope": "project/elibrary/"})
        self.assertEqual(result, mock_response)

    def test_delete_style_package_without_scope(self) -> None:
        """Test delete_style_package method without scope parameter"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_style_package("package1")

        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names/package1", params=None)
        self.assertEqual(result, mock_response)

    def test_get_style_package_with_revision(self) -> None:
        """Test get_style_package method with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_package("package1", revision="1.0")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names/package1/content", params={"revision": "1.0"})
        self.assertEqual(result, mock_response)

    def test_get_style_package_without_revision(self) -> None:
        """Test get_style_package method without revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_package("package1")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names/package1/content", params=None)
        self.assertEqual(result, mock_response)

    def test_get_style_package_with_scope(self) -> None:
        """Test get_style_package method with scope parameter"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_package("package1", scope="project/TEST/")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names/package1/content", params={"scope": "project/TEST/"})
        self.assertEqual(result, mock_response)

    def test_save_style_package(self) -> None:
        """Test save_style_package method"""
        data: JsonDict = {
            "style": "data",
        }
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response

        result: Response = self.api.save_style_package("package1", data, scope="project/elibrary/")

        self.mock_connection.api_request_put.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names/package1/content", data=data, params={"scope": "project/elibrary/"})
        self.assertEqual(result, mock_response)

    def test_save_style_package_without_scope(self) -> None:
        """Test save_style_package method without scope parameter"""
        data: JsonDict = {
            "style": "data",
        }
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response

        result: Response = self.api.save_style_package("package1", data)

        self.mock_connection.api_request_put.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names/package1/content", data=data, params=None)
        self.assertEqual(result, mock_response)

    def test_get_style_packages_names(self) -> None:
        """Test get_style_packages_names method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_packages_names("project/elibrary/")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names", params={"scope": "project/elibrary/"})
        self.assertEqual(result, mock_response)

    def test_get_style_packages_names_without_scope(self) -> None:
        """Test get_style_packages_names method without scope parameter"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_packages_names()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/names", params=None)
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Collections
    # =========================================================================

    def test_get_documents_from_collection(self) -> None:
        """Test get_documents_from_collection method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_documents_from_collection("PROJ", "collection1")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/projects/PROJ/collections/collection1/documents", params=None)
        self.assertEqual(result, mock_response)

    def test_get_documents_from_collection_with_revision(self) -> None:
        """Test get_documents_from_collection method with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_documents_from_collection("PROJ", "collection1", revision="1.0")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/projects/PROJ/collections/collection1/documents", params={"revision": "1.0"})
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Configuration Checks
    # =========================================================================

    def test_check_live_report_config(self) -> None:
        """Test check_live_report_config method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_live_report_config()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/live-report-config")
        self.assertEqual(result, mock_response)

    def test_check_weasyprint(self) -> None:
        """Test check_weasyprint method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_weasyprint()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/weasyprint")
        self.assertEqual(result, mock_response)

    def test_check_default_settings(self) -> None:
        """Test check_default_settings method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_default_settings()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/default-settings", params=None)
        self.assertEqual(result, mock_response)

    def test_check_default_settings_with_scope(self) -> None:
        """Test check_default_settings method with scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_default_settings(scope="project/test")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/default-settings", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_check_document_properties_pane_config(self) -> None:
        """Test check_document_properties_pane_config method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_document_properties_pane_config()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/document-properties-pane-config", params=None)
        self.assertEqual(result, mock_response)

    def test_check_document_properties_pane_config_with_scope(self) -> None:
        """Test check_document_properties_pane_config method with scope"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_document_properties_pane_config(scope="project/test")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/document-properties-pane-config", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_check_dle_toolbar_config(self) -> None:
        """Test check_dle_toolbar_config method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_dle_toolbar_config()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/dle-toolbar-config")
        self.assertEqual(result, mock_response)

    def test_check_cors_config(self) -> None:
        """Test check_cors_config method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.check_cors_config()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/configuration/cors-config")
        self.assertEqual(result, mock_response)

    # =========================================================================
    # PDF Conversion
    # =========================================================================

    def test_convert_html_default_params(self) -> None:
        """Test convert_html method with default parameters"""
        html_content: str = "<html><body>Test</body></html>"
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert_html(html_content)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/pdf-exporter/rest/api/convert/html",
            payload=html_content,
            headers={Header.ACCEPT: MediaType.ANY, Header.CONTENT_TYPE: MediaType.HTML},
            params={"orientation": Orientation.PORTRAIT, "paperSize": PaperSize.A4, "pdfVariant": PdfVariant.PDF_A_2B, "fitToPage": "false", "fileName": "html-to-pdf.pdf"},
        )
        self.assertEqual(result, mock_response)

    def test_convert_html_custom_params(self) -> None:
        """Test convert_html method with custom parameters"""
        html_content: str = "<html><body>Test</body></html>"
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert_html(html_content, orientation=Orientation.LANDSCAPE, paper_size=PaperSize.LETTER, filename="custom.pdf", fit_to_page=True)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/pdf-exporter/rest/api/convert/html",
            payload=html_content,
            headers={Header.ACCEPT: MediaType.ANY, Header.CONTENT_TYPE: MediaType.HTML},
            params={"orientation": Orientation.LANDSCAPE, "paperSize": PaperSize.LETTER, "pdfVariant": PdfVariant.PDF_A_2B, "fitToPage": "true", "fileName": "custom.pdf"},
        )
        self.assertEqual(result, mock_response)

    def test_get_all_pdf_converter_jobs(self) -> None:
        """Test get_all_pdf_converter_jobs method"""
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_all_pdf_converter_jobs()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/convert/jobs")
        self.assertEqual(result, mock_response)

    def test_start_pdf_conversion_job(self) -> None:
        """Test start_pdf_conversion_job method"""
        export_params: JsonDict = {"projectId": "test_project", "documentName": "test_doc"}
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.CREATED
        mock_response.json.return_value = {"jobId": "job-123"}
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.start_pdf_conversion_job(export_params)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/pdf-exporter/rest/api/convert/jobs",
            data=export_params,
            headers={Header.ACCEPT: MediaType.JSON, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    def test_get_pdf_converter_job_result(self) -> None:
        """Test get_pdf_converter_job_result method"""
        job_id: str = "job-456"
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_pdf_converter_job_result(job_id)

        self.mock_connection.api_request_get.assert_called_once_with(
            "/polarion/pdf-exporter/rest/api/convert/jobs/job-456/result",
            headers={Header.ACCEPT: MediaType.PDF, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    def test_get_pdf_converter_job_status(self) -> None:
        """Test get_pdf_converter_job_status method"""
        job_id: str = "job-123"
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_pdf_converter_job_status(job_id)

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/convert/jobs/job-123", allow_redirects=False)
        self.assertEqual(result, mock_response)

    def test_prepared_html_content(self) -> None:
        """Test prepared_html_content method"""
        export_params: JsonDict = {"projectId": "test_project", "documentName": "test_doc"}
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.receive_prepared_html_content(export_params)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/pdf-exporter/rest/api/prepared-html-content",
            data=export_params,
            headers={Header.ACCEPT: MediaType.HTML, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    def test_validate(self) -> None:
        """Test validate method"""
        export_params: JsonDict = {"projectId": "test_project", "documentName": "test_doc"}
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.validate(export_params, max_results=10)

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/validate", data=export_params, params={"max-results": "10"})
        self.assertEqual(result, mock_response)

    def test_convert(self) -> None:
        """Test convert method"""
        export_params: JsonDict = {"projectId": "test_project", "documentName": "test_doc"}
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.convert(export_params)

        self.mock_connection.api_request_post.assert_called_once_with(
            "/polarion/pdf-exporter/rest/api/convert",
            data=export_params,
            headers={Header.ACCEPT: MediaType.PDF, Header.CONTENT_TYPE: MediaType.JSON},
        )
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Localization Settings
    # =========================================================================

    @patch("pathlib.Path.open", new_callable=mock_open, read_data="<xliff>test</xliff>")
    @patch("os.path.basename", return_value="test.xliff")
    def test_settings_localization_upload(self, mock_basename: Mock, mock_file: Mock) -> None:
        """Test settings_localization_upload method"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.upload_localization_settings("/path/to/test.xliff", "en", "project/test")

        expected_url: str = "/polarion/pdf-exporter/rest/api/settings/localization/upload"
        expected_params: dict[str, str] = {"language": "en", "scope": "project/test"}
        self.mock_connection.api_request_post.assert_called_once()
        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertEqual(call_args[0][0], expected_url)
        self.assertEqual(call_args[1]["params"], expected_params)
        self.assertIn("files", call_args[1])
        self.assertEqual(result, mock_response)

    @patch("pathlib.Path.open", create=True)
    def test_settings_localization_upload_with_empty_scope(self, mock_open: Mock) -> None:
        """Test settings_localization_upload with empty scope (falsy value)"""
        mock_file = Mock()
        mock_file.read.return_value = "xliff content"
        mock_open.return_value.__enter__.return_value = mock_file
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.upload_localization_settings("/path/to/file.xliff", "en", scope="")

        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        # Empty string is falsy, so scope should not be added to params
        self.assertEqual(call_args[1]["params"], {"language": "en"})
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

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/suitable-names", data=data)
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Style Package Weights
    # =========================================================================

    def test_get_style_package_weights(self) -> None:
        """Test get_style_package_weights method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_style_package_weights("project/elibrary/")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/weights", params={"scope": "project/elibrary/"})
        self.assertEqual(result, mock_response)

    def test_save_style_package_weights(self) -> None:
        """Test save_style_package_weights method"""
        data: JsonList = [{"name": "package1", "weight": 10}]
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.save_style_package_weights(data)

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/style-package/weights", data=data)
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Cover Page Templates
    # =========================================================================

    def test_get_cover_page_template_names(self) -> None:
        """Test get_cover_page_template_names method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_cover_page_template_names()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/templates")
        self.assertEqual(result, mock_response)

    def test_persist_cover_page_template(self) -> None:
        """Test persist_cover_page_template method without scope"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.persist_cover_page_template("template1")

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/templates/template1", params=None)
        self.assertEqual(result, mock_response)

    def test_persist_cover_page_template_with_scope(self) -> None:
        """Test persist_cover_page_template method with scope"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.persist_cover_page_template("template1", scope="project/test")

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/templates/template1", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    def test_delete_cover_page_images(self) -> None:
        """Test delete_cover_page_images method without scope"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_cover_page_images("cover1")

        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/names/cover1/images", params=None)
        self.assertEqual(result, mock_response)

    def test_delete_cover_page_images_with_scope(self) -> None:
        """Test delete_cover_page_images method with scope"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_cover_page_images("cover1", scope="project/test")

        self.mock_connection.api_request_delete.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/names/cover1/images", params={"scope": "project/test"})
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Localization Download
    # =========================================================================

    def test_settings_localization_download_minimal(self) -> None:
        """Test settings_localization_download with minimal parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.download_localization_settings("en")

        expected_url: str = "/polarion/pdf-exporter/rest/api/settings/localization/names/Default/download"
        expected_params: dict[str, str] = {"language": "en"}
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.XML}, params=expected_params)
        self.assertEqual(result, mock_response)

    def test_settings_localization_download_with_all_params(self) -> None:
        """Test settings_localization_download with all parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.download_localization_settings("de", name="Custom", scope="project/test", revision="12345")

        expected_url: str = "/polarion/pdf-exporter/rest/api/settings/localization/names/Custom/download"
        expected_params: dict[str, str] = {"language": "de", "scope": "project/test", "revision": "12345"}
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.XML}, params=expected_params)
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Test Run Attachments
    # =========================================================================

    def test_get_test_run_attachment(self) -> None:
        """Test get_test_run_attachment method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment("PROJ", "run1", "attach1")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/projects/PROJ/testruns/run1/attachments/attach1", params=None)
        self.assertEqual(result, mock_response)

    def test_get_test_run_attachment_with_revision(self) -> None:
        """Test get_test_run_attachment method with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment("PROJ", "run1", "attach1", revision="1.0")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/projects/PROJ/testruns/run1/attachments/attach1", params={"revision": "1.0"})
        self.assertEqual(result, mock_response)

    def test_get_test_run_attachment_content(self) -> None:
        """Test get_test_run_attachment_content method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment_content("PROJ", "run1", "attach1")

        call_args: tuple[Any, ...] = self.mock_connection.api_request_get.call_args
        self.assertEqual(call_args[0][0], "/polarion/pdf-exporter/rest/api/projects/PROJ/testruns/run1/attachments/attach1/content")
        self.assertIn("headers", call_args[1])
        self.assertEqual(result, mock_response)

    def test_get_test_run_attachment_content_with_revision(self) -> None:
        """Test get_test_run_attachment_content method with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachment_content("PROJ", "run1", "attach1", revision="1.0")

        call_args: tuple[Any, ...] = self.mock_connection.api_request_get.call_args
        self.assertEqual(call_args[0][0], "/polarion/pdf-exporter/rest/api/projects/PROJ/testruns/run1/attachments/attach1/content")
        self.assertEqual(call_args[1]["params"], {"revision": "1.0"})
        self.assertEqual(result, mock_response)

    def test_get_test_run_attachments(self) -> None:
        """Test get_test_run_attachments method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachments("PROJ", "run1")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/projects/PROJ/testruns/run1/attachments", params=None)
        self.assertEqual(result, mock_response)

    def test_get_test_run_attachments_with_all_params(self) -> None:
        """Test get_test_run_attachments method with all parameters"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_test_run_attachments("PROJ", "run1", revision="1.0", filter_query="*.png", test_case_filter_field_id="testCaseId")

        expected_params: dict[str, str] = {"revision": "1.0", "filter": "*.png", "testCaseFilterFieldId": "testCaseId"}
        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/projects/PROJ/testruns/run1/attachments", params=expected_params)
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

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/export-filename", headers={Header.ACCEPT: MediaType.PLAIN}, data=data)
        self.assertEqual(result, mock_response)

    def test_get_link_role_names(self) -> None:
        """Test get_link_role_names method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_link_role_names("project/elibrary/")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/link-role-names", params={"scope": "project/elibrary/"})
        self.assertEqual(result, mock_response)

    def test_get_document_language_with_revision(self) -> None:
        """Test get_document_language method with revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_document_language("PROJ", "space1", "doc1", revision="1.0")

        expected_url: str = "/polarion/pdf-exporter/rest/api/document-language"
        expected_params: dict[str, str] = {"projectId": "PROJ", "spaceId": "space1", "documentName": "doc1", "revision": "1.0"}
        call_args: tuple[Any, ...] = self.mock_connection.api_request_get.call_args
        self.assertEqual(call_args[0][0], expected_url)
        self.assertEqual(call_args[1]["params"], expected_params)
        self.assertEqual(result, mock_response)

    def test_get_document_language_without_revision(self) -> None:
        """Test get_document_language method without revision"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_document_language("PROJ", "space1", "doc1")

        call_args: tuple[Any, ...] = self.mock_connection.api_request_get.call_args
        self.assertNotIn("revision", call_args[0][0])
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Webhooks and Project Info
    # =========================================================================

    def test_get_webhooks_status(self) -> None:
        """Test get_webhooks_status method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_webhooks_status()

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/webhooks/status")
        self.assertEqual(result, mock_response)

    def test_get_project_name(self) -> None:
        """Test get_project_name method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_project_name("test_project")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/projects/test_project/name", headers={Header.ACCEPT: MediaType.PLAIN})
        self.assertEqual(result, mock_response)

    # =========================================================================
    # Base Class Settings Methods
    # =========================================================================

    def test_get_setting_content(self) -> None:
        """Test get_setting_content method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_setting_content("feature1", name="Custom", scope="project/elibrary/")

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

    def test_delete_setting(self) -> None:
        """Test delete_setting method"""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        result: Response = self.api.delete_setting("cover-page", "MySettings", scope="project")

        self.assertEqual(result, mock_response)

    def test_get_setting_names(self) -> None:
        """Test get_setting_names method"""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        result: Response = self.api.get_setting_names("cover-page")

        self.mock_connection.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/names", params=None)
        self.assertEqual(result, mock_response)

    def test_rename_setting(self) -> None:
        """Test rename_setting method"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.rename_setting("cover-page", "OldName", "NewName")

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/names/OldName", payload="NewName", params=None)
        self.assertEqual(result, mock_response)

    def test_rename_setting_with_scope(self) -> None:
        """Test rename_setting method with scope parameter"""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        result: Response = self.api.rename_setting("cover-page", "OldName", "NewName", scope="project/TEST/")

        self.mock_connection.api_request_post.assert_called_once_with("/polarion/pdf-exporter/rest/api/settings/cover-page/names/OldName", payload="NewName", params={"scope": "project/TEST/"})
        self.assertEqual(result, mock_response)


if __name__ == "__main__":
    unittest.main()
