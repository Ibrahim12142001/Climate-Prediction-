import pandas as pd
import matplotlib.pyplot as plt

file_path = "../Combined_Data.csv"  
data = pd.read_csv(file_path)

data['year'] = pd.to_numeric(data['year'], errors='coerce')
filtered_data = data[(data['year'] >= 2000) & (data['year'] <= 2010)]

filtered_data['avg_temperature'] = (filtered_data['temperature_2m_max'] + filtered_data['temperature_2m_min']) / 2

yearly_data = filtered_data.groupby('year').agg({
    'avg_temperature': 'mean',
    'megatonnes CO2': 'mean',
    'GDP per Capita': 'mean'
}).reset_index()

yearly_temp = yearly_data[['year', 'avg_temperature']]
yearly_emissions = yearly_data[['year', 'megatonnes CO2']]
yearly_gdp = yearly_data[['year', 'GDP per Capita']]

fig, ax = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

# Plot average temperature
ax[0].plot(yearly_temp['year'], yearly_temp['avg_temperature'], marker='o', label='Avg Temperature', color='blue')
ax[0].set_title("Yearly Average Temperature")
ax[0].set_xlabel("Year")
ax[0].set_ylabel("Temperature (°C)")
ax[0].grid()
ax[0].legend()

# Plot emissions
ax[1].plot(yearly_emissions['year'], yearly_emissions['megatonnes CO2'], marker='o', label='Emissions (Megatonnes)', color='green')
ax[1].set_title("Yearly Emissions")
ax[1].set_xlabel("Year")
ax[1].set_ylabel("Emissions (Megatonnes)")
ax[1].grid()
ax[1].legend()

# Plot GDP per capita
ax[2].plot(yearly_gdp['year'], yearly_gdp['GDP per Capita'], marker='o', label='GDP per Capita', color='orange')
ax[2].set_title("Yearly GDP per Capita")
ax[2].set_xlabel("Year")
ax[2].set_ylabel("GDP per Capita (USD)")
ax[2].grid()
ax[2].legend()

fig.tight_layout()
plt.savefig("Yearly_Trends_Temperature_Emissions_GDP.png")
#plt.show()
