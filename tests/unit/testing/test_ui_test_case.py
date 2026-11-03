"""Unit tests for UiTestCase."""

from __future__ import annotations

import argparse
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import cv2
import numpy as np

from python_sbb_polarion.testing.ui_test_case import UPDATE_SNAPSHOTS_VARIABLE, UiTestCase


MODULE: str = "python_sbb_polarion.testing.ui_test_case"


def _write_image(path: Path, gray: int = 255) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), np.full((10, 10, 3), gray, dtype=np.uint8))


class _SnapshotTest(UiTestCase):
    # A fixture for the tests below, not a test of its own
    __test__ = False

    def runTest(self) -> None:  # noqa: N802 - the name unittest calls
        """Empty test, so the case can be created."""


class TestAssertImageMatchesExpected(unittest.TestCase):
    """Test assert_image_matches_expected."""

    def setUp(self) -> None:
        folder: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        _SnapshotTest.expected_folder = Path(folder.name) / "expected"
        _SnapshotTest.output_folder = Path(folder.name) / "output"
        self.case: _SnapshotTest = _SnapshotTest()
        self.enterContext(patch.dict(os.environ, {}, clear=False))
        os.environ.pop(UPDATE_SNAPSHOTS_VARIABLE, None)

    def test_equal_images_pass(self) -> None:
        """Test that an equal image passes."""
        _write_image(self.case.output_image("page"))
        _write_image(_SnapshotTest.expected_folder / "page.png")

        self.case.assert_image_matches_expected("page")

    def test_different_image_fails_and_saves_the_difference(self) -> None:
        """Test that a different image fails and leaves an image of the differences."""
        _write_image(self.case.output_image("page"), gray=0)
        _write_image(_SnapshotTest.expected_folder / "page.png")

        with self.assertRaises(AssertionError):
            self.case.assert_image_matches_expected("page")
        self.assertTrue((_SnapshotTest.output_folder / "page_diff.png").is_file())

    def test_missing_expected_image_fails(self) -> None:
        """Test that a missing expected image fails and names the update variable."""
        _write_image(self.case.output_image("page"))

        with self.assertRaises(AssertionError) as context:
            self.case.assert_image_matches_expected("page")
        self.assertIn(UPDATE_SNAPSHOTS_VARIABLE, str(context.exception))

    def test_update_mode_writes_the_expected_image(self) -> None:
        """Test that the update mode copies the generated image instead of comparing."""
        _write_image(self.case.output_image("page"), gray=0)
        _write_image(_SnapshotTest.expected_folder / "page.png")
        os.environ[UPDATE_SNAPSHOTS_VARIABLE] = "1"

        self.case.assert_image_matches_expected("page")

        os.environ.pop(UPDATE_SNAPSHOTS_VARIABLE)
        self.case.assert_image_matches_expected("page")


class TestSetUpClass(unittest.TestCase):
    """Test that setUpClass starts the browser with the credentials."""

    def setUp(self) -> None:
        self.enterContext(patch.dict(os.environ, {}, clear=True))

    def _arguments(self, **values: str | None) -> argparse.Namespace:
        defaults: dict[str, str | None] = {"app_url": None, "app_username": None, "app_password": None}
        defaults.update(values)
        return argparse.Namespace(**defaults)

    def test_starts_the_browser(self) -> None:
        """Test that the browser gets the URL and the credentials and closes with the class."""
        arguments: argparse.Namespace = self._arguments(app_url="http://localhost", app_username="user", app_password="secret")
        with patch(f"{MODULE}.get_script_arguments", return_value=arguments), patch(f"{MODULE}.PolarionUiBrowser") as browser_class:
            _SnapshotTest.setUpClass()
            _SnapshotTest.doClassCleanups()

        browser_class.assert_called_once_with("http://localhost", "user", "secret")
        browser_class.return_value.start.assert_called_once_with()
        browser_class.return_value.close.assert_called_once_with()

    def test_environment_gives_the_credentials(self) -> None:
        """Test that the environment variables work without arguments."""
        os.environ.update({"APP_URL": "http://localhost", "APP_USERNAME": "user", "APP_PASSWORD": "secret"})
        with patch(f"{MODULE}.get_script_arguments", return_value=self._arguments()), patch(f"{MODULE}.PolarionUiBrowser") as browser_class:
            _SnapshotTest.setUpClass()
            _SnapshotTest.doClassCleanups()

        browser_class.assert_called_once_with("http://localhost", "user", "secret")

    def test_missing_password_raises(self) -> None:
        """Test that missing credentials stop the test class."""
        arguments: argparse.Namespace = self._arguments(app_url="http://localhost", app_username="user")
        with patch(f"{MODULE}.get_script_arguments", return_value=arguments), patch(f"{MODULE}.PolarionUiBrowser") as browser_class, self.assertRaises(ValueError):
            _SnapshotTest.setUpClass()

        browser_class.assert_not_called()
