"""Shared paths and helpers."""
import json
from pathlib import Path
import numpy as np
import shapely

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DERIVED = DATA / 'derived'
CAPTION = DATA / 'caption'
OUT = ROOT / 'out'
OUT.mkdir(exist_ok=True)


def load_js(name):
    """Parse a CAPTION data file of the form `parse({...})` / `parseAreas({...})`."""
    s = (CAPTION / name).read_text()
    return json.JSONDecoder().raw_decode(s[s.index('(') + 1:])[0]


def km2(geom):
    """Approximate area in km² of a lon/lat geometry (local equirectangular per vertex)."""
    def f(c):
        return np.c_[np.radians(c[:, 0]) * 6371 * np.cos(np.radians(c[:, 1])), np.radians(c[:, 1]) * 6371]
    return shapely.transform(geom, f).area


def rnd(o, nd=3):
    if isinstance(o, float):
        return round(o, nd)
    if isinstance(o, (list, tuple)):
        return [rnd(i, nd) for i in o]
    return o


def feature(geom, props):
    m = shapely.geometry.mapping(geom)
    return {"type": "Feature", "properties": props, "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}}


def save_fc(path, feats):
    Path(path).write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(',', ':')))


def decode_rle(text, base_val=16):
    """Decode 'v<run36>.v<run36>...' run-length strings produced by the browser acquisition scripts."""
    vals = []
    for tok in text.strip().split('.'):
        vals.append((int(tok[0], base_val), int(tok[1:], 36)))
    return np.concatenate([np.full(n, v, np.uint8) for v, n in vals])


def boxes_union(mask, lon0, lat_top, d):
    """Vectorize a boolean grid (rows north->south) into a union of cell rectangles."""
    from shapely.geometry import box
    from shapely.ops import unary_union
    out = []
    for i in range(mask.shape[0]):
        row = mask[i]; j = 0
        while j < len(row):
            if row[j]:
                s = j
                while j < len(row) and row[j]:
                    j += 1
                out.append(box(lon0 + s * d, lat_top - (i + 1) * d, lon0 + j * d, lat_top - i * d))
            else:
                j += 1
    return unary_union(out)
