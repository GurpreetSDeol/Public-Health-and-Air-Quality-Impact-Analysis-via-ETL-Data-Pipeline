-- Insert into fact table by linking weather and pollution records


INSERT INTO weather_pollution_facts (city_id, date_time, local_time, weather_id, pollution_id)
SELECT 
    w.city_id,
    w.date_time,
    w.local_time,
    w.weather_id,
    p.pollution_id
FROM weather w
JOIN pollution p ON w.city_id = p.city_id AND w.date_time = p.date_time
WHERE NOT EXISTS (
    SELECT 1 
    FROM weather_pollution_facts wf
    WHERE wf.weather_id = w.weather_id
    AND wf.pollution_id = p.pollution_id
    AND wf.city_id = w.city_id 
    AND wf.date_time = w.date_time  
);

