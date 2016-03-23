#! /usr/bin/env python
# -*- coding: utf-8 -*-


# aport.app a script to download latest episode of your favourite TV-series

import requests as req
import os, bs4, re, pyperclip, sys, time
from subprocess import call
from configuration.aport_conf import *
from configuration.utils import Singleton

PATH = os.path.abspath(os.path.dirname(__file__))
BUFFER_DICT = { 'date'          :   0,
                'series_name'   :   1,
                'title'         :   1,
                'season,episode':   2,
                'episode_info'  :   2,
                'path'          :   3,
                'torrent_client':   3,
                'url'           :   4,
                'file_name'     :   5
}



class FetchInfo():
    # Fetch season and episode of a last episode from web
    def __init__(self):
        self.data_seed = data_seeds[data_seed_current] 

    def resolve_url(self, series_title):
        # find correct series_url for a gives tv-series
        pass

    def fetch(self, series_url):
        # return requests.models.Response object
        url = self.data_seed + series_url
        headers = {'User-Agent':'Mozilla/5.0'}
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
        season = txt[s_span[0]:s_span[1]][2:]
        episode = txt[e_span[0]:e_span[1]][2:]
        return 's%se%s' %(season,episode)

    def episode_int_to_string(self, season, episode):
        s_str, e_str = str(season),str(episode)
        return 's%se%s' %(s_str,e_str)
        

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


class FetchTorrent():
    # fetch torrent file
    def __init__(self):
        pass        

    def fetch_torrent_data(self):
        pass

    def check_data(self):
        pass

    def download_torrent(self):
        # save torrent file into torrents/
        pass
    
    def call_torrent_client(self):
        # client configuration in .aportrc
        pass

    def update_history(self):
        # flush history buffer into torrent.history file
        pass

    def update_history_buffer(self):
        # update torrent.history buffer
        pass


class FileManagement():
    """ Handle files:
    torrent_history.txt - information about previously downloaded torrents
    download_history.txt - iformation about previos torrent client lauches
    series_table.txt - information about correct series urls
    
    there is only one instance of this class (Singleton),
    holding data about every file it handled. """

    def __init__(self, file_name):
        self.file_name = file_name
        self.load_file_into_buffer(file_name)

    def load_file_into_buffer(self, file_name):
        # load a file into a buffer in memory and close it
        self.file = open(PATH + '/configuration/' + file_name, 'r')
        self.parse_file(self.file)

    def parse_file(self,file):
        # parse *txt file into python data representation
        self.buffer = []
        lines = file.readlines()
        comments = []
        for _line in range(len(lines)):
            temp = []
            if lines[_line].startswith('#'):
                comments.append(lines[_line].split(' '))
            else:
                temp = lines[_line].split(',')
                if self.is_correct(temp, _line):
                    self.buffer.append(temp)
        self.file.close()
        self.save_buffer(comments)

    def is_correct(self, data, line_nr):
        lenghts = { 'download_history.txt': len(data)!=6,
                    'torrent_history.txt':  len(data)!=3,
                    'series_table.txt':     len(data)< 3     }
        if lenghts[self.file_name]:
            self.error_log(line_nr, data, 'Wrong entry lenght')
            return False
        for field in data:
            if field.startswith(('#',' ','\n', '\t', '\r')) or len(field)==0:
                self.error_log(line_nr, data, 'Invalid entry')
                return False
        return True
            
    def error_log(self, line_nr, data, err_descr):
        log = open(PATH + '/configuration/error_log.txt', 'a')
        error = ' '.join([time.strftime("%H:%M:%S %d %b %Y"),
                        err_descr,
                        'in line',
                        str(line_nr), 
                        'of',
                        self.file_name + ':' + '\t',
                        ','.join(data)])
        log.write(error)
        log.close()

    def update_buffer(self, data):
        if self.is_correct(data,'NEW_ENTRY'):
            self.buffer.append(','.join(data))

    def save_buffer(self, comments):
        # flush buffer into a file
        file = open(PATH + '/configuration/' + self.file_name, 'w')
        for line in comments:
            entry = ' '.join(line)
            file.write(entry)
        file.write('\n')
        for line in self.buffer:
            entry = ','.join(line)
            file.write(entry)
        file.close()


download_history = FileManagement('download_history.txt')
torrent_history = FileManagement('torrent_history.txt')
series_table = FileManagement('series_table.txt')
buffer_dict =   {   'download_history': download_history,
                        'torrent_history':  torrent_history, 
                        'series_table':     series_table
                    }

