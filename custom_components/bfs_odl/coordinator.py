# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Update coordinator for BfS ODL."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ODLApiClient, ODLApiError
from .const import CONF_SCAN_INTERVAL, CONF_STATIONS, DEFAULT_SCAN_INTERVAL, DOMAIN
from .models import ODLStation

_LOGGER = logging.getLogger(__name__)


class ODLDataUpdateCoordinator(DataUpdateCoordinator[dict[str, ODLStation]]):
    """Fetch the latest data once for all selected stations."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: ODLApiClient,
    ) -> None:
        self.api = api
        self.selected_station_ids = set(
            entry.options.get(CONF_STATIONS, entry.data.get(CONF_STATIONS, []))
        )
        interval = int(entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=interval),
            always_update=False,
        )

    async def _async_update_data(self) -> dict[str, ODLStation]:
        try:
            all_stations = await self.api.async_get_stations()
        except ODLApiError as err:
            raise UpdateFailed(str(err)) from err

        selected = {
            station_id: station
            for station_id, station in all_stations.items()
            if station_id in self.selected_station_ids
        }
        missing = self.selected_station_ids - selected.keys()
        if missing:
            _LOGGER.warning(
                "Selected BfS ODL stations are currently absent from the API: %s",
                ", ".join(sorted(missing)),
            )
        return selected
