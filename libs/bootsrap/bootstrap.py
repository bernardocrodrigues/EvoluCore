
import numpy as np
import libs.coreFactory.coreFactory as cf

class bootstrap():

    @staticmethod
    def bootstrap_traits(traits, percent=0.1):

        # traits = np.array(traits)

        size = traits.shape[0]
        resample_size = int(size*percent)

        indexes_to_remove = np.random.randint(size, size=resample_size)
        indexes = [True]*size

        for idx in indexes_to_remove:
            indexes[idx] = False

        traits = traits[indexes]
        resample = cf.factory.generate_random_cores(resample_size)

        return traits, resample

    @staticmethod
    def bootstrap(traits, objectives, percent=0.1):

        # traits = np.array(traits)

        size = traits.shape[0]
        resample_size = int(size*percent)

        indexes_to_remove = np.random.randint(size, size=resample_size)
        indexes = [True]*size

        for idx in indexes_to_remove:
            indexes[idx] = False

        traits = traits[indexes]
        objectives = objectives[indexes]
        resample = cf.factory.generate_random_cores(resample_size)

        return traits, objectives, resample

if __name__ == '__main__':

    import libs.librarian.librarian as l
    # import libs.paretoFrontier.paretoFrontier as pf
    # lib = l.librarian_nsga()
    lib2 = l.librarian_milenium()

    teste = lib2.get_benchmark_data(limit=20)

    traits = teste[:,:12]
    objectives = teste[:,12:]

    new_traits, resample = bootstrap.bootstrap_traits(traits)

    # print(new_traits, resample)

    new_traits, new_objectives, resample = bootstrap.bootstrap(traits, objectives)

    # print(new_traits.shape, new_objectives.shape, resample)


