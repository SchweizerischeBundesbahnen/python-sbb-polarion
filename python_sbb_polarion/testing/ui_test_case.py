"""Test case for checks of the Polarion UI. Needs the ``ui`` extra of this package."""

from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING, ClassVar

import cv2

from python_sbb_polarion.testing.generic_test_case import GenericTestCase
from python_sbb_polarion.testing.image_comparison import ImageDifference, compare_images, save_difference_image
from python_sbb_polarion.testing.ui_browser import PolarionUiBrowser
from python_sbb_polarion.util.argparse import get_script_arguments


if TYPE_CHECKING:
    import argparse
    from pathlib import Path

    import numpy as np
    from numpy.typing import NDArray

    from python_sbb_polarion.testing.image_comparison import IgnoreRegion


UPDATE_SNAPSHOTS_VARIABLE: str = "UPDATE_SNAPSHOTS"


class UiTestCase(GenericTestCase):
    """Mixin for system tests that compare screenshots with expected images.

    Put it before the test case of the extension, for example ``class MyTest(UiTestCase, MyExtensionTestCase)``,
    and set ``expected_folder`` and ``output_folder``. The browser logs in with ``--app_username`` and ``--app_password``,
    or the environment variables ``APP_USERNAME`` and ``APP_PASSWORD``.

    With the environment variable ``UPDATE_SNAPSHOTS=1`` the generated images replace the expected ones.
    The browser always runs in the same container, so such an image is valid on every machine.
    """

    expected_folder: ClassVar[Path]
    output_folder: ClassVar[Path]
    ui_browser: ClassVar[PolarionUiBrowser]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        args: argparse.Namespace = get_script_arguments()
        url: str | None = cls.get_parameter("APP_URL", args.app_url)
        username: str | None = cls.get_parameter("APP_USERNAME", args.app_username)
        password: str | None = cls.get_parameter("APP_PASSWORD", args.app_password)
        if not url or not username or not password:
            raise ValueError("UI tests need 'app_url', 'app_username' and 'app_password': use the arguments or the APP_URL, APP_USERNAME and APP_PASSWORD env variables")
        cls.ui_browser = PolarionUiBrowser(url, username, password)
        cls.addClassCleanup(cls.ui_browser.close)
        cls.ui_browser.start()

    def output_image(self, name: str) -> Path:
        """Get the path of a generated image.

        Args:
            name: Name of the image without extension

        Returns:
            Path: Path in the output folder
        """
        return self.output_folder / f"{name}.png"

    def assert_image_matches_expected(self, name: str, ignore_regions: list[IgnoreRegion] | None = None) -> None:
        """Compare a generated image with the expected image of the same name.

        Without an expected image, the test fails and names the generated one. Check it, then run with ``UPDATE_SNAPSHOTS=1``.

        Args:
            name: Name of the image without extension
            ignore_regions: Rectangles to leave out of the comparison
        """
        actual: Path = self.output_image(name)
        expected: Path = self.expected_folder / f"{name}.png"
        if os.environ.get(UPDATE_SNAPSHOTS_VARIABLE) == "1":
            expected.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(actual, expected)
            return
        if not expected.is_file():
            self.fail(f"No expected image '{expected}'. Check '{actual}', then run with {UPDATE_SNAPSHOTS_VARIABLE}=1.")

        difference: ImageDifference = compare_images(expected, actual, ignore_regions=ignore_regions)
        if difference.image is None:
            self.fail(f"'{actual}' has size {_size(actual)}, expected {_size(expected)} of '{expected}'")
        if difference.pixels > 0:
            save_difference_image(difference.image, self.output_folder / f"{name}_diff.png")
            self.fail(f"'{actual}' differs from '{expected}': {difference.pixels} pixels")


def _size(path: Path) -> str:
    image: NDArray[np.uint8] | None = cv2.imread(str(path))  # ty: ignore[invalid-assignment]
    if image is None:
        return "unknown"
    return f"{image.shape[1]}x{image.shape[0]}"
