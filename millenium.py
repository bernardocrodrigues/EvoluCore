
import sqlite3
conn = sqlite3.connect('millenium.db')
import random
from pprint import pprint

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

def init():
    conn.executescript("""

                    DROP TABLE IF EXISTS core;
                    
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
                                            setting_branchpredictiontype TEXT
                                     );
                    
                    """)

def insert_core(core:dict):
    cur = conn.cursor()
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
    conn.commit()

def get_random_core():
    core ={}
    for param in discreteParams:
        core[list(param.keys())[0]] = random.choice(list(param.values())[0])
    return core

def get_random_core_as_tupple():
    core = ()
    for param in discreteParams:
        core += (random.choice(list(param.values())[0]),)
    return core

def validate_core(core:dict):

    if core['mul_64_impl'] == '1' and (core['mul_32_impl'] == '1' or core['mul_32_impl'] == '0'):
        return False

    return True

def core_already_there(core:dict):
    cur = conn.cursor()
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


init()

inserted = 0

while inserted < 1000:
    core = get_random_core()
    if validate_core(core):
        if not core_already_there(core):
            insert_core(core)
            inserted += 1


