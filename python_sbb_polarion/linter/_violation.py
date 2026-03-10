"""Violation dataclass for linter results."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Violation:
    """Represents a single code style violation."""

    file: Path
    line: int
    col: int
    code: str
    message: str

    def __str__(self) -> str:
        """Return string representation of violation."""
        return f"{self.file}:{self.line}:{self.col}: {self.code} {self.message}"
