import argparse
import os
from datetime import datetime

from storage_control.db_connectors.MysqlConnector import MysqlConnector
from storage_control.db_connectors.databaseConnector import DatabaseConnector


def run_storage(connector: DatabaseConnector):
    connector.launch()
    while True:
        now = datetime.now()
        if not now.hour and not now.minute:
            connector.update(now.year)


if __name__ == '__main__':
    connectors = {
        'mysql': MysqlConnector
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("-db_name", help="Database name", type=str)
    parser.add_argument("-db_host", help="Database host", type=str)
    parser.add_argument("-db_user", help="Database user", type=str)
    parser.add_argument("-db_pass", help="Database user's password", type=str)
    parser.add_argument("-start_year", help="Starting from which year data should be scraped", type=str)
    parser.add_argument("-type", help=f"Type of the database. Currently available types: {tuple(connectors.keys())}", type=str)
    args = parser.parse_args()
    os.environ['db_name'] = args.db_name
    os.environ['db_host'] = args.db_host
    os.environ['db_user'] = args.db_user
    os.environ['db_pass'] = args.db_pass
    os.environ['start_year'] = args.start_year
    try:
        run_storage(connectors[args.type]())
    except KeyError:
        print('Incorrect type')
