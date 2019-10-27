class SelectionFunctionsLibrary():
    """
    This class contains a library of functions for
    mating pool generation and selection.

    Newer functions can be added here.
    """

    @staticmethod
    def default_mating_pool(population, fitness_prob,
                            mating_pool_mutiplier):
        """
        This function generates the mating pool from the population
        based on their fitness.
        :param population: A list caontaining all the candidates of the
        population
        :param fitness_prob: A list containing the fitness probabilities
        of the candidates of the populaiton
        :param mating_pool_mutiplier: This scales the mating pool size

        :returns mating_pool: List contiaing all the candidates chosen for
        mating.
        """
        from evolutionary_algorithms.servicecommon.utils.list_utils \
                        import ListUtils
        fitness_prob = [fitness_of_candidate*mating_pool_mutiplier \
                        for fitness_of_candidate in fitness_prob]
        mating_pool = ListUtils.copy_elements(population, fitness_prob)
        if not len(mating_pool):
              mating_pool = population
        import random
        random.shuffle(mating_pool)
        return mating_pool

    @staticmethod
    def natural_selection(mating_pool, num_parents):
        import random
        """
        This function returns parents selected from the mating pool
        by sampling from it uniformly. It is assumed the mating pool
        has been approporiately scaled based on the fitness.
        :param num_parents: Integer that represents how many parents to
        return
        :param mating_pool: List containing the candidates chosen from
        reproduction appropriately scaled

        :returns parents: Number of parents chosen for reproduction from the
        mating pool
        """
        parents = []
        size_of_mating_pool = len(mating_pool)
        for parent_num in range(num_parents):
            parent = random.randint(0, size_of_mating_pool-1)
            parents.append(mating_pool[parent])
        return parents
