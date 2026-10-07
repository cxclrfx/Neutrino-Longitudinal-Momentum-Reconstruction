# CMS Open Data input

Source: Thomas McCauley, **W to muon and neutrino 2011**, CERN Open Data Portal,
[record 5205](https://opendata.cern.ch/record/5205), published 2019; CMS data recorded
in 2011, derived from Run2011A SingleMu. Parent collection: [545](https://opendata.cern.ch/record/545).
The historical `cms-5205` identifier in the scientific README refers to this record.
The canonical numeric record URL is used for acquisition.

The official [record API](https://opendata.cern.ch/api/records/5205) was retrieved
on 2026-10-07; its exact response is stored in
[evidence/cern-record-5205.json](../evidence/cern-record-5205.json).

| Property | Verified value | Basis |
|---|---|---|
| File | `Wmunu.csv` | CERN metadata and download |
| Events | 100000 | CERN record and parsed CSV rows |
| Bytes | 7969331 | CERN metadata and actual bytes |
| Adler-32 | `0607d5ee` | CERN metadata and local computation |
| SHA-256 | `8031d7f62935b75e02f066caf8d20e7661f98effe18dcc25b63c604bd158b04d` | Locally computed; not represented as a CERN-published SHA-256 |

Download and verify from the repository root:

```sh
python scripts/verify_input.py data/Wmunu.csv --download
python scripts/verify_input.py data/Wmunu.csv
```

The download uses [the official HTTPS file](https://opendata.cern.ch/record/5205/files/Wmunu.csv),
not a mirror. The API also identifies its EOS source as
`root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleMu/CSV/12Oct2013-v1/files/Wmunu.csv`.
Existing input is never overwritten. A differing official future file requires
an explicit provenance update, not disabling verification.

Columns, source selection, and physical interpretation are described in the root
README. We analyze all rows without additional cuts. The second-muon veto is
source metadata: it cannot be re-established from this reduced single-muon CSV.
The CSV contains no true neutrino longitudinal momentum.

Data and source-record metadata: **CC0-1.0**; see the official record and
[CC0 legal text](https://creativecommons.org/publicdomain/zero/1.0/legalcode).
No ownership of CMS/CERN data is claimed. Neither CMS nor CERN endorses this work.
The sample was prepared for education and outreach, not full precision analysis.

The downloaded CSV and full per-event derived tables are intentionally excluded
from Git: acquisition and verification avoid duplicating third-party data, while
small summaries and reproducible figures are versioned. The software license does
not replace the data license.
