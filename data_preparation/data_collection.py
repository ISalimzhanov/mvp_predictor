from config import start_year, end_year, adv_stat_attrs, per_game_stat_attrs
from parsers.mvp_data import get_mvp_data
from parsers.stat_data import get_stat_data
import pandas as pd


def collect_data() -> pd.DataFrame:
    df = pd.DataFrame()
    for year in range(start_year, end_year + 1):
        mvp_data = get_mvp_data(year)
        p_names = mvp_data['name'].tolist()
        adv_data = get_stat_data(year=year, p_names=p_names, stat_type='advanced', needed_attrs=adv_stat_attrs)
        per_game_data = get_stat_data(year=year, p_names=p_names, stat_type='per_game',
                                      needed_attrs=per_game_stat_attrs)
        year_data = adv_data
        year_data = year_data.merge(per_game_data, on='name')
        year_data = year_data.merge(mvp_data, on='name')
        year_data['year'] = [year] * len(p_names)
        df = pd.concat([df, year_data], ignore_index=True)
    df.to_csv('data/collected.csv')
    return df
