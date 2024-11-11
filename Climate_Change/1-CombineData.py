import pandas as pd
import os

data_folder = "climate_data"

dataframes = []

# Loop through each CSV file in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_folder, filename)
        print(f"Processing {filename}...")

        # Read the CSV file
        df = pd.read_csv(file_path)

        dataframes.append(df)

combined_data = pd.concat(dataframes, ignore_index=True)

# Save the combined data to a new CSV file
output_file = "combined_climate_data.csv"
combined_data.to_csv(output_file, index=False)
print(f"All climate data combined and saved to {output_file}")
