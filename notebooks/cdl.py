"""CDL helpers: server-side area counts, and native-grid raster downloads.

CDL is a comparison layer only (CLAUDE.md §5.1). It is never the unit definition.
"""
from pathlib import Path

import ee
import numpy as np
import rasterio
import requests
from rasterio.merge import merge

import common as C


def cdl_image(year: int = C.CDL_YEAR) -> ee.Image:
    col = ee.ImageCollection(C.CDL).filterDate(f"{year}-01-01", f"{year + 1}-01-01")
    n = col.size().getInfo()
    assert n == 1, f"expected 1 CDL image for {year}, found {n}"
    return col.first().select("cropland")


def native_tif(img: ee.Image, path, bbox_lonlat, proj_image=None, n_tiles: int = 6) -> Path:
    """Download a single-band uint8 image on `proj_image`'s native grid, as a GeoTIFF.

    Split into `n_tiles` west-east strips to stay under Earth Engine's per-request download
    limit, then merged. Cached: returns immediately if `path` exists.
    """
    path = Path(path)
    if path.exists():
        return path
    proj = (proj_image or img).projection().getInfo()
    crs = proj.get("crs") or proj["wkt"]

    w, s, e, n = bbox_lonlat
    edges = np.linspace(w, e, n_tiles + 1)
    parts = []
    for i in range(n_tiles):
        url = img.getDownloadURL({
            "region": ee.Geometry.BBox(edges[i], s, edges[i + 1], n),
            "crs": crs, "crs_transform": proj["transform"], "format": "GEO_TIFF",
        })
        resp = requests.get(url, timeout=1800)
        if resp.status_code != 200:
            raise RuntimeError(f"Earth Engine download failed ({resp.status_code}): {resp.text[:500]}")
        part = path.with_name(f"{path.stem}_part{i}.tif")
        part.write_bytes(resp.content)
        parts.append(part)
        print(f"    tile {i + 1}/{n_tiles}: {len(resp.content) / 1e6:.1f} MB")

    srcs = [rasterio.open(p) for p in parts]
    try:
        mosaic, transform = merge(srcs, method="max")
        profile = srcs[0].profile | {"height": mosaic.shape[1], "width": mosaic.shape[2],
                                     "transform": transform, "compress": "deflate"}
        with rasterio.open(path, "w", **profile) as dst:
            dst.write(mosaic)
    finally:
        for s_ in srcs:
            s_.close()
        for p in parts:
            p.unlink()
    return path


def almond_mask_tif(path, bbox_lonlat, year: int = C.CDL_YEAR, n_tiles: int = 6) -> Path:
    """0/1 uint8 GeoTIFF of CDL almonds (class 75) on CDL's native 30 m grid."""
    img = cdl_image(year)
    return native_tif(img.eq(C.CDL_ALMOND).toByte(), path, bbox_lonlat, proj_image=img,
                      n_tiles=n_tiles)


ACRE_M2 = 4046.8564224


def county_geometry(counties) -> ee.Geometry:
    """Dissolved TIGER 2018 county polygons for the named California counties."""
    fc = (ee.FeatureCollection("TIGER/2018/Counties")
          .filter(ee.Filter.eq("STATEFP", "06"))
          .filter(ee.Filter.inList("NAME", list(counties))))
    n = fc.size().getInfo()
    if n != len(counties):
        raise RuntimeError(f"TIGER returned {n} counties for {len(counties)} names: "
                           f"{sorted(set(counties) - set(fc.aggregate_array('NAME').getInfo()))}")
    return fc.geometry()


def dwr_overlap(asset: str, region: str, year: int = C.CDL_YEAR) -> dict:
    """Rasterised area of DWR units in `region`, and how much of it CDL calls almonds.

    The region is applied by filtering on COUNTY against the frozen county list, not on a
    `study_region` attribute stored in the asset -- see the note in ee_assets.PROPS.

    Both numbers come from the same 30 m grid, so they are directly comparable; DWR `ACRES`
    (whole-polygon area) is reported alongside as the vector-side figure.
    """
    cdl = cdl_image(year)
    px = ee.Image.pixelArea().rename("dwr_m2").addBands(
        cdl.eq(C.CDL_ALMOND).multiply(ee.Image.pixelArea()).rename("cdl_almond_m2"))
    fc = (ee.FeatureCollection(asset).filter(ee.Filter.eq("is_unit", 1))
          .filter(ee.Filter.inList("COUNTY", sorted(C.REGION_COUNTIES[region]))))
    stats = px.reduceRegions(fc, ee.Reducer.sum(), 30)
    out = stats.reduceColumns(ee.Reducer.sum().repeat(2),
                              ["dwr_m2", "cdl_almond_m2"]).getInfo()["sum"]
    return {"region": region, "n_units": fc.size().getInfo(),
            "dwr_acres_30m": out[0] / ACRE_M2, "cdl_almond_in_dwr_acres": out[1] / ACRE_M2}


def cdl_almond_in_counties(counties, year: int = C.CDL_YEAR) -> float:
    """Total CDL almond acreage inside the named counties: the denominator for direction 2."""
    cdl = cdl_image(year)
    m2 = cdl.eq(C.CDL_ALMOND).multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(), geometry=county_geometry(counties), scale=30,
        maxPixels=1e13, bestEffort=False).getInfo()["cropland"]
    return m2 / ACRE_M2


def cdl_almond_statewide(year: int = C.CDL_YEAR) -> float:
    """Total CDL almond acreage in California, for scale against the study-county total."""
    ca = (ee.FeatureCollection("TIGER/2018/States")
          .filter(ee.Filter.eq("NAME", "California")).geometry())
    m2 = cdl_image(year).eq(C.CDL_ALMOND).multiply(ee.Image.pixelArea()).reduceRegion(
        reducer=ee.Reducer.sum(), geometry=ca, scale=30, maxPixels=1e13,
        bestEffort=False).getInfo()["cropland"]
    return m2 / ACRE_M2
