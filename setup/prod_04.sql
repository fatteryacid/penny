DROP TABLE f_entries CASCADE;

CREATE TABLE f_entries (
    eid CHAR(36) NOT NULL PRIMARY KEY,
    item_desc VARCHAR(125),
    subcategory_id INT NOT NULL,
    vendor_id INT NOT NULL,
    amount DECIMAL(11,2),
    entry_record_date DATE,
    last_updated TIMESTAMP,
    CONSTRAINT fk_subcat FOREIGN KEY (subcategory_id) REFERENCES d_subcategory(subcategory_id) ON DELETE SET NULL,
    CONSTRAINT fk_vend FOREIGN KEY (vendor_id) REFERENCES d_vendor(vendor_id) ON DELETE SET NULL
);

