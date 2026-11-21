"""7th arc: fit the satellite sub-point and slant range to the CAPTION arc (20,000 ft), then draw the arc.

Output: out/sat.json, out/geo.json (arc polyline and the UWA 28-33°S segment).
"""
import json
import numpy as np
from common import OUT, load_js

A_WGS = 6378137.0; F_WGS = 1 / 298.257223563; E2 = F_WGS * (2 - F_WGS)
GEO_ALT = 35786000.0
H_ARC = 6096.0          # 20,000 ft


def ecef(lat, lon, h=0.0):
    la, lo = np.radians(lat), np.radians(lon)
    n = A_WGS / np.sqrt(1 - E2 * np.sin(la) ** 2)
    return np.stack([(n + h) * np.cos(la) * np.cos(lo), (n + h) * np.cos(la) * np.sin(lo), (n * (1 - E2) + h) * np.sin(la)], -1)


def fit():
    arc = np.array([(la, lo) for lo, la in load_js('areas3.js')['areas']['stharc'][2] if -40.5 < la < -20])
    P = ecef(arc[:, 0], arc[:, 1], H_ARC)
    best = None
    for slat in np.arange(0.30, 0.90, 0.01):
        for slon in np.arange(64.35, 64.60, 0.01):
            r = np.linalg.norm(P - ecef(np.array(slat), np.array(slon), GEO_ALT), axis=1)
            if best is None or r.std() < best[0]:
                best = (r.std(), slat, slon, r.mean())
    return {'sat_lat': round(float(best[1]), 2), 'sat_lon': round(float(best[2]), 2), 'range_m': float(best[3]),
            'fit_sd_m': float(best[0]), 'altitude_m': H_ARC}


def arc_points(sat, h, la):
    S = ecef(np.array(sat['sat_lat']), np.array(sat['sat_lon']), GEO_ALT)
    lo_lo, lo_hi = np.full_like(la, 70.0), np.full_like(la, 125.0)
    for _ in range(50):
        m = (lo_lo + lo_hi) / 2
        r = np.linalg.norm(ecef(la, m, h) - S, axis=-1) - sat['range_m']
        lo_lo = np.where(r < 0, m, lo_lo); lo_hi = np.where(r < 0, lo_hi, m)
    return (lo_lo + lo_hi) / 2


if __name__ == '__main__':
    sat = fit()
    (OUT / 'sat.json').write_text(json.dumps(sat, indent=1))
    print('satellite fit', sat)
    la = np.arange(-8, -40.501, -0.1); lo = arc_points(sat, H_ARC, la)
    lu = np.arange(-28, -33.001, -0.1); lou = arc_points(sat, H_ARC, lu)
    geo = {'arc': [[round(float(x), 3), round(float(y), 3)] for x, y in zip(lo, la)],
           'uwa': [[round(float(x), 3), round(float(y), 3)] for x, y in zip(lou, lu)]}
    (OUT / 'geo.json').write_text(json.dumps(geo, separators=(',', ':')))
    for name, p in (('UGIB LEP', (-34.2342, 93.7875)), ('Godfrey WSPR', (-29.128, 99.934))):
        lon_arc = arc_points(sat, H_ARC, np.array([p[0]]))[0]
        print(f'{name}: arc longitude at its latitude {lon_arc:.3f} (point {p[1]})')
