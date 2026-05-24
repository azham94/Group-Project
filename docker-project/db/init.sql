CREATE DATABASE projectdb;

USE projectdb;

CREATE TABLE scoreboard (
    user VARCHAR(50) PRIMARY KEY,
    points INT,
    datetime_stamp DATETIME
);

INSERT INTO scoreboard VALUES
('python_user', 0, NOW()),
('c_user', 0, NOW());