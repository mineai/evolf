from evolf.elements.tree.tree \
    import Tree
import numpy as np

from string_evolve.reproduction.selection.selection_functions_library \
    import SelectionFunctionsLibrary

class Population:
    def __init__(self, min_height=3, max_height=10, population_size=25,
                 num_parents=2, mating_pool_multiplier=100,
                 initial_population=None, search_space_obj=None):
        self.population_size = population_size
        self.num_parents = num_parents
        self.mating_pool_multiplier = mating_pool_multiplier
        self.symbolic_expressions = []  # Cache to generate unique expressions
        self.mating_pool = None
        self.elites = None
        self.search_space_obj = search_space_obj
        self.trees = []

        if initial_population is None:
            self.min_height = min_height
            self.max_height = max_height
            self.generate_population()
        else:
            tree_heights = []
            for tree in initial_population:
                if tree.symbolic_expression not in self.symbolic_expressions:
                    tree_heights.append(tree.height)
                    self.symbolic_expressions.append(tree.symbolic_expression)
                    self.trees.append(tree)
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
            tree = Tree(self.min_height, self.max_height, self.search_space_obj)
            if tree.symbolic_expression in self.symbolic_expressions:
                continue
            self.symbolic_expressions.append(tree.symbolic_expression)
            if tree.working:
                self.trees.append(tree)
                print(f"Trees Initialized {len(self.trees)} / {self.population_size}: {tree.symbolic_expression}")


    def get_best_fitness_candidate(self):
        fitness = self.get_fitness_array()
        best_candidate_index = np.argmax(fitness)
        best_candidate = self.trees[best_candidate_index]

        return best_candidate

    def get_fitness_array(self):
        fitness = []
        for tree in self.trees:
            fitness.append(tree.fitness)
        return fitness

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
        fitness = self.get_fitness_array()
        self.mating_pool = SelectionFunctionsLibrary.default_mating_pool(
            self.trees, fitness, self.mating_pool_multiplier)

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

    def get_average_fitness(self):
        fitness = self.get_fitness_array()
        average_fitness = np.mean(fitness)
        return average_fitness