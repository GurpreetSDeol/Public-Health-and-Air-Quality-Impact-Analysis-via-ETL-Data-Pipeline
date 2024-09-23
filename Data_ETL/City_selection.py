import requests
import json 
import pandas as pd 
import time
import pycountry
from dotenv import load_dotenv
import os 

load_dotenv()

Nin_api_key = os.getenv('Nin_api_key')
print(Nin_api_key)

#Load sample file to get the list of cities with population over 4,000,000
pop_ranking = pd.read_csv(rf'Data\Raw\world-city-listing-table.csv')
pop_ranking = pop_ranking[pop_ranking['population']>4000000]


def country_to_iso_alpha2(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_2
    except LookupError:
        return None  
    
pop_ranking['country_iso'] = pop_ranking['country'].apply(country_to_iso_alpha2)

countries = set(pop_ranking["country"])
cities = pop_ranking[['city','country_iso']]


#Use Ninja API to get Lon and Lat for the cities with updated Population statistics
cities_coord = []
delay = 2

for index, row in cities.iterrows():
    city = row['city']
    country = row['country_iso']

    api_url = f'https://api.api-ninjas.com/v1/city?name={city}&country={country}&min_population=4500000'
    response = requests.get(api_url , headers={'X-Api-Key': Nin_api_key})
    
    if response.status_code == requests.codes.ok:
        
        cities_coord.append(response.text)
        time.sleep(delay)
    else:
        print("Error:", response.status_code, response.text)
print(cities_coord)


#Flatten the nested JSON data

flattened_list = []

for json_str in cities_coord:

    list_of_dicts = json.loads(json_str)
    
    if isinstance(list_of_dicts, list):
        flattened_list.extend(list_of_dicts)
    else:
        print(f"Unexpected data format: {list_of_dicts}")

file_path = rf'Data\Raw\cities_geodata_list.json'

with open(file_path, 'w') as f:
    json.dump(flattened_list, f, indent=4) 

data_to_csv = flattened_list
data_to_csv.rename(columns={'name': 'city_name'}, inplace=True)
data_to_csv['city_id'] = pd.factorize(data_to_csv['city_name'])[0] + 1

json_save_path = rf'Data_ETL\Final_city_data.json'


city_data_json = data_to_csv.to_json(orient='records')
city_data = json.loads(city_data_json)
with open(json_save_path, 'w') as f:
    json.dump(city_data, f, indent=4)


csv_save_path = rf'Data_ETL\Final_city_data.csv'
cities = ['Tokyo','London','Paris','Seoul','Singapore','New York','Barcelona','Sydney','Shanghai','Delhi']

data_to_csv = data_to_csv[data_to_csv['city_name'].isin(cities)]
data_to_csv.to_csv(csv_save_path, index= False)