import os, subprocess, shutil
from multiprocessing import Process, Queue
import time
from functools import reduce
import parse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Generator(Process):

    def __init__(self, rootDir, toCompile, prefix, referenceDir, toBenchmark):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__toCompile = toCompile
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir
        self.__toBenchmark = toBenchmark

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

        code = subprocess.run(["qsys-generate --synthesis=VHDL "+ self.__rootDir + '/qsys/' + self.__prefix + self.__current + ".qsys --output-directory=" + self.__rootDir + '/' + self.__current], shell=True)
        if code.returncode != 0:
            print('Erro na compilação do Qsys')
            raise AssertionError

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

    def _compileSoftware(self, benchmarks):

        os.makedirs(self.__workingDir+'/software')

        code = subprocess.run(["nios2-bsp", "hal", self.__workingDir+'/software/bsp', self.__rootDir + '/qsys/' + self.__prefix + self.__current+'.sopcinfo', "--script=" + self.__referenceDir+ "/bsp/parameters.tcl"])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        for benchmark in benchmarks:

            code = subprocess.run(["nios2-app-generate-makefile", "--bsp-dir="+self.__workingDir+'/software/bsp', "--src-rdir="+self.__referenceDir +"software/"+benchmark+"/", "--app-dir=" + self.__workingDir+'/software/'+benchmark+"/", "--elf-name", "code.elf"])
            if code.returncode != 0:
                print('Erro na copia dos arquivos quartus')
                exit()

            code = subprocess.run(["make", "-C", self.__workingDir+'/software/'+benchmark+'/'])
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
                self._setupFolder()
                try:
                    self._populateQsys()
                except AssertionError:
                    self.__toBenchmark.put(int(self.__current))
                else:
                    self._compileQuartus()
                    self._compileSoftware(['fractal', 'checksum'])
                    self.__toBenchmark.put(int(self.__current))

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

            p = subprocess.Popen("quartus_pgm -c "+str(self.__cable) + " -z --mode=JTAG --operation=\"p;" + self.__workingDir +"output_files/base_time_limited.sof@2\"",stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)

            for line in iter(p.stdout.readline, b''):
                string = line.decode("utf-8")
                # print(string)
                if "Configuration succeeded" in string:
                    success = True
                    subprocess.run(["kill", str(p.pid)])
                    break
                if "Operation failed" in string:
                    subprocess.run(["kill", str(p.pid)])
                    subprocess.run(["killall", "jtagd"])
                    break
                if 'does not exist or can\'t be read' in string:
                    raise FileNotFoundError

    def _transferCode(self, benchmark):

        confiredProperly = False
        while not confiredProperly:
            returnCode = -1
            retry = -1

            while returnCode != 0:
                code = subprocess.run(["nios2-download", "-c", str(self.__cable), "-r", "-g", self.__workingDir + "/software/"+benchmark+"/code.elf"])
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"])
                returnCode = code.returncode
                retry += 1
                if retry > 5:
                    break

            if returnCode != 0:
                subprocess.run(["killall", "jtagd"])
                self._configureBoard()
            else:
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"])
                confiredProperly = True

    def _benchmark(self, benchmark):

        retry = 3

        while True:

            p = subprocess.Popen('nios2-terminal -c '+str(self.__cable)+' -o 15', stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)
            aux = []
            for x in range(5):
                for line in iter(p.stdout.readline, b''):
                    string = line.decode("utf-8")
                    print(string)
                    try:
                        aux.append(int(string))
                    except:
                        pass
                    else:
                        break

            # print("Resultado desse Hardware: ", result)
            try:
                result = reduce(lambda x, y: x + y, aux[2:]) / len(aux[2:])

                print(bcolors.WARNING + " " + self.__current)
                print(aux)
                print(bcolors.ENDC)
            except:
                if retry > 0:
                    subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"])
                    subprocess.run(["kill", str(p.pid)])
                    retry -= 1
                else:
                    subprocess.run(["kill", str(p.pid)])
                    self._configureBoard()
                    self._transferCode(benchmark)
                    retry = 3
            else:
                subprocess.run(["kill", str(p.pid)])
                return result, aux

    def _getUsageData(self):

        with open(self.__workingDir + "output_files/base.fit.summary", 'r') as f:

            format_string_memory = 'Total block memory bits : {} / {} ( {} % )'
            format_string_ram = 'Total RAM Blocks : {} / {} ( {} % )'
            format_string_alm = 'Logic utilization (in ALMs) : {} / {} ( {} % )'

            output = f.read().splitlines()

            result = {}

            for line in output:
                if 'ALMs' in line:
                    parsed = parse.parse(format_string_alm, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    result['alm'] = used

                if 'block memory bits' in line:
                    parsed = parse.parse(format_string_memory, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    result['memory'] = used

                if 'Total RAM Blocks' in line:
                    parsed = parse.parse(format_string_ram, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    result['ram'] = used

            return result

    def run(self):

        self.__pid = os.getpid()

        while True:

            try:
                self.__current = str(self.__toBenchmark.get_nowait())
            except Exception:
                time.sleep(1)
            else:
                print(str(self.__pid) + " " +self.__current)
                self.__workingDir = self.__rootDir +'/'+self.__current+'/'
                try:
                    self._configureBoard()
                except FileNotFoundError:
                    result = {}
                    result['id'] = int(self.__current)
                    result['time'] = -1
                    self.__result.put(result)
                    print(bcolors.FAIL)
                    print(str(self.__pid) + " " + self.__current + " INVALIDO")
                    print(bcolors.ENDC)
                else:
                    print(bcolors.FAIL)
                    print(str(self.__pid) + " " + self.__current + " config")
                    print(bcolors.ENDC)

                    result = self._getUsageData()
                    result['id'] = int(self.__current)

                    benchmarks = ['checksum', 'fractal']

                    for benchmark in benchmarks:

                        aux= {}

                        self._transferCode(benchmark)
                        print(bcolors.FAIL)
                        print(str(self.__pid) + " " + self.__current + " transf")
                        print(bcolors.ENDC)

                        media, times = self._benchmark(benchmark)
                        aux['time'] = media
                        aux['times'] = times

                        result[benchmark] = aux

                    self.__result.put(result)
                    print(bcolors.FAIL)
                    print(str(self.__pid) + " " + self.__current + " bench")
                    print(bcolors.ENDC)



if __name__ == '__main__':

    target = "/home/bcrodrigues/tcc/"
    base = "/home/bcrodrigues/Dropbox/tcc/script/base/"
    toCompile = Queue()
    toBenchmark = Queue()
    result = Queue()
    prefix = 'q'

    ben1 = TestBench(target, toBenchmark, prefix, base, 1, result)
    ben2 = TestBench(target, toBenchmark, prefix, base, 2, result)

    ben1.start()
    ben2.start()

    results = []

    for x in range(1, 3):
        toBenchmark.put(x)


    while len(results) < 32:
        try:
            results.append(result.get_nowait())
        except Exception:
            time.sleep(1)
            print('\n')

            for i in results:
                print(i)

    ben1.terminate()
    ben2.terminate()

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

