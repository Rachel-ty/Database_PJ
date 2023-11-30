
Customer
INSERT INTO Customer (Name, BillingAddress) VALUES
('John Doe', '123 Maple St, Springfield'),
('Jane Smith', '456 Oak Ave, Centerville'),
('Alex Johnson', '789 Pine Rd, Lakeview'),
('Maria Garcia', '101 Birch Ln, Mountainville');



-- ServiceLocation
INSERT INTO ServiceLocation (CustomerID, Building, UnitNumber, TakeOverDate, SquareFootage, NumberOfBedrooms, NumberOfOccupants, Zcode) VALUES
(1, '123 Maple St Building', 5, '2021-06-01', 1200, 2, 4, '12345'),
(2, '456 Oak Ave Complex', 12, '2020-10-15', 950, 1, 2, '54321'),
(3, 'Pine Rd Villas', 7, '2022-01-20', 1500, 3, 5, '67890'),
(1, 'Maple St Annex', 3, '2021-11-10', 800, 1, 3, '12345');

-- Device
INSERT INTO Device (ServiceLocationID, Type, ModelNumber) VALUES
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
(4, 'Washer', 'Bosch Wash700');



-- Event
-- 添加一些事件数据，包括开关机、能耗等
INSERT INTO Event (DeviceID, Timestamp, EventLabel, Value) VALUES
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
(10, '2023-08-22 07:15:00', 'Energy Use', 0.10);




-- EnergyPrice
-- 添加一些能源价格数据
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
('67890', '2023-08-22 07:00:00', 0.18);

