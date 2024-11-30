import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from shared import state_abbv_map, province_abbv_map

def read_state_province_population_data(population_file):
    # Read the combined state/province population file
    pop_data = pd.read_csv(population_file, parse_dates=['date'])
    pop_data = pop_data[pop_data['year'].between(2011, 2013)]

    # Map full names to abbreviations using province_abbv_map
    pop_data['state_province'] = pop_data['state_province'].apply(
        lambda x: province_abbv_map.get(x, x)  # Map full name to abbreviation if possible
    )
    return pop_data


def interpolate_monthly(data, state_or_province, interpolate_field, starting_month='01'):
    interpolated_data = []
    for name, group in data.groupby(state_or_province):
        group['date'] = pd.to_datetime(group['year'].astype(str) + f'-{starting_month}-01')
        group.set_index('date', inplace=True)
        monthly_index = pd.date_range(start=group.index.min(), end=group.index.max(), freq='MS')
        group = group.reindex(monthly_index)
        group[state_or_province] = name  # Fill NaN values
        group[interpolate_field] = group[interpolate_field].interpolate(method='time')
        group.reset_index(inplace=True)
        group.rename(columns={'index': 'date'}, inplace=True)
        group['year'] = group['date'].dt.year
        group['month'] = group['date'].dt.month
        interpolated_data.append(group)
    return pd.concat(interpolated_data, ignore_index=True)

def scale_using_population(row, city_pop_data, national_pop_data, state_or_province):
    city_col = 'city' if 'city' in city_pop_data.columns else 'City'

    city_cond = (city_pop_data[city_col] == row['city']) & (city_pop_data['date'] == row['date'])
    if city_cond.sum() == 0:
        raise ValueError(f"No matching city population data for city: {row['city']}, date: {row['date']}")
    city_pop = city_pop_data.loc[city_cond, 'Population'].values[0]

    state_cond = (national_pop_data['state_province'] == row[state_or_province]) & \
                 (national_pop_data['date'] == row['date'])
    if state_cond.sum() == 0:
        raise ValueError(f"No matching state population data for state/province: {row[state_or_province]}, date: {row['date']}")
    state_pop = national_pop_data.loc[state_cond, 'population'].values[0]

    return row['megatonnes CO2'] * (city_pop / state_pop)


def transform_to_cities(emissions_data, cities_data, city_population_data, state_province_population_data, region_col):
    print("Emissions Data Columns:", emissions_data.columns)
    print("Cities Data Columns:", cities_data.columns)

    if region_col not in emissions_data.columns:
        raise ValueError(f"Expected region column '{region_col}' not found in emissions data")

    emissions_data['city'] = emissions_data[region_col].apply(
        lambda x: cities_data[cities_data[region_col] == x].index[0]
    )
    emissions_data['megatonnes CO2'] = emissions_data.apply(scale_using_population, axis=1,
        args=(city_population_data, state_province_population_data, region_col))
    return emissions_data[['date', 'city', 'megatonnes CO2', 'year', 'month']]

def plot_city_emissions(new_emissions_file, original_emissions_file, city_name):
    new_data = pd.read_csv(new_emissions_file, parse_dates=['date'])
    original_data = pd.read_csv(original_emissions_file, parse_dates=['date'])
    
    new_city_data = new_data[new_data['city'] == city_name]
    original_city_data = original_data[original_data['city'] == city_name]
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(new_city_data['date'], new_city_data['megatonnes CO2'], label='2011-2013 Emissions', marker='o')
    plt.plot(original_city_data['date'], original_city_data['megatonnes CO2'], label='Original Emissions', marker='x')
    plt.title(f"CO2 Emissions for {city_name}")
    plt.xlabel("Date")
    plt.ylabel("Megatonnes CO2")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    interpolated_state_data = pd.read_csv('interpolated_state_emissions_2011_2013.csv')
    interpolated_province_data = pd.read_csv('interpolated_province_emissions_2011_2013.csv')

    print("Interpolated State Data Columns:", interpolated_state_data.columns)
    print("Interpolated Province Data Columns:", interpolated_province_data.columns)

    cities_data = pd.read_json('../capitals.json').transpose()
    city_population_data = pd.read_csv('../Population/Population_data.csv', parse_dates=['date'])
    state_province_population_data = read_state_province_population_data('../Population/state_province_population.csv')

    print("State/Province Population Data Columns:", state_province_population_data.columns)
    print("Unique state_province values:", state_province_population_data['state_province'].unique())
    print(state_province_population_data[state_province_population_data['date'] == '2011-01-01'])

    state_province_population_data['state_province'] = state_province_population_data['state_province'].apply(
        lambda x: state_abbv_map[x] if x in state_abbv_map else x
    )
    state_province_population_data['date'] = pd.to_datetime(state_province_population_data['date'])
    interpolated_state_data['date'] = pd.to_datetime(interpolated_state_data['date'])
    interpolated_province_data['date'] = pd.to_datetime(interpolated_province_data['date'])

    us_city_emissions = transform_to_cities(
        interpolated_state_data, cities_data, city_population_data, state_province_population_data, 'state'
    )
    canada_city_emissions = transform_to_cities(
        interpolated_province_data, cities_data, city_population_data, state_province_population_data, 'province'
    )

    combined_city_emissions = pd.concat([us_city_emissions, canada_city_emissions])
    combined_city_emissions.to_csv('city_emissions_2011_2013.csv', index=False)
    print("City emissions data for 2011–2013 has been processed and saved.")

    plot_city_emissions('./city_emissions_2011_2013.csv', './city_emissions_data.csv', city_name='Edmonton')


if __name__ == '__main__':
    main()
