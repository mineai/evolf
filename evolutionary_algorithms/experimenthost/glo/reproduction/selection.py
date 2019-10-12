from evolutionary_algorithms.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary
from evolutionary_algorithms.servicecommon.utils.math_utils \
    import MathUtils


class Selection:
    """

    Class Description

    """
    @staticmethod
    def generate_mating_pool(trees, mating_pool_multiplier):
        """

        A static method

        Arguments: trees: A list of trees.

                   mating_pool_multiplier: An integer that will be used to make multiple
                   copies of each tree depending on their individual fitness probability.

        Returns: mating_pool: The larger mating pool that reflects individual trees' fitness 
                 probability along with the mating_pool_multiplier.

                 fitnes_probs: The list of fitness probablities for each tree from the original
                 trees list.

        """

        fitness = []
        for tree in trees:
            fitness.append(tree.fitness)
        fitness_probs = MathUtils.softmax(fitness)
        mating_pool = SelectionFunctionsLibrary.default_mating_pool(
            trees, fitness_probs, mating_pool_multiplier)

        return mating_pool, fitness_probs

    def natural_selection(self, mating_pool, num_of_parents):
        pass
