"""Unit tests for Fake Services API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

from python_sbb_polarion.extensions.fake_services import PolarionFakeServicesApi


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionFakeServicesApi(unittest.TestCase):
    """Test PolarionFakeServicesApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionFakeServicesApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "fake-services")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Authentication
    # =========================================================================

    def test_authenticate(self) -> None:
        """Test authenticate to DMS."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.authenticate("user1", "pass123")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {
            "username": "user1",
            "password": "pass123",
        }
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/api/v1/auth",
            data=expected_data,
        )

    # =========================================================================
    # File Operations
    # =========================================================================

    def test_write_file_to_container(self) -> None:
        """Test write file to DMS container."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        file_content: bytes = b"PDF content here"
        response: Response = self.api.write_file_to_container(
            ticket="ticket123",
            type_param="document",
            parent_id="parent456",
            name="test.pdf",
            file=file_content,
        )

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {
            "OTCSTICKET": "ticket123",
        }
        expected_files: dict[str, tuple[Any, ...]] = {
            "type": ("type.txt", "document"),
            "parent_id": ("parent_id.txt", "parent456"),
            "name": ("name.txt", "test.pdf"),
            "file": ("file.pdf", file_content),
        }
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/api/v1/nodes",
            headers=expected_headers,
            files=expected_files,
        )

    def test_promote_version(self) -> None:
        """Test promote a version of a DMS node."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.promote_version(
            ticket="ticket123",
            node_id="node789",
            version="2.0",
        )

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {
            "OTCSTICKET": "ticket123",
        }
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/api/v2/nodes/node789/versions/2.0/promote",
            headers=expected_headers,
        )

    def test_write_new_file_version(self) -> None:
        """Test write a new file version."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        file_content: bytes = b"New version content"
        response: Response = self.api.write_new_file_version(
            ticket="ticket123",
            node_id="node789",
            add_major_version="true",
            file=file_content,
        )

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {
            "OTCSTICKET": "ticket123",
        }
        expected_files: dict[str, tuple[Any, ...]] = {
            "add_major_version": ("add_major_version.txt", "true"),
            "file": ("file.pdf", file_content),
        }
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/api/v1/nodes/node789/versions",
            headers=expected_headers,
            files=expected_files,
        )

    def test_run_web_report(self) -> None:
        """Test run a WebReport."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_output_from_webreport_node_execution(
            ticket="ticket123",
            node_id="node789",
            destination="dest1",
            name="report1",
            container_id="container456",
            filename="output.pdf",
        )

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {
            "OTCSTICKET": "ticket123",
        }
        expected_params: dict[str, str] = {
            "destination": "dest1",
            "name": "report1",
            "containerid": "container456",
            "filename": "output.pdf",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/api/v1/nodes/node789/output",
            headers=expected_headers,
            params=expected_params,
        )

    # =========================================================================
    # User Management
    # =========================================================================

    def test_get_dms_users(self) -> None:
        """Test get all DMS users."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_dms_users()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/users",
        )

    def test_add_dms_user(self) -> None:
        """Test add a new DMS user."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.add_dms_user("newuser", "newpass")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "username": "newuser",
            "password": "newpass",
        }
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/users",
            params=expected_params,
        )

    def test_delete_dms_user(self) -> None:
        """Test delete DMS user."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_dms_user("olduser")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/users/olduser",
        )

    # =========================================================================
    # Upload Management
    # =========================================================================

    def test_get_dms_uploads_without_ticket(self) -> None:
        """Test get all executed DMS uploads without ticket filter."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_dms_uploads()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/uploads",
            params=None,
        )

    def test_get_dms_uploads_with_ticket(self) -> None:
        """Test get executed DMS uploads filtered by ticket."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_dms_uploads(ticket="ticket123")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "ticket": "ticket123",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/uploads",
            params=expected_params,
        )

    def test_delete_dms_uploads_without_ticket(self) -> None:
        """Test delete all executed DMS uploads without ticket filter."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_dms_uploads()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/uploads",
            params=None,
        )

    def test_delete_dms_uploads_with_ticket(self) -> None:
        """Test delete executed DMS uploads filtered by ticket."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_dms_uploads(ticket="ticket123")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "ticket": "ticket123",
        }
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/uploads",
            params=expected_params,
        )

    # =========================================================================
    # Container Management
    # =========================================================================

    def test_get_dms_containers_without_ticket(self) -> None:
        """Test get all created DMS containers without ticket filter."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_dms_containers()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/containers",
            params=None,
        )

    def test_get_dms_containers_with_ticket(self) -> None:
        """Test get created DMS containers filtered by ticket."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_dms_containers(ticket="ticket123")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "ticket": "ticket123",
        }
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/containers",
            params=expected_params,
        )

    def test_delete_dms_containers_without_ticket(self) -> None:
        """Test delete all created DMS containers without ticket filter."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_dms_containers()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/containers",
            params=None,
        )

    def test_delete_dms_containers_with_ticket(self) -> None:
        """Test delete created DMS containers filtered by ticket."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_dms_containers(ticket="ticket123")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "ticket": "ticket123",
        }
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/containers",
            params=expected_params,
        )

    # =========================================================================
    # Ticket Management
    # =========================================================================

    def test_delete_tickets_without_ticket(self) -> None:
        """Test delete all tickets without ticket filter."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_tickets()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/tickets",
            params=None,
        )

    def test_delete_tickets_with_ticket(self) -> None:
        """Test delete specific ticket."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_tickets(ticket="ticket123")

        self.assertEqual(response, mock_response)
        expected_params: dict[str, str] = {
            "ticket": "ticket123",
        }
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/tickets",
            params=expected_params,
        )

    def test_get_dms_tickets(self) -> None:
        """Test get all DMS tickets."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_dms_tickets()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/tickets",
        )

    def test_get_dms_ticket_for_user_exists(self) -> None:
        """Test get DMS ticket for existing user."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "user1": "ticket123",
            "user2": "ticket456",
        }
        self.mock_connection.api_request_get.return_value = mock_response

        result: str | None = self.api.get_dms_ticket_for_user("user1")

        self.assertEqual(result, "ticket123")
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/tickets",
        )

    def test_get_dms_ticket_for_user_not_exists(self) -> None:
        """Test get DMS ticket for non-existing user returns None."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "user1": "ticket123",
            "user2": "ticket456",
        }
        self.mock_connection.api_request_get.return_value = mock_response

        result: str | None = self.api.get_dms_ticket_for_user("unknown_user")

        self.assertIsNone(result)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/tickets",
        )

    def test_get_dms_ticket_for_user_empty_response(self) -> None:
        """Test get DMS ticket for user when response is empty."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        self.mock_connection.api_request_get.return_value = mock_response

        result: str | None = self.api.get_dms_ticket_for_user("user1")

        self.assertIsNone(result)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/opentext/manage/tickets",
        )
