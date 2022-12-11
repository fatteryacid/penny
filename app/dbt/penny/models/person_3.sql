SELECT
    entry_id,
    entry_date,
    item,
    category,
    subcategory,
    ((amount / (person_1 + person_2 + person_3)) * person_3) AS amount
FROM {{ ref('fact')}}
WHERE person_3 > 0