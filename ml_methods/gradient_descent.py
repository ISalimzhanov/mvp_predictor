import pandas as pd
import numpy as np
import random
import copy
import time

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from config import output_feature
from data_preparation.data_preparation import prepare_data


def sgd_calc(x: pd.DataFrame, y: pd.DataFrame, max_iter: int, alpha: float) -> np.array:
    random.seed(time.time())
    x_ = copy.deepcopy(x)
    x_['ones'] = np.ones(x_.shape[0])
    coefs = np.random.rand(1, x_.shape[1])
    y_estimate = pd.DataFrame(data=np.array(x_.dot(coefs.T)), columns=[output_feature])
    for iter in range(max_iter):
        i = random.randint(0, x_.shape[0] - 1)
        for j in range(coefs.shape[1]):
            coefs[0, j] -= alpha * (y_estimate - y.values).iloc[i, 0] * pow(x_.iloc[i, j], j)
    return coefs


def bgd_calc(x: pd.DataFrame, y: pd.DataFrame, max_iter: int, alpha: float) -> np.array:
    random.seed(time.time())
    x_ = copy.deepcopy(x)
    x_['ones'] = np.ones(x_.shape[0])
    coefs = np.random.rand(1, x_.shape[1])
    batches = np.arange(x_.shape[0])
    batches = np.array_split(batches, 50)
    y_estimate = pd.DataFrame(data=np.array(x_.dot(coefs.T)), columns=[output_feature])
    for iter in range(max_iter):
        i = random.randint(0, len(batches) - 1)
        for j in range(coefs.shape[1]):
            batch = batches[i]
            for i in range(len(batch)):
                coefs[0, j] -= alpha * (y_estimate - y.values).iloc[i, 0] * pow(x_.iloc[i, j], j)
    return coefs


class GdReggression():
    def __init__(self, type: str, alpha: float, max_iter: int):
        self.type = type
        self.alpha = alpha
        self.max_iter = max_iter
        self._x = None
        self._y = None
        self.coef_ = None

    def fit(self, x: pd.DataFrame, y: pd.DataFrame) -> None:
        self._x = x
        self._y = y
        self.coef_calc()

    def coef_calc(self) -> None:
        types = {'sgd': lambda x, y: sgd_calc(x, y, self.max_iter, self.alpha),
                 'bgd': lambda x, y: bgd_calc(x, y, self.max_iter, self.alpha)}
        try:
            self.coef_ = types[self.type](x=self._x, y=self._y)
        except KeyError as e:
            print('Incorrect type', e)

    def predict(self, x: pd.DataFrame):
        x_ = copy.deepcopy(x)
        x_['ones'] = np.ones(x_.shape[0])
        y_pred = pd.DataFrame(data=np.array(x_.dot(self.coef_.T)), columns=[output_feature])
        return y_pred


def mvp_predictor():
    try:
        x_train = pd.read_csv('data/x_train.csv', index_col=0)
        x_test = pd.read_csv('data/x_test.csv', index_col=0)
        y_train = pd.read_csv('data/y_train.csv', index_col=0)
        y_test = pd.read_csv('data/y_test.csv', index_col=0)
    except FileNotFoundError:
        x_train, x_test, y_train, y_test = prepare_data()
    reg = GdReggression(type='bgd', max_iter=2000, alpha=0.05)
    reg.fit(x_train, y_train)
    print('Coefs:', reg.coef_[1:, ])
    print('Intercept_:', reg.coef_[0, :])
    y_pred = reg.predict(x_test)
    print('R2:', r2_score(y_test, y_pred))
    print('MAE:', mean_absolute_error(y_test, y_pred))
    print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
    return reg
