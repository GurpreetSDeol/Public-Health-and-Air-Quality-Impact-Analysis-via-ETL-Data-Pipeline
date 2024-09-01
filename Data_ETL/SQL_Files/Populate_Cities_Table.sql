
COPY cities(city_name, latitude,longitude,country,population,is_capital,city_id) 
FROM 'Final_city_data.csv' DELIMITER ',' CSV HEADER;