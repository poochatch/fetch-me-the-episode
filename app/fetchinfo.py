from aport_conf import data_seeds, data_seed_current
import requests as req, re
import bs4, os, sys


headers = {'User-Agent':'Mozilla/5.0'}
class FetchInfo():
    # Fetch season and episode of a last episode from web
    def __init__(self):
        self.data_seed = data_seeds[data_seed_current] 

    def resolve_url(self, series_title):
        # find correct series_url for a gives tv-series
        return 'Not implemented!'

    def fetch(self, series_url):
        # return requests.models.Response object
        if  not series_url.startswith('/'):
            series_url = '/' + series_url
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

    def episode_int_to_string(self, season, episode):
        s_str, e_str = str(season),str(episode)
        return 's%se%s' %(s_str,e_str)
    
    def get_top_watched(self):
        url = self.data_seed
        response = req.get(url, headers=headers, verify=False)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        top_watched_list = soup.select('#watchliststring > a')
        urls = [(title.text, title.get('href')) for title in top_watched_list]    
        return urls

    def read_last_watched(self, series_title):
        # read last downloaded episode from a file
        pass 
        
    def get_field(self, search_field, search_value, search_buffer):
        buffer = getattr(buffer_dict[search_buffer],'buffer')
        return [line[BUFFER_DICT[search_field]] for line in buffer if line[BUFFER_DICT[search_field]] == search_value]
             
        

    def not_watched(self, last_seen, last_aired):
        # return a list of strings ( see: FetchInfo.parse() )
        # representing all episodes that hasn`t been seen yet
        # sorted oldest first
        pass


