import os
from datetime import datetime

import pandas as pd
import copy
from processing.preprocessing.data_collection import Collector
from storage_control.db_connectors.databaseConnector import DatabaseConnector


class Preprocessor:
    def __new__(cls, *args, **kwargs):
        if not hasattr(Preprocessor, '_instance'):
            setattr(Preprocessor, '_instance', super(Preprocessor, cls).__new__(cls))
        return getattr(Preprocessor, '_instance')

    def __init__(self, db_conn: DatabaseConnector):
        self.db_conn = db_conn
        self.not_to_compare = ['player_id', 'age', 'year', 'ws', 'mp_per_g', 'points_won', 'g', 'points_max']
        self.store_path = 'processing/data'

    def compare_by_year(self, df: pd.DataFrame, year: int) -> pd.DataFrame:
        df = copy.deepcopy(df)
        this_year = df['year'] == year
        for feature in df.columns:
            if feature in self.not_to_compare:
                continue
            df.loc[this_year, feature] = df.loc[this_year, feature].astype(float)
            df.loc[this_year, feature] = df.loc[this_year, feature].div(df.loc[this_year, feature].mean())
        return df

    def run(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(f'{self.store_path}/collected.csv', index_col=0)
        except FileNotFoundError:
            df = Collector(self.db_conn).run()

        end_year = datetime.today().year
        start_year = int(os.environ['start_year'])
        for year in (start_year, end_year + 1):
            df = self.compare_by_year(df, year)
        df['mvp_score'] = df['points_won'] / df['points_max']
        df.drop(columns=['points_won', 'points_max'], inplace=True)
        df.to_csv(f'{self.store_path}/preprocessed.csv')
        return df
