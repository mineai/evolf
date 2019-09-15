## Import Libraries

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
from evolutionary_algorithms.servicecommon.parsers.parse_hocon \
    import ParseHocon
from evolutionary_algorithms.servicecommon.utils.list_utils \
            import ListUtils

import argparse
import random

# Build a Neucleotide Generation Function
# ascii_neucleotide = NeucleotideGenerationLibrary().ascii_neucleotide
def ascii_neucleotide():
    random_ascii = random.randint(32, 127)
    if random_ascii == 127:
        random_ascii = 10
    return chr(random_ascii)

# Evaluate Fitness
fitness_function = FitnessLibrary().character_matching_fitness_function
softtmax = MathUtils().softmax
def calc_fitness_probabilities(population, target):
    fitness = [fitness_function(candidate, target) for candidate in population]
    fitness_probabilities = softtmax(fitness)
    return fitness_probabilities

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This server is used to evolve strings")
    # The model name should not have .json
    parser.add_argument("--config",
            help="The Hocon Config file location")
    parser.add_argument("--target",
                        help="Location of the target file")

    args = parser.parse_args()

    # Read the Config File
    conf = ParseHocon().parse(args.config)
    evolution_specs = conf.get("evolution_specs")
    target_specs = conf.get("target_specs")

    # Parse and initialize variables
    population_size = evolution_specs.get("population_size")

    mating_pool_mutiplier = evolution_specs.get("mating_pool_mutiplier")
    number_parents = evolution_specs.get("num_parents")
    mutation_rate = evolution_specs.get("mutation_rate")
    elitism = evolution_specs.get("elitism")
    num_of_generations = evolution_specs.get("num_of_generations")

    parallelize = target_specs.get("paralellize")
    max_chunk_size = target_specs.get("max_chunk_size")
    # Get the target from the file path
    target = ListUtils().read_file(args.target)

    # Set up Functions for evolution


    # Mating pool
    # The function should have population and fitness as its first two arguments.
    # Even if they are not used. Here we use such one from our library of
    # mating pool generation functions.
    mating_pool_generator = SelectionFunctionsLibrary().default_mating_pool
    # Mating pool object has arguments population and fitness built in`
    # so no need to pass them explicitly.
    # The function we chose for mating_pool_generation has an argument mating_pool_mutiplier
    # apart from population and fitness that need to be passed in externally.
    mating_pool_args = mating_pool_mutiplier

    # Selection
    # The selection function should contain mating_pool as the first argument. Here
    # again we take one from our library.
    selection_parents_functions = SelectionFunctionsLibrary().natural_selection
    # Selection class has mating_pool argument built in so no need to pass it. And
    # our chosen function has an argument to tell it how many parents to select.
    selection_parents_functions_args = number_parents

    # The crossover function should contain parents as the first argument. Here
    # again we take one from our library.
    crossover_function = CrossoverFunctions().crossover_function_lists
    # Selection class has parents argument built in so no need to pass it. And
    # our chosen function accepts no other arguments
    crossover_function_args = None

    # The mutation function should contain neucleotide as the first argument. Here
    # again we take one from our library.
    mutation_function = MutationFunctions().mutate_list_with_ascii
    # Mutation object has argument neucleotide built in`
    # so no need to pass them explicitly.
    # The function we chose for mutation has an argument mutation_rate
    # apart from neucleotide that need to be passed in externally.
    mutation_function_args = mutation_rate

    # Set up Server for Evolving Lists
    evl = EvolveList(target=target,
                    initial_population=None,
                        population_size=population_size,
                        num_of_generations=num_of_generations,
                        elitism=elitism,
                        neucleotide_generator_function_and_args=[ascii_neucleotide,
                                                                None], # We have a Nnne
                                                                    # here as our ascii_neucleotide


                        fitness_functions=calc_fitness_probabilities,
                        mating_pool_function_and_args=[mating_pool_generator,
                                                    mating_pool_args],
                        selection_function_and_args=[selection_parents_functions,
                                                    selection_parents_functions_args],
                        crossover_function_and_args=[crossover_function,
                                                    crossover_function_args],
                        mutation_function_and_args=[mutation_function, mutation_function_args],
                        fitness_recombination_method=None)
    # Evolve
    # Single Core
    if not parallelize:
        import time
        start_time = time.time()
        evolved_candidate = evl.evolve(target)
        # Tet the time taken for evolution
        elapsed_time = time.time() - start_time
        print("Final Evolved Canidate:", evolved_candidate)
        print("Time Taken to evolve: ", elapsed_time/60, " mins" )
    else:
        #Multi Core
        evl.evolve_parallel(max_chunk_size=max_chunk_size)
