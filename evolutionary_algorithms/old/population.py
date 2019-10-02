import random
import numpy as np

class Population():
    """
    This class acts as interface that can be inherited to generate the population.
    """
    def __init__(self, pop_size, mutation_rate, target, **kwargs):
        """
        Override the constructor of this class to properly inherit.

        NOTE: Appropriate DNA Class object should be overriden
        and initialized to self.dna
        Appropraite EcolutionUtils class should be inherited and initialized
        to self.utils

        :param pop_size: Size of the population
        :param mutation_rate: The rate of mutation normalized within 0-1
        :param target: A list containg the target DNA.
        :param **kwargs: A ditionary containig other information, mainly
        external functions to be overriden

        :returns nothing
        """
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.target = target
        self.dna_dimensions = len(self.target)
        self.external_functions = self.build_kwargs_for_external_functions(kwargs)



    def build_kwargs_for_external_functions(self, kwargs):
        """
        This function initializes external functions to
        override defaults.
        :param kwargs: Dictionary contianing the functions

        :returns functions: Returns the functions that can be overriden
        """
        functions_possible = ["fitness_function", "crosover_function",
                                "mutation_function"]

        functions = {}
        for key, item in kwargs.items():
            if key in functions_possible:
                functions[key] = item

        return functions

    def initialize_population(self, pop_size, dna_dimensions, dna_obj):
        """
        This function initializes the first generation of candidates.
        :param pop_size: Size of the population
        :param dna_dimensions: Length of Each DNA
        ::param dna_obj: Object of the DNA Class.

        :returns population: A list caontaining all the candidates of the
        population.
        """
        population = []
        for candidate_num in range(pop_size):
            candidate = dna_obj.generate_dna(dna_dimensions, dna_obj.gene_generator)
            population.append(candidate)
        return population

    def calculate_fitness(self, population, target, dna_obj):
        """
        This function calcuates the fitness of each candidate of
        the population and squishes the into probability values
        using softmax.
        :param population: A list caontaining all the candidates of the
        population
        :param target: A list containg the target DNA.
        :param dna_obj: Object of the DNA Class.

        :returns fitness_prob: A list containing the fitness probibilites
        of the population
        """
        fitness_array = [dna_obj.get_fitness(candidate, target) \
                        for candidate in population]
        fitness_prob = self.utils.softmax(fitness_array)
        return fitness_prob

    def generate_mating_pool(self, population, fitness_prob,
                            mating_pool_mutiplier):
        """
        This function generates the mating pool from the population
        based on their fitness.
        :param population: A list caontaining all the candidates of the
        population
        :param fitness_prob: A list containing the fitness of the candidates
        of the populaiton
        :param mating_pool_mutiplier: This scales the mating pool size

        :returns mating_pool: List contiaing all the candidates chosen for
        mating.
        """
        fitness_prob = [fitness_of_candidate*mating_pool_mutiplier \
                        for fitness_of_candidate in fitness_prob]
        mating_pool = self.utils.copy_elements(population, fitness_prob)
        if not len(mating_pool):
              mating_pool = population
        return mating_pool

    def get_best_fitness_candidate(self, population, fitness_prob):
        """
        This function returns the best candidate of the population.
        :param population: A list containing the population.
        :param fitness_prob: A list containing the fitness of the population

        :returns best_candidate: The candidate with the highest fitness
        """
        fitness_probs = np.array(fitness_prob)
        max_fitness_element = np.argmax(fitness_probs)

        best_candidate = {fitness_prob[max_fitness_element]: population[max_fitness_element]}
        return best_candidate

    def natural_selection(self, num_parents, mating_pool):
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
