# Bundled GeoLibre Viewer

The Windows build packages the unmodified GeoLibre Desktop 3.7.0 x64 portable
archive for the **Process and Open in Viewer** and standalone **Open Viewer**
workflows.

- Upstream project: <https://github.com/opengeos/GeoLibre>
- Version: `3.7.0`
- Archive: `geolibre-desktop-3.7.0-x64-portable.zip`
- SHA-256: `797315931e91e6cf31921b0f2aac2eef794f882a7f28746fcedca9e923a2013c`
- License: MIT; see `LICENSE-GeoLibre.txt`

The application verifies the archive hash before extracting it into its own
per-user runtime directory. It installs the OSLDV viewer plugin in GeoLibre's
standard per-user plugin directory. Simplified chrome is enabled by generated
OSLDV companion projects and by the clean project used for reviewing existing
KML or GeoJSON files.

## Update prompts

The included viewer is pinned and updated through OSLDV releases after
compatibility testing. GeoLibre's **Download update package** button downloads a
standalone installer; it does not replace the portable archive included here or
the version this application's launcher selects. Installing that download can
create a separate GeoLibre installation, while **Open Viewer** still launches
the pinned bundle.

To stop the prompts, open GeoLibre **Settings -> Updates**, turn off **Check for
updates on startup**, and restart the viewer. If Settings is hidden by the
OSLDV simplified interface, close the viewer and make a copy of its `.geolibre`
project. In that copy, change
`plugins.settings.osloc-dat-viz-viewer.simplifiedViewer` from `true` to `false`,
then open the copy in GeoLibre to access the Settings toolbar button. Reopen
the original project afterward to restore the simplified interface. There is
no in-panel simplified-mode toggle. **Skip this version** only suppresses that
particular release, not future releases.

Disabling startup checks does not disable geometry, plugins, or basemap loading,
but it also does not fix security issues or keep the viewer current. Maintainers
must continue reviewing upstream fixes and shipping tested bundle updates.
GeoLibre settings are shared per user, so this preference may also apply to a
separately installed GeoLibre. The launcher does not change it automatically.

Generated viewer projects use the OpenFreeMap Liberty basemap. Loading that
basemap requires a network connection and discloses ordinary tile-request
metadata, including IP address and viewed map area, to OpenFreeMap. Local
source-record processing and export do not imply offline basemap viewing.