"""Unit tests for TempProject."""

from __future__ import annotations

import unittest
from http import HTTPStatus
from pathlib import Path
from unittest.mock import Mock, patch

from python_sbb_polarion.testing.temp_project import TempProject


def _response(status_code: HTTPStatus) -> Mock:
    """Build a mock HTTP response with the given status code."""
    response: Mock = Mock()
    response.status_code = status_code
    return response


def _success_polarion_api() -> Mock:
    """Mock PolarionApiV1 for a successful create flow (not-exists -> create 202 -> ready -> name set)."""
    api: Mock = Mock()
    api.get_project.side_effect = [_response(HTTPStatus.NOT_FOUND), _response(HTTPStatus.OK)]
    api.create_project.return_value = _response(HTTPStatus.ACCEPTED)
    api.update_project.return_value = _response(HTTPStatus.NO_CONTENT)
    return api


class TestTempProject(unittest.TestCase):
    """Test TempProject class."""

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_generates_unique_project_id(self, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test __init__ generates project ID with UUID suffix."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="12345678-1234-1234-1234-123456789abc")
        mock_create_api.return_value = _success_polarion_api()

        # Act
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertEqual(temp_project.temp_project_id, "TEST_st_123456789abc")
        self.assertEqual(temp_project.temp_project_name, "Test Project")
        self.assertEqual(temp_project.temp_project_template_id, "template_id")

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_calls_create_project_with_template(self, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test __init__ creates the project from the template via the standard API."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="uuid-suffix")
        mock_api: Mock = _success_polarion_api()
        mock_create_api.return_value = mock_api

        # Act
        _temp_project = TempProject("PROJ", "Project Name", "template")

        # Assert
        mock_api.create_project.assert_called_once_with(
            {
                "projectId": "PROJ_st_suffix",
                "trackerPrefix": "PROJ_st_suffix",
                "location": "PROJ_st_suffix",
                "templateId": "template",
            }
        )

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_get_temp_project_id(self, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test get_temp_project_id returns project ID."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid-suffix")
        mock_create_api.return_value = _success_polarion_api()

        temp_project = TempProject("ID", "Name", "template")

        # Act
        result: str = temp_project.get_temp_project_id()

        # Assert
        self.assertEqual(result, "ID_st_suffix")

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_success(self, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test _create_temp_project with successful async creation (202 -> ready)."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="uuid-suffix")
        mock_api: Mock = _success_polarion_api()
        mock_create_api.return_value = mock_api

        # Act
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertIsNotNone(temp_project.temp_project_id)
        mock_api.create_project.assert_called_once()
        # name is set after the project becomes available
        mock_api.update_project.assert_called_once()

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_already_exists(self, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test _create_temp_project skips creation when the project already exists (pre-check 200)."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="existing-uuid")

        mock_api: Mock = Mock()
        mock_api.get_project.return_value = _response(HTTPStatus.OK)
        mock_create_api.return_value = mock_api

        # Act - should not raise and should not attempt creation
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertIsNotNone(temp_project.temp_project_id)
        mock_api.create_project.assert_not_called()

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.temp_project.sys.exit")
    def test_create_temp_project_create_error(self, mock_exit: Mock, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test _create_temp_project error handling when create returns a non-202 status."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="error-uuid")

        mock_api: Mock = Mock()
        mock_api.get_project.return_value = _response(HTTPStatus.NOT_FOUND)
        mock_api.create_project.return_value = _response(HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_create_api.return_value = mock_api

        # sys.exit raises SystemExit in production; make the mock stop execution too
        mock_exit.side_effect = SystemExit

        # Act & Assert
        with self.assertRaises(SystemExit):
            TempProject("TEST", "Test Project", "template_id")

        mock_exit.assert_called_once_with(-1)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.temp_project.time.sleep")
    @patch("python_sbb_polarion.testing.temp_project.sys.exit")
    def test_create_temp_project_readiness_timeout(self, mock_exit: Mock, mock_sleep: Mock, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test _create_temp_project exits when the project never becomes available."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="timeout-uuid")

        mock_api: Mock = Mock()
        # pre-check not-exists, then never becomes ready
        mock_api.get_project.return_value = _response(HTTPStatus.NOT_FOUND)
        mock_api.create_project.return_value = _response(HTTPStatus.ACCEPTED)
        mock_create_api.return_value = mock_api

        # sys.exit raises SystemExit in production; make the mock stop execution too
        mock_exit.side_effect = SystemExit

        # Act & Assert
        with self.assertRaises(SystemExit):
            TempProject("TEST", "Test Project", "template_id")

        mock_exit.assert_called_once_with(-1)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_sets_name(self, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test _create_temp_project sets the project name via update_project after creation."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="name-uuid")
        mock_api: Mock = _success_polarion_api()
        mock_create_api.return_value = mock_api

        # Act
        TempProject("TEST", "My Project", "template_id")

        # Assert
        expected_data: dict[str, object] = {
            "data": {
                "type": "projects",
                "id": "TEST_st_uuid",
                "attributes": {
                    "name": "My Project",
                },
            },
        }
        mock_api.update_project.assert_called_once_with("TEST_st_uuid", expected_data)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.temp_project.sys.exit")
    def test_create_temp_project_set_name_failure_does_not_exit(self, mock_exit: Mock, mock_uuid: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test name-setting failure is best-effort (warns, does not exit)."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="warn-uuid")

        mock_api: Mock = Mock()
        mock_api.get_project.side_effect = [_response(HTTPStatus.NOT_FOUND), _response(HTTPStatus.OK)]
        mock_api.create_project.return_value = _response(HTTPStatus.ACCEPTED)
        mock_api.update_project.return_value = _response(HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_create_api.return_value = mock_api

        # Act
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert - project created, name update failed but no exit
        self.assertIsNotNone(temp_project.temp_project_id)
        mock_exit.assert_not_called()

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    def test_tear_down_success(self, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test tear_down with successful async deletion (202 -> gone)."""
        # Arrange
        mock_api: Mock = Mock()
        # __init__: pre-check 404, ready 200; tear_down: gone 404
        mock_api.get_project.side_effect = [
            _response(HTTPStatus.NOT_FOUND),
            _response(HTTPStatus.OK),
            _response(HTTPStatus.NOT_FOUND),
        ]
        mock_api.create_project.return_value = _response(HTTPStatus.ACCEPTED)
        mock_api.update_project.return_value = _response(HTTPStatus.NO_CONTENT)
        mock_api.delete_project.return_value = _response(HTTPStatus.ACCEPTED)
        mock_create_api.return_value = mock_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # Act
            temp_project.tear_down()

            # Assert
            mock_api.delete_project.assert_called_once_with("TEST_st_uuid")

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.sys.exit")
    def test_tear_down_delete_error(self, mock_exit: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test tear_down error handling when delete returns a non-202 status."""
        # Arrange
        mock_api: Mock = Mock()
        mock_api.get_project.side_effect = [_response(HTTPStatus.NOT_FOUND), _response(HTTPStatus.OK)]
        mock_api.create_project.return_value = _response(HTTPStatus.ACCEPTED)
        mock_api.update_project.return_value = _response(HTTPStatus.NO_CONTENT)
        mock_api.delete_project.return_value = _response(HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_create_api.return_value = mock_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # sys.exit raises SystemExit in production; make the mock stop execution too
            mock_exit.side_effect = SystemExit

            # Act & Assert
            with self.assertRaises(SystemExit):
                temp_project.tear_down()

            mock_exit.assert_called_once_with(-1)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.time.sleep")
    @patch("python_sbb_polarion.testing.temp_project.sys.exit")
    def test_tear_down_deletion_timeout(self, mock_exit: Mock, mock_sleep: Mock, mock_create_api: Mock, mock_create_extension: Mock) -> None:
        """Test tear_down exits when the project is never removed."""
        # Arrange
        mock_api: Mock = Mock()
        # __init__: pre-check 404, ready 200; tear_down poll: always 200 (never gone)
        mock_api.get_project.side_effect = [
            _response(HTTPStatus.NOT_FOUND),
            *[_response(HTTPStatus.OK) for _ in range(200)],
        ]
        mock_api.create_project.return_value = _response(HTTPStatus.ACCEPTED)
        mock_api.update_project.return_value = _response(HTTPStatus.NO_CONTENT)
        mock_api.delete_project.return_value = _response(HTTPStatus.ACCEPTED)
        mock_create_api.return_value = mock_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # sys.exit raises SystemExit in production; make the mock stop execution too
            mock_exit.side_effect = SystemExit

            # Act & Assert
            with self.assertRaises(SystemExit):
                temp_project.tear_down()

            mock_exit.assert_called_once_with(-1)

    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=False)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.project_template_uploader.sys.exit")
    def test_upload_project_template_file_not_exists(self, mock_exit: Mock, mock_uuid: Mock, mock_create_extension: Mock, mock_create_polarion: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template exits when file does not exist."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")
        mock_create_extension.return_value = Mock()
        mock_create_polarion.return_value = _success_polarion_api()

        # Make sys.exit raise SystemExit to stop execution
        mock_exit.side_effect = SystemExit

        # Act & Assert
        with self.assertRaises(SystemExit):
            TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/nonexistent"))

        mock_exit.assert_called_with(1)

    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_no_location(self, mock_uuid: Mock, mock_create_polarion: Mock, mock_create_extension: Mock) -> None:
        """Test _upload_project_template returns early when location is None."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")
        mock_api: Mock = _success_polarion_api()
        mock_create_polarion.return_value = mock_api

        # Act - template_location defaults to None
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert - should not crash, project should be created
        self.assertIsNotNone(temp_project.temp_project_id)
        mock_api.create_project.assert_called_once()

    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=True)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_hash_match(self, mock_uuid: Mock, mock_create_extension: Mock, mock_create_polarion: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template skips upload when hash matches."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        test_hash: str = "abc123hash"
        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=test_hash)
        mock_create_extension.return_value = mock_test_data_api
        mock_create_polarion.return_value = _success_polarion_api()

        # Act
        with patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.calculate_folder_hash", return_value=test_hash):
            temp_project = TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/template"))

        # Assert
        mock_test_data_api.save_project_template.assert_not_called()
        self.assertIsNotNone(temp_project.temp_project_id)

    @patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.zip_folder")
    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=True)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_hash_differs(
        self,
        mock_uuid: Mock,
        mock_create_extension: Mock,
        mock_create_polarion: Mock,
        mock_exists: Mock,
        mock_zip_folder: Mock,
    ) -> None:
        """Test _upload_project_template uploads when hash differs."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        # Configure zip_folder mock to return a fake zip path
        mock_zip_folder.return_value = Path("/tmp/fake_template.zip")

        local_hash: str = "abc123hash"
        remote_hash: str = "differenthash"
        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=remote_hash)
        mock_test_data_api.save_project_template.return_value = Mock(status_code=HTTPStatus.CREATED)
        mock_create_extension.return_value = mock_test_data_api
        mock_create_polarion.return_value = _success_polarion_api()

        # Act
        with patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.calculate_folder_hash", return_value=local_hash), patch.object(Path, "exists", return_value=True), patch.object(Path, "unlink"):
            temp_project = TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/template"))

        # Assert
        mock_test_data_api.get_template_hash.assert_called_once_with(template_id="template_id")
        mock_test_data_api.save_project_template.assert_called_once()
        mock_zip_folder.assert_called_once_with(Path("/tmp/template"))
        self.assertIsNotNone(temp_project.temp_project_id)

    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=True)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_extension_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.project_template_uploader.sys.exit")
    def test_upload_project_template_upload_fails(self, mock_exit: Mock, mock_uuid: Mock, mock_create_extension: Mock, mock_create_polarion: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template exits when upload fails."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        local_hash: str = "abc123hash"
        remote_hash: str = "differenthash"

        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=remote_hash)
        mock_test_data_api.save_project_template.return_value = Mock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_create_extension.return_value = mock_test_data_api
        mock_create_polarion.return_value = _success_polarion_api()

        # Make sys.exit raise SystemExit to stop execution
        mock_exit.side_effect = SystemExit

        # Act & Assert
        with patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.calculate_folder_hash", return_value=local_hash):
            with self.assertRaises(SystemExit):
                TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/template"))

            mock_exit.assert_called_with(1)


if __name__ == "__main__":
    unittest.main()
