from config import not_to_compare, start_year, end_year
import pandas as pd
import copy

from data_preparation.data_collection import collect_data


def compare_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df = copy.deepcopy(df)
    this_year = df['year'] == year
    for feature in df.columns:
        if feature in not_to_compare:
            continue
        df.loc[this_year, feature] = df.loc[this_year, feature].astype(float)
        df.loc[this_year, feature] = df.loc[this_year, feature].div(df.loc[this_year, feature].mean())
    return df


def preprocess_data() -> pd.DataFrame:
    try:
        df = pd.read_csv('data/collected.csv', index_col=0)
    except FileNotFoundError:
        df = collect_data()
    for year in (start_year, end_year + 1):
        df = compare_by_year(df, year)
    df.drop(columns=['name', 'year'], inplace=True)
    df.to_csv('data/preprocessed.csv')
    return df
