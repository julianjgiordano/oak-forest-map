"""Rebuild data.js and the public download files.
Inputs: data.js (parcel shapes + fields, made from the QGIS GeoPackage) and the two village CSVs
from 'Oak Forest Property Map/data/'. Private columns (julian_note, julian_comments) are never published."""
import csv, json, re, sys, os
from datetime import datetime
SRC = sys.argv[1]  # folder holding village_deed_history.csv and village_parcels.csv
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
js = open(os.path.join(root, 'data.js')).read()
P = json.loads(re.search(r'const PARCELS=(.*?);\n', js).group(1))
COAL = re.compile(r'CONTURA|IRON PENNSYLVANIA LAND|LAND HOLDINGS|PENNSYLVANIA HOLDINGS CO', re.I)
def company(owner):
    o = owner.upper()
    if 'CONTURA' in o: return 'Contura Pennsylvania Land'
    if 'IRON PENNSYLVANIA' in o or 'IRON SENERGY' in o: return 'Iron Pennsylvania Land (Iron Senergy)'
    if 'LAND HOLDINGS' in o or 'PENNSYLVANIA HOLDINGS CO' in o: return 'Pennsylvania Land Holdings'
    return ''
def year(r):
    m = re.match(r'(\d{4})', r.get('date_iso') or '')
    if m: return int(m.group(1))
    m = re.search(r'(1[89]\d\d|20\d\d)', r.get('date_as_written') or '')
    return int(m.group(1)) if m else None
deeds = {}
for r in csv.DictReader(open(os.path.join(SRC, 'village_deed_history.csv'))):
    deeds.setdefault(r['pid'], []).append(r)
vp = {r['pid']: r for r in csv.DictReader(open(os.path.join(SRC, 'village_parcels.csv')))}
out_deeds = {}; rows = []
for pid, ds in deeds.items():
    out_deeds[pid] = []
    for r in ds:
        coal = bool(COAL.search(r['owner_after_sale']))
        out_deeds[pid].append({'book_page': r['book_page'], 'date': r['date_as_written'], 'year': year(r),
            'owner': r['owner_after_sale'], 'coal': coal, 'company': company(r['owner_after_sale']) if coal else '',
            'price': r['price_as_written'], 'also': r['same_deed_also_covers']})
        rows.append({'pid': pid, 'seq': r['seq'], 'book_page': r['book_page'], 'date_as_written': r['date_as_written'],
            'date_iso': r['date_iso'], 'owner_after_sale': r['owner_after_sale'], 'price_as_written': r['price_as_written'],
            'coal_company': 'yes' if coal else '', 'same_deed_also_covers': r['same_deed_also_covers'],
            'source': 'Greene County Recorder of Deeds, deed book/page as listed; transcribed by Julian Giordano'})
for f in P['features']:
    p = f['properties']; pid = p['pid']
    ys = [d['year'] for d in out_deeds.get(pid, []) if d['coal'] and d['year']]
    p['first_coal_year'] = min(ys) if ys else ''
    p['company'] = company(p.get('owner', '')) if str(p.get('map_class', '')).endswith('coal') else ''
    if pid in vp: p['n_deeds'] = len(out_deeds.get(pid, []))
open(os.path.join(root, 'data.js'), 'w').write('const PARCELS=' + json.dumps(P, separators=(',', ':')) + ';\nconst DEEDS=' + json.dumps(out_deeds, separators=(',', ':')) + ';\n')
# public downloads
json.dump(P, open(os.path.join(root, 'data', 'oak_forest_parcels.geojson'), 'w'))
with open(os.path.join(root, 'data', 'oak_forest_village_deeds.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
v = [f['properties'] for f in P['features'] if str(f['properties'].get('in_village')) == '1']
from collections import Counter
print('village', len(v), 'first coal years', sorted(Counter(p['first_coal_year'] for p in v).items(), key=lambda x: str(x[0])))
