# Bruin - NGC / IC Astroquery Pipeline

This Bruin pipeline ingests the NGC and IC catalogs from Vizier using `astroquery`, stores raw catalog data as Parquet, and builds warehouse tables in DuckDB.

## Pipeline assets
- `assets/ingest_ngc.py` — fetches the NGC catalog from Vizier and writes `raw/ngc/ngc.parquet`
- `assets/ingest_ic.py` — fetches the IC catalog from Vizier and writes `raw/ic/ic.parquet`
- `assets/ngc_catalog.sql` — creates `ngc_catalog` from the NGC raw Parquet file
- `assets/ic_catalog.sql` — creates `ic_catalog` from the IC raw Parquet file
- `assets/ngc_assert.py` — validates the final NGC warehouse table
- `assets/ic_assert.py` — validates the final IC warehouse table

## Setup
Install the pipeline dependencies:

```powershell
cd bruin-pipeline
python -m pip install -r requirements.txt
```

## Running the pipeline

Run the entire pipeline from the `bruin-pipeline` directory:

```powershell
cd bruin-pipeline
bruin run .
```

If you want to execute only the ingestion assets:

```powershell
bruin run assets/ingest_ngc.py
bruin run assets/ingest_ic.py
```

To build the SQL warehouse tables:

```powershell
bruin run assets/ngc_catalog.sql
bruin run assets/ic_catalog.sql
```

To validate the converted warehouse tables:

```powershell
bruin run assets/ngc_assert.py
bruin run assets/ic_assert.py
```

## Data paths
- Raw NGC catalog: `raw/ngc/ngc.parquet`
- Raw IC catalog: `raw/ic/ic.parquet`
- DuckDB warehouse file: `warehouse/bruin.duckdb`

## Columns included
The final catalog assets expose the requested fields where available, including:
- `NGC`
- `IC`
- `Name`
- `RA`
- `DEC`
- `Type`
- `Mag`
- `Notes`
- `Epoch`
- `CatalogSource`

Additional columns such as `BMag`, `VMag`, `SizeMax`, `SizeMin`, `PA`, `Constellation`, `Morphology`, and `SurfaceBrightness` are defined in the warehouse assets for later extension.

## Notes
- This pipeline uses Vizier catalogs `VII/1B` for NGC and `VII/239A` for IC.
- Raw catalog files are written as Parquet for reliable downstream DuckDB usage.

## Deep Sky Objects (catalog mapping)

The pipeline normalizes common deep-sky object classes found in NGC/IC into a small set of categories used by the warehouse tables. Below is the canonical list and a short mapping example that illustrates how the SQL assets map raw `Type` values into normalized categories.

| Category | Example raw `Type` values |
|---|---|
| Galaxies | `G`, `Galaxy`, `Sb`, `E`, `S` |
| Nebulae | `Neb`, `HII`, `diffuse`, `reflection` |
| Globular clusters | `GC`, `gCl` |
| Open clusters | `OC`, `Open Cluster` |
| Planetary nebulae | `PN` |
| Supernova remnants | `SNR`, `SN remnant` |

Example SQL mapping (informational):

```sql
CASE
	WHEN lower(type) LIKE '%galaxy%' OR type IN ('G','Sb','E') THEN 'Galaxy'
	WHEN lower(type) LIKE '%neb%' OR lower(type) LIKE '%hii%' THEN 'Nebula'
	WHEN lower(type) LIKE '%glob%' OR type = 'GC' THEN 'Globular Cluster'
	WHEN lower(type) LIKE '%open%' OR type = 'OC' THEN 'Open Cluster'
	WHEN type = 'PN' THEN 'Planetary Nebula'
	WHEN lower(type) LIKE '%sn%' OR type = 'SNR' THEN 'Supernova Remnant'
	ELSE 'Other'
END AS normalized_type
```

This mapping is implemented in the SQL assets and can be adjusted to suit specific classification rules or scientific needs.

