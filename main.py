from sqlalchemy import Column, Integer, String, Sequence, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, sys, requests, bs4, pyperclip, re, time
from datetime import datetime

URL = 'http://next-episode.net'
db_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/dhistory.db'  
engine = create_engine('sqlite:///%s' %(db_path), echo=False) 
Base = declarative_base(engine)

class Episode(Base):
    __tablename__ = 'dhistory'
    #__table_args__ = {'autoload':True}
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    date = Column(String(30))
    show_title = Column(String(100))
    ep_nr = Column(Integer)
    se_nr = Column(Integer)
    e_title = Column(String(100))
    torrent_client = Column(String(100))
    path = Column(String(100))
    url = Column(String(100))
    
    def __repr__(self):
        return '< [EPISODE]: date="%s", show_title="%s", se_nr="%s", \
ep_nr="%s", e_title="%s", torrent_client="%s"\
path="%s", url="%s" >' %( self.date, self.show_title, self.se_nr,
                        self.ep_nr, self.e_title, self.torrent_client,
                        self.path, self.url)

class HandleDataBase(object):
    def __init__(self):
        metadata = Base.metadata
        #dhistory = Table('dhistory',metadata, autoload=True)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        self.session = Session()

    def get_all_episodes(self, show_title):
        return  self.session.query(Episode).filter(Episode.show_title == show_title).all()
            

    def write_episode(self, single=True, **kwargs):
        self.session.add(Episode(**kwargs)) 
        if single:
            self.session.commit()
        
    def write_episodes(self, episodes):
        for episode in episodes:
            self.write_episode(single=False, **episode)
        self.session.commit()

    def clear_database(self):
        pass

    def delete_episode(self):
        pass

    def close_session(self):
        pass

def now():
    format = '%Y.%m.%d %H:%M:%S'
    return datetime.now().strftime(format)

def fetch_episode(title):
    pass

def fetch_show(url):
    print 'Fetching show info at %s%s' %(URL, url)
    full_url = URL + url
    soup = bs4.BeautifulSoup(requests.get(full_url).text)
    return soup

def parse_season(title, season_nr, url):
    print '     Parsing season %i of %s at %s%s' %(season_nr, title, URL, url)
    soup = fetch_show(url)
    episode_table = soup.select('#middle_section_schedule table tr td')
    epi_list = [field.getText() for field in episode_table]
    episodes = []
    for x in range(3,len(epi_list),3):
        print '             Parsing %s s%ie%s titled %s' %(title, season_nr, epi_list[x], epi_list[x+2])
        episode = { 'date':     now(),
                'show_title':   title,
                'se_nr':        season_nr,
                'ep_nr':        int(epi_list[x]) if epi_list[x] != 'Special' else 0 ,
                'e_title':      epi_list[x+2],
                'torrent_client':None,
                'path':         None,    
                'url':          None}
        episodes.append(episode)
    return episodes

def parse_show(title, url):
    print 'Parsing show %s at %s%s' %(title, URL, url)
    soup = fetch_show(url)
    seasons_table = soup.select('#middle_section_schedule')
    seasons_info = re.findall('Season \d+', seasons_table[0].getText())
    seasons = []
    for season_nr in range(len(seasons_info)):
        season = parse_season(title, season_nr+1, url +  '/season-%i' %(season_nr+1))
        seasons.append(season)
    return seasons
            
if __name__ == "__main__":
    d_base = HandleDataBase()


def get_top_watched_shows():
    print 'I will update database. This may take a while.'
    time.sleep (2)
    top_shows_list = bs4.BeautifulSoup(requests.get(URL).text).select('#watchliststring > a')
    top_shows = []
    for show in top_shows_list:
        title = show.getText()
        url = show['href']
        top_shows.append(parse_show(title, url))
    for show in top_shows:
        for season in show:
            d_base.write_episodes(season)        

    PATH = os.path.abspath(os.path.dirname(__file__))
    TORRENT_PATH = PATH + '/torrents/'


next_e = False      # last watched episode
latest_e = False    # lately released episode
default = 0 if next_e == latest_e else 2    
options = [ 'latest',
            'next',
            'first',
            'from last to latest',
            'all',
            'none']

    
