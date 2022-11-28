DROP TABLE d_category CASCADE;

CREATE TABLE d_category (
    category_id SERIAL NOT NULL PRIMARY KEY,
    category_desc VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO d_category (category_desc)
VALUES
    ('automotive'),
    ('education'),
    ('recreation'),
    ('grocery'),
    ('household'),
    ('dining'),
    ('fitness'),
    ('clothing'),
    ('fee'),
    ('gift'),
    ('office')
;