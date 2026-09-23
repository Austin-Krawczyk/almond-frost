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
| Geography | California almond acreage, stratified by region: Sacramento Valley (north), San Joaquin north (Stanislaus/Merced), San Joaquin south (Fresno/Kern) |
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

### 5.2 Satellite thermal — the candidates

All are night-time observations; daytime LST is irrelevant to frost.

| Product | Earth Engine ID | Band | Resolution | Role |
|---|---|---|---|---|
| **VIIRS LST — PRIMARY** | `NASA/VIIRS/002/VNP21A1N` | `LST_1KM` | 1 km | Primary polar orbiter (**AMENDED**) |
| MODIS Aqua night LST | `MODIS/061/MYD11A1` | `LST_Night_1km` | 1 km | Full candidate, plus the drift experiment (**AMENDED**) |
| MODIS Terra night LST | `MODIS/061/MOD11A1` | `LST_Night_1km` | 1 km | Candidate; too early in the night |
| GOES-18 ABI | `NOAA/GOES/18/MCMIPC` | `CMI_C13`, `CMI_C14` | 2 km | **Timing instrument only**, Step 7 (**AMENDED**) |
| ECOSTRESS | `NASA/ECOSTRESS/L2T_LSTE/V2` | `LST` | ~70 m | Case-study sensor, 2019–2025 (**AMENDED**) |

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
   satellite midnight. Tested on real February scenes over the Central Valley: at 12Z and 14Z
   (04:00 and 06:00 PST — the pre-dawn minimum), **a consistent third of sampled nights are
   0% good by the product's own `DQF_C13` flag, in 2020, 2021 and 2022 alike**, while GOES-18 is
   100% good at the same hours in 2023–2025. GOES-17 is therefore not used. GOES-16 is not used
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

### 5.3 Gridded baselines — what the satellite has to beat

| Product | Earth Engine ID | Resolution | Variable | Units |
|---|---|---|---|---|
| PRISM daily | `OREGONSTATE/PRISM/ANd` | 4 km | `tmin` | °C |
| Daymet V4 | `NASA/ORNL/DAYMET_V4` | 1 km | `tmin` | °C |
| gridMET | `IDAHO_EPSCOR/GRIDMET` | ~4 km | `tmmn` | K |
| ERA5-Land | `ECMWF/ERA5_LAND/HOURLY` | ~11 km | `temperature_2m` | K |

Note the deprecated ID. `OREGONSTATE/PRISM/AN81d` ends in 2020 and will not cover this window.
Use `ANd`.

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
count, size distribution. Build the CIMIS station list: which stations sit inside or within 10 km
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

**Step 5 — Does the advantage come from terrain?** Regress per-station error against terrain
variables: elevation, TPI, height above nearest drainage, distance to nearest CIMIS station, local
relief within 5 km. The hypothesis is specific: gridded product error should grow with terrain
relief and with station distance, and satellite error should not. If both grow together, the
satellite is not resolving anything the grid misses. K3 is tested here. CHECKPOINT.

**Step 6 — Within-orchard structure.** Leave the stations. For the major events from Step 2, map
satellite LST across all almond units in the affected region and compare against each gridded
product's field over the same area. Report: the spatial standard deviation of each product over
the almond acreage, and the spatial correlation between them. A 4 km grid physically cannot show
sub-4 km structure; the question is whether the structure the satellite shows is signal or noise.
Test that by checking whether the same units read cold on independent frost nights. Structure that
repeats is terrain; structure that does not is noise. That test is the point of this step. Where
an ECOSTRESS night scene coincides with a major event, add it as a 70 m panel. CHECKPOINT.

**Step 7 — GOES and the timing question.** For the major events, pull the GOES-18 ABI time series
through the night at a sample of orchards. Report: the hour of observed minimum, how much colder
the true minimum is than the 01:30 polar-orbiter snapshot, and whether that offset is spatially
uniform. If the offset is large and variable in space, then no single-overpass product — however
fine its pixels — measures the hazard, and 2 km every 10 minutes beats 1 km once a night. That
would be the study's most useful finding. Note that GOES-18 restricts this step to the 2023–2025
seasons. CHECKPOINT.

**Step 8 — Write up.** Assemble `EXHIBIT.md` and `SUMMARY.md`. Every number traceable to a
notebook cell. Every kill criterion addressed explicitly, fired or not.

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
10. What this means for an index product — measurement implications only, no product proposal
11. Data and reproducibility

§9 must include, at minimum: the LST-versus-air-temperature confound and how it was handled;
clear-sky sampling bias; the DWR survey year versus the study years; CIMIS station siting
(irrigated grass is not an orchard floor); QC flag behaviour; and any product documentation
surprises found along the way.

**§9 must also carry, as stated design limits rather than caveats:**

- **GOES measures brightness temperature, not LST**, which is why it is a timing instrument only
  and absent from the Step 4 accuracy comparison.
- **ABI continuity for night thermal work in California effectively begins in 2023**, because
  GOES-17's infrared bands are unusable on about a third of February pre-dawn scenes.

**The documentation-risk theme.** The strawberry study's CPC units error — a product stored in
0.1 mm/day that read plausibly wrong — belongs here as a cited precedent for why unit and
documentation checks are part of the method. **This study supplies two more of its own, and they
should be reported the same way:** the VIIRS LST band carries no scale factor where MODIS carries
0.02, so copying the MODIS recipe would have produced −268 °C; and this spec's own instruction to
treat Aqua as the ~01:30 primary was taken from the mission's **design** orbit rather than from
observed view times, which the data contradicts by up to 1¾ hours. Both were caught by checking
the product's own documentation and its own view-time band before use.

## 9. Rules for the agent

- Stop at every checkpoint. Print results, wait.
- Never substitute a dataset. If an ID is dead, stop and ask.
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
