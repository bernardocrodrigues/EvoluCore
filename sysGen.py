import os, subprocess, shutil
from multiprocessing import Process, Queue
import time


class Generator(Process):

    def __init__(self, rootDir, toCompile, prefix, referenceDir):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__toCompile = toCompile
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir

    def _setupFolder(self):
        try:
            if os.path.isdir(self.__workingDir):
                shutil.rmtree(self.__workingDir)
                os.makedirs(self.__workingDir)
            else:
                os.makedirs(self.__workingDir)
        except OSError:
            print('Erro no setup das pastas')
            exit(1)

    def _populateQsys(self):

        # code = subprocess.run(["qsys-generate", "--synthesis=VHDL", self.__rootDir + '/qsys/'+self.__prefix+self.__current+'.qsys', "--output-directory="+self.__rootDir +'/'+self.__current])
        code = subprocess.run(["qsys-generate --synthesis=VHDL "+ self.__rootDir + '/qsys/' + self.__prefix + self.__current + ".qsys --output-directory=" + self.__rootDir + '/' + self.__current], shell=True)
        if code.returncode != 0:
            print('Erro na compilação do Qsys')
            exit()

    def _compileQuartus(self):

        code = subprocess.run(["cp", "-a", self.__referenceDir+"quartus/.", self.__workingDir])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        # code = subprocess.run(["quartus_sh", "--flow", "compile", self.workingDir+"base.qpf"])
        # if code.returncode != 0:
        #     print('Erro na compilação do quartus')
        #     exit()

    def run(self):

        self.__pid = os.getpid()

        while True:
            try:
                self.__current = str(self.__toCompile.get_nowait())
            except Exception:
                exit(0)
            else:
                print(str(self.__pid) + " " +self.__current)
                self.__workingDir = self.__rootDir +'/'+self.__current+'/'
                self._setupFolder()
                self._populateQsys()





            # self._setupFolder()
            # self._populateQsys()
            # self._compileQuartus()




if __name__ == '__main__':

    target = "/home/bcrodrigues/tcc/"
    base = "/home/bcrodrigues/Dropbox/tcc/script/base/"
    toCompile = Queue()
    prefix = 'q'

    for x in range(1, 11):
        toCompile.put(x)



    start = time.time()

    gen = Generator(target, toCompile, prefix, base)
    gen2 = Generator(target, toCompile, prefix, base)
    gen3 = Generator(target, toCompile, prefix, base)
    gen4 = Generator(target, toCompile, prefix, base)
    gen5 = Generator(target, toCompile, prefix, base)
    gen6 = Generator(target, toCompile, prefix, base)
    gen7 = Generator(target, toCompile, prefix, base)
    gen8 = Generator(target, toCompile, prefix, base)
  
    gen.start()  
    gen2.start()
    gen3.start()
    gen4.start()
    gen5.start()
    gen6.start()
    gen7.start()
    gen8.start()

    gen.join()
    gen2.join()
    gen3.join()
    gen4.join()
    gen5.join()
    gen6.join()
    gen7.join()
    gen8.join()

    end = time.time()
    print(end - start)

    # gen = Generator(target, 'systemBench', base)
    # gen2 = Generator(target, 'systemBench2', base)
    # gen3 = Generator(target, 'systemBench3', base)
    # gen4 = Generator(target, 'systemBench4', base)
    #
    #
    # # gen._setupFolder()
    # # gen._populateQsys()
    # # # gen2._compileQuartus()
    # #
    # # gen2._setupFolder()
    # # gen2._populateQsys()
    # #
    # # p = Process(target=gen._compileQuartus,  args=('RODANDO 1',))
    # # p2 = Process(target=gen2._compileQuartus, args=('RODANDO 2',))
    #
    # gen.start()
    # gen2.start()
    # gen3.start()
    # gen4.start()
    #
    # gen.join()
    # gen2.join()
    # gen3.join()
    # gen4.join()

