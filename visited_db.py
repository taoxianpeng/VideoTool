import sqlite3
import logging

class VisitedDB():
    def __init__(self,):
        self.conn = sqlite3.connect('visitedDB.db')
        self.cur = self.conn.cursor()
    
    def addItem(self, time, ip):
        str = r'INSERT INTO visited(time,ip) VALUES ("{}","{}")'.format(time, ip)
        try:
            self.cur.execute(str)
            self.conn.commit()
        except Exception as f:
            logging.error(f)
        finally:
            self.conn.close()

if __name__ == "__main__":
    visited = VisitedDB()
    visited.addItem('2021-02-19 00:30:11','36.99.136.139')