"""Unit tests for main() function in linter module."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from python_sbb_polarion.linter.code_style_linter import main


class TestMain(unittest.TestCase):
    """Test main() CLI function."""

    def test_main_no_violations_returns_0(self) -> None:
        """Test that main returns 0 when no violations found."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "valid.py"
            test_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )
            result: int = main([str(tmp_dir), "--no-cache"])
            self.assertEqual(result, 0)

    def test_main_with_violations_returns_1(self) -> None:
        """Test that main returns 1 when violations found."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "invalid.py"
            test_file.write_text(
                """
def func():
    x = 1
""",
                encoding="utf-8",
            )
            result: int = main([str(tmp_dir), "--no-cache"])
            self.assertEqual(result, 1)

    def test_main_nonexistent_path_returns_2(self) -> None:
        """Test that main returns 2 for non-existent path."""
        result: int = main(["/nonexistent/path"])
        self.assertEqual(result, 2)

    def test_main_disable_rule(self) -> None:
        """Test --disable flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text(
                """
def func():
    x = 1
""",
                encoding="utf-8",
            )
            result: int = main([str(tmp_dir), "--disable", "PSP001", "--no-cache"])
            self.assertEqual(result, 0)

    def test_main_only_rule(self) -> None:
        """Test --only flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text(
                """
def func():
    x = 1
    headers: dict[str, str] = {"key": "value"}
""",
                encoding="utf-8",
            )
            # Only check PSP005, not PSP001
            result: int = main([str(tmp_dir), "--only", "PSP005", "--no-cache"])
            # Should still return 1 because PSP005 violation exists
            self.assertEqual(result, 1)

    def test_main_exclude_path(self) -> None:
        """Test --exclude flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create main file with violation
            main_file: Path = Path(tmp_dir) / "main.py"
            main_file.write_text(
                """
def func():
    x = 1
""",
                encoding="utf-8",
            )
            # Create excluded file with violation
            excluded_dir: Path = Path(tmp_dir) / "excluded"
            excluded_dir.mkdir()
            excluded_file: Path = excluded_dir / "module.py"
            excluded_file.write_text(
                """
def func():
    y = 2
""",
                encoding="utf-8",
            )

            # Without exclude - should find 2 violations
            result1: int = main([str(tmp_dir), "--no-cache"])
            self.assertEqual(result1, 1)

            # With exclude - should find 1 violation
            result2: int = main([str(tmp_dir), "--exclude", str(excluded_dir), "--no-cache"])
            self.assertEqual(result2, 1)

    def test_main_exclude_pattern(self) -> None:
        """Test --exclude-pattern flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create regular file
            regular_file: Path = Path(tmp_dir) / "module.py"
            regular_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )
            # Create generated file with violation
            generated_file: Path = Path(tmp_dir) / "module_generated.py"
            generated_file.write_text(
                """
def func():
    x = 1
""",
                encoding="utf-8",
            )

            result: int = main([str(tmp_dir), "--exclude-pattern", "*_generated.py", "--no-cache"])
            self.assertEqual(result, 0)

    def test_main_cache_functionality(self) -> None:
        """Test caching functionality."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "valid.py"
            test_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )
            cache_dir: Path = Path(tmp_dir) / ".psp-lint-cache"

            # First run - should create cache
            result1: int = main([str(tmp_dir)])
            self.assertEqual(result1, 0)
            # Cache directory may or may not exist depending on cwd

            # Second run - should use cache (if cwd is tmp_dir)
            result2: int = main([str(tmp_dir)])
            self.assertEqual(result2, 0)

    def test_main_clear_cache(self) -> None:
        """Test --clear-cache flag."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "valid.py"
            test_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )

            # Run with clear-cache
            result: int = main([str(tmp_dir), "--clear-cache"])
            self.assertEqual(result, 0)

    def test_main_no_cache_flag(self) -> None:
        """Test --no-cache flag disables caching."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "valid.py"
            test_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )

            result: int = main([str(tmp_dir), "--no-cache"])
            self.assertEqual(result, 0)

    def test_main_default_path(self) -> None:
        """Test that default path is current directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "valid.py"
            test_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )

            # Change to temp directory and run with no args
            import os

            old_cwd: Path = Path.cwd()
            try:
                os.chdir(tmp_dir)
                result: int = main(["--no-cache"])
                self.assertEqual(result, 0)
            finally:
                os.chdir(old_cwd)

    def test_main_multiple_paths(self) -> None:
        """Test linting multiple paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            dir1: Path = Path(tmp_dir) / "dir1"
            dir1.mkdir()
            dir2: Path = Path(tmp_dir) / "dir2"
            dir2.mkdir()

            (dir1 / "module1.py").write_text(
                """
from __future__ import annotations

def func() -> None:
    pass
"""
            )
            (dir2 / "module2.py").write_text(
                """
from __future__ import annotations

def func() -> None:
    pass
"""
            )

            result: int = main([str(dir1), str(dir2), "--no-cache"])
            self.assertEqual(result, 0)

    def test_main_outputs_violations(self) -> None:
        """Test that violations are printed to stdout."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text(
                """
def func():
    x = 1
""",
                encoding="utf-8",
            )

            with patch("sys.stdout.write") as mock_write:
                main([str(tmp_dir), "--no-cache"])
                # Should have called write with violation output
                calls: list[str] = [str(call) for call in mock_write.call_args_list]
                output: str = "".join(calls)
                self.assertIn("PSP001", output)

    def test_main_fix_flag_accepted(self) -> None:
        """Test that --fix flag is accepted (even if it doesn't modify files)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "valid.py"
            test_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )

            # --fix should not raise an error
            result: int = main([str(tmp_dir), "--fix", "--no-cache"])
            self.assertEqual(result, 0)

    def test_main_cache_invalidation_on_violation(self) -> None:
        """Test that cache is invalidated when file has violations."""
        import os

        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "invalid.py"
            test_file.write_text(
                """
def func():
    x = 1
""",
                encoding="utf-8",
            )

            old_cwd: Path = Path.cwd()
            try:
                os.chdir(tmp_dir)
                # First run with cache enabled - should find violation and invalidate
                result1: int = main([str(tmp_dir)])
                self.assertEqual(result1, 1)

                # Second run - should still find violation (not cached because invalidated)
                result2: int = main([str(tmp_dir)])
                self.assertEqual(result2, 1)
            finally:
                os.chdir(old_cwd)

    def test_main_summary_with_cache_skipped(self) -> None:
        """Test summary message when files are skipped due to cache."""
        import os

        with tempfile.TemporaryDirectory() as tmp_dir:
            test_file: Path = Path(tmp_dir) / "valid.py"
            test_file.write_text(
                """
from __future__ import annotations

def func() -> None:
    x: int = 1
""",
                encoding="utf-8",
            )

            old_cwd: Path = Path.cwd()
            try:
                os.chdir(tmp_dir)
                # First run - file gets cached
                result1: int = main([str(tmp_dir)])
                self.assertEqual(result1, 0)

                # Second run - file should be skipped (cached)
                with patch("sys.stdout.write") as mock_write:
                    result2: int = main([str(tmp_dir)])
                    self.assertEqual(result2, 0)
                    calls: str = "".join(str(call) for call in mock_write.call_args_list)
                    # Should mention skipped cached files
                    self.assertIn("skipped", calls)
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
