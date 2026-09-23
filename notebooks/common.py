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

# --- regions -----------------------------------------------------------------------------
# CLAUDE.md §4 names three strata. Two are given as county pairs and are used verbatim. The
# third, "Sacramento Valley (north)", is named without counties. It is defined here as the ten
# Sacramento Valley counties that carry almond acreage, so that all three strata are defined the
# same way and the CDL comparison footprint matches the strata. DWR ships its own published
# boundary in HYDRO_RGN; selecting on "Sacramento River" instead moves 3,607 acres (1.2% of the
# region: Sacramento County 3,435 ac and Solano 214 ac sit in other hydrologic regions). That
# variant is reported as a sensitivity at the Step 1 checkpoint, not used as the definition.
REGION_COUNTIES = {
    "sac_valley": {"Butte", "Colusa", "Glenn", "Placer", "Sacramento", "Solano", "Sutter",
                   "Tehama", "Yolo", "Yuba"},
    "sj_north": {"Stanislaus", "Merced"},
    "sj_south": {"Fresno", "Kern"},
}
SAC_HYDRO_RGN = "Sacramento River"   # the published alternative, reported as a sensitivity

REGION_LABELS = {
    "sac_valley": "Sacramento Valley",
    "sj_north": "San Joaquin north (Stanislaus/Merced)",
    "sj_south": "San Joaquin south (Fresno/Kern)",
    "unassigned": "Almond acreage outside the three strata",
}
REGION_ORDER = ["sac_valley", "sj_north", "sj_south", "unassigned"]


def assign_region(county: str) -> str:
    """Region label for one field, from its DWR county. Unmatched counties are 'unassigned'."""
    for region, counties in REGION_COUNTIES.items():
        if county in counties:
            return region
    return "unassigned"


STUDY_COUNTIES = sorted(set().union(*REGION_COUNTIES.values()))


# Study CRS for distance work: California Albers, metres, equal area.
METRIC_CRS = "EPSG:3310"
