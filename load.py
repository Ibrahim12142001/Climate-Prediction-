import pandas as pd
import os

data_folder = "weather_data_seperate"

dataframes = []

# Loop through each CSV file in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_folder, filename)
        city_name = filename.replace("_daily_weather_2000_2010.csv", "")  
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

combined_data = pd.concat(dataframes, ignore_index=True)

output_file = "combined_long_format_weather_data_2000_2010.csv"
combined_data.to_csv(output_file, index=False)
print(f"All data combined and saved to {output_file}")
