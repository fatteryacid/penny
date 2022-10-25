DROP TABLE d_person;

CREATE TABLE d_person (
    person_id SERIAL NOT NULL PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30)
);

INSERT INTO d_person (first_name, last_name)
VALUES ('mel', 'lname'),
        ('tyler', 'lname'),
        ('thomas', 'lname')
;
