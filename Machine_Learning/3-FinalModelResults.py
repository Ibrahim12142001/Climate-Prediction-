import pandas as pd
import matplotlib.pyplot as plt
import pickle
import lzma
import seaborn

def main():
    # Read in the data from the combined data csv
    combined_data_path = '../Combined_Data.csv'
    data = pd.read_csv(combined_data_path)
    test_data_path = '../Combined_Data_2011_2013.csv'
    test_data = pd.read_csv(test_data_path)

    # Load the pre-trained models for analysis
    with lzma.open('model_YearMonthCO2GDP.xz', 'rb') as f:
        model_YearMonthCO2GDP = pickle.load(f)
    
    with lzma.open('model_OnlyYearMonth.xz', 'rb') as f:
        model_OnlyYearMonth = pickle.load(f)
    
    with lzma.open('model_OnlyCO2GDP.xz', 'rb') as f:
        model_OnlyCO2GDP = pickle.load(f)

    # score the models on the respective datasets
    print(
        f"Model trained only on year and month, score on 2000-2010 data: "
        f"{model_OnlyYearMonth.score(data[['year', 'month']], data[['temperature_2m_max', 'temperature_2m_min']])}"
    )
    print(
        f"Model trained only on year and month, score on 2011-2013 data: "
        f"{model_OnlyYearMonth.score(test_data[['year', 'month']], test_data[['temperature_2m_max', 'temperature_2m_min']])}"
    )
    print(' ')
    print(
        f"Model trained only on CO2 emissions and GDP per Capita, score on 2000-2010 data: "
        f"{model_OnlyCO2GDP.score(data[['megatonnes CO2', 'GDP per Capita']], data[['temperature_2m_max', 'temperature_2m_min']])}"
    )
    print(
        f"Model trained only on CO2 emissions and GDP per Capita, score on 2011-2013 data: "
        f"{model_OnlyCO2GDP.score(test_data[['megatonnes CO2', 'GDP per Capita']], test_data[['temperature_2m_max', 'temperature_2m_min']])}"
    )
    print(' ')
    print(
        f"Model trained on Year/Month/CO2/GDP Per Capita, score on 2000-2010 data: "
        f"{model_YearMonthCO2GDP.score(data[['year', 'month', 'megatonnes CO2', 'GDP per Capita']], data[['temperature_2m_max', 'temperature_2m_min']])}"
    )
    print(
        f"Model trained on Year/Month/CO2/GDP Per Capita, score on 2011-2013 data: "
        f"{model_YearMonthCO2GDP.score(test_data[['year', 'month', 'megatonnes CO2', 'GDP per Capita']], test_data[['temperature_2m_max', 'temperature_2m_min']])}"
    )
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

    # Aggregate test data to take the average for all cities by year and month
    test_data_aggregated = (
        test_data.groupby(['year', 'month'])[['megatonnes CO2', 'GDP per Capita', 'temperature_2m_max', 'temperature_2m_min']]
        .mean()
        .reset_index()
    )

    # Predictions for aggregated data (ensure all required features are passed)
    predicted_values = model_YearMonthCO2GDP.predict(
        test_data_aggregated[['year', 'month', 'megatonnes CO2', 'GDP per Capita']]
    )
    predicted_max = predicted_values[:, 0]
    predicted_min = predicted_values[:, 1]

    # Actuals from aggregated data
    actual_max = test_data_aggregated['temperature_2m_max']
    actual_min = test_data_aggregated['temperature_2m_min']

    # Create plots
    plt.figure(figsize=(12, 8))

    # Plot actual vs predicted temperature max
    plt.subplot(2, 1, 1)
    plt.plot(test_data_aggregated['year'] + test_data_aggregated['month'] / 12, actual_max, label='Actual Max Temperature', marker='o')
    plt.plot(test_data_aggregated['year'] + test_data_aggregated['month'] / 12, predicted_max, label='Predicted Max Temperature', marker='x')
    plt.plot(test_data_aggregated['year'] + test_data_aggregated['month'] / 12, actual_min, label='Actual Min Temperature', marker='o', alpha=0.7, linestyle='--')
    plt.plot(test_data_aggregated['year'] + test_data_aggregated['month'] / 12, predicted_min, label='Predicted Min Temperature', marker='x', linestyle='dotted', alpha=0.8)
    plt.title('Actual vs Predicted Temperatures (Averaged Across Cities)')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)



    # Save the combined plot
    plt.tight_layout()
    plt.savefig("Predictions_vs_Actual_and_Residuals_Aggregated.png")
    #plt.show()

if __name__ == '__main__':
    main()
