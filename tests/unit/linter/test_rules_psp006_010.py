"""Unit tests for PSP006-PSP010 linter rules."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_sbb_polarion.linter.code_style_linter import Violation, lint_file


class TestPSP006HttpStatusCodes(unittest.TestCase):
    """Test PSP006: Use HTTPStatus enum instead of numeric codes."""

    def test_psp006_numeric_status_code_in_comparison_flagged(self) -> None:
        """Test that numeric status code in comparison is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(response):
    if response.status_code == 200:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp006_violations: list[Violation] = [v for v in violations if v.code == "PSP006"]
        self.assertEqual(len(psp006_violations), 1)
        self.assertIn("HTTPStatus.OK", psp006_violations[0].message)

    def test_psp006_httpstatus_enum_ok(self) -> None:
        """Test that HTTPStatus enum is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from http import HTTPStatus

def test_func(response):
    if response.status_code == HTTPStatus.OK:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp006_violations: list[Violation] = [v for v in violations if v.code == "PSP006"]
        self.assertEqual(len(psp006_violations), 0)

    def test_psp006_not_flagged_outside_status_code_compare(self) -> None:
        """Test that numeric values not in status_code comparison are ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    timeout: int = 200  # Not a status code
    count: int = 404  # Just a number
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp006_violations: list[Violation] = [v for v in violations if v.code == "PSP006"]
        self.assertEqual(len(psp006_violations), 0)

    def test_psp006_various_status_codes(self) -> None:
        """Test detection of various status codes."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(response):
    if response.status_code == 201:
        pass
    elif response.status_code == 404:
        pass
    elif response.status_code == 500:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp006_violations: list[Violation] = [v for v in violations if v.code == "PSP006"]
        self.assertEqual(len(psp006_violations), 3)
        messages: str = " ".join(v.message for v in psp006_violations)
        self.assertIn("HTTPStatus.CREATED", messages)
        self.assertIn("HTTPStatus.NOT_FOUND", messages)
        self.assertIn("HTTPStatus.INTERNAL_SERVER_ERROR", messages)


class TestPSP007HeaderEnum(unittest.TestCase):
    """Test PSP007: Use Header enum instead of string literals."""

    def test_psp007_string_header_flagged(self) -> None:
        """Test that string header literal is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    headers: dict[str, str] = {
        "Accept": "application/json",
    }
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp007_violations: list[Violation] = [v for v in violations if v.code == "PSP007"]
        self.assertEqual(len(psp007_violations), 1)
        self.assertIn("Header.ACCEPT", psp007_violations[0].message)

    def test_psp007_header_enum_ok(self) -> None:
        """Test that Header enum is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import Header

def test_func():
    headers: dict[str, str] = {
        Header.ACCEPT: "application/json",
    }
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp007_violations: list[Violation] = [v for v in violations if v.code == "PSP007"]
        self.assertEqual(len(psp007_violations), 0)


class TestPSP008MediaTypeEnum(unittest.TestCase):
    """Test PSP008: Use MediaType enum instead of string literals."""

    def test_psp008_string_media_type_flagged(self) -> None:
        """Test that string media type literal is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    content_type: str = "application/json"
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp008_violations: list[Violation] = [v for v in violations if v.code == "PSP008"]
        self.assertEqual(len(psp008_violations), 1)
        self.assertIn("MediaType.JSON", psp008_violations[0].message)

    def test_psp008_media_type_enum_ok(self) -> None:
        """Test that MediaType enum is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import MediaType

def test_func():
    content_type: str = MediaType.JSON
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp008_violations: list[Violation] = [v for v in violations if v.code == "PSP008"]
        self.assertEqual(len(psp008_violations), 0)

    def test_psp008_various_media_types(self) -> None:
        """Test detection of various media types."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    t1: str = "application/json"
    t2: str = "text/html"
    t3: str = "application/pdf"
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp008_violations: list[Violation] = [v for v in violations if v.code == "PSP008"]
        self.assertEqual(len(psp008_violations), 3)


class TestPSP009AuthSchemeEnum(unittest.TestCase):
    """Test PSP009: Use AuthScheme enum instead of string literals."""

    def test_psp009_string_auth_scheme_flagged(self) -> None:
        """Test that string auth scheme literal is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            # Use plain string assignment, not f-string (f-string parts are FormattedValue nodes)
            f.write(
                """
def test_func():
    scheme: str = "Bearer"
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp009_violations: list[Violation] = [v for v in violations if v.code == "PSP009"]
        self.assertEqual(len(psp009_violations), 1)
        self.assertIn("AuthScheme.BEARER", psp009_violations[0].message)

    def test_psp009_auth_scheme_enum_ok(self) -> None:
        """Test that AuthScheme enum is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import AuthScheme

def test_func(token):
    auth: str = f"{AuthScheme.BEARER} {token}"
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp009_violations: list[Violation] = [v for v in violations if v.code == "PSP009"]
        self.assertEqual(len(psp009_violations), 0)


class TestPSP010QuotedTypes(unittest.TestCase):
    """Test PSP010: Use from __future__ import annotations instead of quoted types."""

    def test_psp010_quoted_type_flagged(self) -> None:
        """Test that quoted type annotation is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> "str":
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp010_violations: list[Violation] = [v for v in violations if v.code == "PSP010"]
        self.assertEqual(len(psp010_violations), 1)

    def test_psp010_future_annotations_ok(self) -> None:
        """Test that using future annotations is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from __future__ import annotations

def test_func() -> str:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp010_violations: list[Violation] = [v for v in violations if v.code == "PSP010"]
        self.assertEqual(len(psp010_violations), 0)

    def test_psp010_quoted_in_optional_flagged(self) -> None:
        """Test that quoted type inside Optional is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Optional

def test_func() -> Optional["str"]:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp010_violations: list[Violation] = [v for v in violations if v.code == "PSP010"]
        self.assertEqual(len(psp010_violations), 1)

    def test_psp010_literal_string_not_flagged(self) -> None:
        """Test that strings inside Literal[] are not flagged as types.

        Note: The linter implementation currently checks Literal at the top level,
        but strings inside Tuple elements of Literal["foo", "bar"] may still be
        visited as they're in ast.Tuple. This test documents current behavior.
        """
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from __future__ import annotations
from typing import Literal

def test_func() -> Literal["foo"]:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        # Single-element Literal - should not be flagged
        psp010_violations: list[Violation] = [v for v in violations if v.code == "PSP010"]
        self.assertEqual(len(psp010_violations), 0)

    def test_psp010_already_has_future_annotations(self) -> None:
        """Test message when future annotations already imported but quotes still used."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from __future__ import annotations

def test_func(x: "int") -> "str":
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp010_violations: list[Violation] = [v for v in violations if v.code == "PSP010"]
        self.assertEqual(len(psp010_violations), 2)
        # Check message mentions quotes are unnecessary
        self.assertIn("unnecessary", psp010_violations[0].message.lower())


if __name__ == "__main__":
    unittest.main()
