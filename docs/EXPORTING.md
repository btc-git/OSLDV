# OSLDV Export and Audit Reference

[README](../README.md) | [Technical reference](TECHNICAL.md) | [Building from source](BUILDING.md)

## Paired Outputs and Audit Logs

Each generation writes a `.kml`, `.geojson`, and `.txt` file with the same base name. The log records source and output SHA-256 hashes (digital fingerprints), column mappings, date/time interpretation, visualization settings, counts of included and skipped records, and warnings without copying source-record contents.

## Coordinate Precision

CSV imports preserve coordinate text and leading zeros in identifiers, while keeping the existing missing-value rules. Geographic calculations still use ordinary numeric coordinates; only source/evidence text retains all supplied digits, and derived geometry remains formatted to six decimal places. Excel numeric cells retain their existing spreadsheet precision.

## Source Integrity

Input hashes are captured when records, cell site lists, or marker lists are loaded. Parsing and hashing use the same open file, with file identity, size, and modification timestamps checked for changes during loading; a detected change stops the load and requires reloading. Later edits or removal of an input do not replace its captured hash in the generation log. Importing different versions of one marker-list file records each loaded version separately.

## Overwrite and Recovery Behavior

Before saving, the application confirms replacement of any existing sibling outputs, not just the selected GeoJSON. All required files, including the TXT log and the optional viewer project, are staged before existing files are replaced. An ordinary save failure restores the previous output set; if recovery itself is blocked, the error identifies retained backup files. This protects against normal I/O failures, but does not provide a crash-atomic multi-file transaction: keep backups of important files independently.

## Viewer Projects and Reopening Outputs

**Process and Open in Viewer** also creates a same-named `.geolibre` companion beside the outputs. This small viewer project does not duplicate the source records: it references the GeoJSON and stores its path, display name, dataset identifier, map extent, and viewer/plugin settings so GeoLibre can reopen it with the OSLDV interface and frame its events automatically. Keep the `.geolibre` file with its GeoJSON; moving or renaming the GeoJSON can break the reference. The project may be deleted without affecting the KML, GeoJSON, or TXT files if convenient reopening is not needed. **Open Viewer** starts a clean, plugin-enabled session. Use the prominent **Load GeoJSON** button beneath the viewer-panel title for previous OSLDV exports; repeat it to add more record sets. KML files remain available through GeoLibre drag and drop. On first use, the application verifies and extracts its pinned GeoLibre portable bundle and installs the included OSLDV viewer plugin in GeoLibre's per-user plugin directory. Because GeoLibre enforces one running instance per Windows session, close any other GeoLibre window before starting the included viewer.

### Viewer Updates

The included viewer is updated through tested OSLDV releases.
GeoLibre's update button offers a standalone installer; it does not update
our pinned portable bundle. To suppress startup prompts, use GeoLibre
**Settings -> Updates -> Check for updates on startup**. See
[bundled viewer update guidance](../GeoLibre-Viewer/README.md#update-prompts) for
accessing Settings in simplified mode and the shared-settings/security caveats.

### Generated Project Provenance

Newly generated `.geolibre` projects use `"generatedBy": "OSLDV"` in both
project-level and layer-level metadata. Previously generated files may contain
`"generatedBy": "OS-LocationDataVisualizer"` and are not rewritten.
External tools that filter on the old producer value may need updating.

This changes only the producer label. The plugin ID `osloc-dat-viz-viewer`,
project settings keys, `osloc_*` export metadata, and schema versions remain
unchanged. See [plugin compatibility](../GeoLibre-Plugin/README.md) and the
[privacy and security notice](../README.md#privacy--security).
