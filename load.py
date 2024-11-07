import pandas as pd
import os

# Define the folder containing the CSV files
data_folder = "data"

# Initialize an empty list to store each DataFrame
dataframes = []

# Loop through each CSV file in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_folder, filename)
        city_name = filename.replace("_daily_weather_2000_2010.csv", "")  # Extract city name
        print(f"Processing {city_name}...")

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if 'time' column exists
        if 'time' not in df.columns:
            print(f"Skipping {city_name} due to missing 'time' column.")
            continue

        # Rename 'time' column to 'date' for consistency
        df = df.rename(columns={'time': 'date'})
        
        # Add 'city' column
        df['city'] = city_name

        # Append to list of dataframes
        dataframes.append(df)

# Concatenate all DataFrames into a single DataFrame
combined_data = pd.concat(dataframes, ignore_index=True)

# Save the combined data to a new CSV file
output_file = "combined_long_format_weather_data_2000_2010.csv"
combined_data.to_csv(output_file, index=False)
print(f"All data combined and saved to {output_file}")
