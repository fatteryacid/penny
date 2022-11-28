DROP TABLE d_vendor CASCADE;

CREATE TABLE d_vendor (
    vendor_id SERIAL NOT NULL PRIMARY KEY,
    vendor_desc VARCHAR(100) UNIQUE
);