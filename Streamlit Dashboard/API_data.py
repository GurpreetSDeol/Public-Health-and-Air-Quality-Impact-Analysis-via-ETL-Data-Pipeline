import requests
import json
import pandas as pd
import time
from json_flatten import flatten
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv
import os

load_dotenv()

OW_api_key = os.getenv('OW_api_key')

# Load data containing cities for the API
json_save_path = rf'Data\Final_city_data.json'
with open(json_save_path) as f:
    city_data = json.load(f)

class WeatherPollutionFetcher:
    def __init__(self, api_key, city_data, delay=2, units="metric"):
        self.api_key = api_key
        self.city_data = city_data
        self.delay = delay
        self.units = units
        self.weather_data = []
        self.pollution_data = []

    def fetch_data(self):
        for city in self.city_data:
            lat = city['latitude']
            lon = city['longitude']
            city_id = city['city_id']
            
            # Fetch the weather data
            weather_data = self.fetch_weather_data(lat, lon, city_id)
            self.weather_data.append(weather_data)
            time.sleep(self.delay)
            
            # Fetch the pollution data
            pollution_data = self.fetch_pollution_data(lat, lon, city_id)
            self.pollution_data.append(pollution_data)
            time.sleep(self.delay)

    def fetch_weather_data(self, lat, lon, city_id):
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={self.units}&appid={self.api_key}'
        response = requests.get(weather_url)
        weather_data = response.json()
        weather_data['latitude'] = lat
        weather_data['longitude'] = lon
        weather_data['city_id'] = city_id
        return weather_data

    def fetch_pollution_data(self, lat, lon, city_id):
        pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&units={self.units}&appid={self.api_key}'
        response = requests.get(pollution_url)
        pollution_data = response.json()
        pollution_data['latitude'] = lat
        pollution_data['longitude'] = lon
        pollution_data['city_id'] = city_id
        return pollution_data

    def rename_and_convert_columns(self, df, column_map):
        """
        Renames columns in a DataFrame and converts them to the specified data types.
        """
        for original_col, (new_col, dtype) in column_map.items():
            if original_col in df.columns:
                df.rename(columns={original_col: new_col}, inplace=True)

                if dtype == 'float':
                    df[new_col] = pd.to_numeric(df[new_col], errors='coerce')
                elif dtype == 'int':
                    df[new_col] = pd.to_numeric(df[new_col], errors='coerce', downcast='integer')
                elif dtype == 'datetime':
                    df[new_col] = pd.to_datetime(pd.to_numeric(df[new_col], errors='coerce'), unit='s', errors='coerce')
                    df[new_col] = df[new_col].dt.round('min')
        return df

    def calculate_local_time(self, datetime_str, lat, lon):
        """
        Calculates the local time based on latitude, longitude, and UK local datetime.
        """
        uk_datetime = pd.to_datetime(datetime_str)
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=lon, lat=lat)
        timezone = pytz.timezone(timezone_str)
        local_time = pd.Timestamp(uk_datetime).tz_localize(pytz.timezone('Europe/London')).astimezone(timezone)
        return local_time.tz_localize(None)

    def process_weather_data(self):
        flattened_weather_data = [flatten(item) for item in self.weather_data]
        weather_data_df = pd.DataFrame(flattened_weather_data)

        weather_column_map = {
            'city_id$int': ('city_id', 'int'),
            'longitude$float': ('longitude', 'float'),
            'latitude$float': ('latitude', 'float'),
            'weather.[0].id$int': ('weather_id', 'int'),
            'weather.[0].main': ('weather_main', 'str'),
            'weather.[0].description': ('weather_description', 'str'),
            'weather.[0].icon': ('weather_icon', 'str'),
            'main.temp$float': ('temperature', 'float'),
            'main.feels_like$float': ('feels_like', 'float'),
            'main.temp_min$float': ('temp_min', 'float'),
            'main.temp_max$float': ('temp_max', 'float'),
            'main.pressure$int': ('pressure', 'int'),
            'main.humidity$int': ('humidity', 'int'),
            'main.sea_level$int': ('sea_level', 'int'),
            'main.grnd_level$int': ('grnd_level', 'int'),
            'visibility$int': ('visibility', 'int'),
            'wind.speed$float': ('wind_speed', 'float'),
            'wind.deg$int': ('wind_deg', 'int'),
            'clouds.all$int': ('clouds_all', 'int'),
            'dt$int': ('date_time', 'datetime'),
            'sys.type$int': ('sys_type', 'int'),
            'sys.id$int': ('sys_id', 'int'),
            'sys.country': ('sys_country', 'str'),
            'sys.sunrise$int': ('sunrise', 'datetime'),
            'sys.sunset$int': ('sunset', 'datetime'),
            'timezone$int': ('timezone', 'int'),
            'id$int': ('id', 'int'),
            'name': ('name', 'str'),
            'cod$int': ('cod', 'int'),
            'wind.gust$float': ('wind_gust', 'float'),
            'rain.1h$float': ('rain_1h', 'float')
        }

        weather_data_df = self.rename_and_convert_columns(weather_data_df, weather_column_map)
        weather_data_df['local_time'] = weather_data_df.apply(
            lambda row: self.calculate_local_time(row['date_time'], row['latitude'], row['longitude']),
            axis=1
        )

        required_columns = [
            'city_id', 'date_time', 'local_time', 'temperature', 'feels_like', 'temp_min', 'temp_max',
            'pressure', 'humidity', 'visibility', 'wind_speed', 'wind_deg', 'clouds_all',
            'weather_main', 'weather_description', 'weather_icon', 'sunrise', 'sunset'
        ]
        return weather_data_df[required_columns]

    def process_pollution_data(self):
        flattened_pollution_data = [flatten(item) for item in self.pollution_data]
        pollution_data_df = pd.DataFrame(flattened_pollution_data)

        pollution_column_map = {
            'city_id$int': ('city_id', 'int'),
            'list.[0].dt$int': ('date_time', 'datetime'),
            'longitude$float': ('longitude', 'float'),
            'latitude$float': ('latitude', 'float'),
            'list.[0].main.aqi$int': ('aqi', 'int'),
            'list.[0].components.co$float': ('co', 'float'),
            'list.[0].components.no$int': ('no', 'floT'),
            'list.[0].components.no2$float': ('no2', 'float'),
            'list.[0].components.o3$float': ('o3', 'float'),
            'list.[0].components.so2$float': ('so2', 'float'),
            'list.[0].components.pm2_5$float': ('pm2_5', 'float'),
            'list.[0].components.pm10$float': ('pm10', 'float'),
            'list.[0].components.nh3$float': ('nh3', 'float')
        }

        pollution_data_df = self.rename_and_convert_columns(pollution_data_df, pollution_column_map)
        required_pollution_columns = [col for col in pollution_column_map.values() if col[0] in pollution_data_df.columns]
        pollution_data_df = pollution_data_df[[col[0] for col in required_pollution_columns]]
        pollution_data_df['local_time'] = pollution_data_df.apply(
            lambda row: self.calculate_local_time(row['date_time'], row['latitude'], row['longitude']),
            axis=1
        )
        return pollution_data_df.drop(columns=['latitude', 'longitude'])
