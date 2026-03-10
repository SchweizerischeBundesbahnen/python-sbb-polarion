"""Unit tests for ProjectTemplateUploader."""

from __future__ import annotations

import tempfile
import unittest
from http import HTTPStatus
from pathlib import Path
from unittest.mock import Mock, patch

from python_sbb_polarion.testing.project_template_uploader import ProjectTemplateUploader


class TestProjectTemplateUploader(unittest.TestCase):
    """Test ProjectTemplateUploader class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_api = Mock()
        self.uploader = ProjectTemplateUploader(self.mock_api)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.uploader._test_data_api, self.mock_api)

    def test_calculate_folder_hash(self) -> None:
        """Test calculate_folder_hash returns consistent hash for folder contents."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)

            # Create test files
            (tmp_path / "file1.txt").write_bytes(b"content1")
            (tmp_path / "file2.txt").write_bytes(b"content2")
            subdir: Path = tmp_path / "subdir"
            subdir.mkdir()
            (subdir / "file3.txt").write_bytes(b"content3")

            result: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path)

            # SHA-512 hash is 128 hex characters
            self.assertEqual(len(result), 128)
            self.assertTrue(all(c in "0123456789abcdef" for c in result))

    def test_calculate_folder_hash_deterministic(self) -> None:
        """Test calculate_folder_hash produces same hash for identical folder contents."""
        with tempfile.TemporaryDirectory() as tmp_dir1, tempfile.TemporaryDirectory() as tmp_dir2:
            tmp_path1: Path = Path(tmp_dir1)
            tmp_path2: Path = Path(tmp_dir2)

            # Create identical content in both folders
            for tmp_path in [tmp_path1, tmp_path2]:
                (tmp_path / "file1.txt").write_bytes(b"content1")
                (tmp_path / "file2.txt").write_bytes(b"content2")
                subdir: Path = tmp_path / "subdir"
                subdir.mkdir()
                (subdir / "file3.txt").write_bytes(b"content3")

            hash1: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path1)
            hash2: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path2)

            self.assertEqual(hash1, hash2)

    def test_calculate_folder_hash_different_content(self) -> None:
        """Test calculate_folder_hash produces different hash for different contents."""
        with tempfile.TemporaryDirectory() as tmp_dir1, tempfile.TemporaryDirectory() as tmp_dir2:
            tmp_path1: Path = Path(tmp_dir1)
            tmp_path2: Path = Path(tmp_dir2)

            # Create different content
            (tmp_path1 / "file1.txt").write_bytes(b"content1")
            (tmp_path2 / "file1.txt").write_bytes(b"different_content")

            hash1: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path1)
            hash2: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path2)

            self.assertNotEqual(hash1, hash2)

    def test_calculate_folder_hash_empty_folder(self) -> None:
        """Test calculate_folder_hash handles empty folder."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)

            result: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path)

            # Should still return valid hash
            self.assertEqual(len(result), 128)

    def test_zip_folder_not_a_directory(self) -> None:
        """Test zip_folder exits when path is not a directory."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(b"test")
            tmp_path: Path = Path(tmp_file.name)

        try:
            with patch("python_sbb_polarion.testing.project_template_uploader.sys.exit") as mock_exit:
                mock_exit.side_effect = SystemExit(1)

                with self.assertRaises(SystemExit):
                    ProjectTemplateUploader.zip_folder(tmp_path)

                mock_exit.assert_called_once_with(1)
        finally:
            tmp_path.unlink()

    def test_zip_folder_creates_valid_zip(self) -> None:
        """Test zip_folder creates a valid zip file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)

            # Create test files
            (tmp_path / "file1.txt").write_bytes(b"content1")
            subdir: Path = tmp_path / "subdir"
            subdir.mkdir()
            (subdir / "file2.txt").write_bytes(b"content2")

            zip_path: Path = ProjectTemplateUploader.zip_folder(tmp_path)

            try:
                # Verify zip file exists and is valid
                self.assertTrue(zip_path.exists())
                self.assertTrue(zip_path.suffix == ".zip")

                # Verify zip contents
                import zipfile

                with zipfile.ZipFile(zip_path, "r") as zipf:
                    namelist: list[str] = zipf.namelist()
                    self.assertIn("file1.txt", namelist)
                    self.assertIn("subdir/file2.txt", namelist)
            finally:
                if zip_path.exists():
                    zip_path.unlink()

    def test_upload_template_folder_not_exists(self) -> None:
        """Test upload_template exits when folder doesn't exist."""
        with patch("python_sbb_polarion.testing.project_template_uploader.sys.exit") as mock_exit:
            mock_exit.side_effect = SystemExit(1)

            with self.assertRaises(SystemExit):
                self.uploader.upload_template("template1", Path("/non/existent/folder"))

            mock_exit.assert_called_once_with(1)

    def test_upload_template_up_to_date(self) -> None:
        """Test upload_template skips upload when hashes match."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)
            (tmp_path / "file.txt").write_bytes(b"test content")

            local_hash: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path)

            mock_response = Mock()
            mock_response.status_code = HTTPStatus.OK
            mock_response.text = local_hash
            self.mock_api.get_template_hash.return_value = mock_response

            self.uploader.upload_template("template1", tmp_path)

            self.mock_api.get_template_hash.assert_called_once_with(template_id="template1")
            self.mock_api.save_project_template.assert_not_called()

    def test_upload_template_hash_differs(self) -> None:
        """Test upload_template uploads when hashes differ."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)
            (tmp_path / "file.txt").write_bytes(b"test content")

            local_hash: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path)

            mock_get_response = Mock()
            mock_get_response.status_code = HTTPStatus.OK
            mock_get_response.text = "different_hash"
            self.mock_api.get_template_hash.return_value = mock_get_response

            mock_save_response = Mock()
            mock_save_response.status_code = HTTPStatus.CREATED
            self.mock_api.save_project_template.return_value = mock_save_response

            with patch.object(ProjectTemplateUploader, "zip_folder") as mock_zip:
                mock_zip_path = Path("/tmp/test.zip")
                mock_zip.return_value = mock_zip_path

                with patch.object(Path, "exists", return_value=True), patch.object(Path, "unlink"):
                    self.uploader.upload_template("template1", tmp_path)

            self.mock_api.get_template_hash.assert_called_once_with(template_id="template1")
            self.mock_api.save_project_template.assert_called_once()

            # Verify the call arguments
            call_kwargs: dict[str, str] = self.mock_api.save_project_template.call_args.kwargs
            self.assertEqual(call_kwargs["template_id"], "template1")
            self.assertEqual(call_kwargs["template_hash"], local_hash)

    def test_upload_template_server_error(self) -> None:
        """Test upload_template uploads when server returns non-OK status."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)
            (tmp_path / "file.txt").write_bytes(b"test content")

            mock_get_response = Mock()
            mock_get_response.status_code = HTTPStatus.NOT_FOUND
            self.mock_api.get_template_hash.return_value = mock_get_response

            mock_save_response = Mock()
            mock_save_response.status_code = HTTPStatus.CREATED
            self.mock_api.save_project_template.return_value = mock_save_response

            with patch.object(ProjectTemplateUploader, "zip_folder") as mock_zip:
                mock_zip_path = Path("/tmp/test.zip")
                mock_zip.return_value = mock_zip_path

                with patch.object(Path, "exists", return_value=True), patch.object(Path, "unlink"):
                    self.uploader.upload_template("template1", tmp_path)

            self.mock_api.save_project_template.assert_called_once()

    def test_upload_template_save_fails(self) -> None:
        """Test upload_template exits when save fails."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)
            (tmp_path / "file.txt").write_bytes(b"test content")

            mock_get_response = Mock()
            mock_get_response.status_code = HTTPStatus.OK
            mock_get_response.text = "different_hash"
            self.mock_api.get_template_hash.return_value = mock_get_response

            mock_save_response = Mock()
            mock_save_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.mock_api.save_project_template.return_value = mock_save_response

            with patch("python_sbb_polarion.testing.project_template_uploader.sys.exit") as mock_exit:
                mock_exit.side_effect = SystemExit(1)

                with patch.object(ProjectTemplateUploader, "zip_folder") as mock_zip:
                    mock_zip_path = Path("/tmp/test.zip")
                    mock_zip.return_value = mock_zip_path

                    with patch.object(Path, "exists", return_value=True), patch.object(Path, "unlink") as mock_unlink:
                        with self.assertRaises(SystemExit):
                            self.uploader.upload_template("template1", tmp_path)

                        # Verify cleanup happened even on error
                        mock_unlink.assert_called_once()

                mock_exit.assert_called_once_with(1)

    def test_upload_template_cleanup_on_success(self) -> None:
        """Test upload_template cleans up zip file after successful upload."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)
            (tmp_path / "file.txt").write_bytes(b"test content")

            mock_get_response = Mock()
            mock_get_response.status_code = HTTPStatus.OK
            mock_get_response.text = "different_hash"
            self.mock_api.get_template_hash.return_value = mock_get_response

            mock_save_response = Mock()
            mock_save_response.status_code = HTTPStatus.CREATED
            self.mock_api.save_project_template.return_value = mock_save_response

            with patch.object(ProjectTemplateUploader, "zip_folder") as mock_zip:
                mock_zip_path = Path("/tmp/test.zip")
                mock_zip.return_value = mock_zip_path

                with patch.object(Path, "exists", return_value=True), patch.object(Path, "unlink") as mock_unlink:
                    self.uploader.upload_template("template1", tmp_path)

                    # Verify cleanup was called
                    mock_unlink.assert_called_once()

    def test_upload_template_no_cleanup_when_up_to_date(self) -> None:
        """Test upload_template doesn't try to clean up when no zip was created."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir)
            (tmp_path / "file.txt").write_bytes(b"test content")

            local_hash: str = ProjectTemplateUploader.calculate_folder_hash(tmp_path)

            mock_response = Mock()
            mock_response.status_code = HTTPStatus.OK
            mock_response.text = local_hash
            self.mock_api.get_template_hash.return_value = mock_response

            with patch.object(Path, "unlink") as mock_unlink:
                # Should complete without error and without calling unlink
                self.uploader.upload_template("template1", tmp_path)

                # unlink should never be called since zip_path is None
                mock_unlink.assert_not_called()


if __name__ == "__main__":
    unittest.main()
