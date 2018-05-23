import subprocess
import os


target ="/home/bcrodrigues/Documents/TCC/run/"
base = "/home/bcrodrigues/Documents/TCC/base/"

if os.path.isdir(target):
    a = subprocess.run(["rm -r " + target], stdout=subprocess.PIPE, shell=True)
    a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)
else:
    a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)

a = subprocess.run(["cp " + base + '/qsys/base.qsys ' + target], stdout=subprocess.PIPE, shell=True)
a = subprocess.run(["qsys-generate --synthesis=VHDL "+target+"base.qsys"], stdout=subprocess.PIPE, shell=True)
a = subprocess.run(["cp -a "+base+"quartus/. "+target], stdout=subprocess.PIPE, shell=True)



# a = subprocess.run(["mkdir " + target], stdout=subprocess.PIPE, shell=True)

#a = subprocess.run(["printenv"], stdout=subprocess.PIPE, shell=True)




# print(a.stdout.decode("utf-8") )