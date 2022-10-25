--Create vendor table
DROP TABLE d_vendor;

CREATE TABLE d_vendor (
    vendor_id SERIAL NOT NULL PRIMARY KEY,
    vendor_desc VARCHAR(100) UNIQUE
);

