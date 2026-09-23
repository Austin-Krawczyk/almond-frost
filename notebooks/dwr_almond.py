"""Almond unit layer from the DWR / Land IQ Statewide Crop Mapping 2023 final geodatabase.

Field-name warning, and the reason CLAUDE.md §9 carries a rule about it: in this survey year the
crop lives in `MAIN_CROP`. `CROPTYP1`, `CLASS1` and `SUBCLASS1` are `****` for 419,240 of the
446,914 fields (93.8%). Selecting on `CROPTYP1 == 'D12'`, as an earlier project did, returns 302
fields and 8,411 acres instead of 45,404 fields and 1,524,133 acres -- a believable number for a
minor crop, which is exactly why it would survive review. Re-verify the schema, never inherit it.
"""
import geopandas as gpd

import common as C

COLS = ["UniqueID", "MAIN_CROP", "MAIN_CROP_DATE", "YR_PLANTED", "ACRES",
        "COUNTY", "REGION", "HYDRO_RGN", "CROPTYP1", "CLASS1", "SUBCLASS1"]


def gdb_path() -> str:
    """fiona/GDAL virtual path into the zipped file geodatabase (raw data is never unpacked)."""
    return "zip://" + str(C.DWR_GDB).replace("\\", "/")


def load_almonds(min_acres: float = C.MIN_ACRES) -> gpd.GeoDataFrame:
    """All D12 fields statewide, with `region` and an `is_unit` flag for the >= min_acres cut.

    Small fields are kept in the table as flagged non-units so the size cut stays visible and
    auditable, in the same way the strawberry study kept its sequence B and C fields.
    engine="fiona": pyogrio's GDAL DLL is blocked by Windows Application Control on this machine.
    """
    g = gpd.read_file(gdb_path(), layer=C.DWR_LAYER, columns=COLS,
                      where=f"MAIN_CROP = '{C.ALMOND_CODE}'", engine="fiona")
    # named study_region, not region: DWR already uses REGION for its own office codes
    # (NRO/NCRO/SCRO), and GeoPackage column names are case-insensitive.
    ll = g.to_crs("EPSG:3310").geometry.centroid.to_crs("EPSG:4326")
    g["lat"] = ll.y
    g["lon"] = ll.x
    g["study_region"] = [C.assign_region(c) for c in g["COUNTY"]]
    # Per-unit region under each alternative stratification, so Step 4 can report the §5.1a
    # sensitivity without rebuilding the units.
    for scheme in C.REGION_SCHEMES:
        if scheme != "base":
            g[f"region_{scheme}"] = [C.assign_region(c, scheme) for c in g["COUNTY"]]
    g["is_unit"] = (g["ACRES"] >= min_acres).astype(int)
    return g


def check_region_rule(g) -> "pd.DataFrame":
    """Re-derive the county->stratum map from the latitude rule and check the frozen list.

    Returns the county membership table (CLAUDE.md §6 Step 1) and raises if the frozen list in
    common.py disagrees with the rule, so the list can never drift away from how it was derived.
    """
    import numpy as np
    import pandas as pd

    B1, B2 = C.BOUNDARY_SAC_SJN, C.BOUNDARY_SJN_SJS
    u = g[g.is_unit == 1]
    rows = []
    for county, s_ in u.groupby("COUNTY"):
        w, lat = s_.ACRES.values, s_.lat.values
        order = np.argsort(lat)
        med = float(np.interp(0.5, np.cumsum(w[order]) / w.sum(), lat[order]))
        band = "sac_valley" if med >= B1 else ("sj_north" if med >= B2 else "sj_south")
        wrong = (w[lat < B1].sum() if band == "sac_valley" else
                 w[(lat < B2) | (lat >= B1)].sum() if band == "sj_north" else
                 w[lat >= B2].sum())
        rows.append({"county": county, "stratum": band, "acres": round(w.sum()),
                     "units": len(s_), "median_lat": round(med, 3),
                     "straddle_acres": round(wrong),
                     "straddle_pct": round(100 * wrong / w.sum(), 1),
                     "central_valley": county not in C.NON_VALLEY})
    t = pd.DataFrame(rows).sort_values(["stratum", "acres"], ascending=[True, False])

    derived = dict(zip(t.county, t.stratum))
    if derived != C.COUNTY_REGION:
        diff = {k: (v, C.COUNTY_REGION.get(k)) for k, v in derived.items()
                if C.COUNTY_REGION.get(k) != v}
        raise RuntimeError(f"frozen county list disagrees with the latitude rule: {diff}")
    return t
