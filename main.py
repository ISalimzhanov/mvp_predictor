from sklearn.linear_model import LinearRegression

from config import end_year
from data_preparation.data_preparation import prepare_data
from ml_methods.gradient_descent import SGD
from ml_methods.least_squares import LeastSquares
from data_preparation.unknown_mvp import next_mvp_prediction_data
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

from ml_methods.regressor import Regressor


def analyze_error(method: str, y_test: pd.DataFrame, y_pred: pd.DataFrame) -> tuple:
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    print(f'{method} R2: ', r2)
    print(f'{method} RMSE: ', rmse)
    return r2, rmse


def predict_next_mvp(reg: Regressor) -> None:
    try:
        nba_mvp_2020 = pd.read_csv(f'data/mvp_{end_year + 1}.csv', index_col=0)
    except FileNotFoundError:
        nba_mvp_2020 = next_mvp_prediction_data()
    predicted_mvp = reg.make_prediction(nba_mvp_2020.drop(columns=['name', 'basket_ref_chance']))
    predicted_mvp = pd.DataFrame(predicted_mvp, columns=['mvp_score'])
    predicted_mvp['name'] = nba_mvp_2020['name']
    predicted_mvp['mvp_score'] = predicted_mvp['mvp_score'].sub(predicted_mvp['mvp_score'].min())
    predicted_mvp['mvp_score'] = predicted_mvp['mvp_score'].div(predicted_mvp['mvp_score'].sum())
    predicted_mvp['mvp_score'] *= 1010
    predicted_mvp.to_csv('prediction.csv')
    plt.bar(nba_mvp_2020['name'], predicted_mvp['mvp_score'])
    plt.tight_layout()
    plt.show()
    plt.clf()


def main():
    try:
        x_train = pd.read_csv('data/x_train.csv', index_col=0)
        x_test = pd.read_csv('data/x_test.csv', index_col=0)
        y_train = pd.read_csv('data/y_train.csv', index_col=0)
        y_test = pd.read_csv('data/y_test.csv', index_col=0)
    except FileNotFoundError:
        x_train, x_test, y_train, y_test = prepare_data()
    LinearRegression(normalize=False).fit(x_train, y_train)
    reg_methods = [LeastSquares, SGD]
    for r_m in reg_methods:
        reg = r_m(x_train=x_train, y_train=y_train)
        reg.fit(x_train, y_train)
        y_pred = reg.make_prediction(x_test)
        analyze_error(str(r_m), y_test, y_pred)
        predict_next_mvp(reg)
    try:
        nba_mvp_2020 = pd.read_csv(f'data/mvp_{end_year + 1}.csv', index_col=0)
    except FileNotFoundError:
        nba_mvp_2020 = next_mvp_prediction_data()
    plt.bar(nba_mvp_2020['name'], nba_mvp_2020['basket_ref_chance'])
    plt.tight_layout()
    plt.show()
    plt.clf()


if __name__ == '__main__':
    main()