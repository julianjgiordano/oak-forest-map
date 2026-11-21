# Change log: Oak Forest village map

Every change is a commit on GitHub (Commits tab). To see or restore an earlier version, open a commit and click "Browse files", or ask Claude to restore it. Milestones are listed here by commit.

## v1.1.1 (21 Nov 2026)
- Custom domain oakforest.juliangiordano.com (CNAME added by Julian in GitHub settings); preview image and citation now use it.

## v1.1 (21 Nov 2026)
- Switched from Mapbox GL JS to MapLibre GL JS. Street map: OpenFreeMap vector tiles (sharp at every zoom, no key). Topographic: shaded relief and contour lines in feet, drawn in the browser from AWS Terrain Tiles (USGS 3DEP). Satellite: Mapbox imagery.
- Headline finding at the top; "About this map" panel (findings, definition of a coal company, sources, limits, privacy note, glossary, citation, downloads).
- "Color by": owner today, or year a coal company first bought the parcel (three waves: 1998–2003, 2007–2011, 2016–2021).
- Coal owners grouped by company, with the recorded name shown; deed citations as "Deed Book X, page Y"; nominal prices flagged; Latin abbreviations explained.
- Hatching for coal parcels (not color alone), keyboard focus handling, reduced-motion support, expandable phone panel, social preview image.
- Public downloads in `data/` (no private notes). `tools/build_data.py` rebuilds data.js and the downloads.

## v1.0 (20–21 Nov 2026), commit 8c998a0
- First public version: sidebar, parcel list and detail timelines, OpenStreetMap / USGS topo / Mapbox satellite base maps.
