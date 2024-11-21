"""
Name: Birfatehjit Grewal
SFU_ID: 301467843

Citations: The code referenced the notes from class
"""

import numpy as np
import pandas as pd
import sys
import os

def monthly_weather(data):
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    monthly_grouped = data.groupby(['year', 'month', 'city', 'state_or_province']).agg({
    'temperature_2m_max': 'max',
    'temperature_2m_min': 'min',
    'precipitation_sum': 'sum',
    'wind_speed_10m_max': 'max'
        }).reset_index()
    return monthly_grouped

def main():
    weather_file = "Weather/combined_weather_data.csv"
    emissions_file = "Emissions/city_emissions_data.csv"
    population_file = "Population/Population_density.csv"
    GDP_file = "GDP_Data/GDP_per_Capita_Data.csv"
    weather_data = pd.read_csv(weather_file,parse_dates=['date'])
    emissions_data = pd.read_csv(emissions_file,parse_dates=['date'])
    population_data = pd.read_csv(population_file,parse_dates=['date'])
    GDP_data = pd.read_csv(GDP_file,parse_dates=['date'])
    data = monthly_weather(weather_data)
    
    population_data.rename(columns={'City': 'city'}, inplace=True)
    GDP_data.rename(columns={'City': 'city'}, inplace=True)
    GDP_data.rename(columns={'Year': 'year'}, inplace=True)
    GDP_data.rename(columns={'Month': 'month'}, inplace=True)
    GDP_data['year'] = GDP_data['date'].dt.year
    GDP_data['month'] = GDP_data['date'].dt.month
    GDP_data.drop(['date'],axis=1,inplace=True)
    population_data['year'] = population_data['date'].dt.year
    population_data['month'] = population_data['date'].dt.month
    
    merged_data = pd.merge(data, emissions_data, on=['city', 'year', 'month'], how='inner')
    merged_data = pd.merge(merged_data, population_data, on=['city', 'year', 'month'], how='inner')
    merged_data = pd.merge(merged_data, GDP_data, on=['city', 'year', 'month'], how='inner')

    
    merged_data.drop(['date_x', 'Year', 'Month', 'State'], axis=1, inplace=True)
    merged_data.rename(columns={'date_y': 'date'}, inplace=True)
    merged_data.to_csv('Combined_Data.csv', index=False)
    

if __name__ == '__main__':
    main()

