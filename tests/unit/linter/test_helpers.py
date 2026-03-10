"""Unit tests for helper functions in linter module."""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

from python_sbb_polarion.linter.code_style_linter import (
    Violation,
    _contains_query_params,  # noqa: PLC2701
    _get_method_name,  # noqa: PLC2701
    _matches_pattern,  # noqa: PLC2701
    _reconstruct_fstring,  # noqa: PLC2701
    find_python_files,
    lint_file,
)


class TestGetMethodName(unittest.TestCase):
    """Test _get_method_name helper function."""

    def test_get_method_name_attribute(self) -> None:
        """Test extracting method name from attribute access."""
        code: str = "obj.method()"
        tree: ast.AST = ast.parse(code)
        call_node: ast.Call = tree.body[0].value  # type: ignore[attr-defined]
        result: str | None = _get_method_name(call_node)
        self.assertEqual(result, "method")

    def test_get_method_name_simple_call(self) -> None:
        """Test extracting function name from simple call."""
        code: str = "func()"
        tree: ast.AST = ast.parse(code)
        call_node: ast.Call = tree.body[0].value  # type: ignore[attr-defined]
        result: str | None = _get_method_name(call_node)
        self.assertEqual(result, "func")

    def test_get_method_name_complex_call(self) -> None:
        """Test that complex call returns None."""
        code: str = "get_obj()['key']()"
        tree: ast.AST = ast.parse(code)
        call_node: ast.Call = tree.body[0].value  # type: ignore[attr-defined]
        result: str | None = _get_method_name(call_node)
        self.assertIsNone(result)


class TestReconstructFstring(unittest.TestCase):
    """Test _reconstruct_fstring helper function."""

    def test_reconstruct_simple_fstring(self) -> None:
        """Test reconstructing simple f-string."""
        code: str = 'f"/api/test"'
        tree: ast.AST = ast.parse(code)
        fstring_node: ast.JoinedStr = tree.body[0].value  # type: ignore[attr-defined]
        result: str = _reconstruct_fstring(fstring_node)
        self.assertEqual(result, "/api/test")

    def test_reconstruct_fstring_with_placeholder(self) -> None:
        """Test reconstructing f-string with expression."""
        code: str = 'f"/api/projects/{project_id}/items"'
        tree: ast.AST = ast.parse(code)
        fstring_node: ast.JoinedStr = tree.body[0].value  # type: ignore[attr-defined]
        result: str = _reconstruct_fstring(fstring_node)
        self.assertEqual(result, "/api/projects/{...}/items")

    def test_reconstruct_fstring_with_query_params(self) -> None:
        """Test reconstructing f-string with query params."""
        code: str = 'f"/api/items?scope={scope}"'
        tree: ast.AST = ast.parse(code)
        fstring_node: ast.JoinedStr = tree.body[0].value  # type: ignore[attr-defined]
        result: str = _reconstruct_fstring(fstring_node)
        self.assertIn("?", result)


class TestContainsQueryParams(unittest.TestCase):
    """Test _contains_query_params helper function."""

    def test_contains_query_params_with_question_mark(self) -> None:
        """Test detecting ? in string concatenation."""
        code: str = '"/api/test" + "?key=value"'
        tree: ast.AST = ast.parse(code)
        binop_node: ast.BinOp = tree.body[0].value  # type: ignore[attr-defined]
        result: bool = _contains_query_params(binop_node)
        self.assertTrue(result)

    def test_contains_query_params_with_ampersand(self) -> None:
        """Test detecting & in string concatenation."""
        code: str = '"/api/test" + "&key=value"'
        tree: ast.AST = ast.parse(code)
        binop_node: ast.BinOp = tree.body[0].value  # type: ignore[attr-defined]
        result: bool = _contains_query_params(binop_node)
        self.assertTrue(result)

    def test_contains_query_params_no_params(self) -> None:
        """Test no query params detected."""
        code: str = '"/api/test" + "/items"'
        tree: ast.AST = ast.parse(code)
        binop_node: ast.BinOp = tree.body[0].value  # type: ignore[attr-defined]
        result: bool = _contains_query_params(binop_node)
        self.assertFalse(result)

    def test_contains_query_params_nested(self) -> None:
        """Test detecting query params in nested concatenation."""
        code: str = '"/api" + "/test" + "?key=value"'
        tree: ast.AST = ast.parse(code)
        binop_node: ast.BinOp = tree.body[0].value  # type: ignore[attr-defined]
        result: bool = _contains_query_params(binop_node)
        self.assertTrue(result)

    def test_contains_query_params_left_side(self) -> None:
        """Test detecting ? on left side of concatenation."""
        code: str = '"?key=value" + "/api/test"'
        tree: ast.AST = ast.parse(code)
        binop_node: ast.BinOp = tree.body[0].value  # type: ignore[attr-defined]
        result: bool = _contains_query_params(binop_node)
        self.assertTrue(result)

    def test_contains_query_params_nested_left(self) -> None:
        """Test detecting query params in nested left concatenation."""
        code: str = '("?key=value" + "/api") + "/test"'
        tree: ast.AST = ast.parse(code)
        binop_node: ast.BinOp = tree.body[0].value  # type: ignore[attr-defined]
        result: bool = _contains_query_params(binop_node)
        self.assertTrue(result)

    def test_contains_query_params_non_string_value(self) -> None:
        """Test that non-string values don't trigger false positives."""
        code: str = "1 + 2"
        tree: ast.AST = ast.parse(code)
        binop_node: ast.BinOp = tree.body[0].value  # type: ignore[attr-defined]
        result: bool = _contains_query_params(binop_node)
        self.assertFalse(result)


class TestMatchesPattern(unittest.TestCase):
    """Test _matches_pattern helper function."""

    def test_matches_glob_pattern(self) -> None:
        """Test matching glob pattern."""
        path: Path = Path("tests/unit/test_example.py")
        result: bool = _matches_pattern(path, ["*_test.py"])
        self.assertFalse(result)  # Pattern doesn't match full path

    def test_matches_filename_pattern(self) -> None:
        """Test matching filename pattern."""
        path: Path = Path("tests/unit/test_example.py")
        result: bool = _matches_pattern(path, ["test_*.py"])
        self.assertTrue(result)

    def test_no_match(self) -> None:
        """Test no pattern match."""
        path: Path = Path("src/module.py")
        result: bool = _matches_pattern(path, ["test_*.py", "*_test.py"])
        self.assertFalse(result)


class TestFindPythonFiles(unittest.TestCase):
    """Test find_python_files function."""

    def test_find_single_file(self) -> None:
        """Test finding a single Python file."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write("x = 1")
            f.flush()
            files: list[Path] = list(find_python_files(Path(f.name)))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0], Path(f.name))

    def test_find_files_in_directory(self) -> None:
        """Test finding Python files in directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create Python files
            (Path(tmp_dir) / "module1.py").write_text("x = 1")
            (Path(tmp_dir) / "module2.py").write_text("y = 2")
            (Path(tmp_dir) / "readme.txt").write_text("not python")

            files: list[Path] = list(find_python_files(Path(tmp_dir)))
            self.assertEqual(len(files), 2)
            names: set[str] = {f.name for f in files}
            self.assertEqual(names, {"module1.py", "module2.py"})

    def test_exclude_paths(self) -> None:
        """Test excluding specific paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create files - resolve paths to handle symlinks (e.g., /var -> /private/var on macOS)
            tmp_path: Path = Path(tmp_dir).resolve()
            (tmp_path / "main.py").write_text("x = 1")
            tests_dir: Path = tmp_path / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_main.py").write_text("y = 2")

            files: list[Path] = list(find_python_files(tmp_path, exclude_paths=[str(tests_dir)]))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].name, "main.py")

    def test_exclude_paths_relative(self) -> None:
        """Test excluding paths with relative paths."""
        import os

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path: Path = Path(tmp_dir).resolve()
            (tmp_path / "main.py").write_text("x = 1")
            tests_dir: Path = tmp_path / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_main.py").write_text("y = 2")

            old_cwd: Path = Path.cwd()
            try:
                os.chdir(tmp_path)
                # Use relative path "tests" instead of absolute
                files: list[Path] = list(find_python_files(tmp_path, exclude_paths=["tests"]))
                self.assertEqual(len(files), 1)
                self.assertEqual(files[0].name, "main.py")
            finally:
                os.chdir(old_cwd)

    def test_exclude_patterns(self) -> None:
        """Test excluding by glob pattern."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            (Path(tmp_dir) / "module.py").write_text("x = 1")
            (Path(tmp_dir) / "module_test.py").write_text("y = 2")
            (Path(tmp_dir) / "test_module.py").write_text("z = 3")

            files: list[Path] = list(find_python_files(Path(tmp_dir), exclude_patterns=["test_*.py", "*_test.py"]))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].name, "module.py")

    def test_skip_hidden_directories(self) -> None:
        """Test that hidden directories are skipped."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            (Path(tmp_dir) / "module.py").write_text("x = 1")
            hidden_dir: Path = Path(tmp_dir) / ".hidden"
            hidden_dir.mkdir()
            (hidden_dir / "secret.py").write_text("y = 2")

            files: list[Path] = list(find_python_files(Path(tmp_dir)))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].name, "module.py")

    def test_skip_pycache(self) -> None:
        """Test that __pycache__ is skipped."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            (Path(tmp_dir) / "module.py").write_text("x = 1")
            cache_dir: Path = Path(tmp_dir) / "__pycache__"
            cache_dir.mkdir()
            (cache_dir / "module.cpython-311.pyc").write_text("bytecode")

            files: list[Path] = list(find_python_files(Path(tmp_dir)))
            self.assertEqual(len(files), 1)


class TestLintFile(unittest.TestCase):
    """Test lint_file function."""

    def test_lint_file_syntax_error(self) -> None:
        """Test linting file with syntax error."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write("def func(:\n    pass")
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].code, "E999")
        self.assertIn("SyntaxError", violations[0].message)

    def test_lint_file_io_error(self) -> None:
        """Test linting non-existent file."""
        violations: list[Violation] = lint_file(Path("/nonexistent/file.py"))
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].code, "E902")
        self.assertIn("IOError", violations[0].message)

    def test_lint_file_valid(self) -> None:
        """Test linting valid file."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", suffix=".py", mode="w", delete=False) as f:
            f.write(
                """
from __future__ import annotations

def test_func() -> None:
    x: int = 1
"""
            )
            f.flush()
            violations: list[Violation] = lint_file(Path(f.name))

        # Should have no violations
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
