"""Unit tests for Cucumber API."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

from python_sbb_polarion.extensions.cucumber import PolarionCucumberApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionCucumberApi(unittest.TestCase):
    """Test PolarionCucumberApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionCucumberApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "cucumber")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Fields
    # =========================================================================

    def test_get_jira_fields(self) -> None:
        """Test get jira fields."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_jira_fields("PROJ")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON, "projectId": "PROJ"}
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/2/field", headers=expected_headers)

    # =========================================================================
    # Features
    # =========================================================================

    def test_save_feature(self) -> None:
        """Test save feature."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.save_feature("PROJ", "WI-123", "Test Feature", "Feature: Test")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {
            "projectId": "PROJ",
            "workItemId": "WI-123",
            "title": "Test Feature",
            "filename": "WI-123.feature",
            "content": "Feature: Test",
        }
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/feature", data=expected_data)

    def test_get_feature(self) -> None:
        """Test get feature."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_feature("PROJ", "WI-123")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/feature/PROJ/WI-123")

    # =========================================================================
    # Export
    # =========================================================================

    def test_export_test_with_keys(self) -> None:
        """Test export test with keys parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.export_test(keys="elibrary/EL-4;elibrary/EL-5")

        self.assertEqual(response, mock_response)
        expected_url: str = f"/polarion/{self.api.extension_name}/rest/raven/1.0/export/test"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.OCTET_STREAM}
        expected_params: dict[str, str] = {"fz": "true", "keys": "elibrary/EL-4;elibrary/EL-5"}
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, headers=expected_headers, params=expected_params)

    def test_export_test_with_filter_query(self) -> None:
        """Test export test with filter_query parameter."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.export_test(filter_query="type:requirement")

        self.assertEqual(response, mock_response)
        expected_url: str = f"/polarion/{self.api.extension_name}/rest/raven/1.0/export/test"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.OCTET_STREAM}
        expected_params: dict[str, str] = {"fz": "true", "keys": "type:requirement"}
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, headers=expected_headers, params=expected_params)

    def test_export_test_with_fz_false(self) -> None:
        """Test export test with fz=False."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.export_test(keys="EL-1", fz=False)

        self.assertEqual(response, mock_response)
        expected_url: str = f"/polarion/{self.api.extension_name}/rest/raven/1.0/export/test"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.OCTET_STREAM}
        expected_params: dict[str, str] = {"fz": "false", "keys": "EL-1"}
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, headers=expected_headers, params=expected_params)

    def test_export_test_without_keys_and_filter(self) -> None:
        """Test export test without keys and filter_query."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.export_test()

        self.assertEqual(response, mock_response)
        expected_url: str = f"/polarion/{self.api.extension_name}/rest/raven/1.0/export/test"
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.OCTET_STREAM}
        expected_params: dict[str, str] = {"fz": "true"}
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, headers=expected_headers, params=expected_params)

    # =========================================================================
    # Import
    # =========================================================================

    def test_import_cucumber_test_results_multipart(self) -> None:
        """Test import cucumber test results multipart."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        # Create temporary files
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w", suffix=".json", delete=False) as info_file, tempfile.NamedTemporaryFile(encoding="utf-8", mode="w", suffix=".json", delete=False) as result_file:
            info_file.write('{"projectKey": "PROJ"}')
            result_file.write('[{"feature": "test"}]')
            info_path: str = info_file.name
            result_path: str = result_file.name

        try:
            response: Response = self.api.import_cucumber_test_results_multipart(info_path, result_path)

            self.assertEqual(response, mock_response)
            expected_url: str = f"/polarion/{self.api.extension_name}/rest/raven/1.0/import/execution/cucumber/multipart"
            expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON}
            self.mock_connection.api_request_post.assert_called_once()
            call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
            self.assertEqual(call_args[0][0], expected_url)
            self.assertEqual(call_args[1]["headers"], expected_headers)
            self.assertIn("files", call_args[1])
        finally:
            Path(info_path).unlink()
            Path(result_path).unlink()

    def test_import_junit_test_results(self) -> None:
        """Test import JUnit test results."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        # Create temporary file
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w", suffix=".json", delete=False) as result_file:
            result_file.write("<testsuite></testsuite>")
            result_path: str = result_file.name

        try:
            parameters: JsonDict = {"projectKey": "PROJ", "testPlanKey": "TP-1"}
            response: Response = self.api.import_junit_test_results(parameters, result_path)

            self.assertEqual(response, mock_response)
            expected_url: str = f"/polarion/{self.api.extension_name}/rest/raven/1.0/import/execution/junit"
            expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON}
            expected_params: dict[str, str] = {"projectKey": "PROJ", "testPlanKey": "TP-1"}
            self.mock_connection.api_request_post.assert_called_once()
            call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
            self.assertEqual(call_args[0][0], expected_url)
            self.assertEqual(call_args[1]["headers"], expected_headers)
            self.assertEqual(call_args[1]["params"], expected_params)
            self.assertIn("files", call_args[1])
        finally:
            Path(result_path).unlink()

    def test_import_junit_test_results_multipart(self) -> None:
        """Test import JUnit test results multipart."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        # Create temporary files
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w", suffix=".json", delete=False) as info_file, tempfile.NamedTemporaryFile(encoding="utf-8", mode="w", suffix=".json", delete=False) as result_file:
            info_file.write('{"projectKey": "PROJ"}')
            result_file.write("<testsuite></testsuite>")
            info_path: str = info_file.name
            result_path: str = result_file.name

        try:
            response: Response = self.api.import_junit_test_results_multipart(info_path, result_path)

            self.assertEqual(response, mock_response)
            expected_url: str = f"/polarion/{self.api.extension_name}/rest/raven/1.0/import/execution/junit/multipart"
            expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.JSON}
            self.mock_connection.api_request_post.assert_called_once()
            call_args: tuple[Any, ...] = self.mock_connection.api_request_post.call_args
            self.assertEqual(call_args[0][0], expected_url)
            self.assertEqual(call_args[1]["headers"], expected_headers)
            self.assertIn("files", call_args[1])
        finally:
            Path(info_path).unlink()
            Path(result_path).unlink()
