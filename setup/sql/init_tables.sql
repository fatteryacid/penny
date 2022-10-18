-- script to be ran for creating table

-- Category & Subcategory group
CREATE TABLE d_category (
    category_id SERIAL NOT NULL,
    category_desc VARCHAR(50),
    PRIMARY KEY category_id
);

CREATE TABLE d_subcategory (
    subcategory_id SERIAL NOT NULL,
    subcategory_desc VARCHAR(75),
    PRIMARY KEY subcategory_id
);

CREATE TABLE d_category_subcategory (
    category_relation_id SERIAL NOT NULL,
    category_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    PRIMARY KEY category_relation_id,
    FOREIGN KEY category_id REFERENCES d_category(category_id),
    FOREIGN KEY subcategory_id REFERENCES d_subcategory(subcategory_id)
);


-- Vendor group
CREATE TABLE d_vendor (
    vendor_id SERIAL NOT NULL,
    vendor_desc VARCHAR(100),
    PRIMARY KEY vendor_id
);


-- Person group
CREATE TABLE d_person (
    person_id SERIAL NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    PRIMARY KEY person_id
);

CREATE TABLE d_person_distribution (    -- Something is off here, but not sure what
    distribution_id BIGSERIAL NOT NULL,
    eid VARCHAR(36),
    person_id INT NOT NULL,
    PRIMARY KEY distribution_id,

)