--Create subcategory table
DROP TABLE d_subcategory;

CREATE TABLE d_subcategory (
    subcategory_id SERIAL NOT NULL PRIMARY KEY,
    subcategory_desc VARCHAR(50) UNIQUE
);

