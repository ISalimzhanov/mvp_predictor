from sklearn.linear_model import SGDRegressor
import pandas as pd

from processing.ml_algorithms.predictor import Predictor
from processing.preprocessing.data_preparation import Preparator
from storage_control.db_connectors.databaseConnector import DatabaseConnector


class SgdPredictor(Predictor):
    def __new__(cls, *args, **kwargs):
        kwargs.get('db_conn')
        if not hasattr(SgdPredictor, '_instance'):
            setattr(SgdPredictor, '_instance', super(SgdPredictor, cls).__new__(cls))
        return getattr(SgdPredictor, '_instance')

    def __init__(self, db_conn: DatabaseConnector):
        self.reg = SGDRegressor(learning_rate='adaptive', loss='squared_loss', penalty='l1')
        super(SgdPredictor, self).__init__(db_conn=db_conn)

    def predict(self) -> pd.DataFrame:
        try:
            x_train = pd.read_csv('processing/data/x_train.csv', index_col=0)
            x_test = pd.read_csv('processing/data/x_test.csv', index_col=0)
            y_train = pd.read_csv('processing/data/y_train.csv', index_col=0)
        except FileNotFoundError:
            x_train, x_test, y_train = Preparator(self.db_conn).run()
        self.train(x_train, y_train)
        res = pd.DataFrame()
        res['name'] = self.db_conn.get_players(list(x_test['player_id'].to_dict().values()))
        res['mvp_prob'] = self.reg.predict(x_test.loc[:, x_test.columns != 'player_id'])
        res['mvp_prob'] = res['mvp_prob'].sub(res['mvp_prob'].min())
        res['mvp_prob'] = res['mvp_prob'].div(res['mvp_prob'].sum())
        return res

    def train(self, x_train: pd.DataFrame, y_train: pd.DataFrame):
        self.reg.fit(x_train, y_train)
