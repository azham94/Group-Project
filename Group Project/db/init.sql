CREATE DATABASE IF NOT EXISTS itt440_db;
USE itt440_db;

CREATE TABLE IF NOT EXISTS game_scores (
    user VARCHAR(50) NOT NULL PRIMARY KEY,
    points INT NOT NULL DEFAULT 0,
    datetime_stamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert starting rows if they do not exist yet
INSERT INTO game_scores (user, points) VALUES ('fakhrusy', 0) ON DUPLICATE KEY UPDATE user=user;
INSERT INTO game_scores (user, points) VALUES ('ariff', 0) ON DUPLICATE KEY UPDATE user=user;
INSERT INTO game_scores (user, points) VALUES ('adib', 0) ON DUPLICATE KEY UPDATE user=user;
