import unittest
from typing import TYPE_CHECKING

from python_sbb_polarion.polarion_project_manager.cli import build_parser


if TYPE_CHECKING:
    from argparse import Namespace


class TestBuildParser(unittest.TestCase):
    """Test suite for build_parser function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.parser = build_parser()

    def test_parser_has_template_dir_argument(self) -> None:
        """Test that parser has --template-dir argument with correct default."""
        args: Namespace = self.parser.parse_args(["download", "--project_id", "test"])
        self.assertEqual(args.template_dir, "./test-data/project-template")

    def test_parser_template_dir_custom_value(self) -> None:
        """Test custom template directory value."""
        args: Namespace = self.parser.parse_args(["--template-dir", "/custom/path", "download", "--project_id", "test"])
        self.assertEqual(args.template_dir, "/custom/path")

    def test_parser_requires_command(self) -> None:
        """Test that parser requires a command."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_parser_has_download_command(self) -> None:
        """Test that download command exists."""
        args: Namespace = self.parser.parse_args(["download", "--project_id", "test_proj"])
        self.assertEqual(args.command, "download")

    def test_parser_has_upload_template_command(self) -> None:
        """Test that upload_template command exists."""
        args: Namespace = self.parser.parse_args(["upload_template"])
        self.assertEqual(args.command, "upload_template")

    def test_parser_has_create_command(self) -> None:
        """Test that create command exists."""
        args: Namespace = self.parser.parse_args(["create", "--project_id", "test_proj"])
        self.assertEqual(args.command, "create")

    def test_download_command_requires_project_id(self) -> None:
        """Test that download command requires --project_id."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["download"])

    def test_download_command_with_all_arguments(self) -> None:
        """Test download command with all arguments."""
        args: Namespace = self.parser.parse_args(["download", "--project_id", "my_project", "--project_group", "my_group", "--output", "custom_output"])
        self.assertEqual(args.command, "download")
        self.assertEqual(args.project_id, "my_project")
        self.assertEqual(args.project_group, "my_group")
        self.assertEqual(args.output, "custom_output")

    def test_download_command_optional_arguments(self) -> None:
        """Test that download command optional arguments work."""
        args: Namespace = self.parser.parse_args(["download", "--project_id", "test"])
        self.assertIsNone(args.project_group)
        self.assertIsNone(args.output)

    def test_upload_template_command_default_values(self) -> None:
        """Test upload_template command default values."""
        args: Namespace = self.parser.parse_args(["upload_template"])
        self.assertEqual(args.command, "upload_template")
        self.assertEqual(args.template_id, "custom_project_template_for_st")
        self.assertIsNone(args.template_path)

    def test_upload_template_command_with_arguments(self) -> None:
        """Test upload_template command with custom arguments."""
        args: Namespace = self.parser.parse_args(["upload_template", "--template_id", "custom_template", "--template_path", "/path/to/template.zip"])
        self.assertEqual(args.template_id, "custom_template")
        self.assertEqual(args.template_path, "/path/to/template.zip")

    def test_create_command_requires_project_id(self) -> None:
        """Test that create command requires --project_id."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["create"])

    def test_create_command_default_values(self) -> None:
        """Test create command default values."""
        args: Namespace = self.parser.parse_args(["create", "--project_id", "test_proj"])
        self.assertEqual(args.command, "create")
        self.assertEqual(args.project_id, "test_proj")
        self.assertEqual(args.project_name, "E-Library")
        self.assertEqual(args.template_id, "custom_project_template_for_st")
        self.assertIsNone(args.template_path)

    def test_create_command_with_all_arguments(self) -> None:
        """Test create command with all custom arguments."""
        args: Namespace = self.parser.parse_args(["create", "--project_id", "my_proj", "--project_name", "My Project", "--template_id", "my_template", "--template_path", "/path/to/template.zip"])
        self.assertEqual(args.project_id, "my_proj")
        self.assertEqual(args.project_name, "My Project")
        self.assertEqual(args.template_id, "my_template")
        self.assertEqual(args.template_path, "/path/to/template.zip")
