"""Pull CIMIS daily minimum air temperature for the almond frost windows.

Scope decision (CLAUDE.md §5.4 asks for hourly and daily): **Step 2 pulls daily only.** The
frost-night calendar is defined from `DayAirTmpMin`, and hourly air temperature is only needed
once the frost nights are known -- at satellite overpass time in Step 4 and across the night in
Step 7. Pulling hourly for the whole window would be ~1.2 million records for data that is mostly
warm nights nobody will look at. Hourly is pulled for the identified frost nights instead.

The app key is a personal credential (CLAUDE.md §9): read from the environment or the gitignored
`.env`, sent only as the `Ocp-Apim-Subscription-Key` header, never printed, committed, or placed
in a URL. Raw JSON responses are cached verbatim in data/raw/cimis/ with a provenance record.

Run:  python download_cimis.py
"""
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cimis  # noqa: E402
import common as C  # noqa: E402

RAW = C.RAW / "cimis"
SEASONS = list(range(2015, 2026))          # 2015..2025, each Feb 1 - Mar 31
WINDOW = ("02-01", "03-31")
MAX_STATIONS_PER_REQUEST = 1750 // 62      # API limit is stations x days; 62 days is the ceiling
STATION_MAX_KM = 20.0                      # "in and adjacent to almond regions" (§5.4)


def selected_stations() -> pd.DataFrame:
    """Stations within STATION_MAX_KM of almond acreage that nominally operated in the window."""
    st = pd.read_csv(C.DERIVED / "01_cimis_stations.csv")
    st["connect"] = pd.to_datetime(st.ConnectDate, format="%m/%d/%Y", errors="coerce")
    st["disconnect"] = pd.to_datetime(st.DisconnectDate, format="%m/%d/%Y", errors="coerce")
    keep = ((st.dist_to_almond_km <= STATION_MAX_KM)
            & (st.connect <= pd.Timestamp(f"{SEASONS[-1]}-{WINDOW[1]}"))
            & (st.disconnect >= pd.Timestamp(f"{SEASONS[0]}-{WINDOW[0]}")))
    return st[keep].copy()


def fetch(stations, year, part, provenance) -> Path:
    """One request: a station chunk for one season. Cached; the raw body is never modified."""
    RAW.mkdir(parents=True, exist_ok=True)
    name = f"daily_tmin_{year}_{part:02d}.json"
    path = RAW / name
    params = {"stationNbrs": ",".join(str(s) for s in stations),
              "startDate": f"{year}-{WINDOW[0]}", "endDate": f"{year}-{WINDOW[1]}",
              "isHourly": "false", "unitOfMeasure": "M", "dataItems": "day-air-tmp-min"}
    if not path.exists():
        blob = cimis.get(cimis.DATA_URL, params)
        path.write_bytes(blob)
        print(f"    {name}: {len(blob):,} bytes")
    blob = path.read_bytes()
    provenance.append({"file": name, "sha256": hashlib.sha256(blob).hexdigest(),
                       "bytes": len(blob), "params": params})
    return path


def main() -> None:
    st = selected_stations()
    numbers = [str(n) for n in st.StationNbr]
    chunks = [numbers[i:i + MAX_STATIONS_PER_REQUEST]
              for i in range(0, len(numbers), MAX_STATIONS_PER_REQUEST)]
    print(f"{len(st)} stations within {STATION_MAX_KM:.0f} km of almond acreage, nominally "
          f"operating {SEASONS[0]}-{SEASONS[-1]}")
    print(f"{len(SEASONS)} seasons x {len(chunks)} station chunks = "
          f"{len(SEASONS) * len(chunks)} requests")

    provenance, files = [], []
    for year in SEASONS:
        print(f"  {year}")
        for part, chunk in enumerate(chunks):
            files.append(fetch(chunk, year, part, provenance))

    # Denominators (CLAUDE.md §9): what was asked for, what came back, what was unusable.
    rows, n_records, flags = [], 0, {}
    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for rec in doc["Data"]["Providers"][0]["Records"]:
            n_records += 1
            item = rec.get("DayAirTmpMin") or {}
            qc = (item.get("Qc") or " ").strip() or "(blank)"
            flags[qc] = flags.get(qc, 0) + 1
            value = item.get("Value")
            rows.append({"station": int(rec["Station"]), "date": rec["Date"],
                         "tmin_c": float(value) if value not in (None, "") else None, "qc": qc})
    df = pd.DataFrame(rows).drop_duplicates(subset=["station", "date"])
    df["date"] = pd.to_datetime(df.date)

    days = sum(pd.date_range(f"{y}-{WINDOW[0]}", f"{y}-{WINDOW[1]}").size for y in SEASONS)
    print(f"\nrecords returned            : {n_records:,}")
    print(f"unique station-nights       : {len(df):,}")
    print(f"maximum possible            : {len(st):,} stations x {days} nights = "
          f"{len(st) * days:,}  ({100 * len(df) / (len(st) * days):.1f}% returned)")
    print(f"with a usable tmin value    : {df.tmin_c.notna().sum():,} "
          f"({100 * df.tmin_c.notna().mean():.1f}% of returned)")
    print(f"missing / null value        : {df.tmin_c.isna().sum():,}")
    print(f"QC flags                    : {dict(sorted(flags.items(), key=lambda kv: -kv[1]))}")

    out = C.DERIVED / "02_cimis_daily_tmin.csv"
    df.sort_values(["station", "date"]).to_csv(out, index=False)
    print(f"\nwrote {out.relative_to(C.ROOT)}")

    (RAW / "SOURCE.md").write_text(
        "# CIMIS daily minimum air temperature — almond frost study\n\n"
        f"Retrieved {pd.Timestamp.today():%Y-%m-%d} for CLAUDE.md §6 Step 2.\n\n"
        f"Station endpoint: {cimis.STATION_URL}\n"
        f"Data endpoint: {cimis.DATA_URL}\n"
        "Authentication: the app key is sent as the `Ocp-Apim-Subscription-Key` HTTP header. "
        "The legacy `appKey` query-parameter API was retired on 31 July 2026. The key is a "
        "personal credential and appears in no file here.\n\n"
        f"Data item `day-air-tmp-min`, `unitOfMeasure=M` (degrees C), `isHourly=false`.\n"
        f"Stations: within {STATION_MAX_KM:.0f} km of DWR 2023 almond acreage and nominally "
        f"operating in the window ({len(st)} stations).\n"
        f"Window: 1 February – 31 March, {SEASONS[0]}–{SEASONS[-1]}.\n\n"
        "## Files\n\n" + "\n".join(
            f"- `{r['file']}` — {r['bytes']:,} bytes, sha256 `{r['sha256']}`, "
            f"stations `{r['params']['stationNbrs']}`, {r['params']['startDate']} to "
            f"{r['params']['endDate']}" for r in provenance) + "\n",
        encoding="utf-8")
    print(f"wrote {(RAW / 'SOURCE.md').relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
