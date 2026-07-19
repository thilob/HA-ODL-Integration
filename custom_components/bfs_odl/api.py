# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Async client for the public ODL WFS interface."""

from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import API_URL, LATEST_LAYER
from .models import ODLStation

PAGE_SIZE = 1000
REQUEST_TIMEOUT = 30


class ODLApiError(Exception):
    """Base exception for ODL communication errors."""


class ODLApiClient:
    """Small asynchronous client for the ODL GeoJSON endpoint."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def async_get_stations(self) -> dict[str, ODLStation]:
        """Fetch all stations, handling WFS pagination."""
        stations: dict[str, ODLStation] = {}
        start_index = 0
        total_features: int | None = None

        while total_features is None or start_index < total_features:
            payload = await self._async_get_page(start_index)
            features = payload.get("features")
            if not isinstance(features, list):
                raise ODLApiError("ODL response contains no GeoJSON feature list")

            for feature in features:
                if not isinstance(feature, dict):
                    continue
                try:
                    station = ODLStation.from_feature(feature)
                except ValueError:
                    continue
                stations[station.kenn] = station

            total_features = _as_nonnegative_int(payload.get("totalFeatures"))
            number_returned = _as_nonnegative_int(payload.get("numberReturned"))
            if number_returned is None:
                number_returned = len(features)

            if number_returned == 0:
                break
            start_index += number_returned

            # Defensive stop for servers omitting totalFeatures or ignoring paging.
            if total_features is None and number_returned < PAGE_SIZE:
                break

        if not stations:
            raise ODLApiError("ODL data service returned no usable measuring stations")
        return stations

    async def _async_get_page(self, start_index: int) -> dict[str, Any]:
        params = {
            "service": "WFS",
            "version": "1.1.0",
            "request": "GetFeature",
            "typeName": LATEST_LAYER,
            "outputFormat": "application/json",
            "maxFeatures": str(PAGE_SIZE),
            "startIndex": str(start_index),
            "sortBy": "kenn",
        }
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                response = await self._session.get(API_URL, params=params)
                response.raise_for_status()
                payload = await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as err:
            raise ODLApiError(f"Error retrieving ODL data: {err}") from err

        if not isinstance(payload, dict):
            raise ODLApiError("Unexpected ODL response format")
        return payload


def _as_nonnegative_int(value: Any) -> int | None:
    try:
        result = int(value)
    except (TypeError, ValueError):
        return None
    return max(result, 0)
