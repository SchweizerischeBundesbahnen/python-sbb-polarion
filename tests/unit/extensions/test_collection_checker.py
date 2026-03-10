"""Unit tests for Collection Checker API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.collection_checker import PolarionCollectionCheckerApi, ReportFormat


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionCollectionCheckerApi(unittest.TestCase):
    """Test PolarionCollectionCheckerApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionCollectionCheckerApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "collection-checker")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Checks
    # =========================================================================

    def test_get_checks_default_params(self) -> None:
        """Test get checks with default parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_checks("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/checks"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"daysInterval": "1", "page": "1", "count": "20"})

    def test_get_checks_custom_params(self) -> None:
        """Test get checks with custom parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_checks("PROJ", days_interval=7, page=2, count=50)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/checks"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"daysInterval": "7", "page": "2", "count": "50"})

    def test_cancel_check(self) -> None:
        """Test cancel check."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.cancel_check("PROJ", "check123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/checks/check123/cancel"
        self.mock_connection.api_request_post.assert_called_once_with(expected_url)

    def test_get_check(self) -> None:
        """Test get single check."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_check("PROJ", "check123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/checks/check123"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_start_check_default_options(self) -> None:
        """Test start check with default options."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.start_check("PROJ", "coll1")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/collections/coll1/checks"
        expected_data: JsonDict = {
            "ignoreLinkRoles": None,
            "ignoreCopyingLinkRoles": None,
            "ignoreWorkItemIsContainedInMultipleRevisionsErrors": False,
            "ignoreLinkOutOfCollectionWithSpecificRevisionErrors": False,
        }
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=expected_data)

    def test_start_check_custom_options(self) -> None:
        """Test start check with custom options."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.start_check(
            "PROJ",
            "coll1",
            ignore_link_roles=["parent", "child"],
            ignore_copying_link_roles=["related"],
            ignore_multiple_revisions_errors=True,
            ignore_link_out_of_collection_errors=True,
        )

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/collections/coll1/checks"
        expected_data: JsonDict = {
            "ignoreLinkRoles": ["parent", "child"],
            "ignoreCopyingLinkRoles": ["related"],
            "ignoreWorkItemIsContainedInMultipleRevisionsErrors": True,
            "ignoreLinkOutOfCollectionWithSpecificRevisionErrors": True,
        }
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=expected_data)

    def test_start_check_partial_options(self) -> None:
        """Test start check with partial custom options."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.start_check("PROJ", "coll1", ignore_link_roles=["parent"], ignore_multiple_revisions_errors=True)

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/collections/coll1/checks"
        expected_data: JsonDict = {
            "ignoreLinkRoles": ["parent"],
            "ignoreCopyingLinkRoles": None,
            "ignoreWorkItemIsContainedInMultipleRevisionsErrors": True,
            "ignoreLinkOutOfCollectionWithSpecificRevisionErrors": False,
        }
        self.mock_connection.api_request_post.assert_called_once_with(expected_url, data=expected_data)

    def test_get_linkroles(self) -> None:
        """Test get project link roles."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_linkroles("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/linkroles"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)

    def test_get_check_json_report(self) -> None:
        """Test get check report in JSON format."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_check_json_report("PROJ", "check123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/checks/check123/report"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"format": ReportFormat.JSON})

    def test_get_check_text_log(self) -> None:
        """Test get check log as text."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_check_text_log("PROJ", "check123")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/checks/check123/report"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url, params={"format": ReportFormat.TXT})

    # =========================================================================
    # Collections
    # =========================================================================

    def test_get_collections(self) -> None:
        """Test get all collections."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_collections("PROJ")

        self.assertEqual(response, mock_response)
        expected_url: str = f"{self.api.rest_api_url}/projects/PROJ/collections"
        self.mock_connection.api_request_get.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
