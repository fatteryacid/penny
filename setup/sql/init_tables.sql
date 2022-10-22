-- Scripts to create shell tables and set relations
-- To be ran by setup.sh on first run

-- Category & Subcategory group
CREATE TABLE d_category (
    category_id SERIAL NOT NULL PRIMARY KEY,
    category_desc VARCHAR(50) UNIQUE
);

CREATE TABLE d_subcategory (
    subcategory_id SERIAL NOT NULL PRIMARY KEY,
    subcategory_desc VARCHAR(75) UNIQUE
);

CREATE TABLE d_category_subcategory (
    category_relation_id SERIAL NOT NULL PRIMARY KEY,
    category_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    FOREIGN KEY category_id REFERENCES d_category(category_id),
    FOREIGN KEY subcategory_id REFERENCES d_subcategory(subcategory_id)
);


-- Vendor group
CREATE TABLE d_vendor (
    vendor_id SERIAL NOT NULL PRIMARY KEY,
    vendor_desc VARCHAR(100) UNIQUE
);


-- Fact table
CREATE TABLE f_entry (
    eid VARCHAR(36) NOT NULL PRIMARY KEY,
    category_relation_id INT NOT NULL,
    vendor_id INT NOT NULL,
    amount DECIMAL,
    entry_record_date DATE,
    last_updated DATETIME,
    FOREIGN KEY category_relation_id REFERENCES d_category_subcategory(category_relation_id),
    FOREIGN KEY vendor_id REFERENCES d_vendor(vendor_id)
);


-- Person group
CREATE TABLE d_person (
    person_id SERIAL NOT NULL PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
);

CREATE TABLE d_person_distribution (
    distribution_id BIGSERIAL NOT NULL PRIMARY KEY,
    eid VARCHAR(36),
    person_id INT NOT NULL,
    FOREIGN KEY eid REFERENCES f_entry(eid),
    FOREIGN KEY person_id REFERENCES d_person(person_id)
);