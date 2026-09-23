"""Gridded baseline extraction at station points (CLAUDE.md §5.3).

Units are read from the Earth Engine catalogue, not assumed: PRISM `tmin` and Daymet `tmin` are
degrees C, gridMET `tmmn` and ERA5-Land `temperature_2m` are kelvin.

**Day conventions differ between products and are tested rather than assumed.** PRISM assets are
timestamped noon UTC rather than midnight, and each provider defines its 24-hour window its own
way, while CIMIS `DayAirTmpMin` is the minimum over the local calendar day. Every product is
therefore extracted at day offsets -1, 0 and +1, and Step 4 reports which alignment minimises
error. ERA5-Land is built from hourly data over the local calendar day (08:00 UTC on day D to
08:00 UTC on D+1), which matches CIMIS by construction.
"""
import ee
import pandas as pd

import common as C

GRIDS = {
    "prism": {"id": C.PRISM, "band": "tmin", "to_c": lambda x: x, "scale": 4000},
    "daymet": {"id": C.DAYMET, "band": "tmin", "to_c": lambda x: x, "scale": 1000},
    "gridmet": {"id": C.GRIDMET, "band": "tmmn", "to_c": lambda x: x - 273.15, "scale": 4000},
}
ERA5_SCALE = 11132


def grid_season(name: str, year: int, pts: ee.FeatureCollection) -> pd.DataFrame:
    """One gridded product, one Feb-Mar season, at every station for every date."""
    g = GRIDS[name]
    col = (ee.ImageCollection(g["id"]).filterDate(f"{year}-01-25", f"{year}-04-05")
           .select([g["band"]]))

    def probe(img):
        # Two bands so ee.Reducer.first() names its outputs after the bands rather than "first".
        stack = img.rename("val").addBands(ee.Image.constant(1).rename("present"))
        return stack.reduceRegions(pts, ee.Reducer.first(), g["scale"]).map(
            lambda f: f.set("date", img.date().format("YYYY-MM-dd")))

    feats = col.map(probe).flatten().getInfo()["features"]
    df = pd.DataFrame([{"grid": name, "station": f["properties"]["station"],
                        "date": f["properties"]["date"],
                        "val": f["properties"].get("val")} for f in feats])
    if not df.empty:
        df["tmin_c"] = g["to_c"](df.val)
    return df


def era5_season(year: int, pts: ee.FeatureCollection) -> pd.DataFrame:
    """ERA5-Land nightly minimum over the local calendar day (08:00 UTC D to 08:00 UTC D+1)."""
    col = (ee.ImageCollection(C.ERA5_LAND).filterDate(f"{year}-01-25", f"{year}-04-05")
           .select(["temperature_2m"]))
    start = ee.Date(f"{year}-02-01")
    n_days = ee.Date(f"{year}-04-01").difference(start, "day")

    def daily(i):
        d0 = start.advance(i, "day").advance(8, "hour")     # 08:00 UTC = 00:00 PST
        img = col.filterDate(d0, d0.advance(1, "day")).min().rename("val")
        return img.addBands(ee.Image.constant(1).rename("present")).set(
            "date", d0.format("YYYY-MM-dd"))

    dc = ee.ImageCollection(ee.List.sequence(0, n_days.subtract(1)).map(daily))
    feats = dc.map(lambda img: img.reduceRegions(pts, ee.Reducer.first(), ERA5_SCALE).map(
        lambda f: f.set("date", img.get("date")))).flatten().getInfo()["features"]
    df = pd.DataFrame([{"grid": "era5land", "station": f["properties"]["station"],
                        "date": f["properties"]["date"],
                        "val": f["properties"].get("val")} for f in feats])
    if not df.empty:
        df["tmin_c"] = df.val - 273.15
    return df
