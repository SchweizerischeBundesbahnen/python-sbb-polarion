"""Unit tests for TempProject."""

from __future__ import annotations

import unittest
from http import HTTPStatus
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

from python_sbb_polarion.testing.errors import TempProjectError
from python_sbb_polarion.testing.temp_project import TempProject


def _response(status_code: HTTPStatus, json_body: Any = None) -> Mock:
    """Build a mock HTTP response with the given status code and JSON body."""
    response: Mock = Mock()
    response.status_code = status_code
    response.json.return_value = json_body
    return response


def _accepted_job(job_id: str = "job-1") -> Mock:
    """Build a 202 (Accepted) response whose body carries an async job descriptor."""
    return _response(HTTPStatus.ACCEPTED, {"data": {"type": "jobs", "id": job_id}})


def _job(status_type: str | None, message: str | None = None) -> Mock:
    """Build a GET /jobs/{id} response with the given terminal status type (None = still running)."""
    status: dict[str, Any] = {}
    if status_type is not None:
        status["type"] = status_type
    if message is not None:
        status["message"] = message
    return _response(HTTPStatus.OK, {"data": {"attributes": {"status": status}}})


def _success_polarion_api() -> Mock:
    """Mock PolarionApiV1 for a successful create flow (not-exists -> create 202 -> job OK -> name set)."""
    api: Mock = Mock()
    api.get_project.return_value = _response(HTTPStatus.NOT_FOUND)
    api.create_project.return_value = _accepted_job()
    api.get_job.return_value = _job("OK")
    api.update_project.return_value = _response(HTTPStatus.NO_CONTENT)
    api.delete_project.return_value = _accepted_job("del-job")
    return api


class TestTempProject(unittest.TestCase):
    """Test TempProject class."""

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_generates_unique_project_id(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
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

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_calls_create_project_with_template(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
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

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_nests_project_under_parent_location(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test parent_location nests the project under the given group folder (appending the project id)."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="uuid-suffix")
        mock_api: Mock = _success_polarion_api()
        mock_create_api.return_value = mock_api

        # Act - a trailing slash on the parent must not produce a doubled separator
        temp_project = TempProject("PROJ", "Project Name", "template", parent_location="Demo Projects/")

        # Assert
        self.assertEqual(temp_project.temp_project_location, "Demo Projects/PROJ_st_suffix")
        mock_api.create_project.assert_called_once_with(
            {
                "projectId": "PROJ_st_suffix",
                "trackerPrefix": "PROJ_st_suffix",
                "location": "Demo Projects/PROJ_st_suffix",
                "templateId": "template",
            }
        )

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_init_defaults_location_to_project_id(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test that without parent_location the project location stays the bare project id (root)."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="uuid-suffix")
        mock_create_api.return_value = _success_polarion_api()

        # Act
        temp_project = TempProject("PROJ", "Project Name", "template")

        # Assert
        self.assertEqual(temp_project.temp_project_location, "PROJ_st_suffix")

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_get_temp_project_id(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
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

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_success(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _create_temp_project with successful async creation (202 -> job OK)."""
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
        # the creation job is polled, then the name is set once it finishes
        mock_api.get_job.assert_called_with("job-1")
        mock_api.update_project.assert_called_once()

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_already_exists(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
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

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_create_error(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _create_temp_project raises when create returns a non-202 status."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="error-uuid")

        mock_api: Mock = Mock()
        mock_api.get_project.return_value = _response(HTTPStatus.NOT_FOUND)
        mock_api.create_project.return_value = _response(HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_create_api.return_value = mock_api

        # Act & Assert
        with self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id")

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_job_failed(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _create_temp_project raises when the creation job reports a FAILED status."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="failed-uuid")

        mock_api: Mock = Mock()
        mock_api.get_project.return_value = _response(HTTPStatus.NOT_FOUND)
        mock_api.create_project.return_value = _accepted_job()
        mock_api.get_job.return_value = _job("FAILED", "template broken")
        mock_create_api.return_value = mock_api

        # Act & Assert
        with self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id")

        # name is never set once the job failed
        mock_api.update_project.assert_not_called()

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.temp_project.time.sleep")
    def test_create_temp_project_job_timeout(self, mock_sleep: Mock, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _create_temp_project raises when the creation job never reaches a terminal status."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="timeout-uuid")

        mock_api: Mock = Mock()
        mock_api.get_project.return_value = _response(HTTPStatus.NOT_FOUND)
        mock_api.create_project.return_value = _accepted_job()
        # job stays in a non-terminal state forever
        mock_api.get_job.return_value = _job("UNKNOWN")
        mock_create_api.return_value = mock_api

        # Act & Assert
        with self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id")

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_unexpected_job_body(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _create_temp_project raises when the 202 response has no usable job id."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="nojob-uuid")

        mock_api: Mock = Mock()
        mock_api.get_project.return_value = _response(HTTPStatus.NOT_FOUND)
        mock_api.create_project.return_value = _response(HTTPStatus.ACCEPTED, {"unexpected": True})
        mock_create_api.return_value = mock_api

        # Act & Assert
        with self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id")

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_sets_name(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
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

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_set_name_failure_does_not_raise(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test name-setting failure is best-effort (warns, does not raise)."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="warn-uuid")

        mock_api: Mock = _success_polarion_api()
        mock_api.update_project.return_value = _response(HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_create_api.return_value = mock_api

        # Act - project is created, name update fails but is swallowed
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertIsNotNone(temp_project.temp_project_id)
        mock_api.update_project.assert_called_once()

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    def test_tear_down_success(self, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test tear_down with successful async deletion (202 -> job OK)."""
        # Arrange
        mock_api: Mock = _success_polarion_api()
        mock_create_api.return_value = mock_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # Act
            temp_project.tear_down()

            # Assert
            mock_api.delete_project.assert_called_once_with("TEST_st_uuid")
            mock_api.get_job.assert_called_with("del-job")

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    def test_tear_down_delete_error(self, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test tear_down raises when delete returns a non-202 status."""
        # Arrange
        mock_api: Mock = _success_polarion_api()
        mock_api.delete_project.return_value = _response(HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_create_api.return_value = mock_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # Act & Assert
            with self.assertRaises(TempProjectError):
                temp_project.tear_down()

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.time.sleep")
    def test_tear_down_deletion_timeout(self, mock_sleep: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test tear_down raises when the deletion job never reaches a terminal status."""
        # Arrange
        mock_api: Mock = _success_polarion_api()
        # creation job finishes (OK), deletion job never reaches a terminal status
        mock_api.get_job.side_effect = [_job("OK"), *[_job("UNKNOWN") for _ in range(200)]]
        mock_create_api.return_value = mock_api

        with patch("python_sbb_polarion.testing.temp_project.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = Mock()
            mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

            temp_project = TempProject("TEST", "Test Project", "template_id")

            # Act & Assert
            with self.assertRaises(TempProjectError):
                temp_project.tear_down()

    @patch("python_sbb_polarion.testing.project_template_uploader.Path.exists", return_value=False)
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_file_not_exists(self, mock_uuid: Mock, mock_factory: Mock, mock_create_polarion: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template raises when file does not exist."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")
        mock_factory.return_value = Mock()
        mock_create_polarion.return_value = _success_polarion_api()

        # Act & Assert
        with self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/nonexistent"))

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_no_location(self, mock_uuid: Mock, mock_create_polarion: Mock, mock_factory: Mock) -> None:
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
    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_hash_match(self, mock_uuid: Mock, mock_factory: Mock, mock_create_polarion: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template skips upload when hash matches."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        test_hash: str = "abc123hash"
        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=test_hash)
        mock_factory.return_value = mock_test_data_api
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
    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_hash_differs(
        self,
        mock_uuid: Mock,
        mock_factory: Mock,
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
        mock_factory.return_value = mock_test_data_api
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
    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_upload_project_template_upload_fails(self, mock_uuid: Mock, mock_factory: Mock, mock_create_polarion: Mock, mock_exists: Mock) -> None:
        """Test _upload_project_template raises when upload fails."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        local_hash: str = "abc123hash"
        remote_hash: str = "differenthash"

        mock_test_data_api = Mock()
        mock_test_data_api.get_template_hash.return_value = Mock(status_code=HTTPStatus.OK, text=remote_hash)
        mock_test_data_api.save_project_template.return_value = Mock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_factory.return_value = mock_test_data_api
        mock_create_polarion.return_value = _success_polarion_api()

        # Act & Assert
        with patch("python_sbb_polarion.testing.project_template_uploader.ProjectTemplateUploader.calculate_folder_hash", return_value=local_hash), self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id", template_location=Path("/tmp/template"))

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    def test_init_keeps_project_id_when_not_mutated(self, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test __init__ keeps the given project id verbatim when mutate_project_id is False."""
        # Arrange
        mock_create_api.return_value = _success_polarion_api()

        # Act
        temp_project = TempProject("FIXED", "Test Project", "template_id", mutate_project_id=False)

        # Assert
        self.assertEqual(temp_project.temp_project_id, "FIXED")

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    def test_create_temp_project_job_id_missing(self, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _create_temp_project raises when the 202 body has a data object but no job id."""
        # Arrange
        mock_api: Mock = _success_polarion_api()
        mock_api.create_project.return_value = _response(HTTPStatus.ACCEPTED, {"data": {"type": "jobs"}})
        mock_create_api.return_value = mock_api

        # Act & Assert
        with self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id", mutate_project_id=False)

    def test_job_status_handles_malformed_bodies(self) -> None:
        """Test _job_status returns (None, None) for bodies without a terminal status object."""
        self.assertEqual(TempProject._job_status({}), (None, None))
        self.assertEqual(TempProject._job_status({"data": "not-a-dict"}), (None, None))
        self.assertEqual(TempProject._job_status({"data": {"attributes": "nope"}}), (None, None))
        self.assertEqual(TempProject._job_status({"data": {"attributes": {"status": "nope"}}}), (None, None))
        self.assertEqual(
            TempProject._job_status({"data": {"attributes": {"status": {"type": "OK", "message": "done"}}}}),
            ("OK", "done"),
        )

    def test_safe_json_handles_non_object_bodies(self) -> None:
        """Test _safe_json returns {} for non-JSON or non-object bodies, and the dict otherwise."""
        non_json: Mock = Mock()
        non_json.json.side_effect = ValueError("no json")
        self.assertEqual(TempProject._safe_json(non_json), {})

        as_list: Mock = Mock()
        as_list.json.return_value = [1, 2, 3]
        self.assertEqual(TempProject._safe_json(as_list), {})

        as_object: Mock = Mock()
        as_object.json.return_value = {"a": 1}
        self.assertEqual(TempProject._safe_json(as_object), {"a": 1})

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    def test_create_temp_project_precheck_error(self, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _create_temp_project raises when the existence pre-check returns a non-200/non-404 status."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="precheck-uuid")

        mock_api: Mock = _success_polarion_api()
        mock_api.get_project.return_value = _response(HTTPStatus.FORBIDDEN)
        mock_create_api.return_value = mock_api

        # Act & Assert
        with self.assertRaises(TempProjectError):
            TempProject("TEST", "Test Project", "template_id")

        # the obstacle is surfaced before any creation attempt
        mock_api.create_project.assert_not_called()

    @patch("python_sbb_polarion.testing.temp_project.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.temp_project.GenericTestCase.create_polarion_api")
    @patch("python_sbb_polarion.testing.temp_project.uuid.uuid4")
    @patch("python_sbb_polarion.testing.temp_project.time.sleep")
    def test_wait_for_job_retries_transient_poll_errors(self, mock_sleep: Mock, mock_uuid: Mock, mock_create_api: Mock, mock_factory: Mock) -> None:
        """Test _wait_for_job keeps polling through a non-200 then a non-JSON response before OK."""
        # Arrange
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="transient-uuid")

        bad_json: Mock = Mock()
        bad_json.status_code = HTTPStatus.OK
        bad_json.json.side_effect = ValueError("html error page")

        mock_api: Mock = _success_polarion_api()
        # transient 503, then a 200 with a non-JSON body, then a finished job
        mock_api.get_job.side_effect = [
            _response(HTTPStatus.SERVICE_UNAVAILABLE),
            bad_json,
            _job("OK"),
        ]
        mock_create_api.return_value = mock_api

        # Act - should not raise
        temp_project = TempProject("TEST", "Test Project", "template_id")

        # Assert
        self.assertIsNotNone(temp_project.temp_project_id)
        self.assertEqual(mock_api.get_job.call_count, 3)
        mock_api.update_project.assert_called_once()


if __name__ == "__main__":
    unittest.main()
