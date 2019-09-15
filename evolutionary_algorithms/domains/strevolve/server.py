from evolutionary_algorithms.elements.neucleotide.neucleotide_generation_library \
            import NeucleotideGenerationLibrary
from evolutionary_algorithms.evaluation.fitness.fitness_library \
            import FitnessLibrary

from evolutionary_algorithms.servicecommon.utils.math_utils import MathUtils
from evolutionary_algorithms.reproduction.selection.selection_functions_library \
            import SelectionFunctionsLibrary
from evolutionary_algorithms.reproduction.crossover.crossover_functions \
            import CrossoverFunctions
from evolutionary_algorithms.reproduction.mutation.mutation_functions \
            import MutationFunctions

from evolutionary_algorithms.evolution.lists.evolve_list \
            import EvolveList

class erver

# Build a Neucleotide Generation Function
neucleotide_gen_func = NeucleotideGenerationLibrary().ascii_neucleotide

# Set the Target
target = list("Its Kwaffee and not Coffee")

# Evaluate Fitness
fitness_function = FitnessLibrary().character_matching_fitness_function
softtmax = MathUtils().softmax
def calc_fitness_probabilities(population, target):
    fitness = [fitness_function(candidate, target) for candidate in population]
    fitness_probabilities = softtmax(fitness)

    return fitness_probabilities

# Generate a mating pool
mating_pool_generator = SelectionFunctionsLibrary().default_mating_pool
mating_pool_mutiplier = 100
selection_parents_functions = SelectionFunctionsLibrary().natural_selection
number_parents = 2
crossover_function = CrossoverFunctions().crossover_function_lists
mutation_function = MutationFunctions().mutate_list_with_ascii
mutation_rate = 0.1

evl = EvolveList(target,
                    None,
                    100,
                    0.1,
                    [neucleotide_gen_func, None],
                    calc_fitness_probabilities,
                    [mating_pool_generator, mating_pool_mutiplier],
                    [selection_parents_functions, 2],
                    [crossover_function, None],
                    [mutation_function, mutation_rate],
                    None)
evl.evolve()
