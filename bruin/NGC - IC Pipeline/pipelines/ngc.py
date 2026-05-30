from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier

NGC_CATALOG_ID = "VII/1B"
RAW_SUBDIR = Path("raw/ngc")
RAW_FILENAME = "ngc.parquet"
CATALOG_SOURCE = "VII/1B/catalog"


def fetch_ngc_catalog(output_path: Path | None = None) -> Path:
    """Download the NGC catalog from Vizier and write it to Parquet."""
    if output_path is None:
        output_path = Path(__file__).resolve().parents[1] / RAW_SUBDIR / RAW_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)

    Vizier.ROW_LIMIT = -1
    vizier = Vizier(columns=["*"], catalog=NGC_CATALOG_ID)
    catalog_list = vizier.get_catalogs(NGC_CATALOG_ID)
    if len(catalog_list) == 0:
        raise RuntimeError(f"No NGC catalog tables returned for {NGC_CATALOG_ID}")

    table = catalog_list[0]
    df = table.to_pandas()

    # Convert angle columns to strings so SQL can use them consistently.
    if "_RA.icrs" in df.columns:
        df["RA_icrs"] = df["_RA.icrs"].astype(str)
    if "_DE.icrs" in df.columns:
        df["DE_icrs"] = df["_DE.icrs"].astype(str)

    output_path = Path(output_path)
    df.to_parquet(output_path, index=False)
    return output_path


if __name__ == "__main__":
    output = fetch_ngc_catalog()
    print(f"Wrote NGC raw catalog to {output}")
