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

    def test_get_baselines(self) -> None:
        """Test get list of baselines for the given project."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_baselines(project_id="project1")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "projectId": "project1",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/baselines",
            params=expected_params,
        )

    def test_get_work_item_types(self) -> None:
        """Test get list of work item types for the given project."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_work_item_types(project_id="project1")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "projectId": "project1",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/work-item-types",
            params=expected_params,
        )

    def test_get_document_types(self) -> None:
        """Test get list of document types for the given project."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_document_types(project_id="project1")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "projectId": "project1",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/document-types",
            params=expected_params,
        )

    def test_get_link_roles(self) -> None:
        """Test get list of work item link roles for the given project."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_link_roles(project_id="project1")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "projectId": "project1",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/link-roles",
            params=expected_params,
        )

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

    def test_start_scan_job(self) -> None:
        """Test start an asynchronous scan job."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        scan_params: JsonDict = {
            "projectId": "project1",
            "entityType": "workitem",
        }
        response: Response = self.api.start_scan_job(scan_params=scan_params)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/scan/jobs",
            data=scan_params,
        )

    def test_get_scan_job_status(self) -> None:
        """Test get scan job status without following the redirect."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_scan_job_status(job_id="job-123")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/scan/jobs/job-123",
            allow_redirects=False,
        )

    def test_get_scan_job_result(self) -> None:
        """Test get scan job result."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_scan_job_result(job_id="job-123")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/scan/jobs/job-123/result",
        )

    def test_stop_scan_job(self) -> None:
        """Test stop a running scan job."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.stop_scan_job(job_id="job-123")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/scan/jobs/job-123/stop",
        )

    def test_start_repair_job(self) -> None:
        """Test start an asynchronous repair job."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        repair_params: JsonDict = {
            "projectId": "project1",
            "entityType": "workitem",
            "repairerId": "repairer1",
        }
        response: Response = self.api.start_repair_job(repair_params=repair_params)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/repair/jobs",
            data=repair_params,
        )

    def test_get_repair_job_status(self) -> None:
        """Test get repair job status without following the redirect."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_repair_job_status(job_id="job-123")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/repair/jobs/job-123",
            allow_redirects=False,
        )

    def test_get_repair_job_result(self) -> None:
        """Test get repair job result."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_repair_job_result(job_id="job-123")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/repair/jobs/job-123/result",
        )

    def test_list_entities(self) -> None:
        """Test list_entities without the optional subtype."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.list_entities(project_id="project1", entity_type="WORKITEM")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "projectId": "project1",
            "entityType": "WORKITEM",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/entities",
            params=expected_params,
        )

    def test_list_entities_with_subtype(self) -> None:
        """Test list_entities narrowed by subtype."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.list_entities(project_id="project1", entity_type="WORKITEM", entity_subtype="task")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "projectId": "project1",
            "entityType": "WORKITEM",
            "entitySubtype": "task",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/entities",
            params=expected_params,
        )

    def test_get_roles_without_scope(self) -> None:
        """Test get_roles from RolesMixin without scope."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_roles()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/roles",
            params=None,
        )

    def test_get_roles_with_scope(self) -> None:
        """Test get_roles from RolesMixin with scope."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_roles(scope="project/project1/")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/roles",
            params={"scope": "project/project1/"},
        )
