import copy
from datetime import datetime

from processing.preprocessing.data_preprocessing import Preprocessor
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from storage_control.db_connectors.databaseConnector import DatabaseConnector


class Preparator:
    def __new__(cls, *args, **kwargs):
        if not hasattr(Preparator, '_instance'):
            setattr(Preparator, '_instance', super(Preparator, cls).__new__(cls))
        return getattr(Preparator, '_instance')

    def __init__(self, db_conn: DatabaseConnector):
        self.db_conn = db_conn
        self.output_feature = 'mvp_score'
        self.store_path = 'processing/data'

    def scale_data(self, data: pd.DataFrame) -> pd.DataFrame:
        df = copy.deepcopy(data)
        not_y = df.columns != self.output_feature
        df.loc[:, not_y] = MinMaxScaler().fit_transform(df.loc[:, not_y].values)
        return df

    def run(self) -> tuple:
        try:
            df = pd.read_csv(f'{self.store_path}/preprocessed.csv', index_col=0)
        except FileNotFoundError:
            df = Preprocessor(self.db_conn).run()
        end_year = datetime.today().year
        this_year = df['year'] == end_year
        not_this_year = df['year'] != end_year

        test_data = df.drop(['year', 'player_id'], axis=1).loc[this_year, :]
        train_data = df.drop(['year', 'player_id'], axis=1).loc[not_this_year, :]

        train_data = self.scale_data(train_data)
        test_data = self.scale_data(test_data)
        train_data.fillna(train_data.mean(), inplace=True)
        test_data.fillna(test_data.mean(), inplace=True)
        test_data['player_id'] = df.loc[this_year, 'player_id']

        x_train = train_data.loc[:, train_data.columns != self.output_feature]
        y_train = train_data[self.output_feature]
        x_test = test_data.loc[:, test_data.columns != self.output_feature]
        x_train.to_csv(f'{self.store_path}/x_train.csv')
        x_test.to_csv(f'{self.store_path}/x_test.csv')
        y_train.to_csv(f'{self.store_path}/y_train.csv')
        return x_train, y_train, x_test
