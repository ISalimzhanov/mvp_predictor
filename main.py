import argparse
import os

import matplotlib.pyplot as plt
from processing.ml_algorithms.lsPredictor import LsPredictor
from processing.ml_algorithms.sgdPredictor import SgdPredictor
from storage_control.db_connectors.databaseConnector import DatabaseConnector
from storage_control.db_connectors.mysqlConnector import MysqlConnector
from presentation.web_interface import app


def plot_predictions(db_conn: DatabaseConnector):
    predictors = {
        'LeastSquares': LsPredictor(db_conn),
        'SGD': SgdPredictor(db_conn)
    }
    for method_name, predictor in predictors.items():
        prediction = predictor.predict()
        plt.clf()
        plt.figure(figsize=(10, 10))
        plt.plot(prediction['name'], prediction['mvp_prob'], 'o')
        plt.xlabel('Name')
        plt.ylabel('MVP Probability%')
        plt.xticks(rotation=90)
        plt.legend()
        plt.savefig(f'presentation/static/{method_name}.png')


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
    parser.add_argument("-type", help=f"Type of the database. Currently available types: {tuple(connectors.keys())}",
                        type=str)
    parser.add_argument('-scrap', help=f"Is needed to scrap all data during the launch?", type=bool)
    args = parser.parse_args()
    os.environ['db_name'] = args.db_name
    os.environ['db_host'] = args.db_host
    os.environ['db_user'] = args.db_user
    os.environ['db_pass'] = args.db_pass
    os.environ['start_year'] = args.start_year
    conn = connectors[args.type]()
    plot_predictions(conn)
    app.run(debug=True, host='0.0.0.0', port=8080)
