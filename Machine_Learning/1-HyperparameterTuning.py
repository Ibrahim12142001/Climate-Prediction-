import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline

# WARNING: THIS WILL TAKE A WHILE TO RUN!!!
def main():
    # Read in the data from the combined data csv
    combined_data_path = '../Combined_Data.csv'
    data = pd.read_csv(combined_data_path)

    # Extract the X and y data, X = input features, y = output values
    X = data[['megatonnes CO2', 'GDP per Capita', 'precipitation_sum', 'wind_speed_10m_max', 'Population Density']]
    y = data[['temperature_2m_max', 'temperature_2m_min']] # regress on two values

    # Split the dataset into training and validation sets
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8) # 80% training data, 20% validation data

    # From our testing, RandomForestRegressor, KNeighborsRegressor, GradientBoostingRegressor, and GaussianProcessRegressor all performed well
    # So, we will try to find the optimal hyperparameters for them

    # RandomForestRegressor hyperparameter tuning
    model = make_pipeline(
        MinMaxScaler(),
        RandomForestRegressor()
    )
    param_grid = {
        'randomforestregressor__n_estimators': [100, 200, 300, 400, 500],
        'randomforestregressor__max_depth': [5, 10, 15, 20, 25, 30, None],
        'randomforestregressor__min_samples_leaf': [1, 3, 5, 10, 15, 20],
        'randomforestregressor__min_samples_split': [2, 5, 10, 15, 20, 30],
        'randomforestregressor__max_features': ['sqrt', 'log2', None]
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=8)
    grid_search.fit(X_train, y_train)
    print(grid_search.best_params_)


if __name__ == '__main__':
    main()
