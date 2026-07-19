# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Persistent station catalog cache for ODL configuration flows."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
import logging
from typing import Any, cast

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store

from .api import ODLApiClient, ODLApiError
from .catalog_cache import cache_is_fresh, cached_options
from .const import DOMAIN, STATION_CATALOG_CACHE_TTL

_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = f"{DOMAIN}.station_catalog"
STORAGE_VERSION = 1
DATA_STATION_CATALOG = "station_catalog"


class ODLStationCatalog:
    """Cache the station selector catalog independently from live measurements."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._api = ODLApiClient(async_get_clientsession(hass))
        self._store = Store[dict[str, Any]](hass, STORAGE_VERSION, STORAGE_KEY)
        self._lock = asyncio.Lock()
        self._cache: dict[str, Any] | None = None
        self._loaded = False

    async def async_get_station_options(self) -> dict[str, str]:
        """Return cached station labels, refreshing them after 48 hours."""
        async with self._lock:
            cached = await self._async_load()
            if cache_is_fresh(
                cached, datetime.now(UTC), STATION_CATALOG_CACHE_TTL
            ):
                return cached_options(cached)

            try:
                stations = await self._api.async_get_stations()
            except ODLApiError:
                stale_options = cached_options(cached)
                if stale_options:
                    _LOGGER.warning(
                        "Using stale ODL station catalog because refresh failed"
                    )
                    return stale_options
                raise

            options = {
                station_id: station.display_name
                for station_id, station in stations.items()
            }
            self._cache = {
                "updated_at": datetime.now(UTC).isoformat(),
                "stations": options,
            }
            await self._store.async_save(self._cache)
            return dict(options)

    async def _async_load(self) -> dict[str, Any] | None:
        """Load the persistent cache once per Home Assistant process."""
        if not self._loaded:
            stored = await self._store.async_load()
            self._cache = stored if isinstance(stored, dict) else None
            self._loaded = True
        return self._cache


def get_station_catalog(hass: HomeAssistant) -> ODLStationCatalog:
    """Return the shared station catalog for this Home Assistant instance."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    catalog = domain_data.get(DATA_STATION_CATALOG)
    if catalog is None:
        catalog = ODLStationCatalog(hass)
        domain_data[DATA_STATION_CATALOG] = catalog
    return cast(ODLStationCatalog, catalog)
