-- Complex multi-condition alert with time windows
CREATE TABLE apartment_events (
    apartment_id BIGINT,
    city STRING,
    property_type STRING,
    rent_amount DECIMAL(10,2),
    status STRING,
    event_time TIMESTAMP_LTZ(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '10' SECOND
) WITH ('connector' = 'kafka', 'topic' = 'apartment-events');

-- Detect anomalous vacancy patterns
INSERT INTO critical_alerts
SELECT 
    city,
    property_type,
    COUNT(*) as vacant_count,
    AVG(rent_amount) as avg_rent,
    'VACANCY_SURGE' as alert_type,
    CURRENT_TIMESTAMP as alert_time
FROM apartment_events
WHERE status = 'vacant' 
  AND rent_amount > 2000  -- Luxury segment
GROUP BY 
    HOP(event_time, INTERVAL '1' MINUTE, INTERVAL '5' MINUTE),
    city, 
    property_type
HAVING COUNT(*) > 500 
   AND city IN ('London', 'New York', 'Tokyo');
