
import sqlite3
import numpy as np


class librarian(object):

    def __init__(self):
        self.__conn = sqlite3.connect('/home/bcrodrigues/Dropbox/tcc/script/millenium.db', isolation_level='EXCLUSIVE')

    def get_data(self, limit = None):

        cur = self.__conn.cursor()
        if limit != None:
            return np.array(cur.execute("select id_core, adpcm, alm from core").fetchmany(limit))
        else:
            return np.array(cur.execute("select id_core, adpcm, alm from core").fetchall())





if __name__ == "__main__":

    lib = librarian()
    print(lib.get_data())


