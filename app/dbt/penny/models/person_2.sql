SELECT
    entry_id,
    entry_date,
    item,
    category,
    subcategory,
    ((amount / (person_1 + person_2 + person_3)) * person_2) AS amount
FROM {{ ref('fact')}}
WHERE person_2 > 0