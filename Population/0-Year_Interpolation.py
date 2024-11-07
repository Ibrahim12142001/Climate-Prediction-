"""
Name: Birfatehjit Grewal
SFU_ID: 301467843

Citations: The code referenced the notes from class and the following websites:
            
    https://www.geeksforgeeks.org/pandas-dataframe-interpolate/
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reindex.html
    https://www.geeksforgeeks.org/reindexing-in-pandas-dataframe/
"""
import numpy as np
import pandas as pd
import sys
import os

MAX_YEAR = 2010
MIN_YEAR = 2000

def interpolate_monthly_data(data):
    interpolated_data = []

    for city, group in data.groupby('City'):
        # Ensure 'year' is of datetime type to expand by months
        group['date'] = pd.to_datetime(group['Year'].astype(str) + '-01-01')  # Convert year to date
        
        # Set date as index
        group.set_index('date', inplace=True)
        
        # Create a monthly date range from the minimum to the maximum date for each city
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        
        # Forward-fill the 'city' column to avoid NaN values
        group['City'] = city
        
        # Interpolate the 'population' column for monthly values
        group['Population'] = group['Population'].interpolate(method='linear')
        
        # Reset the index to bring the 'date' column back into the DataFrame
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        
        # Add 'year' and 'month' columns for easy reference
        group['Year'] = group['date'].dt.year
        group['Month'] = group['date'].dt.month
        
        # Append the processed group to the list
        interpolated_data.append(group)

    # Concatenate all city data into a single DataFrame
    return pd.concat(interpolated_data, ignore_index=True)

def process_file(file_path, city_name):
    # Define the dtype for the columns
    dtypes = {'Year': int, 'Population': str}  # Read Population as string initially
    
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path, usecols=['Year', 'Population'], dtype=dtypes)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path, usecols=['Year', 'Population'])
    else:
        print(f"Skipping unsupported file format: {file_path}")
        return None
    
    data['City'] = city_name
    
    # Remove commas and convert Population to float
    data['Population'] = data['Population'].str.replace(',', '').astype(float)
    interpolated_data = interpolate_monthly_data(data)
    return interpolated_data

def handle_Directory(dir_path):
    allData = []
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        basename, extension = os.path.splitext(filename)
        processed_data = process_file(file_path, basename)
        allData.append(processed_data)
    return pd.concat(allData, ignore_index=True)


def main():
    file_path = sys.argv[1]

    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    
    interpolated_data = interpolate_monthly_data(data)
    
    
    dir_path = sys.argv[2]
    
    dir_data = handle_Directory(dir_path)
    Final = pd.concat((interpolated_data,dir_data),ignore_index=True)
    Final = Final[(Final['Year'] >= MIN_YEAR) & (Final['Year'] <=MAX_YEAR)]
    
    Final.to_csv('Population_data.csv', index=False)
    

if __name__ == '__main__':
    main()

