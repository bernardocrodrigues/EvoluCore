
from libs.bootsrap.bootstrap import bootstrap
from libs.librarian.librarian import librarian_milenium, librarian_milenium_bootstrap
import sysGen
import numpy as np



NA = sysGen.nature(['adpcm', 'sobel', 'vecsum', 'quicksort', 'dotprod'], ['alm', 'memory', 'ram'])

lib = librarian_milenium_bootstrap()
lib2 = librarian_milenium()

# lib.init()
last_iteration, traits, objectives = lib.get_last_iteration()

if last_iteration == -1:
    traits, objectives = lib2.get()
    lib.insert_iteration(0, traits, objectives)
    last_iteration = 1

while last_iteration != 30:

    print("iteration: ", last_iteration)

    last_iteration += 1

    traits, objectives, resample = bootstrap.bootstrap(traits, objectives, 0.1)

    print("boostrap: ", resample)

    resample_traits, resample_objectives = NA.life(resample)

    print("benchmarked: ", resample_traits, resample_objectives)

    traits = np.vstack((traits, resample_traits))
    objectives = np.vstack((objectives, resample_objectives))

    lib.insert_iteration(last_iteration, traits, objectives)






#
# # traits = iteration[]
#
#
#
# print(lib.get_last_iteration())
#
