# Project spec: Almond bloom frost — satellite feasibility study

Austin Krawczyk, UC Davis.

Read this file at the start of every session. It is the source of truth for scope.
If a task would take the work outside this spec, stop and ask.

> **Amendment note.** This file is the spec as issued on 2026-09-21, amended on 2026-09-22 with
> five decisions taken after a pre-flight check of every dataset ID (§5 and §6 below, marked
> **AMENDED**). The original wording is preserved in `SPEC_CHANGELOG.md` where it was changed.
> The amendments are in the file rather than only in the changelog so that the spec never
> contradicts the record.

## 1. The question

Can satellite thermal observation measure frost hazard at California almond orchards more
accurately than the gridded weather products an index insurance product would otherwise use?

That is the whole question. This study measures hazard, not loss. It does not attempt to predict
crop damage, does not use yield or claims data, and does not produce a rate. It asks one narrow,
checkable thing: on the nights that matter, does satellite land surface temperature (LST) track
the ground-truth minimum temperature at an orchard better than PRISM, Daymet, gridMET or
ERA5-Land do?

The motivation is the failure mode identified in interviews: gridded products interpolate between
stations and smooth over terrain. Cold air drains downhill and pools in low ground on
radiative-cooling nights, so the coldest orchards are systematically the ones a grid is worst at.
If a satellite that actually observes the surface near the diurnal minimum resolves that
structure, an index built on it would carry less basis risk than one built on a grid. If it does
not, that is equally publishable and far cheaper to learn now.

The agent must not drift from hazard measurement into damage modelling. If a step starts
requiring assumptions about kernel set, bloom stage sensitivity or yield, stop and flag it.

## 2. Scope

| Item | Decision |
|---|---|
| Crop | Almonds |
| Season | Bloom and early nut development, 1 February – 31 March |
| Years | 2015–2025 (11 seasons) |
| Geography | **All** California almond acreage, stratified into three latitude bands (**AMENDED 2026-09-22**, see §5.1a): Sacramento Valley, San Joaquin north, San Joaquin south. The county pairs named in the original spec were illustrations of the north/south split, not a definition, and taking them literally left 26.7% of state almond acreage unassigned for no reason. |
| Orchard units | DWR/Land IQ Statewide Crop Mapping, almond class. Not CDL — see §5.1 |
| Frost nights | Defined from CIMIS station observations, never from satellite. See §5.4 |
| Damage thresholds | Published UC critical temperatures by growth stage, cited, used only as context for which nights are interesting |

Explicitly out of scope: loss data, yield, claims, rating, premium, any product design, any
recommendation about whether RMA should build something. This is a measurement study.

### Why almonds, why bloom

Almonds bloom earlier than any other major California tree crop — mid-February in a normal year —
which puts the most frost-sensitive stage squarely inside the radiative-frost season. The crop has
documented critical temperatures by stage (published by UC Cooperative Extension), which means
"how cold was it" maps to a physically meaningful threshold rather than an arbitrary one. And
almond acreage is large, contiguous and spread across the valley floor and its edges, which gives
real terrain variation to test against.

## 3. Deliverables

- `EXHIBIT.md` — the full write-up: method, results, tables, figures, limitations. Written so a
  reader at RMA or an actuarial consultancy can check every number.
- `SUMMARY.md` — three paragraphs, no more than 1,000 words: what was tested, what was found,
  what it means for an index product.
- `SPEC_CHANGELOG.md` — every deviation from this spec, with the reason.
- Notebooks, one per numbered step in §6, each runnable end to end.
- `data/derived/` — the station-night table, the unit table, the comparison table. CSV,
  documented columns.
- Figures per §7.

### 1a Which perils suit satellite index design (ADDED 2026-09-23)

**State this before the results, not after.** It is the most transferable finding either study in
this programme has produced, and it belongs in §1 of the exhibit and in the summary.

**Radiative frost requires clear skies, so satellite availability is positively correlated with
the hazard.** Measured in Step 3 over 31,359 station-nights: a usable retrieval exists on **87.0%
of frost nights against 56.8% of ordinary nights for VIIRS** (1.53×), 56.3% against 34.5% for
Aqua, 56.1% against 31.1% for Terra, and **92.0% against 62.7% for at least one polar orbiter**.
The advantage holds or grows at colder thresholds and in every one of eleven seasons.

**That is the opposite of flood.** In the strawberry study the peril arrived with the cloud that
caused it: there was no usable optical view of the Pajaro Valley for 11–14 March 2023, the days
water was at its peak, because the storm that broke the levee also closed the sky. The sensor was
blindest exactly when the event was largest.

**The general rule: a peril whose physical signature requires clear skies is observable by
satellite when it matters; a peril carried by cloud is not.** Frost, heat and drought sit on one
side; flood, hail and wind-driven rain sit on the other. **This is a stronger criterion for
choosing which perils to build satellite index products around than any accuracy statistic**, and
it can be evaluated cheaply before any analysis is commissioned — the question is only whether the
hazard and the obstruction share a cause.

### 1b What this study can and cannot test (ADDED 2026-09-23)

**Also state this before the results.** ECOSTRESS has been **dropped** (§5.2): only 10 frost
station-nights in seven seasons put a station inside a night swath, and on the one widespread
event whose scene footprints covered almond acreage, 18 February 2023, there is no data over any
of it — verified three ways. **Every remaining sensor is 1 km or coarser**, which is the same
footprint as Daymet and coarser than nothing in the comparison set. **No participating instrument
resolves a single orchard**, and the one that could does not observe these nights. Combined with §5.2a — the median almond unit is about a tenth of a
1 km pixel — this fixes what the study is actually testing:

**This study tests measurement against interpolation, not resolution.** Beating PRISM or gridMET
at 4 km, or ERA5-Land at ~11 km, is partly a resolution effect. **Beating Daymet at 1 km cannot
be**, because the footprints are identical; there the only available claim is that the satellite
measures where Daymet interpolates — and interpolates from the same sparse station network the
satellite is being judged against. §5 must keep those two comparisons apart.

## 4. Kill criteria

State these in the exhibit whether or not they fire. A negative result is a result; do not rescue
the study.

- **K1.** Fewer than 200 valid station-nights survive cloud screening across all 11 seasons.
  Below that, nothing can be said about skill with any confidence.
- **K2.** Satellite LST does not beat the best gridded product on median absolute error at station
  locations. If a free 4 km grid is as good, a satellite index has no case.
- **K3.** Satellite advantage, where it exists, does not increase with terrain relief or with
  distance from the nearest CIMIS station. If the advantage is uniform it is a calibration offset,
  not resolved structure, and a bias correction on the grid would capture it more cheaply.
- **K4.** Clear-sky sampling is so biased that the nights the satellite sees are not the nights
  that damage crops. Radiative frost nights are clear nights, so this may work in our favour — but
  it must be demonstrated, not assumed.

## 5. Data

Use these exact IDs. If any is deprecated, stop and ask — do not substitute. (The Pajaro study hit
this twice, with PRISM AN81d and 3DEP.)

**All IDs below were verified against the Earth Engine catalogue on 2026-09-22**: the collection
exists, carries the named band, and returns imagery for 1–7 February in every year 2015–2025.
Coverage exceptions found by that check are recorded in the rows themselves.

### 5.1 Orchard units

- DWR Statewide Crop Mapping, almond class, most recent survey year available in the study window.
  Load as an asset if not already in Earth Engine's catalogue.
- USDA CDL (`USDA/NASS/CDL`, almond class 75) as a comparison only, reported alongside. CDL
  misclassified badly in the strawberry study; do not use it as the unit definition.
- Units: fields ≥ 5 acres, to avoid edge pixels dominating.

### 5.1a Regions (AMENDED 2026-09-22)

**Every county with almond acreage is assigned. Coverage is 100%, not 73%.**

The strata are defined by two latitude boundaries, placed to fall *between* counties rather than
through them, and chosen as the local minima of total almond acreage landing on the wrong side:

| Boundary | Latitude | Separates |
|---|---|---|
| 1 | **38.25 N** | Sacramento Valley │ San Joaquin north |
| 2 | **36.82 N** | San Joaquin north │ San Joaquin south |

A county is assigned whole, by the **acreage-weighted median latitude of its own almond fields**.
Assignment is at county level and never at field level, because **federal crop insurance is
administered county by county**: a stratum that cannot be written as a county list cannot be
mapped onto the program by the audience for this document. The latitude rule is how the list is
*derived*; the list itself is what the study uses, and it is frozen in `notebooks/common.py` and
re-checked against the rule at every run.

**Counties that straddle their boundary are reported, not forced.** At these boundaries three do
so by more than 5% of their own almond acreage: **Sacramento 15.1%** (722 of 4,780 acres),
**Fresno 5.5%** (14,896 of 272,035) and **Madera 5.1%** (7,799 of 154,400). Total straddling
acreage is 23,998 acres, **1.59% of the state**. Sacramento and San Joaquin counties interlock
across the Delta and no latitude separates them cleanly; that is a property of the geography, not
a defect of the rule, and it is stated rather than hidden.

**Six counties with almond acreage sit outside the Central Valley** (Lake, Calaveras, Contra
Costa, Alameda, San Luis Obispo, Riverside). They are assigned by the same rule rather than
special-cased. Together they hold 6,409 acres, **0.42%** of the assigned total.

**Sensitivity, carried into Step 4 and reported there.** Each boundary is moved by one county in
each direction, giving four alternative stratifications; "one county" means the adjacent county by
median latitude holding at least 1% of state almond acreage, so the test is not decided by a
200-acre county. The four are: Solano to San Joaquin north; San Joaquin county to Sacramento
Valley; Madera to San Joaquin south; Fresno to San Joaquin north. The per-unit region under each
scheme is written in Step 1 so Step 4 can report the sensitivity without rebuilding the units.
**If the Step 4 results do not move, say so plainly:** it would mean the stratification is not
load-bearing — that regional grouping is a reporting convenience rather than a physical control
— and that changes how Step 5 must be read, because a regional bias correction fitted on strata
that do not matter is fitting noise.

### 5.2 Satellite thermal — the candidates

All are night-time observations; daytime LST is irrelevant to frost.

| Product | Earth Engine ID | Band | Resolution | Role |
|---|---|---|---|---|
| **VIIRS LST — PRIMARY** | `NASA/VIIRS/002/VNP21A1N` | `LST_1KM` | 1 km | Primary polar orbiter (**AMENDED**) |
| MODIS Aqua night LST | `MODIS/061/MYD11A1` | `LST_Night_1km` | 1 km | Full candidate, plus the drift experiment (**AMENDED**) |
| MODIS Terra night LST | `MODIS/061/MOD11A1` | `LST_Night_1km` | 1 km | Candidate; too early in the night |
| GOES-18 ABI | `NOAA/GOES/18/MCMIPC` | `CMI_C13`, `CMI_C14` | 2 km | **Timing instrument only**, Step 7 (**AMENDED**) |
| ECOSTRESS | `NASA/ECOSTRESS/L2T_LSTE/V2` | `LST` | ~70 m | **DROPPED 2026-09-23** — see below |

**Units and scale, read from the published band documentation, not from memory:**

- MODIS `LST_Night_1km`: Kelvin, **scale 0.02**. Multiply by 0.02, then subtract 273.15.
- VIIRS `LST_1KM`: Kelvin, **no scale factor**. Verified against raw values (274–278 K over
  Fresno in February). **Applying the MODIS recipe to VIIRS would give about −268 °C.**
- GOES `CMI_C13`/`CMI_C14`: Kelvin, no scale. These are **top-of-atmosphere brightness
  temperature**, not LST — see the Step 7 note.
- PRISM `tmin`, Daymet `tmin`: °C. gridMET `tmmn`, ERA5-Land `temperature_2m`: Kelvin.

**AMENDED 2026-09-22 — VIIRS is primary, not Aqua.** The original spec named Aqua primary at
"~01:30 local". Measured night overpass time over Fresno in February, from each product's own
view-time band, is:

| | 2015 | 2020 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| Aqua | 02:03 | 02:01 | 02:04 | 02:11 | 02:29 | **03:16** |
| Terra | 22:11 | 22:08 | 21:53 | 21:39 | 21:26 | 21:16 |
| VIIRS | 01:49 | 01:36 | 01:35 | 01:44 | 01:29 | 01:39 |

Aqua was never at 01:30 and has drifted more than an hour later since 2022; Terra has drifted
earlier. **VIIRS is the only product holding near 01:30 across all eleven seasons**, so it is the
primary. Aqua remains a full candidate, not a footnote.

**AMENDED — Aqua's drift is a designed experiment, not a nuisance.** See §6 Step 4b.

**AMENDED — GOES-18 only, and timing only.** Two reasons, both checked rather than assumed:

1. *Coverage.* GOES-18 ABI over California begins in 2023 (3 of 11 seasons). GOES-17 covers
   2019–2022, but its loop heat pipe under-performed and its infrared detectors warmed near
   satellite midnight. Tested on **every February night** over a Central Valley box at 12Z and
   14Z (04:00 and 06:00 PST — the pre-dawn minimum), using the product's own `DQF_C13` flag,
   with no slots missing:

   | GOES-17, February | 04:00 PST | 06:00 PST |
   |---|---|---|
   | **2019 (control)** | **0 of 28 unusable** | **0 of 28 unusable** |
   | 2020 | 11 of 28 (39%) | 12 of 28 (43%) |
   | 2021 | 8 of 28 (29%) | 11 of 28 (39%) |
   | 2022 | 8 of 28 (29%) | 13 of 28 (46%) |

   "Unusable" means the scene is essentially wholly flagged (under 5% of valley pixels good).
   Across 2020–2022, **63 of 168 pre-dawn scenes are unusable (37.5%)**, against **0 of 56 in
   2019** and **0 of 165 for GOES-18 in 2023–2025**. The clean 2019 control is what separates an
   instrument fault from a screening artefact: the same code, the same box, the same hours, and
   the same flag give a clean year before the degradation and a degraded one after. GOES-17 is
   therefore not used. GOES-16 is not used
   either: its eastern view angle over California adds a path-length problem on top of the
   atmospheric one. **State in the exhibit that ABI continuity for night thermal work in
   California effectively begins in 2023.**
2. *Brightness temperature.* `CMI_C13`/`C14` are TOA brightness temperatures. A per-region bias
   correction cannot absorb a water-vapour-dependent offset, so **GOES is removed from the Step 4
   accuracy comparison entirely.** It is a timing instrument: Step 7 uses the *shape* of the
   cooling curve and the *offset* between the 01:30 reading and the observed minimum, where
   within-night differencing largely cancels the atmospheric term. This is a **stated design
   limit in §9, not a caveat.**

**Landsat thermal is excluded.** Its overpass is ~10:00 local. It cannot see a frost night. State
the exclusion in the exhibit.

**ECOSTRESS** is the high-resolution wildcard; 70 m would resolve cold pools directly. It is in
the Earth Engine catalogue as `NASA/ECOSTRESS/L2T_LSTE/V2` (no ORNL DAAC download needed), with
data from **9 July 2018**, so it has bloom seasons **2019–2025**. Its problem is revisit: the ISS
orbit precesses, so night-time acquisitions over a given orchard on a given frost night are rare.
Treat it as a **case-study sensor** — find the handful of nights where an ECOSTRESS night scene
coincides with a CIMIS frost night, and use those as a spatial-structure demonstration, not as a
statistical comparison.

**Which sensor can see which event (ADDED 2026-09-23).** Collection start dates are read from
Earth Engine, not from memory. The eight widespread freeze events are from Step 2.

| Sensor | Collection begins | Events observable |
|---|---|---|
| MODIS Terra `MOD11A1` | 2000-02-24 | 8 of 8 |
| MODIS Aqua `MYD11A1` | 2002-07-04 | 8 of 8 |
| VIIRS `VNP21A1N` | 2012-01-19 | 8 of 8 |
| ECOSTRESS `L2T_LSTE/V2` | 2018-07-09 | 7 of 8 by date, **0 of 8 with data over almond acreage** |
| GOES-18 `MCMIPC` | 2022-05-11 | 3 of 8 |

| Event | Nights | Peak stations | Coldest | Terra | Aqua | VIIRS | ECOSTRESS | GOES-18 |
|---|---|---|---|---|---|---|---|---|
| **20–24 Feb 2018** | 5 | 49 of 50 | −8.0 °C | ✓ | ✓ | ✓ | — | — |
| 6–7 Feb 2019 | 2 | 39 | −4.9 °C | ✓ | ✓ | ✓ | ✓ | — |
| 23 Feb 2019 | 1 | 41 | −4.4 °C | ✓ | ✓ | ✓ | ✓ | — |
| 6 Feb 2022 | 1 | 35 | −4.3 °C | ✓ | ✓ | ✓ | ✓ | — |
| 24–26 Feb 2022 | 3 | 44 | −6.4 °C | ✓ | ✓ | ✓ | ✓ | — |
| 1 Feb 2023 | 1 | 36 | −4.2 °C | ✓ | ✓ | ✓ | ✓ | ✓ |
| 16 Feb 2023 | 1 | 36 | −5.1 °C | ✓ | ✓ | ✓ | ✓ | ✓ |
| 18 Feb 2023 | 1 | 38 | −4.3 °C | ✓ | ✓ | ✓ | ✓ | ✓ |

**The largest freeze in the record — 20–24 February 2018, five consecutive nights at up to 49 of
50 stations — is observable by three of the five sensors.** ECOSTRESS misses it by five months and
GOES-18 by four years. Note also that **GOES-18 does not cover February 2022**: its collection
begins in May 2022, so the three events it can see are all single nights in February 2023. This
is the constraint that forced the Step 7 redefinition below, and it belongs in §5 of the exhibit
as part of the sensor-availability argument.

**ECOSTRESS is dropped from the study (2026-09-23).** It was kept as a case-study sensor because
at ~70 m it is the only instrument here that resolves a single orchard. It cannot deliver even
that, and the evidence is measured rather than inferred:

- **At stations:** only **10 frost station-nights in seven seasons** put a station inside a night
  swath (Step 3). The deficit is orbital, not cloud — a night scene existed on 44.5% of frost
  nights against 48.4% of ordinary ones, and given the station *was* in swath the QC screen passed
  100% of frost nights.
- **Over almond acreage on the eight widespread events:** five event nights precede the record
  (February 2018; the collection begins 2018-07-09). Of the eleven remaining event nights, **eight
  have no night scene intersecting almond acreage at all**, two put a footprint over a single
  6-acre unit, and one — **18 February 2023** — looked promising with 41 night scenes whose
  footprints covered 1,939 units and 93,661 acres.
- **That one night contains no data over any of it.** Verified three independent ways, per the §9
  zero rule: the masked-area sum over those units is 0 acres; 300 sampled unit centroids return no
  raw LST; and the Step 3 station extraction independently finds 0 of 63 stations with raw LST on
  that date. The same extraction returns 1,474 station-nights with raw LST across the record and
  up to 60 stations in swath on other dates, so the method works and the zero is real.

**A granule footprint is not data coverage.** ECOSTRESS L2T footprints are far larger than the
area actually filled, so 41 scenes "covering" 93,661 acres cover none of it. That is the same
lesson the strawberry study's Step 1d recorded for PlanetScope — catalogue coverage metadata
overstates usable observation — and it should be stated once, generally, in the exhibit.

**Consequence, which belongs in §1b and before the results:** with ECOSTRESS gone, **every
participating sensor is 1 km or coarser.**

**GOES cloud screening, required before Step 7 (ADDED 2026-09-23). This is the most dangerous
trap in the study.** On a cloudy night a geostationary infrared sensor returns the **cloud-top**
brightness temperature, which is colder than the surface and often far colder. Cloud contamination
would therefore make GOES appear to see minima the 01:30 polar snapshot missed — **which is
precisely the finding Step 7 is looking for.** An unscreened run could produce a spectacular,
publishable and entirely spurious result. `DQF_C13` does not protect against this: it is an
*instrument* quality flag, and it reads 0 ("Good pixels") on 100% of station-nights.

**There is no ABI Clear Sky Mask (ACM) in Earth Engine.** The catalogue carries only `MCMIP*`
(cloud and moisture imagery) and `FDC*` (fire detection) for GOES-16/17/18/19; checked
2026-09-23.

**The fire product's cloud flag was tested and rejected, with numbers.** `NOAA/GOES/18/FDCC` has
a `DQF` band documented as `0` good-quality fire, `1` good-quality fire-free land, `2` **invalid
due to opaque cloud**. Over 7,739 station-nights in 2023–2025 it agrees with the VIIRS clear flag
79.7% of the time overall (φ = 0.594) — but **on frost nights it calls only 41.1% clear where
VIIRS retrieves usable LST on 89.8%.** On 16 February 2023, a widespread radiative freeze that
must have been clear, FDCC flagged 56 of 63 stations as opaque cloud. The fire algorithm's
infrared cloud test evidently mistakes a very cold clear land surface for a cloud top. **Using it
would preferentially delete frost nights — the fifth silent-failure category exactly, a screen
whose trigger correlates with the signal.** FDCC `DQF` is therefore not used as a cloud mask, and
the measured reason is recorded rather than the tool being quietly dropped.

**Method adopted:** GOES nights are screened by **cross-referencing the polar-orbiter clear flags
for the same station-night** (VIIRS `QC` bits 0–1 = 0, MODIS `QC_Night` bits 0–1 = 0). §9 must
state plainly that `DQF_C13` is an instrument flag and that GOES cloud screening came from
another sensor entirely.

### 5.2a The unit is smaller than the pixel (ADDED 2026-09-22)

**This reframes the whole comparison and must be read before §5.3.**

A 1 km pixel is 247 acres. The median almond unit is 22–37 acres depending on stratum, about **a
tenth of a MODIS or VIIRS pixel**. **No 1 km product resolves a single orchard.** Every per-unit
LST value in this study is therefore a *neighbourhood* value covering many fields, and every
result downstream is conditioned on that. Step 1 reports the distribution explicitly: the share of
units smaller than one pixel of each product, which belongs in §2 of the exhibit for exactly this
reason.

**Two distinct findings, never one ranking.** The candidates do not all differ from the satellite
in the same way, so a single league table would hide the mechanism:

| Comparison | Pixel | Is a resolution advantage available? |
|---|---|---|
| VIIRS / MODIS **vs Daymet** | 1 km vs 1 km | **No.** Same footprint. |
| VIIRS / MODIS **vs PRISM, gridMET** | 1 km vs 4 km | Yes |
| VIIRS / MODIS **vs ERA5-Land** | 1 km vs ~11 km | Yes, large |

**Against Daymet the satellite has no resolution advantage at all.** Its only claim there is that
it **measures rather than interpolates** — Daymet's 1 km field is interpolated from the same sparse
station network the satellite is being tested against, so beating it would be a statement about
measurement versus interpolation at a fixed footprint. **Beating PRISM could be resolution;
beating Daymet cannot be.** Step 4 must report these as two separate findings and say which
mechanism each supports. A result that beats PRISM and gridMET but not Daymet means the gain is
resolution, not measurement, and would not survive a denser interpolation network.

**ECOSTRESS at ~70 m is the only sensor here that resolves a single orchard**, which raises its
value in the study well above "case-study colour". It is the only instrument that can show what
the 1 km products are averaging over.

### 5.3 Gridded baselines — what the satellite has to beat

| Product | Earth Engine ID | Resolution | Variable | Units |
|---|---|---|---|---|
| PRISM daily | `OREGONSTATE/PRISM/ANd` | 4 km | `tmin` | °C |
| Daymet V4 | `NASA/ORNL/DAYMET_V4` | 1 km | `tmin` | °C |
| gridMET | `IDAHO_EPSCOR/GRIDMET` | ~4 km | `tmmn` | K |
| ERA5-Land | `ECMWF/ERA5_LAND/HOURLY` | ~11 km | `temperature_2m` | K |

Note the deprecated ID. `OREGONSTATE/PRISM/AN81d` ends in 2020 and will not cover this window.
Use `ANd`.

### 5.3a Which products ingest CIMIS — the circularity in K2 (ADDED 2026-09-23)

**The accuracy comparison at station locations is not a fair test between a product fitted to
those stations and one that has never seen them.** Two of the four gridded baselines are
interpolated from a station network that includes CIMIS; the satellites have never seen a CIMIS
observation. Verified against primary documentation, not asserted:

| product | ingests CIMIS? | evidence |
|---|---|---|
| **PRISM `ANd`** | **YES** | PRISM's own *PRISM Datasets* documentation, Table A1, lists **CIMIS — "California Irrigation Management Information System, operated by Univ. California, Davis"** with **`Norm91m, AN91m, AN91d`** in the Tmax/Tmin column. `AN91d` is the daily AN product, which is exactly `OREGONSTATE/PRISM/ANd`. The same document states that AN "includes several networks that have stations sited in irrigated fields (e.g., AGRIMET, CIMIS, COAGMET)… not used in LT, because they do not represent natural climatic variations, but… used in AN". |
| **gridMET** | **YES, inherited** | Climatology Lab: gridMET "blends spatial attributes of gridded climate data from PRISM with desirable temporal attributes… from regional reanalysis (NLDAS-2)", and "daily gridMET temperature and precipitation data now make use of daily PRISM maximum temperature, minimum temperature and precipitation that have been bias corrected". |
| **Daymet V4** | **NO** | ORNL DAAC: Daymet's core input is "daily observations of minimum temperature, maximum temperature, and precipitation… obtained from the NOAA National Centers for Environmental Information's Global Historical Climatology Network (GHCN)-Daily data set". **CIMIS is not a GHCN-Daily source**: the GHCN-D readme's complete source-flag list contains no CIMIS or California agricultural network, and none of the 3,241 GHCN-D stations in California is named CIMIS. Empirically, the median distance from each of the 63 CIMIS stations to the nearest GHCN-D station is **5,604 m**, with only 1 of 63 within 200 m and 3 within 1 km — so the input sites are physically distinct. |
| **ERA5-Land** | **NO** | ECMWF: ERA5-Land "runs without data assimilation"; observations influence it only "indirectly… through the atmospheric forcing of ERA5", whose assimilation uses GTS synoptic reports rather than state agricultural networks. |
| **VIIRS, MODIS** | **NO** | Thermal retrievals; no surface station input. |

**Consequence: Daymet is the fair benchmark at 1 km, and the only one.** PRISM and gridMET are
being scored against the very observations they were interpolated from, at those observations'
own locations. Their apparent advantage may be partly station-data dependency rather than
measurement skill, and the size of that effect is what **Step 5** now exists to measure.

**A hypothesis, not a finding.** The only product any satellite beats is ERA5-Land — which is
also the only gridded product that does not ingest CIMIS at all. That is *consistent* with the
circularity hypothesis, but it is **one data point** and must be stated as a hypothesis and never
presented as evidence on its own.

### 5.4 Ground truth — CIMIS

CIMIS stations in and adjacent to almond regions, 2015–2025. Pull hourly air temperature and daily
minimum.

- API key is in `.env` as `CIMIS_APP_KEY`. Never print it, never write it into a notebook cell, a
  saved response, or a logged URL.
- The legacy `appKey` query-parameter API was retired 31 July 2026. Use the current endpoint with
  the key in the `Ocp-Apim-Subscription-Key` header.
- Pull daily `DayAirTmpMin` and hourly `HlyAirTmp` for each station-season.

Frost nights are defined from CIMIS, not from satellite. A frost night is a station-night where
`DayAirTmpMin` falls at or below a stated threshold. Run the whole analysis at three thresholds —
0 °C, −1.1 °C (30 °F) and −2.2 °C (28 °F) — and report sensitivity, as the strawberry study did
with rainfall.

**The known confound, and it is not small.** CIMIS measures air temperature at 1.5 m over
irrigated grass. Satellite LST measures the surface — soil, cover crop, canopy. On a
radiative-cooling night the surface is colder than the air above it, often by several degrees, and
the offset is not constant: it depends on wind, soil moisture and ground cover. So the comparison
must be run in two forms:

1. **Raw.** Satellite LST versus station air minimum, offset reported, not removed. This shows the
   honest magnitude.
2. **Bias-corrected.** An offset fitted and removed, then residual error compared. This is what an
   index product would actually do — a parametric trigger is calibrated, not taken raw.

**AMENDED 2026-09-22 — the offset is fitted per region AND per year**, not per region across the
whole study. The original spec said a single season-wide offset per region. That is wrong for
Aqua and Terra, whose overpass times drift across the study period, so a single offset would
blend the 2015 satellite with the 2025 one. Per region and per year for every product, so the
products are treated identically.

The bias-corrected form is the one that answers the question. The raw form keeps the exhibit
honest about what LST is.

### 5.5 Terrain

- `USGS/3DEP/10m_collection` — elevation, slope, and a derived cold-air-drainage proxy (e.g.
  topographic position index, or height above nearest drainage).
- This is what K3 tests against. If satellite advantage tracks terrain relief, the mechanism is
  real.

### 5.6 Boundaries

- `TIGER/2018/Counties` for county geometry.

## 6. Method

Each step ends at a **CHECKPOINT**: print the result, stop, wait for my review. Do not chain
steps.

**Step 1 — Units and stations.** Build the almond unit layer from DWR. Report acreage by region,
count, size distribution. Report **county membership of each stratum as a table**, with each
county's almond acreage, its median latitude, and the share of its acreage falling on the wrong
side of its boundary; and report the fraction of state almond acreage assigned, which should be
100%. Build the CIMIS station list: which stations sit inside or within 10 km
of almond acreage, their elevation, their years of record. Report how many units have a station
within 5, 10, 20 km. Report the CDL comparison: what fraction of CDL almond area falls inside DWR
almond fields, and vice versa. CHECKPOINT.

**Step 2 — The frost-night calendar.** Pull CIMIS. For each station-season, list every night at or
below each of the three thresholds. Report: nights per year per region, the coldest nights on
record in the window, the interannual spread. Identify the handful of major events (a widespread
valley freeze is far more useful than a scattered local one). Report how many station-nights exist
in total. This is where K1 is first testable. CHECKPOINT.

**Step 3 — Satellite availability on those nights.** For every frost night from Step 2, check
whether each satellite product has a usable observation over the relevant station. Usable means
the QA band says clear and the LST retrieval is good — use the product's own QC flags, do not
invent a screen.

Report, as a table: frost nights, nights with VIIRS, with Aqua, with Terra, with GOES-18, with
ECOSTRESS. Then the critical cross-tab: is the clear-sky rate on frost nights higher or lower than
on non-frost nights? Radiative frost requires clear skies, so it should be higher — if it is not,
something is wrong with the screen or K4 is firing. CHECKPOINT. This is the step most likely to
kill the study. Do not proceed past it without my sign-off.

**Step 4 — Point comparison at stations.** For each usable station-night, extract satellite LST at
the station pixel per product, each gridded product's tmin at the station cell, and the CIMIS
observed minimum. Compute, per product: bias, median absolute error, RMSE, and the error
distribution's tails. Both raw and bias-corrected per §5.4. Report by region and by threshold.
**GOES is excluded from this step (§5.2).** This is the head-to-head. K2 is tested here.
CHECKPOINT.

**Step 4b — The Aqua drift experiment (AMENDED, added 2026-09-22).** Aqua's overpass moved from
about 02:00 to about 03:16 across the study, walking it steadily toward the true pre-dawn minimum.
Treat that as a designed experiment. Regress Aqua's error against the station minimum on its
**per-pixel view time**, pooling all station-nights. Use per-pixel view time as a covariate —
**do not fit one offset per year for this analysis**, because per-year fitting throws away the
within-night physics that makes it interesting. If a later overpass reads systematically closer to
the observed minimum, that is independent confirmation of whatever Step 7 finds from GOES, by a
completely different mechanism. CHECKPOINT.
**Stratification sensitivity (added 2026-09-22).** Repeat the headline comparison under the four
alternative stratifications defined in §5.1a and report whether the ranking of products, and the
size of any satellite advantage, changes. Report the answer either way. A result that does not
move under a one-county shift of either boundary says the strata are a reporting convenience, not
a physical control, and §5.4's per-region bias correction must then be read in that light.

**Report as two findings, not one ranking (added 2026-09-22, see §5.2a).** Separate the 1 km
comparison (VIIRS and MODIS against **Daymet**, same footprint, so any gain is measurement rather
than resolution) from the coarse comparison (against **PRISM, gridMET at 4 km and ERA5-Land at
~11 km**, where a resolution advantage is genuinely available). State which mechanism each result
supports. Do not average them into a single ranking.

**Step 5 — Terrain, station distance, and the circularity test. THE DECISIVE STEP
(PROMOTED 2026-09-23).** This was a supporting step. It is now the one that determines what the
K2 result means, because §5.3a established that PRISM and gridMET are interpolated from the very
stations they are scored against while the satellites are not.

**The circularity test.** Report each product's error as a function of **distance from the
nearest station it ingests** — for PRISM and gridMET that is the nearest CIMIS station, for
Daymet the nearest GHCN-Daily station, and for the satellites there is no such distance. Then:

- **If PRISM's advantage decays with distance from its own input stations while the satellite's
  error stays flat, the honest conclusion is that the grid wins where it was fitted and the
  satellite may not lose where it was not.** That is a materially different finding from "the
  satellite loses", and it must be stated as such.
- **If PRISM's error is flat with distance too**, the dependency is not doing the work and the
  K2 result stands as measured.

**Extrapolate to the distances that actually matter.** Stations are not where orchards are. The
median almond unit is **14.4 km** from the nearest station that operated in the study window, the
90th percentile is 26.5 km, and **most units are further from a station than any station is from
another** — so the error at 0–5 km, where the comparison is made, is not the error a product
would deliver over the orchards an index would insure. Report the fitted error-versus-distance
relationship evaluated at the unit distance distribution, and state the extrapolation plainly as
an extrapolation.

**Then the terrain question as originally specified:** regress per-station error against terrain
relief and elevation, and report whether any satellite advantage grows with relief. **K3 is
tested here.** CHECKPOINT.

**Step 6 — Neighbourhood-scale spatial structure, and whether it repeats.**
**RENAMED 2026-09-22.** The previous title, "within-orchard structure", claimed a footprint the
sensors do not have: at 1 km the test cannot see inside an orchard, since the median unit is about
a tenth of a pixel (§5.2a). What it actually tests is whether **neighbourhood-scale** terrain
structure repeats across independent frost nights. That is still the right test and still worth
doing — cold-air pooling operates at roughly that scale — but the claim must match the footprint,
and the write-up must not describe a 1 km result as within-orchard. ECOSTRESS at ~70 m is the only
sensor here that resolves a single orchard; where a night scene coincides with a major event it is
the one panel that can show what the 1 km products average over.

Leave the stations. For the major events from Step 2, map
satellite LST across all almond units in the affected region and compare against each gridded
product's field over the same area. Report: the spatial standard deviation of each product over
the almond acreage, and the spatial correlation between them. A 4 km grid physically cannot show
sub-4 km structure; the question is whether the structure the satellite shows is signal or noise.
Test that by checking whether the same units read cold on independent frost nights. Structure that
repeats is terrain; structure that does not is noise. That test is the point of this step. Where
an ECOSTRESS night scene coincides with a major event, add it as a 70 m panel. CHECKPOINT.

**Step 7 — GOES and the timing question. REDEFINED 2026-09-23.**

**Why redefined.** As written, this step ran on the major events from Step 2. Those fall in 2018,
2019, 2022 and 2023, and the GOES-18 collection begins **2022-05-11**, so only the three
single-night February 2023 events were reachable — three event-nights for the analysis this study
most wants. The timing question does not need a valley-wide freeze. It needs a **clear, calm,
strongly cooling night**, and there are many of those in three seasons.

**Redefined sample: every frost night in 2023–2025 that meets a stated radiative-cooling
condition**, not only the widespread events. The condition, to be reported before the step runs:

1. Station-night at or below the 0 °C threshold (§5.4); **and**
2. the clear-sky criterion established in Step 3, applied to the same night.

**Counted from the Step 2 calendar, before the Step 3 criterion is applied:** the GOES-18 era holds
**7,783 usable station-nights, of which 606 are at or below 0 °C, spread over 64 distinct dates**
(37 dates in 2023, 10 in 2024, 17 in 2025). At −1.1 °C it is 281 station-nights over 42 dates, and
at −2.2 °C, 127 over 22 dates. Against three event-nights, that is the difference between a
statement and an anecdote. **Report how many nights survive the clear-sky criterion before running
the step**, and if the surviving count is small, say so rather than proceeding quietly.

For those nights, pull the GOES-18 ABI time series and report:

- **where in the night the minimum falls**, by station and by date;
- **how far above the nightly minimum the ~01:30 polar-orbiter reading sits**, which is the number
  that determines whether a once-a-night snapshot can stand in for a minimum;
- **whether that offset varies in space** across the almond regions, since a spatially varying
  offset cannot be removed by a single calibration constant.

**Falsification check, mandatory, reported whether or not it fires (ADDED 2026-09-23).** If
GOES's apparent extra cooling is cloud rather than surface, it must behave like cloud. Test and
report:

1. whether the apparent extra cooling **correlates with cloud indicators** on the same night; and
2. whether it is **largest on the nights the polar orbiters flag as unclear**, which is what
   contamination predicts and what a real surface signal does not.

A clean result here is a positive finding about the timing gap. A dirty one means the timing
result is an artefact, and that must be stated as the result rather than worked around.

GOES is a **timing instrument only** here: `CMI_C13`/`C14` are top-of-atmosphere brightness
temperatures, not LST, and GOES is absent from the Step 4 accuracy comparison (§5.2). GOES-17 is
not used at all (§5.2). CHECKPOINT.

## 7. Figures

1. Study area: almond units by region, CIMIS stations, elevation shaded.
2. Frost-night frequency by year and region, three thresholds.
3. Satellite availability on frost versus non-frost nights (the K4 figure).
4. Error distributions: each satellite product and each grid, side by side, raw and
   bias-corrected.
5. Error versus terrain relief and versus station distance (the K3 figure).
6. A major event mapped four ways: PRISM, Daymet, VIIRS, and ECOSTRESS or GOES — same colour
   scale, same extent.
7. GOES night curve at several orchards, with the polar-orbit overpass times marked.
8. **AMENDED:** Aqua error against per-pixel view time (the Step 4b figure).

## 8. EXHIBIT.md structure

1. Question and scope, including what is not being tested
2. Study area and units
3. The frost-night calendar
4. Satellite availability and the clear-sky sampling question
5. Head-to-head accuracy at stations
6. Terrain, station distance, and where the advantage comes from
7. Spatial structure across orchards
8. Timing: what a once-a-night snapshot misses
9. Limitations
10. **Silent failure modes in public datasets**
11. What this means for an index product — measurement implications only, no product proposal
12. Data and reproducibility

**§2 must carry the unit-area against pixel-area distribution**, from Step 1: the share of
almond units smaller than one pixel of each product, at 1 km, 4 km and 11 km, with the median unit
area beside it. **Every result in §5 onward is conditioned on this number**, because a per-unit
satellite value is a neighbourhood average rather than an orchard measurement, so it is stated
before any accuracy figure rather than after. §5.2a gives the reasoning; §2 gives the number.

**§2 must carry the crop-map agreement result as a finding, not as a closed check.** Measured
here for almonds and in the strawberry study for strawberries, using the same two products
(DWR/Land IQ and USDA CDL) and the same two directions:

| | almonds (2023) | strawberries (2023) |
|---|---|---|
| CDL crop area falling inside DWR fields of that crop | **69.5%** | **32.6%** |
| DWR field area that CDL calls the same crop | **85.1%** | not computed |

Both almond figures are statewide: the 24 almond counties hold 98.7% of the CDL almond area in
California.

**Two independent crop maps agree far better on a perennial than on a rotating annual.** That is
intuitive — an orchard holds its signature for twenty years while a strawberry field is plastic,
then canopy, then something else within one water year — but it is now measured across two studies
on the same two products rather than asserted. It is useful to anyone choosing a unit layer for
index work on a specialty crop.

**The gap stays stated.** CDL calls 1,849,423 acres almonds in the 24 almond counties against
1,508,863 from DWR, **+23%, a difference of 340,560 acres**. Neither map is ground truth.
The reader must know the unit layer carries that uncertainty **before** any temperature result
lands on it, so this belongs in §2 and not in §9.

§9 must include, at minimum: the LST-versus-air-temperature confound and how it was handled;
clear-sky sampling bias; the DWR survey year versus the study years; CIMIS station siting
(irrigated grass is not an orchard floor); QC flag behaviour; and any product documentation
surprises found along the way.

**§9 must also carry, as stated design limits rather than caveats:**

- **GOES measures brightness temperature, not LST**, which is why it is a timing instrument only
  and absent from the Step 4 accuracy comparison.
- **ABI continuity for night thermal work in California effectively begins in 2023**, because
  GOES-17's infrared bands are unusable on about a third of February pre-dawn scenes.
- **The station comparison is circular for two of the four grids, and this is a limitation of
  the headline result, not a footnote.** **PRISM ingests CIMIS** (its own Table A1 lists CIMIS
  under `AN91d` for Tmax/Tmin) and **gridMET bias-corrects daily PRISM**, so both are interpolated
  from the stations against which they are then scored, at those stations' own locations.
  **Daymet (GHCN-Daily), ERA5-Land and the satellites do not ingest CIMIS.** **The K2 ranking may
  therefore partly reflect station-data dependency rather than measurement skill**, and the
  honest 1 km comparison is satellite against **Daymet**, not against PRISM. Step 5 measures how
  much of the gap is dependency by testing whether each product's error grows with distance from
  the nearest ingested station. See §5.3a.
- **No 1 km product resolves a single orchard.** The median almond unit is about a tenth of a
  MODIS or VIIRS pixel, so every per-unit LST value is a neighbourhood value containing many
  fields. This is a property of the measurement, not a caveat about it, and it conditions every
  accuracy, structure and timing result in the study. See §5.2a and the §2 distribution.
- **Against Daymet there is no resolution advantage**, both being 1 km; the only available claim
  there is measurement versus interpolation. Against PRISM and gridMET (4 km) and ERA5-Land
  (~11 km) a resolution advantage is genuinely available. **These are two different findings and
  §5 must not merge them into one ranking.**
- **The calendar counts frost nights, not damaging nights.** Frost here is concentrated in
  February — 2,299 of 2,910 nights at or below 0 °C, a 15.4% nightly rate against 3.7% in March —
  while almond bloom typically begins in mid-February. A meaningful share of the frost nights in
  this calendar therefore fall before bloom, when the trees are dormant and the same temperature
  causes no loss. **This is not a defect:** the study measures hazard and deliberately does not
  model damage (§1). It must be stated plainly all the same, because a reader will otherwise take
  the night count for a loss-relevant count. **Mapping frost nights to damaging nights requires
  bloom-stage data this study does not use.**
- **Step 6 tests neighbourhood-scale structure, not within-orchard structure.** Nothing in this
  study at 1 km may be described as resolving variation inside an orchard; only ECOSTRESS at
  ~70 m can.

### §10 — Silent failure modes in public datasets

A short section in its own right, not a footnote. It carries every instance this programme has
hit, and for each one records **what the wrong value would have been, why it looked plausible,
and what caught it**:

1. **CPC precipitation stored in 0.1 mm/day** (strawberry study). Read at face value it gave
   792 mm for a six-day event and 5,053 mm for calendar 2021 at Pajaro, against 592 mm from PRISM
   for the same point and year. Plausible because a wet winter in coastal California *should*
   produce large numbers, and because the conclusion it supported — that a coarse grid triggers
   everywhere — was one we half expected. Caught by an independent plausibility check against
   another product and against physical reality: no part of coastal California receives five
   metres of rain.
2. **VIIRS `LST_1KM` carries no scale factor where MODIS `LST_Night_1km` carries 0.02.** Applying
   the MODIS recipe to VIIRS gives about **−268 °C**. Plausible only until you look — but the
   failure mode is the reverse case, applying the *VIIRS* recipe to MODIS, which turns a scaled
   integer into a number near 14,000 K, or worse, a correctly scaled MODIS value into a silently
   wrong one if the offset alone is dropped. Caught by reading each band's catalogue entry before
   use and checking raw values against the expected range.
3. **DWR changed which field carries the crop between survey years.** The strawberry study read
   `CROPTYP1`; in the 2023 final geodatabase that field is `****` for 419,240 of 446,914 fields,
   and the crop lives in `MAIN_CROP`. Reusing the earlier selector unchanged returns **302 almond
   fields and 8,411 acres** instead of roughly 1.5 million — and 8,411 acres is a perfectly
   believable number for a small crop, which is exactly why it would have survived review.
   Caught by tabulating the field's own distribution before trusting it.

4. **A mask that encodes "good" as "absent".** In Earth Engine's `MOD11A1`/`MYD11A1` the
   `QC_Night` band is *masked* wherever its value is 0 — and 0 is "LST produced, good quality".
   The cautious reading, treating a missing quality flag as unusable, therefore **throws away the
   best retrievals and keeps the second-best**: two-thirds of the valid station-nights in a test
   season. Verified rather than assumed: 705 station-nights had LST present with QC masked, 716
   had QC present with LST absent, 343 had both, **none had both missing**, and `unmask(0)`
   returned 0 for all 705. VIIRS, from the same provider family, never masks its `QC` band —
   so the behaviour is not even consistent between sibling products.
5. **A sparse sensor makes a plausible zero.** `ee.Reducer.first()` names its output `first` on a
   single-band image but after the band names on a multi-band one. An ECOSTRESS extraction that
   read back the band name got `None` for every row and reported **zero usable observations in
   every season** — which is exactly what a sparse ISS-orbit sensor might genuinely produce, and
   it was nearly accepted on those grounds. **A bug returning nothing is indistinguishable from
   the sparsity you expected.** Caught only by hand-checking one scene at one station against a
   second method, where `reduceRegion` returned a value that `reduceRegions` did not. The true
   figure is 86–339 usable station-nights per season from 2019.

**The scaling pattern is now a rule, not three anecdotes.** Three independent products in this
programme have stored a physical quantity as a scaled integer in a way their catalogue entry did
not make safe: **CPC precipitation** in 0.1 mm/day (strawberry study), **VIIRS `LST_1KM`** with no
scale factor where sibling MODIS bands carry 0.02, and **GOES `CMI_C13`**, whose catalogue entry
declares units of K and gives no scale factor while the values are scaled integers needing a
**per-image** scale and offset. The GOES case is the sharpest: raw values run 1,980–3,218, plainly
not kelvin, but **a guessed ×0.1 gives 198–322 K — inside the believable range and wrong.** The
image's own `CMI_C13_scale` (0.06145332) and `CMI_C13_offset` (89.62) give 211.3–287.4 K.
**Rule: never infer a scale factor from the plausibility of the result.** Read the product's own
metadata, per image where the metadata is per image, and if it is absent, verify against an
independent source before use.

**All five share one property, and it is the part worth generalising: the error produced a
number in a believable range rather than an exception.** None of them raised an error, none
produced an obviously absurd map, and each supported a conclusion that sounded reasonable. Unit
and schema checks are therefore part of the method, not housekeeping.

#### A fourth category: a check that returns a believable pass

The three above are **data** returning a believable wrong value, and verification catches them.
The fourth is **verification itself** returning a believable pass, and it defeats verification.

It happened in this programme, and the scope should be stated honestly: **it was in the strawberry
repository's environment patch, not in the almond analysis, and it did not touch any result.**
While routing that repository's file reads through fiona, an automated edit inserted
`engine="fiona"` before the last parenthesis on each line, which on a chained call like
`gpd.read_file(...).to_crs(C.GRID_CRS)` placed the argument inside `to_crs` instead. A follow-up
correction then wrote literal backslashes into the notebook JSON, leaving `engine=\"fiona\"` in
the Python source — seven lines that could not parse at all.

Both passed the check that was supposed to catch them. The check compiled every code cell inside

```python
try:
    ast.parse(line)
except SyntaxError:
    continue        # <- silently swallows exactly what the check exists to find
```

so it reported zero errors while three lines were semantically wrong and later seven were
unparseable. **The check could only ever report success**: every failure it was built to detect
was routed to `continue`.

Caught by re-running the check with failures reported rather than skipped, and by printing all
seven lines back as Python to read what the source actually said. That printed form is what
exposed the backslashes, which the compile count alone would never have shown.

The distinction is the point. A wrong number can be caught by checking it. **A check that cannot
fail cannot catch anything**, and it is more dangerous than no check at all, because it produces
a record of having looked.

**The documentation-risk theme.** The strawberry study's CPC units error — a product stored in
0.1 mm/day that read plausibly wrong — belongs here as a cited precedent for why unit and
documentation checks are part of the method. **This study supplies two more of its own, and they
should be reported the same way:** the VIIRS LST band carries no scale factor where MODIS carries
0.02, so copying the MODIS recipe would have produced −268 °C; and this spec's own instruction to
treat Aqua as the ~01:30 primary was taken from the mission's **design** orbit rather than from
observed view times, which the data contradicts by up to 1¾ hours. Both were caught by checking
the product's own documentation and its own view-time band before use.

#### A fifth category: a filter that removes the phenomenon

The first three are **data** returning a believable wrong value. The fourth is **verification**
returning a believable pass. The fifth is a **filter that looks like good hygiene and removes the
thing being measured.** It is the most dangerous of the five, because applying it is a defensible
choice that a reviewer would praise.

Found in this study, in Step 2. CIMIS flags each observation, and two of its informative flags are
historical-limit tests: **`R` "Data is far out of historical limits"** and **`Y` "Data is
moderately out of historical limits."** The obvious, conservative move is to drop flagged data.
**The flags fire because the night was extreme**, so the screen selects against exactly the
observations a frost study exists to measure. Measured over 31,359 usable station-nights:

| | share at or below 0 °C |
|---|---|
| unflagged | **7.7%** |
| `Y`-flagged | **44.2%** |
| `R`-flagged | **54.3%** |

Screening on those flags would have removed **20.2% of frost nights at 0 °C and 46.1% at
−2.2 °C** — nearly half the severe frost nights in the record. Nothing would have looked wrong:
the remaining data would be clean, the counts plausible, the method defensible in a footnote.

**The generalisation, which is the part that matters beyond almonds: any quality filter whose
trigger correlates with the signal biases the result.** Outlier screens, range checks,
historical-limit tests and cloud masks all key on unusualness, and in geophysical data the extreme
event *is* the unusual value. **In an index-insurance context the direction of that bias is
knowable in advance: toward understating tail frequency.** An index priced on screened data
underprices the tail. **That is a mispricing, not a data-cleaning choice**, and it would be
invisible in every diagnostic that looks only at the retained data.

What was done instead: severe flags (`I`, `M`, `S`) are dropped because they carry no value at all
— all 387 in this record are null — while `Y` and `R` are kept, carried in a `flagged` column, and
the flagged share is reported beside every frost-night count.

#### A sixth category: comparing models on different subsets of the world

The fifth category is a filter that removes the phenomenon. The sixth is subtler and, for an
insurance audience, more dangerous: **comparing two products on different subsets of weather
manufactures a difference that is not there.**

Found in Step 4. A satellite is only scored on nights it could see; a gridded product produces a
value on every night. Scored that way — each product on every night it has a value — **VIIRS
appeared to have tighter error tails than the grids on the coldest nights: RMSE 2.39 against
PRISM's 3.10 at −2.2 °C.** That would have been a genuinely important finding, because **a rating
depends on the tails far more than on the median**, and "the satellite is worse on average but
better in the extremes" is exactly the kind of nuance that gets a product built.

**It is an artefact.** The grids were being scored on the cloudy nights the satellite could not
see, and those nights are harder. On the **matched** subset — the same station-nights for every
product — PRISM is 2.28 and Daymet 2.29 against VIIRS 2.39, and the advantage disappears
entirely.

Nothing about this error announces itself: both numbers are correctly computed, the samples are
large, and the conclusion is plausible and interesting. **The generalisation: whenever
availability differs between the things being compared, any comparison not made on identical
observations is measuring availability as well as skill.** This applies well beyond satellites —
to any model scored where it happens to produce output, and to any claim built on records that
exist for one product and not another.

## 9. Rules for the agent

- Stop at every checkpoint. Print results, wait.
- Never substitute a dataset. If an ID is dead, stop and ask.
- **No two products are ever compared except on identical station-nights.** Availability differs
  between products, so a comparison drawn from each product's own available sample measures
  availability as well as skill. Where an unmatched comparison is shown at all, it is shown only
  to quantify the distortion and is labelled as not quotable. See §8 item 10, sixth category.
- **Any result of zero, none or empty must be verified by an independent method before it is
  accepted** — especially where zero is the expected answer. A sparse sensor, a rare event and a
  broken extraction all return nothing, and nothing looks the same in all three cases. Verify with
  a different call, a different granularity, or a hand-checked single case. See §8 item 10,
  entry 5, for the ECOSTRESS zero that survived until one scene was checked by hand.
- **Every filter must report what it removed, and whether what it removed differs from what it
  kept.** Not the count alone: the distribution. A filter is only neutral if the discarded data
  look like the retained data, and that has to be shown rather than assumed. This applies to QC
  flags, cloud masks, outlier screens, minimum-observation cutoffs and every other exclusion in
  this study. Where the removed data differ, say in which direction and by how much. See §8
  item 10, fifth category, for the case that produced this rule.
- **A validation that can pass by skipping is not a validation.** Any check must report its
  failures explicitly and state what it examined. A harness that catches an exception and
  continues must log the catch and fail loudly at the end, never absorb it silently. This applies
  to every checkpoint in this project, not only to syntax checks: the same shape appears in cloud
  screens that silently drop nights and in joins that silently drop rows. **Every checkpoint
  report must carry its denominator** — how many station-nights were examined as well as how many
  passed, how many units joined as well as how many matched — so that a shrinking sample is
  visible rather than invisible. See §8 item 10.
- **Never reuse a selector, field name or scale factor carried over from a previous project
  without re-verifying it against the current file's own schema.** Field names are not stable
  across survey years, and scale factors are not stable across products from the same provider.
  Tabulate the field's own distribution, or read the band's own catalogue entry, before trusting
  anything inherited. See §8 item 10.
- Plausibility-check every extracted quantity against its documentation before using it.
  Temperature products come in K, °C and scaled integers. A number that looks plausible can still
  be wrong by a scale factor. Check the band description, not your memory of it.
- Never modify anything in `data/raw/`.
- Secrets stay in `.env` (gitignored, verified). Never print `CIMIS_APP_KEY` or write it into a
  notebook, an output, or a URL that gets logged.
- Never disable TLS verification or unset `HTTPS_PROXY`.
- Log every spec deviation in `SPEC_CHANGELOG.md` with the reason, at the time it happens.
- Report negative results as findings. Do not retune to rescue a result. If the satellite loses,
  say so and say by how much.
- Do not infer damage. If a step needs a crop-response assumption, stop.
- Commit at each checkpoint. Do not push without asking.

## 10. Open items

Carried deliberately, none blocking. Each is recorded here rather than in a changelog entry so it
stays visible at the top of every session.

1. **A fourth "outside Central Valley" stratum.** Six almond counties — Lake, Calaveras, Contra
   Costa, Alameda, San Luis Obispo, Riverside — sit outside the Central Valley and are currently
   assigned to the three latitude bands by the same rule as everything else (§5.1a). Together they
   hold **6,409 acres, 0.42%** of state almond acreage. The argument for splitting them out is
   that their frost climatology is not valley climatology: coastal San Luis Obispo and the Sierra
   foothills of Calaveras do not pool cold air the way the valley floor does, so folding them in
   adds a different physical regime to each band. The argument against is that 0.42% cannot move
   any stratum-level statistic, and a fourth stratum of 6,409 acres across six disconnected
   counties would be too small and too heterogeneous to interpret. **Recommendation: leave them
   folded in, and report their contribution wherever a stratum result is given, so a reader can
   see the amount at stake.** Revisit only if a result turns on one of those counties.
2. **A compute-footprint estimate before Step 6.** Step 6 maps LST across all almond units for the
   major events, and Step 1 has grown the unit set from 28,748 to **39,102 units over 1.5 million
   acres statewide**. Produce an estimate of the Earth Engine request volume and wall-clock time
   **before** starting Step 6, not during it, and say then whether the step runs on all units, on
   the affected stratum only, or on a sample. The strawberry study hit Earth Engine's interactive
   limits at two-county scale, and this is a far larger area.
3. **~~Asset feature count against unit count.~~ CLOSED 2026-09-22.** The asset holds **45,404**
   features against **39,102** units because it deliberately carries every D12 field, including
   the **6,302** below the 5-acre cut, flagged `is_unit = 0`, so the size cut stays auditable
   inside Earth Engine rather than only in the local table. Step 1 now prints the reconciliation
   and asserts it.
