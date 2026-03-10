"""Unit tests for Polarion Extension API Factory."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING, ClassVar
from unittest.mock import Mock

from python_sbb_polarion.core.factory import ExtensionApiFactory


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionRestApiConnection


class TestExtensionApiFactory(unittest.TestCase):
    """Test ExtensionApiFactory class."""

    EXPECTED_EXTENSIONS: ClassVar[set[str]] = {
        "aad-synchronizer",
        "admin-utility",
        "api-extender",
        "collection-checker",
        "cucumber",
        "diff-tool",
        "dms-doc-connector",
        "dms-wi-connector",
        "excel-importer",
        "fake-services",
        "interceptor-manager",
        "json-editor",
        "mailworkflow",
        "pdf-exporter",
        "docx-exporter",
        "requirements-inspector",
        "strictdoc-exporter",
        "test-data",
        "xml-repair",
    }

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection: PolarionRestApiConnection = Mock(spec="PolarionRestApiConnection")

    def test_invalid_extension_name_raises_value_error(self) -> None:
        """Test that invalid extension name raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ExtensionApiFactory.get_extension_api_by_name("invalid-extension", self.mock_connection)

        self.assertIn("Invalid extension name", str(context.exception))

    def test_empty_extension_name_raises_value_error(self) -> None:
        """Test that empty extension name raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ExtensionApiFactory.get_extension_api_by_name("", self.mock_connection)

        self.assertIn("Invalid extension name", str(context.exception))

    def test_all_extensions_are_registered(self) -> None:
        """Test that all expected extensions are registered in the factory."""
        # Access the private class variable to verify all extensions are registered
        registered_extensions: set[str] = set(ExtensionApiFactory._ExtensionApiFactory__extension_api_classes.keys())  # type: ignore[attr-defined]

        self.assertEqual(registered_extensions, self.EXPECTED_EXTENSIONS)
        self.assertEqual(len(registered_extensions), 19, "Factory should have exactly 19 registered extensions")

    def test_all_registered_extensions_can_be_created(self) -> None:
        """Test that all registered extensions can be successfully instantiated."""
        for extension_name in self.EXPECTED_EXTENSIONS:
            with self.subTest(extension=extension_name):
                api: PolarionGenericExtensionApi = ExtensionApiFactory.get_extension_api_by_name(extension_name, self.mock_connection)
                self.assertIsNotNone(api)
                self.assertEqual(api.polarion_connection, self.mock_connection)


if __name__ == "__main__":
    unittest.main()
