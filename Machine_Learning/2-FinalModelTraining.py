import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
import lzma
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.preprocessing import MinMaxScaler
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

    # Split the dataset into training and validation sets
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8) # 80% training data, 20% validation data

    # Create our model
    # From our testing, we were able to get good results from a few different models, and a StackingRegressor allows us
    # to train a final model/layer based on their predicted values, which allows us to use the strength of each individual
    # model to get an even better overall model.
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
            final_estimator=LinearRegression(), # using LinearRegression as our final layer
            cv=5, # default 5-fold cross validation
            n_jobs=-1, # train models in parallel
            passthrough=False # dont passthrough data, train only on predicted values
        ))
    )
    model.fit(X_train, y_train)
    print(f'Model training score: {model.score(X_train, y_train)}')
    print(f'Model validation score: {model.score(X_valid, y_valid)}')
    
    # Model has been trained, let's try using it on data from 2011-2013
    test_data_path = '../Combined_Data_2011_2013.csv'
    test_data = pd.read_csv(test_data_path)
    X_test = test_data[['year', 'month', 'megatonnes CO2', 'GDP per Capita']]
    y_test = test_data[['temperature_2m_max', 'temperature_2m_min']]
    print(f'Model score on future (2011-2013) data: {model.score(X_test, y_test)}')

    # saving the model to disk using pickle
    # note: this code only creates the model trained on year, month, CO2 and GDP per capita since it was the best one
    # but a couple of other models were created using slight modifications to this script for analysis
    with lzma.open('model_YearMonthCO2GDP.xz', 'wb') as f:
        pickle.dump(model, f, protocol=5)

if __name__ == '__main__':
    main()
