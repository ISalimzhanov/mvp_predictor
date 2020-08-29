import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_mvp_data(year: int) -> pd.DataFrame:
    # time.sleep(2)

    def get_name(txt: str):
        name = ''
        for c in txt:
            if c.isalpha() or c == ' ':
                name += c
        return name

    def pts_won(tag):
        return tag.has_attr('data-stat') and tag['data-stat'] == 'points_won'

    def player_name(tag):
        return tag.has_attr('data-stat') and tag['data-stat'] == 'player'

    url = f'https://www.basketball-reference.com/awards/awards_{year}.html'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('tbody')
    entries = table.find_all('tr')
    mvp_data = {'name': [], 'year': [], 'mvp_score': []}
    for e in entries:
        p_name = get_name(e.find(player_name).get_text())
        mvp_score = e.find(pts_won).get_text()
        mvp_data['name'].append(p_name)
        mvp_data['year'].append(year)
        mvp_data['mvp_score'].append(mvp_score)
    return pd.DataFrame(mvp_data)
