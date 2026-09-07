"""Teardown helpers for system test runners."""

from __future__ import annotations

import logging
from typing import Protocol

from python_sbb_polarion.testing.temp_project import TempProject


logger = logging.getLogger(__name__)


class TearDownable(Protocol):
    """Anything a test run releases at its end, such as a TempProject or a TestContainersHelper."""

    def tear_down(self) -> None:
        """Release the resource."""


def tear_down_all(*targets: TearDownable | None) -> bool:
    """Tear down every target, whatever the outcome of the ones before it.

    A test runner tears down in a finally block, where the first raising step would skip
    all the steps after it and leave temporary projects or a container behind. Here every
    step runs, and a failing one is logged with its traceback. What a failure means is up
    to the caller, typically::

        finally:
            if not tear_down_all(elibrary, drivepilot, testcontainers_helper):
                sys.exit(1)

    A None target is skipped rather than reported: the same finally block runs after a
    setup that failed halfway, where a runner holds its not-yet-created resources as None.

    Args:
        targets: The objects to tear down, in the given order. None stands for a resource
            that was never created and is skipped

    Returns:
        bool: True when every target that exists was torn down
    """
    succeeded: bool = True
    for target in targets:
        if target is None:
            continue
        try:
            target.tear_down()
        # A broad catch is the point here: one failing step must not stop the others.
        except Exception:
            logger.exception("Teardown of %s failed", _describe(target))
            succeeded = False
    return succeeded


def _describe(target: TearDownable) -> str:
    """Name a teardown target for the log message.

    Returns:
        str: The repository location of a temporary project, the class name for anything else
    """
    if isinstance(target, TempProject):
        return f"project '{target.temp_project_location}'"
    return type(target).__name__
