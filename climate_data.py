import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import json
import os

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Base URL for the Open-Meteo climate API
url = "https://climate-api.open-meteo.com/v1/climate"

# Define the folder to save the CSV files
output_folder = "climate_data"
os.makedirs(output_folder, exist_ok=True)

# Load locations from capitals.json
with open("capitals.json", "r") as f:
    locations = json.load(f)

# Define the parameters for the climate data with selected daily variables
params_base = {
    "start_date": "2000-01-01",
    "end_date": "2010-12-31",
    "models": ["CMCC_CM2_VHR4", "FGOALS_f3_H", "HiRAM_SIT_HR", "MRI_AGCM3_2_S", "EC_Earth3P_HR", "MPI_ESM1_2_XR", "NICAM16_8S"],
    "daily": [
        "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
        "precipitation_sum", "rain_sum", "snowfall_sum"
    ]
}

# Fetch data for each location in capitals.json
for city_name, info in locations.items():
    # Set latitude and longitude for each location
    params = params_base.copy()
    params.update({
        "latitude": info["latitude"],
        "longitude": info["longitude"]
    })
    
    try:
        # Fetch data from Open-Meteo API
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Process daily data and extract each variable
        daily = response.Daily()
        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "city": city_name,  # Add city name
            "province_or_state": info.get("state", info.get("province", ""))  # Add province or state
        }
        
        # Add each requested daily variable to daily_data
        for i, variable_name in enumerate(params["daily"]):
            daily_data[variable_name] = daily.Variables(i).ValuesAsNumpy()

        # Create a DataFrame and save to CSV
        df = pd.DataFrame(daily_data)
        output_file = os.path.join(output_folder, f"{city_name}_climate_data_2000_2010.csv")
        df.to_csv(output_file, index=False)
        print(f"Data for {city_name} saved to {output_file}")

    except Exception as e:
        print(f"Failed to retrieve data for {city_name}: {e}")
