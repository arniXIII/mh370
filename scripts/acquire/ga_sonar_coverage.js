// Run in the developer console on any page of https://warehouse.ausseabed.gov.au
// Produces the run-length string stored in data/derived/atsb_phase2_mask_rle.txt
(async () => {
  const B = [85.0, -40.2, 96.5, -32.6], W = 1150, H = 760;             // 0.01 deg pixels
  const layers = {
    deeptow: 'MH370_Phase_2_Sonar_Imagery_Backscatter_Inverse_Deep_Tow__SSS__5m_2018',
    auv: 'MH370_Phase_2_Sonar_Imagery_Backscatter_Inverse_Autonomous_Underwater_Vehicle__SSS__5m_2018',
    dhj: 'MH370_Phase_2_Sonar_Imagery_Backscatter_Wide_DHJ__SAS__5m_2018',
    gophoenix: 'MH370_Phase_2_Sonar_Imagery_Backscatter_Wide_GoPhoenix__SAS__5m_2018',
  };
  const keys = ['deeptow', 'auv', 'dhj', 'gophoenix'];
  const masks = [];
  for (const k of keys) {
    const u = `/geoserver/ausseabed/wms?service=WMS&version=1.1.1&request=GetMap&layers=ausseabed:${layers[k]}&styles=&srs=EPSG:4326&bbox=${B.join(',')}&width=${W}&height=${H}&format=image/png&transparent=true`;
    const bm = await createImageBitmap(await (await fetch(u)).blob());
    const c = new OffscreenCanvas(W, H), x = c.getContext('2d'); x.drawImage(bm, 0, 0);
    const d = x.getImageData(0, 0, W, H).data, m = new Uint8Array(W * H);
    for (let i = 0; i < W * H; i++) m[i] = d[i * 4 + 3] > 0 ? 1 : 0;
    masks.push(m);
  }
  // aggregate 2x2 -> 0.02 deg; a layer bit is set when >= 2 of 4 sub-pixels are covered
  const w = W / 2, h = H / 2, g = new Uint8Array(w * h);
  masks.forEach((m, t) => {
    const cnt = new Uint8Array(w * h);
    for (let y = 0; y < H; y++) for (let xx = 0; xx < W; xx++) if (m[y * W + xx]) cnt[(y >> 1) * w + (xx >> 1)]++;
    for (let j = 0; j < w * h; j++) if (cnt[j] >= 2) g[j] |= 1 << t;
  });
  const out = []; let cur = g[0], run = 0;
  for (let i = 0; i < g.length; i++) { if (g[i] === cur) run++; else { out.push(cur.toString(16) + run.toString(36)); cur = g[i]; run = 1; } }
  out.push(cur.toString(16) + run.toString(36));
  console.log(out.join('.'));
})();
