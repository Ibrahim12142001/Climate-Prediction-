import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, MultiTaskElasticNet, ElasticNet, SGDRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR, NuSVR, LinearSVR
from sklearn.cross_decomposition import PLSRegression
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

def main():
    # Read in the data from the combined data csv
    combined_data_path = '../Combined_Data.csv'
    data = pd.read_csv(combined_data_path)

    # Extract the X and y data, X = input features, y = output values
    X = data[['megatonnes CO2', 'GDP per Capita']]
    y = data[['temperature_2m_max', 'temperature_2m_min']] # regress on two values
    # y = (data['temperature_2m_max'] + data['temperature_2m_min']) / 2 # average temperature
    # y = data['temperature_2m_max'] - data['temperature_2m_min'] # temperature range

    # Split the dataset into training and validation sets
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8) # 80% training data, 20% validation data

    # Instantiate our models to figure out which one best responds to our data
    models = [
        {
            'name': 'Linear Regression',
            'model': make_pipeline(
                MinMaxScaler(),
                LinearRegression(fit_intercept=True)
            )
        },
        {
            'name': 'KNeighbors Regressor',
            'model': make_pipeline(
                MinMaxScaler(),
                KNeighborsRegressor(n_neighbors=3, algorithm='auto', leaf_size=5, p=1, weights='distance')
            )
        },
        {
            'name': 'RandomForestRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                RandomForestRegressor(n_estimators=900, max_depth=30, max_features=None, min_samples_leaf=1, min_samples_split=2)
            )
        },
        {
            'name': 'GradientBoostingRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                MultiOutputRegressor(GradientBoostingRegressor(
                    n_estimators=800, 
                    subsample=1.0, 
                    min_samples_split=5, 
                    min_samples_leaf=3, 
                    max_features='sqrt', 
                    max_depth=10, 
                    loss='squared_error', 
                    learning_rate=0.1, 
                    criterion='squared_error')
                )
                # GradientBoostingRegressor(n_estimators=200)
            )
        },
        {
            'name': 'AdaBoostRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                MultiOutputRegressor(AdaBoostRegressor(n_estimators=200))
            )
        },
        {
            'name': 'MultiTaskElasticNet',
            'model': make_pipeline(
                MinMaxScaler(),
                ElasticNet()
            )
        },
        {
            'name': 'SupportVectorRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                MultiOutputRegressor(LinearSVR()) # support vector regressor only supports one output, so train two
                # LinearSVR()
            )
        },
        {
            'name': 'SGDRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                MultiOutputRegressor(SGDRegressor(loss='squared_epsilon_insensitive'))
                # LinearSVR()
            )
        },
        {
            'name': 'PLSRegression',
            'model': make_pipeline(
                MinMaxScaler(),
                PLSRegression(n_components=2)
            )
        },
        {
            'name': 'MLPRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                MLPRegressor(hidden_layer_sizes=(100,), solver='adam', activation='logistic', max_iter=5000)
            )
        }
    ]

    # Train and score each model
    for m in models:
        model = m['model']
        model.fit(X_train, y_train)
        name = m['name']
        print(f'{name} training score: {model.score(X_train, y_train)}')
        print(f'{name} validation score: {model.score(X_valid, y_valid)}')
        print(' ')


if __name__ == '__main__':
    main()
