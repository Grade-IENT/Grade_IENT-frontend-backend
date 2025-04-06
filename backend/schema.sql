
CREATE TABLE Class(

    id SERIAL PRIMARY KEY,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    pre_req INT references Class(id) ON DELETE SET NULL,
    co_req INT references Class(id) ON DELETE SET NULL,
    SQI DOUBLE PRECISION

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