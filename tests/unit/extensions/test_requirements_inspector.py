"""Unit tests for Requirements Inspector API."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import Mock

from python_sbb_polarion.extensions.requirements_inspector import PolarionRequirementsInspectorApi


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class TestPolarionRequirementsInspectorApi(unittest.TestCase):
    """Test PolarionRequirementsInspectorApi class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_connection = Mock()
        self.api = PolarionRequirementsInspectorApi(self.mock_connection)

    def test_init(self) -> None:
        """Test initialization."""
        self.assertEqual(self.api.extension_name, "requirements-inspector")
        self.assertEqual(self.api.polarion_connection, self.mock_connection)

    def test_inspect_workitems(self) -> None:
        """Test inspect workitems."""
        mock_response = Mock()
        self.mock_connection.api_request_post.return_value = mock_response

        data: JsonDict = {
            "ids": ["WI-1", "WI-2"],
            "projectId": "PROJ",
            "inspectFields": ["title", "description"],
        }
        response: Response = self.api.inspect_workitems(data)

        self.assertEqual(response, mock_response)
        self.mock_connection.api_request_post.assert_called_once_with(
            f"{self.api.rest_api_url}/inspect/workitems",
            data=data,
        )


if __name__ == "__main__":
    unittest.main()
