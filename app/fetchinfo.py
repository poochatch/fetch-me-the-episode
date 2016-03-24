from aport_conf import data_seeds, data_seed_current
import requests as req, re
import bs4, os, sys

def episode_int_to_string(self, season, episode):
    s_str, e_str = str(season),str(episode)
    return 's%se%s' %(s_str,e_str)

def correct_url(url):
    # correct invalid url
    pass

headers = {'User-Agent':'Mozilla/5.0'}
class FetchInfo():
    # Fetch season and episode info from web
    def __init__(self):
        self.data_seed = data_seeds[data_seed_current] 

    def fetch(self, series_url):
        # return requests.models.Response object
        url = self.data_seed + series_url
        response = req.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response

    def parse(self, response):
        # return string 's%se%s' %(season, episode)
        # correct form: 's01e02', 's12e10'
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        last_episode_info = soup.select('div #previous_episode')
        txt = last_episode_info[0].getText()
        self.txt = txt
        self.season = re.search(r'n:\d+',txt)
        self.episode = re.search(r'e:\d+',txt)
        s_span = self.season.span()
        e_span = self.episode.span()
        season = int(txt[s_span[0]:s_span[1]][2:])
        episode = int(txt[e_span[0]:e_span[1]][2:])
        return (season,episode)

    
    def get_top_watched(self):
        url = self.data_seed
        response = req.get(url, headers=headers, verify=False)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        top_watched_list = soup.select('#watchliststring > a')
        urls = [(title.text, title.get('href')) for title in top_watched_list]    
        return urls

