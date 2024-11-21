import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load the dataset
file_path = "../Combined_Data.csv" 
data = pd.read_csv(file_path)

data['year'] = pd.to_numeric(data['year'], errors='coerce')
filtered_data = data[(data['year'] >= 2000) & (data['year'] <= 2010)]

yearly_avg_temp = filtered_data.groupby('year').agg({
    'temperature_2m_max': 'mean',
    'temperature_2m_min': 'mean'
}).reset_index()

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot yearly aggregated max temperature
ax1.plot(yearly_avg_temp['year'], yearly_avg_temp['temperature_2m_max'], label='Max Temperature (°C)', marker='o')
ax1.set_title("Yearly Average Max Temperature (2000-2010)")
ax1.set_xlabel("Year")
ax1.set_ylabel("Temperature (°C)")
ax1.legend()
ax1.grid()

ax2.plot(yearly_avg_temp['year'], yearly_avg_temp['temperature_2m_min'], label='Min Temperature (°C)', marker='o', color='orange')
ax2.set_title("Yearly Average Min Temperature (2000-2010)")
ax2.set_xlabel("Year")
ax2.set_ylabel("Temperature (°C)")
ax2.legend()
ax2.grid()

fig1.tight_layout()
fig1.savefig("Yearly_Temperature_Trend.png")

monthly_avg_temp_max = filtered_data.groupby(['year', 'month']).agg({'temperature_2m_max': 'mean'}).reset_index()
monthly_avg_temp_min = filtered_data.groupby(['year', 'month']).agg({'temperature_2m_min': 'mean'}).reset_index()

monthly_avg_temp_max['date'] = pd.to_datetime(monthly_avg_temp_max[['year', 'month']].assign(day=1))
monthly_avg_temp_max.set_index('date', inplace=True)
decomposition_max = seasonal_decompose(monthly_avg_temp_max['temperature_2m_max'], model='additive', period=12)

monthly_avg_temp_min['date'] = pd.to_datetime(monthly_avg_temp_min[['year', 'month']].assign(day=1))
monthly_avg_temp_min.set_index('date', inplace=True)
decomposition_min = seasonal_decompose(monthly_avg_temp_min['temperature_2m_min'], model='additive', period=12)

fig2, axes = plt.subplots(4, 2, figsize=(15, 15))

# Max temperature decomposition plots
decomposition_max.observed.plot(ax=axes[0, 0], title="Observed Max Temperature", legend=False)
decomposition_max.trend.plot(ax=axes[1, 0], title="Trend (Max Temp)", legend=False)
decomposition_max.seasonal.plot(ax=axes[2, 0], title="Seasonality (Max Temp)", legend=False)
decomposition_max.resid.plot(ax=axes[3, 0], title="Residuals (Max Temp)", legend=False)

# Min temperature decomposition plots
decomposition_min.observed.plot(ax=axes[0, 1], title="Observed Min Temperature", legend=False, color='orange')
decomposition_min.trend.plot(ax=axes[1, 1], title="Trend (Min Temp)", legend=False, color='orange')
decomposition_min.seasonal.plot(ax=axes[2, 1], title="Seasonality (Min Temp)", legend=False, color='orange')
decomposition_min.resid.plot(ax=axes[3, 1], title="Residuals (Min Temp)", legend=False, color='orange')

axes[3, 0].set_xlabel("Date")
axes[3, 1].set_xlabel("Date")
fig2.tight_layout()

fig2.savefig("Monthly_Temperature_Time_Series.png")

print("Yearly Aggregated Temperatures:")
print(yearly_avg_temp)

print("\nTrend Summary (Max Temperature Time Series):")
print(decomposition_max.trend.describe())

print("\nTrend Summary (Min Temperature Time Series):")
print(decomposition_min.trend.describe())
