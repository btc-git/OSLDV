# Diagnostic Tools

These scripts are manual diagnostics, not part of unittest discovery.

## Application icon

The editable logo source is `wifi_icon.svg`. Generate the tracked
`wifi_icon.ico` used by both Qt and the Windows executable after changing it:

```powershell
python tools/generate_app_icon.py
python tools/generate_app_icon.py --check
```

This uses the existing PyQt6 dependency to render native 16, 20, 24, 32, 40, 48,
64, 96, 128, and 256px images with transparent backgrounds. Rebuild through
`app.spec` to update executable and shortcut icons. Existing Windows shortcuts
may retain cached icons; recreate the shortcut if it still displays the old one.

## Manual diagnostics

Generate a matrix of KML variants from a local KML file:

```powershell
python tools/generate_geolibre_import_diagnostics.py --input-kml <input.kml>
```

The default output is the ignored `diagnostics/geolibre_import_matrix/`
directory. Input and generated KML may contain sensitive location data and
must not be committed.

Run the GeoLibre plugin performance and behavior harness with a JSON array of
GeoLibre feature objects:

```powershell
node tools/plugin_performance_harness.mjs <features.json>
```

An alternate plugin JavaScript file can be supplied as the second argument.