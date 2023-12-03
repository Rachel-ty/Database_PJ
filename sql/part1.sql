
-- Q1 (assume that the customer id is 1 and current time is 2023-08-01 15:40:00)
SELECT Device.DeviceId, SUM(Event.Value) AS TotalConsumption 
FROM Event 
JOIN Device ON Event.DeviceId = Device.DeviceId 
WHERE EventLabel = 'Energy Use' 
AND Timestamp > '2023-08-01 15:40:00' - INTERVAL 1 DAY 
AND Device.ServiceLocationId IN (
    SELECT ServiceLocationId 
    FROM ServiceLocation 
    WHERE CustomerId = 1
) 
GROUP BY Device.DeviceId;

-- Q2
SELECT Type, SUM(Value)/COUNT(DISTINCT Event.DeviceID) AS AvgConsumption
FROM Event JOIN Device ON Event.DeviceId = Device.DeviceId
WHERE EventLabel = 'Energy Use' AND Timestamp BETWEEN '2022-08-01' AND '2022-08-31'
GROUP BY Type;


-- Q3
SELECT 
    OpenEvent.Timestamp, 
    Device.ServiceLocationID, 
    OpenEvent.DeviceId, 
    Device.ModelNumber
FROM
    (SELECT *
     FROM Event
     WHERE EventLabel = 'door opened') AS OpenEvent
JOIN
    (SELECT *
     FROM Event
     WHERE EventLabel = 'door closed') AS CloseEvent 
ON OpenEvent.DeviceId = CloseEvent.DeviceId 
AND CloseEvent.Timestamp > OpenEvent.Timestamp 
AND CloseEvent.Timestamp = (
    SELECT MIN(Timestamp)
    FROM Event e
    WHERE e.DeviceId = OpenEvent.DeviceId 
    AND e.Timestamp > OpenEvent.Timestamp
    AND e.EventLabel = 'door closed'
)
JOIN Device ON OpenEvent.DeviceId = Device.DeviceId
WHERE Device.Type = 'Refrigerator' 
AND TIMESTAMPDIFF(MINUTE, OpenEvent.Timestamp, CloseEvent.Timestamp) > 30;


-- Q4
SELECT 
    ServiceLocation.ServiceLocationId, 
    SUM(Event.Value * EnergyPrice.Price) AS TotalEnergyCost
FROM 
    Event 
JOIN 
    Device ON Event.DeviceId = Device.DeviceId
JOIN 
    ServiceLocation ON Device.ServiceLocationId = ServiceLocation.ServiceLocationId
JOIN 
    EnergyPrice ON ServiceLocation.Zcode = EnergyPrice.Zcode 
    AND EXTRACT(HOUR FROM Event.Timestamp) = EXTRACT(HOUR FROM EnergyPrice.Timestamp)
WHERE 
    Event.EventLabel = 'energy use' 
    AND Event.Timestamp BETWEEN '2022-08-01' AND '2022-08-31'
GROUP BY 
    ServiceLocation.ServiceLocationId;


-- Q5
WITH TotalConsumption AS (
    SELECT 
        ServiceLocation.ServiceLocationId, 
        SUM(Event.Value) AS Consumption
    FROM 
        Event 
    JOIN 
        Device ON Event.DeviceId = Device.DeviceId 
    JOIN 
        ServiceLocation ON Device.ServiceLocationId = ServiceLocation.ServiceLocationId
    WHERE 
        Event.EventLabel = 'energy use' 
        AND Event.Timestamp BETWEEN '2022-08-01' AND '2022-08-31'
    GROUP BY 
        ServiceLocation.ServiceLocationId
),
AverageConsumption AS (
    SELECT 
        S1.ServiceLocationId, 
        AVG(TC.Consumption) AS AvgConsumption
    FROM 
        ServiceLocation S1
    JOIN 
        TotalConsumption TC ON S1.ServiceLocationId != TC.ServiceLocationId
    JOIN 
        ServiceLocation S2 ON TC.ServiceLocationId = S2.ServiceLocationId
    WHERE 
        ABS(S1.SquareFootage - S2.SquareFootage) <= S1.SquareFootage * 0.05
    GROUP BY 
        S1.ServiceLocationId
)

SELECT 
    TC.ServiceLocationId, 
    (TC.Consumption / AC.AvgConsumption) * 100 AS ConsumptionPercentage
FROM 
    TotalConsumption TC
JOIN 
    AverageConsumption AC ON TC.ServiceLocationId = AC.ServiceLocationId;


-- Q6
SELECT 
    ServiceLocation.ServiceLocationId, 
    (SUM(CASE WHEN Event.Timestamp BETWEEN '2022-09-01' AND '2022-09-30' THEN Event.Value ELSE 0 END) / 
     SUM(CASE WHEN Event.Timestamp BETWEEN '2022-08-01' AND '2022-08-31' THEN Event.Value ELSE 0 END) - 1) * 100 AS IncreasePercentage
FROM 
    Event 
JOIN 
    Device ON Event.DeviceId = Device.DeviceId 
JOIN 
    ServiceLocation ON Device.ServiceLocationId = ServiceLocation.ServiceLocationId
WHERE 
    Event.EventLabel = 'energy use'
GROUP BY 
    ServiceLocation.ServiceLocationId
ORDER BY 
    IncreasePercentage DESC
LIMIT 1;


-- SELECT * FROM Event;
-- SELECT * FROM Device;
-- SELECT * FROM ServiceLocation;
-- SELECT * FROM EnergyPrice;
-- SELECT * FROM Customer;