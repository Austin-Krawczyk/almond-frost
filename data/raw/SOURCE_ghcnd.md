# GHCN-Daily station list

`ghcnd-stations.txt`, retrieved 2026-09-23 from
https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt (11,395,258 bytes).

Used in §5.3a and Step 5 to establish that **CIMIS does not feed GHCN-Daily**, and therefore that
Daymet V4 — whose core input is GHCN-Daily — is independent of the stations this study scores
products against. The accompanying `readme.txt` at the same location carries the complete
source-flag list, which contains no CIMIS or Californian agricultural network.

Measured from this file: 3,241 GHCN-D stations in California, none named CIMIS; the median
distance from each of the 63 CIMIS stations used here to the nearest GHCN-D station is 5,604 m,
with 1 of 63 within 200 m and 3 within 1 km.

The file is gitignored because it is large and re-downloadable; this record is the provenance.
