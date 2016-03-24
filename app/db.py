from sqlalchemy import Column, Integer, String, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import os, sys

#session = Session()

db_path = os.path.abspath(os.path.dirname(__file__)) + '/shows.db'  
engine = create_engine('sqlite:///%s' %(db_path), echo=True) 
Base = declarative_base(engine)
class Shows(Base):
    __tablename__ = 'shows'
    __table_args__ = {'autoload':True}
    id = Column(Integer, Sequence('show_id_seq'), primary_key=True)
    title = Column(String(60))
    url = Column(String(60))

    def __repr__(self):
        return "<Show(title='%s', url='%s'>" %(self.title, self.url)


class DownloadedEpisodes(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    episode_nr = Column(Integer)
    season_nr = Column(Integer)
    episode = Column(String)
    date_of_download = Column(String)
    torrent_client = Column(String)
    path = Column(String)
    file_name = Column(String)
    torrent_url = Column(String)
    show_id = Column(Integer, ForeignKey('shows.id'))
    show = relationship("Shows", back_populates='downloaded_episodes')

    def __repr__(self):
        return "<Episode(episode='%s', date_of_download='%s', torrent_client='%s', path='%s%s', torrent_url='%s')>"\
                %(self.episode, self.date_of_download, self.torrent_client, \
                self.path, self.file_name, self.torrent_url)


Shows.downloaded_episodes = relationship("DownloadedEpisodes", \
                            order_by=DownloadedEpisodes.id, \
                            back_populates="show")



class HandleDataBase(object):
    def __init__(self):
        metadata = Base.metadata
        Session = sessionmaker(bind=engine)
        #Base.metadata.create_all(engine)
        self.session = Session()
                

    
if __name__ == "__main__":
    a = HandleDataBase()
    b = a.session.query(Shows).all()
    print b[0].title


#last_episode = Column(String(60)) # eg. s03e12
#last_download = Column(String(60)) # eg. s03e11
#last_download_date = Column(String(60)) # 12 mar 2016
#torrent_client = Column(String(60))
#file_name = Column(String(60))


#vikings = Shows(title='The Vikings', url='/vikings')
#session.add(vikings) # vikings User object hasn`t been added to db yet
#show = session.query(Shows).filter_by(title='The Vikings').first() # session flushed object into db and returned data

#print vikings
#print vikings == show # evaluates True

#session.add_all([
#    Shows(title='The Walking Dead', url='/the-walking-dead'),
#    Shows(title='Better Call Saul', url='/better-call-saul') 
#                ])

#vikings.last_episode = 's04e14'

#print session.dirty # prints modified objects
#print session.new # prints pending objects

#session.commit() # Session emits 'UPDATE' SQL statement upon 'The Vikings' and two 'INSTERT' for TWD and BCS

## Rolling back changes
#vikings.title = 'The Simpsons' # the change is in transient state (not in session and not in db)
#session.query(Shows).filter_by(title='The Vikings').first() # the change moves from pending (in session not in db) to persistent (present in session and has a record in db) state 
#session.rollback() # change is detached

#print '\n'
#for instance in session.query(Shows).order_by('id'):
#    print instance.title, instance.url

#print '\n'
#for title, url in session.query(Shows.title, Shows.url):
#    print title, url

#print '\n'
#for row in session.query(Shows, Shows.title).all():
#    print row.Shows, row.title

#print '\n'
#for row in session.query(Shows.title.label('title_label')).all():
#    print row.title_label

#print '\n'
#from sqlalchemy.orm import aliased
#show_alias = aliased(Shows, name='show_alias')
#for row in session.query(show_alias, show_alias.title).all():
#    print row.show_alias

#print '\n'
#for u in session.query(Shows).order_by(Shows.id)[1:3]:
#    print u

#print '\n'
#for title, in session.query(Shows.title).filter_by(url='/vikings'):
#    print title

#print '\n'
#for title, in session.query(Shows.title).filter(Shows.url=='/vikings'):
#    print title

#print '\n'
#for show in session.query(Shows).filter(Shows.title=='The Vikings').filter(Shows.url=='/vikings'):
#    print show


## Common Filter Operators
#session.query(Shows).filter(Shows.title == 'The Vikings') # EQUALS
#session.query(Shows).filter(Shows.title != 'The Vikings') # NOT EQUALS
#session.query(Shows).filter(Shows.title.like('%The Vikings%')) # LIKE
#session.query(Shows).filter(Shows.title.in_(['The Vikings', 'How I Met Your Mother', 'The Wire'])) # IN

## works with query objects too:
#session.query(Shows).filter(Shows.title.in_(session.query(Shows.title.like('%vikings%'))))

#session.query(Shows).filter(~Shows.title.in_(['The Vikings', 'How I Met Your Mother', 'The Wire'])) # NOT IN
#session.query(Shows).filter(Shows.title != None) # IS NOT NULL

#from sqlalchemy import and_, or_
#session.query(Shows).filter(and_(Shows.title == 'The Walking Dead', Shows.url == '/the-walking-dead')) # AND
## different syntex for AND query:
#session.query(Shows).filter(Shows.title == 'The Vikings', Shows.url == '/vikings')

#session.query(Shows).filter(or_(Shows.title == 'Better Call Saul', Shows.url == '/better-call-saul')) # OR 
#session.query(Shows).filter(Shows.title.match('The Vikings')) # MATCH




