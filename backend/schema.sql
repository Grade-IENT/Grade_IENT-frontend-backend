
CREATE TABLE Class(

    id SERIAL PRIMARY KEY,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    --pre_req INT references Class(id) ON DELETE SET NULL,
    co_req INT references Class(id) ON DELETE SET NULL,
    SQI DOUBLE PRECISION,
    pre_req_group INT

);

CREATE TABLE UserAccount (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    userPassword VARCHAR(255) NOT NULL, 
    email VARCHAR(255) UNIQUE
);

CREATE TABLE Pre_Reqs(

    class_id INT references Class(id) ON DELETE CASCADE,
    pre_req_id INT references Class(id) ON DELETE CASCADE,
    pre_req_group INT,
    PRIMARY KEY(class_id, pre_req_id)

);

CREATE TABLE Professor(

    id SERIAL PRIMARY KEY,
    prof_name VARCHAR(100) UNIQUE,-- NOT NULL,
    netid VARCHAR(8), --UNIQUE, --NOT NULL
    --need more info for this
    metrics DOUBLE PRECISION,
    summary TEXT,
    SQI DOUBLE PRECISION

);

CREATE TABLE Teaches(
    
    prof_id INT references PROFESSOR(id) ON DELETE CASCADE,
    class_id INT references Class(id) ON DELETE CASCADE,
    PRIMARY KEY(prof_id, class_id),
    SQI DOUBLE PRECISION

);

CREATE TABLE PlanCourse (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES UserAccount(id) ON DELETE CASCADE,
    class_id INT REFERENCES Class(id) ON DELETE CASCADE,
    year INT CHECK (year BETWEEN 1 AND 4),
    semester VARCHAR(10) CHECK (semester IN ('Fall', 'Spring')),
    course_display TEXT,
    UNIQUE(user_id, class_id)
);