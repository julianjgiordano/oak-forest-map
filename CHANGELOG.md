# Change log: Oak Forest village map

Every change is a commit on GitHub (Commits tab). To see or restore an earlier version, open a commit and click "Browse files", or ask Claude to restore it. Milestones are listed here by commit.

## v1.5 (23 Nov 2026)
- Panel 75 in 3D: mining over time. A slider and play button step through the month-end positions of the longwall face (Cumberland Mine subsidence map, sheet 31-4): panel 73 (Dec 2020–Feb 2021), 74 (Oct 2021–Apr 2022) and 75 (Jul 2022–Jan 2023, passing under Oak Forest in December 2022). The mined part of each panel and the edge walls grow with the face; the unmined part of panel 75 shows as a dashed outline.
- Neighbouring panels: Cumberland 73 and 74 and Emerald 21 Right and 6 Right (1993) as faint sheets, each on its own quadratic fit to PA DEP seam elevations; switchable under Layers. (Emerald 20 Right left out: no seam points near it.)
- Houses link to their parcels: hover for the parcel number and whether a coal company owns it (no owner names); click opens it on the property map.
- Data: beneath/data/p75_extra.json, made by tools/build_beneath_extra.py.

## v1.4 (23 Nov 2026)
- New page: Panel 75 in 3D (/beneath/). The land above Cumberland Mine longwall panel 75 (mined 2022–23) and the panel at its true depth, seen through the ground, in the style of the "Panel 75 from the south" poster. Rotate 360°, zoom, pan, look from below.
- Panel shown as on the poster (red slab at the seam, drawn 10× its 7 ft height, blended through the land; dotted outline on the ground; corner lines), plus translucent edge walls fading from the slab up to the surface outline, with faint dashed verticals.
- Controls: ground transparency slider; views (from the south, Oak Forest close-up, from below; portrait screens open on an oblique view fitted to the block); true height or 3× vertical exaggeration (trees and buildings not stretched); layer switches; labels hide when they overlap or leave the screen; keyboard controls; text description for screen readers; social preview image from the poster.
- Built with three.js r170 (vendored in beneath/vendor, MIT licence). Data: beneath/data/p75.json + p75.bin (~610 KB), made by tools/build_beneath_data.py from Longwall Posters/01_Data/p75_block_data.json and p75_labels.json.
- Property map links to the new page.

## v1.3 (21 Nov 2026)
- Through Time: added the 1876 county atlas plat of Oak Forest (Caldwell's atlas, p. 124; David Rumsey Map Collection scan) as the earliest view. Georeferenced by a similarity fit (scale, rotation, shift) to five street points from the 1992 orthophoto: RMSE about 4 m; plat drawn at about 177 ft to the inch (printed: 260). Clipped to the Oak Forest panel; tiles z14-19. 1876 street names (Main, Broad, Water, South) shown with modern equivalents when "Place names" is on.

## v1.2.1 (21 Nov 2026)
- Through Time: removed 1904, 1961 and 2004 (not presentable); added 1982 (NHAP, placed by feature matching to 1992, black and white with contrast stretch). Older PennPilot years (1939–1967) not yet placed.

## v1.2 (21 Nov 2026)
- New page: Oak Forest Through Time (/through-time/): 11 views, 1992–2022 (aerial photographs 1992–2022 from USGS, USDA NAIP, PAMAP and PEMA), with timeline/play, swipe and lens modes, optional property lines. Tiles in through-time/tiles/<year> (WebP, ~47 MB), made with GDAL from the files in the Oak Forest folder.
- Property map links to the new page.

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
