# MH370 residual-probability analysis — results v1.2

22 November 2026 · [Protocol](protocol.md) · [Interactive map](../index.html) · Independent analysis, not peer-reviewed

Under the pre-registered assumptions, the area Ocean Infinity still has under contract holds only about 2.5% of the remaining probability (0–6% across all runs); far more sits along the arc within 25 NM, including ground already searched, and in bands 25–100 NM from the arc if a piloted glide is allowed. All numbers below are reproduced by `scripts/05_posterior.py` (see `out/results.json`).

## What changed in v1.1 and v1.2

Version 1.0 missed the first phase of the 2025 search. Between 23 and 28 February 2025, Armada 78 06 worked between 34°S and 35°S around 92.8–94.0°E, filling in gaps and low-quality data from the earlier searches, including the High Priority Area south of the UGIB 2020 estimate. v1.1 adds this pass using the same rule as the rest of the 2025–26 coverage (±4.2 km around the hourly ship positions from CAPTION), about 4,900 km². Thanks to the Reddit user who pointed this out.

v1.2 fixes the cause of that miss. v1.0 counted 2025–26 ship positions only inside the 2024 proposed search zone. v1.2 counts every hour between the first and last slow (under 8 km/h) position of each voyage in the search region, inside or outside the zone, with the same ±4.2 km band. This adds about 2,000 km² worked in March 2025 around 36°S 92–93°E and about 300 km² in January 2026. Coverage inside the zone, and its calibration, are unchanged. Whether the January hours outside the zone were search or weather standby is unclear, so run S14 leaves them out.

The headline answers do not change. The main effect is on the exploratory "most likely area": its main block moves north, away from the re-searched ground. Run S13 reproduces the v1.0 coverage exactly, so the original results remain available, as the protocol requires.

## Answers to the pre-stated questions

| Question | Answer | Robust? |
| --- | --- | --- |
| 1. Does the OI remaining contract area hold more posterior mass than any other region of equal size? | **No.** It holds 2.5% in the primary run (0–6.0% across runs). The best region of the same size elsewhere holds 11.4% (6.4–24.9%). | Yes, in all 16 runs |
| 2. Do the OI 2018 likely gaps hold more than 5% of the total? | **Only under some assumptions.** 6.4% in the primary run; 15.7% with the drift prior alone; 0.0–0.5% with the DSTG or UGIB prior alone. | No: depends on the along-arc prior |
| 3. Is any single cluster above 10% in every run? | **No.** The top ten cells form two clusters near 34.3°S, 93.2–93.5°E holding 0.27% together. They sit in thin slivers between coverage layers and are probably a boundary artifact. | Yes |

The searches did make the remaining contract area relatively more likely: its share rose 2.4–5.0 times from prior to posterior in every run where it had any prior mass. It started from a very small base.

## Where the probability sits (primary run)

The chance that all three searches would have missed the aircraft, given the prior, is 25%. After that update the probability is spread thinly: the smallest area holding half of it is about 98,000 km².

| Region | Area (km²) | Prior | Posterior |
| --- | --- | --- | --- |
| R1 OI remaining contract area | 8,006 | 0.6% | 2.5% |
| R2 OI 2018 likely gaps | 13,436 | 1.6% | 6.4% |
| R3 never searched, within 25 NM of the arc | 70,534 | 2.1% | 8.3% |
| R4 never searched, 25–100 NM from the arc | 739,308 | 12.1% | 47.7% |
| R5 all searched cells (imperfect detection) | 247,088 | 83.6% | 35.0% |

By latitude, the 34–36°S band still holds the most (35%), followed by 32–34°S (19%) and 36–38°S (14%). The inner and outer sides of the arc hold similar shares in every band.

## Sensitivity runs

The end-of-flight assumption moves the result most: with no piloted glide (S4) everything stays within 25 NM and the remaining contract area drops to zero; with a 50:50 mix (S5) almost three quarters lies 25–100 NM out. The coverage reconstructions (S8–S11, S13, S14) and arc altitude (S12) barely matter.

| Run | R1 contract area | R2 2018 gaps | R3 unsearched <25 NM | R4 unsearched 25–100 NM | R5 searched | Best equal-area elsewhere |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | 2.5% | 6.4% | 8.3% | 47.7% | 35.0% | 11.4% |
| S1 A1 only | 0.6% | 0.0% | 9.2% | 51.8% | 38.4% | 13.7% |
| S2 A2 only | 6.0% | 0.5% | 3.7% | 49.4% | 40.5% | 24.9% |
| S3 A3 only | 1.5% | 15.7% | 11.1% | 43.4% | 28.4% | 18.6% |
| S4 C1 only | 0.0% | 13.1% | 17.1% | 0.0% | 69.8% | 23.4% |
| S5 C1/C2 50:50 | 3.8% | 2.9% | 3.7% | 72.7% | 16.9% | 6.4% |
| S6 detection ×0.8 | 1.7% | 4.3% | 5.5% | 31.8% | 56.7% | 12.7% |
| S7 detection +0.08 | 3.2% | 8.2% | 10.6% | 61.0% | 17.0% | 12.8% |
| S8 2018 gaps searched | 2.7% | 0.0% | 8.8% | 50.6% | 38.0% | 11.9% |
| S9 only strong 2018 gaps | 2.6% | 2.2% | 8.6% | 49.6% | 36.9% | 11.7% |
| S10a 2025 buffer 3.0 km | 2.7% | 6.4% | 8.3% | 47.5% | 35.1% | 12.1% |
| S10b 2025 buffer 6.0 km | 2.3% | 6.5% | 8.1% | 48.0% | 35.0% | 10.5% |
| S11 no March 2025 | 2.9% | 6.4% | 8.3% | 47.8% | 34.7% | 13.2% |
| S12 arc at sea level | 2.5% | 6.8% | 7.5% | 47.8% | 35.5% | 10.8% |
| S13 2025–26 coverage as in v1.0 | 2.4% | 6.2% | 8.8% | 46.6% | 36.0% | 12.3% |
| S14 Dec–Jan work outside zone ignored | 2.5% | 6.4% | 8.3% | 47.8% | 35.0% | 11.4% |

## Check against official figures

| Quantity | Official | This model (v1.2) | Difference |
| --- | --- | --- | --- |
| ATSB 2014–17 searched area | about 120,000 km² | 124,500 km² | +4% |
| Ocean Infinity 2018 | 112,000 km² | 111,643 km² | calibrated to this |
| 2024 proposed zone | about 15,000 km² | 15,677 km² | +4.5% |
| Zone searched in 2025–26 | 15,000 − 7,428.54 ≈ 7,571 km² | 7,671 km² | +1.3% |
| Zone remaining | 7,428.54 km² | 8,006 km² | +7.8% |

The zone boundary comes from the CAPTION map and is slightly larger than the official 15,000 km², which explains most of the gap in the remaining area.

One figure does not match. Ocean Infinity says it has mapped more than 140,000 km² since 2018. This model has about 126,500 km² in total: 112,000 in 2018 and about 14,800 in 2025–26 (7,671 inside the zone, 4,834 in the February fill-in, 2,328 outside the zone in March and January). The gap of about 13,500 km² could mean the 2018 search was larger than 112,000 km² (the CAPTION boundary encloses 125,000 km²), that the ±4.2 km bands underestimate 2025–26 coverage, or that "mapped" also counts overlaps or transit surveys. Public data cannot settle this. The sensitivity runs show it matters little: treating all 2018 gaps as searched (S8) or widening the 2025 band to 6 km (S10b) moves the headline numbers by a few tenths of a percent and does not change any answer.

## What this does and does not show

The analysis turns published assumptions into a map; it does not add new evidence about where the aircraft is.

- **The decisive unknown is the end of flight.** Whether the aircraft fell within 25 NM or glided farther decides whether the best remaining bet is re-checking the arc strip or opening wide new areas. No search plan is robust to that choice.
- **Searched ground is not cleared ground.** About a third of the probability remains in cells already searched, because detection was assumed at 0.50–0.90. Re-examining difficult terrain near the arc competes with new area.
- **The remaining contract area is a weak bet under these inputs.** All of it lies at least 29 NM (54 km) from the arc, about three quarters on the inner side, where the priors put little weight.
- **The 2018 gaps matter only if the drift evidence is trusted.** They sit at 25–32°S, where only the drift prior has mass.
- **Limits:** priors are other people's models; the 2018 gaps and 2025–26 coverage are reconstructions from hourly ship positions; slope is decoded from a coloured map image; the position of the 7th arc itself is taken as exact apart from aircraft altitude; debris absence on Australian coasts is not used.

## Addendum: most likely area (exploratory)

*Added after the v1.0 results. Not part of the pre-registered protocol, so treat it as exploratory.*

For each of the 16 runs we took the 10,000 km² with the highest posterior probability per km² (0.04° cells), roughly the scale of one season of AUV search. The **robust core** is the set of cells that fall in that area in at least 70% of the runs (12 of 16; 10 of 14 in v1.0).

- The top 10,000 km² holds 12.4% of the probability in the primary run, and 7.4–27.4% across the runs (lowest with glide weight 50%, highest with the UGIB prior only).
- The robust core covers about 5,200 km² and holds 8.0% in the primary run.
- Its largest block (about 2,600 km², 3.4%) is centred at 34.00°S 93.74°E, on the north-west side of the arc within 46 km, just north of the UGIB 2020 estimate. It is almost all ground searched only once, mostly by Ocean Infinity in 2018, on moderately sloped seabed.
- In v1.0 the core also included the High Priority Area south of the UGIB estimate. That ground was re-searched in February 2025 and has dropped out.

This is the best bet under the model, not a likely location: about 88% of the probability lies outside the top 10,000 km² in the primary run.
