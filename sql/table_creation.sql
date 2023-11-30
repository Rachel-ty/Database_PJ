CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    BillingAddress VARCHAR(255)
);

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

CREATE TABLE Device (
    DeviceID INT AUTO_INCREMENT PRIMARY KEY,
    ServiceLocationID INT,
    Type VARCHAR(50),
    ModelNumber VARCHAR(50),
    FOREIGN KEY (ServiceLocationID) REFERENCES ServiceLocation(ServiceLocationID)
);

CREATE TABLE Event (
    EventID INT AUTO_INCREMENT PRIMARY KEY,
    DeviceID INT,
    Timestamp DATETIME,
    EventLabel VARCHAR(50),
    Value DECIMAL(10, 2),
    FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID)
);

CREATE TABLE EnergyPrice (
    Zcode VARCHAR(10),
    Timestamp DATETIME,
    Price DECIMAL(10, 2),
    Primary key (Zcode, Timestamp)
);
