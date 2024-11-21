import pandas as pd

canada_data = "GDP_per_Capita_Canada.csv"
usa_data = "GDP_per_Capita_USA.csv"
data = pd.read_csv(canada_data)
data2 = pd.read_csv(usa_data)
data = pd.concat([data2, data])
data.to_csv('GDP_per_Capita_Data.csv', index=False)