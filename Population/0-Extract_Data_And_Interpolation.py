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
import os

MAX_YEAR = 2010
MIN_YEAR = 2000

file_path = "Manual_Population_data_collection.xlsx"
dir_path = "population_datasets/"

def interpolate_monthly_data(data):
    interpolated_data = []

    for city, group in data.groupby('City'):
        group['date'] = pd.to_datetime(group['Year'].astype(str) + '-01-01')
        group.set_index('date', inplace=True)
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        group['City'] = city
        group['Population'] = group['Population'].interpolate(method='linear')
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        group['Year'] = group['date'].dt.year
        group['Month'] = group['date'].dt.month
        interpolated_data.append(group)
    return pd.concat(interpolated_data, ignore_index=True)

def process_file(file_path, city_name):
    dtypes = {'Year': int, 'Population': str}
    
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path, usecols=['Year', 'Population'], dtype=dtypes)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path, usecols=['Year', 'Population'])
    else:
        print(f"Skipping unsupported file format: {file_path}")
        return None
    
    data['City'] = city_name
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
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    
    interpolated_data = interpolate_monthly_data(data)
    
    
    dir_data = handle_Directory(dir_path)
    Final = pd.concat((interpolated_data,dir_data),ignore_index=True)
    Final = Final[(Final['Year'] >= MIN_YEAR) & (Final['Year'] <=MAX_YEAR)]
    
    Final.to_csv('Population_data.csv', index=False)
    

if __name__ == '__main__':
    main()

