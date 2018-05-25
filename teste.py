import subprocess
import os
from multiprocessing import Process, Queue
import time


target ="/home/bcrodrigues/Documents/TCC/run/"
base = "/home/bcrodrigues/Documents/TCC/base/"
mode = 3

def program(name, q):
    q.put(os.getpid())
    print("Quartus Programmer on PID "+ str(os.getpid()))
    subprocess.run(["quartus_pgm -z --mode=JTAG --operation=\"p;" + target + "output_files/base_time_limited.sof@2\""],
                   stdout=subprocess.PIPE, shell=True)


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


q = Queue()
p = Process(target=program, args=('bob', q,))
p.start()

process = q.get()

key = None

while key != 'y':
    key = input('Exit?')

a = subprocess.run(["kill " + str(process)], stdout=subprocess.PIPE, shell=True)
exit()

#BSP
#nios2-bsp hal ./bsp ../base.sopcinfo --script=parameters.tcl

print(a.stdout.decode("utf-8"))


#a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)
#a = subprocess.run(["printenv"], stdout=subprocess.PIPE, shell=True)

#