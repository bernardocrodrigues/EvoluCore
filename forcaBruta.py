import sysGen, xmlParse
import os, subprocess, shutil, itertools
from multiprocessing import Process, Queue
import time
from functools import reduce
import json
import pickle


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def genCores(analogParams, step, iterations, discreteParams):

    cores = []
    possibleVal = []

    for x,item in enumerate(analogParams):
        possibleVal.append([])
        for y in range(0, iterations*step, step):
            possibleVal[x].append(str(y))

    for item in discreteParams:
        possibleVal.append(list(item.values())[0])

    paramNames = analogParams + [list(d.keys())[0] for d in discreteParams]


    for x,item in enumerate(itertools.product(*possibleVal)):
        aux = {'id': x+1}
        for x in range(len(item)):
            aux[paramNames[x]] = item[x]
        cores.append(aux)


    return cores

def saveFile(file, mode, dict):

    if mode == 'binary':
        with open(file, 'wb') as file:
            file.write(pickle.dumps(dict))

    if mode == 'json':
        with open(file, 'w') as file:
            file.write(json.dumps(dict))


baseFile = "/home/bcrodrigues/Dropbox/tcc/script/base/qsys/baseOriginal.qsys"
targetDir = "/home/bcrodrigues/tcc/qsys/"

qFac = xmlParse.qsysFactory(baseFile, targetDir)

target = "/home/bcrodrigues/tcc/"
base = "/home/bcrodrigues/Dropbox/tcc/script/base/"
toCompile = Queue()
toBenchmark = Queue()
result = Queue()
prefix = 'q'


start = time.time()


#params = ['icache_size', 'dcache_size']
params = []
discreteParams = [
   # {'dcache_bursts': ['true', 'false']},
   # {'dcache_victim_buf_impl': ['reg', 'ram']},
   # {'icache_burstType': ['Sequential', 'None']},
   # {'setting_support31bitdcachebypass': ['true', 'false']},
   {'dividerType': ['no_div', 'srt2']},
    {'mul_32_impl': ['0', '1', '2', '3']},
    # {'shift_rot_impl': ['1', '0']},
    # {'mul_64_impl': ['1', '0']},
    # {'setting_bhtPtrSz': ['8', '12', '13']},
    # {'setting_branchpredictiontype': ['Dynamic', 'Static']}
    {'icache_size': [
                     '0',
                     # '128',
                     '256',
                     # '512'
    ]},
    {'dcache_size': [
        '0',
    #     # '128',
        '256',
    #     # '512'
    ]}
]



cores = genCores(params, 64, 2, discreteParams)


print(cores)




for core in cores:
    qFac.modifyNios(core)
    qFac.writeCurrentQsys('q' + str(core['id']) + '.qsys')
    qFac.resetCurrentQsys()

for x in range(1, len(cores)+1):
    toCompile.put(x)

gen1 = sysGen.Generator(target, toCompile, prefix, base, toBenchmark)
gen2 = sysGen.Generator(target, toCompile, prefix, base, toBenchmark)
gen3 = sysGen.Generator(target, toCompile, prefix, base, toBenchmark)
gen4 = sysGen.Generator(target, toCompile, prefix, base, toBenchmark)

gen1.start()
gen2.start()
gen3.start()
gen4.start()


# gen1.join()
# gen2.join()
# gen3.join()
# gen4.join()
#
# exit()



bench1 = sysGen.TestBench(target, toBenchmark, prefix, base, 1, result)
bench2 = sysGen.TestBench(target, toBenchmark, prefix, base, 2, result)

bench1.start()
bench2.start()

finish = 0
final = []

while len(final) < len(cores):
    try:
        aux = result.get_nowait()
    except Exception:
        time.sleep(1)
    else:
        final.append(aux)

bench1.terminate()
bench2.terminate()


for core in cores:
    for x in final:
        if core['id'] == x['id']:
            core.update(x)
            # core['time'] = x['time']
            # core['alm'] = x['alm']
            # core['memory'] = x['memory']
            # core['ram'] = x['ram']


saveFile('/home/bcrodrigues/resultado.txt', 'json', cores)

print(bcolors.OKGREEN)
end = time.time()
print(end - start)
print(cores)
print(bcolors.ENDC)



