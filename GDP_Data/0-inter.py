import pandas as pd
import os

# Directory containing the CSV files
file_directory = "USA/"  # Replace with your folder path
MAX_YEAR = 2010
MIN_YEAR = 2000


def interpolate_monthly_data(data):
    interpolated_data = []

    for city, group in data.groupby('City'):
        group['date'] = pd.to_datetime(group['Year'].astype(str) + '-01-01')
        group.set_index('date', inplace=True)
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        group['City'] = city
        group['GDP per Capita'] = group['GDP per Capita'].interpolate(method='linear')
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        group['Year'] = group['date'].dt.year
        group['Month'] = group['date'].dt.month
        interpolated_data.append(group)
    return pd.concat(interpolated_data, ignore_index=True)

def process_file(file_path, city_name): 
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    else:
        print(f"Skipping unsupported file format: {file_path}")
        return None
    data.columns = ['Date', 'GDP per Capita']
    
    data['City'] = city_name
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['GDP per Capita'] = data['GDP per Capita'].astype(int, errors='ignore')
    if 2000 not in data['Year'].values:
        gdp_2001 = data.loc[data['Year'] == 2001, 'GDP per Capita'].values[0]
        gdp_2002 = data.loc[data['Year'] == 2002, 'GDP per Capita'].values[0]
        gdp_2000 = gdp_2001 - (gdp_2002 - gdp_2001)
        new_row = pd.DataFrame({
            'Date': [pd.Timestamp('2000-01-01')],
            'GDP per Capita': [gdp_2000],
            'City': [city_name],
            'Year': [2000]
        })
        
        data = pd.concat([new_row, data]).sort_values(by='Year').reset_index(drop=True)
        
        
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

allData =  handle_Directory(file_directory)
allData = allData[(allData['Year'] >= MIN_YEAR) & (allData['Year'] <= MAX_YEAR)]
allData.drop(['Date'], axis=1, inplace=True)
print(allData.columns)
allData.to_csv('GDP_per_Capita_USA.csv', index=False)

        
       
    
