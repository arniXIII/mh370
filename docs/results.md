# MH370 residual-probability analysis — results v1.0

20 November 2026 · [Protocol](protocol.md) · [Interactive map](../index.html) · Independent analysis, not peer-reviewed

Under the pre-registered assumptions, the area Ocean Infinity still has under contract holds only about 2% of the remaining probability (0–6% across all runs); far more sits along the arc within 25 NM, including ground already searched, and in bands 25–100 NM from the arc if a piloted glide is allowed. All numbers below are reproduced by `scripts/05_posterior.py` (see `out/results.json`).

## Answers to the pre-stated questions

| Question | Answer | Robust? |
| --- | --- | --- |
| 1. Does the OI remaining contract area hold more posterior mass than any other region of equal size? | **No.** It holds 2.4% in the primary run (0–5.6% across runs). The best region of the same size elsewhere holds 12.3% (6.6–26.3%). | Yes, in all 14 runs |
| 2. Do the OI 2018 likely gaps hold more than 5% of the total? | **Only under some assumptions.** 6.2% in the primary run; 15.4% with the drift prior alone; 0.0–0.4% with the DSTG or UGIB prior alone. | No: depends on the along-arc prior |
| 3. Is any single cluster above 10% in every run? | **No.** The top ten cells form two clusters near 34.3°S, 93.2–93.5°E holding 0.26% together. They sit in thin slivers between coverage layers and are probably a boundary artifact. | Yes |

The searches did make the remaining contract area relatively more likely: its share rose 2.3–4.8 times from prior to posterior in every run where it had any prior mass. It started from a very small base.

## Where the probability sits (primary run)

The chance that all three searches would have missed the aircraft, given the prior, is 26%. After that update the probability is spread thinly: the smallest area holding half of it is about 95,000 km².

| Region | Area (km²) | Prior | Posterior |
| --- | --- | --- | --- |
| R1 OI remaining contract area | 8,006 | 0.6% | 2.4% |
| R2 OI 2018 likely gaps | 13,436 | 1.6% | 6.2% |
| R3 never searched, within 25 NM of the arc | 70,680 | 2.3% | 8.8% |
| R4 never searched, 25–100 NM from the arc | 741,450 | 12.2% | 46.6% |
| R5 all searched cells (imperfect detection) | 244,801 | 83.3% | 36.0% |

By latitude, the 34–36°S band still holds the most (37%), followed by 32–34°S (19%) and 36–38°S (14%). The inner and outer sides of the arc hold similar shares in every band.

## Sensitivity runs

The end-of-flight assumption moves the result most: with no piloted glide (S4) everything stays within 25 NM and the remaining contract area drops to zero; with a 50:50 mix (S5) almost three quarters lies 25–100 NM out. The coverage reconstructions (S8–S11) and arc altitude (S12) barely matter.

| Run | R1 contract area | R2 2018 gaps | R3 unsearched <25 NM | R4 unsearched 25–100 NM | R5 searched | Best equal-area elsewhere |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | 2.4% | 6.2% | 8.8% | 46.6% | 36.0% | 12.3% |
| S1 A1 only | 0.6% | 0.0% | 9.3% | 51.7% | 38.4% | 13.6% |
| S2 A2 only | 5.6% | 0.4% | 5.1% | 46.3% | 42.6% | 26.3% |
| S3 A3 only | 1.4% | 15.4% | 11.3% | 42.9% | 29.0% | 18.3% |
| S4 C1 only | 0.0% | 12.4% | 17.6% | 0.0% | 70.0% | 24.6% |
| S5 C1/C2 50:50 | 3.7% | 2.9% | 4.0% | 71.9% | 17.5% | 6.6% |
| S6 detection ×0.8 | 1.6% | 4.2% | 5.9% | 31.1% | 57.3% | 13.0% |
| S7 detection +0.08 | 3.1% | 8.0% | 11.3% | 59.7% | 17.9% | 13.5% |
| S8 2018 gaps searched | 2.6% | 0.0% | 9.3% | 49.3% | 38.9% | 12.8% |
| S9 only strong 2018 gaps | 2.5% | 2.1% | 9.1% | 48.3% | 37.9% | 12.6% |
| S10a 2025 buffer 3.0 km | 2.6% | 6.2% | 8.8% | 46.6% | 35.8% | 12.9% |
| S10b 2025 buffer 6.0 km | 2.2% | 6.3% | 8.8% | 46.6% | 36.1% | 11.6% |
| S11 no March 2025 | 2.8% | 6.2% | 8.8% | 46.5% | 35.7% | 14.0% |
| S12 arc at sea level | 2.4% | 6.6% | 8.0% | 46.6% | 36.4% | 11.7% |

## What this does and does not show

The analysis turns published assumptions into a map; it does not add new evidence about where the aircraft is.

- **The decisive unknown is the end of flight.** Whether the aircraft fell within 25 NM or glided farther decides whether the best remaining bet is re-checking the arc strip or opening wide new areas. No search plan is robust to that choice.
- **Searched ground is not cleared ground.** About a third of the probability remains in cells already searched, because detection was assumed at 0.50–0.90. Re-examining difficult terrain near the arc competes with new area.
- **The remaining contract area is a weak bet under these inputs.** All of it lies at least 29 NM (54 km) from the arc, about three quarters on the inner side, where the priors put little weight.
- **The 2018 gaps matter only if the drift evidence is trusted.** They sit at 25–32°S, where only the drift prior has mass.
- **Limits:** priors are other people's models; the 2018 gaps and 2025–26 coverage are reconstructions from hourly ship positions; slope is decoded from a coloured map image; debris absence on Australian coasts is not used.

## Addendum: most likely area (exploratory)

*Added after the v1.0 results. Not part of the pre-registered protocol, so treat it as exploratory.*

For each of the 14 runs we took the 10,000 km² with the highest posterior probability per km² (0.04° cells), roughly the scale of one season of AUV search. The **robust core** is the set of cells that fall in that area in at least 10 of the 14 runs.

- The top 10,000 km² holds 13.2% of the probability in the primary run, and 7.6–28.8% across the runs (lowest with glide weight 50%, highest with the UGIB prior only).
- The robust core covers 6,154 km² and holds 9.7% in the primary run.
- Its largest block (about 3,450 km², 5.5%) is centred at 34.20°S 93.46°E, on the north-west side of the arc within 45 km, near the UGIB 2020 estimate. It is mostly ground searched only once (about 2,970 km², 3.3%), plus a thin strip of about 400 km² between the 2014–17 and 2018 boundaries that appears unsearched in our reconstruction and may be an artefact.
- The second block (about 1,100 km², 1.6%) is at 34.59°S 93.84°E, on steep slopes 10–45 km south-east of the arc, close to Iannello's 2023 High Priority Area.

This is the best bet under the model, not a likely location: about 87% of the probability lies outside the top 10,000 km² in the primary run.
