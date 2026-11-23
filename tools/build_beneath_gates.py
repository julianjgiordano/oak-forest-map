"""Gate roads (development entries and pillars) beside Cumberland panel 75, measured on the mine's subsidence map.

Source: Cumberland Mine subsidence map, 96th projection, sheet 31-4 (Mine Maps/2080_SIXM_200_31-4_P96.jpg, 19,232 x 14,436 px).
The sheet is drawn square to the panels. Entry lines are found as long dark rows; crosscuts as pairs of dark crossings
(one entry width apart) on three sample rows through each pillar row, which also gives their lean. Gaps where a crosscut
was not detected (text, roads, symbols over the lines) are filled at the row's median pitch, and the pattern is continued
at that pitch beyond the sheet to the ends of the block. The result is a measured sketch, not a survey.

Usage: python3 build_beneath_gates.py <Oak Forest folder> <out p75_gates.json>
"""
import json, math, sys, os
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT, OUT = sys.argv[1], sys.argv[2]
G = json.load(open(os.path.join(ROOT, "Longwall Posters/01_Data/sheet_31-4_georef.json")))
S = json.load(open(os.path.join(ROOT, "Longwall Posters/01_Data/section_data.json")))
B = json.load(open(os.path.join(ROOT, "Longwall Posters/01_Data/p75_block_data.json")))
im = Image.open(os.path.join(ROOT, "Mine Maps/2080_SIXM_200_31-4_P96.jpg")).convert("L")
W0, H0_ = im.size
a = np.asarray(im.resize((W0 // 2, H0_ // 2), Image.BILINEAR)); dark = a < 110
H, W = a.shape
R = W0 / 14999.0                       # the georeference was made on the 14,999-px copy (half resolution)

cx, cy = S["center"]; ux, uy = S["u"]; vx, vy = S["v"]
C = np.array(B["center"]); t = math.radians(B["axis_deg"]); A = np.array([math.cos(t), math.sin(t)]); N = np.array([-A[1], A[0]])
def px_to_hd(X, Y):                    # X, Y: pixels of the half-resolution full map
    Xg, Yg = X / R, Y / R
    s = G["smid"] + (G["Y0"] + G["dy"] - Yg) * G["k"]; w = (Xg - G["X0"]) * G["k"]
    x, y = cx + s * ux + w * vx, cy + s * uy + w * vy
    q = np.array([x, y]) - C
    return float(q @ A), float(q @ N)
FT = abs(px_to_hd(0, 1000)[1] - px_to_hd(0, 0)[1]) / 1000   # feet per half-res pixel (across)
FTX = abs(px_to_hd(1000, 500)[0] - px_to_hd(0, 500)[0]) / 1000

# rows (half-res) of the entry lines, read from the row profile of dark pixels (x 600-7800)
# north gate of panel 75 (between 75 and the unmined coal to the north) and south gate (between 75 and 74)
GATES = {
    "north": {"entries": [(879, 897), (991, 1006), (1080, 1097)], "rows": [(897, 991), (1006, 1080)]},
    "south": {"entries": [(2482, 2500), (2640, 2655), (2719, 2736)], "rows": [(2500, 2640), (2655, 2719)]},
}

def runs(row):
    r = dark[row]; d = np.diff(np.r_[0, r.astype(np.int8), 0]); st = np.where(d == 1)[0]; en = np.where(d == -1)[0]
    return [((s + e) / 2, e - s) for s, e in zip(st, en)]
def pairs(row):
    rs = [x for x, w in runs(row) if w <= 8]
    return [(p + q) / 2 for p, q in zip(rs, rs[1:]) if 10 <= q - p <= 28]

X_MIN, X_MAX = 150, 8050               # map area (legend to the right)
out = {"source": "Cumberland Mine subsidence map, 96th projection, sheet 31-4", "ft_per_px": [round(FTX, 4), round(FT, 4)], "gates": {}}
for gname, g in GATES.items():
    ents = []
    for y0, y1 in g["entries"]:
        d0 = px_to_hd(4000, y1)[1]; d1 = px_to_hd(4000, y0)[1]; ents.append([round(d0, 1), round(d1, 1)])
    rows = []
    for y0, y1 in g["rows"]:
        h_ = y1 - y0; ys = [int(y0 + h_ * f) for f in (0.3, 0.5, 0.7)]
        P = [pairs(y) for y in ys]; good = []
        for x in P[1]:
            a_ = [p for p in P[0] if abs(p - x) < h_ * 0.6]; b_ = [p for p in P[2] if abs(p - x) < h_ * 0.6]
            if a_ and b_:
                xa = min(a_, key=lambda p: abs(p - x)); xb = min(b_, key=lambda p: abs(p - x))
                s1 = (x - xa) / (ys[1] - ys[0]); s2 = (xb - x) / (ys[2] - ys[1])
                if abs(s1 - s2) < 0.25 and 0.1 < (s1 + s2) / 2 < 0.7: good.append((x, (s1 + s2) / 2))
        good.sort()
        xs = np.array([x for x, _ in good]); slope = float(np.median([s for _, s in good]))
        gaps = np.diff(xs); pitch = float(np.median(gaps[(gaps > 60) & (gaps < 420)]))
        # keep detections that sit on the pitch; drop near-duplicates
        keep = [xs[0]]
        for x in xs[1:]:
            if x - keep[-1] > 0.6 * pitch: keep.append(x)
        # fill gaps at the pitch
        full = [keep[0]]
        for x in keep[1:]:
            n = int(round((x - full[-1]) / pitch))
            for k in range(1, n): full.append(full[-1] + (x - full[-1]) / (n - k + 1))
            full.append(x)
        ym = (y0 + y1) / 2
        hs = [px_to_hd(x, ym)[0] for x in full]
        d_top, d_bot = px_to_hd(4000, y0)[1], px_to_hd(4000, y1)[1]
        dhdd = -slope * FTX / FT          # lean of the crosscuts in the panel frame (dh per dd)
        pitch_ft = pitch * FTX
        rows.append({"d0": round(d_bot, 1), "d1": round(d_top, 1), "pitch_ft": round(pitch_ft, 1), "lean_dh_per_dd": round(dhdd, 3),
                     "detected": len(keep), "crosscuts_h": [round(h, 1) for h in hs],
                     "map_h_range": [round(px_to_hd(X_MIN, ym)[0], 1), round(px_to_hd(X_MAX, ym)[0], 1)]})
        print(gname, "row d", round(d_bot), round(d_top), "pitch ft", round(pitch_ft), "lean", round(dhdd, 2), "detected", len(keep), "after fill", len(full))
    out["gates"][gname] = {"entries_d": ents, "rows": rows}
    print(gname, "entries d", ents)
out["entry_width_ft"] = 18
json.dump(out, open(OUT, "w"), separators=(",", ":"))
print("ft/px", FTX, FT, "wrote", OUT)
