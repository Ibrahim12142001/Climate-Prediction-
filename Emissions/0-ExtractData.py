import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

state_names_to_abbv_map = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

province_abbv_map = {
    'Alberta': 'AB',
    'British Columbia': 'BC',
    'Manitoba': 'MB',
    'New Brunswick': 'NB',
    'Newfoundland and Labrador': 'NL',
    'Nova Scotia': 'NS',
    'Ontario': 'ON',
    'Prince Edward Island': 'PE',
    'Quebec': 'QC',
    'Saskatchewan': 'SK'
}

YEAR_ROW = 2
TRANSPORTATION_TOTAL_ROW = 25

# Reads all of the raw state data files, extracts the relevant fields and puts it into a nice dataframe
def extract_state_data(state_data_path):
    all_state_data = None
    for file in sorted(os.scandir(state_data_path), key=lambda f: f.name):
        # determine the state from the file name
        state = file.name.split('.')[0].title()
        state_abbv = state_names_to_abbv_map[state]

        # read the state data
        state_data = pd.read_excel(file)

        # extract the years and Transportation Sector (best estimate for vehicle emissions)
        narrowed_data = state_data.iloc[[YEAR_ROW, TRANSPORTATION_TOTAL_ROW]]

        # drop the first two columns since they are labels in the excel sheet
        data = narrowed_data.drop(axis=1, columns=narrowed_data.columns[[0, 1]])
        
        # pivot the data to use the years and co2 measures as the columns, and add state
        data = data.transpose()
        data.columns = ['year', 'megatonnes CO2']
        data['year'] = data['year'].apply(np.int64)
        data = data.reset_index()
        data = data.drop(axis=1, columns=data.columns[[0]])
        data['state'] = state_abbv

        # rearrange the data and add it to the big list
        data = data[['state', 'year', 'megatonnes CO2']]
        if all_state_data is None:
            all_state_data = data
        else:
            all_state_data = pd.concat([all_state_data, data])
    return all_state_data

def extract_province_data(province_data_file):
    # Read in the data file
    data = pd.read_csv(province_data_file)

    # Filter our data down to the Transport sector and totals
    data = data[data['Total'] == 'y']
    data = data[data['Source'] == 'Transport']
    data = data[data['Sector'].isna()]
    data = data[data['Region'].isin(province_abbv_map.keys())] # keep the provinces we want
    data = data.sort_values(by=['Region', 'Year'])
    data['CO2eq'] = data['CO2eq'].astype(np.float64) / 1000 # convert from kilotonnes to megatonnes
    data = data[['Year', 'Region', 'CO2eq']] # extract the fields we want
    data['Region'] = data['Region'].apply(lambda x: province_abbv_map[x]) # convert to the agreed abbreviations
    data = data.rename(columns={'Year': 'year', 'Region': 'province', 'CO2eq': 'megatonnes CO2'})
    data = data.reset_index()[['province', 'year', 'megatonnes CO2']]
    return data

def main():
    # The state emissions data consists of 50 files, one for each state
    # So we need to read them one by one, extract the relevant data/fields
    # And save them to a more usable format
    # to read the xlsx files with Pandas you need to pip install openpyxl
    state_data_path = './state_emissions_data/'
    state_yearly_emission_data = extract_state_data(state_data_path)

    # The province emissions data on the other hand is a single csv file.
    # Therefore, we just need to load it, filter down the table and we'll
    # have our data.
    province_data_file = './province_emissions_data/EN_GHG_Econ_Can_Prov_Terr.csv'
    province_yearly_emission_data = extract_province_data(province_data_file)

    # Canadian data only starts at 1990, so we'll drop everything in the US data before that
    state_yearly_emission_data = state_yearly_emission_data[state_yearly_emission_data['year'] >= 1990]

    # At this point, data has been extracted, and is ready for transforming
    if not os.path.exists('./extracted_data/'):
        os.mkdir('./extracted_data/')
    state_yearly_emission_data.to_csv('./extracted_data/state_emission_data.csv', index=False)
    province_yearly_emission_data.to_csv('./extracted_data/province_emission_data.csv', index=False)


if __name__ == '__main__':
    main()
