DROP TABLE j_distribution CASCADE;

CREATE TABLE j_distribution (
    dist_id SERIAL NOT NULL PRIMARY KEY,
    eid CHAR(36) NOT NULL,
    person_id INT NOT NULL,
    CONSTRAINT fk_entry FOREIGN KEY (eid) REFERENCES f_entries(eid) ON DELETE SET NULL,
    CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES d_person(person_id) ON DELETE SET NULL
);