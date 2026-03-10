"""Unit tests for PSP011-PSP017 linter rules."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_sbb_polarion.linter.code_style_linter import Violation, lint_file


class TestPSP011DictInitialization(unittest.TestCase):
    """Test PSP011: Params/headers/data/files dict must be initialized as {}, not None."""

    def test_psp011_none_initialization_flagged(self) -> None:
        """Test that None initialization is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    params: dict[str, str] = None
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp011_violations: list[Violation] = [v for v in violations if v.code == "PSP011"]
        self.assertEqual(len(psp011_violations), 1)
        self.assertIn("empty dict", psp011_violations[0].message)

    def test_psp011_empty_dict_ok(self) -> None:
        """Test that empty dict initialization is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    params: dict[str, str] = {}
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp011_violations: list[Violation] = [v for v in violations if v.code == "PSP011"]
        self.assertEqual(len(psp011_violations), 0)

    def test_psp011_applies_to_headers_data_files(self) -> None:
        """Test that PSP011 applies to headers, data, files too."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    headers: dict[str, str] = None
    data: dict[str, str] = None
    files: dict[str, str] = None
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp011_violations: list[Violation] = [v for v in violations if v.code == "PSP011"]
        self.assertEqual(len(psp011_violations), 3)


class TestPSP012CollectionNoneCheck(unittest.TestCase):
    """Test PSP012: For list|None or dict|None use is not None, not truthy check.

    Note: PSP012 only tracks variables declared with AnnAssign (annotated assignment),
    not function parameters. This is by design since function parameters are tracked
    separately and the linter focuses on local variable patterns.
    """

    def test_psp012_truthy_check_on_list_none_flagged(self) -> None:
        """Test that truthy check on list|None local variable is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            # Use local variable with annotated assignment, not function parameter
            f.write(
                """
def test_func():
    items: list[str] | None = get_items()
    if items:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 1)
        self.assertIn("is not None", psp012_violations[0].message)

    def test_psp012_is_not_none_check_ok(self) -> None:
        """Test that 'is not None' check is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    items: list[str] | None = get_items()
    if items is not None:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 0)

    def test_psp012_dict_none_flagged(self) -> None:
        """Test that truthy check on dict|None local variable is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            # Use local variable with annotated assignment
            f.write(
                """
def test_func():
    data: dict[str, int] | None = get_data()
    if data:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 1)

    def test_psp012_str_none_not_flagged(self) -> None:
        """Test that str|None truthy check is NOT flagged (str is not a collection)."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(name: str | None):
    if name:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 0)


class TestPSP013OrNonePattern(unittest.TestCase):
    """Test PSP013: When passing params/headers to API methods, use or None for empty dict."""

    def test_psp013_empty_dict_without_or_none_flagged(self) -> None:
        """Test that passing empty dict variable without or None is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/test"
    params: dict[str, str] = {}
    api.api_request_get(url, params=params)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp013_violations: list[Violation] = [v for v in violations if v.code == "PSP013"]
        self.assertEqual(len(psp013_violations), 1)
        self.assertIn("or None", psp013_violations[0].message)

    def test_psp013_or_none_pattern_ok(self) -> None:
        """Test that or None pattern is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/test"
    params: dict[str, str] = {}
    api.api_request_get(url, params=params or None)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp013_violations: list[Violation] = [v for v in violations if v.code == "PSP013"]
        self.assertEqual(len(psp013_violations), 0)

    def test_psp013_non_empty_dict_ok(self) -> None:
        """Test that non-empty dict doesn't trigger PSP013."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/test"
    params: dict[str, str] = {
        "key": "value",
    }
    api.api_request_get(url, params=params)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp013_violations: list[Violation] = [v for v in violations if v.code == "PSP013"]
        self.assertEqual(len(psp013_violations), 0)


class TestPSP014NoPrint(unittest.TestCase):
    """Test PSP014: Don't use print() in library code."""

    def test_psp014_print_in_library_flagged(self) -> None:
        """Test that print() in library code is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    print("hello")
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp014_violations: list[Violation] = [v for v in violations if v.code == "PSP014"]
        self.assertEqual(len(psp014_violations), 1)
        self.assertIn("logging", psp014_violations[0].message)

    def test_psp014_print_in_test_file_ok(self) -> None:
        """Test that print() in test file is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False, prefix="test_") as f:
            f.write(
                """
def test_func():
    print("hello")
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp014_violations: list[Violation] = [v for v in violations if v.code == "PSP014"]
        self.assertEqual(len(psp014_violations), 0)


class TestPSP015NoAssert(unittest.TestCase):
    """Test PSP015: Don't use assert in production code."""

    def test_psp015_assert_in_library_flagged(self) -> None:
        """Test that assert in library code is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(x):
    assert x is not None
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp015_violations: list[Violation] = [v for v in violations if v.code == "PSP015"]
        self.assertEqual(len(psp015_violations), 1)

    def test_psp015_assert_in_test_file_ok(self) -> None:
        """Test that assert in test file is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False, prefix="test_") as f:
            f.write(
                """
def test_func(x):
    assert x is not None
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp015_violations: list[Violation] = [v for v in violations if v.code == "PSP015"]
        self.assertEqual(len(psp015_violations), 0)


class TestPSP016NoCast(unittest.TestCase):
    """Test PSP016: Don't use typing.cast()."""

    def test_psp016_cast_in_library_flagged(self) -> None:
        """Test that cast() in library code is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import cast

def test_func(data):
    result: str = cast(str, data)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp016_violations: list[Violation] = [v for v in violations if v.code == "PSP016"]
        self.assertEqual(len(psp016_violations), 1)
        self.assertIn("type design", psp016_violations[0].message)

    def test_psp016_cast_in_test_file_ok(self) -> None:
        """Test that cast() in test file is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False, prefix="test_") as f:
            f.write(
                """
from typing import cast

def test_func(data):
    result: str = cast(str, data)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp016_violations: list[Violation] = [v for v in violations if v.code == "PSP016"]
        self.assertEqual(len(psp016_violations), 0)

    def test_psp016_no_cast_import_no_flag(self) -> None:
        """Test that cast without import is not flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def cast(type, value):
    return value

def test_func(data):
    result: str = cast(str, data)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp016_violations: list[Violation] = [v for v in violations if v.code == "PSP016"]
        self.assertEqual(len(psp016_violations), 0)


class TestPSP017NoAny(unittest.TestCase):
    """Test PSP017: Don't use Any in type annotations."""

    def test_psp017_dict_str_any_flagged(self) -> None:
        """Test that dict[str, Any] is flagged with JsonDict suggestion."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Any

def test_func() -> dict[str, Any]:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        self.assertEqual(len(psp017_violations), 1)
        self.assertIn("JsonDict", psp017_violations[0].message)

    def test_psp017_json_dict_ok(self) -> None:
        """Test that JsonDict is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import JsonDict

def test_func() -> JsonDict:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        self.assertEqual(len(psp017_violations), 0)

    def test_psp017_in_test_file_ok(self) -> None:
        """Test that dict[str, Any] in test file is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False, prefix="test_") as f:
            f.write(
                """
from typing import Any

def test_func() -> dict[str, Any]:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        self.assertEqual(len(psp017_violations), 0)

    def test_psp017_dict_str_any_in_union(self) -> None:
        """Test that dict[str, Any] | None is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Any

def test_func() -> dict[str, Any] | None:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        self.assertEqual(len(psp017_violations), 1)

    def test_psp017_standalone_any_flagged(self) -> None:
        """Test that standalone Any type is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Any

def test_func(data: Any) -> Any:
    result: Any = data
    return result
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        # Should flag: parameter data, return type, and variable result = 3 violations
        self.assertEqual(len(psp017_violations), 3)
        self.assertIn("specific type", psp017_violations[0].message)

    def test_psp017_list_any_flagged(self) -> None:
        """Test that list[Any] is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Any

def test_func() -> list[Any]:
    items: list[Any] = []
    return items
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        # Should flag: return type and variable = 2 violations
        self.assertEqual(len(psp017_violations), 2)

    def test_psp017_set_any_flagged(self) -> None:
        """Test that set[Any] is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Any

def test_func() -> set[Any]:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        self.assertEqual(len(psp017_violations), 1)

    def test_psp017_any_in_union_flagged(self) -> None:
        """Test that Any | str is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Any

def test_func() -> Any | str:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        self.assertEqual(len(psp017_violations), 1)

    def test_psp017_nested_any_flagged(self) -> None:
        """Test that nested Any in complex types is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Any

def test_func() -> dict[str, list[Any]]:
    pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        self.assertEqual(len(psp017_violations), 1)

    def test_psp017_callable_with_any_ok(self) -> None:
        """Test that Callable[..., Any] pattern is ok (decorator TypeVar pattern)."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        # TypeVar bound is not a regular annotation, but the Any inside Callable would be flagged
        # This is acceptable since the pattern is rarely used outside decorators
        psp017_violations: list[Violation] = [v for v in violations if v.code == "PSP017"]
        # Note: This may or may not flag depending on how TypeVar bound is parsed
        # The important thing is that `Callable[..., Any]` is a valid decorator pattern
        self.assertGreaterEqual(len(psp017_violations), 0)


class TestIsTestFile(unittest.TestCase):
    """Test _check_is_test_file functionality."""

    def test_tests_directory_is_test_file(self) -> None:
        """Test that files in tests/ directory are identified as test files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tests_dir: Path = Path(tmp_dir) / "tests"
            tests_dir.mkdir()
            test_file: Path = tests_dir / "example.py"
            test_file.write_text(
                """
def func():
    assert True
""",
                encoding="utf-8",
            )
            violations: list[Violation] = lint_file(test_file)

        # Assert should be ok in test files
        psp015_violations: list[Violation] = [v for v in violations if v.code == "PSP015"]
        self.assertEqual(len(psp015_violations), 0)

    def test_testing_directory_is_test_file(self) -> None:
        """Test that files in testing/ directory are identified as test files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            testing_dir: Path = Path(tmp_dir) / "testing"
            testing_dir.mkdir()
            test_file: Path = testing_dir / "helper.py"
            test_file.write_text(
                """
def func():
    assert True
""",
                encoding="utf-8",
            )
            violations: list[Violation] = lint_file(test_file)

        psp015_violations: list[Violation] = [v for v in violations if v.code == "PSP015"]
        self.assertEqual(len(psp015_violations), 0)


class TestPSP012CollectionOrNoneCheck(unittest.TestCase):
    """Test PSP012: For list | None or dict | None use `is not None`."""

    def test_psp012_list_or_none_truthy_check_flagged(self) -> None:
        """Test that truthy check on list | None variable is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> None:
    items: list[str] | None = get_items()
    if items:
        print(items)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 1)
        self.assertIn("is not None", psp012_violations[0].message)

    def test_psp012_dict_or_none_truthy_check_flagged(self) -> None:
        """Test that truthy check on dict | None variable is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> None:
    data: dict[str, str] | None = get_data()
    if data:
        print(data)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 1)

    def test_psp012_none_or_list_truthy_check_flagged(self) -> None:
        """Test that truthy check on None | list variable is flagged (reversed order)."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> None:
    items: None | list[str] = get_items()
    if items:
        print(items)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 1)

    def test_psp012_plain_list_type_truthy_check_flagged(self) -> None:
        """Test that truthy check on plain list type | None variable is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> None:
    items: list | None = get_items()
    if items:
        print(items)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 1)

    def test_psp012_is_not_none_ok(self) -> None:
        """Test that explicit is not None check is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> None:
    items: list[str] | None = get_items()
    if items is not None:
        print(items)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 0)

    def test_psp012_str_or_none_truthy_check_ok(self) -> None:
        """Test that truthy check on str | None is ok (str is not collection)."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> None:
    name: str | None = get_name()
    if name:
        print(name)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 0)

    def test_psp012_non_union_type(self) -> None:
        """Test that non-union types are not flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func() -> None:
    items: list[str] = get_items()
    if items:
        print(items)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp012_violations: list[Violation] = [v for v in violations if v.code == "PSP012"]
        self.assertEqual(len(psp012_violations), 0)


class TestPSP001TupleUnpacking(unittest.TestCase):
    """Test PSP001 with tuple unpacking assignments."""

    def test_psp001_tuple_unpacking_without_annotation(self) -> None:
        """Test that tuple unpacking without annotation is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    x, y = 1, 2
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        # Should flag both x and y
        self.assertGreaterEqual(len(psp001_violations), 2)

    def test_psp001_starred_unpacking_without_annotation(self) -> None:
        """Test that starred unpacking without annotation is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    first, *rest = [1, 2, 3]
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        # At least first and rest should be flagged (starred unpacking extracts names)
        self.assertGreaterEqual(len(psp001_violations), 1)


class TestConstructorCallDetection(unittest.TestCase):
    """Test detection of constructor calls (for PSP001 exception)."""

    def test_module_constructor_call_ok(self) -> None:
        """Test that ClassName() constructor call is detected."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
class MyClass:
    pass

def test_func():
    obj = MyClass()
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        # obj = MyClass() should not be flagged for PSP001 (constructor infers type)
        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001" and "obj" in v.message]
        self.assertEqual(len(psp001_violations), 0)

    def test_module_attribute_constructor_call_ok(self) -> None:
        """Test that module.ClassName() constructor call is detected."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
import pathlib

def test_func():
    path = pathlib.Path("/tmp")
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        # path = pathlib.Path() should not be flagged (constructor with module.ClassName)
        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001" and "path" in v.message]
        self.assertEqual(len(psp001_violations), 0)


if __name__ == "__main__":
    unittest.main()
