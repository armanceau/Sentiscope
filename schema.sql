-- Schema MySQL pour Sentiscope (partie 2 - Base de donnees & pipeline de donnees).
-- Usage : mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS sentiscope
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sentiscope;

CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive TINYINT(1) NOT NULL DEFAULT 0,
    negative TINYINT(1) NOT NULL DEFAULT 0
);
