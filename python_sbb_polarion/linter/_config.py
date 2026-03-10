"""Linter configuration from pyproject.toml or CLI."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LinterConfig:
    """Configuration for the linter, loaded from pyproject.toml or CLI."""

    disable: set[str] = field(default_factory=set)
    only: set[str] = field(default_factory=set)
    exclude: list[str] = field(default_factory=list)
    exclude_patterns: list[str] = field(default_factory=list)
    cache: bool = True

    @classmethod
    def from_pyproject(cls, project_root: Path | None = None) -> LinterConfig:
        """Load configuration from pyproject.toml.

        Args:
            project_root: Root directory containing pyproject.toml. If None, searches upward.

        Returns:
            LinterConfig with settings from pyproject.toml or defaults.
        """
        pyproject_path: Path | None = cls._find_pyproject(project_root)
        if pyproject_path is None:
            return cls()

        try:
            with pyproject_path.open("rb") as f:
                data: dict[str, object] = tomllib.load(f)
        except (OSError, tomllib.TOMLDecodeError):
            return cls()

        return cls._parse_config(data)

    @classmethod
    def _parse_config(cls, data: dict[str, object]) -> LinterConfig:
        """Parse configuration from TOML data.

        Args:
            data: Parsed TOML data dictionary.

        Returns:
            LinterConfig with parsed settings or defaults.
        """
        tool_config: object = data.get("tool", {})
        if not isinstance(tool_config, dict):
            return cls()

        linter_config: object = tool_config.get("python-sbb-polarion-lint", {})
        if not isinstance(linter_config, dict):
            return cls()

        return cls._extract_settings(linter_config)

    @classmethod
    def _extract_settings(cls, linter_config: dict[str, object]) -> LinterConfig:
        """Extract settings from linter config section.

        Args:
            linter_config: The [tool.python-sbb-polarion-lint] section.

        Returns:
            LinterConfig with extracted settings.
        """
        disable_raw: object = linter_config.get("disable", [])
        disable: set[str] = set(disable_raw) if isinstance(disable_raw, list) else set()

        only_raw: object = linter_config.get("only", [])
        only: set[str] = set(only_raw) if isinstance(only_raw, list) else set()

        exclude_raw: object = linter_config.get("exclude", [])
        exclude: list[str] = list(exclude_raw) if isinstance(exclude_raw, list) else []

        exclude_patterns_raw: object = linter_config.get("exclude-patterns", [])
        exclude_patterns: list[str] = list(exclude_patterns_raw) if isinstance(exclude_patterns_raw, list) else []

        cache_raw: object = linter_config.get("cache", True)
        cache: bool = bool(cache_raw) if isinstance(cache_raw, bool) else True

        return cls(
            disable=disable,
            only=only,
            exclude=exclude,
            exclude_patterns=exclude_patterns,
            cache=cache,
        )

    @staticmethod
    def _find_pyproject(start_path: Path | None = None) -> Path | None:
        """Find pyproject.toml by searching upward from start_path.

        Returns:
            Path to pyproject.toml or None if not found.
        """
        current: Path = start_path or Path.cwd()
        while current != current.parent:
            pyproject: Path = current / "pyproject.toml"
            if pyproject.is_file():
                return pyproject
            current = current.parent
        return None

    def merge_cli(
        self,
        disable: set[str],
        only: set[str],
        exclude: list[str],
        exclude_patterns: list[str],
        cache: bool | None,
    ) -> LinterConfig:
        """Merge CLI arguments with config (CLI takes precedence).

        Args:
            disable: Rules to disable from CLI.
            only: Rules to check from CLI.
            exclude: Paths to exclude from CLI.
            exclude_patterns: Glob patterns to exclude from CLI.
            cache: Whether to use cache from CLI (None means use config).

        Returns:
            New LinterConfig with merged settings.
        """
        return LinterConfig(
            disable=self.disable | disable,
            only=only or self.only,  # CLI --only overrides config completely
            exclude=self.exclude + exclude,
            exclude_patterns=self.exclude_patterns + exclude_patterns,
            cache=cache if cache is not None else self.cache,
        )
