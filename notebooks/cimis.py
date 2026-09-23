"""CIMIS station metadata and daily/hourly pulls.

Endpoint note, re-verified rather than inherited: the legacy Web API (`/api/data`, key as the
`appKey` query parameter) was retired on 31 July 2026 and requests carrying `appKey` are rejected
by the site firewall whatever the key's value. The current endpoints sit behind Azure API
Management and take the key as an HTTP header.

  stations  https://et.water.ca.gov/StationWeb/GetAllStations
  data      https://et.water.ca.gov/StationWeb/GetDataByStationNumber
  header    Ocp-Apim-Subscription-Key: <app key>

The app key is a personal credential (CLAUDE.md §9). It is read from the environment or the
gitignored `.env`, sent only as a header, and never printed, committed, or put in a URL.
"""
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

import common as C

STATION_URL = "https://et.water.ca.gov/StationWeb/GetAllStations"
DATA_URL = "https://et.water.ca.gov/StationWeb/GetDataByStationNumber"
MAX_RECORDS = 1750            # documented API limit: stations x days per request
RAW = C.RAW / "cimis"
KEY_NAMES = {"cimis_app_key", "cimis_appkey", "cimis_key"}


def app_key() -> str:
    """Environment first (any casing), then the gitignored `.env` at the repo root."""
    for name, value in os.environ.items():
        if name.lower() in KEY_NAMES and value.strip():
            return value.strip()
    env = C.ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            name, _, value = line.strip().partition("=")
            if name.strip().lower() in KEY_NAMES:
                return value.strip().strip('"').strip("'")
    raise SystemExit(
        "No CIMIS app key found. Checked the environment (CIMIS_APP_KEY, any casing) and "
        f"{C.ROOT / '.env'}. Both are gitignored; the key is never printed or committed.")


def get(url: str, params: dict | None = None) -> bytes:
    """The key goes in the Azure APIM header. It never appears in the URL."""
    q = urllib.parse.urlencode(params or {})
    req = urllib.request.Request(
        f"{url}?{q}" if q else url,
        headers={"Accept": "application/json", "Ocp-Apim-Subscription-Key": app_key()})
    with urllib.request.urlopen(req, timeout=300) as r:
        body = r.read()
    if body.lstrip()[:1] not in (b"{", b"["):
        raise RuntimeError(f"Non-JSON response from {url} ({len(body)} bytes); request rejected. "
                           "The key is sent as a header and is not in the URL.")
    return body


def decimal_from_hms(s: str) -> float | None:
    """`HmsLatitude` looks like "36\u00ba20'10N / 36.3360"; take the decimal after the slash."""
    m = re.search(r"/\s*(-?\d+\.\d+)", s or "")
    return float(m.group(1)) if m else None


def fetch_stations(cache: str = "stations_all.json") -> list[dict]:
    """All CIMIS stations with metadata. Raw JSON cached verbatim in data/raw/cimis/."""
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / cache
    if not path.exists():
        blob = get(STATION_URL)
        path.write_bytes(blob)
        print(f"  fetched {cache}: {len(blob):,} bytes, "
              f"sha256 {hashlib.sha256(blob).hexdigest()[:16]}...")
    return json.loads(path.read_text(encoding="utf-8"))["Stations"]
