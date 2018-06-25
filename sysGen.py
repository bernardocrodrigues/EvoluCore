import os, subprocess, shutil
from multiprocessing import Process, Queue
import time
from functools import reduce


class Generator(Process):

    def __init__(self, rootDir, toCompile, prefix, referenceDir, ):

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

    def _fixTopDesignName(self):

        with open(self.__workingDir + 'base.qsf', 'r') as f:
            lines = f.readlines()

        for x, line in enumerate(lines):
            if 'TOP_LEVEL_ENTITY' in line:
                lines[x] = 'set_global_assignment -name TOP_LEVEL_ENTITY '+self.__prefix+self.__current+'\n'
            if 'QIP_FILE' in line:
                lines[x] = 'set_global_assignment -name QIP_FILE synthesis/'+self.__prefix+self.__current+'.qip\n'

        with open(self.__workingDir + 'base.qsf', 'w') as f:
            for line in lines:
                f.write(line)

    def _compileQuartus(self):

        code = subprocess.run(["cp", "-a", self.__referenceDir+"quartus/.", self.__workingDir])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        self._fixTopDesignName()

        code = subprocess.run(["quartus_sh", "--flow", "compile", self.__workingDir+"base.qpf"])
        if code.returncode != 0:
            print('Erro na compilação do quartus')
            exit()

    def _compileSoftware(self, code):

        os.makedirs(self.__workingDir+'/software')

        code = subprocess.run(["nios2-bsp", "hal", self.__workingDir+'/software/bsp', self.__rootDir + '/qsys/' + self.__prefix + self.__current+'.sopcinfo', "--script=" + self.__referenceDir+ "/bsp/parameters.tcl"])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        code = subprocess.run(["nios2-app-generate-makefile", "--bsp-dir="+self.__workingDir+'/software/bsp', "--src-rdir="+self.__referenceDir +"software/"+code+"/", "--app-dir=" + self.__workingDir+'/software/', "--elf-name", "code.elf"])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        code = subprocess.run(["make", "-C", self.__workingDir+'/software/'])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

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
                # self._setupFolder()
                # self._populateQsys()
                # self._compileQuartus()
                # self._compileSoftware('checksum')

class TestBench(Process):

    def __init__(self, rootDir, toBenchmark, prefix, referenceDir, cable, result):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir
        self.__toBenchmark = toBenchmark
        self.__cable = cable

        self.__result = result

    def _configureBoard(self):

        success = False
        while not success:
            # p = subprocess.Popen(["quartus_pgm","-c", str(board), "-z", "--mode=JTAG", "--operation=\"p;"+self.__workingDir +"\""], stdout=subprocess.PIPE, preexec_fn=os.setsid)
            p = subprocess.Popen("quartus_pgm -c "+str(self.__cable) + " -z --mode=JTAG --operation=\"p;" + self.__workingDir +"output_files/base_time_limited.sof@2\"",stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)

            for line in iter(p.stdout.readline, b''):
                string = line.decode("utf-8")
                if "Configuration succeeded" in string:
                    success = True
                    subprocess.run(["kill", str(p.pid)])
                    break
                if "Operation failed" in string:
                    subprocess.run(["kill", str(p.pid)])
                    subprocess.run(["killall", "jtagd"])
                    break

    def _transferCode(self):

        confiredProperly = False
        while not confiredProperly:
            returnCode = -1
            retry = -1

            while returnCode != 0:
                code = subprocess.run(["nios2-download", "-c", str(self.__cable), "-r", "-g", self.__workingDir + "/software/code.elf"])
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"])
                returnCode = code.returncode
                retry += 1
                if retry > 5:
                    break

            if returnCode != 0:
                subprocess.run(["killall", "jtagd"])
                self._configureBoard(1)
            else:
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"])
                confiredProperly = True

    def _benchmark(self):

        while True:
            p = subprocess.Popen('nios2-terminal -c '+str(self.__cable)+' -o 60', stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)

            result = []
            for x in range(8):
                for line in iter(p.stdout.readline, b''):
                    string = line.decode("utf-8")
                    try:
                        result.append(int(string))
                    except:
                        pass
                    else:
                        break

            # print("Resultado desse Hardware: ", result)
            try:
                result = reduce(lambda x, y: x + y, result) / len(result)
            except:
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"])
                subprocess.run(["kill", str(p.pid)])
                pass
            else:
                subprocess.run(["kill", str(p.pid)])
                return result

    def run(self):

        self.__pid = os.getpid()

        while True:
            # print(self.__RUNNING)
            try:
                self.__current = str(self.__toBenchmark.get_nowait())
            except Exception:
                time.sleep(1)
            else:
                print(str(self.__pid) + " " +self.__current)
                self.__workingDir = self.__rootDir +'/'+self.__current+'/'
                self._configureBoard()
                self._transferCode()
                self.__result.put(self._benchmark())

if __name__ == '__main__':

    target = "/home/bcrodrigues/tcc/"
    base = "/home/bcrodrigues/Dropbox/tcc/script/base/"
    toCompile = Queue()
    toBenchmark = Queue()
    result = Queue()
    prefix = 'q'

    gen = TestBench(target, toBenchmark, prefix, base, 1, result)
    gen.start()

    results = []

    for x in range(1, 2):
        toBenchmark.put(x)


    while len(results) < 1:
        try:
            results.append(result.get_nowait())
        except Exception:
            time.sleep(1)

    gen.terminate()
    gen.join()

    print(results)








    # for x in range(1, 2):
    #     toCompile.put(x)
    #
    # start = time.time()
    #
    # gen = Generator(target, toCompile, prefix, base)
    # gen2 = Generator(target, toCompile, prefix, base)
    # gen3 = Generator(target, toCompile, prefix, base)
    # gen4 = Generator(target, toCompile, prefix, base)
    # gen5 = Generator(target, toCompile, prefix, base)
    #
    #
    # gen.start()
    # gen2.start()
    # gen3.start()
    # gen4.start()
    # gen5.start()
    #
    # gen.join()
    # gen2.join()
    # gen3.join()
    # gen4.join()
    # gen5.join()


    # end = time.time()
    # print(end - start)

