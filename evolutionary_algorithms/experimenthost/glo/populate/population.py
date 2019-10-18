from evolutionary_algorithms.experimenthost.glo.elements.tree.tree \
    import Tree
from tqdm import trange

from evolutionary_algorithms.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary
from evolutionary_algorithms.servicecommon.utils.math_utils \
    import MathUtils


class Population:
    def __init__(self, min_height=3, max_height=10, population_size=25,
                 num_parents=2, mating_pool_multiplier=100):
        self.min_height = min_height
        self.max_height = max_height
        self.population_size = population_size
        self.num_parents = num_parents

        self.trees = []
        self.working_trees = []
        self.mating_pool = None
        self.mating_pool_multiplier = mating_pool_multiplier

    def generate_population(self):
        """

        This function uses the class variable population_size that 
        will specify the size of the list of trees that the function 
        will generate. It appends a specified number of Tree() objects 
        to tree_list then iterates through them again to create the 
        populated trees. The function then returns that list.

        arguments: Nothing
        returns: Nothing

        """
        print("\n\n ######### Generating Tress ######### \n\n")
        while len(self.trees) < self.population_size:
            self.trees.append(Tree(self.min_height, self.max_height))

        self.get_working_trees()

    def get_working_trees(self):
        """
        This function collects all the trees that are working and
        stores them in self.working_trees.
        :return nothing:
        """
        print("\n\n ######### Extracting Working Tress ######### \n\n")
        for tree_idx in trange(len(self.trees)):
            tree = self.trees[tree_idx]
            if tree.symbolic_expression is None:
                tree.construct_symbolic_expression()
            if tree.working is None:
                tree.validate_working()

            if tree.working:
                self.working_trees.append(tree)

    def generate_mating_pool(self):
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
        for tree in self.trees:
            fitness.append(tree.fitness)
        fitness_probs = MathUtils.softmax(fitness)
        self.mating_pool = SelectionFunctionsLibrary.default_mating_pool(
            self.trees, fitness_probs, self.mating_pool_multiplier)

    def natural_selection(self):
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
        parents = SelectionFunctionsLibrary().natural_selection(
            self.mating_pool, self.num_parents)
        return parents
