--Create category table
DROP TABLE d_category;

CREATE TABLE d_category (
    category_id SERIAL NOT NULL PRIMARY KEY,
    category_desc VARCHAR(50) UNIQUE
);

