import pandas as pd
import numpy as np
import random
import copy
import time

from sklearn.linear_model import SGDRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from config import output_feature
from data_preparation.data_preparation import prepare_data


def calc_gradient(x: pd.DataFrame, loss: np.array, alpha: float, type: str, batch_size=50) -> np.array:
    if type != 'sgd' and type != 'bgd' and type != 'mbgd':
        raise ValueError
    random.seed(time.time())
    grad = np.zeros(shape=(1, x.shape[1]))
    if type == 'sgd':
        i = random.randint(0, x.shape[0] - 1)
        for j in range(x.shape[1]):
            grad[0, j] += alpha * loss.iloc[i, 0] * pow(x.iloc[i, j], j)
    elif type == 'bgd':
        grad = alpha * np.dot(loss.T, x) / x.shape[0]
    else:
        batch_ind = random.randint(0, int(x.shape[0] / batch_size))
        for j in range(x.shape[1]):
            for i in range(batch_ind * batch_size, min(x.shape[0], (batch_ind + 1) * batch_size)):
                grad[0, j] += 1. / batch_size * alpha * loss.iloc[i, 0] * pow(x.iloc[i, j], j)
    return grad


class GdReggression:
    # ToDo fix
    def __init__(self, type: str, alpha: float, max_iter: int, is_adaptive=False):
        if type != 'sgd' and type != 'bgd' and type != 'mbgd':
            raise AttributeError
        self.type = type
        self.alpha = alpha
        self.max_iter = max_iter
        self._x = None
        self._y = None
        self.coef_ = None
        self.is_adaptive = is_adaptive

    def fit(self, x: pd.DataFrame, y: pd.DataFrame) -> None:
        self._x = copy.deepcopy(x)
        self._y = copy.deepcopy(y)
        self.coef_calc()

    def coef_calc(self) -> None:
        random.seed(time.time())
        self._x.insert(0, '_', np.ones(self._x.shape[0]))
        self.coef_ = np.random.rand(1, self._x.shape[1])
        for _ in range(self.max_iter):
            y_hat = self._x.dot(self.coef_.T)
            loss = y_hat - self._y.values
            gradient = calc_gradient(self._x, loss, self.alpha, self.type)
            if self.is_adaptive:
                nloss = self._x.dot((self.coef_ - gradient).T) - self._y.values
                if np.square(nloss[0]).sum() < np.square(loss[0]).sum():
                    self.coef_ -= gradient
                else:
                    self.alpha /= 2
            else:
                self.coef_ -= gradient

    def predict(self, x: pd.DataFrame):
        x_ = copy.deepcopy(x)
        x_['ones'] = np.ones(x_.shape[0])
        y_pred = pd.DataFrame(data=np.array(x_.dot(self.coef_.T)), columns=[output_feature])
        return y_pred


def mvp_predictor(**kwargs):
    try:
        x_train = pd.read_csv('data/x_train.csv', index_col=0)
        x_test = pd.read_csv('data/x_test.csv', index_col=0)
        y_train = pd.read_csv('data/y_train.csv', index_col=0)
        y_test = pd.read_csv('data/y_test.csv', index_col=0)
    except FileNotFoundError:
        x_train, x_test, y_train, y_test = prepare_data()
    # reg = GdReggression(type='bgd', max_iter=5000, alpha=1, is_adaptive=True)
    reg = SGDRegressor(max_iter=50000, warm_start=True, learning_rate='adaptive')
    reg.fit(x_train, np.ravel(y_train))
    print('Coefs:', reg.coef_)
    print('Intercept_:', reg.intercept_)
    print('Score:', reg.score(x_train, np.ravel(y_train)))
    y_pred = reg.predict(x_test)
    print('R2:', r2_score(y_test, y_pred))
    print('MAE:', mean_absolute_error(y_test, y_pred))
    print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
    return reg
