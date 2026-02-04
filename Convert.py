#!/usr/bin/env python3
"""
Garmin FIT → GPX Converter
Converts .fit files from Garmin devices into standard .gpx format.

Usage:
    python convert.py <input.fit> [output.gpx]

Dependencies:
    pip install fitparse
"""

import fitparse
import sys
import xml.etree.ElementTree as ET
import os

# GPX 1.1 namespaces
GPX_NS = "http://www.topografix.com/GPX/1/1"
GPXTPX_NS = "http://www.garmin.com/xmlschemas/TrackPointExtensionv1"

ET.register_namespace("", GPX_NS)
ET.register_namespace("gpxtpx", GPXTPX_NS)


def semicircles_to_degrees(semicircles: int) -> float:
    """Garmin stores coordinates in semicircles. 2^31 semicircles = 180°."""
    return semicircles / (2**31) * 180.0


def fit_to_gpx(fit_file_path: str, gpx_file_path: str = None):
    fitfile = fitparse.FitFile(fit_file_path)

    # --- GPX skeleton ---
    gpx = ET.Element("gpx", version="1.1", creator="Garmin FIT to GPX Converter")
    gpx.set("xmlns", GPX_NS)
    gpx.set("xmlns:gpxtpx", GPXTPX_NS)

    metadata = ET.SubElement(gpx, "metadata")
    trk = ET.SubElement(gpx, "trk")
    name = ET.SubElement(trk, "name")
    name.text = os.path.splitext(os.path.basename(fit_file_path))[0]
    trkseg = ET.SubElement(trk, "trkseg")

    # --- Extract trackpoints ---
    for record in fitfile.get_messages(name="record"):
        values = record.get_values()

        # Skip records with no GPS position — they'd produce empty <trkpt> nodes
        if "position_lat" not in values or "position_long" not in values:
            continue
        if values["position_lat"] is None or values["position_long"] is None:
            continue

        lat = semicircles_to_degrees(values["position_lat"])
        lon = semicircles_to_degrees(values["position_long"])

        trkpt = ET.SubElement(trkseg, "trkpt", lat=str(lat), lon=str(lon))

        # Elevation
        if values.get("altitude") is not None:
            ele = ET.SubElement(trkpt, "ele")
            ele.text = str(round(values["altitude"], 2))

        # Timestamp — fitparse already returns a datetime object, no .value needed
        if values.get("timestamp") is not None:
            time_el = ET.SubElement(trkpt, "time")
            time_el.text = values["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")

        # Extensions: heart rate and/or cadence (single <extensions> block)
        hr = values.get("heart_rate")
        cadence = values.get("cadence")

        if hr is not None or cadence is not None:
            extensions = ET.SubElement(trkpt, "extensions")
            tpe = ET.SubElement(extensions, "gpxtpx:TrackPointExtension")

            if hr is not None:
                hr_el = ET.SubElement(tpe, "gpxtpx:hr")
                hr_el.text = str(hr)

            if cadence is not None:
                cad_el = ET.SubElement(tpe, "gpxtpx:cadence")
                cad_el.text = str(cadence)

    # --- Write output ---
    output_path = gpx_file_path or fit_file_path.replace(".fit", ".gpx")
    tree = ET.ElementTree(gpx)
    ET.indent(tree, space="  ")  # Pretty-print (Python 3.9+)
    tree.write(output_path, xml_declaration=True, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python convert.py <input.fit> [output.gpx]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) == 3 else None

    if not os.path.isfile(input_path):
        print(f"Error: file not found → {input_path}")
        sys.exit(1)

    result = fit_to_gpx(input_path, output_path)
    print(f"Done → {result}")