import pandas as pd
import os
from HelperFiles.shared import province_abbv_map

file_directory = "Canada/"  # Replace with your folder path
MAX_YEAR = 2010
MIN_YEAR = 2000

pop_file = "HelperFiles/province_pop_data_2000-2011.csv"



# Greg's code for province population
def read_province_population_data(province_pop_file):
    pop_data = pd.read_csv(province_pop_file, parse_dates=[0])
    pop_data = pop_data[pop_data['GEO'].isin(province_abbv_map.keys())] # keep only provinces we want
    pop_data = pop_data[pop_data['REF_DATE'].dt.month == 10] # keep only Q4 data to match US scaling
    pop_data = pop_data[['REF_DATE', 'GEO', 'VALUE']] # trim down to the columns we want
    pop_data.columns = ['year', 'province', 'value'] # rename columns
    pop_data['year'] = pop_data['year'].dt.year
    pop_data['province'] = pop_data['province'].apply(lambda x: province_abbv_map[x])
    pop_data = pop_data.sort_values(by=['province', 'year'])
    return pop_data

def interpolate_monthly_data(data):
    interpolated_data = []

    for city, group in data.groupby('city'):
        group['date'] = pd.to_datetime(group['year'].astype(str) + '-01-01')
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


city_province = pd.read_excel("HelperFiles/Provence_to_Abrivation.xlsx") 
pop_data = read_province_population_data(pop_file)

merged_data = pd.merge(city_province, pop_data, on=['province'], how='inner')


def process_file(file_path, city_name): 
    data = pd.read_excel(
        file_path,
        sheet_name=1,       # Read from the second sheet (index starts at 0)
        skiprows=5,         # Skip the first 5 rows
        usecols='B:C',       # Read from column B onwards (adjust 'Z' as needed)
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
    
    data = pd.merge(data, merged_data, on=['city', 'year'], how='inner')
    data['GDP per Capita']= (data['GDP']/data['value']) * 0.72
        
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
allData.drop(['Date','GDP','year','Full','value','city','province'], axis=1, inplace=True)
allData = allData[(allData['Year'] >= MIN_YEAR) & (allData['Year'] <= MAX_YEAR)]
allData.to_csv('GDP_per_Capita_Canada.csv', index=False)