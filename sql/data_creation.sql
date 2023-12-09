-- Customer
INSERT INTO Customer (UserName, BillingAddress, Password, Email) VALUES
('John Doe', '123 Maple St, Springfield', 'password123', 'johndoe@example.com'),
('Jane Smith', '456 Oak Ave, Centerville', 'password456', 'janesmith@example.com'),
('Alex Johnson', '789 Pine Rd, Lakeview', 'password789', 'alexjohnson@example.com'),
('Maria Garcia', '101 Birch Ln, Mountainville', 'password101', 'mariagarcia@example.com');




-- ServiceLocation
INSERT INTO ServiceLocation (CustomerID, Building, UnitNumber, TakeOverDate, SquareFootage, NumberOfBedrooms, NumberOfOccupants, Zcode) VALUES
(1, '123 Maple St Building', 5, '2021-06-01', 1200, 2, 4, '12345'),
(2, '456 Oak Ave Complex', 12, '2020-10-15', 950, 1, 2, '54321'),
(3, 'Pine Rd Villas', 7, '2022-01-20', 1500, 3, 5, '67890'),
(1, 'Maple St Annex', 3, '2021-11-10', 800, 1, 3, '12345'),
(4, 'Birch St Building', 8, '2022-03-15', 1140, 1, 2, '12345'),
(4, 'Oak Rd Complex', 9, '2022-04-10', 1180, 1, 1, '54321');


-- Device
INSERT INTO Device (ServiceLocationID, Type, ModelName) VALUES
(1, 'AC System', 'Samsung AC123'),
(1, 'Refrigerator', 'LG Fridge 400'),
(2, 'Washer', 'Bosch Wash500'),
(3, 'Dryer', 'GE Dry900'),
(4, 'Light', 'Philips Bulb60'),
(1, 'Dryer', 'Samsung Dry100'),
(1, 'Oven', 'Whirlpool Oven200'),
(2, 'AC System', 'LG AC310'),
(2, 'Light', 'Philips Bulb60'),
(3, 'Refrigerator', 'Samsung Fridge500'),
(4, 'Washer', 'Bosch Wash700'),
(5, 'Heater', 'HeatMax 200'),
(6, 'AC System', 'CoolPro AC400');



-- Event
INSERT INTO Event (DeviceId, Timestamp, EventLabel, Value) VALUES
(1, '2023-08-01 08:00:00', 'Switched On', NULL),
(1, '2023-08-01 08:15:00', 'Energy Use', 0.05),
(2, '2023-08-01 09:00:00', 'Door Opened', NULL),
(2, '2023-08-01 09:30:00', 'Door Closed', NULL),
(3, '2023-08-01 10:30:00', 'Switched Off', NULL),
(4, '2023-08-01 11:00:00', 'Temp Lowered', 70.00),
(2, '2023-08-02 12:00:00', 'Door Opened', NULL),
(2, '2023-08-02 12:35:00', 'Door Closed', NULL),
(5, '2023-08-02 08:00:00', 'Switched On', NULL),
(5, '2023-08-02 08:20:00', 'Energy Use', 0.08),
(6, '2023-08-05 18:30:00', 'Switched On', NULL),
(6, '2023-08-05 19:00:00', 'Energy Use', 0.06),
(7, '2023-08-10 15:00:00', 'Switched On', NULL),
(7, '2023-08-10 15:30:00', 'Energy Use', 0.07),
(8, '2023-08-15 21:00:00', 'Switched Off', NULL),
(9, '2023-08-20 10:00:00', 'Temp Lowered', 68.00),
(10, '2023-08-22 07:00:00', 'Switched On', NULL),
(10, '2023-08-22 07:15:00', 'Energy Use', 0.10),
(1, '2022-08-05 10:00:00', 'Energy Use', 0.15),
(1, '2022-08-10 10:00:00', 'Energy Use', 0.20),
(2, '2022-08-15 10:00:00', 'Energy Use', 0.10),
(2, '2022-08-20 10:00:00', 'Energy Use', 0.12),
(1, '2022-08-25 10:00:00', 'Energy Use', 0.18),
(1, '2022-08-03 09:00:00', 'Energy Use', 0.16),
(1, '2022-08-07 10:00:00', 'Energy Use', 0.20),
(2, '2022-08-10 14:00:00', 'Energy Use', 0.11),
(2, '2022-08-22 08:30:00', 'Energy Use', 0.13),
(3, '2022-08-15 11:00:00', 'Energy Use', 0.15),
(3, '2022-08-28 09:45:00', 'Energy Use', 0.19),
(12, '2022-08-03 11:00:00', 'Energy Use', 0.22),
(12, '2022-08-15 13:30:00', 'Energy Use', 0.25),
(13, '2022-08-12 14:00:00', 'Energy Use', 0.19),
(13, '2022-08-22 15:45:00', 'Energy Use', 0.21),
(1, '2022-08-05 10:00:00', 'Energy Use', 0.15),
(1, '2022-08-12 10:00:00', 'Energy Use', 0.17),
(2, '2022-08-09 10:00:00', 'Energy Use', 0.12),
(2, '2022-08-27 10:00:00', 'Energy Use', 0.14),
(3, '2022-08-15 10:00:00', 'Energy Use', 0.18),
(3, '2022-08-23 10:00:00', 'Energy Use', 0.20),
(1, '2022-09-03 10:00:00', 'Energy Use', 0.25),
(1, '2022-09-20 10:00:00', 'Energy Use', 0.30),
(2, '2022-09-10 10:00:00', 'Energy Use', 0.16),
(2, '2022-09-26 10:00:00', 'Energy Use', 0.18),
(3, '2022-09-05 10:00:00', 'Energy Use', 0.22),
(3, '2022-09-25 10:00:00', 'Energy Use', 0.25);


-- EnergyPrice
INSERT INTO EnergyPrice (Zcode, Timestamp, Price) VALUES
('12345', '2023-08-01 08:00:00', 0.15),
('54321', '2023-08-01 09:00:00', 0.18),
('67890', '2023-08-01 10:00:00', 0.20),
('12345', '2023-08-01 11:00:00', 0.17),
('12345', '2023-08-02 08:00:00', 0.16),
('12345', '2023-08-05 18:00:00', 0.14),
('54321', '2023-08-10 15:00:00', 0.19),
('54321', '2023-08-15 21:00:00', 0.17),
('67890', '2023-08-20 10:00:00', 0.21),
('67890', '2023-08-22 07:00:00', 0.18),
('12345', '2022-08-05 10:00:00', 0.12),
('12345', '2022-08-15 10:00:00', 0.15),
('54321', '2022-08-20 10:00:00', 0.10),
('12345', '2022-08-03 09:00:00', 0.13),
('12345', '2022-08-07 10:00:00', 0.14),
('54321', '2022-08-10 14:00:00', 0.17),
('54321', '2022-08-22 08:30:00', 0.16),
('67890', '2022-08-15 11:00:00', 0.20),
('67890', '2022-08-28 09:45:00', 0.18);

-- More Event records
INSERT INTO Event (DeviceId, Timestamp, EventLabel, Value) VALUES
(1, '2023-09-01 08:00:00', 'Energy Use', 0.12),
(2, '2023-09-01 09:15:00', 'Energy Use', 0.10),
(3, '2023-09-02 10:30:00', 'Energy Use', 0.14),
(4, '2023-09-02 11:45:00', 'Energy Use', 0.18),
(5, '2023-09-03 08:20:00', 'Energy Use', 0.11),
(6, '2023-09-04 19:30:00', 'Energy Use', 0.15),
(7, '2023-09-05 15:30:00', 'Energy Use', 0.13),
(8, '2023-09-06 21:00:00', 'Energy Use', 0.09),
(9, '2023-09-07 10:30:00', 'Energy Use', 0.12),
(10, '2023-09-08 07:45:00', 'Energy Use', 0.16);


INSERT INTO EnergyPrice (Zcode, Timestamp, Price) VALUES
-- Zcode 12345
('12345', '2023-08-02 12:00:00', 0.20),
('12345', '2023-08-10 15:00:00', 0.22),
('12345', '2023-08-15 21:00:00', 0.23),
('12345', '2023-08-20 10:00:00', 0.24),
('12345', '2023-08-22 07:00:00', 0.25),
-- Zcode 54321
('54321', '2023-08-02 12:00:00', 0.17),
('54321', '2023-08-20 10:00:00', 0.21),
('54321', '2023-08-22 07:00:00', 0.22),
-- Zcode 67890
('67890', '2023-08-02 08:00:00', 0.19),
('67890', '2023-08-05 18:00:00', 0.18),
('67890', '2023-08-10 15:00:00', 0.17),
('67890', '2023-08-15 21:00:00', 0.16),
('67890', '2023-08-20 10:00:00', 0.15);
