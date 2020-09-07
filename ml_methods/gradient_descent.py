from sklearn.model_selection import GridSearchCV
import json
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import r2_score, make_scorer
import pandas as pd

from ml_methods.regressor import Regressor


class SGD(Regressor):
    def __init__(self, **kwargs):
        try:
            with open('ml_methods/best_params/sgd_params.json', 'r') as f:
                params = json.load(f)
                reg = SGDRegressor()
                reg.__dict__.update(params)
                super(SGD, self).__init__(reg)
        except FileNotFoundError:
            super(SGD, self).__init__(SGD.best_estimator(**kwargs))

    @staticmethod
    def best_estimator(x_train: pd.DataFrame, y_train: pd.DataFrame) -> SGDRegressor:
        params = {
            'loss': ['squared_loss', 'squared_epsilon_insensitive', 'huber'],
            'penalty': ['l2', 'l1'],
            'learning_rate': ['adaptive', 'optimal'],
        }
        grid = GridSearchCV(SGDRegressor(), param_grid=params,
                            scoring=make_scorer(r2_score), cv=10,  n_jobs=-1).fit(x_train, y_train)
        reg = grid.best_estimator_
        with open('ml_methods/best_params/sgd_params.json', 'w') as f:
            json.dump(grid.best_params_, f)
        return reg

    def fit(self, x_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
        self.reg.fit(x_train, y_train)

    def make_prediction(self, x_test: pd.DataFrame) -> pd.DataFrame:
        return self.reg.predict(x_test)
