"""Unit tests for Violation class."""

from __future__ import annotations

import unittest
from pathlib import Path

from python_sbb_polarion.linter.code_style_linter import Violation


class TestViolation(unittest.TestCase):
    """Test Violation dataclass."""

    def test_violation_creation(self) -> None:
        """Test creating a Violation instance."""
        v = Violation(
            file=Path("test.py"),
            line=10,
            col=5,
            code="PSP001",
            message="Test message",
        )
        self.assertEqual(v.file, Path("test.py"))
        self.assertEqual(v.line, 10)
        self.assertEqual(v.col, 5)
        self.assertEqual(v.code, "PSP001")
        self.assertEqual(v.message, "Test message")

    def test_violation_str(self) -> None:
        """Test Violation string representation."""
        v = Violation(
            file=Path("src/module.py"),
            line=42,
            col=8,
            code="PSP005",
            message="Dict must have each key-value pair on a separate line",
        )
        result: str = str(v)
        expected_path: str = str(Path("src/module.py"))
        self.assertEqual(result, f"{expected_path}:42:8: PSP005 Dict must have each key-value pair on a separate line")

    def test_violation_is_frozen(self) -> None:
        """Test that Violation is immutable (frozen dataclass)."""
        v = Violation(
            file=Path("test.py"),
            line=1,
            col=0,
            code="PSP001",
            message="Test",
        )
        with self.assertRaises(AttributeError):
            v.line = 2  # type: ignore[misc]

    def test_violation_equality(self) -> None:
        """Test Violation equality."""
        v1 = Violation(
            file=Path("test.py"),
            line=1,
            col=0,
            code="PSP001",
            message="Test",
        )
        v2 = Violation(
            file=Path("test.py"),
            line=1,
            col=0,
            code="PSP001",
            message="Test",
        )
        self.assertEqual(v1, v2)

    def test_violation_inequality(self) -> None:
        """Test Violation inequality."""
        v1 = Violation(
            file=Path("test.py"),
            line=1,
            col=0,
            code="PSP001",
            message="Test",
        )
        v2 = Violation(
            file=Path("test.py"),
            line=2,
            col=0,
            code="PSP001",
            message="Test",
        )
        self.assertNotEqual(v1, v2)

    def test_violation_hash(self) -> None:
        """Test Violation can be used in sets (hashable)."""
        v1 = Violation(
            file=Path("test.py"),
            line=1,
            col=0,
            code="PSP001",
            message="Test",
        )
        v2 = Violation(
            file=Path("test.py"),
            line=1,
            col=0,
            code="PSP001",
            message="Test",
        )
        violations: set[Violation] = {v1, v2}
        self.assertEqual(len(violations), 1)


if __name__ == "__main__":
    unittest.main()
