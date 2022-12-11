WITH proc1 AS (
    SELECT
        id AS entry_id,
        extract_date,
        date AS entry_date,
        REGEXP_REPLACE(item, ' ', '_', 'g') AS item,
        REGEXP_REPLACE(amount, '\$', '', 'g') AS amount,
        REGEXP_REPLACE(category, '\s', '', 'g') AS category,
        REGEXP_REPLACE(subcategory, '\s', '_', 'g') AS subcategory,
        REGEXP_REPLACE(vendor, '\s', '_', 'g') AS vendor,
        mel,
        tyler,
        thomas
    FROM {{ source('raw_data', 'raw') }}
),

proc2 AS (
    SELECT
        entry_id,
        CAST(extract_date AS TIMESTAMP) AS extract_date,
        CAST(entry_date AS DATE) AS entry_date,
        REGEXP_REPLACE(REGEXP_REPLACE(item, '\W*', '', 'g'), '__', '_') AS item,
        REGEXP_REPLACE(amount, '\s', '', 'g') AS amount,
        category,
        subcategory,
        REGEXP_REPLACE(vendor, '\W*', '', 'g') AS vendor,
        mel,
        tyler,
        thomas
    FROM proc1
),

proc3 AS (
    SELECT
        entry_id,
        extract_date,
        entry_date,
        LOWER(item) AS item,
        REGEXP_REPLACE(amount, '\(', '-', 'g') AS amount,
        LOWER(category) AS category,
        LOWER(subcategory) AS subcategory,
        LOWER(vendor) AS vendor,
        mel,
        tyler,
        thomas
    FROM proc2
),

proc4 AS (
    SELECT
        entry_id,
        extract_date,
        entry_date,
        item,
        CAST(REGEXP_REPLACE(amount, '\)', '', 'g') AS FLOAT) AS amount,
        category,
        subcategory,
        vendor,
        CAST(mel AS INTEGER) AS mel,
        CAST(tyler AS INTEGER) AS tyler,
        CAST(thomas AS INTEGER) AS thomas
    FROM  proc3
)

SELECT * FROM proc4