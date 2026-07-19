"""Tests for ODL WFS query helpers."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest
from xml.etree import ElementTree

INTEGRATION_DIR = Path(__file__).parents[1] / "custom_components" / "bfs_odl"
sys.path.insert(0, str(INTEGRATION_DIR))

from wfs import OGC_NAMESPACE, build_station_filter  # noqa: E402


class WFSFilterTest(unittest.TestCase):
    """Test server-side station filtering."""

    def test_no_filter_for_full_catalog(self) -> None:
        """A full catalog request does not add an OGC filter."""
        self.assertIsNone(build_station_filter(None))
        self.assertIsNone(build_station_filter(set()))

    def test_single_station_filter(self) -> None:
        """A single identifier produces one equality comparison."""
        xml_filter = build_station_filter({"053580243"})

        self.assertIsNotNone(xml_filter)
        root = ElementTree.fromstring(xml_filter or "")
        comparisons = root.findall(f"{{{OGC_NAMESPACE}}}PropertyIsEqualTo")
        self.assertEqual(len(comparisons), 1)
        self.assertEqual(
            comparisons[0].findtext(f"{{{OGC_NAMESPACE}}}PropertyName"), "kenn"
        )
        self.assertEqual(
            comparisons[0].findtext(f"{{{OGC_NAMESPACE}}}Literal"), "053580243"
        )

    def test_multiple_station_filter_is_sorted_and_escaped(self) -> None:
        """Multiple identifiers are deduplicated, sorted, and XML-safe."""
        xml_filter = build_station_filter(
            {" 053580243 ", "051200001", "051200001", "<&"}
        )

        self.assertIsNotNone(xml_filter)
        root = ElementTree.fromstring(xml_filter or "")
        literals = root.findall(
            f"{{{OGC_NAMESPACE}}}Or/"
            f"{{{OGC_NAMESPACE}}}PropertyIsEqualTo/"
            f"{{{OGC_NAMESPACE}}}Literal"
        )
        self.assertEqual(
            [literal.text for literal in literals],
            ["051200001", "053580243", "<&"],
        )


if __name__ == "__main__":
    unittest.main()
