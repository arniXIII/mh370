"""Posterior per the pre-registered protocol v1.0: primary run and sensitivity runs S1-S12.

Outputs: out/results.json (region masses per run), out/posterior_runs.geojson.json (50/80/95% areas per run, for the map),
out/post_primary.npy, out/prior_primary.npy.
Also an exploratory addendum (after v1.0 results): the highest-density 10,000 km2 per run and the cells that are in it in >= 10 of 14 runs.
"""
import json, math
import numpy as np
from common import DERIVED, OUT, boxes_union, feature

z = dict(np.load(OUT / 'inputs.npz'))
A = z['cell_km2'].astype(float)
NM = 1.852
A1 = json.loads((DERIVED / 'dstg_fig10_3_digitized.json').read_text())

# ---------- along-arc priors (density per degree of latitude of the 7th-arc crossing) ----------
def f_A1(lat): return np.interp(lat, A1['lat'], np.array(A1['p']) / 0.25, left=0, right=0)
def f_A2(lat): return np.exp(-0.5 * ((lat + 34.23) / 0.5) ** 2) / (0.5 * np.sqrt(2 * np.pi))
def f_A3(lat): return 0.5 * ((lat >= -36) & (lat <= -33)) / 3.0 + 0.5 * ((lat > -33) & (lat <= -28)) / 5.0
ALONG = {'A1': f_A1, 'A2': f_A2, 'A3': f_A3}


def cross(d, w1):
    """Cross-arc density per km: w1 x uniform within 25 NM (C1) + (1-w1) x uniform within 100 NM (C2)."""
    return w1 * (np.abs(d) <= 25 * NM) / (50 * NM) + (1 - w1) * (np.abs(d) <= 100 * NM) / (200 * NM)


def prior(along=('A1', 'A2', 'A3'), w1=0.8, arc='h20k'):
    lat, d, j = z['la_' + arc], z['d_' + arc], z['j_' + arc]
    fa = sum(ALONG[k](lat) for k in along) / len(along)
    dom = (lat >= -40) & (lat <= -24) & (np.abs(d) <= 100 * NM)
    p = fa * j * cross(d, w1) * A * dom
    return p / p.sum()


# ---------- detection probabilities (flat, moderate, steep) ----------
PD = {'deeptow': (0.90, 0.75, 0.50), 'sas': (0.90, 0.80, 0.60), 'auv': (0.90, 0.90, 0.85),
      'oi18': (0.90, 0.85, 0.75), 'oi25': (0.90, 0.85, 0.75)}
R18, R18S, R25 = 25.2, 34.4, 4.2


def miss_prob(pd_scale=None, pd_up=False, gaps='likely', buf25=R25, march=True, fillin=True, outside=True, jan_outside=True):
    cls = z['slope'].astype(int); cls = np.where(cls == 9, 1, cls)      # no bathymetry -> moderate (change log)
    def d(key):
        v = np.array(PD[key])[cls]
        if pd_scale: v = v * pd_scale
        if pd_up: v = np.minimum(0.98, v + 0.08)
        return v
    m = np.ones_like(A); bits = z['atsb']
    m *= np.where(bits & 1, 1 - d('deeptow'), 1)
    m *= np.where(bits & 2, 1 - d('auv'), 1)
    m *= np.where(bits & 4, 1 - d('sas'), 1)
    m *= np.where(bits & 8, 1 - d('sas'), 1)
    env = z['oi18_env']
    cov18 = env & (z['d18'] <= R18) if gaps == 'likely' else env & (z['d18'] <= R18S) if gaps == 'strong' else env
    m *= np.where(cov18, 1 - d('oi18'), 1)
    # 2025-26: v1.0 counted only positions inside the proposed zone; v1.1 added the Feb fill-in; v1.2 counts all work positions
    zb = z['zb']
    cov25 = zb & (z['d25b'] <= buf25)
    if march: cov25 = cov25 | (zb & (z['d25a'] <= buf25))
    if outside and jan_outside: cov25 = cov25 | (~zb & (z['d25bx'] <= buf25))
    if outside and march: cov25 = cov25 | (~zb & (z['d25ax'] <= buf25))
    if fillin: cov25 = cov25 | (z['d25f'] <= buf25)
    m *= np.where(cov25, 1 - d('oi25'), 1)
    return m, cov18, cov25


def regions(cov18, cov25, d):
    searched = (z['atsb'] > 0) | cov18 | cov25
    r1 = z['oi25_zone'] & ~cov25
    r2 = z['oi18_env'] & ~cov18
    near = np.abs(d) <= 25 * NM
    return {'R1': r1, 'R2': r2, 'R3': near & ~searched & ~r1 & ~r2,
            'R4': ~near & (np.abs(d) <= 100 * NM) & ~searched & ~r1 & ~r2, 'R5': searched & ~r1 & ~r2}


REGION_NAMES = {'R1': 'OI remaining contract area', 'R2': 'OI 2018 likely gaps', 'R3': 'Never searched, within 25 NM',
                'R4': 'Never searched, 25-100 NM', 'R5': 'Searched cells (imperfect detection)'}

RUNS = [
    ('P', 'Primary', {}),
    ('S1', 'DSTG prior only (A1)', {'along': ('A1',)}), ('S2', 'UGIB prior only (A2)', {'along': ('A2',)}),
    ('S3', 'Drift prior only (A3)', {'along': ('A3',)}),
    ('S4', 'No piloted glide (C1 only)', {'w1': 1.0}), ('S5', 'Glide weight 50%', {'w1': 0.5}),
    ('S6', 'Detection x0.8', {'pd_scale': 0.8}), ('S7', 'Detection +0.08', {'pd_up': True}),
    ('S8', '2018 gaps treated as searched', {'gaps': 'none'}), ('S9', 'Only strong 2018 gaps', {'gaps': 'strong'}),
    ('S10a', '2025 band 3.0 km', {'buf25': 3.0}), ('S10b', '2025 band 6.0 km', {'buf25': 6.0}),
    ('S11', 'March 2025 excluded', {'march': False}), ('S12', 'Arc at sea level', {'arc': 'h0'}),
    ('S13', '2025-26 coverage as in v1.0', {'fillin': False, 'outside': False}),
    ('S14', 'Dec-Jan work outside zone ignored', {'jan_outside': False}),
]


def hpd_features(post, run_id):
    P = post.reshape(500, 2, 600, 2).sum((1, 3)); AA = A.reshape(500, 2, 600, 2).sum((1, 3)); Dn = P / AA
    o = np.argsort(-Dn.ravel()); cum = np.cumsum(P.ravel()[o]); feats = []; areas = {}
    for q, name in ((0.95, 'hpd95'), (0.8, 'hpd80'), (0.5, 'hpd50')):
        k = np.searchsorted(cum, q); mm = np.zeros(Dn.shape, bool); mm.ravel()[o[:k + 1]] = True
        areas[name] = float(AA[mm].sum())
        feats.append(feature(boxes_union(mm, 82.0, -22.0, 0.04).simplify(0.03), {'layer': name, 'run': run_id}))
    return feats, areas


TOP_KM2 = 10000      # exploratory addendum (not in protocol v1.0): size of the "most likely area"
CORE_SHARE = 0.7     # a cell is in the robust core if it is in the top area in at least 70% of the runs (10 of 14 in v1.0)


def top_area(post):
    """Highest-density 0.04-degree cells adding up to TOP_KM2 (exploratory addendum)."""
    P = post.reshape(500, 2, 600, 2).sum((1, 3)); AA = A.reshape(500, 2, 600, 2).sum((1, 3))
    Dn = np.where(AA > 0, P / np.maximum(AA, 1e-9), 0)
    o = np.argsort(-Dn.ravel()); k = np.searchsorted(np.cumsum(AA.ravel()[o]), TOP_KM2)
    mm = np.zeros(Dn.shape, bool); mm.ravel()[o[:k + 1]] = True
    return mm, P, AA


def run(along=('A1', 'A2', 'A3'), w1=0.8, arc='h20k', **kw):
    p0 = prior(along, w1, arc)
    m, cov18, cov25 = miss_prob(**kw)
    post = p0 * m; pf = post.sum(); post /= pf
    R = regions(cov18, cov25, z['d_' + arc])
    mass = {k: float(post[v].sum()) for k, v in R.items()}
    pmass = {k: float(p0[v].sum()) for k, v in R.items()}
    area = {k: float(A[v].sum()) for k, v in R.items()}
    dens = post / A; other = ~R['R1'] & (post > 0)
    o = np.argsort(-dens[other]); k = np.searchsorted(np.cumsum(A[other][o]), area['R1'])
    return {'p_all_missed': float(pf), 'mass': mass, 'prior_mass': pmass, 'area_km2': area,
            'R1_post_over_prior': mass['R1'] / pmass['R1'] if pmass['R1'] > 0 else None,
            'best_equal_area_elsewhere': float(post[other][o][:k + 1].sum())}, post, p0


if __name__ == '__main__':
    results, feats = [], []
    count = None
    for rid, label, kw in RUNS:
        r, post, p0 = run(**kw)
        f, areas = hpd_features(post, rid); feats += f
        r.update({'id': rid, 'label': label, 'hpd_km2': areas}); results.append(r)
        mm, P4, AA = top_area(post)
        r['top_area'] = {'area_km2': float(AA[mm].sum()), 'mass': float(P4[mm].sum())}
        feats.append(feature(boxes_union(mm, 82.0, -22.0, 0.04).simplify(0.01), {'layer': 'top', 'run': rid}))
        count = mm.astype(int) if count is None else count + mm
        if rid == 'P':
            P4_primary = P4
            np.save(OUT / 'post_primary.npy', post.astype(np.float32)); np.save(OUT / 'prior_primary.npy', p0.astype(np.float32))
        m = r['mass']
        print(f"{rid:<5} {label:<30} R1 {m['R1']:.3f} R2 {m['R2']:.3f} R3 {m['R3']:.3f} R4 {m['R4']:.3f} R5 {m['R5']:.3f} "
              f"best-equal-area {r['best_equal_area_elsewhere']:.3f} P(all missed) {r['p_all_missed']:.3f}")
    core_min = math.ceil(CORE_SHARE * len(RUNS)); core = count >= core_min
    from scipy import ndimage
    lab, n = ndimage.label(core, structure=np.ones((3, 3)))
    lat4 = -22 - 0.04 * (np.arange(500) + 0.5); lon4 = 82 + 0.04 * (np.arange(600) + 0.5)
    blocks = []
    for i in range(1, n + 1):
        c = lab == i; ii, jj = np.nonzero(c)
        blocks.append({'area_km2': float(AA[c].sum()), 'mass_primary': float(P4_primary[c].sum()),
                       'lat': float(lat4[ii].mean()), 'lon': float(lon4[jj].mean())})
    blocks.sort(key=lambda b: -b['mass_primary'])
    core_info = {'top_km2': TOP_KM2, 'min_runs': core_min, 'n_runs': len(RUNS),
                 'area_km2': float(AA[core].sum()), 'mass_primary': float(P4_primary[core].sum()), 'blocks': blocks[:5]}
    feats.append(feature(boxes_union(core, 82.0, -22.0, 0.04).simplify(0.01), {'layer': 'core', 'run': 'all'}))
    print(f"robust core: {core_info['area_km2']:.0f} km2, primary mass {core_info['mass_primary']:.3f}; main block {blocks[0]}")
    (OUT / 'results.json').write_text(json.dumps({'regions': REGION_NAMES, 'runs': results, 'core': core_info}, indent=1))
    (OUT / 'posterior_runs.geojson').write_text(json.dumps({'type': 'FeatureCollection', 'features': feats}, separators=(',', ':')))
