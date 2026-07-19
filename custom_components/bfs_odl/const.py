# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Constants for the ODL integration."""

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "bfs_odl"
NAME = "ODL-Messwerte für Home Assistant"

API_URL = "https://www.imis.bfs.de/ogc/opendata/ows"
LATEST_LAYER = "opendata:odlinfo_odl_1h_latest"

DATA_PROVIDER = "Bundesamt für Strahlenschutz (BfS)"
DATA_SOURCE = "ODL-Datenschnittstelle des Bundesamtes für Strahlenschutz"
DATA_LICENSE = "Datenlizenz Deutschland – Namensnennung – Version 2.0"
DATA_LICENSE_ID = "dl-de/by-2-0"
DATA_LICENSE_URL = "https://www.govdata.de/dl-de/by-2-0"
SOFTWARE_LICENSE = "MIT"
SOFTWARE_COPYRIGHT = "Copyright (c) 2026 Thilo Berger"

DATA_SERVICE_URL = (
    "https://odlinfo.bfs.de/ODL/DE/service/datenschnittstelle/"
    "datenschnittstelle_node.html"
)

CONF_STATIONS = "stations"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 30
MIN_SCAN_INTERVAL = 10
MAX_SCAN_INTERVAL = 180
DEFAULT_UPDATE_INTERVAL = timedelta(minutes=DEFAULT_SCAN_INTERVAL)
STATION_CATALOG_CACHE_TTL = timedelta(hours=48)

PLATFORMS = [Platform.SENSOR]
