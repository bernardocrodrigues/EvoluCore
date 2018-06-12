import os, subprocess, shutil
from multiprocessing import Process


class Generator(Process):

    def __init__(self, workingDir, DirName, referenceDir):
        Process.__init__(self)
        self.workingDir = workingDir + '/'+ DirName+'/'
        self.referenceDir = referenceDir

    def _setupFolder(self):
        try:
            if os.path.isdir(self.workingDir):
                shutil.rmtree(self.workingDir)
                os.makedirs(self.workingDir)
            else:
                os.makedirs(self.workingDir)
        except OSError:
            print('Erro no setup das pastas')
            exit(1)
    def _populateQsys(self):

        shutil.copy2(self.referenceDir + '/qsys/base.qsys', self.workingDir)
        code = subprocess.run(["qsys-generate", "--synthesis=VHDL", self.workingDir + "base.qsys"])
        if code.returncode != 0:
            print('Erro na compilação do Qsys')
            exit()
    def _compileQuartus(self):

        code = subprocess.run(["cp", "-a", self.referenceDir+"quartus/.", self.workingDir])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        code = subprocess.run(["quartus_sh", "--flow", "compile", self.workingDir+"base.qpf"])
        if code.returncode != 0:
            print('Erro na compilação do quartus')
            exit()

    def run(self):

        self._setupFolder()
        self._populateQsys()
        self._compileQuartus()








if __name__ == '__main__':

    target = "/home/bcrodrigues/tcc/"
    base = "/home/bcrodrigues/Dropbox/tcc/script/base/"

    gen = Generator(target, 'systemBench', base)
    gen2 = Generator(target, 'systemBench2', base)
    gen3 = Generator(target, 'systemBench3', base)
    gen4 = Generator(target, 'systemBench4', base)


    # gen._setupFolder()
    # gen._populateQsys()
    # # gen2._compileQuartus()
    #
    # gen2._setupFolder()
    # gen2._populateQsys()
    #
    # p = Process(target=gen._compileQuartus,  args=('RODANDO 1',))
    # p2 = Process(target=gen2._compileQuartus, args=('RODANDO 2',))

    gen.start()
    gen2.start()
    gen3.start()
    gen4.start()

    gen.join()
    gen2.join()
    gen3.join()
    gen4.join()

