"""Close the gaps where roads meet in beneath/data/p75.json (24 Nov 2026).

The road centre lines came from several sources and some stop short of the road they join (Maple Run Road ~17 ft short of
Oak Forest Road, Water Street ~40 ft off it at both ends). Checked against the Cumberland Mine subsidence map, sheet 31-4
(georeferenced overlay): the alignments match; only the junctions are open. Each road end that is not at the edge of the
block and lies within 80 ft of another road is extended to the nearest point on that road (a vertex is added there too).

Usage: python3 fix_beneath_roads.py <beneath/data/p75.json>
"""
import json, math, sys
P = sys.argv[1]; m = json.load(open(P)); R = m["roads"]; G = m["grid"]
def near_edge(p): return min(p[0] - G["h0"], G["h1"] - p[0], p[1] - G["d0"], G["d1"] - p[1]) < 30
def closest(p, pts):
    best = (1e18, None, None)
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; dx, dy = b[0] - a[0], b[1] - a[1]; L = dx * dx + dy * dy
        t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
        q = [a[0] + t * dx, a[1] + t * dy, a[2] + t * (b[2] - a[2])]; d = math.dist(p[:2], q[:2])
        if d < best[0]: best = (d, q, i)
    return best
fixed = 0
for k, r in enumerate(R):
    for end in (0, -1):
        p = r["pts"][end]
        if near_edge(p): continue
        cands = [(closest(p, o["pts"]), j) for j, o in enumerate(R) if j != k]
        (d, q, i), j = min(cands, key=lambda c: c[0][0])
        if 1.0 < d <= 80:
            q = [round(v, 1) for v in q]
            if end == 0: r["pts"].insert(0, q)
            else: r["pts"].append(q)
            o = R[j]["pts"]
            if all(math.dist(q[:2], v[:2]) > 1 for v in o): o.insert(i + 1, q)
            fixed += 1; print(f"{r.get('name') or 'road %d' % k} end {end}: joined to {R[j].get('name') or 'road %d' % j} ({d:.0f} ft)")
json.dump(m, open(P, "w"), separators=(",", ":"))
print("junctions closed:", fixed)
