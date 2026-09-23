"""Per-station-night extraction of satellite LST and each product's own QC.

Screens use the products' own quality flags, read from the Earth Engine catalogue's bitmask
definitions (CLAUDE.md §6 Step 3: "use the product's own QC flags, do not invent a screen").

**MODIS QC quirk, verified not assumed.** In `MOD11A1`/`MYD11A1` the `QC_Night` band is *masked*
wherever its value is 0 — that is, wherever the retrieval is best quality. Over one test season,
station-nights split (LST present, QC present) as 705/(1,0), 716/(0,1), 343/(1,1) with **no case
of both missing**, and `unmask(0)` returned 0 for all 705. Reading a masked QC as "unusable" would
therefore discard two-thirds of the valid retrievals, and precisely the best ones — the same shape
as the CIMIS flag trap in §8 item 10. MODIS QC is read with `.unmask(0)`. VIIRS never masks its
`QC` band; the same call is harmless there.
"""
import ee
import pandas as pd

import common as C

# Night for ECOSTRESS: local 18:00–06:00 PST is 02:00–14:00 UTC.
ECO_NIGHT_UTC = (2, 13)

PRODUCTS = {
    "terra": {"id": C.MODIS_TERRA_LST, "lst": "LST_Night_1km", "qc": "QC_Night",
              "vt": "Night_view_time", "lst_scale": 0.02, "vt_scale": 0.1},
    "aqua": {"id": C.MODIS_AQUA_LST, "lst": "LST_Night_1km", "qc": "QC_Night",
             "vt": "Night_view_time", "lst_scale": 0.02, "vt_scale": 0.1},
    "viirs": {"id": C.VIIRS_LST, "lst": "LST_1KM", "qc": "QC", "vt": "View_Time",
              "lst_scale": 1.0, "vt_scale": 1.0},
}


def station_points(stations: pd.DataFrame) -> ee.FeatureCollection:
    return ee.FeatureCollection([
        ee.Feature(ee.Geometry.Point([float(r.lon), float(r.lat)]), {"station": int(r.StationNbr)})
        for r in stations.itertuples()])


def polar_season(product: str, year: int, pts: ee.FeatureCollection) -> pd.DataFrame:
    """One product, one Feb–Mar season: LST, QC and view time at every station, every date."""
    p = PRODUCTS[product]
    col = ee.ImageCollection(p["id"]).filterDate(f"{year}-02-01", f"{year}-04-01")

    def probe(img):
        qc = img.select(p["qc"]).unmask(0)            # see the module docstring
        stack = ee.Image.cat(
            img.select(p["lst"]).rename("lst_raw"),
            qc.rename("qc"),
            img.select(p["vt"]).unmask(-1).rename("view_time"))
        return stack.reduceRegions(pts, ee.Reducer.first(), 1000).map(
            lambda f: f.set("date", img.date().format("YYYY-MM-dd")))

    feats = col.map(probe).flatten().getInfo()["features"]
    rows = [{"product": product, "station": f["properties"]["station"],
             "date": f["properties"]["date"],
             "lst_raw": f["properties"].get("lst_raw"),
             "qc": f["properties"].get("qc", 0),
             "view_time": f["properties"].get("view_time", -1)} for f in feats]
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["lst_k"] = df.lst_raw * p["lst_scale"]
    df["lst_c"] = df.lst_k - 273.15
    df["view_time_h"] = df.view_time.where(df.view_time >= 0) * p["vt_scale"]
    # Mandatory QA, bits 0–1: 0 = produced, good quality; 1 = produced, other quality;
    # 2 = not produced due to cloud; 3 = not produced for other reasons.
    df["qa"] = df.qc.fillna(0).astype(int) & 3
    df["produced"] = df.lst_raw.notna()
    df["good"] = df.produced & (df.qa == 0)
    return df


def eco_season(year: int, pts: ee.FeatureCollection) -> pd.DataFrame:
    """ECOSTRESS night availability per station-date: good quality and clear sky, any scene."""
    col = (ee.ImageCollection(C.ECOSTRESS).filterDate(f"{year}-02-01", f"{year}-04-01")
           .filterBounds(pts.geometry())
           .filter(ee.Filter.calendarRange(ECO_NIGHT_UTC[0], ECO_NIGHT_UTC[1], "hour")))
    start = ee.Date(f"{year}-02-01")
    n_days = ee.Date(f"{year}-04-01").difference(start, "day")

    def daily(i):
        d0 = start.advance(i, "day")
        sub = col.filterDate(d0, d0.advance(1, "day"))
        # QC bit 0: 0 = good quality. QC bit 3: 0 = clear sky.
        # Two layers, so the deficit can be split into "swath missed the station" and
        # "swath covered it but the QC screen rejected it".
        raw = sub.map(lambda im: im.select("LST"))
        good = sub.map(lambda im: im.select("LST").updateMask(
            im.select("QC").bitwiseAnd(1).eq(0)
            .And(im.select("QC").rightShift(3).bitwiseAnd(1).eq(0))))
        # An empty date mosaics to a band-less image, which reduceRegions rejects.
        img = ee.Image(ee.Algorithms.If(
            sub.size().gt(0),
            good.mosaic().rename("eco_lst").addBands(raw.mosaic().rename("eco_raw")),
            ee.Image.constant(0).rename("eco_lst").selfMask()
              .addBands(ee.Image.constant(0).rename("eco_raw").selfMask())))
        return img.set("date", d0.format("YYYY-MM-dd"), "scenes", sub.size())

    # setOutputs is not cosmetic: on a SINGLE-band image ee.Reducer.first() names its output
    # "first", not the band name, so reading the band name back returns None for every row and
    # the extraction reports a believable zero. MODIS and VIIRS avoid this only because they are
    # reduced as multi-band stacks, where outputs do take the band names.
    # Multi-band now, so ee.Reducer.first() names outputs after the bands.
    reducer = ee.Reducer.first()

    dc = ee.ImageCollection(ee.List.sequence(0, n_days.subtract(1)).map(daily))
    feats = dc.map(lambda img: img.reduceRegions(pts, reducer, 70).map(
        lambda f: f.set("date", img.get("date"), "scenes", img.get("scenes")))
    ).flatten().getInfo()["features"]
    return pd.DataFrame([{"product": "ecostress", "station": f["properties"]["station"],
                          "date": f["properties"]["date"],
                          "scenes": f["properties"].get("scenes", 0),
                          "lst_k": f["properties"].get("eco_lst"),
                          "lst_raw_k": f["properties"].get("eco_raw")} for f in feats])


def goes_season(year: int, pts: ee.FeatureCollection, utc_hour: int = 9) -> pd.DataFrame:
    """GOES-18 availability at a fixed reference hour (default 09:00 UTC = 01:00 PST).

    A fixed hour is used so the figure is comparable with the ~01:30 polar overpass rather than
    being a statement about how many of the day's 288 scenes were clear. `DQF_C13` = 0 is good.
    """
    col = (ee.ImageCollection(C.GOES18).filterDate(f"{year}-02-01", f"{year}-04-01")
           .filter(ee.Filter.calendarRange(utc_hour, utc_hour, "hour"))
           .filter(ee.Filter.calendarRange(0, 5, "minute")))
    if col.size().getInfo() == 0:
        return pd.DataFrame()

    def probe(img):
        # CMI bands are stored as scaled integers with a PER-IMAGE scale and offset carried as
        # image properties. The catalogue lists the band's units as K with no scale factor, and
        # the raw values (1,980-3,218) are obviously not kelvin -- but a guessed x0.1 would give
        # 198-322 K, a believable range that is silently wrong. Read the image's own properties.
        scale = ee.Number(img.get("CMI_C13_scale"))
        offset = ee.Number(img.get("CMI_C13_offset"))
        stack = ee.Image.cat(
            img.select("CMI_C13").multiply(scale).add(offset).rename("bt_k"),
            img.select("DQF_C13").unmask(-1).rename("dqf"))
        return stack.reduceRegions(pts, ee.Reducer.first(), 2000).map(
            lambda f: f.set("date", img.date().format("YYYY-MM-dd")))

    feats = col.map(probe).flatten().getInfo()["features"]
    return pd.DataFrame([{"product": "goes18", "station": f["properties"]["station"],
                          "date": f["properties"]["date"],
                          "bt_k": f["properties"].get("bt_k"),
                          "dqf": f["properties"].get("dqf", 0)} for f in feats])
