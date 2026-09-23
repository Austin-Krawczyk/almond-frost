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
    g["study_region"] = [C.assign_region(c) for c in g["COUNTY"]]
    g["is_unit"] = (g["ACRES"] >= min_acres).astype(int)
    return g
