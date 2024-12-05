import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, MultiTaskElasticNet, ElasticNet, SGDRegressor, RidgeCV, Ridge, Lasso, BayesianRidge, HuberRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler
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
    X = data[['year', 'month', 'megatonnes CO2', 'GDP per Capita']]
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
                LinearRegression(fit_intercept=True)
            )
        },
        {
            'name': 'Ridge',
            'model': make_pipeline(
                Ridge(fit_intercept=True)
            )
        },
        {
            'name': 'Lasso',
            'model': make_pipeline(
                Lasso(fit_intercept=True)
            )
        },
        {
            'name': 'BayesianRidge',
            'model': make_pipeline(
                MultiOutputRegressor(BayesianRidge(fit_intercept=True))
            )
        },
        {
            'name': 'HuberRegressor',
            'model': make_pipeline(
                MultiOutputRegressor(HuberRegressor(fit_intercept=True))
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
                RandomForestRegressor(
                    n_estimators=900, 
                    max_depth=30, 
                    max_features=None, 
                    min_samples_leaf=1, 
                    min_samples_split=2
                )
            )
        },
        {
            'name': 'GradientBoostingRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                MultiOutputRegressor(GradientBoostingRegressor(
                    n_estimators=700, 
                    subsample=0.9, 
                    min_samples_split=2, 
                    min_samples_leaf=1, 
                    max_features=None, 
                    max_depth=20, 
                    loss='absolute_error', 
                    learning_rate=0.1, 
                    criterion='friedman_mse'
                ))
            )
        },
        {
            'name': 'AdaBoostRegressor',
            'model': make_pipeline(
                MinMaxScaler(),
                MultiOutputRegressor(AdaBoostRegressor(n_estimators=800))
            )
        },
        {
            'name': 'MultiTaskElasticNet',
            'model': make_pipeline(
                MinMaxScaler(),
                MultiTaskElasticNet()
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
                MLPRegressor(hidden_layer_sizes=(128, 128), solver='adam', activation='logistic', max_iter=5000)
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

    # Part 2: Test combining the models in a VotingRegressor and StackingRegressor
    # StackingRegressor testing
    estimators = [
        ('kneighbors', KNeighborsRegressor(n_neighbors=3, algorithm='auto', leaf_size=5, p=1, weights='distance')),
        ('randomforest', RandomForestRegressor(
            n_estimators=900, 
            max_depth=30, 
            max_features=None, 
            min_samples_leaf=1, 
            min_samples_split=2
        )),
        ('gradientboosting', GradientBoostingRegressor(
            n_estimators=700, 
            subsample=0.9, 
            min_samples_split=2, 
            min_samples_leaf=1, 
            max_features=None, 
            max_depth=20, 
            loss='absolute_error', 
            learning_rate=0.1, 
            criterion='friedman_mse'
        ))
    ]
    stacking_model = make_pipeline(
        MinMaxScaler(),
        MultiOutputRegressor(StackingRegressor(
            estimators=estimators,
            final_estimator=LinearRegression(),
            cv=5, # default cross validation
            n_jobs=-1, # train models in parallel
            passthrough=False # passthrough the training data for the final estimator
        ))
    )
    stacking_model.fit(X_train, y_train)
    print(f'StackingRegressor training score: {stacking_model.score(X_train, y_train)}')
    print(f'StackingRegressor validation score: {stacking_model.score(X_valid, y_valid)}')
    print(' ')

    # VotingRegressor testing
    estimators = [
        ('kneighbors', KNeighborsRegressor(n_neighbors=3, algorithm='auto', leaf_size=5, p=1, weights='distance')),
        ('randomforest', RandomForestRegressor(
            n_estimators=900, 
            max_depth=30, 
            max_features=None, 
            min_samples_leaf=1, 
            min_samples_split=2
        )),
        ('gradientboosting', GradientBoostingRegressor(
            n_estimators=700, 
            subsample=0.9, 
            min_samples_split=2, 
            min_samples_leaf=1, 
            max_features=None, 
            max_depth=20, 
            loss='absolute_error', 
            learning_rate=0.1, 
            criterion='friedman_mse'
        ))
    ]
    voting_model = make_pipeline(
        MinMaxScaler(),
        MultiOutputRegressor(VotingRegressor(
            estimators=estimators,
            n_jobs=-1
        ))
    )
    voting_model.fit(X_train, y_train)
    print(f'VotingRegressor training score: {voting_model.score(X_train, y_train)}')
    print(f'VotingRegressor validation score: {voting_model.score(X_valid, y_valid)}')
    print(' ')

if __name__ == '__main__':
    main()
