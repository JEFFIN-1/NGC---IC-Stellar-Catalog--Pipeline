# NGC / IC Stellar Catalog Pipeline

This repository contains a Bruin-driven data pipeline that ingests, validates, and warehouses the NGC and IC deep-sky catalogs for downstream analysis in DuckDB.

Quick links:
- Project pipeline folder: [Bruin - NGC + IC Pipeline](Bruin%20-%20NGC%20+%20IC%20Pipeline/README.md)

## Quickstart

Requirements:
- Python 3.10+ (recommended)
- `pip` and a virtual environment tool (optional but recommended)

Install dependencies:

```powershell
cd "Bruin - NGC + IC Pipeline"
python -m pip install -r requirements.txt
```

Run the full pipeline (from the project folder):

```powershell
cd "Bruin - NGC + IC Pipeline"
bruin run .
```

Run only specific assets (ingest or build steps):

```powershell
bruin run assets/ingest_ngc.py
bruin run assets/ingest_ic.py
bruin run assets/ngc_catalog.sql
bruin run assets/ic_catalog.sql
```

## What this pipeline does
- Fetches the NGC and IC catalogs from Vizier using `astroquery`.
- Stores raw catalog extracts as Parquet files (`raw/ngc/...`, `raw/ic/...`).
- Builds normalized warehouse tables in DuckDB using the SQL assets.
- Provides validation assets to assert table quality.

## Data sources and why this pipeline

The pipeline targets two classic astronomical catalogs provided by Vizier:

- NGC (New General Catalogue) — an historical catalog of many deep-sky objects (galaxies, nebulae, clusters) widely used in astronomy.
- IC (Index Catalogue) — a supplement to the NGC containing additional objects and corrections.

Why this pipeline?
- Centralizes catalog ingestion from Vizier for reproducible analysis.
- Normalizes type and coordinate fields for cross-catalog joins and science queries.
- Stores data in Parquet and DuckDB for fast, local analytics.

## Deep Sky Objects (NGC & IC)

This pipeline extracts the standard deep-sky object classes commonly recorded in NGC/IC catalogs. The table below lists the high-level categories, typical catalog `Type` labels, and a short description.

| Category | Typical type labels (NGC/IC) | Description |
|---|---:|---|
| Galaxies | `G`, `Galaxy`, `Sb`, `E` | Large systems of stars, gas, and dark matter; includes morphological subclasses (spiral, elliptical, irregular). |
| Nebulae | `Neb`, `HII`, `Diffuse`, `Reflection` | Emission/Reflection nebulae and large diffuse clouds of gas and dust. |
| Globular clusters | `GC`, `gCl` | Dense, spherical collections of old stars bound gravitationally. |
| Open clusters | `OC`, `Open Cluster` | Loose associations of younger stars within the Galactic disk. |
| Planetary nebulae | `PN` | Ejected shells around evolved low-mass stars; often compact and emission-line dominated. |
| Supernova remnants | `SNR`, `SN remnant` | Expanding shock-heated shells from exploded stars; radio/X-ray bright in many cases. |

Notes:
- Catalog `Type` fields are not standardized across all Vizier sources. The pipeline assets include SQL mapping logic to normalize common labels into the categories above (see the assets SQL files).
- Use the `assets/*_assert.py` validation scripts to confirm the expected columns and types are present in the warehouse tables.

## Pipeline configuration

Configuration and runtime variables are stored in the pipeline YAML (`Bruin - NGC + IC Pipeline/pipeline.yml`). Edit the YAML to change Vizier catalog IDs, output paths, timeouts, or retries.

## Where to look next
- Ingest scripts: `Bruin - NGC + IC Pipeline/assets/ingest_ngc.py`, `assets/ingest_ic.py`
- Warehouse SQL: `Bruin - NGC + IC Pipeline/assets/ngc_catalog.sql`, `assets/ic_catalog.sql`
- Validation: `Bruin - NGC + IC Pipeline/assets/ngc_assert.py`, `assets/ic_assert.py`

If you'd like, I can also add example queries or a short Jupyter notebook demonstrating common queries against the DuckDB warehouse.
