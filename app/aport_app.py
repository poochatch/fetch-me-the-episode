#! /usr/bin/env python
# -*- coding: utf-8 -*-


# aport.app a script to download latest episode of your favourite TV-series

import requests as re
import os, bs4
from subprocess import call

class FetchInfo():
    # Fetch season and episode of a last episode from web
    def __init__(self):
        pass

    def fetch(self, series_title):
        url = 'http://next-episode.net/' + series_title
        headers = {'User-Agent':'Mozilla/5.0'}
        respond = re.get(url, headers=headers, verify=False)
        return respond

    def parse(self, data):
        pass

    def read_last_watched(self):
        # read last downloaded episode from a file
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

class Menu():
    def __init__(self):
        pass

    def print_menu(self):
        pass

    def parse_command(self):
        pass

    def ready(self):
        # program is waiting for commands
        pass

class FileManagement():
    """ Handle files:
    torrent_history.txt - information about previously downloaded torrents
    download_history.txt - iformation about previos torrent client lauches
    aport_conf.txt - program configuration"""
    def __init__(self, file):
        pass

    def read_file_into_buffer(self, file):
        # load a file into a buffer in memory and close it
        pass

    def update_buffer(self, buffer):
        pass 

    def save_buffer(self, file):
        # flush buffer into a file
        pass

