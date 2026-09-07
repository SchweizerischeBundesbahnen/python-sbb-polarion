"""Unit tests for the teardown helpers."""

from __future__ import annotations

import logging
import unittest
from unittest.mock import patch

from python_sbb_polarion.testing.tear_down import _describe, tear_down_all


class _Recorder:
    """Teardown target that records whether it ran, and can fail on demand."""

    def __init__(self, error: Exception | None = None) -> None:
        self.error: Exception | None = error
        self.torn_down: bool = False

    def tear_down(self) -> None:
        self.torn_down = True
        if self.error:
            raise self.error


class TestTearDownAll(unittest.TestCase):
    """Test tear_down_all."""

    def test_returns_true_when_every_target_succeeds(self) -> None:
        """Test tear_down_all tears every target down and reports success."""
        first: _Recorder = _Recorder()
        second: _Recorder = _Recorder()

        self.assertTrue(tear_down_all(first, second))
        self.assertTrue(first.torn_down)
        self.assertTrue(second.torn_down)

    def test_runs_every_target_after_a_failure(self) -> None:
        """Test a failing target neither stops the others nor hides its own failure."""
        failing: _Recorder = _Recorder(RuntimeError("stuck job"))
        following: _Recorder = _Recorder()

        with self.assertLogs("python_sbb_polarion.testing.tear_down", level=logging.ERROR) as logs:
            succeeded: bool = tear_down_all(failing, following)

        self.assertFalse(succeeded)
        self.assertTrue(following.torn_down)
        self.assertIn("stuck job", "\n".join(logs.output))

    def test_accepts_no_targets(self) -> None:
        """Test tear_down_all reports success when there is nothing to tear down."""
        self.assertTrue(tear_down_all())

    def test_describes_a_temp_project_by_its_location(self) -> None:
        """Test the log names a temporary project by its repository location."""

        class FakeTempProject:
            """Stands in for TempProject, which needs a live API to build."""

            temp_project_location: str = "Demo Projects/elibrary_st_1234"

            def tear_down(self) -> None:
                """Do nothing."""

        target: FakeTempProject = FakeTempProject()
        with patch("python_sbb_polarion.testing.tear_down.TempProject", FakeTempProject):
            self.assertEqual(_describe(target), "project 'Demo Projects/elibrary_st_1234'")

    def test_describes_other_targets_by_class_name(self) -> None:
        """Test a target that is not a temporary project is named by its class."""
        self.assertEqual(_describe(_Recorder()), "_Recorder")


if __name__ == "__main__":
    unittest.main()
