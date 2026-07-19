# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Data models for the ODL integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class ODLStation:
    """An ODL measuring station and its latest values."""

    kenn: str
    international_id: str | None
    name: str
    postal_code: str | None
    longitude: float | None
    latitude: float | None
    height_above_sea: float | None
    site_status: int | None
    site_status_text: str | None
    network_node: int | None
    start_measure: datetime | None
    end_measure: datetime | None
    value: float | None
    value_cosmic: float | None
    value_terrestrial: float | None
    unit: str
    validated: int | None
    nuclide: str | None
    duration: str | None

    @property
    def display_name(self) -> str:
        """Return a compact name for configuration selectors."""
        suffix = f" ({self.postal_code})" if self.postal_code else ""
        return f"{self.name}{suffix} – {self.kenn}"

    @classmethod
    def from_feature(cls, feature: dict[str, Any]) -> ODLStation:
        """Build a station from one GeoJSON feature."""
        props = feature.get("properties") or {}
        geometry = feature.get("geometry") or {}
        coordinates = geometry.get("coordinates") or []

        longitude = _as_float(coordinates[0]) if len(coordinates) > 0 else None
        latitude = _as_float(coordinates[1]) if len(coordinates) > 1 else None

        kenn = str(props.get("kenn") or "").strip()
        if not kenn:
            raise ValueError("Feature has no station identifier 'kenn'")

        return cls(
            kenn=kenn,
            international_id=_as_str(props.get("id")),
            name=_as_str(props.get("name")) or kenn,
            postal_code=_as_str(props.get("plz")),
            longitude=longitude,
            latitude=latitude,
            height_above_sea=_as_float(props.get("height_above_sea")),
            site_status=_as_int(props.get("site_status")),
            site_status_text=_as_str(props.get("site_status_text")),
            network_node=_as_int(props.get("kid")),
            start_measure=_as_datetime(props.get("start_measure")),
            end_measure=_as_datetime(props.get("end_measure")),
            value=_as_float(props.get("value")),
            value_cosmic=_as_float(props.get("value_cosmic")),
            value_terrestrial=_as_float(props.get("value_terrestrial")),
            unit=_as_str(props.get("unit")) or "µSv/h",
            validated=_as_int(props.get("validated")),
            nuclide=_as_str(props.get("nuclide")),
            duration=_as_str(props.get("duration")),
        )


def _as_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
