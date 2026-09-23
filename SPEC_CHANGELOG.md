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
