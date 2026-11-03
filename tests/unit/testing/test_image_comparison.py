"""Unit tests for the image comparison."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from python_sbb_polarion.testing.image_comparison import ImageDifference, compare_images, save_difference_image


def _write_image(path: Path, height: int = 20, width: int = 30, gray: int = 255) -> Path:
    image: np.ndarray = np.full((height, width, 3), gray, dtype=np.uint8)
    cv2.imwrite(str(path), image)
    return path


class TestCompareImages(unittest.TestCase):
    """Test compare_images."""

    def setUp(self) -> None:
        self.folder: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path: Path = Path(self.folder.name)

    def test_equal_images_have_no_difference(self) -> None:
        """Test two equal images."""
        expected: Path = _write_image(self.path / "expected.png")
        actual: Path = _write_image(self.path / "actual.png")

        self.assertEqual(0, compare_images(expected, actual).pixels)

    def test_counts_pixels_above_the_tolerance(self) -> None:
        """Test that each pixel with a clear difference counts once."""
        expected: Path = _write_image(self.path / "expected.png")
        image: np.ndarray = np.full((20, 30, 3), 255, dtype=np.uint8)
        image[0:2, 0:3] = 0
        actual: Path = self.path / "actual.png"
        cv2.imwrite(str(actual), image)

        difference: ImageDifference = compare_images(expected, actual)

        self.assertEqual(6, difference.pixels)
        self.assertIsNotNone(difference.image)

    def test_ignores_differences_within_the_tolerance(self) -> None:
        """Test that anti-aliasing noise does not count."""
        expected: Path = _write_image(self.path / "expected.png", gray=200)
        actual: Path = _write_image(self.path / "actual.png", gray=205)

        self.assertEqual(0, compare_images(expected, actual).pixels)

    def test_leaves_ignore_regions_out(self) -> None:
        """Test that a difference inside an ignore region does not count."""
        expected: Path = _write_image(self.path / "expected.png")
        image: np.ndarray = np.full((20, 30, 3), 255, dtype=np.uint8)
        image[5:10, 5:10] = 0
        actual: Path = self.path / "actual.png"
        cv2.imwrite(str(actual), image)

        self.assertEqual(0, compare_images(expected, actual, ignore_regions=[(5, 5, 10, 10)]).pixels)

    def test_images_of_different_sizes_are_not_comparable(self) -> None:
        """Test two images of different sizes."""
        expected: Path = _write_image(self.path / "expected.png")
        actual: Path = _write_image(self.path / "actual.png", height=21)

        difference: ImageDifference = compare_images(expected, actual)

        self.assertEqual(float("inf"), difference.pixels)
        self.assertIsNone(difference.image)

    def test_missing_image_raises(self) -> None:
        """Test an image that cannot be read."""
        expected: Path = _write_image(self.path / "expected.png")

        with self.assertRaises(ValueError):
            compare_images(expected, self.path / "missing.png")


class TestSaveDifferenceImage(unittest.TestCase):
    """Test save_difference_image."""

    def test_marks_different_pixels_blue(self) -> None:
        """Test that only the different pixels become blue."""
        difference: np.ndarray = np.zeros((4, 4, 3), dtype=np.uint8)
        difference[1, 2] = [0, 40, 0]

        with tempfile.TemporaryDirectory() as folder:
            path: Path = Path(folder) / "diff.png"
            save_difference_image(difference, path)
            saved: np.ndarray = cv2.imread(str(path))  # ty: ignore[invalid-assignment]

        self.assertEqual([255, 0, 0], saved[1, 2].tolist())
        self.assertEqual([0, 0, 0], saved[0, 0].tolist())
