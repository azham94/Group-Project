CREATE DATABASE projectdb;

USE projectdb;

CREATE TABLE scoreboard (
    user VARCHAR(50) PRIMARY KEY,
    points INT,
    datetime_stamp DATETIME
);

INSERT INTO scoreboard VALUES
('python_user1',0,NOW()),
('python_user2',0,NOW()),
('python_user3',0,NOW()),
('c_user1',0,NOW()),
('c_user2',0,NOW()),
('c_user3',0,NOW());