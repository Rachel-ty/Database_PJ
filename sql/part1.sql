
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

