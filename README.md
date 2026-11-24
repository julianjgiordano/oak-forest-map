# Oak Forest, Pennsylvania: research website

Research on Oak Forest and coal-company land ownership in Greene County, Pennsylvania: a county-wide property map ("Who owns Greene County?"), aerial views of the village through time, and the longwall panel mined beneath it in 3D.

Live: https://oakforest.juliangiordano.com/ (also https://julianjgiordano.github.io/oak-forest-map/)

- Chains of title for the 31 village parcels are from deeds read at the Greene County Recorder of Deeds (Julian Giordano). They are partial: earlier owners have not yet been traced.
- Parcel boundaries: Pennsylvania DEP PA_Parcels. Acreage and coal-company classification: Greene County assessment records via Vision Government Solutions (accessed 17–18 Nov 2026) and the Greene County Coal-Company Land Ownership Dataset v5.6.
- Pages: `index.html` (landing page), `map/` (county property map, MapLibre GL JS; data in `map/data/`, built by `build_web_data.py` in the project's Mac folder "Greene County Web Map"), `through-time/`, `beneath/` (Panel 75 in 3D, three.js), `about/`. Shared navigation style in `assets/site.css`.
- `data.js` is generated from the project's QGIS GeoPackage and deed CSVs.
