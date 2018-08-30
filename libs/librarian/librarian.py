
import sqlite3
import numpy as np


class librarian(object):

    def __init__(self):
        self.__conn = sqlite3.connect('/home/bcrodrigues/Dropbox/tcc/script/millenium.db', isolation_level='EXCLUSIVE')

    def get_data(self, limit = None) -> np.array:

        cur = self.__conn.cursor()
        if limit != None:
            return np.array(cur.execute("select id_core, adpcm, alm from core").fetchmany(limit))
        else:
            return np.array(cur.execute("select id_core, adpcm, alm from core").fetchall())

    def get_benchmark_data(self, benchmark ="adpcm", metrics: list = None, limit = None) -> np.array:

        cur = self.__conn.cursor()
        if metrics == None:
            query = "select id_core, " + benchmark + ", alm, memory, ram from core"
            if limit != None:
                return np.array(cur.execute(query).fetchmany(limit))
            else:
                return np.array(cur.execute(query).fetchall())
        else:
            query = "select id_core, " + benchmark + ", "
            for metric in metrics:
                query += (metric + ", ")
            query = query[:-2] +" from core"
            if limit != None:
                return np.array(cur.execute(query).fetchmany(limit))
            else:
                return np.array(cur.execute(query).fetchall())

    def get_core_characteristics(self, id_core: int) -> (int, int, int):
        cur = self.__conn.cursor()
        return cur.execute('''select 
                                     dcache_size, 
                                     dcache_bursts,                                                
                                     dcache_victim_buf_impl, 
                                     icache_size, 
                                     icache_burstType, 
                                     setting_support31bitdcachebypass, 
                                     dividerType, 
                                     mul_32_impl, 
                                     shift_rot_impl, 
                                     mul_64_impl, 
                                     setting_bhtPtrSz, 
                                     setting_branchpredictiontype 
                                     from core where id_core='''+str(id_core)).fetchone()

if __name__ == "__main__":

    lib = librarian()
    print(lib.get_benchmark_data(limit=5, metrics=["alm, memory"]))

    print(lib.get_core_characteristics(10))

