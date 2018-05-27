import subprocess
import os
from multiprocessing import Process, Queue
import time
from functools import reduce
target ="/home/bcrodrigues/Documents/TCC/run/"
base = "/home/bcrodrigues/Documents/TCC/base/"
mode = 3
to_program = True

def configure(q):
    q.put(os.getpid())
    print("Quartus Programmer on PID "+ str(os.getpid()))
    subprocess.run(["quartus_pgm -z --mode=JTAG --operation=\"p;" + target + "output_files/base_time_limited.sof@2\""],
                   stdout=subprocess.PIPE, shell=True)

def program():
    time.sleep(1)
    subprocess.run(["nios2-download -r -g " + target + "/software/hello_world.elf"], shell=True)



if mode < 1:
    if os.path.isdir(target):
        a = subprocess.run(["rm -r " + target], stdout=subprocess.PIPE, shell=True)
        a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)
    else:
        a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)

if mode < 2:
    a = subprocess.run(["cp " + base + '/qsys/base.qsys ' + target], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["qsys-generate --synthesis=VHDL "+target+"base.qsys"], stdout=subprocess.PIPE, shell=True)

if mode < 3:
    a = subprocess.run(["cp -a "+base+"quartus/. "+target], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["quartus_sh --flow compile "+target+"base.qpf"], stdout=subprocess.PIPE, shell=True)

if mode < 4:
    a = subprocess.run(["mkdir " + target+"software"], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["nios2-bsp hal "+target+"/software/bsp "+target+"/base.sopcinfo --script="+base+"/bsp/parameters.tcl"], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["nios2-app-generate-makefile --bsp-dir="+target+"/software/bsp --src-files ="+base+"software/hello_world.c --app-dir="+target+"/software/"], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["make -C "+target+"/software/"], stdout=subprocess.PIPE, shell=True)

if mode < 5 and to_program:
    q = Queue()
    p = Process(target=configure, args=(q,))
    p.start()
    process = q.get()
    time.sleep(10)
    #a = subprocess.run(["kill " + str(process)], stdout=subprocess.PIPE, shell=True)


# subprocess.run(["nios2-download -r -g "+target+"/software/hello_world.elf"], shell=True)
# subprocess.run(["nios2-download -g "], shell=True)
p1 = Process(target=program)
p1.start()
p = subprocess.Popen('nios2-terminal', stdout=subprocess.PIPE, preexec_fn=os.setsid)
result = []

for x in range(20):
    for line in iter(p.stdout.readline, b''):
        string = line.decode("utf-8")
        # print(string)
        try:
            result.append(int(string))
        except:
            pass
        else:
            break

print("Resultado desse Hardware: ", result)
print(reduce(lambda x, y: x + y, result) / len(result))
subprocess.run(["kill " + str(p.pid)], stdout=subprocess.PIPE, shell=True)

exit()

# key = None
# while key != 'y':
#     key = input('Exit?')

#a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)
#a = subprocess.run(["printenv"], stdout=subprocess.PIPE, shell=True)

#