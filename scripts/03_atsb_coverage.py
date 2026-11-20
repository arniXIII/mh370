"""ATSB 2014-17 measured coverage from Geoscience Australia's Phase 2 sonar mosaics.

Input: data/derived/atsb_phase2_mask_rle.txt — a 0.02° grid (575 x 380 cells, west edge 85.0°E,
north edge 32.6°S, rows north->south). Each cell holds a bit mask: 1 Fugro deep tow, 2 Fugro AUV,
4 Dong Hai Jiu 101 SAS, 8 GO Phoenix SAS. See scripts/acquire/README.md for how it was made.

The WMS rendering draws the outlines of the DHJ and GO Phoenix survey extents; those 1-2 cell lines
are removed here. Output: out/atsb_grid.npy and out/atsb_coverage.geojson.
"""
import numpy as np
from shapely.geometry import Polygon, Point
from shapely.prepared import prep
from shapely.ops import unary_union
from common import DERIVED, OUT, decode_rle, boxes_union, feature, save_fc

W0, N0, D, NX, NY = 85.0, -32.6, 0.02, 575, 380

# Survey-extent outlines from the AusSeabed WFS layers *_DHJ__SAS__5m_2018_L0_Coverage and *_GoPhoenix__SAS__5m_2018_L0_Coverage
DHJ = [[[89.5167,-37.3494],[89.5199,-37.3494],[89.5201,-37.3501],[89.538,-37.8845],[89.3268,-37.889],[89.0816,-37.8936],[88.8382,-37.8976],[88.692,-37.8996],[88.68,-37.3643],[89.1066,-37.3575],[89.5167,-37.3494]],
       [[92.1379,-36.1667],[92.1385,-36.1669],[92.1388,-36.17],[92.1591,-36.4802],[92.1863,-36.8844],[92.2391,-37.6485],[91.9383,-37.6616],[91.6042,-37.6752],[91.2861,-37.6872],[90.9556,-37.6987],[90.6287,-37.7093],[90.3063,-37.7188],[89.9862,-37.7273],[89.6932,-37.7343],[89.6659,-36.9686],[89.6413,-36.248],[89.9438,-36.241],[90.2528,-36.233],[90.5697,-36.2239],[90.8745,-36.2144],[91.1867,-36.2039],[91.5178,-36.1918],[91.8249,-36.1798],[92.1379,-36.1667]],
       [[92.7692,-35.1798],[92.7698,-35.1799],[92.7699,-35.1803],[92.8111,-35.7541],[92.4326,-35.772],[92.0764,-35.7875],[92.0403,-35.2125],[92.402,-35.1969],[92.7692,-35.1798]],
       [[95.3452,-33.0372],[95.3477,-33.0372],[95.3479,-33.0388],[95.3754,-33.3266],[95.3757,-33.3331],[94.9996,-33.3579],[94.9726,-33.0618],[95.3452,-33.0372]]]
GOPHOENIX = [[[92.71456679,-32.71210312],[95.85067497,-32.71210312],[95.85067497,-35.28258753],[92.71456679,-35.28258753],[92.71456679,-32.71210312]]]


def strip_outline(g, bit, rings, buf=0.025):
    zone = prep(unary_union([Polygon(r).exterior.buffer(buf) for r in rings]))
    ys, xs = np.nonzero((g >> bit) & 1)
    n = 0
    for y, x in zip(ys, xs):
        if zone.contains(Point(W0 + (x + .5) * D, N0 - (y + .5) * D)):
            g[y, x] &= ~np.uint8(1 << bit); n += 1
    return n


if __name__ == '__main__':
    g = decode_rle((DERIVED / 'atsb_phase2_mask_rle.txt').read_text()).reshape(NY, NX)
    assert (g > 0).sum() == 32739, 'checksum of the transferred mask'
    print('removed outline cells: DHJ', strip_outline(g, 2, DHJ), 'GO Phoenix', strip_outline(g, 3, GOPHOENIX))
    np.save(OUT / 'atsb_grid.npy', g)
    lat = N0 - (np.arange(NY) + 0.5) * D
    cell = (D * 111.32 * np.cos(np.radians(lat)))[:, None] * (D * 110.57)
    feats = []
    for b, k in enumerate(['deeptow', 'auv', 'dhj', 'gophoenix']):
        m = ((g >> b) & 1).astype(bool)
        print(f'{k}: {(cell * m).sum():,.0f} km2')
        feats.append(feature(boxes_union(m, W0, N0, D).simplify(0.008, preserve_topology=True), {'layer': k}))
    print(f'union: {(cell * (g > 0)).sum():,.0f} km2 (official figure about 120,000 km2)')
    save_fc(OUT / 'atsb_coverage.geojson', feats)
