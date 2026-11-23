"""Session 3 data for the Panel 75 3D page: neighbouring panels, longwall face positions, building -> parcel links.

Usage (from the Oak Forest folder):
  python3 build_beneath_extra.py <Longwall Posters/01_Data> <Longwall Posters/05_Scripts> <parcels.geojson> <out p75_extra.json>
Reads p75_block_data.json (panels, buildings), scene_2272.json (faces), raw/coal_seam_elevations_oak_forest.geojson (seam points).
All output coordinates are in the panel-75 frame (h along the panel, ESE +; d across, NNE +; feet).
"""
import json, math, sys, os
from datetime import date
import numpy as np

DATA, SCRIPTS, PARCELS, OUT = sys.argv[1:5]
sys.path.insert(0, SCRIPTS)
import proj

B = json.load(open(os.path.join(DATA, "p75_block_data.json")))
SC = json.load(open(os.path.join(DATA, "scene_2272.json")))
SEAM = json.load(open(os.path.join(DATA, "raw", "coal_seam_elevations_oak_forest.geojson")))
PAR = json.load(open(PARCELS))

C = np.array(B["center"]); t = math.radians(B["axis_deg"])
A = np.array([math.cos(t), math.sin(t)]); N = np.array([-A[1], A[0]])
def hd(x, y): q = np.array([x, y]) - C; return float(q @ A), float(q @ N)
def xy(h, d): return C[0] + h * A[0] + d * N[0], C[1] + h * A[1] + d * N[1]

# ---- seam points in the panel frame
SP = []
for f in SEAM["features"]:
    lon, lat = f["geometry"]["coordinates"][:2]
    h, d = hd(*proj.ll_to_sp(lon, lat)); SP.append((h, d, f["properties"]["COAL_ELEVATION"]))
SP = np.array(SP)

def fit_seam(poly, margin=1500.0):
    P = np.array(poly)
    m = (SP[:, 0] >= P[:, 0].min() - margin) & (SP[:, 0] <= P[:, 0].max() + margin) & (SP[:, 1] >= P[:, 1].min() - margin) & (SP[:, 1] <= P[:, 1].max() + margin)
    pts = SP[m]
    if len(pts) < 30: return None, 0, None
    hh, dd, zz = pts[:, 0] / 1000, pts[:, 1] / 1000, pts[:, 2]
    M = np.c_[np.ones_like(hh), hh, dd, hh * hh, hh * dd, dd * dd]
    coef, *_ = np.linalg.lstsq(M, zz, rcond=None)
    rms = float(np.sqrt(np.mean((M @ coef - zz) ** 2)))
    return [float(c) for c in coef], int(len(pts)), round(rms, 1)

# ---- neighbouring panels
WANT = [("Cumberland", "74"), ("Cumberland", "73"), ("Emerald", "21 Right"), ("Emerald", "20 Right"), ("Emerald", "6 Right")]
neigh = []
for mine, pid in WANT:
    p = [q for q in B["panels"] if q["mine"] == mine and str(q["id"]) == pid][0]
    q_, n_, rms = fit_seam(p["poly"])
    neigh.append({"id": pid, "mine": mine, "year": p["year"], "status": p["status"],
                  "poly": [[round(a, 1), round(b, 1)] for a, b in p["poly"]], "seam_q": q_, "seam_n": n_, "seam_rms": rms})
    print(mine, pid, p["year"], "seam pts", n_, "rms", rms)

# ---- face positions (month ends, sheet 31-4): h of the face line's midpoint
def pdate(s): m, d_, y = map(int, s.split("/")); return date(y, m, d_)
faces = {}
for f in SC["faces"]:
    (x0, y0), (x1, y1) = f["p0"], f["p1"]
    h0, d0 = hd(x0, y0); h1, d1 = hd(x1, y1)
    faces.setdefault(str(f["panel"]), []).append({"date": pdate(f["date"]).isoformat(), "h": round((h0 + h1) / 2, 1), "w": round(f["w"], 1),
                                                   "skew": round(h1 - h0, 1)})
for k in faces: faces[k].sort(key=lambda r: r["date"])
for k, v in faces.items(): print("faces", k, [(r["date"], r["h"], r["w"]) for r in v])

# ---- buildings -> parcels (point in polygon, lon/lat)
def inside(pt, ring):
    x, y = pt; c = False
    for i in range(len(ring)):
        x1, y1 = ring[i]; x2, y2 = ring[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
def rings(geom):
    if geom["type"] == "Polygon": return [geom["coordinates"]]
    return geom["coordinates"]
parcels = []
for f in PAR["features"]:
    pr = f["properties"]
    parcels.append((pr, rings(f["geometry"])))
blinks = []
bld = [b for b in B["buildings"]]
Dg = np.array(B["Dg"]); Dg = Dg[(Dg >= -760.0 - 1e-6) & (Dg <= 2150.0 + 1e-6)]   # same block as build_beneath_data.py
H0, H1, D0, D1 = float(B["Hg"][0]), float(B["Hg"][-1]), float(Dg[0]), float(Dg[-1])
for b in bld:
    if not all(H0 <= a <= H1 and D0 <= c <= D1 for a, c in b["poly"]):
        continue   # same filter as build_beneath_data.py, so indexes line up
    P = np.array(b["poly"]); hc, dc = P.mean(axis=0)
    lon, lat = proj.sp_to_ll(*xy(hc, dc))
    hit = None
    for pr, rs in parcels:
        for poly in rs:
            if inside((lon, lat), poly[0]) and not any(inside((lon, lat), hole) for hole in poly[1:]):
                hit = pr; break
        if hit: break
    if hit:
        blinks.append({"pid": hit["pid"], "coal": bool(hit.get("coal_owner_class")) or hit["map_class"].endswith("_coal"),
                       "company": hit.get("company", ""), "village": int(hit.get("in_village", 0)), "first_coal_year": hit.get("first_coal_year", "")})
    else:
        blinks.append(None)
print("buildings", len(blinks), "linked", sum(1 for x in blinks if x))

json.dump({"neighbours": neigh, "faces": faces, "building_parcels": blinks,
           "notes": "Face positions: Cumberland Mine subsidence map sheet 31-4 (month ends). Neighbour seam surfaces: quadratic fits to PA DEP seam elevation points within 1,500 ft of each panel."},
          open(OUT, "w"), separators=(",", ":"))
print("wrote", OUT, os.path.getsize(OUT))
