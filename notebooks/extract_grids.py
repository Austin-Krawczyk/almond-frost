"""Step 4 extraction: gridded baselines at every station for every night. Cached."""
import sys
import time
from pathlib import Path

import ee
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import grids  # noqa: E402
import thermal  # noqa: E402

SEASONS = list(range(2015, 2026))


def main():
    ee.Initialize(project=C.EE_PROJECT)
    st = pd.read_csv(C.DERIVED / "01_cimis_stations.csv")
    keep = pd.read_csv(C.DERIVED / "02_station_nights.csv").station.unique()
    pts = thermal.station_points(st[st.StationNbr.isin(keep)])
    out = C.DERIVED / "04_grid_station_nights.csv"
    if out.exists():
        print(f"{out.name} exists; not rebuilt")
        return
    frames = []
    for name in list(grids.GRIDS) + ["era5land"]:
        for year in SEASONS:
            t0 = time.time()
            df = (grids.era5_season(year, pts) if name == "era5land"
                  else grids.grid_season(name, year, pts))
            frames.append(df)
            n_ok = int(df.tmin_c.notna().sum()) if len(df) else 0
            print(f"  {name:<9} {year}: {len(df):>5} rows, {n_ok:>5} with a value, "
                  f"{time.time() - t0:.0f} s")
    pd.concat(frames, ignore_index=True).to_csv(out, index=False)
    print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
