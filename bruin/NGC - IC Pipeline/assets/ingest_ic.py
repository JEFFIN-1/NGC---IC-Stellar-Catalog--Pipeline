"""@bruin
name: ingest_ic
@bruin"""

from pipelines.ic import fetch_ic_catalog


def main() -> None:
    output_path = fetch_ic_catalog()
    print(f"IC raw catalog written to: {output_path}")


if __name__ == "__main__":
    main()
