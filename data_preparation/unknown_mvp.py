from config import end_year, adv_stat_attrs, per_game_stat_attrs
from data_preparation.data_preparation import scale_data, modify_data
from data_preparation.data_preprocessing import compare_by_year
from parsers.mvp_tracker_data import get_mvp_tracker_data
from parsers.stat_data import get_stat_data
import pandas as pd


def next_mvp_prediction_data() -> pd.DataFrame():
    mvp_tracker_data = get_mvp_tracker_data()
    p_names = mvp_tracker_data['name'].tolist()
    adv_data = get_stat_data(year=end_year + 1, p_names=p_names, stat_type='advanced', needed_attrs=adv_stat_attrs)
    per_game_data = get_stat_data(year=end_year + 1, p_names=p_names, stat_type='per_game',
                                  needed_attrs=per_game_stat_attrs)
    data = adv_data
    data = data.merge(per_game_data, on='name')
    data.drop(columns=['name'], inplace=True)
    # Data preprocessing assumes that there is no categorical features. Thus, colunm name should be deleted
    data['year'] = [end_year + 1] * len(p_names)
    data = compare_by_year(data, end_year + 1)
    data.drop(columns=['year'], inplace=True)
    data = scale_data(data)
    data = modify_data(data)
    # Adding some column for better presentability
    data['basket_ref_chance'] = mvp_tracker_data['award_prob']
    data['name'] = p_names
    data.to_csv(f'data/mvp_{end_year + 1}.csv')
    # Ready for be prediction data (columns 'basket_ref_chance', 'name' needed only for plotting)
    return data
