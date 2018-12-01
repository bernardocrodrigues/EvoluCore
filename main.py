import libs.eidetic.eidetic as eye
import libs.coreFactory.coreFactory as fac
import sysGen
import libs.evo.nsga as nsga
import libs.librarian.librarian as l
import sysGen
import os
import sqlite3
import numpy as np


class log:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    pid = os.getpid()

    @classmethod
    def begin_task(cls, message):
        print(cls.OKGREEN +str(cls.pid)+ cls.ENDC + " | " + cls.BOLD +'MAIN'+ cls.ENDC + " | " + str(message) +" ...")

    @classmethod
    def end_task(cls, message):
        print(cls.OKGREEN +str(cls.pid)+ cls.ENDC + " | " + cls.BOLD +'MAIN'+ cls.ENDC + " | " + str(message) + cls.BOLD + " OK!" + cls.ENDC)



size = 50
cross_over_ratio = 0.9
num_traits = 12
num_objectives = 3
num_generations = 30
experimento = 31
benchmark = 'quicksort'

GA = nsga(size, num_traits, num_objectives, cross_over_ratio)
NA = sysGen.nature([benchmark], ['alm', 'memory'])
lib = l.librarian_nsga()

try:

    lib.create_experimento(experimento, size, cross_over_ratio, num_traits, num_objectives, num_generations, benchmark)

except sqlite3.IntegrityError:

    last_generation, traits, objectives = lib.get_last_population(experimento, num_objectives)
    log.begin_task('Starting NSGA-II')
    log.end_task('Grabbed Generation ' + str(last_generation))

    iterable = range(last_generation, num_generations)
    GA.insert_initial_population(traits, objectives)

else:

    log.begin_task('Starting NSGA-II')
    initial_population = fac.factory.generate_random_cores(size)
    log.end_task('Got first Generation')

    log.begin_task('Benchmarking first Generation')
    traits, objectives = NA.life(initial_population)
    log.end_task('Benchmarking first Generation')

    GA.insert_initial_population(traits, objectives)
    lib.insert_generation(experimento, 0, 0, GA.traits, GA.objectives)

    iterable = range(num_generations)



#
# traits = np.array([['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
#                    ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
#                    ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
#                    ['8192', 'false', 'ram', '2048', 'Sequential', 'false', 'srt2', '3', '0', '0', '13', 'Dynamic'],
#                    ['8192', 'false', 'ram', '2048', 'Sequential', 'false', 'no_div', '2', '0', '1', '12', 'Dynamic'],
#                    ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '3', '1', '0', '13', 'Dynamic'],
#                    ['8192', 'false', 'ram', '1024', 'Sequential', 'true', 'no_div', '2', '0', '0', '12', 'Dynamic'],
#                    ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
#                    ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
#                    ['4096', 'false', 'ram', '1024', 'Sequential', 'true', 'srt2', '3', '0', '0', '13', 'Dynamic']])
#
# objectives = np.array([[1.65900600e+06, 1.29400000e+03],
#                        [1.65898967e+06, 1.29500000e+03],
#                        [1.65898700e+06, 1.29700000e+03],
#                        [9.86180500e+05, 1.62600000e+03],
#                        [1.00909567e+06, 1.55400000e+03],
#                        [1.63605167e+06, 1.35400000e+03],
#                        [1.00909750e+06, 1.50900000e+03],
#                        [1.65900400e+06, 1.29400000e+03],
#                        [1.65900100e+06, 1.29600000e+03],
#                        [1.00791117e+06, 1.63600000e+03]])


generations = [GA.objectives]

# generation =-1

for generation in iterable:


    print('\n################################################')
    print('Geração {}: \n {}\n {}'.format(generation, GA.traits, GA.objectives))

    # eye.plot([GA.objectives], file="geracao_"+str(generation)+'.png')


    log.begin_task('Getting children')
    children = GA.get_children()
    log.end_task('Getting children')

    print('Filhos {}: \n {}'.format(generation, children))

    # children_traits = np.array([['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '3', '0', '0', '13', 'Dynamic'],
    #                             ['4096', 'false', 'ram', '1024', 'Sequential', 'true', 'srt2', '3', '1', '0', '13', 'Dynamic'],
    #                             ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
    #                             ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
    #                             ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
    #                             ['8192', 'false', 'ram', '1024', 'Sequential', 'true', 'no_div', '2', '0', '0', '12', 'Dynamic'],
    #                             ['8192', 'false', 'ram', '2048', 'Sequential', 'false', 'no_div', '2', '0', '1', '12', 'Dynamic'],
    #                             ['8192', 'false', 'ram', '2048', 'Sequential', 'false', 'srt2', '3', '0', '0', '13', 'Dynamic'],
    #                             ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic'],
    #                             ['0', 'false', 'reg', '2048', 'None', 'false', 'srt2', '0', '0', '0', '12', 'Dynamic']])
    # #
    # children_objectives = np.array([[1.63605600e+06, 1.34900000e+03],
    #                                 [1.00909867e+06, 1.55800000e+03],
    #                                 [1.65900200e+06, 1.29700000e+03],
    #                                 [1.65900400e+06, 1.29500000e+03],
    #                                 [1.00790350e+06, 1.62700000e+03],
    #                                 [1.65900600e+06, 1.29700000e+03],
    #                                 [1.00909667e+06, 1.50100000e+03],
    #                                 [9.86180500e+05, 1.62600000e+03],
    #                                 [1.65900100e+06, 1.29400000e+03],
    #                                 [1.65900400e+06, 1.29100000e+03]]
    #                                )

    log.begin_task('Benchmarking children')
    children_traits, children_objectives = NA.life(children)
    log.end_task('Benchmarking children')

    lib.insert_generation(experimento, generation, 1, children_traits, children_objectives)

    print('Filhos benched {}: \n {}'.format(generation, children_objectives))

    # try:
        # eye.plot([children_objectives], file="filhos_" + str(generation) + '.png')
    # except Exception:
    #     pass

    GA.iterate_population(children_traits, children_objectives)
    lib.insert_generation(experimento, generation + 1, 0, GA.traits, GA.objectives)
    generations.append(GA.objectives)

print(generations)

eye.plot(generations, file="generations_"+ str(experimento)+".png")
