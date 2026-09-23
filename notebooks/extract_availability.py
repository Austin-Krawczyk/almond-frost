"""Step 3 extraction: satellite availability at every station for every night of the window.

Writes data/derived/03_polar_station_nights.csv, 03_eco_station_nights.csv and
03_goes_station_nights.csv. Cached: an existing file is not rebuilt.
Run:  python extract_availability.py
"""
import sys
import time
from pathlib import Path

import ee
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import thermal  # noqa: E402

SEASONS = list(range(2015, 2026))


def main():
    ee.Initialize(project=C.EE_PROJECT)
    st = pd.read_csv(C.DERIVED / "01_cimis_stations.csv")
    keep = pd.read_csv(C.DERIVED / "02_station_nights.csv").station.unique()
    st = st[st.StationNbr.isin(keep)]
    pts = thermal.station_points(st)
    print(f"{len(st)} stations, {len(SEASONS)} seasons")

    out = C.DERIVED / "03_polar_station_nights.csv"
    if not out.exists():
        frames = []
        for product in thermal.PRODUCTS:
            for year in SEASONS:
                t0 = time.time()
                df = thermal.polar_season(product, year, pts)
                frames.append(df)
                print(f"  {product:<6} {year}: {len(df):>5} rows, "
                      f"{int(df.good.sum()) if len(df) else 0:>4} good, {time.time() - t0:.0f} s")
        pd.concat(frames, ignore_index=True).to_csv(out, index=False)
        print(f"wrote {out.name}")

    out = C.DERIVED / "03_eco_station_nights.csv"
    if not out.exists():
        frames = []
        for year in SEASONS:
            t0 = time.time()
            df = thermal.eco_season(year, pts)
            frames.append(df)
            print(f"  eco   {year}: {len(df):>5} rows, "
                  f"{int(df.lst_k.notna().sum()) if len(df) else 0:>4} with LST, "
                  f"{time.time() - t0:.0f} s")
        pd.concat(frames, ignore_index=True).to_csv(out, index=False)
        print(f"wrote {out.name}")

    out = C.DERIVED / "03_goes_station_nights.csv"
    if not out.exists():
        frames = []
        for year in SEASONS:
            t0 = time.time()
            df = thermal.goes_season(year, pts)
            frames.append(df)
            print(f"  goes  {year}: {len(df):>5} rows, {time.time() - t0:.0f} s")
        pd.concat(frames, ignore_index=True).to_csv(out, index=False)
        print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
