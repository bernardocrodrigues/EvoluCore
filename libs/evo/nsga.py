import numpy as np
import random
import libs.coreFactory.coreFactory as factory
import libs
import libs.eidetic.eidetic as eye
import libs.paretoFrontier as pf


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
        self.mutation_rate = 1 / num_traits

        self.traits = None
        self.objectives = None

    def __check_population(self, traits, objectives):

        if traits.shape[0] != self.population_size or objectives.shape[0] != self.population_size:
            raise self.InvalidPopulationSize
        if traits.shape[0] % 2 != 0:
            raise self.InvalidPopulationSize("Not even")
        if traits.shape[1] != self.num_traits:
            raise self.InvalidTraitsSize
        if objectives.shape[1] != self.num_objectives:
            raise self.InvalidObjectivesSize

    def insert_initial_population(self, traits, objectives):

        self.traits = traits
        self.objectives = objectives

    def get_children(self):

        parents = self.__binary_tournament(self.traits)
        children = []
        for parent_a, parent_b in parents:
            if np.random.uniform(0,1) < self.cross_over_ratio:
                child_a, child_b = self.__crossover(parent_a, parent_b)

                if not factory.factory.validate_core(child_a):
                    child_a = factory.factory.generate_random_cores(1)[0]

                if not factory.factory.validate_core(child_b):
                    child_b = factory.factory.generate_random_cores(1)[0]

                child_a = self.__mutation(child_a)
                child_b = self.__mutation(child_b)
                children.append(child_a)
                children.append(child_b)
        return np.array(children)

    def __binary_tournament(self, traits):

        random_indexes = random.sample(range(0, self.population_size), self.population_size)

        parents = []
        for a, b in zip(random_indexes[1::2], random_indexes[0::2]):
            parents.append((traits[a], traits[b]))

        return parents

    def __crossover(self, parent_a, parent_b):

        cut_point = np.random.randint(1, parent_a.size)
        child_a = np.concatenate((parent_a[:cut_point], parent_b[cut_point:]))
        child_b = np.concatenate((parent_b[:cut_point], parent_a[cut_point:]))

        return child_a, child_b

    def __mutation(self, traits):

        if np.random.uniform(0, 1) < self.mutation_rate:

            return factory.factory.randomize_genes(traits, [np.random.randint(0, self.num_traits)])
        else:
            return traits

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
            return (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives)
        except UnboundLocalError:
            return (trait_frontier, objective_frontier), (np.array([]), np.array([]))

    def __get_stacked_frontiers(self, traits, objectives):

        (aux_trait_frontier, aux_objective_frontier), (
            aux_dominated_traits, aux_dominated_objectives) = self.__fast_non_dominated_sort(traits, objectives)

        trait_frontiers = [aux_trait_frontier]
        objective_frontiers = [aux_objective_frontier]
        rank = np.ones(trait_frontiers[0].shape[0])

        print(aux_trait_frontier.shape[0])

        rank_index = 2
        a = 1
        while aux_dominated_traits.shape[0] != 0:
            a += 1
            (aux_trait_frontier, aux_objective_frontier), (
                aux_dominated_traits, aux_dominated_objectives) = self.__fast_non_dominated_sort(aux_dominated_traits,
                                                                                                 aux_dominated_objectives)
            trait_frontiers.append(aux_trait_frontier)
            objective_frontiers.append(aux_objective_frontier)
            rank = np.concatenate((rank, rank_index * np.ones(aux_trait_frontier.shape[0])))
            rank_index += 1
            print(aux_trait_frontier.shape[0])

        # trait_frontiers = np.vstack(trait_frontiers)
        # objective_frontiers = np.vstack(objective_frontiers)
        # print(a)
        return np.vstack(trait_frontiers), np.vstack(objective_frontiers), rank

    def __get_frontiers(self, traits, objectives):

        (aux_trait_frontier, aux_objective_frontier), (
            aux_dominated_traits, aux_dominated_objectives) = self.__fast_non_dominated_sort(traits, objectives)

        trait_frontiers = [aux_trait_frontier]
        objective_frontiers = [aux_objective_frontier]

        while aux_dominated_traits.shape[0] != 0:
            (aux_trait_frontier, aux_objective_frontier), (
                aux_dominated_traits, aux_dominated_objectives) = self.__fast_non_dominated_sort(aux_dominated_traits,
                                                                                                 aux_dominated_objectives)
            trait_frontiers.append(aux_trait_frontier)
            objective_frontiers.append(aux_objective_frontier)

        return trait_frontiers, objective_frontiers

    def __get_fittest(self, traits, objectives, max_size):

        frontier_trait, frontier_objectives = self.__get_frontiers(traits, objectives)

        coverage_idx = 0
        population = frontier_trait[coverage_idx].shape[0]

        if population == max_size:
            return frontier_trait[0], frontier_objectives[0]
        else:
            while population < max_size:
                coverage_idx += 1
                population += frontier_trait[coverage_idx].shape[0]

            if coverage_idx != 0:
                partial_trait = np.vstack(frontier_trait[:coverage_idx])
                partial_objective = np.vstack(frontier_objectives[:coverage_idx])
                ordered_traits, ordered_objectives = self.__sort_by_crowding_distance(frontier_trait[coverage_idx], frontier_objectives[coverage_idx])
                delta = max_size - partial_trait.shape[0]
                fittest_trait = np.vstack((partial_trait, ordered_traits[:delta]))
                fittest_objective = np.vstack((partial_objective, ordered_objectives[:delta]))

            else:

                ordered_traits, ordered_objectives = self.__sort_by_crowding_distance(frontier_trait[coverage_idx],
                                                                                      frontier_objectives[coverage_idx])

                delta = max_size - ordered_traits.shape[0]
                fittest_trait = ordered_traits[:delta]
                fittest_objective = ordered_objectives[:delta]


            return fittest_trait, fittest_objective

    def __sort_by_crowding_distance(self, traits: np.array, objectives: np.array):

        upper = objectives.shape[0]
        distance = np.zeros(upper)

        for column in objectives.T:

            new_order = column.argsort()
            sorted_column = column[new_order]

            distance[new_order[0]] = -1
            distance[new_order[upper - 1]] = -1

            min = sorted_column[0]
            max = sorted_column[-1]
            denominador = max - min

            for idx, item in enumerate(sorted_column[1:-1]):

                if distance[new_order[idx + 1]] != -1:
                    this_distance = sorted_column[idx + 2] - sorted_column[idx]
                    distance[new_order[idx + 1]] += (this_distance-min)/denominador

        edges = distance == -1

        ordered_objectives = objectives[edges]
        ordered_traits = traits[edges]

        aux = objectives[~edges]
        aux1 = traits[~edges]
        aux2 = distance[~edges]

        ordered_objectives = np.vstack((ordered_objectives, aux[list(reversed(aux2.argsort()))]))
        ordered_traits = np.vstack((ordered_traits, aux1[list(reversed(aux2.argsort()))]))

        return ordered_traits, ordered_objectives

    def get_current_population(self):
        pass

    def iterate_population(self, traits, objectives):

        try:
            self.traits = np.vstack((self.traits, traits))
            self.objectives = np.vstack((self.objectives, objectives))
            self.traits, self.objectives = self.__get_fittest(self.traits, self.objectives, self.population_size)
        except ValueError:
            pass



if __name__ == '__main__':

    import libs.librarian.librarian as l

    import libs.coreFactory.coreFactory as fac
    import sysGen

    size = 100
    cross_over_ratio = 0.9
    num_traits = 12
    num_objectives = 2
    num_generations = 5
    experimento = 1
    benchmark = 'adpcm'

    GA = nsga(size, num_traits, num_objectives, cross_over_ratio)
    NA = sysGen.nature([benchmark])
    lib = l.librarian_nsga()

    lib.create_experimento(experimento, size, cross_over_ratio, num_traits, num_objectives, num_generations, benchmark)


    # initial_population = fac.factory.generate_random_cores(8)
    # traits, objectives = natur.life(initial_population)

    aux_trait, aux_objective = lib.get(100)
    traits = aux_trait[:50]
    objectives = aux_objective[:50]

    eye.plot([objectives], file="a.png")

    n.insert_initial_population(traits, objectives)

    # for generation in range(num_generations):

    children = n.get_children()

    traits, objectives = natur.life(children)

    eye.plot([objectives], file="a.png")





    # get initial population
    # nsga.insert initial population
    # while rodando:
        #nsga. get children
        #        eye.plot([fittest_objective], file="b.png")
        #benchmark children
        #insert children
        #get new population





    # n.insert_initial_population(traits, objectives)

    # print(traits, objectives)





