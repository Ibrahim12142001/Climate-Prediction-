import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def scale_population_data(population_data):
    # Our population data is interpolated for the year, and we want to use a common ratio across a year
    city_pop_data = pd.read_csv(population_data)
    scaled_data = city_pop_data.groupby(['City', 'Year']).agg({'Population': 'mean'}).reset_index()
    return scaled_data

def read_state_population_data(state_pop_file):
    # reading in the older xls file requires pip install xlrd
    pop_data = pd.read_excel(state_pop_file)
    pop_data = pop_data.iloc[8:59] # keep all of the state rows
    pop_data = pop_data.drop(pop_data.columns[[1, 12]], axis=1) # drop extra columns we don't need
    # the default column names are inferred from the excel spreadsheet but they suck
    pop_data.columns = ['state', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']
    pop_data['state'] = pop_data['state'].str.removeprefix('.')
    pop_data = pop_data.set_index('state')
    pop_data = pop_data.astype(np.int64)
    return pop_data

def interpolate_monthly(data, state_or_province):
    interpolated_data = []
    # Interpolation code is based on the yearly interpolation code for the population data
    for name, group in data.groupby(state_or_province):
        group['date'] = pd.to_datetime(group['year'].astype(str) + '-01-01')
        group.set_index('date', inplace=True)
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        group[state_or_province] = name # fix NaN values
        group['megatonnes CO2'] = group['megatonnes CO2'].interpolate(method='time') # since we're based on a year
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        group['year'] = group['date'].dt.year
        group['month'] = group['date'].dt.month
        interpolated_data.append(group)
    return pd.concat(interpolated_data, ignore_index=True)

def transform_to_us_cities(state_data, cities):
    pass

def transform_to_canada_cities(province_data, cities):
    pass

def main():
    # Read in the constructed province and state data
    state_data = pd.read_csv('./extracted_data/state_emission_data.csv')
    province_data = pd.read_csv('./extracted_data/province_emission_data.csv')

    # Do interpolation first so we have nice trends in the data
    interpolated_state_data = interpolate_monthly(state_data, 'state')
    interpolated_province_data = interpolate_monthly(province_data, 'province')

    # Now that we have interpolated, we can now chop off to the years we want
    interpolated_state_data = interpolated_state_data[interpolated_state_data['year'] >= 2000]
    interpolated_state_data = interpolated_state_data[interpolated_state_data['year'] <= 2010]
    interpolated_province_data = interpolated_province_data[interpolated_province_data['year'] >= 2000]
    interpolated_province_data = interpolated_province_data[interpolated_province_data['year'] <= 2010]
    
    # Read in the cities data
    cities_data = pd.read_json('../capitals.json').transpose()

    # Read in population files to be able to get ratios
    city_population_data = scale_population_data('../Population/Population_data.csv')
    state_population_data = read_state_population_data('./state_pop_data_2000-2010.xls')
    # state population data is yearly taken from the US Census
    # source: https://www.census.gov/data/tables/time-series/demo/popest/intercensal-2000-2010-state.html

    # Process each data file to convert them from State/Province emissions to estimated City emissions
    


if __name__ == '__main__':
    main()
