import requests
import pandas as pd
import json
import time

# Load the capitals data from JSON
with open("capitals.json", "r") as f:
    capitals = json.load(f)

# Load the missing data information from missing.json
with open("missing.json", "r") as f:
    missing_data = json.load(f)

# Define the base URL for Open-Meteo API
url = "https://archive-api.open-meteo.com/v1/archive"

# Define a delay in seconds to avoid rate limits
request_delay = 5   

# Loop through each missing entry and retry the request
for entry in missing_data:
    city_name = entry['city']
    years = entry['years']
    info = capitals.get(city_name)

    if not info:
        print(f"City {city_name} not found in capitals data.")
        continue

    print(f"Retrying data for {city_name}...")

    # Initialize an empty DataFrame to store data for the city
    city_data = pd.DataFrame()

    # Loop through each year that needs retrying
    for year in years:
        # Define the API parameters
        params = {
            "latitude": info['latitude'],
            "longitude": info['longitude'],
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto"
        }

        # Fetch data from Open-Meteo API with retry and delay
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error if the request fails

            # Process the response JSON
            data = response.json()
            if 'daily' in data:
                daily_data = data['daily']
                df = pd.DataFrame(daily_data)

                # Add the 'year' and 'city' columns
                df['year'] = year
                df['city'] = city_name
                df['state_or_province'] = info.get('state', info.get('province'))

                # Append to city_data DataFrame
                city_data = pd.concat([city_data, df], ignore_index=True)
                print(f"Data for {city_name} in {year} processed.")

            else:
                print(f"No daily data available for {city_name} in {year}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data for {city_name} in {year}: {e}")

        # Wait before the next request to avoid hitting the rate limit
        time.sleep(request_delay)

    # Save the city's data to a CSV file if data was retrieved
    if not city_data.empty:
        # Append or update the existing CSV if it exists
        file_path = f"{city_name}_daily_weather_2000_2010.csv"
        try:
            existing_data = pd.read_csv(file_path)
            updated_data = pd.concat([existing_data, city_data], ignore_index=True)
        except FileNotFoundError:
            updated_data = city_data  # No existing data; use new data directly

        # Save updated data to CSV
        updated_data.to_csv(file_path, index=False)
        print(f"Daily weather data for {city_name} updated successfully.")
    else:
        print(f"No new data available for {city_name}.")
