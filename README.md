# Oak Forest, Pennsylvania: property map

Interactive map of who owns the land in the village of Oak Forest, Greene County, Pennsylvania, and how it changed hands.

Live: https://oakforest.juliangiordano.com/ (also https://julianjgiordano.github.io/oak-forest-map/)

- Chains of title for the 31 village parcels are from deeds read at the Greene County Recorder of Deeds (Julian Giordano). They are partial: earlier owners have not yet been traced.
- Parcel boundaries: Pennsylvania DEP PA_Parcels. Acreage and coal-company classification: Greene County assessment records via Vision Government Solutions (accessed 17–18 Nov 2026) and the Greene County Coal-Company Land Ownership Dataset v5.6.
- Pages: `index.html` (landing page), `map/` (property map, MapLibre GL JS), `through-time/`, `beneath/` (Panel 75 in 3D, three.js), `about/`. Shared navigation style in `assets/site.css`.
- `data.js` is generated from the project's QGIS GeoPackage and deed CSVs.
