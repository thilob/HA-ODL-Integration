"""Tests for persistent ODL station catalog cache validation."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
import sys
import unittest

INTEGRATION_DIR = Path(__file__).parents[1] / "custom_components" / "bfs_odl"
sys.path.insert(0, str(INTEGRATION_DIR))

from catalog_cache import cache_is_fresh, cached_options  # noqa: E402

CACHE_TTL = timedelta(hours=48)
NOW = datetime(2026, 7, 19, 18, tzinfo=UTC)


class StationCatalogCacheTest(unittest.TestCase):
    """Test station catalog cache lifetime and validation."""

    def test_cache_is_fresh_before_48_hours(self) -> None:
        """A populated catalog younger than 48 hours is reused."""
        cache = _cache(NOW - timedelta(hours=47, minutes=59))
        self.assertTrue(cache_is_fresh(cache, NOW, CACHE_TTL))

    def test_cache_expires_at_48_hours(self) -> None:
        """A catalog is refreshed once it reaches 48 hours."""
        cache = _cache(NOW - CACHE_TTL)
        self.assertFalse(cache_is_fresh(cache, NOW, CACHE_TTL))

    def test_future_timestamp_is_not_fresh(self) -> None:
        """A future timestamp cannot keep a catalog cached indefinitely."""
        cache = _cache(NOW + timedelta(minutes=1))
        self.assertFalse(cache_is_fresh(cache, NOW, CACHE_TTL))

    def test_invalid_cache_is_not_fresh(self) -> None:
        """Missing options or an invalid timestamp trigger a refresh."""
        self.assertFalse(cache_is_fresh(None, NOW, CACHE_TTL))
        self.assertFalse(
            cache_is_fresh(
                {"updated_at": "invalid", "stations": {"123": "Station"}},
                NOW,
                CACHE_TTL,
            )
        )
        self.assertFalse(
            cache_is_fresh(
                {"updated_at": NOW.isoformat(), "stations": {}}, NOW, CACHE_TTL
            )
        )

    def test_cached_options_discards_invalid_labels(self) -> None:
        """Only string labels are restored from persistent storage."""
        self.assertEqual(
            cached_options({"stations": {123: "Station", "bad": None}}),
            {"123": "Station"},
        )


def _cache(updated_at: datetime) -> dict[str, object]:
    return {
        "updated_at": updated_at.isoformat(),
        "stations": {"053580243": "Jülich (52428) – 053580243"},
    }


if __name__ == "__main__":
    unittest.main()
