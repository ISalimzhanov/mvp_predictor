from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def get_stat_data(year: int, p_names: list, stat_type: str, needed_attrs: list) -> pd.DataFrame:
    # time.sleep(2)
    def get_name(txt: str):
        name = ''
        for c in txt:
            if c.isalpha() or c == ' ':
                name += c
        return name

    def player_name(tag):
        return tag.has_attr('data-stat') and tag['data-stat'] == 'player'

    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_{stat_type}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('tbody')
    entries = table.find_all('tr')
    adv_stats = []
    used_names = {}
    for e in entries:
        p_name = get_name(e.find(player_name).get_text())
        if p_name not in p_names or p_name in used_names:
            continue
        used_names[p_name] = True
        p_stat = {'name': p_name}
        for attr in needed_attrs:
            def specific_stat_attr(tag):
                return tag.has_attr('data-stat') and tag['data-stat'] == attr

            p_stat[attr] = e.find(specific_stat_attr).get_text()
        adv_stats.append(p_stat)
    return pd.DataFrame(adv_stats)
