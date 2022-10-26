DROP TABLE f_entries;

CREATE TABLE f_entries (
    eid CHAR(17) NOT NULL PRIMARY KEY,
    item_desc VARCHAR(125),
    type_id INT NOT NULL
    vendor_id INT NOT NULL,
    amount DECIMAL(11,2),
    entry_record_date DATE,
    last_updated TIMESTAMP,
    CONSTRAINT fk_type FOREIGN KEY (type_id) REFERENCES j_type(type_id) ON DELETE SET NULL,
    CONSTRAINT fk_vend FOREIGN KEY (vendor_id) REFERENCES d_vendor(vendor_id) ON DELETE SET NULL
);

