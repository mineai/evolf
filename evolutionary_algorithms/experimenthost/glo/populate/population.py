from evolutionary_algorithms.experimenthost.glo.elements.tree.tree \
    import Tree
import numpy as np

from evolutionary_algorithms.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary
from evolutionary_algorithms.servicecommon.utils.math_utils \
    import MathUtils


class Population:
    def __init__(self, min_height=3, max_height=10, population_size=25,
                 num_parents=2, mating_pool_multiplier=100,
                 initial_population=None):
        self.population_size = population_size
        self.num_parents = num_parents
        self.mating_pool_multiplier = mating_pool_multiplier
        self.working_trees = []  # These are the trees filtered out after symbolic expressions have been created
        self.trainable_trees = []  # These are the trees that were actually trainable on the evaluator
        self.trainable_trees_fitness = []  # Thus contains the fitness of the trainable trees
        self.symbolic_experssions = []  # Cache to generate unique expressions
        self.mating_pool = None

        if initial_population is None:
            self.min_height = min_height
            self.max_height = max_height
            self.trees = []
            self.generate_population()
        else:
            self.trees = initial_population
            tree_heights = []
            for tree in self.trees:
                tree_heights.append(tree.height)
                tree.symbolic_expression.append(tree.symbolic_expression)
            self.population_size = len(self.trees)
            self.min_height = min(tree_heights)
            self.max_height = max(tree_heights)

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
        print("\n\nGenerating Tress ...")
        while len(self.trees) < self.population_size:

            tree = Tree(self.min_height, self.max_height)
            if tree.symbolic_expression in self.symbolic_experssions:
                continue
            self.trees.append(tree)
            self.symbolic_experssions.append(tree.symbolic_expression)

        self.get_working_trees()

    def get_working_trees(self):
        """
        This function collects all the trees that are working and
        stores them in self.working_trees.
        :return nothing:
        """
        print("Extracting Working Tress ... \n\n")
        for tree_idx in range(len(self.trees)):
            tree = self.trees[tree_idx]
            if tree.symbolic_expression is None:
                tree.construct_symbolic_expression()
            if tree.working is None:
                tree.validate_working()

            if tree.working:
                self.working_trees.append(tree)

    def initialize_trainable_tree_fitness(self):
        self.trainable_trees_fitness = []
        for tree in self.trainable_trees:
            self.trainable_trees_fitness.append(tree.fitness)

    def get_best_fitness_candidate(self):
        if not len(self.trainable_trees):
            print("Trees have not yet been trained or no Trained Trees Exist")
        else:
            best_candidate_index = np.argmax(self.trainable_trees_fitness)
            best_candidate = self.trainable_trees[best_candidate_index]
            return best_candidate

    def generate_mating_pool(self):
        """

        A static method

        Arguments: trees: A list of trees.

                   mating_pool_multiplier: An integer that will be used to make multiple
                   copies of each tree depending on their individual fitness probability.

        Returns: mating_pool: The larger mating pool that reflects individual trees' fitness 
                 probability along with the mating_pool_multiplier.

                 fitness_probs: The list of fitness probabilities for each tree from the original
                 trees list.

        """
        if not len(self.trainable_trees_fitness):
            self.trainable_trees_fitness = []
            for tree in self.trainable_trees:
                self.trainable_trees_fitness.append(tree.fitness)

        fitness_probs = MathUtils.softmax(self.trainable_trees_fitness)
        self.mating_pool = SelectionFunctionsLibrary.default_mating_pool(
            self.trainable_trees, fitness_probs, self.mating_pool_multiplier)

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
