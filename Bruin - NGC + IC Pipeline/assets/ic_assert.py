"""@bruin
name: ic_assert
@bruin"""

from pathlib import Path

import duckdb


def main() -> None:
    db_path = Path(__file__).resolve().parents[1] / "warehouse" / "bruin.duckdb"
    conn = duckdb.connect(database=str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ic_catalog")
        row_count = cursor.fetchone()[0]
        assert row_count > 0, "ic_catalog must contain at least one row."

        cursor.execute("PRAGMA table_info('ic_catalog')")
        columns = [row[1] for row in cursor.fetchall()]
        required_columns = [
            "NGC",
            "IC",
            "Name",
            "RA",
            "DEC",
            "Type",
            "Notes",
            "Epoch",
            "CatalogSource",
        ]
        for col in required_columns:
            assert col in columns, f"Missing required column in ic_catalog: {col}"

        print(f"IC assert passed: {row_count} rows and required columns present.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
