"""Shared paths, dataset IDs and region definitions for the almond bloom-frost study.

Every dataset ID here is copied from CLAUDE.md §5 and was verified against the Earth Engine
STAC catalogue before use (SPEC_CHANGELOG, 2026-09-21). Do not substitute an ID; if one is
dead, stop and ask (CLAUDE.md §9).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"

EE_PROJECT = "cropczyk"

# --- units -------------------------------------------------------------------------------
DWR_GDB = RAW / "dwr_crop_mapping" / "i15_crop_mapping_2023_final.gdb.zip"
DWR_LAYER = "i15_Crop_Mapping_2023"

# DWR Standard Land Use Legend (2022 remote-sensing version), class D "Deciduous Fruits and
# Nuts", subclass 12 "Almonds". Confirmed against the published legend PDF, not inferred from
# acreage: data/raw/dwr_crop_mapping/SOURCE.md records the URL and checksum.
ALMOND_CODE = "D12"

# CLAUDE.md §5.1: fields >= 5 acres, so edge pixels do not dominate a 1 km LST cell.
MIN_ACRES = 5.0

# --- comparison / thermal / gridded ------------------------------------------------------
CDL = "USDA/NASS/CDL"          # comparison only (CLAUDE.md §5.1)
CDL_ALMOND = 75                # CDL class 75 = Almonds
CDL_YEAR = 2023                # matched to the DWR survey year

VIIRS_LST = "NASA/VIIRS/002/VNP21A1N"
MODIS_AQUA_LST = "MODIS/061/MYD11A1"
MODIS_TERRA_LST = "MODIS/061/MOD11A1"
GOES18 = "NOAA/GOES/18/MCMIPC"
ECOSTRESS = "NASA/ECOSTRESS/L2T_LSTE/V2"

PRISM = "OREGONSTATE/PRISM/ANd"
DAYMET = "NASA/ORNL/DAYMET_V4"
GRIDMET = "IDAHO_EPSCOR/GRIDMET"
ERA5_LAND = "ECMWF/ERA5_LAND/HOURLY"

# --- regions (CLAUDE.md §5.1a, amended 2026-09-22) ---------------------------------------
# Every county with almond acreage is assigned; coverage is 100%. The strata come from two
# latitude boundaries placed BETWEEN counties -- chosen as the local minima of almond acreage
# landing on the wrong side -- with each county assigned whole by the acreage-weighted median
# latitude of its own almond fields.
#
# Assignment is at county level and never at field level: federal crop insurance is administered
# county by county, so a stratum that cannot be written as a county list is of no use to the
# audience for this document. The latitude rule DERIVES the list; the frozen list below is what
# the study uses, and Step 1 re-checks it against the rule on every run.
BOUNDARY_SAC_SJN = 38.25   # Sacramento Valley | San Joaquin north
BOUNDARY_SJN_SJS = 36.82   # San Joaquin north | San Joaquin south

REGION_COUNTIES = {
    "sac_valley": {"Butte", "Colusa", "Glenn", "Lake", "Placer", "Sacramento", "Solano",
                   "Sutter", "Tehama", "Yolo", "Yuba"},
    "sj_north": {"Alameda", "Calaveras", "Contra Costa", "Madera", "Merced", "San Joaquin",
                 "Stanislaus"},
    "sj_south": {"Fresno", "Kern", "Kings", "Riverside", "San Luis Obispo", "Tulare"},
}

# Counties whose almond acreage straddles their boundary by more than 5% of their own acreage.
# Reported, never forced: Sacramento and San Joaquin interlock across the Delta and no latitude
# separates them cleanly. Values measured in Step 1.
STRADDLING = {"Sacramento": 15.1, "Fresno": 5.5, "Madera": 5.1}

# Almond counties outside the Central Valley, assigned by the same rule rather than special-cased.
NON_VALLEY = {"Lake", "Calaveras", "Contra Costa", "Alameda", "San Luis Obispo", "Riverside"}

# Stratification sensitivity: each boundary moved by one county each way. "One county" is the
# adjacent county by median latitude holding at least 1% of state almond acreage, so the test is
# not decided by a 200-acre county. Step 4 reports whether the headline result moves.
REGION_SCHEMES = {
    "base": {},
    "b1_up": {"Solano": "sj_north"},          # boundary 1 north past Solano
    "b1_down": {"San Joaquin": "sac_valley"},  # boundary 1 south past San Joaquin county
    "b2_up": {"Madera": "sj_south"},           # boundary 2 north past Madera
    "b2_down": {"Fresno": "sj_north"},         # boundary 2 south past Fresno
}

SAC_HYDRO_RGN = "Sacramento River"   # DWR's published boundary, kept as a 1.2% sensitivity

REGION_LABELS = {
    "sac_valley": "Sacramento Valley",
    "sj_north": "San Joaquin north",
    "sj_south": "San Joaquin south",
}
REGION_ORDER = ["sac_valley", "sj_north", "sj_south"]

COUNTY_REGION = {c: r for r, cs in REGION_COUNTIES.items() for c in cs}
STUDY_COUNTIES = sorted(COUNTY_REGION)


def assign_region(county: str, scheme: str = "base") -> str:
    """Region label for one field, from its DWR county, under a named stratification scheme.

    Returns "unassigned" only for a county with no almond acreage in the 2023 survey; Step 1
    asserts that no unit falls there.
    """
    return REGION_SCHEMES[scheme].get(county, COUNTY_REGION.get(county, "unassigned"))


# Study CRS for distance work: California Albers, metres, equal area.
METRIC_CRS = "EPSG:3310"
