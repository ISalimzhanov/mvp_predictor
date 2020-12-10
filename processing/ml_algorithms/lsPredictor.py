from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import pandas as pd

from processing.ml_algorithms.predictor import Predictor
from processing.preprocessing.data_preparation import Preparator
from storage_control.db_connectors.databaseConnector import DatabaseConnector


class LsPredictor(Predictor):
    def __new__(cls, *args, **kwargs):
        kwargs.get('db_conn')
        if not hasattr(LsPredictor, '_instance'):
            setattr(LsPredictor, '_instance', super(LsPredictor, cls).__new__(cls))
        return getattr(LsPredictor, '_instance')

    def __init__(self, db_conn: DatabaseConnector):
        self.reg = LinearRegression()
        super(LsPredictor, self).__init__(db_conn=db_conn)

    @staticmethod
    def regularize(data: pd.DataFrame):
        pca = PCA(data.shape[1])
        pca.fit(data)
        exp_var = dict(zip(data.columns, pca.explained_variance_ratio_))
        exp_var = sorted(exp_var.items(), key=lambda x: -x[1])

        exp_total = 0
        i = 0
        while exp_total < 0.99:
            exp_total += exp_var[i][1]
            yield exp_var[i][0]
            i += 1

    def predict(self) -> pd.DataFrame:
        try:
            x_train = pd.read_csv('processing/data/x_train.csv', index_col=0)
            x_test = pd.read_csv('processing/data/x_test.csv', index_col=0)
            y_train = pd.read_csv('processing/data/y_train.csv', index_col=0)
        except FileNotFoundError:
            x_train, x_test, y_train = Preparator(self.db_conn)
        use_columns = [col for col in LsPredictor.regularize(x_train)]
        self.train(x_train[use_columns], y_train)
        res = pd.DataFrame()
        res['name'] = self.db_conn.get_players(list(x_test['player_id'].to_dict().values()))
        res['mvp_prob'] = self.reg.predict(x_test[use_columns])

        res['mvp_prob'] = res['mvp_prob'].sub(res['mvp_prob'].min())
        res['mvp_prob'] = res['mvp_prob'].div(res['mvp_prob'].sum())
        return res

    def train(self, x_train: pd.DataFrame, y_train: pd.DataFrame):
        self.reg.fit(x_train, y_train)
