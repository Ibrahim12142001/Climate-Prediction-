import pandas as pd
import os


MIN_YEAR = 2000


pop_file = "State_Population/Canada_Pro_pop.csv"
canada_abr = "State_Population/Provence_to_Abrivation.xlsx"
usa_abr = "State_Population/usa_abr.xlsx"

states_dir = "State_Population/States/"
manual_file = "State_Population/Manual/Manual_State_Pop.xlsx"

def interpolate_monthly_data(data):
    interpolated_data = []

    for state, group in data.groupby('state'):
        group['date'] = pd.to_datetime(group['year'].astype(str) + '-01-01')
        group.set_index('date', inplace=True)
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        group['state'] = state
        group['population'] = group['population'].interpolate(method='linear')
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        group['year'] = group['date'].dt.year
        group['month'] = group['date'].dt.month
        interpolated_data.append(group)
    return pd.concat(interpolated_data, ignore_index=True)

def interpolate_monthly_data2(data):
    interpolated_data = []

    for province, group in data.groupby('province'):
        group['date'] = pd.to_datetime(group['year'].astype(str) + '-01-01')
        group.set_index('date', inplace=True)
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        group['province'] = province
        group['population'] = group['population'].interpolate(method='linear')
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        group['year'] = group['date'].dt.year
        group['month'] = group['date'].dt.month
        interpolated_data.append(group)
    return pd.concat(interpolated_data, ignore_index=True)



def read_province_population_data(province_pop_file):
    pop_data = pd.read_csv(province_pop_file, parse_dates=[0])
    pop_data = pop_data[pop_data['REF_DATE'].dt.month == 10]
    pop_data = pop_data[['REF_DATE', 'GEO', 'VALUE']]
    pop_data.columns = ['year', 'province', 'population']
    pop_data['year'] = pop_data['year'].dt.year
    pop_data = pop_data.sort_values(by=['province', 'year'])
    return pop_data

pop_data = read_province_population_data(pop_file)
province = pd.read_excel(canada_abr)

merged_data = pd.merge(province, pop_data, on=['province'], how='inner')

def process_file(file_path, state_name): 
    
    data = pd.read_csv(
        file_path, parse_dates=[0]
    )
    data.columns = ['date', 'population']
    data['state'] = state_name
    data['year'] = data['date'].dt.year
    data['population'] = data['population'].astype(int) * 1000
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

allData =  handle_Directory(states_dir)

manual_data = pd.read_excel(manual_file)
manual_data = interpolate_monthly_data(manual_data)

data = pd.concat([allData, manual_data],ignore_index=True)


states = pd.read_excel(usa_abr)
states['abr'] = states['state'].copy()
states['state'] = states['Full']
data = pd.merge(data, states, on=['state'], how='inner')
data['state_province'] = data['Full']
data.drop(['Full','state'], axis=1, inplace=True)

merged_data = interpolate_monthly_data2(merged_data)
merged_data.drop(['city','abr'], axis=1, inplace=True)
merged_data = pd.merge(province, merged_data, on=['province'], how='inner')
merged_data['state_province'] = merged_data['province']
merged_data.drop(['province'], axis=1, inplace=True)

data = pd.concat([data, merged_data],ignore_index=True)

data = data[(data['year'] >= MIN_YEAR)]


data.to_csv('state_province_population.csv', index=False)









