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
    # Project Operations
    # =========================================================================

    def test_create_project(self) -> None:
        """Test create project."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_project("PROJ", "Test Project", "template1")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {"projectId": "PROJ", "projectName": "Test Project", "templateId": "template1"}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects", data=expected_data)

    def test_create_test_run_template(self) -> None:
        """Test create test run template."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_test_run_template("PROJ", "template1")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {"templateId": "template1"}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/test-run-templates", data=expected_data)

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

    def test_create_document(self) -> None:
        """Test create module."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_document("PROJ", "space1", "module1", MediaType.XML, "<content>")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.CONTENT_TYPE: MediaType.XML}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/module1", headers=expected_headers, payload="<content>")

    def test_delete_document(self) -> None:
        """Test delete module."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_document("PROJ", "space1", "module1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/documents/module1")

    # =========================================================================
    # Collection Operations
    # =========================================================================

    def test_delete_collection(self) -> None:
        """Test delete collection."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_collection("PROJ", "collection1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/collections/collection1")

    def test_add_to_collection(self) -> None:
        """Test add to collection."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.add_to_collection("PROJ", "collection1", "module1")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {"moduleId": "module1"}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/collections/collection1/modules", data=expected_data)

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
    # Live Reports - Project
    # =========================================================================

    def test_create_live_report_with_project(self) -> None:
        """Test create live report with project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_live_report("PROJ", "space1", "report1", MediaType.XML, "<content>")

        self.assertEqual(response, mock_response)
        expected_headers: dict[str, str] = {Header.CONTENT_TYPE: MediaType.XML}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/report/report1", headers=expected_headers, payload="<content>")

    def test_delete_live_report_with_project(self) -> None:
        """Test delete live report with project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_live_report("PROJ", "space1", "report1")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/spaces/space1/report/report1")

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
    # Collection Creation
    # =========================================================================

    def test_create_collection(self) -> None:
        """Test create collection."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        response: Response = self.api.create_collection("PROJ", "collection1")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {"collectionName": "collection1"}
        self.mock_connection.api_request_post.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/collections", data=expected_data)

    # =========================================================================
    # Project Get/Delete
    # =========================================================================

    def test_get_project(self) -> None:
        """Test get project."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_project("PROJ")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ")

    def test_delete_project(self) -> None:
        """Test delete project."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_project("PROJ")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ")

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def test_set_custom_field_type_minimal(self) -> None:
        """Test set custom field type with minimal parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response

        response: Response = self.api.set_custom_field_type("field1", "Field 1", "string")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {
            "workItemType": None,
            "customFields": [{"id": "field1", "name": "Field 1", "type": "string", "description": None, "isRequired": False}],
        }
        self.mock_connection.api_request_put.assert_called_once_with(f"{self.api.rest_api_url}/custom-fields", data=expected_data)

    def test_set_custom_field_type_full(self) -> None:
        """Test set custom field type with all parameters."""
        mock_response = Mock()
        self.mock_connection.api_request_put.return_value = mock_response

        response: Response = self.api.set_custom_field_type("field1", "Field 1", "string", field_description="Test field", is_required=True, project_id="PROJ", work_item_type="task")

        self.assertEqual(response, mock_response)
        expected_data: JsonDict = {
            "workItemType": "task",
            "customFields": [{"id": "field1", "name": "Field 1", "type": "string", "description": "Test field", "isRequired": True}],
        }
        self.mock_connection.api_request_put.assert_called_once_with(f"{self.api.rest_api_url}/projects/PROJ/custom-fields", data=expected_data)

    # =========================================================================
    # Field Declarations
    # =========================================================================

    def test_get_custom_field_declarations_without_project(self) -> None:
        """Test get field declarations without project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_custom_field_declarations("workitem", "task")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/custom-fields/workitem/task",
            params=None,
        )

    def test_get_custom_field_declarations_with_project(self) -> None:
        """Test get field declarations with project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_get.return_value = mock_response

        response: Response = self.api.get_custom_field_declarations("workitem", "task", project_id="PROJ")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_get.assert_called_once_with(
            f"{self.api.rest_api_url}/custom-fields/workitem/task",
            params={"projectId": "PROJ"},
        )

    def test_declare_custom_field_without_project(self) -> None:
        """Test declare field without project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        data: JsonDict = {
            "id": "custom_field",
            "name": "Custom Field",
            "type": "string",
        }
        response: Response = self.api.declare_custom_field("workitem", "task", data)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/custom-fields/workitem/task",
            params=None,
            data=data,
        )

    def test_declare_custom_field_with_project(self) -> None:
        """Test declare field with project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        data: JsonDict = {
            "id": "custom_field",
            "name": "Custom Field",
            "type": "string",
        }
        response: Response = self.api.declare_custom_field("workitem", "task", data, project_id="PROJ")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/custom-fields/workitem/task",
            params={"projectId": "PROJ"},
            data=data,
        )

    def test_delete_custom_field_declaration_without_project(self) -> None:
        """Test delete field declaration without project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_custom_field_declaration("workitem", "task", "custom_field")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/custom-fields/workitem/task/custom_field",
            params=None,
        )

    def test_delete_custom_field_declaration_with_project(self) -> None:
        """Test delete field declaration with project ID."""
        mock_response = Mock()
        self.mock_connection.api_request_delete.return_value = mock_response

        response: Response = self.api.delete_custom_field_declaration("workitem", "task", "custom_field", project_id="PROJ")

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_delete.assert_called_once_with(
            f"{self.api.rest_api_url}/custom-fields/workitem/task/custom_field",
            params={"projectId": "PROJ"},
        )

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
