from evolutionary_algorithms.experimenthost.glo.elements.tree \
    import Tree
from evolutionary_algorithms.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary
from evolutionary_algorithms.servicecommon.utils.math_utils \
    import MathUtils


class Population:
    def __init__(self, min_height=3, max_height=10, population_size=25, parents_size=2):
        self.min_height = min_height
        self.max_height = max_height
        self.population_size = population_size
        self.parents_size = parents_size

        self.trees = []
        self.working_trees = []
        self.mating_pool = None

    def generate_trees(self):
        """

        This function uses the class variable population_size that 
        will specify the size of the list of trees that the function 
        will generate. It appends a specified number of Tree() objects 
        to tree_list then iterates through them again to create the 
        populated trees. The function then returns that list.

        arguments: Nothing
        returns: tree_list (list of Tree() objects)

        """

        while len(self.trees) < self.population_size:
            self.trees.append(Tree(self.min_height, self.max_height))

        for tree in self.trees:
            token = tree.request_token()
            tree.root = tree.helper_function(token)

    def get_working_trees(self):

        for tree in self.trees:
            if tree.symbolic_expression is None:
                tree.construct_symbolic_expression()
            if tree.working is None:
                tree.validate_working()

            if tree.working:
                self.working_trees.append(tree)

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

    def natural_selection(self, func_mating_pool=None, num_parents=None):
        """

        This function is used to access a function with the same name in the file
        selection_functions_library.py

        Arguments: func_mating_pool: A list of trees that have been chosen to be
                   more fit than other trees.

                   num_parents: An integer that will specify how many parents will
                   be selected from the mating pool.

        Returns: parents: A list of randomly selected trees from the mating pool
                 with the size of num_parents.

        """
        if num_parents is None:
            num_parents = parents_size

        if func_mating_pool is None:
            func_mating_pool = mating_pool

        parents = SelectionFunctionsLibrary().natural_selection(
            func_mating_pool, num_parents)

        return parents
