"""Unit tests for TempProject."""

from __future__ import annotations

import unittest
from http import HTTPStatus
from pathlib import Path
from unittest.mock import Mock, patch

from python_sbb_polarion.testing.temp_project import TempProject
from python_sbb_polarion.types import Header, MediaType


class TestTempProject(unittest.TestCase):
    """Test TempProject class."""

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_generates_unique_project_id(self, mock_uuid: Mock, mock_create_api: Mock) -> None:
        """Test __init__ generates project ID with UUID suffix."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="12345678-1234-1234-1234-123456789abc")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.text = "Success"

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response
        mock_create_api.return_value = mock_admin_api

        # Act
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertEqual(temp_project.temp_project_id, "TEST_st_123456789abc")
        self.assertEqual(temp_project.temp_project_name, "Test Project")
        self.assertEqual(temp_project.temp_project_template_id, "template_id")

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_calls_create_temp_project(self, mock_uuid: Mock, mock_create_api: Mock) -> None:
        """Test __init__ calls _create_temp_project."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="uuid-suffix")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response
        mock_create_api.return_value = mock_admin_api

        # Act
        _temp_project = TempProject("PROJ", "Project Name", "template")

        # Assert
        mock_admin_api.create_project.assert_called_once_with(project_id="PROJ_st_suffix", project_name="Project Name", template_id="template")

    def test_get_temp_project_id(self) -> None:
        """Test get_temp_project_id returns project ID."""
        # Arrange
        with patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api") as mock_create_api, patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid-suffix")

            mock_response = Mock()
            mock_response.status_code = HTTPStatus.OK

            mock_admin_api = Mock()
            mock_admin_api.create_project.return_value = mock_response
            mock_create_api.return_value = mock_admin_api

            temp_project = TempProject("ID", "Name", "template")

            # Act
            result: str = temp_project.get_temp_project_id()

            # Assert
            self.assertEqual(result, "ID_st_suffix")

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.temp_project.time.time")
    def test_create_temp_project_success(self, mock_time: Mock, mock_uuid: Mock, mock_create_api: Mock) -> None:
        """Test _create_temp_project with successful creation (200)."""
        # Arrange
        mock_time.return_value = 1000.0
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="uuid-suffix")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.text = "Project created"

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response
        mock_create_api.return_value = mock_admin_api

        # Act
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertIsNotNone(temp_project.temp_project_id)
        mock_admin_api.create_project.assert_called_once()

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_already_exists(self, mock_uuid: Mock, mock_create_api: Mock) -> None:
        """Test _create_temp_project when project already exists (400)."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="existing-uuid")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.BAD_REQUEST
        # UUID is "existing-uuid", split gives ["existing", "uuid"], [-1] gives "uuid"
        mock_response.text = "Project id 'TEST_st_uuid' clashes with existing project id 'TEST_st_uuid'."

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response
        mock_create_api.return_value = mock_admin_api

        # Act - should not raise exception
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertIsNotNone(temp_project.temp_project_id)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.temp_project.sys.exit")
    def test_create_temp_project_error(self, mock_exit: Mock, mock_uuid: Mock, mock_create_api: Mock) -> None:
        """Test _create_temp_project error handling with sys.exit."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="error-uuid")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_response.text = "Internal Server Error"
        mock_response.headers = {Header.CONTENT_TYPE: MediaType.JSON}
        mock_response.content = b"Error content"

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response
        mock_create_api.return_value = mock_admin_api

        # Act
        TempProject("TEST", "Test Project", "template_id")

        # Assert
        mock_exit.assert_called_once_with(-1)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_400_different_error(self, mock_uuid: Mock, mock_create_api: Mock) -> None:
        """Test _create_temp_project with 400 status but different error message."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="error-uuid")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.BAD_REQUEST
        mock_response.text = "Different error message"
        mock_response.headers = {Header.CONTENT_TYPE: MediaType.JSON}
        mock_response.content = b"Error content"

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response
        mock_create_api.return_value = mock_admin_api

        # Act & Assert
        with patch("python_sbb_polarion.testing.temp_project.sys.exit") as mock_exit:
            TempProject("TEST", "Test Project", "template_id")
            mock_exit.assert_called_once_with(-1)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.time.time")
    def test_tear_down_success(self, mock_time: Mock, mock_create_api: Mock) -> None:
        """Test tear_down with successful deletion (204)."""
        # Arrange
        mock_time.return_value = 1000.0

        # Setup for __init__
        mock_create_response = Mock()
        mock_create_response.status_code = HTTPStatus.OK

        # Setup for tear_down
        mock_delete_response = Mock()
        mock_delete_response.status_code = HTTPStatus.NO_CONTENT

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_create_response
        mock_admin_api.delete_project.return_value = mock_delete_response
        mock_create_api.return_value = mock_admin_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # Act
            temp_project.tear_down()

            # Assert
            mock_admin_api.delete_project.assert_called_once_with(project_id="TEST_st_uuid")

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.sys.exit")
    def test_tear_down_error(self, mock_exit: Mock, mock_create_api: Mock) -> None:
        """Test tear_down error handling with sys.exit."""
        # Arrange
        # Setup for __init__
        mock_create_response = Mock()
        mock_create_response.status_code = HTTPStatus.OK

        # Setup for tear_down
        mock_delete_response = Mock()
        mock_delete_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_delete_response.headers = {Header.CONTENT_TYPE: MediaType.JSON}
        mock_delete_response.content = b"Error content"

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_create_response
        mock_admin_api.delete_project.return_value = mock_delete_response
        mock_create_api.return_value = mock_admin_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # Act
            temp_project.tear_down()

            # Assert
            mock_exit.assert_called_once_with(-1)

    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=False)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.project_template_uploader.sys.exit")
    def test_upload_project_template_file_not_exists(self, mock_exit: Mock, mock_uuid: Mock, mock_create_api: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template exits when file does not exist."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        mock_admin_api = Mock()
        mock_create_api.return_value = mock_admin_api

        # Make sys.exit raise SystemExit to stop execution
        mock_exit.side_effect = SystemExit

        # Act & Assert
        with self.assertRaises(SystemExit):
            TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/nonexistent"))

        mock_exit.assert_called_with(1)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_no_location(self, mock_uuid: Mock, mock_create_api: Mock) -> None:
        """Test _upload_project_template returns early when location is None."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response
        mock_create_api.return_value = mock_admin_api

        # Act - template_location defaults to None
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert - should not crash, project should be created
        self.assertIsNotNone(temp_project.temp_project_id)
        mock_admin_api.create_project.assert_called_once()

    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=True)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_hash_match(self, mock_uuid: Mock, mock_create_api: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template skips upload when hash matches."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK

        test_hash: str = "abc123hash"
        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=test_hash)

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response

        def create_api_side_effect(extension_name: str) -> Mock:
            if extension_name == "test-data":
                return mock_test_data_api
            return mock_admin_api

        mock_create_api.side_effect = create_api_side_effect

        # Act
        with patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.calculate_folder_hash", return_value=test_hash):
            temp_project = TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/template"))

        # Assert
        mock_test_data_api.save_project_template.assert_not_called()
        self.assertIsNotNone(temp_project.temp_project_id)

    @patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.zip_folder")
    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=True)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_hash_differs(
        self,
        mock_uuid: Mock,
        mock_create_api: Mock,
        mock_exists: Mock,
        mock_zip_folder: Mock,  # This parameter name matches the decorator
    ) -> None:
        """Test _upload_project_template uploads when hash differs."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK

        # Configure zip_folder mock to return a fake zip path
        mock_zip_folder.return_value = Path("/tmp/fake_template.zip")

        local_hash: str = "abc123hash"
        remote_hash: str = "differenthash"
        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=remote_hash)
        mock_test_data_api.save_project_template.return_value = Mock(status_code=HTTPStatus.CREATED)

        mock_admin_api = Mock()
        mock_admin_api.create_project.return_value = mock_response

        def create_api_side_effect(extension_name: str) -> Mock:
            if extension_name == "test-data":
                return mock_test_data_api
            return mock_admin_api

        mock_create_api.side_effect = create_api_side_effect

        # Act
        with patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.calculate_folder_hash", return_value=local_hash), patch.object(Path, "exists", return_value=True), patch.object(Path, "unlink"):
            temp_project = TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/template"))

        # Assert
        mock_test_data_api.get_template_hash.assert_called_once_with(template_id="template_id")
        mock_test_data_api.save_project_template.assert_called_once()
        mock_zip_folder.assert_called_once_with(Path("/tmp/template"))

    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=True)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.project_template_uploader.sys.exit")
    def test_upload_project_template_upload_fails(self, mock_exit: Mock, mock_uuid: Mock, mock_create_api: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template exits when upload fails."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        local_hash: str = "abc123hash"
        remote_hash: str = "differenthash"

        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=remote_hash)
        mock_test_data_api.save_project_template.return_value = Mock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        mock_create_api.return_value = mock_test_data_api

        # Make sys.exit raise SystemExit to stop execution
        mock_exit.side_effect = SystemExit

        # Act & Assert
        with patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.calculate_folder_hash", return_value=local_hash):
            with self.assertRaises(SystemExit):
                TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/template"))

            mock_exit.assert_called_with(1)


if __name__ == "__main__":
    unittest.main()
