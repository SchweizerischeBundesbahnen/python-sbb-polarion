"""Unit tests for path utilities."""

from __future__ import annotations

import unittest
from pathlib import Path

from python_sbb_polarion.util.path import abs_path, abs_path_str


class TestAbsPath(unittest.TestCase):
    """Test abs_path function."""

    def test_returns_path_object(self) -> None:
        """Test that abs_path returns a Path object."""
        result: Path = abs_path("some_file.txt")
        self.assertIsInstance(result, Path)

    def test_returns_absolute_path(self) -> None:
        """Test that abs_path returns an absolute path."""
        result: Path = abs_path("some_file.txt")
        self.assertTrue(result.is_absolute())

    def test_resolves_relative_to_caller_file(self) -> None:
        """Test that path is resolved relative to this test file, not cwd."""
        result: Path = abs_path("some_file.txt")
        this_file: Path = Path(__file__).resolve()
        expected: Path = this_file.parent / "some_file.txt"
        self.assertEqual(result, expected)

    def test_handles_subdirectory(self) -> None:
        """Test resolving path to a subdirectory."""
        result: Path = abs_path("data/config.json")
        this_file: Path = Path(__file__).resolve()
        expected: Path = this_file.parent / "data" / "config.json"
        self.assertEqual(result, expected)

    def test_handles_parent_directory(self) -> None:
        """Test resolving path with parent directory reference."""
        result: Path = abs_path("../other_file.txt")
        this_file: Path = Path(__file__).resolve()
        expected: Path = (this_file.parent.parent / "other_file.txt").resolve()
        self.assertEqual(result, expected)

    def test_accepts_path_object(self) -> None:
        """Test that abs_path accepts Path object as input."""
        input_path: Path = Path("some_file.txt")
        result: Path = abs_path(input_path)
        self.assertIsInstance(result, Path)
        self.assertTrue(result.is_absolute())

    def test_returns_none_for_none_input(self) -> None:
        """Test that abs_path returns None when given None."""
        result: None = abs_path(None)
        self.assertIsNone(result)


class TestAbsPathStr(unittest.TestCase):
    """Test abs_path_str function."""

    def test_returns_string(self) -> None:
        """Test that abs_path_str returns a string."""
        result: str = abs_path_str("some_file.txt")
        self.assertIsInstance(result, str)

    def test_returns_absolute_path_string(self) -> None:
        """Test that abs_path_str returns an absolute path string."""
        result: str = abs_path_str("some_file.txt")
        self.assertTrue(Path(result).is_absolute())

    def test_resolves_relative_to_caller_file(self) -> None:
        """Test that path is resolved relative to this test file, not cwd."""
        result: str = abs_path_str("some_file.txt")
        this_file: Path = Path(__file__).resolve()
        expected: str = str(this_file.parent / "some_file.txt")
        self.assertEqual(result, expected)

    def test_handles_subdirectory(self) -> None:
        """Test resolving path to a subdirectory."""
        result: str = abs_path_str("data/config.json")
        this_file: Path = Path(__file__).resolve()
        expected: str = str(this_file.parent / "data" / "config.json")
        self.assertEqual(result, expected)

    def test_handles_parent_directory(self) -> None:
        """Test resolving path with parent directory reference."""
        result: str = abs_path_str("../other_file.txt")
        this_file: Path = Path(__file__).resolve()
        expected: str = str((this_file.parent.parent / "other_file.txt").resolve())
        self.assertEqual(result, expected)

    def test_accepts_path_object(self) -> None:
        """Test that abs_path_str accepts Path object as input."""
        input_path: Path = Path("some_file.txt")
        result: str = abs_path_str(input_path)
        self.assertIsInstance(result, str)
        self.assertTrue(Path(result).is_absolute())

    def test_returns_none_for_none_input(self) -> None:
        """Test that abs_path_str returns None when given None."""
        result: None = abs_path_str(None)
        self.assertIsNone(result)


class TestAbsPathConsistency(unittest.TestCase):
    """Test consistency between abs_path and abs_path_str."""

    def test_both_functions_return_same_path(self) -> None:
        """Test that abs_path and abs_path_str return the same path."""
        path_result: Path = abs_path("test_file.txt")
        str_result: str = abs_path_str("test_file.txt")
        self.assertEqual(str(path_result), str_result)

    def test_both_functions_handle_complex_path(self) -> None:
        """Test both functions with a complex relative path."""
        relative: str = "../data/../other/file.txt"
        path_result: Path = abs_path(relative)
        str_result: str = abs_path_str(relative)
        self.assertEqual(str(path_result), str_result)


if __name__ == "__main__":
    unittest.main()
