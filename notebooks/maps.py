"""Figure furniture: scale bar, north arrow, and a DEM backdrop for the study-area map."""
from pathlib import Path

import ee
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import requests
from matplotlib.patches import FancyArrow, Rectangle

import common as C


def dem_tif(path, bbox_lonlat, scale_m: int = 500) -> Path:
    """SRTM elevation (m) over `bbox_lonlat`, resampled to `scale_m`. Cached."""
    path = Path(path)
    if path.exists():
        return path
    img = ee.Image("USGS/SRTMGL1_003").rename("elev")
    url = img.getDownloadURL({"region": ee.Geometry.BBox(*bbox_lonlat), "scale": scale_m,
                              "crs": "EPSG:4326", "format": "GEO_TIFF"})
    r = requests.get(url, timeout=900)
    if r.status_code != 200:
        raise RuntimeError(f"Earth Engine download failed ({r.status_code}): {r.text[:300]}")
    path.write_bytes(r.content)
    return path


def read_tif(path):
    with rasterio.open(path) as src:
        arr = src.read(1).astype("float32")
        arr[arr == src.nodata] = np.nan if src.nodata is not None else arr[0, 0]
        b = src.bounds
    return arr, (b.left, b.right, b.bottom, b.top)


def add_scale_bar(ax, length_km: int, x: float = 0.06, y: float = 0.06, lat: float | None = None):
    """Scale bar in axes fraction, for an axis in degrees. `lat` sets the degree-per-km factor."""
    y0, y1 = ax.get_ylim()
    lat = lat if lat is not None else (y0 + y1) / 2
    x0, x1 = ax.get_xlim()
    deg = length_km / (111.32 * np.cos(np.radians(lat)))
    xs = x0 + x * (x1 - x0)
    ys = y0 + y * (y1 - y0)
    ax.add_patch(Rectangle((xs, ys), deg, 0.02 * (y1 - y0), facecolor="k", edgecolor="k", zorder=6))
    ax.text(xs + deg / 2, ys + 0.035 * (y1 - y0), f"{length_km} km", ha="center", va="bottom",
            fontsize=7, zorder=6)


def add_north_arrow(ax, x: float = 0.93, y: float = 0.86):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    xs, ys = x0 + x * (x1 - x0), y0 + y * (y1 - y0)
    dy = 0.07 * (y1 - y0)
    ax.add_patch(FancyArrow(xs, ys, 0, dy, width=0.004 * (x1 - x0), head_width=0.016 * (x1 - x0),
                            head_length=0.3 * dy, facecolor="k", edgecolor="k", zorder=6))
    ax.text(xs, ys + dy * 1.25, "N", ha="center", va="bottom", fontsize=8, fontweight="bold",
            zorder=6)


REGION_COLORS = {"sac_valley": "#1b7837", "sj_north": "#762a83", "sj_south": "#c51b7d"}
