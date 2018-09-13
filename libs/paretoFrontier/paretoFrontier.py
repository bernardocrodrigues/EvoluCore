import sqlite3
import numpy as np
from functools import reduce

def get_data():
    conn = sqlite3.connect('/home/bcrodrigues/Dropbox/tcc/script/millenium.db', isolation_level='EXCLUSIVE')
    cur = conn.cursor()
    return np.array(cur.execute("select id_core, adpcm, alm from core").fetchmany(1000))

def get_strongly_dominated(reference: np.array, space: np.array):

    no_core_id_reference = reference[1:]
    no_core_id_space = space[:,1:]

    indexes = (no_core_id_space > no_core_id_reference).all(axis=1)

    return indexes

def get_frontier(full_space: np.array):
    frontier = full_space
    dominated = []
    searching = True

    while searching:
        for candidate in frontier:
            dominated_indexes = get_strongly_dominated(candidate, frontier)
            if np.any(dominated_indexes):
                dominated.append(frontier[dominated_indexes])
                frontier = frontier[~dominated_indexes]
                break
        else:
            searching = False
    if len(dominated) > 0:
        return frontier, np.vstack(dominated)
    else:
        return frontier, np.array([])

def get_frontiers(full_space: np.array, num: int):

    frontiers = []
    space = full_space

    for x in range(num):
        frontier, dominated = get_frontier(space)
        frontiers.append(frontier)
        if dominated.size == 0:
            space = dominated
            break
        else:
            space = dominated

    return frontiers, space

def get_pareto_fittest(full_space: np.array, num: int):

    if num > 0 and num <= full_space.shape[0]:
        fittest, space = get_frontier(full_space)

        if fittest.shape[0] > num:
            fittest, discarted = sumerize_frontier_with_id(fittest, num)
            space = np.vstack((space,discarted))
        else:
            while fittest.shape[0] < num:
                frontier, dominated = get_frontier(space)
                if fittest.shape[0] + frontier.shape[0] > num:
                    frontier, discarted = sumerize_frontier_with_id(frontier, (num - fittest.shape[0]))
                    dominated = np.vstack((dominated, discarted))
                fittest = np.vstack((fittest, frontier))
                space = dominated

        return fittest, space
    else:
        raise ValueError

def sumerize_frontier(full_space: np.array, num: int):

    space = full_space

    while(np.shape(space)[0] > num):
        greatest = -1
        greatest_distance = -1

        for i, candidate in enumerate(space):

            previous_slice = space[:i, :]
            next_slice = space[i + 1:, :]
            candidate_less_space = np.vstack((previous_slice, next_slice))
            distance = get_total_space_distance(candidate_less_space)

            if greatest_distance == -1:
                greatest = i
                greatest_distance = distance
            elif greatest_distance < distance:
                greatest = i
                greatest_distance = distance
            elif greatest_distance == distance:

                previous_slice = space[:i, :]
                next_slice = space[i + 1:, :]
                candidate_less_space = np.vstack((previous_slice, next_slice))
                deviation1 = get_total_space_distance_std_deviation(candidate_less_space)

                previous_slice = space[:greatest, :]
                next_slice = space[greatest + 1:, :]
                candidate_less_space = np.vstack((previous_slice, next_slice))
                deviation2 = get_total_space_distance_std_deviation(candidate_less_space)

                if deviation1 < deviation2:
                    greatest = i
                    greatest_distance = distance

        print(greatest)
        space = np.delete(space, greatest, 0)

        print(space)

    return space

def sumerize_frontier_with_id(full_space: np.array, num: int):

    space = full_space[:, 1:]
    space_with_core_id = full_space
    discarted = []


    while(np.shape(space)[0] > num):

        greatest = -1
        greatest_distance = -1

        for i, candidate in enumerate(space):

            previous_slice = space[:i, :]
            next_slice = space[i + 1:, :]
            candidate_less_space = np.vstack((previous_slice, next_slice))
            distance = get_total_space_distance(candidate_less_space)

            if greatest_distance == -1:
                greatest = i
                greatest_distance = distance
            elif greatest_distance < distance:
                greatest = i
                greatest_distance = distance
            elif greatest_distance == distance:

                previous_slice = space[:i, :]
                next_slice = space[i + 1:, :]
                candidate_less_space = np.vstack((previous_slice, next_slice))
                deviation1 = get_total_space_distance_std_deviation(candidate_less_space)

                previous_slice = space[:greatest, :]
                next_slice = space[greatest + 1:, :]
                candidate_less_space = np.vstack((previous_slice, next_slice))
                deviation2 = get_total_space_distance_std_deviation(candidate_less_space)

                if deviation1 < deviation2:
                    greatest = i
                    greatest_distance = distance

        discarted.append(space_with_core_id[greatest])
        space = np.delete(space, greatest, 0)
        space_with_core_id = np.delete(space_with_core_id, greatest, 0)

    discarted = np.vstack(discarted)
    # print(discarted)
    return space_with_core_id, discarted

def get_total_distante_other_nodes(node, nodes):

    print(np.sqrt((nodes -node)**2))

    return np.sum(np.sqrt((nodes - node) ** 2))

def get_total_space_distance(full_space: np.array):
    distances = []
    for i, candidate in enumerate(full_space):
        distances.append(np.sum(np.sqrt((full_space - candidate)**2)))


    # print(distances)

    return reduce(lambda x, y: x + y, distances) / len(distances)

def get_total_space_distance_std_deviation(full_space: np.array):
    distances = []
    for i, candidate in enumerate(full_space):
        distances.append(np.sum(np.sqrt((full_space - candidate)**2)))
    return np.std(distances)

def closest_two_nodes(full_space: np.array):

    closest_a = -1
    closest_b = -1
    closest_distance = -1

    for i, candidate in enumerate(full_space):

        previous_slice = full_space[:i, :]
        next_slice = full_space[i + 1:, :]
        candidate_less_space = np.vstack((previous_slice, next_slice))
        (node, distance) = closest_node(candidate, candidate_less_space)

        if node >= i:
            node += 1

        if closest_distance == -1:
            closest_a = i
            closest_b = node
            closest_distance = distance
        elif closest_distance > distance:
            closest_a = i
            closest_b = node
            closest_distance = distance

        # print(node, distance)

    return(closest_a, closest_b, closest_distance)

def closest_node(node, nodes):
    # nodes = np.asarray(nodes)
    # print((nodes - node)**2)
    # distance_vetor = np.sqrt(np.sum((nodes - node) ** 2, axis=1))
    distance_vetor = np.sum((nodes - node) ** 2, axis=1)
    # print(distance_vetor)
    # print(np.argmin(distance_vetor))

    return (np.argmin(distance_vetor), np.min(distance_vetor))

def average_std_deviation(full_space: np.array):
    average = []
    for i, candidate in enumerate(full_space):
        average.append(std_deviation_of_points_distances(candidate,full_space))
    return reduce(lambda x, y: x + y, average) / len(average)

def average_average_deviation(full_space: np.array):
    average = []
    for i, candidate in enumerate(full_space):
        average.append(average_of_points_distances(candidate,full_space))
    return reduce(lambda x, y: x + y, average) / len(average)

def std_deviation_of_points_distances(node, nodes):
    std_deviation = np.std(np.sum((nodes - node) ** 2, axis=1))
    return(std_deviation)

def average_of_points_distances(node, nodes):

    average = np.average(np.sqrt(np.sum((nodes - node) ** 2, axis=1)))
    return(average)

def fast_non_dominated_sort(full_space: np.array):

    frontier = np.array(full_space[0:1])
    no_core_id_frontier = frontier[:,1:]

    for candidate in full_space[1:,]:

        no_core_id_candidate = candidate[1:]
        partial_objective_domination = (no_core_id_candidate < no_core_id_frontier)
        dominated_indexes = partial_objective_domination.all(axis=1)

        try:
            dominated = np.vstack((dominated, frontier[dominated_indexes]))
        except UnboundLocalError:
            dominated = frontier[dominated_indexes]

        frontier = frontier[~dominated_indexes]
        no_core_id_frontier = no_core_id_frontier[~dominated_indexes]

        will_go = partial_objective_domination.any(axis=1).all()

        if will_go:
            frontier = np.vstack((frontier, candidate))
            no_core_id_frontier = np.vstack((no_core_id_frontier, no_core_id_candidate))
        else:
            dominated = np.vstack((dominated, candidate))

    return frontier,dominated











if __name__ == "__main__":
    import time
    data = get_data()

    # data = data[:, 1:]


    t0 = time.time()

    a = fast_non_dominated_sort(data)

    t1 = time.time()

    total = t1 - t0
    print(total)

    t0 = time.time()
    b = get_frontier(data)
    t1 = time.time()
    total = t1 - t0
    print(total)

    # print(np.isin(a[0],b[0]).all(), np.isin(a[1],b[1]).all())
    there = True

    for i in a[1][:,0:1]:
        if i in b[1][:,0:1]:
            pass
        else:
            print(i)
            there= False

    print(there)

    for i in b[0][:,0:1]:
        if i in a[0][:,0:1]:
            pass
        else:
            print(i)
            there= False

    print(there)


    # print(a)
    # print(b)

    # print(get_pareto_fittest(data, 9))
    # print(sumerize_frontier_with_id(data, 6))

    # print(get_pareto_fittest(data, 6))

    # data = np.array([[1,1,1],
    #                  [1,2,2],
    #                  [1,4,400],
    #                  [1,5,5]])

    # print(sumerize_frontier(data, 2))

    # sumerize_frontier(data, 2)


    # fittest, dominated = get_pareto_fittest(data, 5)
    #
    # print(fittest)
    #
    # print(dominated)



