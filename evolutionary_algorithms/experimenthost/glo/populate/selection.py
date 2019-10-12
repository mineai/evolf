from evolutionary_algorithms.reproduction.selection.selection_functions_library import SelectionFunctionsLibrary
from evolutionary_algorithms.servicecommon.utils.math_utils import MathUtils


class Selection:
    """

    Multiline Comment Stuff

    """
    @staticmethod
    def generate_mating_pool(trees, mating_pool_multiplier):

            fitness = []
            for tree in trees:
                fitness.append(tree.fitness)
            fitness_probs = MathUtils.softmax(fitness)
            mating_pool = SelectionFunctionsLibrary.default_mating_pool(
                trees, fitness_probs, mating_pool_multiplier)

            return mating_pool, fitness_probs
