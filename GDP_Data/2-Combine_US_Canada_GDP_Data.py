import pandas as pd

canada_data = "GDP_per_Capita_Canada.csv"
usa_data = "GDP_per_Capita_USA.csv"
data = pd.read_csv(canada_data)
data2 = pd.read_csv(usa_data)
data2.rename(columns={'City': 'city'}, inplace=True)
data2.rename(columns={'Year': 'year'}, inplace=True)
data2.rename(columns={'Month': 'month'}, inplace=True)
data = pd.concat([data2, data],ignore_index=True)

data.to_csv('GDP_per_Capita_Data.csv', index=False)