"""Unit tests for Admin Utility API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.admin_utility import PolarionAdminUtilityApi
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionAdminUtilityApi(unittest.TestCase):
    """Test PolarionAdminUtilityApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionAdminUtilityApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "admin-utility")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    # =========================================================================
    # Tokens
    # =========================================================================

    def test_create_token(self) -> None:
        """Test create token."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_token("token1", "2024-12-31")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {"name": "token1", "expiresOn": "2024-12-31"}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/tokens", data=expected_data)

    def test_delete_all_tokens(self) -> None:
        """Test delete all tokens."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_all_tokens()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/tokens")

    def test_delete_token(self) -> None:
        """Test delete token."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_token("token-id-123")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/tokens/token-id-123")

    # =========================================================================
    # License
    # =========================================================================

    def test_activate_trial_license(self) -> None:
        """Test activate trial license."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.activate_trial_license()

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/licenses/trial/activation")

    # =========================================================================
    # Module Operations
    # =========================================================================

    def test_delete_document(self) -> None:
        """Test delete module."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_document("PROJ", "space1", "module1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/module1")

    # =========================================================================
    # Wiki Pages - Project
    # =========================================================================

    def test_create_wiki_page_with_project(self) -> None:
        """Test create wiki page with project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_wiki_page("PROJ", "space1", "page1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/wiki/page1")

    def test_delete_wiki_page_with_project(self) -> None:
        """Test delete wiki page with project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_wiki_page("PROJ", "space1", "page1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/wiki/page1")

    # =========================================================================
    # Wiki Pages - Global Repository
    # =========================================================================

    def test_create_wiki_page_without_project(self) -> None:
        """Test create wiki page without project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_wiki_page_in_global_repo("space1", "page1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/spaces/space1/wiki/page1")

    def test_delete_wiki_page_without_project(self) -> None:
        """Test delete wiki page without project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_wiki_page_in_global_repo("space1", "page1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/spaces/space1/wiki/page1")

    # =========================================================================
    # Live Reports - Default Space
    # =========================================================================

    def test_create_live_report_without_project(self) -> None:
        """Test create live report without project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_live_report_in_default_space("space1", "report1", MediaType.XML, "<content>")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.CONTENT_TYPE: MediaType.XML}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/spaces/space1/report/report1", headers=expected_headers, payload="<content>")

    def test_delete_live_report_without_project(self) -> None:
        """Test delete live report without project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_live_report_in_default_space("space1", "report1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/spaces/space1/report/report1")

    # =========================================================================
    # Document Types Configuration
    # =========================================================================

    def test_get_document_types_configuration(self) -> None:
        """Test get document types configuration."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_document_types_configuration("PROJ")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.XML}
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/document-types-config", headers=expected_headers)

    def test_get_document_custom_fields_configuration(self) -> None:
        """Test get document custom fields configuration."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_document_custom_fields_configuration("PROJ", "req")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.XML}
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/document-custom-fields-config/req", headers=expected_headers)

    def test_set_document_custom_fields_configuration(self) -> None:
        """Test set document custom fields configuration."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.set_document_custom_fields_configuration("PROJ", "req", "<config>")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.CONTENT_TYPE: MediaType.XML}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/document-custom-fields-config/req", headers=expected_headers, payload="<config>")

    # =========================================================================
    # Workitem Custom Fields Configuration
    # =========================================================================

    def test_get_workitem_custom_fields_configuration(self) -> None:
        """Test get workitem custom fields configuration."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_workitem_custom_fields_configuration("PROJ", "task")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.ACCEPT: MediaType.XML}
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/projects/PROJ/workitem-custom-fields-config/task",
            headers=expected_headers,
        )

    def test_set_workitem_custom_fields_configuration(self) -> None:
        """Test set workitem custom fields configuration."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.set_workitem_custom_fields_configuration("PROJ", "task", "<config>")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.CONTENT_TYPE: MediaType.XML}
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/projects/PROJ/workitem-custom-fields-config/task",
            headers=expected_headers,
            payload="<config>",
        )

    # =========================================================================
    # Vault Operations
    # =========================================================================

    def test_create_vault_record(self) -> None:
        """Test create vault record."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_vault_record("my-key", "my-user", "my-password")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {
            "key": "my-key",
            "user": "my-user",
            "password": "my-password",
        }
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/vault",
            data=expected_data,
        )

    def test_get_vault_record(self) -> None:
        """Test get vault record."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_vault_record("my-key")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/vault/my-key",
        )

    def test_delete_vault_record(self) -> None:
        """Test delete vault record."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_vault_record("my-key")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/vault/my-key",
        )
