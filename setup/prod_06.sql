DROP TABLE d_person CASCADE;

CREATE TABLE d_person (
    person_id SERIAL NOT NULL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30)
);

INSERT INTO d_person (first_name)
SELECT name FROM stg_people
;

DROP TABLE stg_people;