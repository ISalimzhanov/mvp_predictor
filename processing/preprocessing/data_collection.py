import pandas as pd
from datetime import datetime
import os

from storage_control.db_connectors.databaseConnector import DatabaseConnector


class Collector:
    def __new__(cls, *args, **kwargs):
        if not hasattr(Collector, '_instance'):
            setattr(Collector, '_instance', super(Collector, cls).__new__(cls))
        return getattr(Collector, '_instance')

    def __init__(self, db_conn: DatabaseConnector):
        self.db_conn = db_conn
        self.store_path = 'processing/data'

    def run(self) -> pd.DataFrame:
        df = pd.DataFrame()
        end_year = datetime.today().year
        start_year = int(os.environ['start_year'])
        for year in range(start_year, end_year + 1):
            mvp_data = self.db_conn.get_mvp_score(year)
            adv_data = self.db_conn.get_advanced(year)
            per_game_data = self.db_conn.get_per_game(year)
            year_data = adv_data
            year_data = year_data.merge(per_game_data, on=['player_id', 'year'])
            year_data = year_data.merge(mvp_data, on=['player_id', 'year'])
            df = pd.concat([df, year_data], ignore_index=True)
        df.to_csv(f'{self.store_path}/collected.csv')
        return df
