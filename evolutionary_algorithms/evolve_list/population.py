import random
from evolutionary_algorithms.evolve_list.dna_list import DNAList
from evolutionary_algorithms.evolve_list.evolution_list_utils import EvolutionListUtils

import numpy as np

class Population():

    def __init__(self, pop_size, mutation_rate, target, **kwargs):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.target = target
        self.gene_length = len(self.target)
        external_functions = self.build_kwargs_for_external_functions(kwargs)
        self.dna = DNAList(self.gene_length, self.mutation_rate,
                    **external_functions)

        self.utils = EvolutionListUtils()


    def build_kwargs_for_external_functions(self, kwargs):
        functions_possible = ["fitness_function", "crosover_function",
                                "mutation_function"]

        functions = {}
        for key, item in kwargs.items():
            if key in functions_possible:
                functions[key] = item

        return functions

    def initialize_population(self, pop_size, gene_length, dna_obj):
        population = []
        for candidate_num in range(pop_size):
            candidate = dna_obj.generate_dna(gene_length, dna_obj.gene_generator)
            population.append(candidate)
        return population

    def calculate_fitness(self, population, target, dna_obj):
        fitness_array = [dna_obj.get_fitness(candidate, target) \
                        for candidate in population]
        fitness_prob = self.utils.softmax(fitness_array)
        return fitness_prob

    def generate_mating_pool(self, population, fitness_prob,
                            mating_pool_mutiplier):
        fitness_prob = [fitness_of_candidate*mating_pool_mutiplier \
                        for fitness_of_candidate in fitness_prob]
        mating_pool = self.utils.copy_elements(population, fitness_prob)
        if not len(mating_pool):
              mating_pool = population
        return mating_pool

    def get_best_fitness_candidate(self, population, fitness_prob):
        fitness_probs = np.array(fitness_prob)
        max_fitness_element = np.argmax(fitness_probs)
        return {fitness_prob[max_fitness_element]: population[max_fitness_element]}

    def natural_selection(self, num_parents, mating_pool):
        parents = []
        size_of_mating_pool = len(mating_pool)
        for parent_num in range(num_parents):
            parent = random.randint(0, size_of_mating_pool-1)
            parents.append(mating_pool[parent])
        return parents
