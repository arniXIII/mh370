// Open the figure image URL directly in the browser, then run this in the developer console:
// https://media.springernature.com/full/springer-static/image/chp%3A10.1007%2F978-981-10-0379-0_10/MediaObjects/371511_1_En_10_Fig3_HTML.gif
// Fig. 10.3 of Davey et al. (2016). Bottom panel = pdf with BFO measurements. Axes found by inspection:
// x = -50 deg at pixel column 34, +50 deg at column 537; bottom-panel baseline at row 416, panel top at row 250.
(() => {
  const img = document.querySelector('img'), W = img.naturalWidth, H = img.naturalHeight;
  const c = new OffscreenCanvas(W, H), x = c.getContext('2d'); x.drawImage(img, 0, 0);
  const d = x.getImageData(0, 0, W, H).data;
  const blue = (i, j) => { const k = (j * W + i) * 4; return d[k + 2] > 150 && d[k + 2] - d[k] > 60; };
  const out = [];
  for (let i = 35; i < 537; i++) {
    let top = null; for (let j = 251; j <= 417; j++) if (blue(i, j)) { top = j; break; }
    const lat = -50 + (i - 34) * 100 / 503;
    if (lat >= -45 && lat <= -20) out.push([+lat.toFixed(2), top === null ? null : 416 - top]);
  }
  console.log(JSON.stringify(out));
})();
