from API_data import WeatherPollutionFetcher  
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
import os 
import json
from datetime import datetime


#Load credentials 

load_dotenv()

OW_api_key = os.getenv('OW_api_key')
db_name = os.getenv('db_name')
db_user = os.getenv('user')
db_pass = os.getenv('password')
db_host = os.getenv('host')
db_port = os.getenv('port')

json_save_path = rf'Final_city_data.json'
with open(json_save_path) as f:
    city_data = json.load(f)

#Fetch Data

fetch = WeatherPollutionFetcher(api_key=OW_api_key,city_data=city_data)
fetch.fetch_data()
weather_df = fetch.process_weather_data()
pollution_df = fetch.process_pollution_data()


timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
weather_csv_path = rf'Data\Failed_to_Upload\Weather\Weather_{timestamp}.csv'
pollution_csv_path = rf'Data\Failed_to_Upload\Pollution\pollution_{timestamp}.csv'

# Connect to the PostgreSQL database
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
cursor = conn.cursor()

def bulk_insert_pandas(df, table_name):
    columns = ', '.join(df.columns)
    values = ', '.join([f"%({col})s" for col in df.columns])
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    
 
    data = df.to_dict(orient='records')
    execute_batch(cursor, sql, data)
    conn.commit()


# Upload data

try:
    bulk_insert_pandas(weather_df, 'weather')
except Exception as e:
    print(f"Error uploading weather data: {e}")
    weather_df.to_csv(weather_csv_path, index=False)

try:
    bulk_insert_pandas(pollution_df, 'pollution')
except Exception as e:
    print(f"Error uploading pollution data: {e}")
    pollution_df.to_csv(pollution_csv_path, index=False)


cursor.close()
conn.close()