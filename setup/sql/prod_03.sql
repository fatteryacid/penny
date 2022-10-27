DROP TABLE j_type;

CREATE TABLE j_type (
    type_id SERIAL NOT NULL PRIMARY KEY,
    category_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    CONSTRAINT fk_cat FOREIGN KEY (category_id) REFERENCES d_category(category_id) ON DELETE SET NULL,
    CONSTRAINT fk_sbcat FOREIGN KEY (subcategory_id) REFERENCES d_subcategory(subcategory_id) ON DELETE SET NULL
);

