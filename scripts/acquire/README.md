# How the derived input files were acquired

Three inputs could not be downloaded as plain files, so they were extracted in a web browser from public web services and transferred as compact run-length strings. The scripts in this folder are the exact JavaScript that was run in the browser's developer console on the page named in each file. The resulting strings are stored in `data/derived/` and checked by checksums in `scripts/03_atsb_coverage.py` and `scripts/04_inputs.py`.

| Output file | Script | Page to run it on |
| --- | --- | --- |
| `data/derived/atsb_phase2_mask_rle.txt` | `ga_sonar_coverage.js` | any page on `https://warehouse.ausseabed.gov.au` (same-origin requests) |
| `data/derived/slope_class_004deg_rle.txt` | `ga_slope_classes.js` | same |
| `data/derived/dstg_fig10_3_digitized.json` | `dstg_digitize.js` | the image URL `https://media.springernature.com/full/springer-static/image/chp%3A10.1007%2F978-981-10-0379-0_10/MediaObjects/371511_1_En_10_Fig3_HTML.gif` |

## Run-length format

`v<run>.v<run>...` where `v` is one hexadecimal (coverage) or decimal (slope) digit and `<run>` is the run length in base 36. Grids are stored row by row from north to south.

- Coverage: 575 × 380 cells of 0.02°, west edge 85.0°E, north edge 32.6°S. Bits: 1 Fugro deep tow, 2 Fugro AUV, 4 Dong Hai Jiu 101 SAS, 8 GO Phoenix SAS. A cell is set when at least 2 of its four 0.01° sub-pixels are non-transparent in the WMS rendering.
- Slope: 450 × 425 cells of 0.04°, west edge 85.0°E, north edge 24.0°S. 0 flat (<5°), 1 moderate (5–15°), 2 steep (>15°), 9 no data.

## Known limitations

- The WMS rendering of the GO Phoenix and Dong Hai Jiu 101 layers draws the outline of their survey extents; `scripts/03_atsb_coverage.py` removes those lines.
- Depth is decoded from the colour ramp of the `_OV` bathymetry layer (the server does not offer WCS or custom styles), so depth precision is about 10–25 m and slope is computed over an 800 m baseline after 3×3 smoothing.
