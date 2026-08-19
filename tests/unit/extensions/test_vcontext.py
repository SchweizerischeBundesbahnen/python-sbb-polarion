"""Unit tests for Wiki Velocity Context API."""

from __future__ import annotations

import unittest
from unittest.mock import Mock

from python_sbb_polarion.extensions.vcontext import PolarionVContextApi


class TestPolarionVContextApi(unittest.TestCase):
    """Test PolarionVContextApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionVContextApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "vcontext")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    def test_automatic_module_name(self) -> None:
        """Test the custom (com.polarion.alm.*) automatic module name is reported."""
        self.assertEqual(self.api.automatic_module_name, "com.polarion.alm.extension.vcontext")


if __name__ == "__main__":
    unittest.main()
