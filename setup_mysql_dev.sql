-- MySQL setup script for AirBnB clone v2 development environment
-- Creates database hbnb_dev_db and user hbnb_dev with appropriate privileges

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create user if it doesn't exist (MySQL 5.7+ syntax)
-- For older MySQL versions, this will be handled by the GRANT statement
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on hbnb_dev_db to hbnb_dev user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_dev user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to ensure changes take effect
FLUSH PRIVILEGES;
