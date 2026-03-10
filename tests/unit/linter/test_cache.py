"""Unit tests for LinterCache class."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from python_sbb_polarion.linter.code_style_linter import LinterCache


class TestLinterCache(unittest.TestCase):
    """Test LinterCache class."""

    def test_init_creates_empty_cache(self) -> None:
        """Test that initializing cache with no file creates empty cache."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)
            self.assertEqual(cache._cache, {})

    def test_save_creates_cache_file(self) -> None:
        """Test that save creates cache file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)
            cache.save()
            self.assertTrue(cache.cache_file.exists())

    def test_load_existing_cache(self) -> None:
        """Test loading existing cache from disk."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache_dir.mkdir(parents=True)
            cache_file: Path = cache_dir / "cache.json"
            cache_file.write_text('{"test_file.py": "abc123"}', encoding="utf-8")

            cache = LinterCache(cache_dir)
            self.assertEqual(cache._cache, {"test_file.py": "abc123"})

    def test_load_invalid_json(self) -> None:
        """Test loading invalid JSON cache file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache_dir.mkdir(parents=True)
            cache_file: Path = cache_dir / "cache.json"
            cache_file.write_text("invalid json {{{{", encoding="utf-8")

            cache = LinterCache(cache_dir)
            self.assertEqual(cache._cache, {})

    def test_is_unchanged_returns_false_for_new_file(self) -> None:
        """Test is_unchanged returns False for file not in cache."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)

            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text("print('hello')", encoding="utf-8")

            self.assertFalse(cache.is_unchanged(test_file))

    def test_is_unchanged_returns_true_for_unchanged_file(self) -> None:
        """Test is_unchanged returns True for unchanged cached file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)

            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text("print('hello')", encoding="utf-8")

            cache.update(test_file)
            self.assertTrue(cache.is_unchanged(test_file))

    def test_is_unchanged_returns_false_for_modified_file(self) -> None:
        """Test is_unchanged returns False when file content changes."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)

            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text("print('hello')", encoding="utf-8")
            cache.update(test_file)

            # Modify file
            test_file.write_text("print('world')", encoding="utf-8")
            self.assertFalse(cache.is_unchanged(test_file))

    def test_update_adds_file_to_cache(self) -> None:
        """Test update adds file hash to cache."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)

            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text("print('hello')", encoding="utf-8")

            cache.update(test_file)
            key: str = str(test_file.resolve())
            self.assertIn(key, cache._cache)

    def test_invalidate_removes_file_from_cache(self) -> None:
        """Test invalidate removes file from cache."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)

            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text("print('hello')", encoding="utf-8")

            cache.update(test_file)
            cache.invalidate(test_file)

            key: str = str(test_file.resolve())
            self.assertNotIn(key, cache._cache)

    def test_invalidate_nonexistent_file_no_error(self) -> None:
        """Test invalidate on non-cached file doesn't raise error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            cache = LinterCache(cache_dir)

            test_file: Path = Path(tmp_dir) / "test.py"
            # Should not raise
            cache.invalidate(test_file)

    def test_save_and_reload(self) -> None:
        """Test that saved cache can be reloaded."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text("print('hello')", encoding="utf-8")

            # Save cache
            cache1 = LinterCache(cache_dir)
            cache1.update(test_file)
            cache1.save()

            # Reload cache
            cache2 = LinterCache(cache_dir)
            self.assertTrue(cache2.is_unchanged(test_file))

    def test_file_hash_returns_empty_for_missing_file(self) -> None:
        """Test _file_hash returns empty string for missing file."""
        missing_file: Path = Path("/nonexistent/file.py")
        result: str = LinterCache._file_hash(missing_file)
        self.assertEqual(result, "")

    def test_cache_persists_across_instances(self) -> None:
        """Test cache data persists across LinterCache instances."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_dir: Path = Path(tmp_dir) / ".cache"
            test_file: Path = Path(tmp_dir) / "test.py"
            test_file.write_text("x: int = 1", encoding="utf-8")

            # First instance - add file
            cache1 = LinterCache(cache_dir)
            cache1.update(test_file)
            cache1.save()

            # Second instance - should have file
            cache2 = LinterCache(cache_dir)
            self.assertTrue(cache2.is_unchanged(test_file))


if __name__ == "__main__":
    unittest.main()
