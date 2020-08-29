from data_preparation.data_preparation import prepare_data
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd


def mvp_predictor():
    try:
        x_train = pd.read_csv('data/x_train.csv', index_col=0)
        x_test = pd.read_csv('data/x_test.csv', index_col=0)
        y_train = pd.read_csv('data/y_train.csv', index_col=0)
        y_test = pd.read_csv('data/y_test.csv', index_col=0)
    except FileNotFoundError:
        x_train, x_test, y_train, y_test = prepare_data()
    reg = LinearRegression().fit(x_train, y_train)
    print('Coefs:', reg.coef_)
    print('Intercept_:', reg.intercept_)
    print('Score:', reg.score(x_train, y_train))
    y_pred = reg.predict(x_test)
    print('R2:', r2_score(y_test, y_pred))
    print('MAE:', mean_absolute_error(y_test, y_pred))
    print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
    return reg
