import subprocess
import os
from multiprocessing import Process, Queue
import time
import parse
from functools import reduce


target = "/home/bcrodrigues/tcc/run/"
base = "/home/bcrodrigues/Dropbox/tcc/script/base/"
code = "fractal"

mode = 1
to_program = False

def configure(q):
    q.put(os.getpid())
    print("Quartus Programmer on PID "+ str(os.getpid()))

    success = False

    p = subprocess.Popen("quartus_pgm -z --mode=JTAG --operation=\"p;" + target + "output_files/base_time_limited.sof@2\"", stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)

    for line in iter(p.stdout.readline, b''):
        string = line.decode("utf-8")
        if "Configuration succeeded" in string:
            success = True
            break
        if "Operation failed" in string:
            break

    subprocess.run(["kill " + str(p.pid)], stdout=subprocess.PIPE, shell=True)

    q.put(success)

    # subprocess.run(["quartus_pgm -z --mode=JTAG --operation=\"p;" + target + "output_files/base_time_limited.sof@2\""], stdout=subprocess.PIPE, shell=True)

def program():
    time.sleep(1)
    subprocess.run(["nios2-download -r -g " + target + "/software/hello_world.elf"], shell=True)

def doTheConfiguration():
    q = Queue()
    p = Process(target=configure, args=(q,))
    p.start()
    process = q.get()
    success = q.get()
    subprocess.run(["kill " + str(process)], stdout=subprocess.PIPE, shell=True)
    return success


if mode <= 1:
    if os.path.isdir(target):
        a = subprocess.run(["rm -r " + target], stdout=subprocess.PIPE, shell=True)
        a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)
    else:
        a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)

if mode <= 2:
    subprocess.run(["cp " + base + '/qsys/base.qsys ' + target], shell=True)
    a = subprocess.run(["qsys-generate --synthesis=VHDL "+target+"base.qsys"], shell=True)
    returnCode = a.returncode
    if returnCode != 0:
        exit()



if mode <= 3:
    a = subprocess.run(["cp -a "+base+"quartus/. "+target], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["quartus_sh --flow compile "+target+"base.qpf"], stdout=subprocess.PIPE, shell=True)


exit()

if mode <= 4:
    a = subprocess.run(["mkdir " + target+"software"], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["nios2-bsp hal "+target+"/software/bsp "+target+"/base.sopcinfo --script="+base+"/bsp/parameters.tcl"], stdout=subprocess.PIPE, shell=True)
    # a = subprocess.run(["nios2-app-generate-makefile --bsp-dir="+target+"/software/bsp --src-files ="+base+"software/hello_world.c --app-dir="+target+"/software/"], stdout=subprocess.PIPE, shell=True)
    subprocess.run(["nios2-app-generate-makefile --bsp-dir=" + target + "/software/bsp --src-rdir=" + base + "software/"+code+"/ --app-dir=" + target + "/software/ --elf-name code.elf"],
                   stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["make -C "+target+"/software/"], stdout=subprocess.PIPE, shell=True)

if mode <= 5 and to_program:
    while not doTheConfiguration():
        subprocess.run(["killall jtagd"], shell=True)

if mode <= 6:

    confiredProperly = False

    while not confiredProperly:
        returnCode = -1
        retry = -1

        while returnCode != 0:
            a = subprocess.run(["nios2-download -r -g " + target + "/software/code.elf"], shell=True)

            returnCode = a.returncode
            retry += 1
            if retry > 5:
                break

        if returnCode != 0:
            subprocess.run(["killall jtagd"], shell=True)
            doTheConfiguration()
        else:
            subprocess.run(["nios2-download -g"], shell=True)
            confiredProperly = True

    time.sleep(0.5)

    gotBenchmark = False

    while not gotBenchmark:
        p = subprocess.Popen('nios2-terminal -o 60', stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)

        result = []
        for x in range(20):
            for line in iter(p.stdout.readline, b''):
                string = line.decode("utf-8")
                try:
                    result.append(int(string))
                except:
                    pass
                else:
                    break

        print("Resultado desse Hardware: ", result)
        try:
            print(reduce(lambda x, y: x + y, result) / len(result))
        except:
            subprocess.run(["nios2-download -g"], shell=True)
            subprocess.run(["kill " + str(p.pid)], stdout=subprocess.PIPE, shell=True)
            pass
        else:
            gotBenchmark = True
            subprocess.run(["kill " + str(p.pid)], stdout=subprocess.PIPE, shell=True)

with open(target+"output_files/base.fit.summary",'r') as f:

    format_string_memory = 'Total block memory bits : {} / {} ( {} % )'
    format_string_ram = 'Total RAM Blocks : {} / {} ( {} % )'
    format_string_alm = 'Logic utilization (in ALMs) : {} / {} ( 3 % )'

    output = f.read().splitlines()

    for line in output:
        if 'ALMs' in line:

            parsed = parse.parse(format_string_alm, line)

            used = int(parsed[0].replace(',', ''))
            total = int(parsed[1].replace(',', ''))

            print(used / total)

        if 'block memory bits' in line:
            parsed = parse.parse(format_string_memory, line)

            used = int(parsed[0].replace(',', ''))
            total = int(parsed[1].replace(',', ''))

            print(used/total)

        if 'Total RAM Blocks' in line:
            parsed = parse.parse(format_string_ram, line)

            used = int(parsed[0].replace(',', ''))
            total = int(parsed[1].replace(',', ''))

            print(used/total)

exit()

# key = None
# while key != 'y':
#     key = input('Exit?')

#a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)
#a = subprocess.run(["printenv"], stdout=subprocess.PIPE, shell=True)

#