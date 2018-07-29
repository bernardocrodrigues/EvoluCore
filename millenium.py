
import sqlite3

import random
from pprint import pprint
import time
from multiprocessing import Process
import os
import random


class db(object):

    discreteParams = [
                        {'dcache_bursts': ['true', 'false']},
                        {'dcache_victim_buf_impl': ['reg', 'ram']},
                        {'icache_burstType': ['Sequential', 'None']},
                        {'setting_support31bitdcachebypass': ['true', 'false']},
                        {'dividerType': ['no_div', 'srt2']},
                        {'mul_32_impl': ['0', '1', '2', '3']},
                        {'shift_rot_impl': ['1', '0']},
                        {'mul_64_impl': ['1', '0']},
                        {'setting_bhtPtrSz': ['8', '12', '13']},
                        {'setting_branchpredictiontype': ['Dynamic', 'Static']},
                        {'icache_size': [
                                        '0',
                                        '1024',
                                        '2048',
                                        '4096',
                                        '8192'
                        ]},
                        {'dcache_size': [
                                        '0',
                                        '1024',
                                        '2048',
                                        '4096',
                                        '8192'
                        ]}
                    ]

    def __init__(self):
        self.__conn = sqlite3.connect('millenium.db', isolation_level='EXCLUSIVE')

    def init(self):
        self.__conn.executescript("""
    
                        DROP TABLE IF EXISTS core;
                        DROP TABLE IF EXISTS benchmark;
                        
                        create table core(
                                                id_core INTEGER PRIMARY KEY,
                                                dcache_size TEXT,
                                                dcache_bursts TEXT,
                                                dcache_victim_buf_impl TEXT,
                                                icache_size TEXT,
                                                icache_burstType TEXT,
                                                setting_support31bitdcachebypass TEXT,
                                                dividerType TEXT,
                                                mul_32_impl TEXT,
                                                shift_rot_impl TEXT,
                                                mul_64_impl TEXT,
                                                setting_bhtPtrSz TEXT,
                                                setting_branchpredictiontype TEXT,
                                                adpcm INTEGER DEFAULT 0,
                                                sobel INTEGER  DEFAULT 0,
                                                vecsum INTEGER  DEFAULT 0,
                                                quicksort INTEGER  DEFAULT 0,
                                                alm INTEGER  DEFAULT 0,
                                                memory INTEGER  DEFAULT 0,
                                                ram INTEGER DEFAULT 0
                                         );
                        
                        """)

    def insert_core(self, core:dict):
        cur = self.__conn.cursor()
        cur.execute("insert into core("
                    "dcache_size, "
                    "dcache_bursts, "
                    "dcache_victim_buf_impl, "
                    "icache_size, "
                    "icache_burstType, "
                    "setting_support31bitdcachebypass, "
                    "dividerType, "
                    "mul_32_impl, "
                    "shift_rot_impl,"
                    "mul_64_impl, "
                    "setting_bhtPtrSz, "
                    "setting_branchpredictiontype) "
                    "values (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (core['dcache_size'],
                     core['dcache_bursts'],
                     core['dcache_victim_buf_impl'],
                     core['icache_size'],
                     core['icache_burstType'],
                     core['setting_support31bitdcachebypass'],
                     core['dividerType'],
                     core['mul_32_impl'],
                     core['shift_rot_impl'],
                     core['mul_64_impl'],
                     core['setting_bhtPtrSz'],
                     core['setting_branchpredictiontype']))
        self.__conn.commit()

    def get_random_core(self):
        core ={}
        for param in self.discreteParams:
            core[list(param.keys())[0]] = random.choice(list(param.values())[0])
        return core

    def get_random_core_as_tupple(self):
        core = ()
        for param in self.discreteParams:
            core += (random.choice(list(param.values())[0]),)
        return core

    def validate_core(self, core:dict):

        if core['mul_64_impl'] == '1' and (core['mul_32_impl'] == '1' or core['mul_32_impl'] == '0'):
            return False

        return True

    def core_already_there(self, core:dict):
        cur = self.__conn.cursor()
        cur.execute("select count(*) from core where "
                    "dcache_size=? and "
                    "dcache_bursts=? and "
                    "dcache_victim_buf_impl=? and "
                    "icache_size=? and "
                    "icache_burstType=? and "
                    "setting_support31bitdcachebypass=? and "
                    "dividerType=? and "
                    "mul_32_impl=? and "
                    "shift_rot_impl=? and "
                    "mul_64_impl=? and "
                    "setting_bhtPtrSz=? and "
                    "setting_branchpredictiontype=?",
                    (core['dcache_size'],
                     core['dcache_bursts'],
                     core['dcache_victim_buf_impl'],
                     core['icache_size'],
                     core['icache_burstType'],
                     core['setting_support31bitdcachebypass'],
                     core['dividerType'],
                     core['mul_32_impl'],
                     core['shift_rot_impl'],
                     core['mul_64_impl'],
                     core['setting_bhtPtrSz'],
                     core['setting_branchpredictiontype']))

        if list(cur)[0][0]:
            return True
        else:
            return False

    def get_free_core(self):
        cur = self.__conn.cursor()
        result = None
        while True:
            try:
                cur.execute("begin")
                result = cur.execute("select * from core where sobel=0 and alm=0").fetchone()
                names = [description[0] for description in cur.description]
                if result == None:
                    return None
                else:
                    cur.execute("UPDATE core SET sobel = ? ,alm = ? WHERE id_core= ? ", (-1, -1, result[0]))
                    cur.execute("end")
                    core ={}
                    for param, value in zip(names, result):
                        core[param] = value
                    return core
            except sqlite3.OperationalError:
                cur = self.__conn.cursor()
                cur.execute("end")
                time.sleep(1)



    def generate_cores(self, size):
        self.init()
        inserted = 0
        while inserted < size:
            core = self.get_random_core()
            if self.validate_core(core):
                if not self.core_already_there(core):
                    self.insert_core(core)
                    inserted += 1


def worker():

    db_ = db()
    core = db_.get_free_core()

    while core != None:
        print(os.getpid(), core)
        time.sleep(random.random()/10)
        core = db_.get_free_core()





if __name__ == "__main__":

    db_ = db()
    db_.generate_cores(100)


    p1 = Process(target=worker)
    p2 = Process(target=worker)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


    #
    # print(db_.get_free_core())
