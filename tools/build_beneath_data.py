"""Build the compact data for the Panel 75 3D web page (/beneath/).

Usage: python3 build_beneath_data.py <p75_block_data.json> <p75_labels.json> <out_dir>
Writes <out_dir>/p75.json (vectors, metadata) and <out_dir>/p75.bin (terrain heights and trees).
All coordinates are in the panel frame (h along the panel, ESE positive; d across, NNE positive; z feet above sea level).
"""
import json, sys, os
import numpy as np

src, lab_src, out = sys.argv[1], sys.argv[2], sys.argv[3]
B = json.load(open(src)); LAB = json.load(open(lab_src))
D0_CUT, D1_CUT = -760.0, 2150.0          # same block as the poster

Hg = np.array(B["Hg"]); Dg_all = np.array(B["Dg"]); Zg_all = np.array(B["Zg"]); STEP = B["step"]
keep = (Dg_all >= D0_CUT - 1e-6) & (Dg_all <= D1_CUT + 1e-6)
Dg = Dg_all[keep]; Zg = Zg_all[keep]
H0, H1, D0, D1 = float(Hg[0]), float(Hg[-1]), float(Dg[0]), float(Dg[-1])
inside = lambda h, d: H0 <= h <= H1 and D0 <= d <= D1
r1 = lambda v: round(float(v), 1)

# terrain: int16 decifeet
terr = np.round(Zg * 10).astype("<i2")

# trees in the block: int16 h, d, z (decifeet) + uint8 height, crown radius
T = np.array([t for t in B["trees"] if inside(t[0], t[1])])
t_i16 = np.c_[np.round(T[:, 0]), np.round(T[:, 1]), np.round(T[:, 2] * 10)].astype("<i2")
t_u8 = np.c_[np.clip(np.round(T[:, 3]), 0, 255), np.clip(np.round(T[:, 4]), 0, 255)].astype("u1")

p75 = [p for p in B["panels"] if p["mine"] == "Cumberland" and str(p["id"]) == "75"][0]
P = np.array(p75["poly"])
panel = {"id": "75", "mine": "Cumberland", "year": p75.get("year"), "status": p75.get("status"),
         "h0": r1(P[:, 0].min()), "h1": r1(P[:, 0].max()), "d0": r1(P[:, 1].min()), "d1": r1(P[:, 1].max())}

roads = []
for r in B["roads"]:
    pts = [[r1(a), r1(b), r1(c)] for a, b, c in r["pts"]]
    # keep runs inside the block
    run = []
    for p in pts:
        if inside(p[0], p[1]): run.append(p)
        else:
            if len(run) > 1: roads.append({"name": r.get("name", ""), "major": bool(r["major"]), "pts": run})
            run = []
    if len(run) > 1: roads.append({"name": r.get("name", ""), "major": bool(r["major"]), "pts": run})

streams = [[r1(v) for v in s] for s in B["streams"] if inside(s[0], s[1]) and inside(s[3], s[4])]
power = [{"v": p.get("v", ""), "kind": p.get("kind", ""), "pts": [[r1(a), r1(b)] for a, b, *_ in p["pts"] if inside(a, b)]} for p in B["power"]]
towers = [[r1(v) for v in t] for t in B["towers"] if inside(t[0], t[1])]
poles = [[r1(v) for v in t] for t in B["poles"] if inside(t[0], t[1])]
subs = [[[r1(a), r1(b)] for a, b in s] for s in B["subs"] if all(inside(a, b) for a, b in s)]
blds = [{"type": b.get("type", ""), "eave": b["eave"], "ridge": b["ridge"], "z": r1(b["z"]), "src": b.get("src", ""),
         "poly": [[r1(a), r1(c)] for a, c in b["poly"]]} for b in B["buildings"] if all(inside(a, c) for a, c in b["poly"])]

meta = {
    "frame": {"center_2272": B["center"], "axis_deg": B["axis_deg"], "note": "h along panel 75 (ESE +), d across (NNE +), z ft above sea level"},
    "grid": {"h0": H0, "d0": D0, "step": STEP, "nh": len(Hg), "nd": len(Dg), "h1": H1, "d1": D1},
    "seam_q": B["seam_q"], "seam_rms": B.get("seam_rms"), "seam_ft": 7.0, "slab_scale": 10.0, "zbot": 250.0,
    "panel": panel, "roads": roads, "streams": streams, "power": power, "towers": towers, "poles": poles,
    "subs": subs, "buildings": blds, "labels": LAB,
    "bin": {"terrain_i16": [0, int(terr.size)], "trees_i16": [int(terr.nbytes), int(t_i16.size)],
            "trees_u8": [int(terr.nbytes + t_i16.nbytes), int(t_u8.size)], "ntrees": int(len(T))},
}
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "p75.bin"), "wb") as f:
    f.write(terr.tobytes()); f.write(t_i16.tobytes()); f.write(t_u8.tobytes())
json.dump(meta, open(os.path.join(out, "p75.json"), "w"), separators=(",", ":"))
print("grid", len(Hg), "x", len(Dg), "trees", len(T), "roads", len(roads), "streams", len(streams), "buildings", len(blds),
      "towers", len(towers), "poles", len(poles), "subs", len(subs), "bin bytes", os.path.getsize(os.path.join(out, "p75.bin")),
      "json bytes", os.path.getsize(os.path.join(out, "p75.json")))
print("panel", panel)
print("z range", float(Zg.min()), float(Zg.max()))
