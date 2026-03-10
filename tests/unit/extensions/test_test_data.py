"""Unit tests for Test Data API."""

from __future__ import annotations

import tempfile
import unittest
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.test_data import PolarionTestDataApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from typing import Any

    from requests import Response


class TestPolarionTestDataApi(unittest.TestCase):
    """Test PolarionTestDataApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionTestDataApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "test-data")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Document Operations
    # =========================================================================

    def test_create_document_with_generated_workitems_without_quantity(self) -> None:
        """Test create document without quantity parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_document_with_generated_workitems("PROJ", "space1", "doc1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, params=None)

    def test_create_document_with_generated_workitems_with_quantity(self) -> None:
        """Test create document with quantity parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_document_with_generated_workitems("PROJ", "space1", "doc1", quantity=10)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, params={"quantity": "10"})

    def test_extend_document_with_generated_workitems_without_quantity(self) -> None:
        """Test extend document without quantity parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_patch.return_value = mock_response

        response: Response = self.api.extend_document_with_generated_workitems("PROJ", "space1", "doc1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1/append"
        self.mock_connection.api_request_patch.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, params=None)

    def test_extend_document_with_generated_workitems_with_quantity(self) -> None:
        """Test extend document with quantity parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_patch.return_value = mock_response

        response: Response = self.api.extend_document_with_generated_workitems("PROJ", "space1", "doc1", quantity=5)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1/append"
        self.mock_connection.api_request_patch.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, params={"quantity": "5"})

    def test_change_document_work_item_descriptions_without_interval(self) -> None:
        """Test change descriptions without interval parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_patch.return_value = mock_response

        response: Response = self.api.change_document_work_item_descriptions("PROJ", "space1", "doc1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1/change-wi-descriptions"
        self.mock_connection.api_request_patch.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, params=None)

    def test_change_document_work_item_descriptions_with_interval(self) -> None:
        """Test change descriptions with interval parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_patch.return_value = mock_response

        response: Response = self.api.change_document_work_item_descriptions("PROJ", "space1", "doc1", interval=HTTPStatus.CONTINUE)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/doc1/change-wi-descriptions"
        self.mock_connection.api_request_patch.assert_called_once_with(expected_url, headers={Header.ACCEPT: MediaType.PLAIN}, params={"interval": "100"})

    # =========================================================================
    # Template Operations
    # =========================================================================

    def test_get_template_hash_success(self) -> None:
        """Test get template hash with valid template ID."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_template_hash("template1")

        self.assertEqual(response, mock_response)
        expected_endpoint: str = f"{self.api.rest_api_url}/templates/template1/hash"
        self.mock_connection.api_request_get.assert_called_once_with(expected_endpoint, headers={Header.ACCEPT: MediaType.PLAIN})

    def test_get_template_hash_empty_id(self) -> None:
        """Test get template hash with empty template ID."""
        with self.assertRaises(ValueError) as context:
            self.api.get_template_hash("")

        self.assertIn("cannot be null or empty", str(context.exception))

    def test_get_template_hash_whitespace_id(self) -> None:
        """Test get template hash with whitespace-only template ID."""
        with self.assertRaises(ValueError) as context:
            self.api.get_template_hash("   ")

        self.assertIn("cannot be null or empty", str(context.exception))

    def test_save_project_template_success(self) -> None:
        """Test save project template with valid file."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".zip", delete=False) as tmp_file:
            tmp_file.write(b"test zip content")
            tmp_file_path: Path = Path(tmp_file.name)

        try:
            response: Response = self.api.save_project_template("template1", tmp_file_path, "hash123")

            self.assertEqual(response, mock_response)
            expected_endpoint: str = f"{self.api.rest_api_url}/templates/template1/hash123"
            self.mock_connection.api_request_post.assert_called_once()
            call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
            self.assertEqual(call_args[0][0], expected_endpoint)
            self.assertIn("files", call_args[1])
            self.assertEqual(call_args[1]["headers"], {Header.ACCEPT: MediaType.JSON})
        finally:
            # Cleanup
            tmp_file_path.unlink()

    def test_save_project_template_file_not_found(self) -> None:
        """Test save project template with non-existent file."""
        with self.assertRaises(FileNotFoundError) as context:
            self.api.save_project_template("template1", Path("/non/existent/file.zip"), "hash123")

        self.assertIn("File not found", str(context.exception))

    def test_download_project_template_success(self) -> None:
        """Test download project template with valid project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.download_project_template("project1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"/{self.api.rest_api_url}/templates/project1/download"
        self.mock_connection.api_request_get.assert_called_once_with(
            expected_url,
            headers={Header.ACCEPT: MediaType.OCTET_STREAM},
            params=None,
        )

    def test_download_project_template_with_project_group(self) -> None:
        """Test download project template with project group parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.download_project_template("project1", project_group="group1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"/{self.api.rest_api_url}/templates/project1/download"
        self.mock_connection.api_request_get.assert_called_once_with(
            expected_url,
            headers={Header.ACCEPT: MediaType.OCTET_STREAM},
            params={"projectGroup": "group1"},
        )

    def test_download_project_template_empty_id(self) -> None:
        """Test download project template with empty project ID."""
        with self.assertRaises(ValueError) as context:
            self.api.download_project_template("")

        self.assertIn("cannot be null or empty", str(context.exception))

    def test_download_project_template_whitespace_id(self) -> None:
        """Test download project template with whitespace-only project ID."""
        with self.assertRaises(ValueError) as context:
            self.api.download_project_template("   ")

        self.assertIn("cannot be null or empty", str(context.exception))
