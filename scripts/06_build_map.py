"""Assemble index.html (the interactive map) from map/template.html and the generated layers."""
import json
from common import ROOT, DATA, OUT

if __name__ == '__main__':
    res = json.loads((OUT / 'results.json').read_text())
    slim = {'regions': res['regions'], 'runs': [{k: r[k] for k in ('id', 'label', 'mass', 'hpd_km2', 'best_equal_area_elsewhere', 'p_all_missed', 'top_area')} for r in res['runs']], 'core': res['core']}
    t = (ROOT / 'map' / 'template.html').read_text()
    for key, val in {
        '__LAND__': (DATA / 'land_clip.json').read_text(),
        '__GEO__': (OUT / 'geo.json').read_text(),
        '__PTS__': json.dumps(json.loads((DATA / 'points.json').read_text()), ensure_ascii=False, separators=(',', ':')),
        '__COV__': (OUT / 'atsb_coverage.geojson').read_text(),
        '__OI__': (OUT / 'oi_coverage.geojson').read_text(),
        '__GAP__': (OUT / 'oi2018_gaps.geojson').read_text(),
        '__HPD__': (OUT / 'posterior_runs.geojson').read_text(),
        '__RES__': json.dumps(slim, separators=(',', ':')),
    }.items():
        assert key in t, key
        t = t.replace(key, val)
    (ROOT / 'index.html').write_text(t)
    print(f'index.html: {len(t) / 1e6:.2f} MB')
