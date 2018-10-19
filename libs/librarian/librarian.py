
import sqlite3
import numpy as np


class librarian_milenium(object):



    def __init__(self):

        self.__conn = sqlite3.connect('/home/bcrodrigues/Dropbox/tcc/script/millenium.db', isolation_level='EXCLUSIVE')
        # self.__conn = sqlite3.connect('/home/bcrodrigues/Dropbox/tcc/script/nsga.db')

    def get_data(self, limit = None) -> np.array:

        cur = self.__conn.cursor()
        if limit != None:
            return np.array(cur.execute("select id_core, adpcm, alm from core").fetchmany(limit))
        else:
            return np.array(cur.execute("select id_core, adpcm, alm from core").fetchall())

    def get_benchmark_data(self, benchmark = "adpcm", metrics: list = None, limit = None) -> np.array:

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

    def get_core_characteristics(self, id_core: int):
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

    def get(self, limit = None):
        cur = self.__conn.cursor()
#TODO: POR RAM, memory DE VOLTA NA BUSCA
        query = '''select 
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
                         setting_branchpredictiontype,
                         adpcm, 
                         alm,
                         memory
                    from core'''
        if limit != None:
            aux = np.array(cur.execute(query).fetchmany(limit))
            return aux[:, :12], aux[:, 12:].astype(float)
        else:
            aux = np.array(cur.execute(query).fetchall())
            return aux[:, :12], aux[:, 12:].astype(float)

class librarian_nsga(object):

    def __init__(self):
        self.__conn = sqlite3.connect('/home/bcrodrigues/Dropbox/tcc/script/nsga.db')

    def init(self):
        self.__conn.executescript("""

                        DROP TABLE IF EXISTS experimento;
                        DROP TABLE IF EXISTS core;
                        
                        create table experimento(
                                                id_experimento INTEGER PRIMARY KEY,
                                                size INTEGER,
                                                cross_over_ratio INTEGER,
                                                num_traits INTEGER,
                                                num_objectives INTEGER,
                                                num_generations INTEGER,
                                                benchmark TEXT
                                                );

                        create table core(
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
                                            benchmark INTEGER DEFAULT 0,
                                            alm INTEGER  DEFAULT 0,
                                            memory INTEGER  DEFAULT 0,
                                            ram INTEGER DEFAULT 0,
                                            id_experimento INTEGER,
                                            geracao INTERGER,
                                            filho INTEGER,
                                            FOREIGN KEY(id_experimento) REFERENCES experimento(id_experimento)
                                         );

                        """)

    def insert_population(self, traits: np.array, objectives: np.array):
        pass

    def create_experimento(self, id_experimento, size, cross_over_ratio, num_traits, num_objectives, num_generations, benchmark):
        cur = self.__conn.cursor()
        cur.execute("PRAGMA foreign_keys = 1")

        cur.execute("insert into experimento("
                    "id_experimento, "
                    "size, "
                    "cross_over_ratio, "
                    "num_traits, "
                    "num_objectives, "
                    "num_generations,"
                    "benchmark) "
                    "values (?,?,?,?,?,?,?)",
                    (id_experimento, size, cross_over_ratio, num_traits, num_objectives, num_generations, benchmark))
        self.__conn.commit()

    def insert_generation(self, id_experimento, generation, children, traits, objectives):

        cur = self.__conn.cursor()

        cur.execute("PRAGMA foreign_keys = 1")

        for trait, objective in zip(traits, objectives):

            try:
                aux = trait + objective
            except TypeError:
                aux = np.hstack((trait, objective))

            zeros = 4 - len(objective)

            try:
                aux += zeros * (0,)
            except TypeError:
                aux = np.hstack((aux, zeros * (0,)))

            try:
                aux += (id_experimento, generation, children)
            except TypeError:
                aux = np.hstack((aux, (id_experimento, generation, children)))

            print(len(aux))
            cur.execute('''insert into core(
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
                                                setting_branchpredictiontype,
                                                benchmark,
                                                alm,
                                                memory,
                                                ram,
                                                id_experimento,
                                                geracao,
                                                filho) 
                                                values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', aux)

        self.__conn.commit()

    def insert_children(self, id_experimento, generation, traits):

        cur = self.__conn.cursor()

        cur.execute("PRAGMA foreign_keys = 1")

        for trait in traits:

            zeros = 4
            aux = trait

            try:
                aux += zeros * (0,)
            except TypeError:
                aux = np.hstack((aux, zeros * (0,)))

            try:
                aux += (id_experimento, generation, 0)
            except TypeError:
                aux = np.hstack((aux, (id_experimento, generation, 1)))

            cur.execute('''insert into core(
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
                                                setting_branchpredictiontype,
                                                benchmark,
                                                alm,
                                                memory,
                                                ram,
                                                id_experimento,
                                                geracao,
                                                filho) 
                                                values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', aux)

        self.__conn.commit()

    def get_generation(self, id_experiment, generation):

        cur = self.__conn.cursor()
        cur.execute("PRAGMA foreign_keys = 1")
        result = cur.execute("select * from core where id_experimento=? and geracao=?", (id_experiment, generation)).fetchall()
        return result

    def get_experiment_meta(self, id_experiment):

        cur = self.__conn.cursor()
        cur.execute("PRAGMA foreign_keys = 1")
        result = cur.execute("select * from experimento where id_experimento=?", (id_experiment,)).fetchone()
        return result

    def get_experiment_data(self, id_experiment):
        meta = self.get_experiment_meta(id_experiment)
        num_gen =  meta[5]

        generations = []

        for gen in range(num_gen):
            generation = self.get_generation(id_experiment, gen)
            generations.append(generation)


        return generations

    def get_last_population(self, id_experiment, objective_num):

        cur = self.__conn.cursor()
        cur.execute("PRAGMA foreign_keys = 1")
        last_generation = cur.execute("select max(geracao) from core where id_experimento =? and filho=0", (id_experiment,)).fetchone()[0]

        data = np.array(self.get_generation(id_experiment, last_generation))

        traits = data[:,:12]
        objectives = data[:,12:12+objective_num].astype(float)

        return last_generation, traits, objectives





if __name__ == "__main__":

    lib = librarian_nsga()

    # lib_old = librarian_milenium()
    # traits, objectives = lib_old.get(10)
    # lib.init()

    print(lib.get_last_population(5,2))


    # size = 10
    # cross_over_ratio = 0.9
    # num_traits = 12
    # num_objectives = 2
    # num_generations = 10
    # experimento = 10
    # benchmark = "adpcm"

    # lib.create_experimento(experimento, size, cross_over_ratio, num_traits, num_objectives, num_generations, benchmark)
    # lib.insert_generation(experimento, 0, traits, objectives)
    # lib.insert_children(experimento, 0, traits)

    # print(traits,objectives)



    # print(lib.get_benchmark_data(limit=5, metrics=["alm, memory"]))
    # print(lib.get_core_characteristics(10))

    # print(lib.get(10))
