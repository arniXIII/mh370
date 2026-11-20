# Data sources and terms

The code in this repository is MIT-licensed (see `LICENSE`). The data keep their own terms.

| Data | Where it is used | Source | Terms |
| --- | --- | --- | --- |
| ATSB 2014–17 sonar coverage (`data/derived/atsb_phase2_mask_rle.txt`) | Coverage layer | Geoscience Australia, MH370 Phase 2 5 m sonar mosaics, via the AusSeabed GeoServer ([dataset](https://pid.geoscience.gov.au/dataset/ga/120969)) | CC BY 4.0. Attribution: *Source: Governments of Australia, Malaysia and the People's Republic of China, 2018. MH370 Phase 2 data.* |
| Seabed slope classes (`data/derived/slope_class_004deg_rle.txt`) | Detection probability | Derived from Geoscience Australia, Southern Indian Ocean (MH370) Bathymetry 150 m 2017, via the AusSeabed GeoServer | CC BY 4.0, same attribution |
| OI 2018 search boundary, 2024 proposed area, 7th-arc polyline, ship tracks (Seabed Constructor 2018, Armada 78 06 and 86 05 2025–26) | Coverage layers, arc fit | [MH370-CAPTION](https://www.mh370-caption.net/index.php/armada-tracking/), files at `github.com/trise5631/trise5631.github.io` | No licence stated by the authors. The raw files are **not** included here; `scripts/01_fetch_caption.py` downloads them. Derived layers in `out/` and `index.html` credit CAPTION. |
| DSTG along-arc density (`data/derived/dstg_fig10_3_digitized.json`) | Prior A1 | Digitized from Fig. 10.3 of Davey et al. (2016), *Bayesian Methods in the Search for MH370*, Springer, open access | © Commonwealth of Australia 2016, open access book; figure values digitized and cited |
| Debris list (`data/points.json`) | Map | Malaysia Ministry of Transport, *Summary of Possible MH370 Debris Recovered* (30 Dec 2018); one item from Godfrey and Gibson (2022) | Factual list; coordinates assigned by hand at beach or town level |
| Coastlines (`data/land_clip.json`) | Map | Natural Earth 1:50m land, via the `world-atlas` npm package | Public domain |
| Prior parameters (UGIB 2020 last estimated position, CSIRO and UWA drift bands, First Principles Review ±25 NM) | Priors A2, A3, C1 | Cited in `docs/protocol.md` | Published figures, cited |
