import pandas as pd
import os

file_directory = "Canada/"
MAX_YEAR = 2015
MIN_YEAR = 2000

pop_file = "../Population/state_province_population.csv"





def interpolate_monthly_data(data):
    interpolated_data = []

    for city, group in data.groupby('city'):
        group['date'] = pd.to_datetime(group['year'].astype(str) + '-01-01')
        group.set_index('date', inplace=True)
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        group['city'] = city
        group['GDP'] = group['GDP'].interpolate(method='linear')
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        group['year'] = group['date'].dt.year
        group['month'] = group['date'].dt.month
        interpolated_data.append(group)
    return pd.concat(interpolated_data, ignore_index=True)


pop_data = pd.read_csv(pop_file)
pop_data.drop(['date', 'abr', 'state_province'], axis=1, inplace=True)



def process_file(file_path, city_name): 
    data = pd.read_excel(
        file_path,
        sheet_name=1,       # Read from the second sheet
        skiprows=5,         # Skip the first 5 rows
        usecols='B:C',       # Read from column B and C
        header=None,         # Avoid treating any row as the header
        names=['year','GDP']
    )
    data.columns = ['Date', 'GDP']

    
    data['city'] = city_name
    data['year'] = data['Date'].astype(int)
    data['GDP'] = data['GDP'].astype(float, errors='ignore') * 1000000
    
    if 2000 not in data['year'].values:
        gdp_2001 = data.loc[data['year'] == 2001, 'GDP'].values[0]
        gdp_2002 = data.loc[data['year'] == 2002, 'GDP'].values[0]
        gdp_2000 = gdp_2001 - (gdp_2002 - gdp_2001)
        new_row = pd.DataFrame({
            'Date': [2000],
            'GDP': [gdp_2000],
            'city': [city_name],
            'year': [2000]
        })
        data = pd.concat([new_row, data]).sort_values(by='year').reset_index(drop=True)
        
    interpolated_data = interpolate_monthly_data(data)
    data = pd.merge(interpolated_data, pop_data, on=['city', 'year','month'], how='inner')
    data['GDP per Capita']= (data['GDP']/data['population']) * 0.72
    return data



def handle_Directory(dir_path):
    allData = []
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        basename, extension = os.path.splitext(filename)
        processed_data = process_file(file_path, basename)
        allData.append(processed_data)
    return pd.concat(allData, ignore_index=True)

allData =  handle_Directory(file_directory)
allData.drop(['Date','GDP','population'], axis=1, inplace=True)
allData = allData[(allData['year'] >= MIN_YEAR) & (allData['year'] <= MAX_YEAR)]
allData.to_csv('GDP_per_Capita_Canada.csv', index=False)