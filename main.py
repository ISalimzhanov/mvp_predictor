from config import end_year
from ml_methods.linear_regression import mvp_predictor
from data_preparation.unknown_mvp import next_mvp_prediction_data
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    reg = mvp_predictor()
    try:
        nba_mvp_2020 = pd.read_csv(f'data/mvp_{end_year + 1}.csv', index_col=0)
    except FileNotFoundError:
        nba_mvp_2020 = next_mvp_prediction_data()
    predicted_mvp = reg.predict(nba_mvp_2020.drop(columns=['name', 'basket_ref_chance']))
    predicted_mvp = pd.DataFrame(predicted_mvp, columns=['mvp_score'])
    predicted_mvp['name'] = nba_mvp_2020['name']
    predicted_mvp['mvp_score'] = predicted_mvp['mvp_score'].sub(predicted_mvp['mvp_score'].min())
    predicted_mvp['mvp_score'] = predicted_mvp['mvp_score'].div(predicted_mvp['mvp_score'].sum())
    predicted_mvp['mvp_score'] *= 1010
    predicted_mvp.to_csv('prediction.csv')

    plt.bar(nba_mvp_2020['name'], nba_mvp_2020['basket_ref_chance'])
    plt.tight_layout()
    plt.show()
    plt.clf()
    plt.bar(nba_mvp_2020['name'], predicted_mvp['mvp_score'])
    plt.tight_layout()
    plt.show()
