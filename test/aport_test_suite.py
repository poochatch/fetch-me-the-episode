#! /usr/bin/env python

# aport.app test suite

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) ) 
        from app.aport_app import FileManagement, FetchInfo, FetchTorrent
    else:
        from  ..app.aport_app import FileManagement, FetchInfo, FetchTorrent 


class TestFileManagement(object):
    pass
    
class TestFetchInfo(object):
    pass
    
class TestFetchTorrent(object):
    pass

