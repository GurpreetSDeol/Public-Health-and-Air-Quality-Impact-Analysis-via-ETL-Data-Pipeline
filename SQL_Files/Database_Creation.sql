DROP TABLE IF EXISTS cities, weather, pollution, weather_pollution_facts;

-- Dimension Table: Cities

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    population INTEGER NOT NULL,
    is_capital BOOLEAN,
    country_iso VARCHAR(100) NOT NULL,
    national_population INTEGER NOT NULL
);

-- Dimension Table: Weather

CREATE TABLE weather (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    date_time TIMESTAMP NOT NULL,
    local_time TIMESTAMP NOT NULL,
    temperature FLOAT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    pressure INTEGER,
    humidity INTEGER,
    visibility INTEGER,
    wind_speed FLOAT,
    wind_deg INTEGER,
    clouds_all INTEGER,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100),
    weather_icon VARCHAR(10),
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE (city_id, date_time) 
);


-- Dimension Table: Pollution

CREATE TABLE pollution (
    pollution_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    date_time TIMESTAMP NOT NULL,
    local_time TIMESTAMP NOT NULL,
    aqi INTEGER,
    co FLOAT,
    no FLOAT,
    no2 FLOAT,
    o3 FLOAT,
    so2 FLOAT,
    pm2_5 FLOAT,
    pm10 FLOAT,
    nh3 FLOAT,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE (city_id, date_time) 
);

-- Fact Table: Weather and Pollution Facts

CREATE TABLE weather_pollution_facts (
    fact_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    date_time TIMESTAMP NOT NULL,
    local_time TIMESTAMP NOT NULL,
    weather_id INTEGER NOT NULL,
    pollution_id INTEGER NOT NULL,
    FOREIGN KEY (weather_id) REFERENCES weather(weather_id),
    FOREIGN KEY (pollution_id) REFERENCES pollution(pollution_id),
    UNIQUE (weather_id, pollution_id)  -- Ensure unique pairing of weather and pollution records
);
