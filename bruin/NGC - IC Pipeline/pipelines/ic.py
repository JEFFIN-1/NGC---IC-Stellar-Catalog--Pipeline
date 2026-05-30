from pathlib import Path

import pandas as pd
from astroquery.vizier import Vizier

IC_CATALOG_ID = "VII/239A"
RAW_SUBDIR = Path("raw/ic")
RAW_FILENAME = "ic.parquet"
CATALOG_SOURCE = "VII/239A/icdata"


def _find_ic_table(catalog_list):
    for table in catalog_list:
        name = (table.meta.get("name") or "").lower()
        if "icdata" in name:
            return table
    return catalog_list[0]


def fetch_ic_catalog(output_path: Path | None = None) -> Path:
    """Download the IC catalog from Vizier and write it to Parquet."""
    if output_path is None:
        output_path = Path(__file__).resolve().parents[1] / RAW_SUBDIR / RAW_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)

    Vizier.ROW_LIMIT = -1
    vizier = Vizier(columns=["*"], catalog=IC_CATALOG_ID)
    catalog_list = vizier.get_catalogs(IC_CATALOG_ID)
    if len(catalog_list) == 0:
        raise RuntimeError(f"No IC catalog tables returned for {IC_CATALOG_ID}")

    table = _find_ic_table(catalog_list)
    df = table.to_pandas()

    if "NGC/IC" in df.columns:
        df["NGC_IC"] = df["NGC/IC"].astype(str)
    if "_RA.icrs" in df.columns:
        df["RA_icrs"] = df["_RA.icrs"].astype(str)
    if "_DE.icrs" in df.columns:
        df["DE_icrs"] = df["_DE.icrs"].astype(str)

    output_path = Path(output_path)
    df.to_parquet(output_path, index=False)
    return output_path


if __name__ == "__main__":
    output = fetch_ic_catalog()
    print(f"Wrote IC raw catalog to {output}")
