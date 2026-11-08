# OSLDV - Open Source Location Data Visualizer

### Development Transparency
This application was developed with AI assistance and has undergone human review and testing. The program itself does not use AI. As with any AI-assisted software, additional scrutiny and verification are recommended before critical use.

---

⚠️ **In active development and testing. Not a validated forensic tool; verify all findings independently.**
OSLDV is a preliminary location-data triage and visualization aid.

## Download

1. **[Download OSLDV.exe](https://github.com/btc-git/OSLDV/releases/latest/download/OSLDV.exe)**
   (latest version for Windows; no installation needed).
2. Double-click it to run. Windows may show "Windows protected your PC" because
   the app is not code-signed: click **More info** → **Run anyway**.

## Privacy & Security

Location-data processing and export run locally; the application does not upload source or output files. Marker entry is coordinate-only: the application does not send addresses to an online geocoding service. Generated KML, GeoJSON, TXT, and GeoLibre project files can contain sensitive information and should be handled together. The GeoLibre project does not duplicate source records, but it contains the GeoJSON's absolute path, dataset name or identifier, and map extent. The included viewer loads its default basemap from OpenFreeMap, which requires a network connection and discloses ordinary tile-request metadata such as IP address and viewed map area to that service. Opening project links or exported files in other applications is subject to those applications' behavior.

## Important Disclaimers

- **This tool is in continuous development and may contain errors.**
- Visualizations are visual aids only and are not RF coverage estimates.
- Verify all findings independently.
- Work from copies of original records and preserve the originals.
- This tool is not a replacement for professional forensic analysis or expert review.

## How to Use

1. Download and run `OSLDV.exe` (see [Download](#download)).
2. Drag and drop a CSV or Excel file into the program, or use the Browse for File button.
3. CSV and XLSX files using the application's standard template column names are recognized automatically. Files in the older XLS format open the mapping wizard.
4. For other files, the **Import Original Records** mapping wizard opens automatically. Select the worksheet and the row containing the column names, choose the record type, and check that each source column is matched to the correct field. You can optionally limit the import to a date/time range.
5. Review the timezone, date order (month or day first), units, and visualization settings. Optionally add or import markers for the current source records on the **Markers** tab.
6. Click **Process** to create the KML, GeoJSON, and TXT generation log, or **Process and Open in Viewer** to create them and immediately open the GeoJSON in the included viewer. Use **Open Viewer**, then **Load GeoJSON**, to review existing GeoJSON files without generating new outputs. GeoJSON is recommended for GeoLibre; KML can be opened in Google Earth Pro.
7. Review warnings and row outcomes in the TXT log. All visualizations remain preliminary and require independent expert review.

See the [technical reference](docs/TECHNICAL.md) for full import, mapping, date/time, cell-site-list, marker, and template details.

## Features

- CSV/XLS/XLSX imports, template detection, and a column-mapping wizard.
- Cell Site/Sector, Distance from Cell Site, and Location Point visualizations.
- Configurable geometry, colors, units, timezones, and timeline playback.
- Separate static reference-cell-site and marker record sets.
- Paired KML/GeoJSON outputs, TXT audit logs, and the bundled GeoLibre viewer.

See the [complete feature reference](docs/TECHNICAL.md#features) and [export guarantees and limitations](docs/EXPORTING.md).

## Application Screenshot

<div align="center">
  <img src="screenshot.PNG" alt="Application Interface" width="350">
</div>

## Documentation

- [Technical reference](docs/TECHNICAL.md): full features, import workflow, data formats, timestamps, missing-data outcomes, templates, and troubleshooting.
- [Export and audit reference](docs/EXPORTING.md): output sets, precision, hashes, overwrite recovery, viewer projects, updates, and provenance.
- [Building from source](docs/BUILDING.md): requirements, setup, tests, locked Windows builds, release preparation, and checksums.
- [Bundled viewer](GeoLibre-Viewer/README.md) and [viewer plugin](GeoLibre-Plugin/README.md): versions, integration, and update guidance.
- [Automated tests](tests/README.md) and [manual diagnostics](tools/README.md).
- [Third-party notices](THIRD_PARTY_NOTICES.md) and [changelog](CHANGELOG.md).

## Troubleshooting

Review the status console and TXT log first. For hidden records, slow viewing, launch problems, or unexpected times, see the [detailed troubleshooting guide](docs/TECHNICAL.md#troubleshooting).

## Open Source & Contributing

This is an open source project. Found a bug or have a suggestion? [Open an issue or suggest a feature here.](https://github.com/btc-git/OSLDV/issues)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

---
Copyright (c) 2025-2026 CrimLawTech LLC
**Version 2.0.1**
_Open Source Location Data Visualization Tool_
