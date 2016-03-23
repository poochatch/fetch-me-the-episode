#! /usr/bin/env/python

from app.fetchinfo import FetchInfo
from app.fetchtorrent import FetchTorrent
from app.aport_conf import *
import sys, os, pyperclip

arguments = sys.argv

info = FetchInfo()
torrent = FetchTorrent()

PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
TORRENT_PATH = PATH + '/torrents/'

print PATH + TORRENT_PATH
print download_path

top = info.get_top_watched()

for title in range(len(top)):
    print title,top[title][0]

nr = int(raw_input( 'Please enter show number: '))
print info.parse(info.fetch(top[nr][1]))


