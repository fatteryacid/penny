DROP TABLE j_distribution;

CREATE TABLE j_distribution (
    dist_id SERIAL NOT NULL PRIMARY KEY,
    eid CHAR(17) NOT NULL,
    person_id INT NOT NULL,
    CONSTRAINT fk_entry FOREIGN KEY (eid) REFERENCES f_entries(eid),
    CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES d_person(person_id)
);