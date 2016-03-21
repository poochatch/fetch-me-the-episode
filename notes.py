#! /usr/bin/python

# dwonload latest episode of your favourite tv series!

import requests, os, bs4

torrent = 'http://www.torrenthound.com/torrent/391781cab16df66db537f601b6330d0656c61a68'
url = 'http://next-episode.net/vikings'

headers = {'User-Agent':'Mozzilla/5.0'}
res = requests.get(url,headers=headers,verify=False)

file = open('vikings.torrent', 'wb')
soup = bs4.BeautifulSoup(res.text)
episode = soup.select('div #previous_episode')
for x in episode: print x.getText()
#episode_name = episode[1].getText()
#episode_nr = int(episode[2].getText())

#print episode_name[5:], episode_nr[-2:]

torr = requests.get(torrent)

from subprocess import call


#for chunk in torr.iter_content(10**5):
#    file.write(chunk)

file.close()

#all(['ktorrent','vikings.torrent'])
