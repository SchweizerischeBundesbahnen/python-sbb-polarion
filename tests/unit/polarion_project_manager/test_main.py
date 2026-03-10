import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from python_sbb_polarion.polarion_project_manager.cli import main


class TestMain(unittest.TestCase):
    """Test suite for main function."""

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "download", "--project_id", "test_project"])
    def test_main_download_command_success(self, mock_manager_class: Mock) -> None:
        """Test main function with download command."""
        mock_manager = Mock()
        mock_manager.download_project.return_value = Path("/path/to/downloaded.zip")
        mock_manager_class.return_value = mock_manager

        main()

        mock_manager_class.assert_called_once_with(template_dir="./test-data/project-template")
        mock_manager.download_project.assert_called_once_with(project_id="test_project", project_group=None, output_filename=None)

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "download", "--project_id", "test_project", "--project_group", "test_group", "--output", "custom_output"])
    def test_main_download_with_all_args(self, mock_manager_class: Mock) -> None:
        """Test main function with download command and all arguments."""
        mock_manager = Mock()
        mock_manager.download_project.return_value = Path("/path/to/custom_output.zip")
        mock_manager_class.return_value = mock_manager

        main()

        mock_manager.download_project.assert_called_once_with(project_id="test_project", project_group="test_group", output_filename="custom_output")

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "upload_template"])
    def test_main_upload_template_command_success(self, mock_manager_class: Mock) -> None:
        """Test main function with upload_template command."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        main()

        mock_manager_class.assert_called_once_with(template_dir="./test-data/project-template")
        mock_manager.upload_template.assert_called_once_with(template_id="custom_project_template_for_st", template_path=None)

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "upload_template", "--template_id", "my_template", "--template_path", "/path/to/template.zip"])
    def test_main_upload_template_with_args(self, mock_manager_class: Mock) -> None:
        """Test main function with upload_template command and arguments."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        main()

        mock_manager.upload_template.assert_called_once_with(template_id="my_template", template_path="/path/to/template.zip")

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "create", "--project_id", "test_proj"])
    def test_main_create_command_success(self, mock_manager_class: Mock) -> None:
        """Test main function with create command."""
        mock_manager = Mock()
        mock_temp_project = Mock()
        mock_temp_project.temp_project_id = "temp_test_proj_123"
        mock_manager.create_project.return_value = mock_temp_project
        mock_manager_class.return_value = mock_manager

        main()

        mock_manager_class.assert_called_once_with(template_dir="./test-data/project-template")
        mock_manager.create_project.assert_called_once_with(template_path=None, template_id="custom_project_template_for_st", project_id="test_proj", project_name="E-Library")

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "create", "--project_id", "my_proj", "--project_name", "My Project", "--template_id", "my_template", "--template_path", "/path/to/template.zip"])
    def test_main_create_with_all_args(self, mock_manager_class: Mock) -> None:
        """Test main function with create command and all arguments."""
        mock_manager = Mock()
        mock_temp_project = Mock()
        mock_temp_project.temp_project_id = "temp_my_proj_456"
        mock_manager.create_project.return_value = mock_temp_project
        mock_manager_class.return_value = mock_manager

        main()

        mock_manager.create_project.assert_called_once_with(template_path="/path/to/template.zip", template_id="my_template", project_id="my_proj", project_name="My Project")

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "--template-dir", "/custom/dir", "download", "--project_id", "test"])
    def test_main_with_custom_template_dir(self, mock_manager_class: Mock) -> None:
        """Test main function with custom template directory."""
        mock_manager = Mock()
        mock_manager.download_project.return_value = Path("/path/to/file.zip")
        mock_manager_class.return_value = mock_manager

        main()

        mock_manager_class.assert_called_once_with(template_dir="/custom/dir")

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "download", "--project_id", "test_project"])
    def test_main_file_not_found_error(self, mock_manager_class: Mock) -> None:
        """Test main function handles FileNotFoundError."""
        mock_manager = Mock()
        mock_manager.download_project.side_effect = FileNotFoundError("Template not found")
        mock_manager_class.return_value = mock_manager

        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 2)

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "download", "--project_id", "test_project"])
    def test_main_generic_exception(self, mock_manager_class: Mock) -> None:
        """Test main function handles generic exceptions."""
        mock_manager = Mock()
        mock_manager.download_project.side_effect = Exception("Something went wrong")
        mock_manager_class.return_value = mock_manager

        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 1)

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "create", "--project_id", "test"])
    def test_main_create_file_not_found(self, mock_manager_class: Mock) -> None:
        """Test main function handles FileNotFoundError in create command."""
        mock_manager = Mock()
        mock_manager.create_project.side_effect = FileNotFoundError("Template file not found")
        mock_manager_class.return_value = mock_manager

        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 2)

    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "upload_template"])
    def test_main_upload_generic_exception(self, mock_manager_class: Mock) -> None:
        """Test main function handles exceptions in upload_template command."""
        mock_manager = Mock()
        mock_manager.upload_template.side_effect = Exception("Upload failed")
        mock_manager_class.return_value = mock_manager

        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 1)

    @patch("python_sbb_polarion.polarion_project_manager.cli.logger")
    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "download", "--project_id", "test"])
    def test_main_logs_download_success(self, mock_manager_class: Mock, mock_logger: Mock) -> None:
        """Test that main logs successful download."""
        mock_manager = Mock()
        mock_path = Path("/path/to/downloaded.zip")
        mock_manager.download_project.return_value = mock_path
        mock_manager_class.return_value = mock_manager

        main()

        mock_logger.info.assert_called_with(f"Downloaded to: {mock_path}")

    @patch("python_sbb_polarion.polarion_project_manager.cli.logger")
    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "upload_template", "--template_id", "my_template"])
    def test_main_logs_upload_success(self, mock_manager_class: Mock, mock_logger: Mock) -> None:
        """Test that main logs successful upload."""
        mock_manager = Mock()
        mock_manager_class.return_value = mock_manager

        main()

        mock_logger.info.assert_called_with("Uploaded template: my_template")

    @patch("python_sbb_polarion.polarion_project_manager.cli.logger")
    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "create", "--project_id", "test"])
    def test_main_logs_create_success(self, mock_manager_class: Mock, mock_logger: Mock) -> None:
        """Test that main logs successful project creation."""
        mock_manager = Mock()
        mock_temp_project = Mock()
        mock_temp_project.temp_project_id = "temp_proj_789"
        mock_manager.create_project.return_value = mock_temp_project
        mock_manager_class.return_value = mock_manager

        main()

        mock_logger.info.assert_called_with("Created project: temp_proj_789")

    @patch("python_sbb_polarion.polarion_project_manager.cli.logger")
    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "download", "--project_id", "test"])
    def test_main_logs_file_not_found_error(self, mock_manager_class: Mock, mock_logger: Mock) -> None:
        """Test that main logs FileNotFoundError."""
        mock_manager = Mock()
        error_msg: str = "Template not found"
        mock_manager.download_project.side_effect = FileNotFoundError(error_msg)
        mock_manager_class.return_value = mock_manager

        with self.assertRaises(SystemExit):
            main()

        mock_logger.critical.assert_called_with(f"File not found: {error_msg}")

    @patch("python_sbb_polarion.polarion_project_manager.cli.logger")
    @patch("python_sbb_polarion.polarion_project_manager.cli.PolarionProjectManager")
    @patch("sys.argv", ["cli.py", "download", "--project_id", "test"])
    def test_main_logs_generic_error(self, mock_manager_class: Mock, mock_logger: Mock) -> None:
        """Test that main logs generic exceptions."""
        mock_manager = Mock()
        error_msg: str = "Something went wrong"
        mock_manager.download_project.side_effect = Exception(error_msg)
        mock_manager_class.return_value = mock_manager

        with self.assertRaises(SystemExit):
            main()

        mock_logger.critical.assert_called_with(f"An unhandled error occurred: {error_msg}")


if __name__ == "__main__":
    unittest.main()
