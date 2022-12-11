SELECT
    entry_id,
    entry_date,
    item,
    category,
    subcategory,
    ((amount / (person_1 + person_2 + person_3)) * person_1) AS amount
FROM {{ ref('fact')}}
WHERE person_1 > 0