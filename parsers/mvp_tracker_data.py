import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_mvp_tracker_data() -> pd.DataFrame:
    def get_name(txt: str):
        name = ''
        for c in txt:
            if c.isalpha() or c == ' ':
                name += c
        return name

    def player_name(tag):
        return tag.has_attr('data-stat') and tag['data-stat'] == 'player'

    def award_prob(tag):
        return tag.has_attr('data-stat') and tag['data-stat'] == 'value'

    url = 'https://www.basketball-reference.com/friv/mvp.html'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('tbody')
    entries = table.find_all('tr')
    mvp_tracker = {'name': [], 'award_prob': []}
    for e in entries:
        p_name = get_name(e.find(player_name).get_text())
        chance = float(e.find(award_prob).get_text()[:-1])
        mvp_tracker['name'].append(p_name)
        mvp_tracker['award_prob'].append(chance)
    return pd.DataFrame(mvp_tracker)
