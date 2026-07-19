# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Validation helpers for the persistent ODL station catalog cache."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any


def cache_is_fresh(
    cache: dict[str, Any] | None,
    now: datetime,
    cache_ttl: timedelta,
) -> bool:
    """Return whether a stored catalog is still within its cache lifetime."""
    if not cache or not cached_options(cache):
        return False
    try:
        updated_at = datetime.fromisoformat(str(cache["updated_at"]))
    except (KeyError, TypeError, ValueError):
        return False
    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=UTC)
    age = now.astimezone(UTC) - updated_at.astimezone(UTC)
    return timedelta(0) <= age < cache_ttl


def cached_options(cache: dict[str, Any] | None) -> dict[str, str]:
    """Validate and normalize station options from persistent storage."""
    if not cache or not isinstance(cache.get("stations"), dict):
        return {}
    return {
        str(station_id): label
        for station_id, label in cache["stations"].items()
        if isinstance(label, str)
    }
