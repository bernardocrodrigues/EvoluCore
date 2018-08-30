
import numpy as np
import libs.librarian.librarian as lib
import libs.paretoFrontier.paretoFrontier as pf

class eda(object):

    libr = lib.librarian()

    @classmethod
    def get_population_statistics(self, population: np.array):

        for individual in population:
            print(individual[0])
            traits = libr.get_core_characteristics(individual[0])
            print(traits)


if __name__ == "__main__":

    libr = lib.librarian()

    data = libr.get_data(20)
    fittest, dominated = pf.get_pareto_fittest(data, 10)

    eda.get_population_statistics(fittest)