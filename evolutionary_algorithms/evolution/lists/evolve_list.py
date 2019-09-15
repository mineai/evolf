# Import Libs
from evolutionary_algorithms.evolution.lists.candidate_list \
            import CandidateList
from evolutionary_algorithms.elements.population.population \
            import Population
from evolutionary_algorithms.evaluation.fitness.fitness_objectives \
            import FitnessObjectives
from evolutionary_algorithms.reproduction.selection.selection import Selection
from evolutionary_algorithms.reproduction.selection.mating_pool \
            import MatingPool
from evolutionary_algorithms.reproduction.crossover.crossover \
            import Crossover
from evolutionary_algorithms.reproduction.mutation.mutation \
            import Mutation

from evolutionary_algorithms.evaluation.fitness.fitness_library \
            import FitnessLibrary
from evolutionary_algorithms.servicecommon.utils.list_utils \
            import ListUtils

import math
from tqdm import trange
from multiprocessing import Process, current_process, Manager, Pool

class EvolveList():
    def __init__(self, target,
                        initial_population=None,
                        population_size=10,
                        num_of_generations=10000,
                        elitism=0.1,
                        neucleotide_generator_function_and_args=None,
                        fitness_functions=None,
                        mating_pool_function_and_args=None,
                        selection_function_and_args=None,
                        crossover_function_and_args=None, mutation_function_and_args=None,
                        fitness_recombination_method=None):


        self.initial_population = initial_population
        self.population_size = population_size
        self.num_of_generations = num_of_generations
        self.target = target
        self.elitism = elitism


        self.candidate_length = len(self.target)
        self.neucleotide_generator_function = neucleotide_generator_function_and_args[0]
        self.neucleotide_generator_function_args = neucleotide_generator_function_and_args[1]
        self.fitness_functions = fitness_functions
        self.mating_pool_function = mating_pool_function_and_args[0]
        self.mating_pool_function_args = mating_pool_function_and_args[1]
        self.selection_function = selection_function_and_args[0]
        self.selection_function_args = selection_function_and_args[1]
        self.crossover_function = crossover_function_and_args[0]
        self.crossover_function_and_args = crossover_function_and_args[1]
        self.mutation_function = mutation_function_and_args[0]
        self.mutation_function_and_args = mutation_function_and_args[1]
        self.fitness_recombination_method = fitness_recombination_method

    def initialize_functions(self, neucleotide_generator_function_and_args=None,
                            fitness_functions_and_args=None,
                            mating_pool_function_and_args=None,
                            selection_function_and_args=None,
                            crossover_function_and_args=None,
                            mutation_function_and_args=None,
                            fitness_recombination_method=None):
        self.neucleotide_generator_function,
        self.neucleotide_generator_function_args = neucleotide_generator_function_and_args
        self.fitness_functions = fitness_functions
        self.mating_pool_function, self.mating_pool_function_args = mating_pool_function_and_args
        self.selection_function, self.selection_function_args = selection_function_and_args
        self.crossover_function, self.crossover_function_and_args = crossover_function_and_args
        self.mutation_function, self.mutation_function_and_args = mutation_function_and_args
        self.fitness_recombination_method = fitness_recombination_method

    def evolve(self, target):

        # Generate A candidate Object
        candidate_list_obj = CandidateList(self.candidate_length, self.neucleotide_generator_function)
        # Create a Population
        if not self.initial_population:
            p = Population(self.population_size, candidate_list_obj)
            p.generate_population()
            population = p.get_population_decoded()
        else:
            population = self.initial_population

        best_fitness_canddidate_extractor = FitnessLibrary.get_best_fitness_candidate

        elites = []
        elites_to_keep = math.floor(self.population_size * self.elitism)

        # For all the generations
        for generation in trange(self.num_of_generations):
            # Retain elites
            population[:elites_to_keep] = elites

            # Evaluate Fintess objectives
            fitness_objectives_object = FitnessObjectives(self.fitness_functions,
                                    [population, target])
            fitness_from_objectives = fitness_objectives_object.execute_all_fitness( \
                                        self.fitness_functions,
                                        [population, target])

            fitness = fitness_objectives_object.get_recombined_fitness(self.fitness_recombination_method)

            best_candidate = best_fitness_canddidate_extractor(population, fitness)

            # print("Genration ", generation)

            best_candidate = best_candidate[list(best_candidate)[0]]
            # print("Best Candidate: ", "".join(best_candidate))

            # Sort the values in descending order
            population_desc = ListUtils().sort_lists(population, fitness)
            elites = population_desc[:elites_to_keep]

            # Generate Mating Pool
            mating_pool_obj = MatingPool(self.mating_pool_function, self.mating_pool_function_args)
            mating_pool = mating_pool_obj.generate_mating_pool(population,
                                                            fitness)

            children = []
            # Select Parents
            for parent_idx in range(self.population_size):
                selection = Selection(mating_pool, self.selection_function,
                                                self.selection_function_args)
                parents = selection.select_parents()
                crossover_obj = Crossover(parents,
                                            self.crossover_function,
                                            self.crossover_function_and_args)


                child = crossover_obj.crossover()
                mutation = Mutation(child, self.mutation_function,
                                    self.mutation_function_and_args)
                mutated_child = mutation.mutate()
                children.append(child)

            population = children

            if target == best_candidate:
                break

        return best_candidate

    def evolve_parallel_using_single(self, args):
        target, queue = args
        best_candidate = self.evolve(target)
        queue.put(target)

        return best_candidate

    def evolve_parallel(self, max_chunk_size):
        import time
        start_time = time.time()
        target_chunks = ListUtils().block_list(self.target, max_chunk_size)
        print(target_chunks)

        # Start Multicore Processing
        pool = Pool()
        manager = Manager()
        queue = manager.Queue()

        # Generate args such that there is a queue for each target
        args = [(target, queue) for target in target_chunks]

        # Asynchronously map the function and the args to the pool
        evolved_chunks = pool.map_async(self.evolve_parallel_using_single, args)
        # Close the pool
        pool.close()

        while not evolved_chunks.ready():
            pass

        # Once All jobs have finished, get the result
        evolved_chunks = evolved_chunks.get()

        # Tet the time taken for evolution
        elapsed_time = time.time() - start_time

        #Recombine the Chunks
        if isinstance(evolved_chunks[0], list):
            for chunk_idx, chunk in enumerate(evolved_chunks):
                evolved_chunks[chunk_idx] = "".join(chunk)

        evolved_candidate = "".join(evolved_chunks)

        print("Final Evolved Canidate:", evolved_candidate)
        print("Time Taken to evolve: ", elapsed_time/60, " mins" )
