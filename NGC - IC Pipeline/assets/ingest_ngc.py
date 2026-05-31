"""@bruin
name: ingest_ngc
@bruin"""

from pipelines.ngc import fetch_ngc_catalog


def main() -> None:
    output_path = fetch_ngc_catalog()
    print(f"NGC raw catalog written to: {output_path}")


if __name__ == "__main__":
    main()
