# MH370 residual-probability analysis — results v1.1

22 November 2026 · [Protocol](protocol.md) · [Interactive map](../index.html) · Independent analysis, not peer-reviewed

Under the pre-registered assumptions, the area Ocean Infinity still has under contract holds only about 2.5% of the remaining probability (0–6% across all runs); far more sits along the arc within 25 NM, including ground already searched, and in bands 25–100 NM from the arc if a piloted glide is allowed. All numbers below are reproduced by `scripts/05_posterior.py` (see `out/results.json`).

## What changed in v1.1

Version 1.0 missed the first phase of the 2025 search. Between 23 and 28 February 2025, Armada 78 06 worked between 34°S and 35°S around 92.8–94.0°E, filling in gaps and low-quality data from the earlier searches, including the High Priority Area south of the UGIB 2020 estimate. v1.1 adds this pass using the same rule as the rest of the 2025–26 coverage (±4.2 km around the hourly ship positions from CAPTION), about 4,900 km². Thanks to the Reddit user who pointed this out.

The headline answers do not change. The main effect is on the exploratory "most likely area": its main block moves north, away from the re-searched ground. Run S13 reproduces the v1.0 coverage exactly, so the original results remain available, as the protocol requires.

## Answers to the pre-stated questions

| Question | Answer | Robust? |
| --- | --- | --- |
| 1. Does the OI remaining contract area hold more posterior mass than any other region of equal size? | **No.** It holds 2.5% in the primary run (0–6.0% across runs). The best region of the same size elsewhere holds 11.3% (6.3–24.8%). | Yes, in all 15 runs |
| 2. Do the OI 2018 likely gaps hold more than 5% of the total? | **Only under some assumptions.** 6.4% in the primary run; 15.7% with the drift prior alone; 0.0–0.5% with the DSTG or UGIB prior alone. | No: depends on the along-arc prior |
| 3. Is any single cluster above 10% in every run? | **No.** The top ten cells form two clusters near 34.3°S, 93.2–93.5°E holding 0.27% together. They sit in thin slivers between coverage layers and are probably a boundary artifact. | Yes |

The searches did make the remaining contract area relatively more likely: its share rose 2.4–5.0 times from prior to posterior in every run where it had any prior mass. It started from a very small base.

## Where the probability sits (primary run)

The chance that all three searches would have missed the aircraft, given the prior, is 25%. After that update the probability is spread thinly: the smallest area holding half of it is about 99,000 km².

| Region | Area (km²) | Prior | Posterior |
| --- | --- | --- | --- |
| R1 OI remaining contract area | 8,006 | 0.6% | 2.5% |
| R2 OI 2018 likely gaps | 13,436 | 1.6% | 6.4% |
| R3 never searched, within 25 NM of the arc | 70,534 | 2.1% | 8.3% |
| R4 never searched, 25–100 NM from the arc | 741,450 | 12.2% | 48.0% |
| R5 all searched cells (imperfect detection) | 244,947 | 83.5% | 34.8% |

By latitude, the 34–36°S band still holds the most (35%), followed by 32–34°S (19%) and 36–38°S (14%). The inner and outer sides of the arc hold similar shares in every band.

## Sensitivity runs

The end-of-flight assumption moves the result most: with no piloted glide (S4) everything stays within 25 NM and the remaining contract area drops to zero; with a 50:50 mix (S5) almost three quarters lies 25–100 NM out. The coverage reconstructions (S8–S11, S13) and arc altitude (S12) barely matter.

| Run | R1 contract area | R2 2018 gaps | R3 unsearched <25 NM | R4 unsearched 25–100 NM | R5 searched | Best equal-area elsewhere |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | 2.5% | 6.4% | 8.3% | 48.0% | 34.8% | 11.3% |
| S1 A1 only | 0.6% | 0.0% | 9.1% | 52.1% | 38.2% | 13.6% |
| S2 A2 only | 6.0% | 0.5% | 3.7% | 49.6% | 40.3% | 24.8% |
| S3 A3 only | 1.5% | 15.7% | 11.0% | 43.6% | 28.2% | 18.5% |
| S4 C1 only | 0.0% | 13.1% | 17.1% | 0.0% | 69.7% | 23.4% |
| S5 C1/C2 50:50 | 3.8% | 2.9% | 3.7% | 72.9% | 16.7% | 6.3% |
| S6 detection ×0.8 | 1.7% | 4.3% | 5.5% | 32.0% | 56.5% | 12.7% |
| S7 detection +0.08 | 3.2% | 8.2% | 10.6% | 61.2% | 16.8% | 12.7% |
| S8 2018 gaps searched | 2.6% | 0.0% | 8.8% | 50.8% | 37.8% | 11.9% |
| S9 only strong 2018 gaps | 2.6% | 2.2% | 8.6% | 49.8% | 36.7% | 11.6% |
| S10a 2025 buffer 3.0 km | 2.7% | 6.4% | 8.3% | 47.7% | 35.0% | 12.1% |
| S10b 2025 buffer 6.0 km | 2.3% | 6.5% | 8.1% | 48.3% | 34.8% | 10.4% |
| S11 no March 2025 | 2.9% | 6.4% | 8.3% | 47.9% | 34.6% | 13.2% |
| S12 arc at sea level | 2.5% | 6.8% | 7.4% | 48.0% | 35.3% | 10.7% |
| S13 Feb 2025 fill-in ignored (v1.0 coverage) | 2.4% | 6.2% | 8.8% | 46.6% | 36.0% | 12.3% |

## What this does and does not show

The analysis turns published assumptions into a map; it does not add new evidence about where the aircraft is.

- **The decisive unknown is the end of flight.** Whether the aircraft fell within 25 NM or glided farther decides whether the best remaining bet is re-checking the arc strip or opening wide new areas. No search plan is robust to that choice.
- **Searched ground is not cleared ground.** About a third of the probability remains in cells already searched, because detection was assumed at 0.50–0.90. Re-examining difficult terrain near the arc competes with new area.
- **The remaining contract area is a weak bet under these inputs.** All of it lies at least 29 NM (54 km) from the arc, about three quarters on the inner side, where the priors put little weight.
- **The 2018 gaps matter only if the drift evidence is trusted.** They sit at 25–32°S, where only the drift prior has mass.
- **Limits:** priors are other people's models; the 2018 gaps and 2025–26 coverage are reconstructions from hourly ship positions; slope is decoded from a coloured map image; the position of the 7th arc itself is taken as exact apart from aircraft altitude; debris absence on Australian coasts is not used.

## Addendum: most likely area (exploratory)

*Added after the v1.0 results. Not part of the pre-registered protocol, so treat it as exploratory.*

For each of the 15 runs we took the 10,000 km² with the highest posterior probability per km² (0.04° cells), roughly the scale of one season of AUV search. The **robust core** is the set of cells that fall in that area in at least 10 of the 15 runs.

- The top 10,000 km² holds 12.3% of the probability in the primary run, and 7.4–27.4% across the runs (lowest with glide weight 50%, highest with the UGIB prior only).
- The robust core covers about 7,400 km² and holds 10.0% in the primary run.
- Its largest block (about 2,700 km², 3.5%) is centred at 34.00°S 93.73°E, on the north-west side of the arc within 46 km, just north of the UGIB 2020 estimate. It is almost all ground searched only once, mostly by Ocean Infinity in 2018, on moderately sloped seabed.
- In v1.0 the core also included the High Priority Area south of the UGIB estimate. That ground was re-searched in February 2025 and has dropped out.

This is the best bet under the model, not a likely location: about 88% of the probability lies outside the top 10,000 km² in the primary run.
