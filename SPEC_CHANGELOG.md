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
- 2026-09-22 — **§5.2a added: the unit is smaller than the pixel, and it reframes the comparison.**
  A 1 km pixel is 247 acres; the median almond unit is 22–37 acres by stratum, about a tenth of a
  MODIS or VIIRS pixel. **No 1 km product resolves a single orchard**, so every per-unit LST value
  is a neighbourhood value containing many fields, and every downstream result is conditioned on
  it. Step 1 now reports the share of units smaller than one pixel of each product, and §8 requires
  that distribution in **§2 of the exhibit**, stated before any accuracy figure rather than after.
- 2026-09-22 — **§6 Step 4 must report two findings, not one ranking.** VIIRS and MODIS against
  **Daymet** is a 1 km-to-1 km comparison in which **no resolution advantage exists**; the only
  available claim is that the satellite measures where Daymet interpolates — and interpolates from
  the same sparse network the satellite is being tested against. Against **PRISM and gridMET
  (4 km) and ERA5-Land (~11 km)** a resolution advantage is genuinely available. Beating PRISM
  could be resolution; beating Daymet cannot be. Merging them into a single league table would
  hide which mechanism is doing the work, so §5 must keep them separate.
- 2026-09-22 — **§6 Step 6 renamed** from "Within-orchard structure" to "Neighbourhood-scale
  spatial structure, and whether it repeats." The old title claimed a footprint the sensors do not
  have. The test itself is unchanged and still right — cold-air pooling operates at roughly the
  scale a 1 km pixel resolves — but nothing at 1 km may be described as resolving variation inside
  an orchard. **ECOSTRESS at ~70 m is the only sensor here that resolves a single orchard**, which
  raises its value in the study: it is the only instrument that can show what the 1 km products
  are averaging over.
- 2026-09-22 — **§10 Open items added**, carrying the fourth "outside Central Valley" stratum (six
  counties, 6,409 acres, 0.42%; recommendation is to leave them folded in and report their
  contribution) and the compute-footprint estimate required before Step 6, now that the unit set
  has grown to 39,102 units statewide. The asset-count question is closed there: 45,404 features
  = 39,102 units plus 6,302 fields below the 5-acre cut carried with `is_unit = 0`, printed and
  asserted in Step 1.
- 2026-09-22 — **Step 2 scope: daily only, hourly deferred.** §5.4 asks for hourly and daily air
  temperature. A frost night is defined from the daily minimum, and hourly is needed only once the
  frost nights are known — at satellite overpass time in Step 4 and across the night in Step 7 —
  so Step 2 pulls `day-air-tmp-min` for the whole window and hourly is pulled for the identified
  nights instead. Pulling hourly for every night 2015–2025 would be roughly 1.2 million records,
  mostly warm nights nobody will look at. 63 stations within 20 km of almond acreage, 33 requests,
  31,746 station-nights returned of a theoretical 41,076 (77.3%; the gap is stations not yet
  connected or already disconnected within the window).
- 2026-09-22 — **CIMIS QC flags: a trap that would have removed the study's own subject.** Flag
  meanings were taken from DWR's published *Current Flags* document, not assumed. It splits flags
  into **severe** (`I` no meaning, `M` missing, `S` sensor out of service or out of threshold) and
  **informative**, which includes `R` "data is far out of historical limits" and `Y` "data is
  moderately out of historical limits". **`Y` and `R` are historical-limit tests, so they fire
  precisely because a night was extreme.** Unflagged station-nights are at or below 0 °C 7.7% of
  the time; `Y`-flagged ones 44.2% and `R`-flagged 54.3%. Dropping all flagged data — the obvious
  conservative choice — would have removed **20% of frost nights at 0 °C and 46% at −2.2 °C**.
  Adopted rule: drop severe flags only (they carry no value at all; all 387 of them are null), keep
  `Y` and `R` with a `flagged` column, and report the flagged share alongside every frost-night
  count. This belongs in the exhibit's §9 QC-flag requirement.
- 2026-09-22 — **K1 PASSES at all three thresholds**, and not marginally: 2,910 usable frost
  station-nights at 0 °C, 1,472 at −1.1 °C and **687 at −2.2 °C — 3.4× the 200 minimum**, spread
  over 54 stations and 10 seasons. Sample size is not the constraint on this study. The binding
  number will be how many of those nights a satellite actually saw, which Step 3 tests.
- 2026-09-22 — Step 2 results: frost nights are **overwhelmingly a February phenomenon** (2,299 of
  2,910 at 0 °C, a 15.4% nightly rate in February against 3.7% in March), and the interannual
  spread is a **factor of 14** — 571 frost station-nights in 2018 against 40 in 2024 — on an
  observing network stable at 2,553–3,220 station-nights per season, so the spread is weather and
  not a changing denominator. Eight multi-night widespread events were identified (≥75% of
  observing stations at or below 0 °C); the largest is **20–24 February 2018**, five consecutive
  nights peaking at 49 of 50 stations and −8.0 °C, followed by **24–26 February 2022** and
  **6–7 February 2019**. Station extremes are concentrated — the 12 coldest station-nights come
  from 5 stations — so per-station minima are reported alongside the event view, since a single
  station's minimum is a siting statement as much as a climate one.
- 2026-09-23 — **§8 item 10 gains a fifth category: a filter that removes the phenomenon.** The
  first three are data returning a believable wrong value; the fourth is verification returning a
  believable pass; the fifth is a filter that **looks like good hygiene and removes the thing being
  measured**, and it is the most dangerous of the five because applying it is a choice a reviewer
  would praise. The case is the Step 2 CIMIS QC flags: `Y` and `R` are historical-limit tests, so
  they fire because the night was extreme — 7.7% of unflagged station-nights are at or below 0 °C
  against **44.2% of `Y`-flagged and 54.3% of `R`-flagged** — and screening on them would have
  removed **20.2% of frost nights at 0 °C and 46.1% at −2.2 °C**. **Generalisation stated
  explicitly: any quality filter whose trigger correlates with the signal biases the result, and in
  an index-insurance context the direction is knowable in advance — toward understating tail
  frequency, which is a mispricing rather than a data-cleaning choice.** Approved by user, who
  called it the strongest result either project has produced.
- 2026-09-23 — **§9 gains the matching rule:** every filter applied anywhere in this study must
  report what it removed **and whether what it removed differs from what it kept** — the
  distribution, not the count alone. Applies to QC flags, cloud masks, outlier screens and
  minimum-observation cutoffs alike.
- 2026-09-23 — **§9 gains the frost-versus-bloom limitation, recorded before Step 3.** Frost is
  concentrated in February (2,299 of 2,910 nights at or below 0 °C; 15.4% nightly against 3.7% in
  March) while almond bloom typically begins mid-February, so a meaningful share of the calendar's
  frost nights fall before bloom, when the trees are dormant and the same temperature causes no
  loss. Not a defect — the study measures hazard and deliberately does not model damage — but it
  must be stated, because a reader will otherwise take the night count for a loss-relevant count.
  **The calendar counts frost nights, not damaging nights; mapping the two requires bloom-stage
  data this study does not use.**
- 2026-09-23 — **§5.2 gains a sensor-by-event coverage table**, with collection start dates read
  from Earth Engine rather than memory: MODIS Terra 2000-02-24, Aqua 2002-07-04, VIIRS 2012-01-19,
  ECOSTRESS 2018-07-09, GOES-18 **2022-05-11**. Against the eight widespread events from Step 2:
  Terra, Aqua and VIIRS see 8 of 8; ECOSTRESS 7 of 8; **GOES-18 only 3 of 8**. **The largest freeze
  in the record — 20–24 February 2018, five consecutive nights at up to 49 of 50 stations,
  −8.0 °C — is observable by three of the five sensors**, ECOSTRESS missing it by five months and
  GOES-18 by four years. Note GOES-18 does **not** cover February 2022, contrary to a reading of
  "2022 onward": its three reachable events are all single nights in February 2023.
- 2026-09-23 — **§6 Step 7 REDEFINED, urgently rather than cosmetically.** As written it ran on the
  Step 2 major events, of which GOES-18 can see three, all single nights — too thin for the timing
  analysis. Redefined to use **every frost night in 2023–2025 meeting a stated radiative-cooling
  condition** (station-night at or below 0 °C, plus the clear-sky criterion Step 3 establishes),
  since the timing question needs a clear calm cooling night rather than a valley-wide freeze.
  Counted from the calendar before the clear-sky criterion: the GOES-18 era holds 7,783 usable
  station-nights, **606 at or below 0 °C over 64 distinct dates** (37 in 2023, 10 in 2024, 17 in
  2025); 281 over 42 dates at −1.1 °C; 127 over 22 dates at −2.2 °C. Step 7 must report how many
  nights survive the clear-sky criterion **before** running, and say so plainly if the count is
  small.
- 2026-09-23 — Both Step 2 scope decisions confirmed by user and logged with numbers. **Hourly
  deferred**: pulled for the identified frost nights only, not the whole window. **20 km station
  radius**: 63 stations against 55 at 10 km, farthest selected 19.7 km, and the median
  unit-to-nearest-station distance barely moves (14.4 km against 14.7 km on the operating set), so
  K3's spread survives the wider radius.
- 2026-09-23 — **Step 3 complete. K4 does not fire for the polar orbiters; the bias runs in our
  favour**, as the physics predicts. Usable retrievals on frost nights against ordinary nights:
  **VIIRS 87.0% vs 56.8% (1.53×), Aqua 56.3% vs 34.5% (1.63×), Terra 56.1% vs 31.1% (1.80×),
  at least one polar orbiter 92.0% vs 62.7%.** The advantage holds or grows at colder thresholds
  (any-polar 93.8% at −1.1 °C, 93.3% at −2.2 °C) and in every individual season. Sample carried
  into Step 4: at 0 °C, VIIRS 2,532, Aqua 1,638, Terra 1,633, any 2,676; the smallest cell
  anywhere is Terra at −2.2 °C with 361, still above the K1 minimum of 200. **The study survives
  the step most likely to kill it.**
- 2026-09-23 — **K4 does fire for ECOSTRESS, orbitally rather than through cloud, and the deficit
  was decomposed rather than reported as a rate.** ECOSTRESS is usable on 0.5% of frost nights
  against 6.0% of ordinary ones (0.09×). A night scene existed somewhere on 44.5% of frost nights
  against 48.4% of ordinary ones — essentially equal — so the deficit is not about acquisitions.
  It is entirely in whether the swath covered the station: **0.52% against 6.27%, a factor of 12**.
  Given the station *was* in swath, the QC screen passed **100% of frost nights against 95.5% of
  ordinary ones**, so the screen behaves as physics predicts and is not the cause. **Only 10 frost
  station-nights in seven seasons put a station inside an ECOSTRESS night swath.** That is a
  sampling property of the ISS orbit, not a sensor failure; ECOSTRESS remains a case-study sensor
  and cannot carry Step 4 or the station side of Step 6.
- 2026-09-23 — **Three extraction traps hit in Step 3, each producing a believable wrong answer
  rather than an error.** (1) **MODIS masks its `QC_Night` band wherever the value is 0** — that
  is, wherever quality is best. Reading a masked QC as unusable would have discarded two-thirds of
  valid retrievals, the best ones. Verified over a test season: 705 station-nights had LST with QC
  masked, 716 had QC with LST absent, 343 had both, **none had both missing**, and `unmask(0)`
  returned 0 for all 705. VIIRS never masks its `QC`. (2) **`ee.Reducer.first()` names its output
  `first` on a single-band image** but after the band names on a multi-band one; the first
  ECOSTRESS extraction read back the band name, got `None` for every row, and reported **zero
  usable ECOSTRESS observations in every season** — entirely plausible for a sparse ISS sensor and
  very nearly accepted. Caught by checking one scene at one station by hand, where `reduceRegion`
  returned a value `reduceRegions` did not. (3) **GOES `CMI_C13` is a scaled integer with a
  per-image scale and offset** while the catalogue declares its units as K with no scale factor;
  raw values of 1,980–3,218 are obviously not kelvin, but **a guessed ×0.1 gives 198–322 K, a
  believable range that is silently wrong**. The image's own `CMI_C13_scale` 0.06145332 and
  `CMI_C13_offset` 89.62 give 211.3–287.4 K. All three belong in §8 item 10.
- 2026-09-23 — **GOES-18 availability is not comparable with the polar orbiters and §5 must say
  so.** `DQF_C13` is an instrument quality flag, not a cloud mask: a geostationary sensor returns a
  good radiance every night, but on a cloudy night that radiance is the cloud top rather than the
  ground. Its 100% availability figure is near-certain by construction and says nothing about
  whether the surface was visible. It is excluded from Figure 3 for that reason.
- 2026-09-23 — Per the new §9 filter rule, Step 3 reports what each QC screen removed. On frost
  nights the screen discards the "produced but other quality" retrievals — VIIRS 113 of 2,645,
  Aqua 801 of 2,439, Terra 778 of 2,411 — and the removed nights' median tmin (−0.7, −1.3,
  −1.2 °C) sits close to the kept nights' (−1.1, −1.0, −1.1 °C). **The screen is not selecting on
  cold**, unlike the CIMIS flags in Step 2 where it would have been. Reported either way.
- 2026-09-23 — **§1a added: which perils suit satellite index design.** Radiative frost requires
  clear skies, so **satellite availability is positively correlated with the hazard** — VIIRS 87.0%
  on frost nights against 56.8% on ordinary ones, any polar orbiter 92.0% against 62.7%. **That is
  the opposite of flood**, where the storm that caused the peril also closed the sky: the
  strawberry study had no usable optical view of the Pajaro Valley on 11–14 March 2023, the days
  water was at its peak. General rule, and the most transferable finding either study has produced:
  **a peril whose physical signature requires clear skies is observable when it matters; a peril
  carried by cloud is not.** It can be judged before any analysis is commissioned — the question is
  only whether the hazard and the obstruction share a cause. Belongs in §1 of the exhibit and in
  the summary.
- 2026-09-23 — **ECOSTRESS DROPPED from the study.** Kept until now because at ~70 m it was the
  only instrument resolving a single orchard. Evidence, measured: only 10 frost station-nights in
  seven seasons put a station in a night swath; of the eight widespread events, five precede the
  record, eight of the remaining eleven event nights have no night scene intersecting almond
  acreage, two cover a single 6-acre unit, and **18 February 2023 — 41 night scenes whose
  footprints cover 1,939 units and 93,661 acres — contains no data over any of it.** That zero was
  verified three independent ways per the new §9 rule: masked-area sum = 0 acres, 300 sampled unit
  centroids return no raw LST, and the Step 3 station extraction finds 0 of 63 stations with raw
  LST that date while returning 1,474 station-nights with raw LST across the record. **A granule
  footprint is not data coverage** — the same lesson the strawberry Step 1d recorded for
  PlanetScope.
- 2026-09-23 — **§1b added: with ECOSTRESS gone, every participating sensor is 1 km or coarser**,
  the same footprint as Daymet. **This study therefore tests measurement against interpolation,
  not resolution.** Beating PRISM or gridMET at 4 km, or ERA5-Land at ~11 km, is partly a
  resolution effect; **beating Daymet at 1 km cannot be.** Stated before the results, not after.
- 2026-09-23 — **GOES cloud screening settled before Step 7; it is the most dangerous trap in the
  study.** On a cloudy night a geostationary IR sensor returns the cloud-top temperature, colder
  than the surface — so contamination would make GOES appear to see minima the 01:30 polar snapshot
  missed, **which is exactly what Step 7 is looking for**. `DQF_C13` gives no protection: it is an
  instrument flag and reads 0 on 100% of station-nights. **There is no ABI Clear Sky Mask in Earth
  Engine** (only `MCMIP*` and `FDC*`, checked 2026-09-23). **The fire product's cloud flag was
  tested and rejected with numbers:** `NOAA/GOES/18/FDCC` `DQF` = 2 is documented as "invalid due
  to opaque cloud", and over 7,739 station-nights it agrees with the VIIRS clear flag 79.7% overall
  (phi = 0.594) — but **on frost nights it calls only 41.1% clear where VIIRS retrieves usable LST
  on 89.8%**, and on 16 February 2023, a widespread radiative freeze, it flagged 56 of 63 stations
  as opaque cloud. The fire algorithm's IR test mistakes very cold clear land for cloud top, so
  using it would preferentially delete frost nights — **the fifth silent-failure category exactly**.
  Method adopted: screen GOES nights by cross-referencing the polar-orbiter clear flags for the
  same station-night, stated as such in §9.
- 2026-09-23 — **§6 Step 7 gains a mandatory falsification check**, reported whether or not it
  fires: if GOES's apparent extra cooling is cloud, it must correlate with cloud indicators and be
  largest on nights the polar orbiters flag as unclear. A dirty result means the timing finding is
  an artefact and must be stated as the result rather than worked around.
- 2026-09-23 — **§8 item 10 gains entries 4 and 5, and the scaling pattern becomes a rule.**
  (4) **A mask that encodes "good" as "absent"** — MODIS masks `QC_Night` where the value is 0,
  which is "good quality", so the cautious reading throws away the best retrievals and keeps the
  second-best; VIIRS, from the same provider family, never masks its `QC`. (5) **A sparse sensor
  makes a plausible zero** — a reducer-output-name bug reported zero usable ECOSTRESS observations
  in every season, indistinguishable from the sparsity expected of an ISS-orbit sensor, and caught
  only by hand-checking one scene against a second method. **The scaling pattern is now three
  independent instances** — CPC 0.1 mm/day, VIIRS with no scale factor where MODIS carries 0.02,
  and GOES `CMI_C13` needing a per-image scale and offset the catalogue does not mention — so it is
  stated as a rule: **never infer a scale factor from the plausibility of the result.** The GOES
  case is the sharpest: **x0.1 gives 198–322 K, inside the believable range and wrong**, against
  211.3–287.4 K from the image's own properties.
- 2026-09-23 — **§9 gains the zero rule:** any result of zero, none or empty must be verified by an
  independent method before it is accepted, especially where zero is the expected answer. A sparse
  sensor, a rare event and a broken extraction all return nothing, and nothing looks the same in
  all three cases.
- 2026-09-23 — **Step 4 complete. K2 FIRES.** On the 2,532 frost station-nights VIIRS can see,
  bias-corrected per region and year and fitted leave-one-station-out, median absolute error is
  **PRISM 0.72 °C, gridMET 0.85, Daymet 1.03, VIIRS 1.19, ERA5-Land 1.41.** The satellite is worse
  than the best grid by 0.47 °C, 65% larger, and worse on RMSE and on the width of the central 90%
  of its error distribution. The ordering holds at all three thresholds, for Aqua (1.24) and Terra
  (1.23) on their own matched subsets, and in all three strata. **The only product any satellite
  beats is ERA5-Land at ~11 km.**
- 2026-09-23 — **The two §5.2a findings, kept apart.** (1) Against **Daymet at the same 1 km
  footprint**, where no resolution advantage exists, Daymet 1.03 against VIIRS 1.19: **interpolation
  beats measurement at equal footprint**, and Daymet interpolates from the same sparse network the
  satellite is being judged against. (2) Against the **coarser** grids, where a resolution advantage
  was available, PRISM at 4 km scores 0.72 against VIIRS at 1 km: the satellite did not realise it,
  and the coarser product is the more accurate one, so nothing here is explained by pixel size.
- 2026-09-23 — **A tail advantage that turned out to be an artefact, recorded because it nearly
  stood.** Scored on every night each product has a value, VIIRS appeared to have tighter tails
  than the grids on the coldest nights — RMSE 2.39 against PRISM 3.10 at −2.2 °C — which would have
  been a real finding for insurance, where tails matter more than medians. **It is an artefact of
  comparing different subsets of weather**: a satellite is only scored on nights it could see. On
  the matched subset PRISM is 2.28 and Daymet 2.29 against VIIRS 2.39 and the advantage disappears.
  Every head-to-head in Step 4 is therefore run on identical station-nights, with the unmatched
  version shown only to expose the distortion.
- 2026-09-23 — **Day alignment tested rather than assumed.** PRISM assets are timestamped noon UTC
  and each provider defines its 24-hour window differently, while CIMIS `DayAirTmpMin` is the local
  calendar day. Each grid was matched at offsets −1, 0 and +1: **all four minimise error at offset
  0** (PRISM 0.94 against 1.50 and 1.96; Daymet 1.54 against 2.18 and 2.14; gridMET 1.25 against
  1.75 and 2.15; ERA5-Land 1.95 against 2.61 and 2.52), so no shift is applied. ERA5-Land is built
  from hourly data over 08:00 UTC to 08:00 UTC, matching the local calendar day by construction.
- 2026-09-23 — **Bias correction is fitted leave-one-station-out**, not in-sample. Fitting an
  offset on a region-year and scoring the same station-nights with it is self-fitting. The effect
  is small and changes no ranking — VIIRS 1.13 in-sample against 1.19 LOSO, PRISM 0.68 against
  0.72 — but every corrected figure quoted is the LOSO one.
- 2026-09-23 — **Stratification sensitivity (§5.1a) reported: the strata are NOT load-bearing.**
  Under all four alternative schemes, each moving one boundary by one county, the largest movement
  in any product's MdAE is **0.050 °C** and **the ranking is identical in every scheme**. As §5.1a
  required this to be stated either way: regional grouping in this study is a reporting convenience
  rather than a physical control, and §5.4's per-region bias correction must be read in that light —
  a correction fitted on strata that do not matter is largely fitting a single national offset.
