import unittest
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

from python_sbb_polarion.polarion_project_manager.project_manager import PolarionProjectManager


if TYPE_CHECKING:
    from python_sbb_polarion.testing import TempProject


class TestPolarionProjectManager(unittest.TestCase):
    """Test suite for PolarionProjectManager class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_template_dir = Path("./test-templates")
        self.manager = PolarionProjectManager(template_dir=self.test_template_dir)

    def tearDown(self) -> None:
        """Clean up after tests."""
        # Clean up any created directories in tests
        if self.test_template_dir.exists():
            import shutil

            shutil.rmtree(self.test_template_dir, ignore_errors=True)

    def test_init_creates_template_directory(self) -> None:
        """Test that initialization creates the template directory."""
        self.assertTrue(self.test_template_dir.exists())
        self.assertTrue(self.test_template_dir.is_dir())

    def test_init_with_path_object(self) -> None:
        """Test initialization with Path object."""
        path_obj = Path("./another-test-dir")
        manager = PolarionProjectManager(template_dir=path_obj)
        self.assertEqual(manager.template_dir, path_obj)
        path_obj.rmdir()  # Clean up

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.GenericTestCase")
    def test_download_project_success(self, mock_generic_test: Mock) -> None:
        """Test successful project download."""
        # Setup mock response
        mock_response = Mock()
        mock_response.content = b"fake zip content"
        mock_response.raise_for_status = Mock()

        mock_api = Mock()
        mock_api.download_project_template.return_value = mock_response
        mock_generic_test.create_extension_api.return_value = mock_api

        # Execute
        result_path: Path = self.manager.download_project(project_id="test_project", project_group="test_group")

        # Verify
        self.assertTrue(result_path.exists())
        self.assertEqual(result_path.name, "test_project_remote.zip")
        mock_api.download_project_template.assert_called_once_with(project_id="test_project", project_group="test_group")

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.GenericTestCase")
    def test_download_project_with_custom_filename(self, mock_generic_test: Mock) -> None:
        """Test project download with custom output filename."""
        mock_response = Mock()
        mock_response.content = b"fake zip content"
        mock_response.raise_for_status = Mock()

        mock_api = Mock()
        mock_api.download_project_template.return_value = mock_response
        mock_generic_test.create_extension_api.return_value = mock_api

        result_path: Path = self.manager.download_project(project_id="test_project", output_filename="custom_name")

        self.assertEqual(result_path.name, "custom_name.zip")

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.GenericTestCase")
    def test_download_project_empty_content(self, mock_generic_test: Mock) -> None:
        """Test that empty response content raises ValueError."""
        mock_response = Mock()
        mock_response.content = b""
        mock_response.raise_for_status = Mock()

        mock_api = Mock()
        mock_api.download_project_template.return_value = mock_response
        mock_generic_test.create_extension_api.return_value = mock_api

        with self.assertRaises(ValueError) as context:
            self.manager.download_project(project_id="test_project")

        self.assertIn("Empty content", str(context.exception))

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.GenericTestCase")
    def test_download_project_api_error(self, mock_generic_test: Mock) -> None:
        """Test handling of API errors during download."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = ValueError("API Error")

        mock_api = Mock()
        mock_api.download_project_template.return_value = mock_response
        mock_generic_test.create_extension_api.return_value = mock_api

        with self.assertRaises(ValueError):
            self.manager.download_project(project_id="test_project")

    def test_find_first_zip_file_success(self) -> None:
        """Test finding first zip file in directory."""
        # Create a test zip file
        test_zip_dir = Path("test-data/project-template")
        test_zip_dir.mkdir(parents=True, exist_ok=True)
        test_zip_file: Path = test_zip_dir / "test_template.zip"
        test_zip_file.write_bytes(b"fake content")

        try:
            result: Path = PolarionProjectManager._find_first_zip_file()
            self.assertEqual(result.name, "test_template.zip")
        finally:
            # Clean up
            test_zip_file.unlink()
            test_zip_dir.rmdir()

    def test_find_first_zip_file_not_found(self) -> None:
        """Test error when no zip files exist."""
        # Ensure directory exists but is empty
        test_dir = Path("test-data/project-template")
        test_dir.mkdir(parents=True, exist_ok=True)

        try:
            with self.assertRaises(FileNotFoundError) as context:
                PolarionProjectManager._find_first_zip_file()
            self.assertIn("No zip files found", str(context.exception))
        finally:
            test_dir.rmdir()

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.TempProject")
    def test_create_project_success(self, mock_temp_project: Mock) -> None:
        """Test successful project creation from template."""
        # Create a fake template file
        template_path: Path = self.test_template_dir / "test_template.zip"
        template_path.write_bytes(b"fake zip content")

        mock_project_instance = Mock()
        mock_project_instance.temp_project_id = "temp_test_project"
        mock_temp_project.return_value = mock_project_instance

        result: TempProject = PolarionProjectManager.create_project(template_path=str(template_path), template_id="test_template", project_id="test_proj", project_name="Test Project")

        self.assertEqual(result.temp_project_id, "temp_test_project")
        mock_temp_project.assert_called_once_with(project_id="test_proj", project_name="Test Project", template_id="test_template", template_location=template_path)

    def test_create_project_file_not_found(self) -> None:
        """Test error when template file doesn't exist."""
        with self.assertRaises(FileNotFoundError) as context:
            PolarionProjectManager.create_project(template_path="nonexistent_file.zip", project_id="test_proj")
        self.assertIn("No such file or directory", str(context.exception))

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.PolarionProjectManager._find_first_zip_file")
    @patch("python_sbb_polarion.polarion_project_manager.project_manager.TempProject")
    def test_create_project_no_template_path(self, mock_temp_project: Mock, mock_find_zip: Mock) -> None:
        """Test project creation when no template path is provided."""
        # Mock finding a zip file
        mock_zip_path = Path("test-data/project-template/found.zip")
        mock_find_zip.return_value = mock_zip_path

        # Create the file so it passes the is_file() check
        mock_zip_path.parent.mkdir(parents=True, exist_ok=True)
        mock_zip_path.write_bytes(b"fake content")

        try:
            mock_project_instance = Mock()
            mock_project_instance.temp_project_id = "temp_proj"
            mock_temp_project.return_value = mock_project_instance

            result: TempProject = PolarionProjectManager.create_project(template_path=None, project_id="test_proj")

            mock_find_zip.assert_called_once()
            self.assertIsNotNone(result)
        finally:
            mock_zip_path.unlink(missing_ok=True)

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.ProjectTemplateUploader")
    @patch("python_sbb_polarion.polarion_project_manager.project_manager.GenericTestCase")
    def test_upload_template_success(self, mock_generic_test: Mock, mock_uploader_class: Mock) -> None:
        """Test successful template upload."""
        # Create a fake template file
        template_path: Path = self.test_template_dir / "upload_template.zip"
        template_path.write_bytes(b"fake zip content")

        mock_api = Mock()
        mock_generic_test.create_extension_api.return_value = mock_api

        mock_uploader = Mock()
        mock_uploader_class.return_value = mock_uploader

        PolarionProjectManager.upload_template(template_path=str(template_path), template_id="custom_template")

        mock_uploader.upload_template.assert_called_once_with(template_id="custom_template", template_location=template_path)

    @patch("python_sbb_polarion.polarion_project_manager.project_manager.PolarionProjectManager._find_first_zip_file")
    @patch("python_sbb_polarion.polarion_project_manager.project_manager.ProjectTemplateUploader")
    @patch("python_sbb_polarion.polarion_project_manager.project_manager.GenericTestCase")
    def test_upload_template_no_path(self, mock_generic_test: Mock, mock_uploader_class: Mock, mock_find_zip: Mock) -> None:
        """Test template upload when no path is provided."""
        mock_zip_path = Path("test-data/project-template/found.zip")
        mock_find_zip.return_value = mock_zip_path

        mock_api = Mock()
        mock_generic_test.create_extension_api.return_value = mock_api

        mock_uploader = Mock()
        mock_uploader_class.return_value = mock_uploader

        PolarionProjectManager.upload_template(template_path=None, template_id="custom_template")

        mock_find_zip.assert_called_once()
        mock_uploader.upload_template.assert_called_once()


if __name__ == "__main__":
    unittest.main()
