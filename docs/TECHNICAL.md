# OSLDV Technical Reference

[README and basic import steps](../README.md#how-to-use) | [Export and audit reference](EXPORTING.md) | [Building from source](BUILDING.md)

## Features

### Data Type Support

- **Cell Site/Sector Data**: Creates directional wedges using antenna direction (azimuth), or circles when direction is missing; neither depicts RF coverage
- **Distance from Cell Site Data**: Generates distance-based band visualization with configurable inner/outer band thickness
- **Location Point Data**: Displays points with optional accuracy circles; zero or invalid accuracy produces points without circles, and missing accuracy uses the configured default

### Customizable Visualization

- Adjustable sector width, leg length, and shaded area length
- Configurable distance band (inner/outer) for Distance from Cell Site data
- Color-coded data types with customizable colors
- Static reference-site dots with a selectable color and a configurable nearby-CSL radius
- Unlimited static markers with individual colors, map labels, and details
- Configurable unit support (Meters, Feet, Miles, Kilometers)
- Time animation support for chronological display

### Output & Interoperability

- Paired KML and GeoJSON exports with matching event and dataset metadata
- Independently toggleable, untimed reference-cell-site record set for cell-site-based outputs
- Separate static Markers record set with whole-set and individual marker controls
- KML output for Google Earth Pro and compatible GIS software
- GeoJSON output optimized for GeoLibre/MapLibre workflows
- Included [GeoLibre viewer plugin](../GeoLibre-Plugin/README.md) for filtering, timeline playback, labels, and event details
- Direct **Process**, **Process and Open in Viewer**, and **Open Viewer** actions using the included GeoLibre Desktop 3.7.0 portable viewer
- Same-named TXT generation log with source/output hashes, settings, row outcomes, and warnings

### User-Friendly Interface

- Drag-and-drop CSV, XLS, and XLSX input
- Built-in sample XLSX templates for proper formatting
- Manual marker entry plus CSV/XLS/XLSX marker-list drag and drop
- Automatic column-mapping wizard for files that do not match a standard template
- Optional matching to a separate cell site list using site/node and sector/cell IDs to obtain cell site coordinates and antenna direction
- Optional inclusive date/time range filtering during import
- Named timezone and fixed UTC-offset handling
- Human-readable TXT generation log with hashes, settings, row outcomes, and warnings

## Importing Original Records

For original carrier records that do not match a template, the import wizard opens automatically. It supports CSV, XLS, and XLSX files. Select the worksheet, the row containing the column names, and the record type, then match the source columns to the application fields. Its live preview shows the first 25 source rows with each original column name and the application field currently matched to it. Azimuth may be left unmapped when it is unavailable; the application will use a 360-degree visualization. Imported records are prepared in memory and the original file is not modified.

### Date/Time Range Filtering

You can optionally limit the import to a date/time range. By default, the full selected days are included; select **Use exact times** for narrower limits. **Check Matching Rows** shows how many records match the range and have valid mapped coordinates. The filter uses the selected display timezone; **No Change** keeps filtering in the source timezone. The app converts the selected limits and record times to UTC for comparison. While filtering is enabled, records with missing, unreadable, or uncertain times are excluded because the app cannot confirm that they fall within the range. The TXT log records the filter limits and counts.

### Separate Cell Site Lists

Cell Site/Sector and Distance from Cell Site imports can optionally use a separate cell site list. Enable **Use a separate cell site list**, drop or browse to the CSL, select its worksheet and header row, then map a two-part lookup: the original record's site/node ID and sector/cell ID to the corresponding CSL columns. Map CSL cell site latitude, cell site longitude, and optionally sector azimuth. While enabled, the corresponding original-record mappings are disabled and ignored; timestamp, lookup IDs, and Distance from cell site still come from the original records. An unmatched lookup leaves the cell site fields blank. Repeated lookup keys with equivalent mapped cell site values are collapsed automatically. Conflicting duplicates stop the import only when the original records reference that key; the message identifies its site/node ID, sector/cell ID, CSL rows, and differing mapped fields. The TXT generation log records the CSL filename and hash, mappings, source policy, duplicate counts, and match outcomes without recording lookup-key values.

### Reference Cell Sites

Cell-site-based outputs also contain a separate **Reference Cell Sites** record set that can be toggled independently. Without a CSL, it contains each unique cell site coordinate used by the records. With a CSL, it contains the used cell sites plus unique CSL cell sites within the configured radius of any used cell site; the default radius is 25 miles. Sectors sharing one coordinate are combined into one dot. Reference dots show every contributing CSL spreadsheet row, the mapped site ID when available, and the source coordinates. If no CSL is used, they show the contributing original-record rows instead. They use the color selected under **Reference Cell Site Dots** and remain visible during timeline playback and date filtering.

### Markers

The **Markers** tab accepts unlimited manual points or a dropped/browsed CSV, XLS, or XLSX marker list. Each valid row needs `Label`, `Latitude`, `Longitude`, and `Color`; colors may be familiar names such as `red`, `green`, `yellow`, `orange`, `blue`, `purple`, or `black`, or a `#RRGGBB` value. Invalid imported rows are skipped with row-specific status warnings. Markers are exported as a separate untimed record set, remain visible during timeline playback, and provide both whole-set and individual controls in GeoLibre. An enabled marker always shows its label, and its details include the label and source coordinates. Markers belong only to the current source record set: selecting or importing another source clears them, and they are not retained between application sessions.

### Settings and Colors

A small note at the top of Settings and Colors reminds you to hover over labels
for more information. Hover over those labels to see their tooltips.
**Nearby Cell Site Radius (miles)** applies only when using a separate cell
site list: it selects nearby static reference dots, not coverage or event
geometry. Without a CSL, the radius has no effect.

## Data Format Reference

These are the standard template columns, not a list of required values.
Usable latitude and longitude are needed to map each record; cell-site-based
imports can obtain them from a separate cell site list. `Timestamp` is optional
unless an import date/time filter is enabled. `Azimuth` and `Accuracy` are
optional. The wizard requires a mapped `Distance` column for Distance from
Cell Site imports, but individual missing distances omit the distance band
rather than the usable location.

**For Cell Site/Sector Data:**
- `Timestamp`, `Latitude`, `Longitude`, `Azimuth`

**For Distance from Cell Site Data:**
- `Timestamp`, `Latitude`, `Longitude`, `Azimuth`, `Distance`

**For Location Point Data:**
- `Timestamp`, `Latitude`, `Longitude`, `Accuracy` (optional)

**For Marker Lists:**
- `Label`, `Latitude`, `Longitude`, `Color`

The templates use one combined `Timestamp` column, which is recommended. Input files may instead use separate `Date` and `Time` columns, including common variants such as `Conn. Date` and `Conn. Time (UTC)`. Common combined fields such as `Start DateTime`, `StartTime`, `Record Open Date/Time`, and `Msg Send Date` are also recognized.

## Supported Date and Time Formats

The application supports many common date and time formats, including:

**Common Formats:**
- ISO: `2025-01-15T14:30:00`, `2025-01-15 14:30`, `2025/02/11 11:06:07`
- US (4-digit year): `01/15/2025 2:30 PM`, `01/15/2025 2:30`, `08/01/2015 22:14:13`
- US (2-digit year): `07/30/24 13:00:20` (auto-converts: 00–30 → 2000–2030, 31–99 → 1931–1999)
- European: `15.01.2025 14:30:00`, `15.01.2025 14:30`
- Time-only: `14:30:00`, `2:30 PM` (uses today's date)

**Other Date and Time Options:**
- **Excel dates:** The app can read dates and times that Excel stores as numbers, such as `45696.7637037037`
- **With timezone information:** Examples include `2025-02-11 11:06:07.557 EST`, `2019/05/03 18:36:04 (GMT -4)`, and `2025-01-15T14:30:00Z`. An explicit offset, such as `-05:00`, takes priority over your selected source timezone. Resolved times are converted to UTC for the KML and GeoJSON timeline metadata
- **Without timezone information:** The app uses your selected source timezone, either a named timezone or a fixed UTC offset (UTC by default)
- Fixed offsets are shown with familiar North American abbreviations where useful; the numeric UTC offset is authoritative because abbreviations can be ambiguous
- Slash or dash dates use the selected Month-Day-Year or Day-Month-Year order; year-first dates use Year-Month-Day unless Year-Day-Month is selected. Review the wizard's suggested date order before import
- Named timezones apply historical daylight-saving rules. When a local time happens twice or is skipped during a clock change, usable location information is kept without a date/time in both KML and GeoJSON. The app reports source-row numbers rather than guessing a time; an explicit UTC offset can resolve the uncertainty
- **Parts of a second:** For dates and times written as text, digits after the seconds are ignored. For example, `14:30:00.123` is treated as `14:30:00`. Time-only entries use today's date; verify that this matches the source records before use

**Missing-data outcomes:**
- Missing antenna direction (azimuth) uses a 360-degree visualization.
- Missing distance omits the distance band.
- For Location Point data, a positive accuracy value draws an accuracy circle. Missing accuracy uses the configured default radius (initially 0).
- A zero default means no accuracy radius is assumed; it does not mean the location is exact. The point remains visible without a circle.
- A source accuracy value of zero also means unknown accuracy, not an exact location, and draws no circle.
- Invalid accuracy produces a point without an accuracy circle, even when a positive default is configured.
- A positive default is your visualization assumption, not measured accuracy.

Warnings and the TXT log summarize these defaults and omissions, which must be independently verified. Exported records remain initially hidden until enabled in the viewer.

**Missing or unreadable dates and times:** All record types retain usable location information when the date/time is missing, unreadable, or uncertain. These records are labeled `date/time unavailable` and have no timeline time. Warnings and the TXT log count records exported without timeline metadata, including a separate count for daylight-saving conflicts. Timestamp mapping is optional when no import date/time filter is enabled; for separate columns, map both Date and Time or leave both unmapped. An active import date/time range requires timestamp mapping and excludes records with unresolved times because the app cannot confirm that they fall within the selected range. Invalid coordinates are still skipped.

## Sample Data Templates

The application includes built-in templates for each source data type plus marker lists. Click the "📁 Templates" button in the application to download properly formatted XLSX files with sample data and correct column headers.

## Troubleshooting

- **Slow KML viewing:** Try the paired GeoJSON in the included GeoLibre viewer using **Process and Open in Viewer**, or **Open Viewer** followed by **Load GeoJSON**. GeoJSON is optimized for this viewer workflow and may provide smoother interaction; performance still depends on dataset size, geometry, and hardware. Limit the imported date/time range or process smaller subsets if generation or viewing remains slow.
- **Data loaded but nothing visible:** GeoLibre starts records hidden. Enable individual events or use **Show All** for the record set, check any active **From/Through** filter, then use **Focus Set**. Reference-site dots and markers have separate controls.
- **Viewer will not start:** Close other GeoLibre windows before starting the included viewer; only one instance can run per Windows session. Review the status console or error dialog for remaining launch problems.
- **Missing records or unexpected times:** Review source/display timezones, date order, timestamp mappings, coordinates, cell-site-list matches, and import filters. Check summarized warnings and TXT-log row outcomes. All record types retain usable locations without a date/time when timestamps are missing, unreadable, or uncertain, including daylight-saving conflicts. Active import date/time filters exclude these records because their times cannot be confirmed as matching the range.

Processing and export are local. External viewers, map services, and opened links have their own network and privacy behavior; do not assume they are offline.
