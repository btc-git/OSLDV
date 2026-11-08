# OSLDV Viewer Plugin

This directory contains the installable GeoLibre viewer plugin used with
OSLDV KML and GeoJSON exports.

The viewer provides a prominent **Load GeoJSON** action for previous
OSLDV exports and supports inclusive local date/time filtering to the
minute, timeline playback, map labels, event details, and focused navigation.
Additional GeoJSON exports can be loaded by repeating the action. KML remains
available through GeoLibre drag and drop. Static reference-cell-site record sets
remain independently toggleable and visible during timeline playback and
date/time filtering. Their event cards and details show the contributing CSL
spreadsheet rows, or original-record rows when no CSL was used.
Static marker record sets are also independently toggleable at the record-set
and individual-event levels. Each marker uses its exported color, keeps its
label visible whenever enabled, remains visible during timeline playback, and
shows its label and coordinates in event details.
Loaded events start hidden. Enable individual events or use **Show All** for
the record set, check the active **From/Through** filter, and use **Focus Set**
to frame the records. Reference cell sites and markers have separate controls.
The panel's **About & licenses** section identifies the GPL-licensed plugin and
the bundled GeoLibre 3.7.0 viewer under its MIT License.

- `plugin.json` defines the plugin package and version.
- `dist/index.js` and `dist/style.css` are the maintained, readable runtime
  source required by GeoLibre.
- `GeoLibre-Plugin.zip` is a generated local package and is intentionally
  ignored. Rebuild it from `plugin.json` and `dist/` when preparing a plugin
  release.

The plugin is covered by the repository's GNU GPL v3.0 license.

The display name is OSLDV, but the plugin ID remains `osloc-dat-viz-viewer`.
Existing projects continue to use that ID in `plugins.activePluginIds` and
`plugins.settings`, including the `simplifiedViewer` setting. Exported
`osloc_*` metadata and legacy `osloc_export_id`/`osloc_export_name` fields
remain supported; renaming the product does not migrate saved data or IDs.