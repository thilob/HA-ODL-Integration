# SPDX-FileCopyrightText: 2026 Thilo Berger
# SPDX-License-Identifier: MIT

"""Helpers for ODL WFS queries."""

from __future__ import annotations

from collections.abc import Collection
from xml.etree import ElementTree

OGC_NAMESPACE = "http://www.opengis.net/ogc"


def build_station_filter(station_ids: Collection[str] | None) -> str | None:
    """Build an OGC filter matching one or more station identifiers."""
    if station_ids is None:
        return None

    normalized = sorted(
        normalized_id
        for station_id in station_ids
        if (normalized_id := str(station_id).strip())
    )
    if not normalized:
        return None

    filter_element = ElementTree.Element(f"{{{OGC_NAMESPACE}}}Filter")
    parent = (
        ElementTree.SubElement(filter_element, f"{{{OGC_NAMESPACE}}}Or")
        if len(normalized) > 1
        else filter_element
    )
    for station_id in normalized:
        comparison = ElementTree.SubElement(
            parent, f"{{{OGC_NAMESPACE}}}PropertyIsEqualTo"
        )
        property_name = ElementTree.SubElement(
            comparison, f"{{{OGC_NAMESPACE}}}PropertyName"
        )
        property_name.text = "kenn"
        literal = ElementTree.SubElement(comparison, f"{{{OGC_NAMESPACE}}}Literal")
        literal.text = station_id

    return ElementTree.tostring(filter_element, encoding="unicode")
