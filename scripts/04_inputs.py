"""Build every input layer of the posterior on one 0.02° grid (protocol v1.0, section 1-3).

Outputs: out/inputs.npz (grids) and the map layers out/oi_coverage.geojson, out/oi2018_gaps.geojson.
"""
import json, math
import numpy as np
import shapely
from scipy.spatial import cKDTree
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
from common import DERIVED, OUT, load_js, decode_rle, boxes_union, feature, save_fc
import importlib
arcmod = importlib.import_module('02_arc')

D = 0.02
LON0, LON1, LAT0, LAT1 = 82.0, 106.0, -42.0, -22.0
lons = np.arange(LON0, LON1, D) + D / 2
lats = np.arange(LAT1, LAT0, -D) - D / 2
X, Y = np.meshgrid(lons, lats)
CELL = (D * 111.32 * np.cos(np.radians(Y))) * (D * 110.57)

# Fixed by the protocol (calibrated once, before the freeze, to the reported searched areas)
R_2018_KM = 25.2        # OI 2018: AUV reach from the ship that reproduces 112,000 km2
R_2018_STRONG_KM = 34.4  # OI 2018: reach that reproduces 120,000 km2 ("strong" gaps beyond it)
R_2025_KM = 4.2          # OI 2025-26: band that reproduces ~7,200 km2 for Dec 2025 - Jan 2026


def unit(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1)


def gc_km(chord):
    return 2 * 6371.0 * np.arcsin(np.clip(chord / 2, 0, 1))


def arc_fields(sat, h):
    la = np.arange(-46, -16, 0.005)
    lo = arcmod.arc_points(sat, h, la)
    tree = cKDTree(unit(la, lo))
    chord, idx = tree.query(unit(Y.ravel(), X.ravel()))
    S = arcmod.ecef(np.array(sat['sat_lat']), np.array(sat['sat_lon']), arcmod.GEO_ALT)
    side = np.sign(np.linalg.norm(arcmod.ecef(Y.ravel(), X.ravel(), h) - S, axis=-1) - sat['range_m'])
    seg = gc_km(np.linalg.norm(unit(la[1:], lo[1:]) - unit(la[:-1], lo[:-1]), axis=-1))
    dlat_dkm = np.r_[0.005 / seg, 0.005 / seg[-1]]
    return (gc_km(chord) * side).reshape(X.shape), la[idx].reshape(X.shape), dlat_dkm[idx].reshape(X.shape)


def track_rows(files, t0=None, t1=None):
    rows = []
    for fn in files:
        j = load_js(fn); rows += j['data'][j['vessels'][0]]
    return [r for r in rows if (t0 is None or r[0] >= t0) and (t1 is None or r[0] <= t1)]


def track_points(rows, near):
    pts = []
    for p, q in zip(rows, rows[1:]):
        pa, pb = (p[2], p[1]), (q[2], q[1])
        if not (near.contains(Point(pa)) and near.contains(Point(pb))):
            continue
        n = max(1, int(math.hypot(pb[0] - pa[0], pb[1] - pa[1]) / 0.005))
        for t in np.linspace(0, 1, n + 1):
            pts.append((pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t))
    return np.array(pts)


def dist_to(pts):
    chord, _ = cKDTree(unit(pts[:, 1], pts[:, 0])).query(unit(Y.ravel(), X.ravel()))
    return gc_km(chord).reshape(X.shape)


if __name__ == '__main__':
    sat = json.loads((OUT / 'sat.json').read_text())
    z = {}
    for h, name in ((arcmod.H_ARC, 'h20k'), (0.0, 'h0')):
        d, la, j = arc_fields(sat, h)
        z[f'd_{name}'], z[f'la_{name}'], z[f'j_{name}'] = d.astype(np.float32), la.astype(np.float32), j.astype(np.float32)

    atsb = np.load(OUT / 'atsb_grid.npy')
    a = np.zeros(X.shape, np.uint8)
    r0 = int(round((LAT1 - (-32.6)) / D)); c0 = int(round((85.0 - LON0) / D))
    a[r0:r0 + atsb.shape[0], c0:c0 + atsb.shape[1]] = atsb
    z['atsb'] = a

    slope = decode_rle((DERIVED / 'slope_class_004deg_rle.txt').read_text(), base_val=10).reshape(425, 450)
    assert [int((slope == k).sum()) for k in (0, 1, 2)] == [15353, 4281, 415], 'checksum of the transferred slope grid'
    r = np.floor((-24.0 - Y) / 0.04).astype(int); c = np.floor((X - 85.0) / 0.04).astype(int)
    ok = (r >= 0) & (r < 425) & (c >= 0) & (c < 450)
    s = np.full(X.shape, 9, np.uint8); s[ok] = slope[r[ok], c[ok]]
    z['slope'] = s

    A = load_js('areas3.js')['areas']
    atsb_poly = Polygon(A['ATSB'][2]).buffer(0)
    env18 = Polygon(A['OI2018'][2]).buffer(0)
    oi18 = env18.difference(atsb_poly)
    zone = unary_union([Polygon(A['OI2025A'][2]).buffer(0), Polygon(A['OI2025B'][2]).buffer(0)])
    zb = zone.buffer(0.15)
    z['oi18_env'] = shapely.contains_xy(oi18, X, Y)
    z['oi25_zone'] = shapely.contains_xy(zone, X, Y)
    z['zb'] = shapely.contains_xy(zb, X, Y)
    sc = track_rows(['sc1.js', 'sc2.js', 'sc3.js', 'sc4.js'])
    p18 = track_points(sc, env18.buffer(0.3))
    z['d18'] = dist_to(p18).astype(np.float32)
    rows_b = track_rows(['phase3.js'], '2025-12-30', '2026-01-24'); rows_a = track_rows(['phase2.js'], '2025-03-09', '2025-03-30')
    z['d25b'] = dist_to(track_points(rows_b, zb)).astype(np.float32)
    z['d25a'] = dist_to(track_points(rows_a, zb)).astype(np.float32)
    z['cell_km2'] = CELL.astype(np.float32); z['X'] = X.astype(np.float32); z['Y'] = Y.astype(np.float32)
    np.savez_compressed(OUT / 'inputs.npz', **z)

    env = z['oi18_env']
    print(f"OI 2018 envelope minus ATSB: {CELL[env].sum():,.0f} km2; within {R_2018_KM} km of track: {CELL[env & (z['d18'] <= R_2018_KM)].sum():,.0f} km2 (reported 112,000)")
    cb = z['zb'] & (z['d25b'] <= R_2025_KM); ca = z['zb'] & (z['d25a'] <= R_2025_KM)
    print(f"OI 2025-26: Dec-Jan {CELL[cb].sum():,.0f} km2 (reported ~7,200); March {CELL[ca].sum():,.0f} km2; zone {CELL[z['oi25_zone']].sum():,.0f} km2; zone left {CELL[z['oi25_zone'] & ~(ca | cb)].sum():,.0f} km2 (official remaining 7,429)")

    # map layers
    to_poly = lambda m: boxes_union(m, LON0, LAT1, D).simplify(0.008, preserve_topology=True)
    tr = lambda rows: LineString([(r[2], r[1]) for r in rows if zb.contains(Point(r[2], r[1]))]).simplify(0.003)
    save_fc(OUT / 'oi_coverage.geojson', [
        feature(oi18.simplify(0.01), {'layer': 'oi2018'}),
        feature(zone.simplify(0.005), {'layer': 'oi2025zone'}),
        feature(to_poly(ca), {'layer': 'oi2025p1'}), feature(to_poly(cb), {'layer': 'oi2025p2'}),
        feature(tr(rows_a), {'layer': 'track2025p1'}), feature(tr(rows_b), {'layer': 'track2025p2'})])
    gap = env & (z['d18'] > R_2018_KM); strong = env & (z['d18'] > R_2018_STRONG_KM)
    print(f'OI 2018 likely gaps {CELL[gap].sum():,.0f} km2, strong {CELL[strong].sum():,.0f} km2')
    save_fc(OUT / 'oi2018_gaps.geojson', [feature(boxes_union(gap & ~strong, LON0, LAT1, D).simplify(0.01), {'layer': 'gap2018'}),
                                         feature(boxes_union(strong, LON0, LAT1, D).simplify(0.01), {'layer': 'gap2018strong'})])
