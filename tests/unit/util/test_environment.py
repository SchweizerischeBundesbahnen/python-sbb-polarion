"""Unit tests for environment information utilities."""

import locale
import sys
import unittest
from importlib.metadata import Distribution
from typing import Any
from unittest.mock import Mock, patch

from python_sbb_polarion.util.environment import print_encoding, print_pip_information, print_python_information


class TestPrintPythonInformation(unittest.TestCase):
    """Test print_python_information function."""

    @patch("python_sbb_polarion.util.environment.logger")
    def test_print_python_information(self, mock_logger: Mock) -> None:
        """Test that Python version is logged."""
        print_python_information()

        mock_logger.info.assert_called_once()
        call_args: tuple[Any, ...] = mock_logger.info.call_args[0]
        self.assertIn("Python version:", call_args[0])
        # Verify the logged version matches sys.version
        self.assertIn(sys.version, call_args)

    @patch("python_sbb_polarion.util.environment.logger")
    @patch("python_sbb_polarion.util.environment.sys")
    def test_print_python_information_with_custom_version(self, mock_sys: Mock, mock_logger: Mock) -> None:
        """Test with custom Python version."""
        mock_sys.version = "3.13.0 (main, Oct 23 2025, 12:00:00)"
        print_python_information()

        mock_logger.info.assert_called_once()
        call_args: tuple[Any, ...] = mock_logger.info.call_args[0]
        self.assertIn("3.13.0", call_args[1])


class TestPrintPipInformation(unittest.TestCase):
    """Test print_pip_information function."""

    @patch("python_sbb_polarion.util.environment.logger")
    @patch("python_sbb_polarion.util.environment.distributions")
    def test_print_pip_information(self, mock_distributions: Mock, mock_logger: Mock) -> None:
        """Test that installed packages are logged."""
        # Create mock distributions
        mock_dist1 = Mock(spec=Distribution)
        mock_dist1.name = "requests"
        mock_dist1.version = "2.31.0"

        mock_dist2 = Mock(spec=Distribution)
        mock_dist2.name = "pytest"
        mock_dist2.version = "7.4.0"

        mock_distributions.return_value = [mock_dist1, mock_dist2]

        print_pip_information()

        # Should log debug messages for each package (sorted)
        self.assertEqual(mock_logger.debug.call_count, 2)
        calls: list[str] = [call[0][0] for call in mock_logger.debug.call_args_list]
        # Packages should be sorted
        self.assertEqual(calls[0], "'pytest' == 7.4.0")
        self.assertEqual(calls[1], "'requests' == 2.31.0")

    @patch("python_sbb_polarion.util.environment.logger")
    @patch("python_sbb_polarion.util.environment.distributions")
    def test_print_pip_information_empty_list(self, mock_distributions: Mock, mock_logger: Mock) -> None:
        """Test with no installed packages."""
        mock_distributions.return_value = []

        print_pip_information()

        # Should not log any debug messages
        mock_logger.debug.assert_not_called()

    @patch("python_sbb_polarion.util.environment.logger")
    @patch("python_sbb_polarion.util.environment.distributions")
    def test_print_pip_information_single_package(self, mock_distributions: Mock, mock_logger: Mock) -> None:
        """Test with single installed package."""
        mock_dist = Mock(spec=Distribution)
        mock_dist.name = "python-sbb-polarion"
        mock_dist.version = "1.0.0"

        mock_distributions.return_value = [mock_dist]

        print_pip_information()

        mock_logger.debug.assert_called_once_with("'python-sbb-polarion' == 1.0.0")

    @patch("python_sbb_polarion.util.environment.logger")
    @patch("python_sbb_polarion.util.environment.distributions")
    def test_print_pip_information_sorting(self, mock_distributions: Mock, mock_logger: Mock) -> None:
        """Test that packages are sorted alphabetically."""
        # Create distributions in random order
        mock_dists: list[Mock] = []
        for name, version in [("zlib", "1.0.0"), ("aaa", "2.0.0"), ("middle", "3.0.0")]:
            mock_dist = Mock(spec=Distribution)
            mock_dist.name = name
            mock_dist.version = version
            mock_dists.append(mock_dist)

        mock_distributions.return_value = mock_dists

        print_pip_information()

        # Verify packages are logged in sorted order
        self.assertEqual(mock_logger.debug.call_count, 3)
        calls: list[str] = [call[0][0] for call in mock_logger.debug.call_args_list]
        self.assertEqual(calls[0], "'aaa' == 2.0.0")
        self.assertEqual(calls[1], "'middle' == 3.0.0")
        self.assertEqual(calls[2], "'zlib' == 1.0.0")


class TestPrintEncoding(unittest.TestCase):
    """Test print_encoding function."""

    @patch("python_sbb_polarion.util.environment.logger")
    @patch("python_sbb_polarion.util.environment.locale")
    def test_print_encoding(self, mock_locale: Mock, mock_logger: Mock) -> None:
        """Test that preferred encoding is logged."""
        mock_locale.getpreferredencoding.return_value = "UTF-8"

        print_encoding()

        mock_logger.info.assert_called_once()
        call_args: tuple[Any, ...] = mock_logger.info.call_args[0]
        self.assertIn("Preferred encoding:", call_args[0])
        self.assertEqual(call_args[1], "UTF-8")

    @patch("python_sbb_polarion.util.environment.logger")
    @patch("python_sbb_polarion.util.environment.locale")
    def test_print_encoding_different_encodings(self, mock_locale: Mock, mock_logger: Mock) -> None:
        """Test with different encoding values."""
        test_encodings: list[str] = ["UTF-8", "ASCII", "ISO-8859-1", "Windows-1252"]

        for encoding in test_encodings:
            mock_logger.reset_mock()
            mock_locale.getpreferredencoding.return_value = encoding

            print_encoding()

            call_args: tuple[Any, ...] = mock_logger.info.call_args[0]
            self.assertEqual(call_args[1], encoding)

    @patch("python_sbb_polarion.util.environment.logger")
    def test_print_encoding_real_locale(self, mock_logger: Mock) -> None:
        """Test with real locale module (integration-like test)."""
        print_encoding()

        mock_logger.info.assert_called_once()
        call_args: tuple[Any, ...] = mock_logger.info.call_args[0]
        # Verify the format but use actual encoding from system
        self.assertIn("Preferred encoding:", call_args[0])
        # Second argument should be a string (the encoding)
        self.assertIsInstance(call_args[1], str)
        # It should match the actual preferred encoding
        self.assertEqual(call_args[1], locale.getpreferredencoding())


if __name__ == "__main__":
    unittest.main()
