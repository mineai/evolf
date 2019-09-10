# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 21:14:52 2019

@author: alexa
"""

from population import Population
from evolution_function_lib import EvolutionFunctionLib 
from gene import Gene

pop = Population(100, 0.1, "Unicorn")
population = pop.initialize_population(pop.pop_size, pop.gene_length,
                                        pop.dna)
fitness = pop.calculate_fitness(population, pop.target, pop.dna)
a = pop.get_best_fitness_candidate(population, fitness)
#fitness = pop.calculate_fitness(population, pop.target, pop.dna)
#print(pop.get_best_fitness_candidate(population, fitness))

EFL = EvolutionFunctionLib()
G = Gene()
b = EFL.default_mutation_function("Unicorn poops rainbow", 0.2, G)
print("".join(b))