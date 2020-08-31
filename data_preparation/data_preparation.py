from data_preparation.data_preprocessing import preprocess_data
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, RobustScaler
from config import modification_rules, output_feature
import copy
from sklearn.model_selection import train_test_split


def scale_data(data: pd.DataFrame) -> pd.DataFrame:
    df = copy.deepcopy(data)
    not_y = df.columns != output_feature
    df.loc[:, not_y] = MinMaxScaler().fit_transform(df.loc[:, not_y].values)
    return df


def modify_data(data: pd.DataFrame) -> pd.DataFrame:
    df = copy.deepcopy(data)
    with_all = modification_rules['all']  # feature that should be multiplied with all other features
    for feature in with_all:
        for other_feature in data.columns:
            if other_feature == feature or other_feature in modification_rules['ignore']:
                continue
            df[f'{feature}_{other_feature}'] = df[feature].mul(df[other_feature])
    for feature, mult_with in modification_rules.items():
        if feature == 'all' or feature == 'ignore':
            continue
        for other_feature in mult_with:
            df[f'{feature}_{other_feature}'] = df[feature].mul(df[other_feature])
    return df


def split_data(data: pd.DataFrame) -> tuple:
    x_train, x_test, y_train, y_test = train_test_split(data.loc[:, data.columns != output_feature],
                                                        data[output_feature], test_size=0.2,
                                                        random_state=True)
    return x_train, x_test, y_train, y_test


def prepare_data() -> tuple:
    try:
        df = pd.read_csv('data/preprocessed.csv', index_col=0)
    except FileNotFoundError:
        df = preprocess_data()
    df = scale_data(df)
    df = modify_data(df)
    df.fillna(df.mean(), inplace=True)
    x_train, x_test, y_train, y_test = split_data(df)
    x_train.to_csv('data/x_train.csv')
    x_test.to_csv('data/x_test.csv')
    y_train.to_csv('data/y_train.csv')
    y_test.to_csv('data/y_test.csv')
    return x_train, x_test, y_train, y_test
