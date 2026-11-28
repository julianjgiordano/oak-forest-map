# Change log: Oak Forest project website

Every change is a commit on GitHub (Commits tab). To see or restore an earlier version, open a commit and click "Browse files", or ask Claude to restore it. Milestones are listed here by commit.

## v2.1 (28 Nov 2026): Through Time from 1939
- Four early aerial years added to Through Time, from U.S. Department of Agriculture photographs via Penn Pilot (Pennsylvania Geological Survey and PASDA): 1939 (frame APU-106-8, 25 June 1939), 1950 (APU-4F-41, 2 June 1950), 1958 (APU-3V-134, 27 August 1958) and 1967 (APU-7HH-232 and APU-8HH-13, 4 October 1967). 17 views in all.
- Placed on the map with a camera model that corrects for the hills (3DEP elevation), fitted to hundreds of automatically matched features per photograph against the 1992 orthophoto and the other early years. Average error about 1.6 m (1967), 3 m (1958), 3 to 4 m (1950) and 4 m (1939); each year's caption gives its method and error. Tiles: through-time/tiles/1939, 1950, 1958, 1967 (zoom 14 to 18).
- Labelled years on the timeline are now 1876, 1958, 1992, 2010 and 2022 (evenly spaced, so they don't run together on phones). Intro text on Through Time and the landing page: "aerial photographs from 1939 to 2022".
- The 1876 street names are now point labels at each street's midpoint, turned to the street, with the modern name on a second line (Broad Street's label used to be dropped). Shown from zoom 16 as before.
- Site icon (favicon.svg, favicon.ico, apple-touch-icon.png) linked from every page.
- About page: a row per new year in the Through Time sources table, "Seventeen views", the sentence promising the older photographs removed.
- Not published in this release: the Panel 75 story and the Panel 75 close-up changes (still on the drafts branch).

## v2.0.1 (24 Nov 2026)
- Property map: clicking one of the 298 parcel shapes that have no county record no longer opens an empty panel; the tooltip says there is no county record.

## v2.0 (24 Nov 2026): the property map covers all of Greene County
- /map/ is now "Who owns Greene County?": all 29,117 mapped parcels in the county, opening on the whole county (the village view is at /map/#oak-forest). Replaces the village-only map (v1.0–v1.8.1); the old version stays in this repository's history (commit 0e80dd0, file map/index.html) and can be restored.
- Colours match the county figures: CONSOL / Core and affiliates (blue), Iron Senergy and predecessors (orange), other coal companies including Duquesne Light's Warwick Mine land (mauve); Pennsylvania Game Commission land in green, darker where acquired directly from a coal company; other owners left clear. "Coal, outside village" merged into the company colours; Oak Forest marked by a dashed outline.
- Switches: mine permit areas (active solid, no longer active dashed), longwall panels (one colour), older mined-out areas, game lands. Base maps unchanged (Map / Topographic / Satellite).
- "Coal purchases over time" replaces the "year a coal company bought it" colouring: a slider and play button (1940 to today) colour parcels as the county's sales records show coal companies buying them, with a stacked chart of coal-owned acres by company group.
- Parcel panel: a one- or two-sentence plain-language summary (who bought it, when, from whom, acreage, price and how it is known, 2026-dollar equivalent, later transfers between affiliated companies, what the sellers had paid); facts incl. land use in plain words and mining context (permit area, share above longwall panels and years mined); every recorded sale shown as "from A to B" with a label for how the price is known (stated in the deed, calculated from the transfer tax, county record, one total for N parcels, $0 on file, nominal, between affiliated companies). Oak Forest parcels keep Julian's deed chains.
- Search by owner or parcel number across the county; "Go to" Oak Forest, Waynesburg and the four operating mines.
- Data: map/data/ (parcels.json, sales/s*.json loaded on click, mines, panels, mined-out areas, outlines), built by build_web_data.py in the Mac folder "Greene County Web Map/02_Scripts" from dataset v5.6, the coal-map and underground-mines GeoPackages and the village deed data. Owners' names shown as recorded (setting SHOW_PRIVATE_NAMES in map/index.html).
- Landing page card, navigation labels ("Who owns Greene County") and the About page's property-map section and sources updated; new landing preview image (from Fig. 1 of the county figure series).
- Not changed: Through Time, Panel 75 in 3D (only the navigation label).

## v1.8.1 (23 Nov 2026)
- About page: new section "Coal-company land across the county" with the county-wide results (51,829.9 surface acres, 14.2% of listed surface acreage / 14.1% of the county's land; Iron Senergy and predecessors 4.4%), coal-rights figures, sources, procedure, difficult cases, acreage checks and limits, from the Greene County Coal-Company Land Ownership Dataset v5.6.

## v1.8 (23 Nov 2026): landing page, About page, Panel 75 longwall and subsidence
- New landing page at the site root with preview cards for the three projects. The property map moved to /map/ (old links to a parcel, /#4861, are forwarded there). A navigation bar on every page links home, to the three projects and to About.
- New About page (/about/): sources, methods and limits for the property map, Through Time and Panel 75; downloads, citations, research-assistance note, names and corrections.
- Panel 75 in 3D:
  - Gate-road pillars drawn as solid blocks as tall as the panel, so the entries between them read as tunnels.
  - The parts of the Emerald panels (21 Right, 6 Right) that pass beneath the block are always shown; "Neighbouring panels, full extent" shows the rest and adds 73 and 74 to the sequence. (Panel 74 lies just outside the block; its gate road, shared with 75, is drawn.)
  - Shearer close-up at true size: a double-drum ranging shearer on the face conveyor and about 240 two-leg shields 1.75 m wide. Behind the shearer each shield lowers, steps forward one web and resets; the conveyor is pushed over in an S-bend; the roof caves in behind the shields; the coal face steps back where the drums have cut. The camera follows the shearer. Labels name the parts.
  - One pass across the 1,393 ft face takes 30 s by default (about 70× real speed), with 2 min and 7 min settings.
  - Subsidence (modelled, drawn 10×): the ground, trees, houses and roads sink over the mined panel, about 4 ft at the centre, reaching ~200 ft beyond the edges (15° angle of draw), a little as the face passes and the rest over ~7 months. Red contour lines mark 1, 2 and 3 ft of sinking; the ground just behind the moving face pulses while the sequence plays. Switch: "Ground sinking".
  - Broken rock above the mined panel: faint cracks in the caved and fractured zones, appearing as the face advances. Switch: "Broken rock above the panel".

## v1.7.1 (23 Nov 2026): security
- Map libraries pinned to exact versions (MapLibre GL JS 5.24.1, maplibre-contour 0.1.1) with integrity fingerprints (SRI), so a changed or tampered copy on unpkg will not run.
- Content-Security-Policy on all three pages: scripts, styles, fonts and map tiles may load only from this site and the services the maps use (unpkg, Google Fonts, OpenFreeMap, Mapbox, AWS Terrain Tiles); no plugins, no forms.
- To update MapLibre later: change the version in both `<script>`/`<link>` tags and replace the `integrity` values with the new file's sha384 hash.

## v1.7 (23 Nov 2026)
- Panel 75 in 3D: the longwall drawn to scale. The shearer (a dark block, about 45 ft long) runs back and forth across the 1,393 ft face, advancing one 42-inch web per pass (bi-directional cutting, as reported for Cumberland in 2005): about 3,200 passes for panel 75. Its path over the last 14 passes is drawn as a fine zigzag behind it. Timing still follows the month-end face positions on sheet 31-4; the shearer's place along the face is worked out from the face advance.
- New "Shearer" button: flies to the face and plays one pass about every 2 seconds (roughly 1,000 times real speed), with an approximate date and the pass number. The month-by-month play is unchanged (at that speed each pass is far too quick to see).
- Gate roads: the three entries on each side of panel 75, with their pillars and angled crosscuts, measured on the Cumberland Mine subsidence map (96th projection, sheet 31-4) and continued at the same spacing beyond the sheet. Pillars drawn as dark blocks at seam depth; switchable under Layers. Data: beneath/data/p75_gates.json from tools/build_beneath_gates.py.

## v1.6 (23 Nov 2026)
- Panel 75 in 3D: neighbouring panels off by default; with them off, the mining sequence plays panel 75 only (Jul 2022 to Jan 2023), from a new "Before mining began" step. Turning them on restores the 73–75 sequence.
- "From below" view replaced by "From above" (straight down, north up; turned 90° on portrait screens).
- House-to-parcel links switched off for now (code kept; `PARCEL_LINKS` in beneath/index.html).

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
