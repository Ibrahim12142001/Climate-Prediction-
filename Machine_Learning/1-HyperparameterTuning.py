import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from scipy.stats import randint

# WARNING: THIS WILL TAKE A WHILE TO RUN!!!
def main():
    # Read in the data from the combined data csv
    combined_data_path = '../Combined_Data.csv'
    data = pd.read_csv(combined_data_path)

    # Extract the X and y data, X = input features, y = output values
    X = data[['megatonnes CO2', 'GDP per Capita']]
    y = data[['temperature_2m_max', 'temperature_2m_min']] # regress on two values

    # Split the dataset into training and validation sets
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8) # 80% training data, 20% validation data

    # From our testing, RandomForestRegressor, KNeighborsRegressor, GradientBoostingRegressor all performed well
    # So, we will try to find the optimal hyperparameters for them

    # RandomForestRegressor hyperparameter tuning
    model = make_pipeline(
        MinMaxScaler(),
        RandomForestRegressor()
    )
    param_grid = {
        'randomforestregressor__n_estimators': [400, 500, 600, 700, 800, 900],
        'randomforestregressor__max_depth': [5, 10, 15, 20, 25, 30, None],
        'randomforestregressor__min_samples_leaf': [1, 3, 5, 10, 15, 20],
        'randomforestregressor__min_samples_split': [2, 5, 10, 15, 20, 30],
        'randomforestregressor__max_features': ['sqrt', 'log2', None]
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=8, scoring='explained_variance')
    with np.errstate(invalid='ignore'): # some weird runtime errors can happen sometimes, just ignore it
        grid_search.fit(X_train, y_train)
        print(grid_search.best_params_)
    # this took a super long time to run, but it spit out: max_depth: 30, max_features: None, min_samples_leaf: 1, min_samples_split: 2, n_estimators: 900

    # KNeighborsRegressor hyperparameter tuning
    model = make_pipeline(
        MinMaxScaler(),
        KNeighborsRegressor()
    )
    param_grid = {
        'kneighborsregressor__n_neighbors': [1, 3, 5, 8, 10, 11, 12, 13, 14, 15, 18, 20, 25, 30, 35, 40, 50],
        'kneighborsregressor__weights': ['uniform', 'distance'],
        'kneighborsregressor__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
        'kneighborsregressor__leaf_size': [5, 10, 15, 20, 30, 40, 50, 60],
        'kneighborsregressor__p': [1, 2]
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=8, scoring='explained_variance')
    with np.errstate(invalid='ignore'): # some weird runtime errors can happen sometimes, just ignore it
        grid_search.fit(X_train, y_train)
        print(grid_search.best_params_)
    # output: n_neighbors=3, algorithm='auto', leaf_size=5, p=1, weights='distance'

    # GradientBoostingRegressor hyperparameter tuning
    model = make_pipeline(
        MinMaxScaler(),
        MultiOutputRegressor(GradientBoostingRegressor())
    )
    param_grid = {
        'multioutputregressor__estimator__n_estimators': [600, 700, 800, 900, 1000],
        'multioutputregressor__estimator__max_depth': [1, 3, 5, 10, 15, 20],
        'multioutputregressor__estimator__loss': ['squared_error', 'absolute_error', 'huber', 'quantile'],
        'multioutputregressor__estimator__learning_rate': [0.1, 0.2, 0.05],
        'multioutputregressor__estimator__subsample': [0.8, 0.9, 1.0],
        'multioutputregressor__estimator__criterion': ['friedman_mse', 'squared_error'],
        'multioutputregressor__estimator__min_samples_split': [2, 5, 10, 15, 20, 30],
        'multioutputregressor__estimator__min_samples_leaf': [1, 3, 5, 10, 15, 20],
        'multioutputregressor__estimator__max_features': ['sqrt', 'log2', None]
    }
    grid_search = RandomizedSearchCV(estimator=model, param_distributions=param_grid, cv=5, n_jobs=8, n_iter=1000, scoring='explained_variance')
    with np.errstate(invalid='ignore'): # some weird runtime errors can happen sometimes, just ignore it
        grid_search.fit(X_train, y_train)
        print(grid_search.best_params_)
    # output: n_estimators=700, subsample=0.9, min_samples_split=2, min_samples_leaf=1, max_features=None, max_depth=20, loss='absolute_error', learning_rate=0.1, criterion='friedman_mse'

    # Final model testing
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
    model = make_pipeline(
        MinMaxScaler(),
        MultiOutputRegressor(StackingRegressor(
            estimators=estimators,
            cv=5, # default cross validation
            n_jobs=-1, # train models in parallel
            passthrough=False # dont passthrough data, train only on predicted values
        ))
    )
    param_grid = {
        'multioutputregressor__estimator__final_estimator': [
            RidgeCV(),
            LinearRegression(),
            RandomForestRegressor()
        ],
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=8, scoring='explained_variance')
    with np.errstate(invalid='ignore'): # some weird runtime errors can happen sometimes, just ignore it
        grid_search.fit(X_train, y_train)
        print(grid_search.best_params_)
    # output: LinearRegression()

if __name__ == '__main__':
    main()
