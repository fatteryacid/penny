--Create entry fact table
DROP TABLE f_entries;

CREATE TABLE f_entries (
    eid CHAR(17) NOT NULL PRIMARY KEY,
    item_desc VARCHAR(125),
    category_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    vendor_id INT NOT NULL,
    amount DECIMAL(11,2),
    entry_record_date DATE,
    last_updated TIMESTAMP,
    CONSTRAINT fk_cat FOREIGN KEY (category_id) REFERENCES d_category(category_id),
    CONSTRAINT fk_sbcat FOREIGN KEY (subcategory_id) REFERENCES d_subcategory(subcategory_id),
    CONSTRAINT fk_vend FOREIGN KEY (vendor_id) REFERENCES d_vendor(vendor_id)
);

