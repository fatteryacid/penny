-- Run this script to initialize vendors table with data
DROP TABLE d_vendor;

CREATE TABLE d_vendor (
    vendor_id SERIAL NOT NULL PRIMARY KEY,
    vendor_desc VARCHAR(100) UNIQUE
);

INSERT INTO d_vendor (vendor_desc)
VALUES
    ('home_depot'),
    ('lowes'),
    ('microcenter'),
    ('best_buy'),
    ('toms_bikes'),
    ('jennys_auto_body'),
    ('cafe_boulard')
;