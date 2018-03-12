import sqlite3
import sys
import os
import xml.dom.minidom

class DataInit ():

    def __init__( self ):
        pass

    def print_databases( self ):
        conn = sqlite3.connect('battledb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scoreboard")
        for a in cursor.fetchall():
            print a

        conn.close()

    def create_dbs(self):
        conn = sqlite3.connect('battle.db')
        c = conn.cursor()
        c.execute("CREATE TABLE scoreboard (pname text, pwin real, plost real, totgame real, win_rate real, ranking real)")
      
        conn.commit()
        conn.close()
