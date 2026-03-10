"""Linter cache for skipping unchanged files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


# Cache file name
CACHE_FILE: str = "cache.json"


class LinterCache:
    """Cache for linter results to skip unchanged files."""

    def __init__(self, cache_dir: Path) -> None:
        """Initialize cache.

        Args:
            cache_dir: Directory to store cache files.
        """
        self.cache_dir: Path = cache_dir
        self.cache_file: Path = cache_dir / CACHE_FILE
        self._cache: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        """Load cache from disk."""
        if self.cache_file.is_file():
            try:
                with self.cache_file.open("r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except (OSError, json.JSONDecodeError):
                self._cache = {}

    def save(self) -> None:
        """Save cache to disk."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with self.cache_file.open("w", encoding="utf-8") as f:
            json.dump(self._cache, f, indent=2)

    @staticmethod
    def _file_hash(file_path: Path) -> str:
        """Compute hash of file content.

        Args:
            file_path: Path to file.

        Returns:
            MD5 hash of file content.
        """
        try:
            content: bytes = file_path.read_bytes()
            return hashlib.md5(content, usedforsecurity=False).hexdigest()
        except OSError:
            return ""

    def is_unchanged(self, file_path: Path) -> bool:
        """Check if file is unchanged since last lint.

        Args:
            file_path: Path to file.

        Returns:
            True if file content hash matches cached hash.
        """
        key: str = str(file_path.resolve())
        current_hash: str = self._file_hash(file_path)
        return key in self._cache and self._cache[key] == current_hash

    def update(self, file_path: Path) -> None:
        """Update cache with current file hash.

        Args:
            file_path: Path to file.
        """
        key: str = str(file_path.resolve())
        self._cache[key] = self._file_hash(file_path)

    def invalidate(self, file_path: Path) -> None:
        """Remove file from cache (file has violations).

        Args:
            file_path: Path to file.
        """
        key: str = str(file_path.resolve())
        self._cache.pop(key, None)
