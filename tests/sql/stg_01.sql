DROP TABLE d_category;

CREATE TABLE d_category (
    category_id SERIAL NOT NULL PRIMARY KEY,
    category_desc VARCHAR(50) UNIQUE
);

INSERT INTO d_category (category_desc)
VALUES
    ('automotive'),
    ('clothing'),
    ('dining'),
    ('education'),
    ('fee'),
    ('fitness'),
    ('gift'),
    ('grocery'),
    ('household'),
    ('office'),
    ('recreation')
;
