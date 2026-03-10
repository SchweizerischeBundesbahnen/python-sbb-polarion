"""Unit tests for PSP001-PSP005 linter rules."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_sbb_polarion.linter.code_style_linter import Violation, lint_file


class TestPSP001LocalVariableAnnotation(unittest.TestCase):
    """Test PSP001: All local variables must have type annotations."""

    def test_psp001_unannotated_variable(self) -> None:
        """Test that unannotated local variable is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    x = 1
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 1)
        self.assertIn("'x'", psp001_violations[0].message)

    def test_psp001_annotated_variable_ok(self) -> None:
        """Test that annotated local variable is not flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    x: int = 1
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_function_args_ok(self) -> None:
        """Test that function arguments don't need local annotation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(x: int):
    x = x + 1
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_private_vars_ok(self) -> None:
        """Test that private/underscore variables are ok without annotation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    _private = 1
    __dunder = 2
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_constructor_call_ok(self) -> None:
        """Test that constructor calls don't need annotation (type is obvious)."""
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

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_for_loop_ok(self) -> None:
        """Test that for loop variables don't need annotation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    for i in range(10):
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_with_statement_ok(self) -> None:
        """Test that context manager variables don't need annotation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    with open('test') as f:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_except_handler_ok(self) -> None:
        """Test that exception handler variables don't need annotation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    try:
        pass
    except Exception as e:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_comprehension_ok(self) -> None:
        """Test that comprehension variables don't need annotation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    result: list[int] = [x for x in range(10)]
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp001_walrus_operator_ok(self) -> None:
        """Test that walrus operator variables don't need separate annotation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    if (n := len([1,2,3])) > 2:
        pass
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)


class TestPSP002ApiRequestArgs(unittest.TestCase):
    """Test PSP002: api_request_* arguments must be variables."""

    def test_psp002_inline_dict_flagged(self) -> None:
        """Test that inline dict in api_request call is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/test"
    api.api_request_get(url, headers={"Accept": "application/json"})
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp002_violations: list[Violation] = [v for v in violations if v.code == "PSP002"]
        self.assertEqual(len(psp002_violations), 1)
        self.assertIn("headers", psp002_violations[0].message)

    def test_psp002_variable_ok(self) -> None:
        """Test that variable argument is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/test"
    headers: dict[str, str] = {}
    api.api_request_get(url, headers=headers)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp002_violations: list[Violation] = [v for v in violations if v.code == "PSP002"]
        self.assertEqual(len(psp002_violations), 0)

    def test_psp002_none_ok(self) -> None:
        """Test that None is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/test"
    api.api_request_get(url, headers=None)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp002_violations: list[Violation] = [v for v in violations if v.code == "PSP002"]
        self.assertEqual(len(psp002_violations), 0)


class TestPSP003UrlVariable(unittest.TestCase):
    """Test PSP003: URL must be assigned to a variable."""

    def test_psp003_inline_fstring_flagged(self) -> None:
        """Test that inline f-string URL is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    project_id: str = "test"
    api.api_request_get(f"/api/projects/{project_id}")
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp003_violations: list[Violation] = [v for v in violations if v.code == "PSP003"]
        self.assertEqual(len(psp003_violations), 1)
        self.assertIn("f-string", psp003_violations[0].message)

    def test_psp003_inline_literal_flagged(self) -> None:
        """Test that inline literal URL is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    api.api_request_get("/api/test")
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp003_violations: list[Violation] = [v for v in violations if v.code == "PSP003"]
        self.assertEqual(len(psp003_violations), 1)
        self.assertIn("literal", psp003_violations[0].message)

    def test_psp003_variable_ok(self) -> None:
        """Test that variable URL is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/test"
    api.api_request_get(url)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp003_violations: list[Violation] = [v for v in violations if v.code == "PSP003"]
        self.assertEqual(len(psp003_violations), 0)


class TestPSP004QueryParams(unittest.TestCase):
    """Test PSP004: Query params must use params= dict."""

    def test_psp004_url_with_query_params_flagged(self) -> None:
        """Test that query params in URL are flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    scope: str = "test"
    api.api_request_get(f"/api/items?scope={scope}")
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp004_violations: list[Violation] = [v for v in violations if v.code == "PSP004"]
        self.assertEqual(len(psp004_violations), 1)

    def test_psp004_params_dict_ok(self) -> None:
        """Test that params dict is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func(api):
    url: str = "/api/items"
    params: dict[str, str] = {
        "scope": "test",
    }
    api.api_request_get(url, params=params or None)
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp004_violations: list[Violation] = [v for v in violations if v.code == "PSP004"]
        self.assertEqual(len(psp004_violations), 0)


class TestPSP005DictMultiline(unittest.TestCase):
    """Test PSP005: Dict must have each key-value pair on separate line."""

    def test_psp005_single_line_dict_flagged(self) -> None:
        """Test that single-line dict is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    headers: dict[str, str] = {"Accept": "application/json"}
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertEqual(len(psp005_violations), 1)

    def test_psp005_multiline_dict_ok(self) -> None:
        """Test that multiline dict is ok."""
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

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertEqual(len(psp005_violations), 0)

    def test_psp005_empty_dict_ok(self) -> None:
        """Test that empty dict is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    headers: dict[str, str] = {}
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertEqual(len(psp005_violations), 0)

    def test_psp005_multiple_items_same_line_flagged(self) -> None:
        """Test that multiple items on same line is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    params: dict[str, str] = {"key1": "val1", "key2": "val2"}
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertEqual(len(psp005_violations), 1)

    def test_psp005_nested_dict_single_line_in_jsondict_flagged(self) -> None:
        """Test that nested dict on single line inside JsonDict is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import JsonDict

def test_func():
    data: JsonDict = {"data": {"type": "testruns"}}
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertGreaterEqual(len(psp005_violations), 1)

    def test_psp005_list_with_dict_single_line_in_jsondict_flagged(self) -> None:
        """Test that dict on single line inside a list in JsonDict is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import JsonDict

def test_func():
    data: JsonDict = {"data": [{"type": "testruns"}]}
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertGreaterEqual(len(psp005_violations), 1)

    def test_psp005_properly_formatted_nested_jsondict_ok(self) -> None:
        """Test that properly formatted nested JsonDict is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import JsonDict

def test_func():
    data: JsonDict = {
        "data": {
            "type": "testruns",
        },
    }
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertEqual(len(psp005_violations), 0)

    def test_psp005_properly_formatted_list_with_dict_ok(self) -> None:
        """Test that properly formatted list with dict in JsonDict is ok."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import JsonDict

def test_func():
    data: JsonDict = {
        "data": [
            {
                "type": "testruns",
            },
        ],
    }
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertEqual(len(psp005_violations), 0)

    def test_psp005_nested_dict_in_data_variable_flagged(self) -> None:
        """Test that nested dict in 'data' variable with JsonDict type is flagged."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from python_sbb_polarion.types import JsonDict

def test_func():
    data: JsonDict = {
        "items": [{"id": "123", "name": "test"}],
    }
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp005_violations: list[Violation] = [v for v in violations if v.code == "PSP005"]
        self.assertGreaterEqual(len(psp005_violations), 1)
        self.assertIn("Nested dict", psp005_violations[0].message)


class TestPspIgnoreComment(unittest.TestCase):
    """Test psp-ignore comment functionality."""

    def test_psp_ignore_suppresses_violation(self) -> None:
        """Test that psp-ignore comment suppresses violation."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    x = 1  # psp-ignore: PSP001
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp_ignore_multiple_codes(self) -> None:
        """Test that psp-ignore can suppress multiple codes."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    x = 1  # psp-ignore: PSP001, PSP002
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)

    def test_psp_ignore_with_reason(self) -> None:
        """Test that psp-ignore with reason works."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
def test_func():
    x = 1  # psp-ignore: PSP001 - type inferred from context
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        psp001_violations: list[Violation] = [v for v in violations if v.code == "PSP001"]
        self.assertEqual(len(psp001_violations), 0)


if __name__ == "__main__":
    unittest.main()
