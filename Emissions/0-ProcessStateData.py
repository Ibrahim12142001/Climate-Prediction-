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

YEAR_ROW = 2
TRANSPORTATION_TOTAL_ROW = 25

# Reads all of the raw data files, extracts the relevant fields and puts it into a nice dataframe
def extract_transportation_data(state_data_path):
    all_state_data = None
    for file in os.scandir(state_data_path):
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


def main():
    # The state emissions data consists of 50 files, one for each state
    # So we need to read them one by one, extract the relevant data/fields
    # And save them to a more usable format
    state_data_path = './state_emissions_data/'
    state_yearly_emission_data = extract_transportation_data(state_data_path)


if __name__ == '__main__':
    main()