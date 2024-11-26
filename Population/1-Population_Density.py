"""
Name: Birfatehjit Grewal
SFU_ID: 301467843

Citations: The code referenced the notes from class
"""

import numpy as np
import pandas as pd
import sys
import os

area_path = "Manual_area_collection.xlsx"
population_path = "Population_data.csv"
    
def main():

    area_data = pd.read_excel(area_path)
    population_data = pd.read_csv(population_path)
    area_data['City'] = area_data['City'].astype(str)
    population_data['City'] = population_data['City'].astype(str)
    merged_data = pd.merge(population_data, area_data, on='City', how='inner')
    if(merged_data['Area(km^2)'].dtype != float):
        merged_data['Area(km^2)'] = merged_data['Area(km^2)'].str.replace(',', '').str.strip()
    merged_data['Population Density'] = merged_data['Population']/merged_data['Area(km^2)']
    
    merged_data.to_csv('Population_density.csv', index=False)
    
    

if __name__ == '__main__':
    main()