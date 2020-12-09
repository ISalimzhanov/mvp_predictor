import requests
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp
import time


class Scraper:
    @staticmethod
    def _is_player(tag):
        return tag.has_attr('data-stat') and tag['data-stat'] == 'player' and tag.has_attr('data-append-csv')

    @staticmethod
    async def scrap_mvp_by_year(year: int) -> pd.DataFrame:
        async with aiohttp.ClientSession() as session:
            def pts_won(tag):
                return tag.has_attr('data-stat') and tag['data-stat'] == 'points_won'

            def pts_max(tag):
                return tag.has_attr('data-stat') and tag['data-stat'] == 'points_max'

            url = f'https://www.basketball-reference.com/awards/awards_{year}.html'
            response = await session.get(url)
            soup = BeautifulSoup(await response.text(), 'html.parser')
            table = soup.find('tbody')
            entries = table.find_all('tr')
            mvp_data = {'name': [], 'year': [], 'points_won': [], 'points_max': [], 'player_id': []}
            for e in entries:
                player = e.find(Scraper._is_player)
                name = player.get_text()
                player_id = player['data-append-csv']
                points_won = float(e.find(pts_won).get_text())
                points_max = int(e.find(pts_max).get_text())

                mvp_data['name'].append(name)
                mvp_data['year'].append(year)
                mvp_data['player_id'].append(player_id)
                mvp_data['points_max'].append(points_max)
                mvp_data['points_won'].append(int(points_won))
            return pd.DataFrame(mvp_data)

    @staticmethod
    async def scrap_stats_by_year(year: int, stat_type: str, needed_attrs: list) -> pd.DataFrame:
        async with aiohttp.ClientSession() as session:
            url = f'https://www.basketball-reference.com/leagues/NBA_{year}_{stat_type}.html'
            response = await session.get(url)
            soup = BeautifulSoup(await response.text(), 'html.parser')
            table = soup.find('tbody')
            entries = table.find_all('tr')
            delete_g: bool = False
            if 'g' not in needed_attrs:
                needed_attrs.append('g')
                delete_g = True
            stats = []
            for e in entries:
                player = e.find(Scraper._is_player)
                if not player:
                    continue
                name = player.get_text()
                player_id = player['data-append-csv']
                p_stat = {'name': name, 'player_id': player_id}
                for attr in needed_attrs:
                    def specific_stat_attr(tag):
                        return tag.has_attr('data-stat') and tag['data-stat'] == attr

                    try:
                        p_stat[attr] = float(e.find(specific_stat_attr).get_text())
                    except ValueError:
                        p_stat[attr] = 0
                if stats and player_id == stats[len(stats) - 1]['player_id']:
                    last_stats = stats[len(stats) - 1]
                    for attr in needed_attrs:
                        if attr == 'g':
                            continue
                        last_stats[attr] = (last_stats[attr] * last_stats['g'] + p_stat[attr] * p_stat['g']) / (
                                last_stats['g'] + p_stat['g'])
                    last_stats['g'] += p_stat['g']
                else:
                    stats.append(p_stat)
            df = pd.DataFrame(stats)
            if delete_g:
                df = df.loc[:, df.columns != 'g']
            return df

    @staticmethod
    async def scrap_stats_by_period(start_year: int, end_year: int, stat_type: str, needed_attrs: list) -> pd.DataFrame:
        res = pd.DataFrame()
        for year in range(start_year, end_year):
            df = await Scraper.scrap_stats_by_year(year=year, stat_type=stat_type, needed_attrs=needed_attrs)
            pd.concat([res, df], ignore_index=True)
        return res

