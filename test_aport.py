#! /usr/bin/env python


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) ) 
        from db import HandleDataBase() , Episode

    else:
        from db import HandleDataBase() , Episode



