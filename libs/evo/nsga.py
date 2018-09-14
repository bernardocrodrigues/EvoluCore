
import numpy as np
import random
import libs.coreFactory.coreFactory as factory

class nsga(object):

    class InvalidPopulationSize(Exception):
        pass

    class InvalidTraitsSize(Exception):
        pass

    class InvalidObjectivesSize(Exception):
        pass

    def __init__(self, population_size, num_traits, num_objectives, cross_over_ratio):
        self.population_size = population_size
        self.cross_over_ratio = cross_over_ratio
        self.num_traits = num_traits
        self.num_objectives = num_objectives
        self.mutation_rate = 1/num_traits

    def __check_population(self, traits, objectives):

        if traits.shape[0] != self.population_size or objectives.shape[0] != self.population_size:
            raise self.InvalidPopulationSize
        if traits.shape[0] % 2  != 0:
            raise self.InvalidPopulationSize
        if traits.shape[1] != self.num_traits:
            raise self.InvalidTraitsSize
        if objectives.shape[1] != self.num_objectives:
            raise self.InvalidObjectivesSize

    def insert_initial_population(self, traits, objectives):

        self.__check_population(traits,objectives)



        # (aux_trait_frontier, aux_objective_frontier), (aux_dominated_traits, aux_dominated_objectives) = self.__fast_non_dominated_sort(traits,objectives)
        #
        # trait_frontiers = [aux_trait_frontier]
        # objective_frontiers = [aux_objective_frontier]
        # rank = np.ones(trait_frontiers[0].shape[0])
        #
        # rank_index = 2
        #
        # while aux_dominated_traits.shape[0] != 0:
        #
        #     (aux_trait_frontier, aux_objective_frontier), (aux_dominated_traits, aux_dominated_objectives) = self.__fast_non_dominated_sort(aux_dominated_traits, aux_dominated_objectives)
        #     trait_frontiers.append(aux_trait_frontier)
        #     objective_frontiers.append(aux_objective_frontier)
        #     rank = np.concatenate((rank, rank_index*np.ones(aux_trait_frontier.shape[0])))
        #     rank_index += 1
        #
        # trait_frontiers = np.vstack(trait_frontiers)
        # objective_frontiers = np.vstack(objective_frontiers)

        parents = self.__binary_tournament(traits)
        children = []
        for parent_a, parent_b in parents:
            if np.random.uniform(0,1) < self.cross_over_ratio:
                child_a, child_b = self.__crossover(parent_a, parent_b)
                child_a = self.__mutation(child_a)
                child_b = self.__mutation(child_b)
                children.append(child_a)
                children.append(child_b)











    def __binary_tournament(self, traits):

        random_indexes = random.sample(range(0, self.population_size), self.population_size)

        parents = []
        for a, b in zip(random_indexes[1::2],random_indexes[0::2]):
            parents.append((traits[a], traits[b]))

        return parents

    def __crossover(self, parent_a, parent_b):

        cut_point = np.random.randint(1, parent_a.size)
        child_a = np.concatenate((parent_a[:cut_point], parent_b[cut_point:]))
        child_b = np.concatenate((parent_b[:cut_point], parent_a[cut_point:]))

        return  child_a, child_b

    def __mutation(self, traits):

        if np.random.uniform(0, 1) < self.mutation_rate:

            return factory.factory.randomize_genes(traits, [np.random.randint(0, self.num_traits)])
        else:
            return traits





    def get_current_population(self):
        pass

    def iterate_population(self, population : np.array):
        pass

        # print(self.__fast_non_dominated_sort(population))


    def __fast_non_dominated_sort(self, trait_space: np.array, objective_space: np.array):

        trait_frontier = np.array(trait_space[0:1])
        objective_frontier = np.array(objective_space[0:1])

        for trait_candidate, objective_candidate in zip(trait_space[1:, ], objective_space[1:, ]):

            partial_objective_domination = (objective_candidate < objective_frontier)
            dominated_indexes = partial_objective_domination.all(axis=1)

            try:
                dominated_traits = np.vstack((dominated_traits, trait_frontier[dominated_indexes]))
                dominated_objectives = np.vstack((dominated_objectives, objective_frontier[dominated_indexes]))
            except UnboundLocalError:
                dominated_traits = trait_frontier[dominated_indexes]
                dominated_objectives = objective_frontier[dominated_indexes]

            trait_frontier = trait_frontier[~dominated_indexes]
            objective_frontier = objective_frontier[~dominated_indexes]

            will_go = partial_objective_domination.any(axis=1).all()

            if will_go:
                trait_frontier = np.vstack((trait_frontier, trait_candidate))
                objective_frontier = np.vstack((objective_frontier, objective_candidate))
            else:
                dominated_traits = np.vstack((dominated_traits, trait_candidate))
                dominated_objectives = np.vstack((dominated_objectives, objective_candidate))
        try:
            return (trait_frontier, objective_frontier), (dominated_traits,dominated_objectives)
        except UnboundLocalError:
            return (trait_frontier, objective_frontier), (np.array([]), np.array([]))





if __name__ == '__main__':

    import libs.librarian.librarian as l

    size = 10
    cross_over_ratio = 0.9
    num_traits = 12
    num_objectives = 4

    lib = l.librarian()
    traits, objectives = lib.get(size)

    n = nsga(size, num_traits, num_objectives, cross_over_ratio)
    n.insert_initial_population(traits, objectives)

    # print(traits, objectives)





