# MH370 residual-probability analysis — pre-registered protocol

Version 1.0, frozen 20 November 2026 · [Results](results.md) · [Interactive map](../index.html)

## Purpose and status

The analysis estimates where along the 7th arc the probability of finding MH370 remains after three unsuccessful seabed searches, and how much of it lies in the area Ocean Infinity still has under contract (about 7,429 km², valid to 30 June 2027).

- **Status:** v1.0, frozen on 20 November 2026, before any posterior was computed. Changes after the first computation are logged with date and reason, and results are reported under the original choices as well.
- **What was computed before the freeze:** only the search-coverage inputs (section 1). No prior, likelihood or posterior had been evaluated.
- **Output:** a probability map on a 0.02° grid, plus a short table of probability mass by region (section 4).

## 1. Search coverage inputs

The three searches enter the model as fixed coverage layers. Only the 2014–17 layer is measured; the other two are reconstructions and are treated as uncertain (section 5).

| Search | Layer used | Area | Basis | Confidence |
| --- | --- | --- | --- | --- |
| ATSB 2014–17 | Per-sensor coverage from Geoscience Australia 5 m sonar mosaics, on a 0.02° grid | ≈124,500 km² (official ≈120,000) | Measured | High |
| OI 2018 | CAPTION outer boundary minus ATSB area | ≈125,100 km² envelope; OI reports 112,000 km² searched | Published envelope | Medium |
| OI 2018 gaps | Envelope cells more than 25.2 km from the Seabed Constructor's hourly track | ≈13,100 km² (≈5,100 km² more than 34.4 km away) | Calibrated to the reported 112,000 km² | Low |
| OI 2025–26 | ±4.2 km band around Armada 86 05 and Armada 78 06 hourly positions, inside the 2024 proposed area | ≈7,150 km² (Dec 2025–Jan 2026) + ≈4,200 km² (Mar 2025) | Calibrated to the reported ≈7,200 km² | Low |

**Fixed rule for overlaps:** a cell covered by several searches gets each search's detection probability applied independently (section 3).

**Validation already done:** the proposed 2024 area minus the estimated 2025–26 coverage leaves ≈8,100 km², against the 7,429 km² officially remaining.

## 2. Prior distributions

The prior is the product of an along-arc density (where the aircraft crossed the 7th arc) and a cross-arc density (how far from the arc it hit the water). Three along-arc priors and two cross-arc models are fixed in advance; no prior is chosen after seeing results.

**Along-arc priors** (latitude of the 7th-arc crossing, 24°S to 40°S):

| ID | Name | Definition | Source |
| --- | --- | --- | --- |
| A1 | Satellite-data prior | DSTG particle-filter density along the arc, digitized from the published figure on a 0.25° latitude grid, before any search result is applied | [DSTG book (2016)](https://link.springer.com/book/10.1007/978-981-10-0379-0); [ATSB, Dec 2015](https://atsb.gov.au/sites/default/files/media/5733650/AE-2014-054_MH370-Definition%20of%20Underwater%20Search%20Areas_3Dec2015.pdf) |
| A2 | Reconstructed-path prior | Normal distribution in latitude, mean 34.23°S (UGIB 2020 last estimated position), SD 0.5° | UGIB 2020 |
| A3 | Drift prior | Equal mixture of two uniform bands: 33°S–36°S (CSIRO / First Principles Review) and 28°S–33°S (UWA) | [ATSB First Principles Review (2016)](https://www.atsb.gov.au/sites/default/files/media/5772107/ae2014054_final-first-principles-report.pdf); [CSIRO (2017)](https://www.csiro.au/en/news/all/articles/2017/april/mh370) |

The **primary analysis** uses the mixture 1/3 A1 + 1/3 A2 + 1/3 A3. Each prior is also run on its own (section 5).

**Cross-arc models** (signed distance from the arc, positive = outward / south-east):

- **C1, unpiloted end of flight:** uniform from −25 NM to +25 NM, following the First Principles Review conclusion that the aircraft most likely hit within ~25 NM of the arc.
- **C2, piloted glide:** uniform from −100 NM to +100 NM.
- **Primary mixture:** 0.8 × C1 + 0.2 × C2. Sensitivity runs use 1.0/0.0 and 0.5/0.5.

The weights 1/3 and 0.8/0.2 are judgement calls, stated here so they cannot be tuned later.

## 3. Detection probability

A covered cell is not a cleared cell: the probability that a debris field there would have been detected depends on the sensor and on the terrain. The values below are fixed assumptions, not measurements.

**Terrain class** per 0.02° cell, from the Phase 1 bathymetry (150 m grid, Geoscience Australia): the 90th-percentile seabed slope within the cell. Flat < 5°, moderate 5–15°, steep > 15°.

| Search and sensor | Flat | Moderate | Steep |
| --- | --- | --- | --- |
| ATSB deep-tow side-scan (Fugro) | 0.90 | 0.75 | 0.50 |
| ATSB synthetic aperture sonar (GO Phoenix, Dong Hai Jiu 101) | 0.90 | 0.80 | 0.60 |
| ATSB AUV side-scan (Fugro) | 0.90 | 0.90 | 0.85 |
| OI 2018 AUVs, inside envelope and not a likely gap | 0.90 | 0.85 | 0.75 |
| OI 2018 likely gap cells | 0 | 0 | 0 |
| OI 2025–26 AUVs, estimated coverage | 0.90 | 0.85 | 0.75 |

All cells outside every coverage layer have detection probability 0. A 2022 Geoscience Australia re-review of the 2014–17 data found eleven contact sites not analysed in the original search; this is one reason the flat-terrain value is 0.90 and not higher ([ATSB MH370 Data Review 2022](https://www.atsb.gov.au/sites/default/files/2024-02/mh370-data-review-2022-final-report-v2.pdf)).

## 4. Computation and outputs

The posterior is the prior multiplied, cell by cell, by the probability that every search that covered the cell missed the debris field, then renormalized:

```
P_post(c) = P_prior(c) · Π_s (1 − d_s(c))  /  Σ_c' P_prior(c') · Π_s (1 − d_s(c'))
```

Here c is a grid cell and d_s(c) the detection probability of search s in that cell (0 where s did not cover it).

- **Domain:** 7th-arc crossings from 24°S to 40°S, up to 100 NM either side of the arc. The result is conditional on the aircraft being in this domain.
- **Grid:** 0.02° in latitude and longitude, the same grid as the coverage layers.
- **Arc:** equal slant range from Inmarsat-3F1 at 20,000 ft, satellite sub-point 0.54°N 64.46°E (fitted to the CAPTION arc, residual SD 25 m).

**Outputs, all fixed in advance:**

1. Posterior map, published as a layer on the interactive map.
2. Probability mass in five regions: OI 2025–26 remaining contract area; OI 2018 likely gaps; within ±25 NM of the arc but never searched; 25–100 NM from the arc and never searched; all searched cells together (residual from imperfect detection).
3. The ten 0.02° cells with the highest posterior, merged into clusters, with their latitude, side of the arc and which search last covered them.
4. Prior-to-posterior ratio for the OI remaining contract area: whether three failed searches made that area more or less likely.

## 5. Sensitivity analyses

A finding is called **robust** only if it holds in every run below; otherwise it is reported as depending on the named assumption.

| Run | What changes | Values |
| --- | --- | --- |
| S1–S3 | Along-arc prior alone | A1, A2, A3 one at a time |
| S4–S5 | Cross-arc mixture | C1 only; 0.5 × C1 + 0.5 × C2 |
| S6–S7 | All detection probabilities | Each value × 0.8; each value raised to min(0.98, value + 0.08) |
| S8 | OI 2018 gaps | Treat the likely gaps as searched (detection as the rest of 2018) |
| S9 | OI 2018 gaps | Only the strong gaps (> 34.4 km from track) unsearched |
| S10 | OI 2025–26 coverage | Track buffer 3.0 km and 6.0 km instead of 4.2 km |
| S11 | March 2025 activity | Excluded from coverage |
| S12 | Arc altitude | Arc at sea level instead of 20,000 ft |

**Pre-stated questions the runs must answer:**

1. Does the OI 2025–26 remaining contract area hold more posterior mass than any other region of equal size?
2. Do the OI 2018 likely gaps hold enough mass that checking them would matter (more than 5% of the total)?
3. Is any single cluster above 10% of the total in every run?

## 6. Limitations

The result is a structured way of combining published inputs, not a new location estimate.

- **Inherited assumptions:** the priors come from other people's models. If the southern-route, 7th-arc framework is wrong, the posterior is wrong too.
- **Reconstructed coverage:** the OI 2018 gaps and the OI 2025–26 coverage are inferred from hourly ship positions. Neither is the real AUV track.
- **Debris absence not modelled:** the lack of debris on Australian shores and the 2014 aerial search are not used as evidence in this version.
- **WSPR:** Godfrey's WSPR-based location is not used as a prior, so this analysis stays independent of a separate WSPR validation project.
- **No claim of precision:** the posterior is reported at 0.02° resolution, but the inputs do not support pinpointing the aircraft to a single cell.

## Change log

Deviations made while computing, after the freeze. None changes a prior, a weight or a detection value.

| Date | Change | Reason |
| --- | --- | --- |
| 20 Nov 2026 | A1 digitized from DSTG Fig. 10.3 (latitude of the aircraft at 00:19, with BFO), resampled to 0.25° | The figure is the only published 1-D form of the DSTG density |
| 20 Nov 2026 | Terrain class assigned on a 0.04° grid (most common class of four 0.02° cells), not 0.02° | Data transfer limit |
| 20 Nov 2026 | Depth read from the colour-ramped WMS rendering of the 150 m grid, sampled at 0.004°; slope from 3×3-smoothed depth over an 800 m baseline | The raw grid was not reachable; colour decoding limits depth precision to about 10–25 m |
| 20 Nov 2026 | Searched cells without Phase 1 bathymetry (≈37,000 km²) treated as moderate terrain | Rule was not specified in v1.0 |
| 20 Nov 2026 | Question 3 answered literally (clusters of the top ten cells), plus 50/80/95% highest-probability areas reported | Ten 0.02° cells cannot reach 10%; the literal question was poorly specified |
| 22 Nov 2026 | v1.1: Feb 2025 fill-in pass of Armada 78 06 (23–28 Feb, 34–35°S) added to the 2025–26 coverage with the same ±4.2 km rule; run S13 keeps the v1.0 coverage | The pass was missed in v1.0 (pointed out by a reader); it re-searched gaps of earlier searches |
| 22 Nov 2026 | v1.2: 2025–26 coverage counts all work hours (first to last slow position of each voyage) in the search region, not only inside the 2024 zone; run S14 drops the Jan 2026 hours outside the zone; robust core threshold set to 70% of runs | Same cause as the v1.1 miss; work outside the zone was not counted |

## Sources

- [Geoscience Australia: MH370 Phase 2 5 m sonar mosaics](https://pid.geoscience.gov.au/dataset/ga/120969), via the [AusSeabed GeoServer](https://warehouse.ausseabed.gov.au/geoserver/ausseabed/ows). Source: Governments of Australia, Malaysia and the People's Republic of China, 2018. MH370 Phase 2 data. CC BY 4.0.
- [MH370-CAPTION: Armada-tracking](https://www.mh370-caption.net/index.php/armada-tracking/) — OI 2018 boundary, 2024 proposed area, 7th arc, ship tracks.
- [Ocean Infinity: 2018 search update](https://oceaninfinity.com/news/update-on-search-for-malaysian-airlines-flight-mh370/) — 112,000 km² searched.
- [AP via ABC News: contract extension, June 2026](https://abcnews.com/International/wireStory/malaysia-extends-search-mh370-year-keeping-families-hopes-134301629) — 7,428.54 km² remaining, to 30 June 2027.
- [Davey et al., Bayesian Methods in the Search for MH370 (2016)](https://link.springer.com/book/10.1007/978-981-10-0379-0).
- [ATSB: Definition of Underwater Search Areas, Dec 2015](https://atsb.gov.au/sites/default/files/media/5733650/AE-2014-054_MH370-Definition%20of%20Underwater%20Search%20Areas_3Dec2015.pdf).
- [ATSB: First Principles Review, Dec 2016](https://www.atsb.gov.au/sites/default/files/media/5772107/ae2014054_final-first-principles-report.pdf).
- [ATSB: MH370 Data Review 2022](https://www.atsb.gov.au/sites/default/files/2024-02/mh370-data-review-2022-final-report-v2.pdf).
- [Iannello: The Search for MH370 Continues into 2026](https://mh370.radiantphysics.com/2026/01/01/the-search-for-mh370-continues-into-2026/) — UGIB last estimated position.
