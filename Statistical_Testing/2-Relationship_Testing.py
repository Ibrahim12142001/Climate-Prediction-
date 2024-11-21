import pandas as pd
import seaborn as sns
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

pairwise_results = {
    "Avg Temp vs Emissions": yearly_data['avg_temperature'].corr(yearly_data['megatonnes CO2']),
    "Avg Temp vs GDP": yearly_data['avg_temperature'].corr(yearly_data['GDP per Capita']),
    "Emissions vs GDP": yearly_data['megatonnes CO2'].corr(yearly_data['GDP per Capita']),
}

print("Pairwise Correlation Coefficients (Using Average Temperature):")
for key, value in pairwise_results.items():
    print(f"{key}: {value:.3f}")

correlation_matrix = yearly_data[['avg_temperature', 'megatonnes CO2', 'GDP per Capita']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".3f", cbar=True, annot_kws={"size": 12})
plt.title("Correlation Matrix (Avg Temp, Emissions, and GDP)")
plt.tight_layout()
plt.savefig("Correlation_Matrix_Avg_Temp_Emissions_GDP.png")
#plt.show()

