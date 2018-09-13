
import numpy as np
import libs.librarian.librarian as li
import math
import itertools
import libs.paretoFrontier.paretoFrontier as pf
import libs.eidetic.eidetic as eye
import pprint





class eda(object):

    lib = li.librarian()

    @classmethod
    def get_population_statistics_beta(cls, population: np.array):

        model = [{},{},{},{},{},{},{},{},{},{},{},{}]
        population_size = population.shape[0]

        for individual in population:
            genotype = cls.lib.get_core_characteristics(individual[0])
            for gen, trait in zip(genotype, model):
                if gen in trait.keys():
                    trait[gen] += 1
                else:
                    trait[gen] = 1

        for trait in model:
            for key, value in trait.items():
                trait[key] = value/population_size


        return model

    @classmethod
    def get_population_statistics(cls, population: np.array, bbs = None):

        model = {}
        population_size = population.shape[0]

        for bb in bbs:
            model[bb] = {}

        for individual in population:
            for bb in bbs:
                alelo = ()
                for gen in bb:
                    alelo += (individual[gen-1],)
                if alelo in model[bb].keys():
                    model[bb][alelo] += 1
                else:
                    model[bb][alelo] = 1

        for key, value in model.items():
            for inner_key, inner_value in value.items():
                model[key][inner_key] = inner_value/population_size

        return model

    @classmethod
    def gen_partition(cls, partitioning = None, size = 5):

        if partitioning == None:
            partitioning = []
            for i in range(1, size+1):
                partitioning.append((i,))
        else:
            for i in range(1, size+1):
                for bb in partitioning:
                    there = False
                    for item in bb:
                        if item == i:
                            there = True
                            break
                    if there:
                        break
                else:
                    partitioning.append((i,))
        return partitioning

    @classmethod
    def gen_initial_partition(cls, size):

        partitioning = []
        for i in range(0, size):
            partitioning.append((i,))
        return partitioning

    @classmethod
    def fill_in_partion(cls, new_bb, old_partition):

        partition = [new_bb]
        for item in old_partition:
            for sub_item in item:
                if sub_item in new_bb:
                    break
            else:
                partition.append(item)
        return partition


    @classmethod
    def get_model_compexity(cls, partitioning, population_size):

        complexity = 0
        for bb in partitioning:
            complexity += 2**(len(bb))-1
        return complexity*math.log(population_size,2)

    @classmethod
    def get_compressed_model_complexity(cls, model, population_size):

        outer_aux = 0
        for bb in model.values():
            inner_aux=0
            for instance in bb.values():
                try:
                    inner_aux -= instance * (math.log(instance, 2))
                except ValueError:
                    pass
            outer_aux += inner_aux

        return(outer_aux*population_size)

    @classmethod
    def get_linkage(cls, population: np.array, max_patiton_size: int):

        population_size = population.shape[0]
        trait_num = population.shape[1]

        partition = cls.gen_initial_partition(trait_num)
        model = cls.get_population_statistics(population,partition)
        combined_complexity = cls.get_model_compexity(model, population_size) + cls.get_compressed_model_complexity(model, population_size)

        smallest_complexity = combined_complexity

        while True:
            found = False
            for compound_bb in itertools.combinations(partition, 2):
                aux = ()
                for element in compound_bb:
                    aux += element

                if len(aux) > max_patiton_size:
                    continue

                new_partition = cls.fill_in_partion(aux, partition)
                # print(new_partition)
                model = cls.get_population_statistics(population, new_partition)
                combined_complexity = cls.get_model_compexity(model, population_size) + cls.get_compressed_model_complexity(
                    model, population_size)

                # print(new_partition)
                # print(combined_complexity)
                # pprint.pprint(model)
                # print('\n')

                if combined_complexity < smallest_complexity:
                    smallest_complexity = combined_complexity
                    aux_partition = new_partition
                    found = True

            if not found:
                break
            else:
                partition = aux_partition

        return partition

        # for compound_bb in itertools.combinations(chosen_partition, 2):
        #     aux = ()
        #     for element in compound_bb:
        #         aux += element
        #
        #     new_partition = cls.fill_in_partion(aux, chosen_partition)
        #
        #     model = cls.get_population_statistics(population, new_partition)
        #     combined_complexity = cls.get_model_compexity(model, population_size) + cls.get_compressed_model_complexity(
        #         model, population_size)
        #
        #     print(new_partition)
        #     print(combined_complexity)
            # pprint.pprint(model)

            # print(new_partition)

            # pprint.pprint(model)


            # compound_bb = compound_bb

            # print(i)

        # print(partition)


        # a = [(0, 2), (1, 3)]
        #
        # b = {(0,2):{(0,0):0,
        #             (0,1):3/8,
        #             (1,0):5/8,
        #             (1,1):0},
        #      (1, 3): {(0, 0): 3/8,
        #               (0, 1): 1 / 8,
        #               (1, 0): 1 / 8,
        #               (1, 1): 3/8}}


        # x = cls.get_model_compexity(a,8)
        # y = cls.get_compressed_model_complexity(b,8)
        #
        # print(x,y)
        #
        # print(x + y)

    @classmethod
    def get_population_traits(cls, population: np.array) -> np.array:

        population_traits = []

        for individual in population:
            population_traits.append(cls.lib.get_core_characteristics(individual[0]))

        return np.array(population_traits)



if __name__ == "__main__":

    import libs.eidetic.eidetic as eye

    # population = [(1, 0, 0, 0),
    #               (1, 1, 0, 1),
    #               (0, 1, 1, 1),
    #               (1, 1, 0, 0),
    #               (0, 0, 1, 0),
    #               (0, 1, 1, 1),
    #               (1, 0, 0, 0),
    #               (1, 0, 0, 1)]
    # population = np.array(population)

    # eda.get_linkage(1)

    lib = li.librarian()
    # data = lib.get_data(1000)
    data = lib.get_benchmark_data(benchmark="quicksort", metrics=["alm", "memory", "ram"])
    fittest, dominated = pf.get_pareto_fittest(data, 100)
    # population = eda.get_population_traits(fittest)
    # partition = eda.get_linkage(population, 10)

    eye.plot_3D([fittest, dominated], xlabel="quicksort", title="adpcm", ylabel="alm", zlabel="memory",
                    barlabel="ram")

    # pprint.pprint(eda.get_population_statistics(population,partition))

    # print(population)



    # data = lib.get_benchmark_data(benchmark="quicksort", metrics=["alm", "memory", "ram"])

    #

    # eye.plot_3D([fittest, dominated], xlabel="quicksort", title="adpcm", ylabel="alm", zlabel="memory",
    #                 barlabel="ram")
    # model = eda.get_population_statistics(fittest)

    # model = eda.get_population_statistics(data, [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12)])

    # pprint.pprint(model)

    # model = eda.get_population_statistics(data)
    # for item in model:
    #     for key, value in item.items():
    #         print("{0}: {1:.2f}%".format(key, value*100))
    #     print('\n')