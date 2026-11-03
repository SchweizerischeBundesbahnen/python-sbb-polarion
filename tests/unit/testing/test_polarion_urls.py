"""Unit tests for PolarionUrls."""

from __future__ import annotations

import unittest

from python_sbb_polarion.testing.polarion_urls import PolarionUrls


class TestPolarionUrls(unittest.TestCase):
    """Test PolarionUrls class."""

    def test_page_in_default_space(self) -> None:
        """Test that the default space is left out."""
        self.assertEqual("/polarion/#/project/elibrary/wiki/My%20Page", PolarionUrls.page("elibrary", "My Page"))

    def test_page_in_space(self) -> None:
        """Test a page in another space."""
        self.assertEqual("/polarion/#/project/elibrary/wiki/Testing/My%20Doc", PolarionUrls.page("elibrary", "My Doc", space="Testing"))

    def test_work_item(self) -> None:
        """Test a work item."""
        self.assertEqual("/polarion/#/project/elibrary/workitem?id=EL-1", PolarionUrls.work_item("elibrary", "EL-1"))

    def test_project_home(self) -> None:
        """Test a project home."""
        self.assertEqual("/polarion/#/project/elibrary", PolarionUrls.project_home("elibrary"))
