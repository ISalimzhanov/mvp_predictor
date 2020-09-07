from abc import ABC, abstractmethod
import pandas as pd


class Regressor(ABC):
    def __init__(self, reg):
        self.reg = reg

    @abstractmethod
    def fit(self, x_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def make_prediction(self, x_test: pd.DataFrame) -> pd.DataFrame:
        pass
