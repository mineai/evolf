from dna import DNA
from evolution_utils import EvolutionUtils

import numpy as np

class Population():

    def __init__(self, pop_size, mutation_rate, target, **kwargs):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.target = target
        self.gene_length = len(self.target)
        external_functions = self.build_kwargs_for_external_functions(kwargs)
        self.dna = DNA(self.gene_length, self.mutation_rate,
                    **external_functions)
        self.utils = EvolutionUtils()


    def build_kwargs_for_external_functions(self, kwargs):
        functions_possible = ["fitness_function", "crosover_function",
                                "mutation_function"]

        functions = {}
        for key, items in kwargs.items():
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

    def generate_mating_pool(self, population, fitness_prob):
        return pop.utils.copy_elements(population, fitness_prob)

    def get_best_fitness_candidate(self, population, fitness_prob):
        fitness_probs = np.array(fitness_prob)
        max_fitness_element = np.argmax(fitness_probs)
        return {fitness_prob[max_fitness_element]: population[max_fitness_element]}



pop = Population(10, 0.1, "Unicorn")
population = pop.initialize_population(pop.pop_size, pop.gene_length,
                                        pop.dna)
fitness = pop.calculate_fitness(population, pop.target, pop.dna)
print(pop.get_best_fitness_candidate(population, fitness))
