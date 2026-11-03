"""Pixel comparison of images. Needs the ``ui`` extra of this package."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import cv2
import numpy as np


if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray


# Rendering noise such as anti-aliasing stays below this difference in each color channel.
TOLERANCE: int = 10

# (left, top, right, bottom) in pixels, with the origin at the top left corner
IgnoreRegion = tuple[int, int, int, int]


class ImageDifference(NamedTuple):
    """Result of an image comparison.

    Attributes:
        pixels: Number of different pixels, infinity if the images have different sizes
        image: Image of the differences, None if the images have different sizes
    """

    pixels: int | float
    image: NDArray[np.uint8] | None


def compare_images(expected_path: Path, actual_path: Path, ignore_regions: list[IgnoreRegion] | None = None) -> ImageDifference:
    """Compare two images.

    Args:
        expected_path: Path to the expected image
        actual_path: Path to the actual image
        ignore_regions: Rectangles to leave out of the comparison

    Returns:
        ImageDifference: Number of different pixels and the image of the differences

    Raises:
        ValueError: If an image cannot be read
    """
    expected: NDArray[np.uint8] | None = cv2.imread(str(expected_path))  # ty: ignore[invalid-assignment]
    actual: NDArray[np.uint8] | None = cv2.imread(str(actual_path))  # ty: ignore[invalid-assignment]
    if expected is None or actual is None:
        raise ValueError(f"Cannot read images: '{expected_path}' or '{actual_path}'")

    if expected.shape != actual.shape:
        return ImageDifference(float("inf"), None)

    difference: NDArray[np.uint8] = np.asarray(cv2.absdiff(expected, actual), dtype=np.uint8)
    for left, top, right, bottom in ignore_regions or []:
        difference[max(top, 0) : max(bottom, 0), max(left, 0) : max(right, 0)] = 0

    # Zero the noise, so the count and the saved image of the differences agree
    difference[difference.max(axis=2) <= TOLERANCE] = 0
    return ImageDifference(int(np.count_nonzero(difference.any(axis=2))), difference)


def save_difference_image(difference: NDArray[np.uint8], path: Path) -> None:
    """Save an image in which every different pixel is blue.

    Args:
        difference: Image of the differences
        path: Path of the image to write
    """
    highlighted: NDArray[np.uint8] = difference.copy()
    highlighted[(highlighted != 0).any(axis=2)] = [255, 0, 0]
    cv2.imwrite(str(path), highlighted)
