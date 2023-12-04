-- drop before creation
DROP TABLE Event;
DROP TABLE Device;
DROP TABLE Servicelocation;
DROP TABLE Energyprice;
DROP TABLE Customer;


CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(255),
    BillingAddress VARCHAR(255),
    Password VARCHAR(255),
    Email VARCHAR(255) UNIQUE
);
ALTER TABLE Customer AUTO_INCREMENT = 1;

-- CREATE TRIGGER CheckEmailBeforeInsertOrUpdate
-- BEFORE INSERT ON Customer
-- FOR EACH ROW
-- BEGIN
--     IF NEW.Email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Invalid email format';
--     END IF;
-- END;

CREATE TABLE ServiceLocation (
    ServiceLocationID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    Building VARCHAR(255),
    UnitNumber INT,
    TakeOverDate DATE,
    SquareFootage INT,
    NumberOfBedrooms INT,
    NumberOfOccupants INT,
    Zcode VARCHAR(10),
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);
ALTER TABLE ServiceLocation AUTO_INCREMENT = 1;


CREATE TABLE Device (
    DeviceID INT AUTO_INCREMENT PRIMARY KEY,
    ServiceLocationID INT,
    Type VARCHAR(50),
    ModelNumber VARCHAR(50),
    FOREIGN KEY (ServiceLocationID) REFERENCES ServiceLocation(ServiceLocationID)
);
ALTER TABLE Device AUTO_INCREMENT = 1;


CREATE TABLE Event (
    EventID INT AUTO_INCREMENT PRIMARY KEY,
    DeviceID INT,
    Timestamp DATETIME,
    EventLabel VARCHAR(50),
    Value DECIMAL(10, 2),
    FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID)
);
ALTER TABLE Event AUTO_INCREMENT = 1;


CREATE TABLE EnergyPrice (
    Zcode VARCHAR(10),
    Timestamp DATETIME,
    Price DECIMAL(10, 2),
    Primary key (Zcode, Timestamp)
);
