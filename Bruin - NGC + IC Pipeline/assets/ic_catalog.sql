CREATE OR REPLACE TABLE ic_catalog AS
SELECT
    NULL::INTEGER AS NGC,
    TRY_CAST(REGEXP_REPLACE(NGC_IC, '[^0-9]', '') AS INTEGER) AS IC,
    NULL::VARCHAR AS Name,
    RA_icrs AS RA,
    DE_icrs AS DEC,
    NULL::DOUBLE AS GLON,
    NULL::DOUBLE AS GLAT,
    NULL::VARCHAR AS Type,
    NULL::DOUBLE AS Mag,
    NULL::DOUBLE AS BMag,
    NULL::DOUBLE AS VMag,
    NULL::VARCHAR AS SizeMax,
    NULL::VARCHAR AS SizeMin,
    NULL::VARCHAR AS PA,
    NULL::VARCHAR AS Constellation,
    NULL::VARCHAR AS Morphology,
    NULL::VARCHAR AS SurfaceBrightness,
    Comm AS Notes,
    NULL::VARCHAR AS Discoverer,
    2000.0 AS Epoch,
    'VII/239A/icdata' AS CatalogSource
FROM read_parquet('raw/ic/ic.parquet');
