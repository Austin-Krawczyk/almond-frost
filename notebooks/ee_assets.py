"""Upload the DWR almond field layer to Earth Engine as a reusable asset.

Uploaded in chunks because an inline FeatureCollection of all 45,404 fields exceeds the request
size limit; the chunks are then merged server-side into one asset. DWR geometries carry a Z
coordinate that Earth Engine rejects as invalid GeoJSON, so they are flattened to 2D first --
this changes no planimetric area.
"""
import json
import time

import ee
import geopandas as gpd
from shapely import force_2d

import common as C

FOLDER = f"projects/{C.EE_PROJECT}/assets/almond"
ASSET = f"{FOLDER}/dwr2023_almond_fields"
CHUNK = 4000
# Source attributes only. `study_region` is deliberately NOT uploaded: it is derived from the
# frozen county list in common.py, which has already changed once, and an asset carrying a stale
# derived stratum is exactly the kind of believable-but-wrong value §8 item 10 is about. Region
# is applied at use time by filtering on COUNTY.
PROPS = ["UniqueID", "ACRES", "COUNTY", "HYDRO_RGN", "is_unit", "YR_PLANTED"]


def asset_exists(asset_id: str) -> bool:
    try:
        ee.data.getAsset(asset_id)
        return True
    except ee.EEException:
        return False


def _features(sub: gpd.GeoDataFrame) -> list:
    out = []
    for geom, (_, r) in zip(sub.geometry, sub[PROPS].iterrows()):
        props = {k: (None if v is None else (v.item() if hasattr(v, "item") else v))
                 for k, v in r.items()}
        props = {k: v for k, v in props.items() if v is not None and v != ""}
        out.append(ee.Feature(ee.Geometry(json.loads(json.dumps(geom.__geo_interface__)),
                                          None, False), props))
    return out


def upload(gdf: gpd.GeoDataFrame, timeout_s: int = 2400) -> str:
    """Export `gdf` to ASSET. Returns the asset id. Existing assets are never overwritten."""
    if asset_exists(ASSET):
        print(f"{ASSET} exists; not overwritten")
        return ASSET
    if not asset_exists(FOLDER):
        ee.data.createAsset({"type": "FOLDER"}, FOLDER)

    g = gdf.to_crs("EPSG:4326").copy()
    g["geometry"] = force_2d(g.geometry)
    chunks = [g.iloc[i:i + CHUNK] for i in range(0, len(g), CHUNK)]
    tasks = []
    for i, sub in enumerate(chunks):
        cid = f"{FOLDER}/_chunk{i:02d}"
        if asset_exists(cid):
            print(f"  chunk {i:02d}: exists")
            continue
        t = ee.batch.Export.table.toAsset(collection=ee.FeatureCollection(_features(sub)),
                                          description=f"almond_chunk{i:02d}", assetId=cid)
        t.start()
        tasks.append((i, cid, t))
    print(f"  {len(tasks)} chunk export(s) started, {len(chunks)} chunks total")

    t0 = time.time()
    failed = []
    while tasks and time.time() - t0 < timeout_s:
        time.sleep(20)
        still = []
        for i, cid, t in tasks:
            st = t.status()["state"]
            if st in ("UNSUBMITTED", "READY", "RUNNING"):
                still.append((i, cid, t))
            elif st != "COMPLETED":
                failed.append((i, st, t.status().get("error_message", "")))
            else:
                print(f"  chunk {i:02d}: COMPLETED at {time.time() - t0:.0f} s")
        tasks = still
    # Fail loudly: a chunk that silently vanished would shrink the unit table invisibly (§9).
    if tasks:
        raise RuntimeError(f"chunk exports still running after {timeout_s} s: "
                           f"{[c for _, c, _ in tasks]}")
    if failed:
        raise RuntimeError(f"chunk exports failed: {failed}")

    merged = ee.FeatureCollection([ee.FeatureCollection(f"{FOLDER}/_chunk{i:02d}")
                                   for i in range(len(chunks))]).flatten()
    task = ee.batch.Export.table.toAsset(collection=merged, description="almond_fields_merge",
                                         assetId=ASSET)
    task.start()
    t0 = time.time()
    while task.status()["state"] in ("UNSUBMITTED", "READY", "RUNNING") and time.time() - t0 < timeout_s:
        time.sleep(20)
    if task.status()["state"] != "COMPLETED":
        raise RuntimeError(f"merge export did not complete: {task.status()}")
    print(f"  merged in {time.time() - t0:.0f} s")

    n = ee.FeatureCollection(ASSET).size().getInfo()
    if n != len(g):
        raise RuntimeError(f"asset has {n} features, expected {len(g)}")
    print(f"{ASSET}: {n} features (matches the {len(g)} fields read from DWR)")
    return ASSET
