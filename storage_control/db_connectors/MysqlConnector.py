import pandas as pd
import mysql.connector
from storage_control.db_connectors.databaseConnector import DatabaseConnector


class MysqlConnector(DatabaseConnector):
    def __init__(self):
        database_info = {
            'database': 'Nba',
            'host': 'localhost',
            'user': 'user1',
            'password': 'Password123@#!'
        }
        self.conn = mysql.connector.connect(**database_info)
        self.create_tables()

    def create_tables(self):
        tables = {
            'Player': 'CREATE TABLE Player('
                      'player_id VARCHAR (9) PRIMARY KEY, '
                      'name VARCHAR (64)'
                      ');',
            'Advanced': 'CREATE TABLE Advanced('
                        'year INTEGER,'
                        'player_id VARCHAR (9),'
                        'ws FLOAT (3), '
                        'dws FLOAT (3),'
                        'vorp FLOAT (3),'
                        'ts_pct FLOAT (3),'
                        'per FLOAT (3),'
                        'PRIMARY KEY (year, player_id),'
                        'FOREIGN KEY (player_id) REFERENCES Player(player_id)'
                        ');',
            'PerGame': 'CREATE TABLE PerGame('
                       'year INTEGER,'
                       'player_id VARCHAR (9),'
                       'g INTEGER , '
                       'age INTEGER ,'
                       'pts_per_g FLOAT (3),'
                       'trb_per_g FLOAT (3),'
                       'ast_per_g FLOAT (3),'
                       'stl_per_g FLOAT (3),'
                       'blk_per_g FLOAT (3),'
                       'mp_per_g FLOAT (3),'
                       'fg_pct FLOAT (3),'
                       'PRIMARY KEY (year, player_id),'
                       'FOREIGN KEY (player_id) REFERENCES Player(player_id)'
                       ');',
            'MVPScore': 'CREATE TABLE MVPScore('
                        'player_id VARCHAR (9),'
                        'year INTEGER, '
                        'points_won INTEGER,'
                        'points_max INTEGER,'
                        'PRIMARY KEY (year, player_id),'
                        'FOREIGN KEY (player_id) REFERENCES Player(player_id)'
                        ');'
        }
        with self.conn.cursor() as cursor:
            for table_name, query in tables.items():
                try:
                    cursor.execute(query)
                    self.conn.commit()
                except Exception as e:
                    print(e)

    def get_data(self, query: str) -> pd.DataFrame:
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            columns = [i[0] for i in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
        return pd.DataFrame(data)

    def get_advanced(self, year: int) -> pd.DataFrame:
        query = 'SELECT * ' \
                'FROM Advanced as adv ' \
                f'WHERE adv.year = {year};'
        return self.get_data(query)

    def get_per_game(self, year: int) -> pd.DataFrame:
        query = 'SELECT * ' \
                'FROM PerGame as pg ' \
                f'WHERE pg.year = {year};'
        return self.get_data(query)

    def get_mvp_score(self, year: int) -> pd.DataFrame:
        query = 'SELECT * ' \
                'FROM MVPScore as mvp ' \
                f'WHERE mvp.year = {year};'
        return self.get_data(query)

    def add_data(self, query: str, data: list):
        with self.conn.cursor() as cursor:
            cursor.executemany(query, data)
            self.conn.commit()

    def add_advanced(self, df: pd.DataFrame) -> None:
        query = 'INSERT INTO Advanced ({}) ' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s)'.format(', '.join(col for col in df.columns))
        data = [tuple(val) for val in df.T.to_dict(orient='list').values()]
        self.add_data(query, data)

    def add_mvp_score(self, df: pd.DataFrame) -> None:
        query = 'INSERT INTO MVPScore ({}) ' \
                'VALUES (%s, %s, %s, %s)'.format(', '.join(col for col in df.columns))
        data = [tuple(val) for val in df.T.to_dict(orient='list').values()]
        self.add_data(query, data)

    def add_per_game(self, df: pd.DataFrame) -> None:
        query = 'INSERT INTO PerGame({}) ' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'.format(', '.join(col for col in df.columns))
        data = [tuple(val) for val in df.T.to_dict(orient='list').values()]
        self.add_data(query, data)

    def add_players(self, df: pd.DataFrame) -> None:
        n_rows = df.shape[0]
        players = df.to_dict(orient='list')
        existed_query = 'SELECT player_id ' \
                        'FROM Player as player ' \
                        'WHERE player.player_id IN ({})'.format(', '.join('%s' for unused in players['player_id']))
        insert_query = 'INSERT INTO Player VALUES (%s, %s)'
        with self.conn.cursor() as cursor:
            cursor.execute(existed_query, players['player_id'])
            existed = cursor.fetchall()
            not_existed = [(players["player_id"][i], players["name"][i])
                           for i in range(n_rows) if players["player_id"][i] not in existed]
        self.add_data(insert_query, not_existed)
