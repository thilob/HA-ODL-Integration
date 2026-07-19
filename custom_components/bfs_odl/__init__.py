# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""BfS ODL measuring network integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ODLApiClient
from .const import PLATFORMS
from .coordinator import ODLDataUpdateCoordinator


@dataclass(slots=True)
class ODLRuntimeData:
    """Runtime data kept by a config entry."""

    coordinator: ODLDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BfS ODL from a config entry."""
    api = ODLApiClient(async_get_clientsession(hass))
    coordinator = ODLDataUpdateCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = ODLRuntimeData(coordinator=coordinator)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a BfS ODL config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
