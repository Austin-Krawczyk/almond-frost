# Spec changelog

Every deviation from `CLAUDE.md`, dated, with the reason. One line each.

- 2026-09-22 — Project opened. The spec as issued on 2026-09-21 was saved as `CLAUDE.md` and
  immediately amended with the five decisions below, so that the spec never contradicts this
  changelog. Before any analysis, every Earth Engine ID in §5 was verified: the collection exists,
  carries the named band, and returns imagery for 1–7 February in each year 2015–2025. Band units
  and scale factors were read from the published catalogue entries rather than from memory.

- 2026-09-22 — **§5.2 VIIRS replaces Aqua as the primary polar orbiter.** The spec named
  `MODIS/061/MYD11A1` (Aqua) primary "at ~01:30 local". Measured February night overpass time over
  Fresno, taken from each product's own view-time band, is: Aqua 02:03 (2015) → 02:04 (2022) →
  02:29 (2024) → **03:16 (2025)**; Terra 22:11 → 21:16; VIIRS 01:49 → 01:39, stable throughout.
  Aqua was never at 01:30 and has drifted more than an hour later since its orbit stopped being
  maintained. VIIRS (`NASA/VIIRS/002/VNP21A1N`) is the only candidate holding near 01:30 across
  all eleven seasons and is therefore primary. Aqua stays as a full candidate, not a footnote.
  **The incorrect instruction came from the mission's design orbit rather than from observed view
  times**, and is carried into §8 as a worked example of the documentation-risk theme the exhibit
  is meant to carry. Approved by user.

- 2026-09-22 — **§6 Step 4b added: the Aqua drift experiment.** Aqua's overpass walked from about
  02:00 to about 03:16 across the study, steadily toward the true pre-dawn minimum, so the drift is
  treated as a designed experiment rather than a nuisance. Aqua's error against the station minimum
  is regressed on its **per-pixel view time**, pooling all station-nights, with view time as a
  covariate and explicitly **not** as a per-year offset, because per-year fitting would discard the
  within-night physics that makes the test interesting. If a later overpass reads systematically
  closer to the observed minimum, that independently confirms whatever Step 7 finds from GOES, by a
  different mechanism. Approved by user.

- 2026-09-22 — **§5.4 bias correction is now fitted per region AND per year**, replacing the
  spec's single season-wide offset per region. A single offset would blend the 2015 satellite with
  the 2025 one for Aqua and Terra, whose overpass times drift. Applied identically to every
  product so none is advantaged. The spec's original instruction was wrong for this reason.
  Approved by user.

- 2026-09-22 — **§5.2 GOES reduced to GOES-18 only (2023–2025), option (a).** The spec named
  `NOAA/GOES/18/MCMIPC`, which covers 3 of the 11 seasons; option (b) would have added GOES-17 for
  2019–2022, conditional on verifying that its infrared bands were usable on February nights.
  Tested on a **full February census** over a Central Valley box using the product's own
  `DQF_C13` flag — every night, 12Z and 14Z (04:00 and 06:00 PST), 2019–2022, no slots missing.
  Wholly unusable scenes (under 5% of valley pixels good): **0 of 28 at each slot in 2019**, then
  11/28 and 12/28 in 2020, 8/28 and 11/28 in 2021, 8/28 and 13/28 in 2022 — **63 of 168 across
  2020–2022, or 37.5%**, against **0 of 165 for GOES-18 in 2023–2025**. An earlier six-day-per-year
  sample had suggested "about a third"; the census confirms the rate and is what the exhibit
  quotes. The clean 2019 control, same code and box and flag, is what distinguishes an instrument
  fault from a screening artefact. GOES-17 is
  therefore substantially degraded in precisely our window and our hours — consistent with its loop
  heat pipe under-performing near satellite midnight — and is not used. GOES-16 is not used either:
  a steep eastern view angle over California adds a path-length problem on top of the atmospheric
  one. The exhibit will state that **ABI continuity for night thermal work in California
  effectively begins in 2023.** Approved by user, per the conditional check the user requested.

- 2026-09-22 — **§5.2 and §6 Step 4: GOES removed from the accuracy comparison entirely.**
  `CMI_C13`/`CMI_C14` are top-of-atmosphere brightness temperatures, not LST; the published band
  descriptions say "Brightness". A per-region bias correction cannot absorb a
  water-vapour-dependent offset, so an absolute accuracy comparison against a station would be
  unfair to GOES and misleading to a reader. GOES becomes a **timing instrument only** (Step 7),
  where within-night differencing largely cancels the atmospheric term. Recorded in §9 as a stated
  design limit, not a caveat. Approved by user.

- 2026-09-22 — **§5.2 ECOSTRESS confirmed present in Earth Engine** as
  `NASA/ECOSTRESS/L2T_LSTE/V2`, band `LST` in Kelvin, so the spec's hedge about possibly needing an
  ORNL DAAC download does not apply. Data begin 9 July 2018, giving bloom seasons **2019–2025**.
  Role unchanged: case-study sensor, never in the statistical comparison. Approved by user.

- 2026-09-22 — **Units check, recorded because it would have been a silent error.** MODIS
  `LST_Night_1km` carries scale 0.02 and is converted with ×0.02 − 273.15, as the spec says. VIIRS
  `LST_1KM` carries **no scale factor**: its catalogue entry gives none, and raw values over Fresno
  in February 2023 read 274–278, i.e. already Kelvin. Applying the MODIS recipe to VIIRS would have
  produced about −268 °C. Carried into §8 alongside the strawberry study's CPC 0.1 mm/day error as
  a second worked example of documentation risk.

- 2026-09-22 — Repository `almond-frost` created, public from the start, separate from the
  strawberry study's repository. The DWR statewide crop-mapping source and the CIMIS API client
  are reused from that study; provenance is recorded in `data/raw/`.

- 2026-09-22 — **Environment blocker, worked around.** `pyogrio` now fails to import: Windows
  Application Control blocks its bundled GDAL DLL (`ImportError: DLL load failed while importing
  _geometry: An Application Control policy has blocked this file`). Because geopandas 1.x uses
  pyogrio as its default and only installed engine, **geopandas could not read any file at all**,
  including files it read successfully the day before. Resolved by installing `fiona==1.10.1`,
  which ships its own GDAL binaries and is not blocked; geopandas reads through it with
  `engine="fiona"`. Added to `requirements.txt`. This is the same class of problem as the
  strawberry study's matplotlib 3.11.2 block, and it affects that repository's reproducibility
  too, since its notebooks call `gpd.read_file` with the default engine.
- 2026-09-22 — **DWR field-name finding.** The 2023 final geodatabase does not carry the crop in
  `CROPTYP1`, which the strawberry study used: in this file `CROPTYP1` is `****` for 419,240 of
  446,914 fields (13.8M acres). The populated field is **`MAIN_CROP`**, in which **`D12` covers
  1,524,133 acres** — the right order for California almonds, against D14 pistachios 602,106 and
  D13 walnuts 419,422. Almond units are therefore selected on `MAIN_CROP == 'D12'`, pending the
  documentation and CDL cross-checks in Step 1.

- 2026-09-22 — GOES-17 sample widened from six days per February to every February night at both
  pre-dawn slots, 2019–2022, before the figure goes in the exhibit: 224 scenes, none missing. The
  degradation holds and is now quoted as a rate. Raw per-night values saved to
  `data/derived/01x_goes17_dqf_february.json`.
- 2026-09-22 — **§8 gains a section, 'Silent failure modes in public datasets'**, carrying all
  three instances this programme has hit (CPC 0.1 mm/day scaling; VIIRS missing scale factor; DWR
  moving the crop field between survey years), each with the wrong value it would have produced,
  why that value looked plausible, and what caught it. The shared property — the error yields a
  believable number rather than an exception — is the generalisable point. Approved by user.
- 2026-09-22 — **§9 gains a rule:** no selector, field name or scale factor carried over from a
  previous project may be used without re-verification against the current file's own schema.
  Prompted by the DWR `CROPTYP1` near-miss, which would have returned 8,411 almond acres instead
  of about 1.5 million while looking entirely believable. Approved by user.
- 2026-09-22 — **§8 item 10 gains a fourth category: a check that returns a believable pass.**
  The first three instances are data returning a believable wrong value, which verification
  catches; the fourth is verification itself returning a believable pass, which defeats it. It
  occurred in the strawberry repository's environment patch, not in the almond analysis, and
  touched no result: a syntax check written as `try: ast.parse(...) except SyntaxError: continue`
  reported zero errors while three lines were semantically wrong (the engine argument landed
  inside a chained `.to_crs()`) and later seven were unparseable (literal backslashes in the
  notebook JSON). Caught by re-running with failures reported rather than skipped, and by
  printing the lines back as Python. Approved by user.
- 2026-09-22 — **§9 gains the matching rule:** a validation that can pass by skipping is not a
  validation. Checks must report failures explicitly and state what they examined; a harness that
  catches an exception and continues must log the catch and fail loudly at the end. Applies to
  every checkpoint, not only syntax checks — the same shape appears in cloud screens that
  silently drop nights and joins that silently drop rows — so **every checkpoint report carries
  its denominator.** Approved by user.
- 2026-09-22 — **D12 confirmed against DWR's published legend, closing the provisional finding.**
  *2022 DWR Standard Land Use Legend (Remote Sensing Version)*, linked from the CNRA dataset page
  recorded in `data/raw/dwr_crop_mapping/SOURCE.md`, sha256 `8fdc5aea368161cd96df33e7773de7d
  8936c8317a79391e8b1b7eedd1c01ec4e`: class **D — Deciduous Fruits and Nuts**, subclass **12 —
  Almonds**. The same page gives **13 — Walnuts** and **14 — Pistachios**, which the file's own
  acreage ordering matches (D12 1,524,133 ac, D14 602,106 ac, D13 419,422 ac). The magnitude is
  no longer doing the work: the legend is.
- 2026-09-22 — **Sacramento Valley defined by county, not by hydrologic region.** CLAUDE.md §4
  gives San Joaquin north and south as county pairs but names "Sacramento Valley (north)" without
  counties. It is defined as the ten Sacramento Valley counties carrying almond acreage (Butte,
  Colusa, Glenn, Placer, Sacramento, Solano, Sutter, Tehama, Yolo, Yuba), so that all three strata
  are defined the same way and the CDL comparison footprint matches the strata. DWR's own
  published boundary (`HYDRO_RGN` = "Sacramento River") moves 84 units and 3,564 acres, 1.2% of
  the region; it is reported as a sensitivity in Step 1 rather than used as the definition.
- 2026-09-22 — **CIMIS `Elevation` verified as feet, not assumed.** The API response states no
  unit. Compared against SRTM GL1 at each station's own coordinates, 258 of 276 stations: median
  ratio to SRTM-in-feet 0.999, median absolute difference 7 ft; ratio to SRTM-in-metres 3.278.
  `elev_m` is derived from it. The notebook asserts the ratio rather than trusting a comment.
- 2026-09-22 — **Earth Engine asset created:**
  `projects/cropczyk/assets/almond/dwr2023_almond_fields`, all 45,404 D12 fields with
  `study_region`, `is_unit`, `ACRES`, `COUNTY`, `HYDRO_RGN` and `YR_PLANTED`. Uploaded in twelve
  chunks because an inline FeatureCollection of the whole layer exceeds the request size limit,
  then merged server-side; the count is asserted against the DWR read. DWR geometries carry a Z
  coordinate that Earth Engine rejects as invalid GeoJSON, so they are flattened to 2D, which
  changes no planimetric area.
- 2026-09-22 — Project virtualenv created from `requirements.txt`, reading through `fiona` for the
  same Windows Application Control reason recorded for the strawberry repository.
- 2026-09-22 — **Strata redefined as latitude bands; every almond county is now assigned.** The
  county pairs in the original §4 ("Stanislaus/Merced", "Fresno/Kern") were illustrations of a
  north/south split, not a definition, and reading them literally left **26.7% of state almond
  acreage unassigned** — Madera 154,400 ac, San Joaquin 109,266, Tulare 87,260, Kings 35,420 and
  others — for no reason. Replaced by two boundaries, **38.25 N** (Sacramento Valley | San Joaquin
  north) and **36.82 N** (San Joaquin north | San Joaquin south), placed to fall *between*
  counties and chosen as the local minima of almond acreage landing on the wrong side. Coverage is
  now **100.00%: 24 counties, 39,102 units, 1,509,261 acres** — Sacramento Valley 11 counties /
  292,322 ac, San Joaquin north 7 / 621,091, San Joaquin south 6 / 595,848.
- 2026-09-22 — **Counties are assigned whole, and straddling is reported rather than forced.** Each
  county goes to the band containing the acreage-weighted median latitude of its own almond fields.
  Total straddling acreage is 23,998 ac, **1.59% of the state**; three counties straddle by more
  than 5% of their own acreage — **Sacramento 15.1%** (722 of 4,780 ac), **Fresno 5.5%** (14,896 of
  272,035) and **Madera 5.1%** (7,799 of 154,400). Sacramento and San Joaquin counties interlock
  across the Delta and **no latitude separates them cleanly**; that is the geography, not a defect
  of the rule, and it is stated in §5.1a rather than hidden. Six almond counties lie outside the
  Central Valley (Lake, Calaveras, Contra Costa, Alameda, San Luis Obispo, Riverside) and are
  assigned by the same rule rather than special-cased; together 6,409 ac, 0.42% of the total.
- 2026-09-22 — **Assignment stays at county level, never at field level.** Federal crop insurance is
  administered county by county, so a stratum that cannot be written as a county list cannot be
  mapped onto the program by the audience for this document. The latitude rule *derives* the list;
  the frozen list in `notebooks/common.py` is what the study uses, and Step 1 re-derives it from the
  rule on every run and raises if the two have drifted apart. **Sacramento Valley therefore stays
  county-defined**, with DWR's published `HYDRO_RGN` = "Sacramento River" kept as the stated
  sensitivity: 7,279 units / 288,723 ac against 7,366 / 292,322, a difference of 87 units and 3,599 ac, **1.2%
  of the region**.
- 2026-09-22 — **Stratification sensitivity added to §6 Step 4.** Each boundary is moved by one
  county in each direction, giving four alternative schemes — Solano to San Joaquin north; San
  Joaquin county to Sacramento Valley; Madera to San Joaquin south; Fresno to San Joaquin north.
  "One county" means the adjacent county by median latitude holding at least 1% of state almond
  acreage, so the test is not decided by a 200-acre county. The per-unit region under each scheme
  is written in Step 1 (`region_b1_up` and the rest) so Step 4 reports the sensitivity without
  rebuilding the units. **If the results do not move, that is to be stated plainly:** it would mean
  the stratification is a reporting convenience rather than a physical control, which changes how
  Step 5 must be read, since a per-region bias correction fitted on strata that do not matter is
  fitting noise.
- 2026-09-22 — **The Earth Engine asset was rebuilt carrying source attributes only.** The first
  upload stored `study_region`, which the redefinition above made stale within a day. An asset
  carrying a stale derived stratum is precisely the believable-but-wrong value §8 item 10 is about,
  so `study_region` was dropped: the asset holds `UniqueID`, `ACRES`, `COUNTY`, `HYDRO_RGN`,
  `is_unit` and `YR_PLANTED`, and region is applied at use time by filtering on `COUNTY` against
  the frozen county list. This also means a change of stratification no longer requires a re-upload.
- 2026-09-22 — **Step 1 re-run on the statewide unit set; the CDL comparison numbers moved and are
  restated rather than left.** The 14-county figures quoted before the redefinition (1,370,038 CDL
  acres against 1,116,227 DWR, a 254,000-acre gap) covered 73% of the crop and are superseded.
  Statewide, over all 24 almond counties: **CDL calls 1,849,423 acres almonds against 1,508,863
  from DWR, +23%, a gap of 340,560 acres.** Direction 1 (DWR unit area CDL agrees is almond)
  **85.1%**; direction 2 (CDL almond area inside a DWR almond unit) **69.5%**. Both are within
  half a point of the 14-county values, so the agreement result is a property of the two products
  and not of the county subset. Those counties hold 98.7% of CDL's statewide almond area, so this
  is effectively the statewide comparison.
- 2026-09-22 — Widening the footprint also widened the station set: **82 of 276 CIMIS stations now
  sit within 10 km of almond acreage** (was 60) and **55 nominally operated in 2015–2025** (was
  38). Unit-to-nearest-station distance is essentially unchanged — median 14.4 km against 14.7 km
  on the operating set — so the extra acreage is no better served than the original strata, and
  the K3 test still has real variation to work with.
