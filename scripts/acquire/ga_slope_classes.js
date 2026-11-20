// Run in the developer console on any page of https://warehouse.ausseabed.gov.au
// Produces the run-length string stored in data/derived/slope_class_004deg_rle.txt
// Depth is decoded from the colour ramp of the *_Bathymetry__150m_2017_OV layer (WCS and SLD_BODY are not available).
(async () => {
  const L = 'ausseabed:Southern_Indian_Ocean__MH370__Bathymetry__150m_2017';
  const leg = await (await fetch(`/geoserver/ausseabed/wms?service=WMS&version=1.1.1&request=GetLegendGraphic&format=application/json&layer=${L}`)).json();
  const ramp = leg.Legend.find(l => l.layerName.endsWith('_OV')).rules[0].symbolizers[0].Raster.colormap.entries
    .filter(e => e.opacity !== '0.0').map(e => [+e.quantity, e.color]);
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const samples = [];
  for (let q = -6500; q <= -1; q++) {
    let k = 0; while (k < ramp.length - 2 && ramp[k + 1][0] < q) k++;
    const [q0, c0] = [ramp[k][0], hex(ramp[k][1])], [q1, c1] = [ramp[k + 1][0], hex(ramp[k + 1][1])];
    const t = Math.min(1, Math.max(0, (q - q0) / (q1 - q0)));
    samples.push([q, c0.map((v, i) => Math.round(v + (c1[i] - v) * t))]);
  }
  const lut = new Map(); for (const [q, c] of samples) { const key = (c[0] << 16) | (c[1] << 8) | c[2]; if (!lut.has(key)) lut.set(key, []); lut.get(key).push(q); }
  const cache = new Map();
  const depthOf = (r, g, b) => {
    const key = (r << 16) | (g << 8) | b;
    if (lut.has(key)) { const v = lut.get(key); return v.reduce((a, c) => a + c, 0) / v.length; }
    if (cache.has(key)) return cache.get(key);
    let best = 1e9, bq = null; for (const [q, c] of samples) { const d = (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2; if (d < best) { best = d; bq = q; } }
    cache.set(key, bq); return bq;
  };
  // 1-degree tiles touching the searched areas (computed from the CAPTION polygons)
  const tiles = [[85,-41],[85,-40],[85,-39],[86,-41],[86,-40],[86,-39],[87,-40],[87,-39],[87,-38],[88,-40],[88,-39],[88,-38],[88,-37],[89,-39],[89,-38],[89,-37],[90,-39],[90,-38],[90,-37],[90,-36],[91,-38],[91,-37],[91,-36],[91,-35],[92,-37],[92,-36],[92,-35],[92,-34],[93,-37],[93,-36],[93,-35],[93,-34],[94,-36],[94,-35],[94,-34],[94,-33],[95,-35],[95,-34],[95,-33],[95,-32],[96,-34],[96,-33],[96,-32],[96,-31],[97,-33],[97,-32],[97,-31],[97,-30],[98,-31],[98,-30],[98,-29],[99,-30],[99,-29],[99,-28],[99,-27],[100,-29],[100,-28],[100,-27],[100,-26],[101,-28],[101,-27],[101,-26],[101,-25],[102,-26],[102,-25]];
  const N = 250, W = 900, H = 850, G = new Uint8Array(W * H).fill(9);    // 0.02 deg classes, 85-103E, 24-41S
  for (const [lo, la] of tiles) {
    const u = `/geoserver/ausseabed/wms?service=WMS&version=1.1.1&request=GetMap&layers=${L}_OV&styles=&srs=EPSG:4326&bbox=${lo},${la},${lo + 1},${la + 1}&width=${N}&height=${N}&format=image/png&transparent=true`;
    const bm = await createImageBitmap(await (await fetch(u)).blob());
    const c = new OffscreenCanvas(N, N), x = c.getContext('2d'); x.drawImage(bm, 0, 0);
    const d = x.getImageData(0, 0, N, N).data;
    const Dp = new Float32Array(N * N).fill(NaN);
    for (let i = 0; i < N * N; i++) if (d[i * 4 + 3] > 100) Dp[i] = depthOf(d[i * 4], d[i * 4 + 1], d[i * 4 + 2]);
    const S = new Float32Array(N * N).fill(NaN);                        // 3x3 smoothing
    for (let y = 1; y < N - 1; y++) for (let xx = 1; xx < N - 1; xx++) { let s = 0, n = 0; for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) { const v = Dp[(y + a) * N + xx + b]; if (!isNaN(v)) { s += v; n++; } } if (n >= 6) S[y * N + xx] = s / n; }
    const lat = la + 0.5, dx = 0.004 * 111320 * Math.cos(lat * Math.PI / 180), dy = 0.004 * 110574;
    const SL = new Float32Array(N * N).fill(NaN);                       // slope over a 4-pixel (~800 m) baseline
    for (let y = 2; y < N - 2; y++) for (let xx = 2; xx < N - 2; xx++) { const zx = (S[y * N + xx + 2] - S[y * N + xx - 2]) / (4 * dx), zy = (S[(y + 2) * N + xx] - S[(y - 2) * N + xx]) / (4 * dy); if (!isNaN(zx) && !isNaN(zy)) SL[y * N + xx] = Math.atan(Math.hypot(zx, zy)) * 180 / Math.PI; }
    const x0 = (lo - 85) * 50, y0 = (-24 - (la + 1)) * 50;
    for (let cy = 0; cy < 50; cy++) for (let cx = 0; cx < 50; cx++) {
      const v = []; for (let a = 0; a < 5; a++) for (let b = 0; b < 5; b++) { const s = SL[(cy * 5 + a) * N + cx * 5 + b]; if (!isNaN(s)) v.push(s); }
      let code = 9; if (v.length >= 8) { v.sort((p, q) => p - q); const p90 = v[Math.floor(0.9 * (v.length - 1))]; code = p90 < 5 ? 0 : p90 < 15 ? 1 : 2; }
      G[(y0 + cy) * W + x0 + cx] = code;
    }
  }
  // most common class of each 2x2 block -> 0.04 deg (ties go to the steeper class)
  const w = 450, h = 425, C = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const v = [G[2 * y * W + 2 * x], G[2 * y * W + 2 * x + 1], G[(2 * y + 1) * W + 2 * x], G[(2 * y + 1) * W + 2 * x + 1]].filter(a => a !== 9);
    if (!v.length) { C[y * w + x] = 9; continue; }
    const c = [0, 0, 0]; v.forEach(a => c[a]++); let best = 0; for (let k = 1; k < 3; k++) if (c[k] >= c[best]) best = k; C[y * w + x] = best;
  }
  const out = []; let cur = C[0], run = 0;
  for (let i = 0; i < C.length; i++) { if (C[i] === cur) run++; else { out.push(cur + run.toString(36)); cur = C[i]; run = 1; } }
  out.push(cur + run.toString(36));
  console.log(out.join('.'));
})();
