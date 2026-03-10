"""Unit tests for AAD Synchronizer API."""

from __future__ import annotations

import unittest
from unittest.mock import Mock

from python_sbb_polarion.extensions.aad_synchronizer import PolarionAadSynchronizerApi


class TestPolarionAadSynchronizerApi(unittest.TestCase):
    """Test PolarionAadSynchronizerApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionAadSynchronizerApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "aad-synchronizer")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)


if __name__ == "__main__":
    unittest.main()
