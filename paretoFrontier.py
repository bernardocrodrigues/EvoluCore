import sqlite3
import numpy as np
from functools import reduce

def get_data():
    conn = sqlite3.connect('/home/bcrodrigues/Dropbox/tcc/script/millenium.db', isolation_level='EXCLUSIVE')
    cur = conn.cursor()
    return np.array(cur.execute("select id_core, adpcm, alm from core").fetchmany(10))

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
                # print('vai tirar alguem')
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
        space = dominated

    return frontiers, space

def get_pareto_fittest(full_space: np.array, num: int):
    fittest, space = get_frontier(full_space)
    while fittest.shape[0] < num:
        frontier, dominated = get_frontier(space)

        if (fittest.shape[0] + fittest.shape[0]) > num:
            print('tem q podar')
        else:
            fittest = np.vstack((fittest,frontier))
            space = dominated

    return fittest, space

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

        # print(get_total_space_distance(candidate_less_space))
        # print(get_total_space_distance_std_deviation(candidate_less_space))
        # print('\n')

    # for i, candidate in enumerate(full_space):
    #     previous_slice = full_space[:i, :]
    #     next_slice = full_space[i + 1:, :]
    #     candidate_less_space = np.vstack((previous_slice, next_slice))
    #
    #     media = []
    #     for i2, candidate2 in enumerate(candidate_less_space):
    #         media.append(get_total_distante_other_nodes(candidate2,candidate_less_space))
    #
    #     print(media)

        # print(candidate_less_space)
        #
        # print(average_average_deviation(candidate_less_space), '\n')

        # print(get_total_distante_other_nodes(candidate, candidate_less_space))

    # print(average_std_deviation(full_space))
    #
    # for i, candidate in enumerate(full_space):
    #     previous_slice = full_space[:i, :]
    #     next_slice = full_space[i + 1:, :]
    #     candidate_less_space = np.vstack((previous_slice, next_slice))
    #     print(average_average_deviation(candidate_less_space), average_std_deviation(candidate_less_space))
    #     # print(average_std_deviation(candidate_less_space))

def get_total_distante_other_nodes(node, nodes):

    print(np.sqrt((nodes -node)**2))

    return np.sum(np.sqrt((nodes - node) ** 2))

def get_total_space_distance(full_space: np.array):
    distances = []
    for i, candidate in enumerate(full_space):
        distances.append(np.sum(np.sqrt((full_space - candidate)**2)))


    print(distances)

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





# data = get_data()

data = np.array([[1,1,1],
                 [1,2,2],
                 [1,4,400],
                 [1,5,5]])

# print(sumerize_frontier(data, 2))

sumerize_frontier(data, 2)

exit()


# fittest, dominated = get_pareto_fittest(data, 5)
#
# print(fittest)
#
# print(dominated)



