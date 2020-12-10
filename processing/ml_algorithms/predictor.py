from abc import ABC, abstractmethod
import pandas as pd

from storage_control.db_connectors.databaseConnector import DatabaseConnector


class Predictor(ABC):
    def __init__(self, db_conn: DatabaseConnector):
        self.db_conn = db_conn

    @abstractmethod
    def train(self, x_train: pd.DataFrame, y_train: pd.DataFrame):
        pass

    @abstractmethod
    def predict(self):
        pass
