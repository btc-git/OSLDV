/*
 * Open Source Location Data Visualizer - github.com/btc-git/OSLDV
 * Licensed under the GNU General Public License v3.0 - see LICENSE for details
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const pluginPath = path.join(repositoryRoot, "GeoLibre-Plugin", "dist", "index.js");
const manifestPath = path.join(repositoryRoot, "GeoLibre-Plugin", "plugin.json");
const stylePath = path.join(repositoryRoot, "GeoLibre-Plugin", "dist", "style.css");

const toolbarClasses = new Set();
const toolbar = {
    classList: {
        add(value) { toolbarClasses.add(value); },
        remove(value) { toolbarClasses.delete(value); },
    },
};
const pluginButton = {
    getAttribute(name) {
        return name === "aria-label" ? "OSLDV" : null;
    },
    closest(selector) {
        return selector === "header" ? toolbar : null;
    },
};

let observerDisconnects = 0;
globalThis.document = {
    body: {},
    querySelectorAll(selector) {
        assert.equal(selector, "header button");
        return [pluginButton];
    },
};
globalThis.MutationObserver = class {
    observe(target, options) {
        assert.equal(target, globalThis.document.body);
        assert.deepEqual(options, { childList: true, subtree: true });
    }

    disconnect() {
        observerDisconnects += 1;
    }
};

const pluginSource = fs.readFileSync(pluginPath, "utf8");
const pluginModule = await import(
    `data:text/javascript;base64,${Buffer.from(pluginSource).toString("base64")}`
);
const plugin = pluginModule.default;

assert.equal(pluginModule.humanizeEventType("tower_sector"), "Cell Site/Sector");
assert.equal(
    pluginModule.humanizeEventType("tower_sector_distance"),
    "Cell Site/Sector + distance",
);
assert.equal(
    pluginModule.humanizeEventType("tower_no_azimuth"),
    "Cell Site / no azimuth",
);
const {
    eventDisplayMinute,
    eventMatchesDateTimeBounds,
    eventUsesMapLabel,
    formatMapTimeLabel,
    humanizeEventType,
    loadOslocGeoJson,
    markerColorExpression,
    normalizeDateTimeFilterValue,
    parseOslocGeoJson,
    referenceSiteRowDetails,
    sharedPointVisibilityFilter,
} = pluginModule;
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
assert.equal(plugin.id, "osloc-dat-viz-viewer");
assert.equal(manifest.id, plugin.id);
assert.equal(plugin.name, "OSLDV Viewer");
assert.equal(manifest.name, plugin.name);
assert.equal(plugin.version, manifest.version);
assert.equal(plugin.restoresPanelCollapseState, true);

assert.equal(
    normalizeDateTimeFilterValue("2024-01-15", false),
    "2024-01-15T00:00",
);
assert.equal(
    normalizeDateTimeFilterValue("2024-01-15", true),
    "2024-01-15T23:59",
);
assert.equal(
    normalizeDateTimeFilterValue("2024-01-15T14:30", true),
    "2024-01-15T14:30",
);
assert.equal(normalizeDateTimeFilterValue("2024-02-30T14:30"), null);
assert.equal(normalizeDateTimeFilterValue("2024-01-15T24:00"), null);
assert(
    JSON.stringify(sharedPointVisibilityFilter()).includes('reference_site')
);
assert(
    JSON.stringify(sharedPointVisibilityFilter()).includes('marker')
);
assert.deepEqual(
    markerColorExpression(),
    ["coalesce", ["get", "osloc_style_marker_color_rgba"], "#e53935"],
);
assert.equal(humanizeEventType("marker"), "Marker");
assert.equal(
    formatMapTimeLabel({ eventType: "marker", label: "Residence" }),
    "Residence",
);
assert(eventUsesMapLabel({ eventType: "marker" }, false));
assert(!eventUsesMapLabel({ eventType: "reference_site" }, false));
assert(eventUsesMapLabel({ eventType: "location", startMs: 1, endMs: 2 }, true));
assert.deepEqual(
    referenceSiteRowDetails({
        eventType: "reference_site",
        cslSourceRows: "12, 13",
    }),
    { label: "CSL Rows", value: "12, 13" },
);
assert.deepEqual(
    referenceSiteRowDetails({
        eventType: "reference_site",
        sourceRows: "7",
    }),
    { label: "Source Row", value: "7" },
);
assert.equal(
    referenceSiteRowDetails({ eventType: "tower_sector" }),
    null,
);

const localEvent = {
    startMs: Date.parse("2024-01-15T19:30:59Z"),
    endMs: Date.parse("2024-01-15T19:31:59Z"),
    localStart: "2024-01-15T14:30:59-05:00",
    timezone: "America/New_York",
};
assert.equal(eventDisplayMinute(localEvent), "2024-01-15T14:30");
assert(eventMatchesDateTimeBounds(
    localEvent,
    "2024-01-15T14:30",
    "2024-01-15T14:30",
));
assert(!eventMatchesDateTimeBounds(
    localEvent,
    "2024-01-15T14:31",
    "",
));
assert(eventMatchesDateTimeBounds(
    { startMs: Number.NaN, endMs: Number.NaN },
    "2024-01-15T14:31",
    "2024-01-15T15:00",
));
assert.equal(
    eventDisplayMinute({
        startMs: Date.parse("2024-01-15T19:30:00Z"),
        endMs: Date.parse("2024-01-15T19:31:00Z"),
        timezone: "America/New_York",
    }),
    "2024-01-15T14:30",
);

const previousExport = {
    type: "FeatureCollection",
    osloc_dataset_id: "previous-export",
    osloc_dataset_name: "Previous Export",
    features: [{
        type: "Feature",
        properties: {
            osloc_dataset_id: "previous-export",
            osloc_event_id: "event-1",
        },
        geometry: { type: "Point", coordinates: [-77.61, 43.15] },
    }],
};
assert.equal(parseOslocGeoJson(JSON.stringify(previousExport)).name, "Previous Export");
const legacyExport = {
    type: "FeatureCollection",
    osloc_export_id: "legacy-export",
    features: [{
        ...previousExport.features[0],
        properties: {
            osloc_export_id: "legacy-export",
            osloc_export_name: "Legacy Export",
            osloc_event_id: "event-1",
        },
    }],
};
const parsedLegacyExport = parseOslocGeoJson(JSON.stringify(legacyExport));
assert.equal(parsedLegacyExport.datasetId, "legacy-export");
assert.equal(parsedLegacyExport.name, "Legacy Export");
assert.throws(
    () => parseOslocGeoJson('{"type":"FeatureCollection","features":[]}'),
    /OSLDV event metadata/,
);

let importOptions = null;
let addedLayer = null;
const imported = await loadOslocGeoJson({
    importTextFile(options) {
        importOptions = options;
        return Promise.resolve(JSON.stringify(previousExport));
    },
    addGeoJsonLayer(name, data) {
        addedLayer = { name, data };
        return "loaded-layer";
    },
});
assert.deepEqual(importOptions.extensions, ["geojson"]);
assert.equal(importOptions.description, "OSLDV GeoJSON");
assert.equal(imported.layerId, "loaded-layer");
assert.equal(addedLayer.name, "Previous Export");
assert.deepEqual(addedLayer.data, previousExport);
assert.equal(
    eventDisplayMinute({
        startMs: Date.parse("2024-01-15T19:30:00Z"),
        endMs: Date.parse("2024-01-15T19:31:00Z"),
        timezone: "Fixed UTC -05:00",
    }),
    "2024-01-15T14:30",
);

let panelOpenCalls = 0;
let registeredPanel = null;
let registeredMenu = null;
const app = {
    getMap() { return null; },
    registerRightPanel(panel) { registeredPanel = panel; return () => { }; },
    registerToolbarMenu(menu) { registeredMenu = menu; return () => { }; },
    openRightPanel(id) {
        assert.equal(id, "osloc-dat-viz-panel");
        panelOpenCalls += 1;
    },
    closeRightPanel() { },
    closeFloatingPanel() { },
};
const simplifiedClass = "osloc-simplified-viewer-toolbar";

const savedProject = {
    plugins: {
        activePluginIds: ["osloc-dat-viz-viewer"],
        settings: {
            "osloc-dat-viz-viewer": {
                autoShowAll: false,
                autoFocus: true,
                simplifiedViewer: true,
                startupDatasetId: "previous-export",
            },
        },
    },
};
assert(savedProject.plugins.activePluginIds.includes(plugin.id));
plugin.applyProjectState(app, savedProject.plugins.settings[plugin.id]);
plugin.activate(app);
assert.equal(registeredPanel.id, "osloc-dat-viz-panel");
assert.equal(registeredPanel.title, "OSLDV");
assert.equal(registeredMenu.id, "osloc-dat-viz-menu");
assert.equal(registeredMenu.label, "OSLDV");
assert(toolbarClasses.has(simplifiedClass));
assert.equal(panelOpenCalls, 1);

plugin.applyProjectState(app, { simplifiedViewer: false });
assert(!toolbarClasses.has(simplifiedClass));
assert.equal(observerDisconnects, 1);

plugin.applyProjectState(app, { simplifiedViewer: true });
assert.equal(panelOpenCalls, 2);
plugin.deactivate(app);
assert(!toolbarClasses.has(simplifiedClass));
assert.equal(observerDisconnects, 2);

const styleSource = fs.readFileSync(stylePath, "utf8");
assert(styleSource.includes(`header.${simplifiedClass} button`));
assert(styleSource.includes(`button[aria-label="OSLDV"]`));
assert(pluginSource.includes('"OSLDV source and license", "https://github.com/btc-git/OSLDV"'));
assert(pluginSource.includes('input.type = "datetime-local"'));
assert(pluginSource.includes('input.step = "60"'));
assert(pluginSource.includes('makeButton("Load GeoJSON"'));
assert(styleSource.includes('input[type="datetime-local"]'));

console.log("Simplified viewer chrome and date/time filter contracts passed.");