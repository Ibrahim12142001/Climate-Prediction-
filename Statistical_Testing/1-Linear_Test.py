import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess

# Load the dataset
file_path = "../Combined_Data.csv"  
data = pd.read_csv(file_path)

# Filter data for years 2000 to 2010
data['year'] = pd.to_numeric(data['year'], errors='coerce')
filtered_data = data[(data['year'] >= 2000) & (data['year'] <= 2010)]

# Calculate monthly averages across all cities for emissions, GDP, and temperatures
monthly_avg = filtered_data.groupby(['year', 'month']).agg({
    'megatonnes CO2': 'mean',
    'GDP per Capita': 'mean',
    'temperature_2m_max': 'mean',
    'temperature_2m_min': 'mean'
}).reset_index()

monthly_avg['month_count'] = (monthly_avg['year'] - 2000) * 12 + monthly_avg['month']

# Function to perform linear regression and plot
def plot_with_loess_and_regression(data, x, y, ax, title, y_label):
    X = sm.add_constant(data[x])  
    model = sm.OLS(data[y], X).fit()
    predictions = model.predict(X)
    p_value = model.pvalues.iloc[1] 

    # LOESS for best fit line (no smoothing)
    loess_result = lowess(data[y], data[x], frac=0.0001)
    
    ax.scatter(data[x], data[y], alpha=0.5, label='Data Points')
    ax.plot(data[x], predictions, color='blue', linestyle='--', label=f'Linear Regression (p={p_value:.3f})')
    ax.plot(loess_result[:, 0], loess_result[:, 1], color='red', label='LOESS Best Fit')
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel(y_label)

    ax.set_xticks(np.arange(0, 121, 12))  
    ax.set_xticklabels(range(2000, 2011))  
    ax.legend()

    return p_value

# Create subplots for emissions, GDP, temp_max, and temp_min
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
p_values = {}

p_values['Emissions'] = plot_with_loess_and_regression(
    monthly_avg, 'month_count', 'megatonnes CO2', axes[0, 0], 
    "Emissions vs Months (2000-2010)", "Megatonnes CO2")

p_values['GDP'] = plot_with_loess_and_regression(
    monthly_avg, 'month_count', 'GDP per Capita', axes[0, 1], 
    "GDP per Capita vs Months (2000-2010)", "GDP per Capita")

p_values['Temp Max'] = plot_with_loess_and_regression(
    monthly_avg, 'month_count', 'temperature_2m_max', axes[1, 0], 
    "Temperature Max vs Months (2000-2010)", "Temperature Max (°C)")

p_values['Temp Min'] = plot_with_loess_and_regression(
    monthly_avg, 'month_count', 'temperature_2m_min', axes[1, 1], 
    "Temperature Min vs Months (2000-2010)", "Temperature Min (°C)")

plt.tight_layout()
output_file = "Monthly_Data_Plots_Yearly_Labels_Fixed.png"
plt.savefig(output_file)
#plt.show()

print("P-values for the linear regression:")
for key, value in p_values.items():
    print(f"{key}: {value:.6e}")

