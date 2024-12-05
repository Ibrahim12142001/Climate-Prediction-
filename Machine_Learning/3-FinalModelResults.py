import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import lzma
import seaborn
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

def main():
    # Read in the data from the combined data csv
    combined_data_path = '../Combined_Data.csv'
    data = pd.read_csv(combined_data_path)
    test_data_path = '../Combined_Data_2011_2013.csv'
    test_data = pd.read_csv(test_data_path)

    # load the pre-trained models for analysis
    with lzma.open('model_YearMonthCO2GDP.xz', 'rb') as f:
        model_YearMonthCO2GDP = pickle.load(f)
    
    with lzma.open('model_OnlyYearMonth.xz', 'rb') as f:
        model_OnlyYearMonth = pickle.load(f)
    
    with lzma.open('model_OnlyCO2GDP.xz', 'rb') as f:
        model_OnlyCO2GDP = pickle.load(f)

    # score the models on the respective datasets
    print(f'Model trained only on year and month, score on 2000-2010 data: {model_OnlyYearMonth.score(
        data[['year', 'month']], data[['temperature_2m_max', 'temperature_2m_min']]
    )}')
    print(f'Model trained only on year and month, score on 2011-2013 data: {model_OnlyYearMonth.score(
        test_data[['year', 'month']], test_data[['temperature_2m_max', 'temperature_2m_min']]
    )}')
    print(' ')
    print(f'Model trained only on CO2 emissions and GDP per Capita, score on 2000-2010 data: {model_OnlyCO2GDP.score(
        data[['megatonnes CO2', 'GDP per Capita']], data[['temperature_2m_max', 'temperature_2m_min']]
    )}')
    print(f'Model trained only on CO2 emissions and GDP per Capita, score on 2011-2013 data: {model_OnlyCO2GDP.score(
        test_data[['megatonnes CO2', 'GDP per Capita']], test_data[['temperature_2m_max', 'temperature_2m_min']]
    )}')
    print(' ')
    print(f'Model trained on Year/Month/CO2/GDP Per Capita, score on 2000-2010 data: {model_YearMonthCO2GDP.score(
        data[['year', 'month', 'megatonnes CO2', 'GDP per Capita']], data[['temperature_2m_max', 'temperature_2m_min']]
    )}')
    print(f'Model trained on Year/Month/CO2/GDP Per Capita, score on 2011-2013 data: {model_YearMonthCO2GDP.score(
        test_data[['year', 'month', 'megatonnes CO2', 'GDP per Capita']], test_data[['temperature_2m_max', 'temperature_2m_min']]
    )}')

    # additional analysis below

    # Final model residuals graph
    seaborn.set_theme()
    test_averages = (test_data['temperature_2m_max'].values + test_data['temperature_2m_min'].values) / 2
    predicted_values = model_YearMonthCO2GDP.predict(test_data[['year', 'month', 'megatonnes CO2', 'GDP per Capita']])
    predicted_averages = (predicted_values[:, 0] + predicted_values[:, 1]) / 2
    residuals = test_averages - predicted_averages
    plt.figure()
    plt.title('Histogram of Best Model Averaged Residuals')
    plt.xlabel('Temperature (°C) Residuals')
    plt.ylabel('Frequency')
    plt.hist(residuals, bins=20)
    plt.savefig("BestModelAveragedResidualsHistogram.png")

if __name__ == '__main__':
    main()