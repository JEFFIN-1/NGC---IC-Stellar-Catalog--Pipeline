CREATE OR REPLACE TABLE ngc_catalog AS
SELECT
    TRY_CAST(NGC AS INTEGER) AS NGC,
    NULL::INTEGER AS IC,
    NULL::VARCHAR AS Name,
    RA_icrs AS RA,
    DE_icrs AS DEC,
    NULL::DOUBLE AS GLON,
    NULL::DOUBLE AS GLAT,
    "Type" AS Type,
    TRY_CAST(Mag AS DOUBLE) AS Mag,
    NULL::DOUBLE AS BMag,
    NULL::DOUBLE AS VMag,
    NULL::VARCHAR AS SizeMax,
    NULL::VARCHAR AS SizeMin,
    NULL::VARCHAR AS PA,
    NULL::VARCHAR AS Constellation,
    NULL::VARCHAR AS Morphology,
    NULL::VARCHAR AS SurfaceBrightness,
    Notes AS Notes,
    NULL::VARCHAR AS Discoverer,
    2000.0 AS Epoch,
    'VII/1B/catalog' AS CatalogSource
FROM read_parquet('raw/ngc/ngc.parquet');
