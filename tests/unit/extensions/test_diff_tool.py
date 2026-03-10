"""Unit tests for Diff Tool API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

from python_sbb_polarion.extensions.diff_tool import Orientation, PaperSize, PolarionDiffToolApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionDiffToolApi(unittest.TestCase):
    """Test PolarionDiffToolApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionDiffToolApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "diff-tool")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Conversion
    # =========================================================================

    def test_convert_html_to_pdf_default_params(self) -> None:
        """Test convert HTML to PDF with default parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.convert_html_to_pdf("<html></html>")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/conversion/html-to-pdf"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.ANY, Header.CONTENT_TYPE: MediaType.HTML}
        expected_params: dict[str, str] = {"orientation": Orientation.LANDSCAPE, "paperSize": PaperSize.A4}
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data="<html></html>", headers=expected_headers, params=expected_params)

    def test_convert_html_to_pdf_custom_params(self) -> None:
        """Test convert HTML to PDF with custom parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.convert_html_to_pdf("<html></html>", orientation=Orientation.PORTRAIT, paper_size=PaperSize.A3)

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {"orientation": Orientation.PORTRAIT, "paperSize": PaperSize.A3}
        call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
        self.assertEqual(call_args[1]["params"], expected_params)

    # =========================================================================
    # Difference
    # =========================================================================

    def test_diff_collections(self) -> None:
        """Test diff collections."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.diff_collections("PROJ1", "coll1", "PROJ2", "coll2")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/collections"
        expected_data: JsonDict = {
            "leftCollection": {"id": "coll1", "name": "any", "projectId": "PROJ1", "projectName": "any"},
            "rightCollection": {"id": "coll2", "name": "any", "projectId": "PROJ2", "projectName": "any"},
        }
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=expected_data)

    def test_diff_detached_workitems(self) -> None:
        """Test diff detached workitems."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.diff_detached_workitems(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/detached-workitems"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_diff_document_workitems(self) -> None:
        """Test diff document workitems."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.diff_document_workitems(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/document-workitems"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_diff_documents(self) -> None:
        """Test diff documents."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.diff_documents(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/documents"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_diff_documents_fields(self) -> None:
        """Test diff documents fields."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.diff_documents_fields(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/documents-fields"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_diff_documents_content(self) -> None:
        """Test diff documents content."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.diff_documents_content(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/documents-content"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_diff_html(self) -> None:
        """Test diff HTML strings."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.diff_html("<html>v1</html>", "<html>v2</html>")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/html"
        expected_files: dict[str, str] = {"html1": "<html>v1</html>", "html2": "<html>v2</html>"}
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, files=expected_files)

    def test_diff_text(self) -> None:
        """Test diff plain text strings."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.diff_text("text v1", "text v2")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/text"
        expected_files: dict[str, str] = {"text1": "text v1", "text2": "text v2"}
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, files=expected_files)

    def test_find_workitems_pairs(self) -> None:
        """Test find workitems pairs."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.find_workitems_pairs(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/diff/workitems-pairs"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    # =========================================================================
    # Merge
    # =========================================================================

    def test_merge_document_workitems(self) -> None:
        """Test merge document workitems."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.merge_document_workitems(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/merge/documents"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_merge_documents_fields(self) -> None:
        """Test merge documents fields."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.merge_documents_fields(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/merge/documents-fields"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_merge_documents_content(self) -> None:
        """Test merge documents content."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.merge_documents_content(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/merge/documents-content"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_merge_detached_workitems(self) -> None:
        """Test merge detached workitems."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.merge_detached_workitems(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/merge/workitems"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    # =========================================================================
    # Utility API - Spaces and Documents
    # =========================================================================

    def test_get_spaces(self) -> None:
        """Test get spaces."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_spaces("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_documents_in_space(self) -> None:
        """Test get documents in space."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_documents_in_space("PROJ", "space1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_document_revisions(self) -> None:
        """Test get document revisions."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_document_revisions("PROJ", "space1", "doc1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1/revisions"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_create_document_duplicate(self) -> None:
        """Test create document duplicate."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "targetSpaceId": "space2",
            "targetDocumentName": "doc2",
        }

        response: Response = self.api.create_document_duplicate("PROJ", "space1", "doc1", data, revision="rev123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1/duplicate"
        expected_params: dict[str, str] = {"revision": "rev123"}
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, params=expected_params, data=data)

    def test_create_document_duplicate_without_revision(self) -> None:
        """Test create document duplicate without revision."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "targetSpaceId": "space2",
            "targetDocumentName": "doc2",
        }

        response: Response = self.api.create_document_duplicate("PROJ", "space1", "doc1", data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1/duplicate"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, params=None, data=data)

    # =========================================================================
    # Utility API - Work Item Fields and Statuses
    # =========================================================================

    def test_get_all_workitem_fields(self) -> None:
        """Test get all workitem fields."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_all_workitem_fields("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/workitem-fields"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_all_workitem_statuses(self) -> None:
        """Test get all workitem statuses."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_all_workitem_statuses("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/workitem-statuses"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_all_hyperlink_roles(self) -> None:
        """Test get all hyperlink roles."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_all_hyperlink_roles("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/hyperlink-roles"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_all_linked_workitem_roles(self) -> None:
        """Test get all linked workitem roles."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_all_linked_workitem_roles("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/linked-workitem-roles"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    # =========================================================================
    # Queue Statistics
    # =========================================================================

    def test_receive_queue_statistics(self) -> None:
        """Test get queue statistics."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.receive_queue_statistics(data)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/queueStatistics"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=data)

    def test_receive_queue_statistics_no_data(self) -> None:
        """Test get queue statistics without data."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.receive_queue_statistics()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/queueStatistics"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url)

    def test_clear_queue_statistics(self) -> None:
        """Test clear queue statistics."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.clear_queue_statistics()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/queueStatistics"
        self.mock_connection.api_request_delete.assert_called_once_with(expected_url)

    # =========================================================================
    # Extension Info
    # =========================================================================

    def test_get_communication_settings(self) -> None:
        """Test get communication settings."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_communication_settings()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/communication/settings"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_extension_info(self) -> None:
        """Test get extension info."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_extension_info()

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/extension/info"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

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
    # Diff Settings Convenience Methods
    # =========================================================================

    def test_save_diff_settings(self) -> None:
        """Test save_diff_settings method."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response
        data: JsonDict = {
            "key": "value",
        }

        response: Response = self.api.save_diff_settings(data, name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_put.assert_called_once_with(
            f"{self.api.rest_api_url}/settings/diff/names/Custom/content",
            data=data,
            params={"scope": "project/test"},
        )

    def test_delete_diff_settings(self) -> None:
        """Test delete_diff_settings method."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_diff_settings("Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/settings/diff/names/Custom",
            params={"scope": "project/test"},
        )

    def test_get_diff_settings(self) -> None:
        """Test get_diff_settings method."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_diff_settings(name="Custom", scope="project/test")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/settings/diff/names/Custom/content",
            params={"scope": "project/test"},
        )


if __name__ == "__main__":
    unittest.main()
