# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Config flow for BfS ODL."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlowWithReload
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .api import ODLApiClient, ODLApiError
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_STATIONS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    NAME,
)
from .models import ODLStation


class ODLConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a BfS ODL config flow."""

    VERSION = 1

    def __init__(self) -> None:
        self._stations: dict[str, ODLStation] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Create the integration and select stations."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        errors: dict[str, str] = {}
        if not self._stations:
            try:
                self._stations = await ODLApiClient(
                    async_get_clientsession(self.hass)
                ).async_get_stations()
            except ODLApiError:
                errors["base"] = "cannot_connect"

        if user_input is not None and not errors:
            return self.async_create_entry(
                title=NAME,
                data={CONF_STATIONS: user_input[CONF_STATIONS]},
                options={CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL]},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(
                self._stations,
                selected=[],
                scan_interval=DEFAULT_SCAN_INTERVAL,
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow."""
        return ODLOptionsFlow()


class ODLOptionsFlow(OptionsFlowWithReload):
    """Allow station selection and polling interval changes."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        try:
            stations = await ODLApiClient(
                async_get_clientsession(self.hass)
            ).async_get_stations()
        except ODLApiError:
            stations = {}
            errors["base"] = "cannot_connect"

        if user_input is not None and not errors:
            return self.async_create_entry(data=user_input)

        selected = self.config_entry.options.get(
            CONF_STATIONS, self.config_entry.data.get(CONF_STATIONS, [])
        )
        interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(stations, selected, interval),
            errors=errors,
        )


def _build_schema(
    stations: dict[str, ODLStation],
    selected: list[str],
    scan_interval: int,
) -> vol.Schema:
    options = [
        {"value": station.kenn, "label": station.display_name}
        for station in sorted(
            stations.values(), key=lambda item: (item.name.casefold(), item.kenn)
        )
    ]
    return vol.Schema(
        {
            vol.Required(CONF_STATIONS, default=selected): SelectSelector(
                SelectSelectorConfig(
                    options=options,
                    multiple=True,
                    mode=SelectSelectorMode.DROPDOWN,
                    sort=False,
                )
            ),
            vol.Required(CONF_SCAN_INTERVAL, default=scan_interval): NumberSelector(
                NumberSelectorConfig(
                    min=MIN_SCAN_INTERVAL,
                    max=MAX_SCAN_INTERVAL,
                    step=5,
                    unit_of_measurement="min",
                    mode=NumberSelectorMode.BOX,
                )
            ),
        }
    )
