"""Unit tests for LinterConfig class."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_sbb_polarion.linter.code_style_linter import LinterConfig


class TestLinterConfig(unittest.TestCase):
    """Test LinterConfig class."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config: LinterConfig = LinterConfig()
        self.assertEqual(config.disable, set())
        self.assertEqual(config.only, set())
        self.assertEqual(config.exclude, [])
        self.assertEqual(config.exclude_patterns, [])
        self.assertTrue(config.cache)

    def test_custom_values(self) -> None:
        """Test configuration with custom values."""
        config: LinterConfig = LinterConfig(
            disable={"PSP001", "PSP002"},
            only={"PSP005"},
            exclude=["tests/"],
            exclude_patterns=["*_test.py"],
            cache=False,
        )
        self.assertEqual(config.disable, {"PSP001", "PSP002"})
        self.assertEqual(config.only, {"PSP005"})
        self.assertEqual(config.exclude, ["tests/"])
        self.assertEqual(config.exclude_patterns, ["*_test.py"])
        self.assertFalse(config.cache)

    def test_from_pyproject_no_file(self) -> None:
        """Test loading config when pyproject.toml doesn't exist."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config: LinterConfig = LinterConfig.from_pyproject(Path(tmp_dir))
            # Should return defaults
            self.assertEqual(config.disable, set())
            self.assertEqual(config.only, set())
            self.assertTrue(config.cache)

    def test_from_pyproject_empty_tool_section(self) -> None:
        """Test loading config when pyproject.toml has no linter section."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pyproject_path: Path = Path(tmp_dir) / "pyproject.toml"
            pyproject_path.write_text(
                """
[project]
name = "test"
""",
                encoding="utf-8",
            )
            config: LinterConfig = LinterConfig.from_pyproject(Path(tmp_dir))
            self.assertEqual(config.disable, set())
            self.assertTrue(config.cache)

    def test_from_pyproject_with_config(self) -> None:
        """Test loading config from pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pyproject_path: Path = Path(tmp_dir) / "pyproject.toml"
            pyproject_path.write_text(
                """
[tool.python-sbb-polarion-lint]
disable = ["PSP001", "PSP002"]
only = ["PSP005"]
exclude = ["tests/", "migrations/"]
exclude-patterns = ["*_test.py", "*_generated.py"]
cache = false
""",
                encoding="utf-8",
            )
            config: LinterConfig = LinterConfig.from_pyproject(Path(tmp_dir))
            self.assertEqual(config.disable, {"PSP001", "PSP002"})
            self.assertEqual(config.only, {"PSP005"})
            self.assertEqual(config.exclude, ["tests/", "migrations/"])
            self.assertEqual(config.exclude_patterns, ["*_test.py", "*_generated.py"])
            self.assertFalse(config.cache)

    def test_from_pyproject_invalid_toml(self) -> None:
        """Test loading config from invalid TOML file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pyproject_path: Path = Path(tmp_dir) / "pyproject.toml"
            pyproject_path.write_text("invalid toml {{{{", encoding="utf-8")
            config: LinterConfig = LinterConfig.from_pyproject(Path(tmp_dir))
            # Should return defaults on parse error
            self.assertEqual(config.disable, set())
            self.assertTrue(config.cache)

    def test_from_pyproject_invalid_tool_type(self) -> None:
        """Test loading config when tool section is not a dict."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pyproject_path: Path = Path(tmp_dir) / "pyproject.toml"
            pyproject_path.write_text(
                """
tool = "invalid"
""",
                encoding="utf-8",
            )
            config: LinterConfig = LinterConfig.from_pyproject(Path(tmp_dir))
            self.assertEqual(config.disable, set())

    def test_from_pyproject_invalid_linter_config_type(self) -> None:
        """Test loading config when linter config section is not a dict."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pyproject_path: Path = Path(tmp_dir) / "pyproject.toml"
            pyproject_path.write_text(
                """
[tool]
python-sbb-polarion-lint = "invalid"
""",
                encoding="utf-8",
            )
            config: LinterConfig = LinterConfig.from_pyproject(Path(tmp_dir))
            self.assertEqual(config.disable, set())

    def test_merge_cli_disable(self) -> None:
        """Test merging CLI disable with config disable."""
        base_config: LinterConfig = LinterConfig(disable={"PSP001"})
        merged: LinterConfig = base_config.merge_cli(
            disable={"PSP002"},
            only=set(),
            exclude=[],
            exclude_patterns=[],
            cache=None,
        )
        self.assertEqual(merged.disable, {"PSP001", "PSP002"})

    def test_merge_cli_only_overrides(self) -> None:
        """Test that CLI only completely overrides config only."""
        base_config: LinterConfig = LinterConfig(only={"PSP001"})
        merged: LinterConfig = base_config.merge_cli(
            disable=set(),
            only={"PSP005"},
            exclude=[],
            exclude_patterns=[],
            cache=None,
        )
        self.assertEqual(merged.only, {"PSP005"})

    def test_merge_cli_only_empty_uses_config(self) -> None:
        """Test that empty CLI only uses config only."""
        base_config: LinterConfig = LinterConfig(only={"PSP001"})
        merged: LinterConfig = base_config.merge_cli(
            disable=set(),
            only=set(),
            exclude=[],
            exclude_patterns=[],
            cache=None,
        )
        self.assertEqual(merged.only, {"PSP001"})

    def test_merge_cli_exclude_appends(self) -> None:
        """Test that CLI exclude appends to config exclude."""
        base_config: LinterConfig = LinterConfig(exclude=["tests/"])
        merged: LinterConfig = base_config.merge_cli(
            disable=set(),
            only=set(),
            exclude=["migrations/"],
            exclude_patterns=[],
            cache=None,
        )
        self.assertEqual(merged.exclude, ["tests/", "migrations/"])

    def test_merge_cli_exclude_patterns_appends(self) -> None:
        """Test that CLI exclude patterns appends to config patterns."""
        base_config: LinterConfig = LinterConfig(exclude_patterns=["*_test.py"])
        merged: LinterConfig = base_config.merge_cli(
            disable=set(),
            only=set(),
            exclude=[],
            exclude_patterns=["*_generated.py"],
            cache=None,
        )
        self.assertEqual(merged.exclude_patterns, ["*_test.py", "*_generated.py"])

    def test_merge_cli_cache_none_uses_config(self) -> None:
        """Test that None cache uses config value."""
        base_config: LinterConfig = LinterConfig(cache=False)
        merged: LinterConfig = base_config.merge_cli(
            disable=set(),
            only=set(),
            exclude=[],
            exclude_patterns=[],
            cache=None,
        )
        self.assertFalse(merged.cache)

    def test_merge_cli_cache_overrides(self) -> None:
        """Test that CLI cache overrides config."""
        base_config: LinterConfig = LinterConfig(cache=True)
        merged: LinterConfig = base_config.merge_cli(
            disable=set(),
            only=set(),
            exclude=[],
            exclude_patterns=[],
            cache=False,
        )
        self.assertFalse(merged.cache)

    def test_find_pyproject_searches_upward(self) -> None:
        """Test that _find_pyproject searches parent directories."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create pyproject.toml in parent
            pyproject_path: Path = Path(tmp_dir) / "pyproject.toml"
            pyproject_path.write_text("[project]\nname = 'test'\n", encoding="utf-8")

            # Create nested directory
            nested: Path = Path(tmp_dir) / "src" / "module"
            nested.mkdir(parents=True)

            # Should find pyproject.toml in parent
            found: Path | None = LinterConfig._find_pyproject(nested)
            self.assertIsNotNone(found)
            self.assertEqual(found, pyproject_path)


if __name__ == "__main__":
    unittest.main()
