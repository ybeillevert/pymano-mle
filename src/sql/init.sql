CREATE DATABASE IF NOT EXISTS pymanoDB;

USE pymanoDB;

CREATE TABLE Users (
    Id int NOT NULL AUTO_INCREMENT,
    UserName varchar(255) NOT NULL,
    Password varchar(255) NOT NULL, 
    PublicId varchar(255) NOT NULL,    
    PRIMARY KEY (Id)
);
INSERT INTO Users
    (UserName, Password, PublicId)
VALUES 
    ('admin', 'admin', 'publicid1'),
    ('sophie', 'password', 'publicid2'),
    ('john', 'azerty', 'publicid3');