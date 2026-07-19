"""Tests for BfS ODL GeoJSON model parsing."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

INTEGRATION_DIR = Path(__file__).parents[1] / "custom_components" / "bfs_odl"
sys.path.insert(0, str(INTEGRATION_DIR))

from models import ODLStation  # noqa: E402


class ODLStationTest(unittest.TestCase):
    """Test ODL station conversion."""

    def test_from_feature_parses_measurement(self) -> None:
        """A complete GeoJSON feature is converted to typed values."""
        station = ODLStation.from_feature(
            {
                "geometry": {"coordinates": [6.36, 50.92]},
                "properties": {
                    "id": "DEZ1234",
                    "kenn": "053580243",
                    "plz": "52428",
                    "name": "Jülich",
                    "site_status": 1,
                    "site_status_text": "in Betrieb",
                    "kid": 6,
                    "height_above_sea": 92,
                    "start_measure": "2026-07-19T14:00:00Z",
                    "end_measure": "2026-07-19T15:00:00Z",
                    "value": 0.105,
                    "value_cosmic": 0.043,
                    "value_terrestrial": 0.062,
                    "unit": "µSv/h",
                    "validated": 1,
                    "nuclide": "Gamma-ODL-Brutto",
                    "duration": "1h",
                },
            }
        )

        self.assertEqual(station.kenn, "053580243")
        self.assertEqual(station.name, "Jülich")
        self.assertEqual(station.value, 0.105)
        self.assertEqual(station.value_cosmic, 0.043)
        self.assertEqual(station.value_terrestrial, 0.062)
        self.assertEqual(station.end_measure, datetime(2026, 7, 19, 15, tzinfo=timezone.utc))
        self.assertEqual(station.display_name, "Jülich (52428) – 053580243")

    def test_from_feature_accepts_missing_measurements(self) -> None:
        """An inactive station with null values remains usable."""
        station = ODLStation.from_feature(
            {
                "geometry": None,
                "properties": {
                    "kenn": "010020001",
                    "name": "Leuchtturm Kiel",
                    "value": None,
                    "value_cosmic": None,
                    "value_terrestrial": None,
                    "unit": None,
                },
            }
        )

        self.assertIsNone(station.value)
        self.assertIsNone(station.latitude)
        self.assertIsNone(station.longitude)
        self.assertEqual(station.unit, "µSv/h")

    def test_from_feature_normalizes_invalid_optional_values(self) -> None:
        """Malformed optional data does not prevent station discovery."""
        station = ODLStation.from_feature(
            {
                "geometry": {"coordinates": ["invalid", 51]},
                "properties": {
                    "kenn": " 123 ",
                    "height_above_sea": "unknown",
                    "validated": "unknown",
                    "end_measure": "not-a-date",
                },
            }
        )

        self.assertEqual(station.kenn, "123")
        self.assertEqual(station.name, "123")
        self.assertIsNone(station.longitude)
        self.assertEqual(station.latitude, 51.0)
        self.assertIsNone(station.height_above_sea)
        self.assertIsNone(station.validated)
        self.assertIsNone(station.end_measure)

    def test_from_feature_requires_station_identifier(self) -> None:
        """A feature without a station identifier is rejected."""
        with self.assertRaisesRegex(ValueError, "station identifier"):
            ODLStation.from_feature({"properties": {"name": "Unknown"}})


if __name__ == "__main__":
    unittest.main()
