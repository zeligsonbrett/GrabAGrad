DROP TABLE GRADUATES, GRAD_INDUSTRIES, GRAD_EXPERIENCES, GRAD_INTERESTS, GRAD_CONTACT;

CREATE TABLE IF NOT EXISTS GRADUATES
    (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255),
     acad_dept VARCHAR(70),
     bio TEXT,
     undergrad_university TEXT,
     masters_university TEXT,
     research_focus TEXT,
     expected_grad_date VARCHAR(10),
     years_worked INTEGER,
     photo_link TEXT,
     website_link TEXT,
     netid VARCHAR (15)
    );

CREATE TABLE IF NOT EXISTS GRAD_INDUSTRIES
    (
     id INTEGER,
     industry TEXT
    );

CREATE TABLE IF NOT EXISTS GRAD_EXPERIENCES
    (
     id INTEGER,
     experience TEXT,
     experience_desc TEXT
    );

CREATE TABLE IF NOT EXISTS GRAD_INTERESTS
    (
     id INTEGER,
     interest TEXT
    );

CREATE TABLE IF NOT EXISTS GRAD_CONTACT
    (
     id INTEGER,
     email TEXT,
     phone TEXT
    );

ALTER TABLE GRAD_INDUSTRIES
    ADD CONSTRAINT FK_Grad_Student
    FOREIGN KEY (id)
    REFERENCES GRADUATES(id);

ALTER TABLE GRAD_EXPERIENCES
    ADD CONSTRAINT FK_Grad_Student
    FOREIGN KEY (id)
    REFERENCES GRADUATES(id);

ALTER TABLE GRAD_INTERESTS
    ADD CONSTRAINT FK_Grad_Student
    FOREIGN KEY (id)
    REFERENCES GRADUATES(id);

ALTER TABLE GRAD_CONTACT
    ADD CONSTRAINT FK_Grad_Student
    FOREIGN KEY (id)
    REFERENCES GRADUATES(id);