from abc import ABC, abstractmethod
import pandas as pd


class DatabaseConnector(ABC):
    def __new__(cls, *args, **kwargs):
        if not hasattr(DatabaseConnector, '_instance'):
            setattr(DatabaseConnector, '_instance', super(DatabaseConnector, cls).__new__(cls))
        return getattr(DatabaseConnector, '_instance')

    @abstractmethod
    def launch(self) -> None:
        pass

    @abstractmethod
    def update(self, year: int) -> None:
        pass
        
    @abstractmethod
    def get_advanced(self, year: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_per_game(self, year: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_mvp_score(self, year: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def add_advanced(self, data: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def add_per_game(self, data: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def add_mvp_score(self, data: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def add_players(self, df: pd.DataFrame) -> None:
        pass
