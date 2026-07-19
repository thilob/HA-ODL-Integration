# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Sensor entities for BfS ODL stations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ODLRuntimeData
from .const import (
    DATA_LICENSE,
    DATA_LICENSE_ID,
    DATA_LICENSE_URL,
    DATA_PROVIDER,
    DATA_SERVICE_URL,
    DATA_SOURCE,
    DOMAIN,
    SOFTWARE_COPYRIGHT,
    SOFTWARE_LICENSE,
)
from .coordinator import ODLDataUpdateCoordinator
from .models import ODLStation


@dataclass(frozen=True, kw_only=True)
class ODLSensorDescription(SensorEntityDescription):
    """Description for one ODL sensor type."""

    key: str
    translation_key: str
    value_fn: Callable[[ODLStation], Any]
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None
    icon: str | None = None
    unit_fn: Callable[[ODLStation], str | None] | None = None


SENSORS: tuple[ODLSensorDescription, ...] = (
    ODLSensorDescription(
        key="dose_rate",
        translation_key="dose_rate",
        value_fn=lambda station: station.value,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:radioactive",
        unit_fn=lambda station: station.unit,
    ),
    ODLSensorDescription(
        key="cosmic_dose_rate",
        translation_key="cosmic_dose_rate",
        value_fn=lambda station: station.value_cosmic,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:weather-sunny-alert",
        unit_fn=lambda station: station.unit,
    ),
    ODLSensorDescription(
        key="terrestrial_dose_rate",
        translation_key="terrestrial_dose_rate",
        value_fn=lambda station: station.value_terrestrial,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:terrain",
        unit_fn=lambda station: station.unit,
    ),
    ODLSensorDescription(
        key="measurement_end",
        translation_key="measurement_end",
        value_fn=lambda station: station.end_measure,
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    ODLSensorDescription(
        key="station_status",
        translation_key="station_status",
        value_fn=lambda station: station.site_status_text,
        icon="mdi:list-status",
    ),
    ODLSensorDescription(
        key="validation_status",
        translation_key="validation_status",
        value_fn=lambda station: (
            "validated" if station.validated == 1 else "unvalidated"
            if station.validated == 2 else None
        ),
        icon="mdi:check-decagram-outline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up all selected ODL station entities."""
    runtime: ODLRuntimeData = entry.runtime_data
    coordinator = runtime.coordinator
    async_add_entities(
        ODLStationSensor(coordinator, station_id, description)
        for station_id in sorted(coordinator.selected_station_ids)
        for description in SENSORS
    )


class ODLStationSensor(CoordinatorEntity[ODLDataUpdateCoordinator], SensorEntity):
    """One measurement or metadata sensor for an ODL station."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ODLDataUpdateCoordinator,
        station_id: str,
        description: ODLSensorDescription,
    ) -> None:
        super().__init__(coordinator, context=station_id)
        self.station_id = station_id
        self.entity_description = description
        self._attr_unique_id = f"{station_id}_{description.key}"
        self._attr_translation_key = description.translation_key
        self._attr_device_class = description.device_class
        self._attr_state_class = description.state_class
        self._attr_icon = description.icon

    @property
    def _station(self) -> ODLStation | None:
        return self.coordinator.data.get(self.station_id)

    @property
    def available(self) -> bool:
        return super().available and self._station is not None

    @property
    def native_value(self) -> float | str | datetime | None:
        station = self._station
        return self.entity_description.value_fn(station) if station else None

    @property
    def native_unit_of_measurement(self) -> str | None:
        station = self._station
        if station and self.entity_description.unit_fn:
            return self.entity_description.unit_fn(station)
        return None

    @property
    def suggested_display_precision(self) -> int | None:
        return 3 if self.entity_description.state_class else None

    @property
    def device_info(self) -> DeviceInfo:
        station = self._station
        name = station.name if station else self.station_id
        info: DeviceInfo = DeviceInfo(
            identifiers={(DOMAIN, self.station_id)},
            name=f"ODL {name}",
            manufacturer="Bundesamt für Strahlenschutz",
            model="ODL-Messstelle",
            configuration_url=(
                "https://odlinfo.bfs.de/ODL/DE/themen/wo-stehen-die-sonden/"
                f"karte/_documents/Messstelle.html?id={self.station_id}"
            ),
        )
        if station:
            info["serial_number"] = station.international_id or station.kenn
            if station.latitude is not None:
                info["suggested_area"] = station.name
        return info

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        station = self._station
        if not station:
            return {}
        return {
            "station_id": station.kenn,
            "international_id": station.international_id,
            "postal_code": station.postal_code,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "height_above_sea_m": station.height_above_sea,
            "network_node": station.network_node,
            "measurement_start": station.start_measure,
            "measurement_end": station.end_measure,
            "nuclide": station.nuclide,
            "duration": station.duration,
            "validated_code": station.validated,
            "station_status_code": station.site_status,
            "data_provider": DATA_PROVIDER,
            "data_source": DATA_SOURCE,
            "data_license": DATA_LICENSE,
            "data_license_id": DATA_LICENSE_ID,
            "data_license_url": DATA_LICENSE_URL,
            "data_service_url": DATA_SERVICE_URL,
            "integration_software_license": SOFTWARE_LICENSE,
            "integration_software_copyright": SOFTWARE_COPYRIGHT,
            "data_processing_note": (
                "Technische Auswahl und Darstellung der vom BfS "
                "bereitgestellten Mess- und Metadaten; keine fachliche Bewertung."
            ),
        }
