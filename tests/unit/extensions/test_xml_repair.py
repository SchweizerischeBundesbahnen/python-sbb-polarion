"""Unit tests for XML Repair API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.xml_repair import PolarionXmlRepairApi


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionXmlRepairApi(unittest.TestCase):
    """Test PolarionXmlRepairApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionXmlRepairApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "xml-repair")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Repair Operations
    # =========================================================================

    def test_get_repairers(self) -> None:
        """Test get list of repairers for specified entity type."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_repairers(entity_type="workitem")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "entityType": "workitem",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/repairers",
            params=expected_params,
        )

    def test_scan(self) -> None:
        """Test scan entities for XML issues."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        scan_params: JsonDict = {
            "projectId": "project1",
            "entityType": "workitem",
        }
        response: Response = self.api.scan(scan_params=scan_params)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/scan",
            data=scan_params,
        )

    def test_repair(self) -> None:
        """Test repair XML issues identified by scan."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        repair_params: JsonDict = {
            "projectId": "project1",
            "entityType": "workitem",
            "repairerId": "repairer1",
        }
        response: Response = self.api.repair(repair_params=repair_params)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/repair",
            data=repair_params,
        )
