import requests
import pandas as pd
import json
import time
import os

with open("capitals.json", "r") as f:
    capitals = json.load(f)

url = "https://archive-api.open-meteo.com/v1/archive"
request_delay = 5
years = range(2011, 2013)
output_folder = "weather_data_ML_testing"
os.makedirs(output_folder, exist_ok=True)

for city_name, info in capitals.items():
    print(f"Processing data for {city_name}...")

    city_data = pd.DataFrame()

    for year in years:
        params = {
            "latitude": info['latitude'],
            "longitude": info['longitude'],
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'daily' in data:
                df = pd.DataFrame(data['daily'])
                df['year'] = year
                df['city'] = city_name
                df['state_or_province'] = info.get('state', info.get('province', ''))
                city_data = pd.concat([city_data, df], ignore_index=True)
                print(f"Data for {city_name} in {year} processed.")
            else:
                print(f"No daily data available for {city_name} in {year}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data for {city_name} in {year}: {e}")

        time.sleep(request_delay)

    if not city_data.empty:
        file_path = os.path.join(output_folder, f"{city_name}_daily_weather_2011_2013.csv")
        try:
            existing_data = pd.read_csv(file_path)
            updated_data = pd.concat([existing_data, city_data], ignore_index=True)
        except FileNotFoundError:
            updated_data = city_data

        updated_data.to_csv(file_path, index=False)
        print(f"Daily weather data for {city_name} saved to {file_path}")
    else:
        print(f"No new data available for {city_name}.")
